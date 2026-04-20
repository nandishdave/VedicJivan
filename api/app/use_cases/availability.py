"""Availability use cases — application workflows for slots, unavailability,
business-hours and report-section settings.

Use cases:
  - GetAvailableSlots
  - ListUnavailabilityForDate / ForRange
  - ListHolidaysInRange
  - AddUnavailability
  - RemoveUnavailability
  - GetBusinessHours / UpdateBusinessHours
  - GetReportSections / UpdateReportSections

The router translates HTTP -> use case -> response. Domain rules
(holiday-already-marked, start-before-end, missing times, invalid
timezone) raise BookingValidationError -> 400 via the shared handler.
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from app.domain.exceptions import (
    BookingValidationError,
    EntityNotFoundError,
)
from app.models.availability import (
    AvailableSlot,
    BusinessHoursSettings,
    DayHours,
    DEFAULT_REPORT_SECTIONS,
    ReportSection,
    UnavailabilityCreate,
)
from app.repositories.booking_repository import BookingRepository
from app.repositories.settings_repository import SettingsRepository
from app.repositories.unavailability_repository import UnavailabilityRepository
from app.services.slot_generator import generate_30min_slots
from app.utils.time_helpers import ranges_overlap, time_to_minutes


# ── Helper: load business-hours model from settings repo ─────────────────


_DEFAULT_BUSINESS_HOURS = BusinessHoursSettings()


async def _load_business_hours(repo: SettingsRepository) -> BusinessHoursSettings:
    doc = await repo.get_business_hours_doc()
    if not doc:
        return _DEFAULT_BUSINESS_HOURS
    return BusinessHoursSettings(
        timezone=doc.get("timezone", "Asia/Kolkata"),
        weekly_hours=[DayHours(**d) for d in doc.get("weekly_hours", [])],
    )


# ── GetAvailableSlots ────────────────────────────────────────────────────


class GetAvailableSlots:
    """Return bookable 30-min slots for a date.

    Filters out: closed days, full-day holidays, admin time blocks, existing
    confirmed/pending bookings, and (if today) past slots.
    """

    def __init__(
        self,
        unavailability_repo: UnavailabilityRepository,
        booking_repo: BookingRepository,
        settings_repo: SettingsRepository,
    ) -> None:
        self._unavail = unavailability_repo
        self._bookings = booking_repo
        self._settings = settings_repo

    async def execute(self, date_str: str) -> list[AvailableSlot]:
        # Calendar validity (regex on the route only checks shape)
        try:
            requested_date = date.fromisoformat(date_str)
        except ValueError:
            raise BookingValidationError(f"Invalid date: {date_str}")

        bh = await _load_business_hours(self._settings)
        day_of_week = requested_date.weekday()
        day_config = next(
            (d for d in bh.weekly_hours if d.day == day_of_week), None
        )
        if not day_config or not day_config.is_open:
            return []

        if await self._unavail.find_holiday(date_str):
            return []

        block_docs = await self._unavail.list_blocks_for_date(date_str)
        unavailable: list[tuple[str, str]] = [
            (b["start_time"], b["end_time"])
            for b in block_docs
            if b.get("start_time") and b.get("end_time")
        ]

        booking_docs = await self._bookings.find_active_on_date(date_str)
        booked: list[tuple[str, str]] = []
        for b in booking_docs:
            start_min = time_to_minutes(b["time_slot"])
            end_min = start_min + b.get("duration_minutes", 30)
            hours, mins = divmod(end_min, 60)
            booked.append((b["time_slot"], f"{hours:02d}:{mins:02d}"))

        all_slots = generate_30min_slots(day_config.open_time, day_config.close_time)

        now = datetime.now()
        is_today = requested_date == now.date()
        now_minutes = now.hour * 60 + now.minute if is_today else 0

        available: list[AvailableSlot] = []
        for slot in all_slots:
            if is_today and time_to_minutes(slot["start"]) <= now_minutes:
                continue
            if any(
                ranges_overlap(slot["start"], slot["end"], u_start, u_end)
                for u_start, u_end in unavailable
            ):
                continue
            if any(
                ranges_overlap(slot["start"], slot["end"], b_start, b_end)
                for b_start, b_end in booked
            ):
                continue
            available.append(AvailableSlot(start=slot["start"], end=slot["end"]))
        return available


# ── ListUnavailabilityForDate / ForRange ─────────────────────────────────


class ListUnavailabilityForDate:
    def __init__(self, repo: UnavailabilityRepository) -> None:
        self._repo = repo

    async def execute(self, booking_date: str) -> list[dict]:
        return await self._repo.list_for_date(booking_date)


class ListUnavailabilityForRange:
    def __init__(self, repo: UnavailabilityRepository) -> None:
        self._repo = repo

    async def execute(self, start: str, end: str) -> list[dict]:
        return await self._repo.list_for_range(start, end)


class ListHolidaysInRange:
    def __init__(self, repo: UnavailabilityRepository) -> None:
        self._repo = repo

    async def execute(self, start: str, end: str) -> list[str]:
        return await self._repo.list_holiday_dates_in_range(start, end)


# ── AddUnavailability / RemoveUnavailability ─────────────────────────────


class AddUnavailability:
    """Create either a full-day holiday or a time-window block."""

    def __init__(self, repo: UnavailabilityRepository) -> None:
        self._repo = repo

    async def execute(self, data: UnavailabilityCreate) -> dict:
        if data.is_holiday:
            existing = await self._repo.find_holiday(data.date)
            if existing:
                raise BookingValidationError(
                    f"{data.date} is already marked as a holiday"
                )
            doc: dict = {
                "date": data.date,
                "is_holiday": True,
                "reason": data.reason,
            }
        else:
            if not data.start_time or not data.end_time:
                raise BookingValidationError(
                    "start_time and end_time are required for time blocks"
                )
            if time_to_minutes(data.start_time) >= time_to_minutes(data.end_time):
                raise BookingValidationError("start_time must be before end_time")
            doc = {
                "date": data.date,
                "start_time": data.start_time,
                "end_time": data.end_time,
                "is_holiday": False,
                "reason": data.reason,
            }

        inserted_id = await self._repo.insert(doc)
        doc["_id"] = inserted_id
        return doc


class RemoveUnavailability:
    def __init__(self, repo: UnavailabilityRepository) -> None:
        self._repo = repo

    async def execute(self, block_id: str) -> None:
        deleted = await self._repo.delete_by_id(block_id)
        if deleted == 0:
            raise EntityNotFoundError("Unavailability block not found")


# ── Business hours ────────────────────────────────────────────────────────


class GetBusinessHours:
    def __init__(self, repo: SettingsRepository) -> None:
        self._repo = repo

    async def execute(self) -> BusinessHoursSettings:
        return await _load_business_hours(self._repo)


class UpdateBusinessHours:
    """Persist a new business-hours configuration. Validates the timezone."""

    def __init__(self, repo: SettingsRepository) -> None:
        self._repo = repo

    async def execute(self, data: BusinessHoursSettings) -> BusinessHoursSettings:
        try:
            ZoneInfo(data.timezone)
        except (ZoneInfoNotFoundError, ValueError):
            raise BookingValidationError(f"Invalid timezone: {data.timezone}")
        await self._repo.save_business_hours_doc(
            {
                "timezone": data.timezone,
                "weekly_hours": [dh.model_dump() for dh in data.weekly_hours],
            }
        )
        return data


# ── Report sections ───────────────────────────────────────────────────────


class GetReportSections:
    """Return the merged, ordered list of report sections.

    Defaults provide the source of truth for which sections exist; any
    section saved in the DB overrides the default for that ID; new sections
    added to DEFAULT_REPORT_SECTIONS surface even if the saved doc predates
    them.
    """

    def __init__(self, repo: SettingsRepository) -> None:
        self._repo = repo

    async def execute(self) -> list[ReportSection]:
        doc = await self._repo.get_report_sections_doc()
        if not doc or not doc.get("sections"):
            return list(DEFAULT_REPORT_SECTIONS)
        saved = {s["id"]: s for s in doc["sections"]}
        merged: list[ReportSection] = []
        for default in DEFAULT_REPORT_SECTIONS:
            if default.id in saved:
                merged.append(ReportSection(**saved[default.id]))
            else:
                merged.append(default)
        return sorted(merged, key=lambda s: s.order)


class UpdateReportSections:
    def __init__(self, repo: SettingsRepository) -> None:
        self._repo = repo

    async def execute(
        self, sections: list[ReportSection]
    ) -> list[ReportSection]:
        await self._repo.save_report_sections_doc(
            {"sections": [s.model_dump() for s in sections]}
        )
        return sorted(sections, key=lambda s: s.order)
