"""Booking use cases — application workflows for the booking aggregate.

Each use case is a small class with a single `execute()` method. Dependencies
(repository, db, email service) are passed in `__init__` so tests can
substitute fakes.

Use cases:
  - CreateBooking
  - ListBookings
  - GetBooking          (auth-gated)
  - GetBookingPublic    (anyone with the ID can view a confirmed booking)
  - ResumeBooking       (check pending booking is still resumable)
  - CancelBooking
  - SetBookingStatus    (admin-only)
  - RescheduleBooking

These are what `routers/bookings.py` calls. The router becomes thin: parse
request → call use case → translate domain exceptions to HTTP errors.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from typing import Any
from zoneinfo import ZoneInfo

from bson import ObjectId
from bson.errors import InvalidId

from app.domain.exceptions import (
    AccessDeniedError,
    BookingExpiredError,
    BookingNotConfirmedError,
    BookingTooSoonToRescheduleError,
    BookingValidationError,
    EntityNotFoundError,
)
from app.infrastructure.logging import get_logger
from app.models.booking import (
    PENDING_EXPIRY_MINUTES,
    BookingCreate,
    BookingInDB,
    BookingReschedule,
    BookingStatus,
)
from app.repositories.booking_repository import BookingRepository
from app.services.booking_validator import validate_slot

logger = get_logger(__name__)

# Reschedule cutoff. TODO (Phase 5): move to settings.RESCHEDULE_CUTOFF_HOURS
_RESCHEDULE_CUTOFF_HOURS = 24
# Booking timezone for reschedule cutoff. TODO (Phase 5): move to settings.TIMEZONE
_BOOKING_TIMEZONE = "Asia/Kolkata"


# ── Helpers ────────────────────────────────────────────────────────────────


def _safe_object_id(value: str) -> ObjectId:
    """Coerce a string to ObjectId; raise EntityNotFoundError on garbage.

    Use cases never raise HTTP errors — the router translates this to 404.
    """
    try:
        return ObjectId(value)
    except (InvalidId, TypeError):
        raise EntityNotFoundError("Booking not found")


# ── CreateBooking ──────────────────────────────────────────────────────────


class CreateBooking:
    """Validate + persist a new booking in PENDING state."""

    def __init__(self, booking_repo: BookingRepository, db: Any, pricing) -> None:
        self._repo = booking_repo
        self._db = db
        self._pricing = pricing  # callable: (slug, duration) -> (inr, eur)

    async def execute(self, data: BookingCreate) -> dict:
        price_inr, price_eur = self._pricing(data.service_slug, data.duration_minutes)

        # Slot validation (skipped for reports — duration_minutes == 0)
        await validate_slot(
            self._repo,
            self._db,
            booking_date=data.date,
            time_slot=data.time_slot,
            duration_minutes=data.duration_minutes,
        )

        booking = BookingInDB(
            user_name=data.user_name,
            user_email=data.user_email,
            user_phone=data.user_phone,
            service_slug=data.service_slug,
            service_title=data.service_title,
            date=data.date,
            time_slot=data.time_slot,
            duration_minutes=data.duration_minutes,
            price_inr=price_inr,
            price_eur=price_eur,
            notes=data.notes,
            date_of_birth=data.date_of_birth,
            time_of_birth=data.time_of_birth,
            birth_time_unknown=data.birth_time_unknown,
            place_of_birth=data.place_of_birth,
            birth_latitude=data.birth_latitude,
            birth_longitude=data.birth_longitude,
        )
        inserted_id = await self._repo.insert(booking)
        doc = await self._repo.find_by_id(inserted_id)
        return doc


# ── ListBookings ──────────────────────────────────────────────────────────


class ListBookings:
    """List bookings for an authenticated user. Admin sees all; everyone
    else only sees their own."""

    def __init__(self, booking_repo: BookingRepository) -> None:
        self._repo = booking_repo

    async def execute(
        self,
        *,
        current_user: dict,
        status: BookingStatus | None = None,
        booking_date: str | None = None,
    ) -> list[dict]:
        user_email = None if current_user["role"] == "admin" else current_user["email"]
        return await self._repo.list_for_user(
            user_email=user_email,
            status=status,
            date=booking_date,
        )


# ── GetBooking (auth-gated) ───────────────────────────────────────────────


class GetBooking:
    """Fetch a booking by ID. Non-admin can only see their own."""

    def __init__(self, booking_repo: BookingRepository) -> None:
        self._repo = booking_repo

    async def execute(self, booking_id: str, current_user: dict) -> dict:
        oid = _safe_object_id(booking_id)
        doc = await self._repo.find_by_id(oid)
        if not doc:
            raise EntityNotFoundError("Booking not found")
        if current_user["role"] != "admin" and doc.get("user_email") != current_user["email"]:
            raise AccessDeniedError("Access denied")
        return doc


# ── GetBookingPublic ──────────────────────────────────────────────────────


class GetBookingPublic:
    """Public view — anyone with the ID can fetch a confirmed booking
    (used by reschedule page; the booking ID acts as a soft auth token)."""

    def __init__(self, booking_repo: BookingRepository) -> None:
        self._repo = booking_repo

    async def execute(self, booking_id: str) -> dict:
        oid = _safe_object_id(booking_id)
        doc = await self._repo.find_by_id(oid)
        if not doc:
            raise EntityNotFoundError("Booking not found")
        if doc["status"] != BookingStatus.CONFIRMED:
            raise BookingNotConfirmedError("Only confirmed bookings can be viewed publicly")
        return doc


# ── ResumeBooking ─────────────────────────────────────────────────────────


class ResumeBooking:
    """Check whether a pending booking can still be resumed (not expired)."""

    def __init__(self, booking_repo: BookingRepository) -> None:
        self._repo = booking_repo

    async def execute(self, booking_id: str) -> dict:
        oid = _safe_object_id(booking_id)
        doc = await self._repo.find_by_id(oid)
        if not doc:
            raise EntityNotFoundError("Booking not found")
        if doc["status"] != BookingStatus.PENDING:
            raise BookingNotConfirmedError("Booking is no longer pending")
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=PENDING_EXPIRY_MINUTES)
        if doc["created_at"] < cutoff:
            raise BookingExpiredError("Booking has expired")
        return doc


# ── CancelBooking ─────────────────────────────────────────────────────────


class CancelBooking:
    """Cancel a booking. Owner or admin. Cannot cancel completed/cancelled."""

    def __init__(self, booking_repo: BookingRepository) -> None:
        self._repo = booking_repo

    async def execute(self, booking_id: str, current_user: dict) -> dict:
        oid = _safe_object_id(booking_id)
        doc = await self._repo.find_by_id(oid)
        if not doc:
            raise EntityNotFoundError("Booking not found")
        if current_user["role"] != "admin" and doc.get("user_email") != current_user["email"]:
            raise AccessDeniedError("Access denied")
        if doc["status"] in [BookingStatus.COMPLETED, BookingStatus.CANCELLED]:
            raise BookingValidationError(f"Cannot cancel a {doc['status']} booking")

        await self._repo.update_status(oid, BookingStatus.CANCELLED)
        doc["status"] = BookingStatus.CANCELLED
        return doc


# ── SetBookingStatus (admin) ──────────────────────────────────────────────


class SetBookingStatus:
    """Admin-only status mutation."""

    def __init__(self, booking_repo: BookingRepository) -> None:
        self._repo = booking_repo

    async def execute(self, booking_id: str, status: BookingStatus) -> dict:
        oid = _safe_object_id(booking_id)
        doc = await self._repo.find_by_id(oid)
        if not doc:
            raise EntityNotFoundError("Booking not found")
        await self._repo.update_status(oid, status)
        doc["status"] = status.value
        return doc


# ── RescheduleBooking ─────────────────────────────────────────────────────


class RescheduleBooking:
    """Reschedule a confirmed booking to a new date/time.

    Rules: must be confirmed, must be more than 24h away, new date must be
    in the future, new slot must satisfy all standard slot-validation rules.
    On success, optionally sends a "rescheduled" email — failure to send is
    logged but does NOT fail the reschedule.
    """

    def __init__(
        self,
        booking_repo: BookingRepository,
        db: Any,
        email_sender,  # callable matching send_booking_rescheduled signature
    ) -> None:
        self._repo = booking_repo
        self._db = db
        self._send_rescheduled_email = email_sender

    async def execute(self, booking_id: str, data: BookingReschedule) -> dict:
        oid = _safe_object_id(booking_id)
        doc = await self._repo.find_by_id(oid)
        if not doc:
            raise EntityNotFoundError("Booking not found")
        if doc["status"] != BookingStatus.CONFIRMED:
            raise BookingNotConfirmedError("Only confirmed bookings can be rescheduled")

        # 24-hour cutoff against the *existing* booking time
        ist = ZoneInfo(_BOOKING_TIMEZONE)
        booking_dt = datetime.fromisoformat(
            f"{doc['date']}T{doc['time_slot']}:00"
        ).replace(tzinfo=ist)
        if booking_dt - datetime.now(timezone.utc) < timedelta(hours=_RESCHEDULE_CUTOFF_HOURS):
            raise BookingTooSoonToRescheduleError(
                "Rescheduling is not available within 24 hours of your session"
            )

        # New date validity + future check
        try:
            new_date = date.fromisoformat(data.date)
        except ValueError:
            raise BookingValidationError(f"Invalid date: {data.date}")
        if new_date <= date.today():
            raise BookingValidationError("New date must be in the future")

        # Standard slot validation, excluding *this* booking from conflicts
        await validate_slot(
            self._repo,
            self._db,
            booking_date=data.date,
            time_slot=data.time_slot,
            duration_minutes=data.duration_minutes,
            exclude_booking_id=oid,
        )

        old_date = doc["date"]
        old_time = doc["time_slot"]

        await self._repo.update_schedule(
            oid,
            date=data.date,
            time_slot=data.time_slot,
            duration_minutes=data.duration_minutes,
        )

        # Best-effort email notification — never fails the reschedule
        try:
            await self._send_rescheduled_email(
                to_email=doc["user_email"],
                user_name=doc["user_name"],
                service_title=doc["service_title"],
                old_date=old_date,
                old_time=old_time,
                new_date=data.date,
                new_time=data.time_slot,
                booking_id=booking_id,
            )
        except Exception as e:
            logger.error("Reschedule email failed for booking_id=%s: %s", booking_id, e)

        return await self._repo.find_by_id(oid)
