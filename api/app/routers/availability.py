"""Availability HTTP layer.

Thin: parses requests, picks a use case via Depends(), shapes responses.
Slot generation, holiday/block validation, business-hours and report-section
state all live in `app/use_cases/availability.py`.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.dependencies import (
    get_booking_repository,
    get_settings_repository,
    get_unavailability_repository,
    require_admin,
)
from app.models.availability import (
    AvailableSlot,
    BusinessHoursResponse,
    BusinessHoursSettings,
    ReportSection,
    UnavailabilityCreate,
    UnavailabilityResponse,
)
from app.repositories.booking_repository import BookingRepository
from app.repositories.settings_repository import SettingsRepository
from app.repositories.unavailability_repository import UnavailabilityRepository
from app.use_cases.availability import (
    AddUnavailability,
    GetAvailableSlots,
    GetBusinessHours,
    GetReportSections,
    ListHolidaysInRange,
    ListUnavailabilityForDate,
    ListUnavailabilityForRange,
    RemoveUnavailability,
    UpdateBusinessHours,
    UpdateReportSections,
)

router = APIRouter(prefix="/api/availability", tags=["Availability"])


# Back-compat shims — tests import these names from this module.
from app.services.slot_generator import generate_30min_slots as _generate_all_slots  # noqa: E402,F401
from app.utils.time_helpers import ranges_overlap as _overlaps  # noqa: E402,F401
from app.utils.time_helpers import time_to_minutes as _time_to_minutes  # noqa: E402,F401


# ── Use-case factories ────────────────────────────────────────────────────


def _get_available_slots_use_case(
    unavail_repo: UnavailabilityRepository = Depends(get_unavailability_repository),
    booking_repo: BookingRepository = Depends(get_booking_repository),
    settings_repo: SettingsRepository = Depends(get_settings_repository),
) -> GetAvailableSlots:
    return GetAvailableSlots(unavail_repo, booking_repo, settings_repo)


def _list_unavailability_use_case(
    repo: UnavailabilityRepository = Depends(get_unavailability_repository),
) -> ListUnavailabilityForDate:
    return ListUnavailabilityForDate(repo)


def _list_unavailability_range_use_case(
    repo: UnavailabilityRepository = Depends(get_unavailability_repository),
) -> ListUnavailabilityForRange:
    return ListUnavailabilityForRange(repo)


def _list_holidays_use_case(
    repo: UnavailabilityRepository = Depends(get_unavailability_repository),
) -> ListHolidaysInRange:
    return ListHolidaysInRange(repo)


def _add_unavailability_use_case(
    repo: UnavailabilityRepository = Depends(get_unavailability_repository),
) -> AddUnavailability:
    return AddUnavailability(repo)


def _remove_unavailability_use_case(
    repo: UnavailabilityRepository = Depends(get_unavailability_repository),
) -> RemoveUnavailability:
    return RemoveUnavailability(repo)


def _get_business_hours_use_case(
    repo: SettingsRepository = Depends(get_settings_repository),
) -> GetBusinessHours:
    return GetBusinessHours(repo)


def _update_business_hours_use_case(
    repo: SettingsRepository = Depends(get_settings_repository),
) -> UpdateBusinessHours:
    return UpdateBusinessHours(repo)


def _get_report_sections_use_case(
    repo: SettingsRepository = Depends(get_settings_repository),
) -> GetReportSections:
    return GetReportSections(repo)


def _update_report_sections_use_case(
    repo: SettingsRepository = Depends(get_settings_repository),
) -> UpdateReportSections:
    return UpdateReportSections(repo)


# ── Response shaping ─────────────────────────────────────────────────────


def _doc_to_response(doc: dict) -> UnavailabilityResponse:
    return UnavailabilityResponse(
        id=str(doc["_id"]),
        date=doc["date"],
        start_time=doc.get("start_time"),
        end_time=doc.get("end_time"),
        is_holiday=doc.get("is_holiday", False),
        reason=doc.get("reason", ""),
    )


# ── Endpoints ────────────────────────────────────────────────────────────


@router.get("/slots", response_model=list[AvailableSlot])
async def get_available_slots(
    date_str: str = Query(..., alias="date", pattern=r"^\d{4}-\d{2}-\d{2}$"),
    use_case: GetAvailableSlots = Depends(_get_available_slots_use_case),
):
    """Get available 30-min slots for a date, respecting business hours."""
    return await use_case.execute(date_str)


@router.get("/unavailable", response_model=list[UnavailabilityResponse])
async def get_unavailability(
    date: str = Query(..., pattern=r"^\d{4}-\d{2}-\d{2}$"),
    use_case: ListUnavailabilityForDate = Depends(_list_unavailability_use_case),
):
    docs = await use_case.execute(date)
    return [_doc_to_response(d) for d in docs]


@router.get("/unavailable/range", response_model=list[UnavailabilityResponse])
async def get_unavailability_range(
    start: str = Query(..., pattern=r"^\d{4}-\d{2}-\d{2}$"),
    end: str = Query(..., pattern=r"^\d{4}-\d{2}-\d{2}$"),
    use_case: ListUnavailabilityForRange = Depends(_list_unavailability_range_use_case),
):
    docs = await use_case.execute(start, end)
    return [_doc_to_response(d) for d in docs]


@router.get("/holidays", response_model=list[str])
async def get_holidays(
    start: str = Query(..., pattern=r"^\d{4}-\d{2}-\d{2}$"),
    end: str = Query(..., pattern=r"^\d{4}-\d{2}-\d{2}$"),
    use_case: ListHolidaysInRange = Depends(_list_holidays_use_case),
):
    return await use_case.execute(start, end)


@router.post("/unavailable", response_model=UnavailabilityResponse)
async def add_unavailability(
    data: UnavailabilityCreate,
    _admin: dict = Depends(require_admin),
    use_case: AddUnavailability = Depends(_add_unavailability_use_case),
):
    doc = await use_case.execute(data)
    return _doc_to_response(doc)


@router.delete("/unavailable/{block_id}")
async def remove_unavailability(
    block_id: str,
    _admin: dict = Depends(require_admin),
    use_case: RemoveUnavailability = Depends(_remove_unavailability_use_case),
):
    await use_case.execute(block_id)
    return {"message": "Removed"}


# ── Business Hours Settings ──


@router.get("/settings", response_model=BusinessHoursResponse)
async def get_business_hours_settings(
    use_case: GetBusinessHours = Depends(_get_business_hours_use_case),
):
    settings = await use_case.execute()
    return BusinessHoursResponse(
        timezone=settings.timezone,
        weekly_hours=settings.weekly_hours,
    )


@router.put("/settings", response_model=BusinessHoursResponse)
async def update_business_hours_settings(
    data: BusinessHoursSettings,
    _admin: dict = Depends(require_admin),
    use_case: UpdateBusinessHours = Depends(_update_business_hours_use_case),
):
    saved = await use_case.execute(data)
    return BusinessHoursResponse(
        timezone=saved.timezone,
        weekly_hours=saved.weekly_hours,
    )


# ── Report Sections Settings ──


@router.get("/settings/report-sections", response_model=list[ReportSection])
async def get_report_sections(
    use_case: GetReportSections = Depends(_get_report_sections_use_case),
):
    return await use_case.execute()


@router.put("/settings/report-sections", response_model=list[ReportSection])
async def update_report_sections(
    sections: list[ReportSection],
    _admin: dict = Depends(require_admin),
    use_case: UpdateReportSections = Depends(_update_report_sections_use_case),
):
    return await use_case.execute(sections)
