"""Booking slot-validation logic shared by create + reschedule flows.

Pulls together:
  - calendar-day parse (rejects "0000-00-00")
  - holiday lookup
  - business-hours window
  - unavailability blocks
  - existing-booking conflicts (confirmed + non-expired pending)

This used to live duplicated in `routers/bookings.py:create_booking` (lines
85-138) and `routers/bookings.py:reschedule_booking` (lines 311-346). Now
it's one function called from both.

Raises BookingValidationError on any rule failure — the router maps that to
400 BadRequest. The validator never raises HTTP-specific exceptions, so it
can be reused from background tasks / CLI.
"""

from __future__ import annotations

from datetime import date

from bson import ObjectId

from app.domain.exceptions import BookingValidationError
from app.repositories.booking_repository import BookingRepository
from app.services.settings import get_business_hours
from app.utils.time_helpers import ranges_overlap, time_to_minutes


async def validate_slot(
    booking_repo: BookingRepository,
    db,
    *,
    booking_date: str,
    time_slot: str,
    duration_minutes: int,
    exclude_booking_id: ObjectId | None = None,
) -> None:
    """Validate that a booking can be placed at this date/time/duration.

    Args:
        booking_repo: BookingRepository — used for booking-conflict checks.
        db: Motor database handle, used for unavailability lookups (which
            don't yet have a dedicated repository — future cleanup).
        booking_date: ISO date "YYYY-MM-DD". Calendar-validity is checked
            here — Pydantic only enforces shape.
        time_slot: "HH:MM" in 24-hour. Caller has already passed the regex.
        duration_minutes: 0 means "report" (no scheduling). Anything > 0 is
            a real session.
        exclude_booking_id: ObjectId — when rescheduling, exclude this
            booking from the conflict check (otherwise it'd conflict with
            itself).

    Raises:
        BookingValidationError: any rule failure. The string message is
            user-facing; format it as "<reason>".
    """
    # Reports (duration=0) skip all scheduling rules — they have no slot.
    if duration_minutes == 0:
        return

    # Calendar validity
    try:
        requested_date = date.fromisoformat(booking_date)
    except ValueError:
        raise BookingValidationError(f"Invalid date: {booking_date}")

    # Holiday block
    holiday = await db.unavailability.find_one({"date": booking_date, "is_holiday": True})
    if holiday:
        raise BookingValidationError("This date is a holiday")

    booking_start = time_to_minutes(time_slot)
    # `max(.., 30)` handles ad-hoc bookings that pass duration < 30; a
    # 30-minute floor for unavailability checks. Reports already returned above.
    booking_end = booking_start + max(duration_minutes, 30)

    # Business-hours window for the day
    bh_settings = await get_business_hours()
    day_of_week = requested_date.weekday()
    day_config = next(
        (d for d in bh_settings.weekly_hours if d.day == day_of_week),
        None,
    )
    if not day_config or not day_config.is_open:
        raise BookingValidationError("Bookings are not available on this day")

    bh_open = time_to_minutes(day_config.open_time)
    bh_close = time_to_minutes(day_config.close_time)
    if booking_start < bh_open or booking_end > bh_close:
        raise BookingValidationError(
            f"Booking must be within business hours "
            f"({day_config.open_time} - {day_config.close_time})"
        )

    # Admin-defined unavailability blocks (e.g., lunch hours)
    cursor = db.unavailability.find({"date": booking_date, "is_holiday": False})
    async for block in cursor:
        start_t = block.get("start_time")
        end_t = block.get("end_time")
        if start_t and end_t:
            if ranges_overlap(booking_start, booking_end, start_t, end_t):
                raise BookingValidationError("This time slot is unavailable")

    # Existing booking conflicts via the repository — encapsulates the
    # confirmed-or-non-expired-pending query.
    existing = await booking_repo.find_active_on_date(
        booking_date, exclude_id=exclude_booking_id
    )
    for ex in existing:
        ex_start = time_to_minutes(ex["time_slot"])
        ex_end = ex_start + ex.get("duration_minutes", 30)
        if ranges_overlap(booking_start, booking_end, ex_start, ex_end):
            raise BookingValidationError("This time slot is already booked")
