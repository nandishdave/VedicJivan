from datetime import datetime, timedelta

from bson import ObjectId
from fastapi import APIRouter, Depends, Query

from app.database import get_db
from app.dependencies import require_admin
from app.models.availability import (
    AvailableSlot,
    UnavailabilityCreate,
    UnavailabilityResponse,
)
from app.utils.exceptions import BadRequestError, NotFoundError

router = APIRouter(prefix="/api/availability", tags=["Availability"])

SLOT_DURATION_MINUTES = 30


def _generate_all_slots() -> list[dict]:
    """Generate all 30-minute slots for a full day (00:00 - 23:30)."""
    slots = []
    current = datetime(2000, 1, 1, 0, 0)
    end = datetime(2000, 1, 2, 0, 0)
    delta = timedelta(minutes=SLOT_DURATION_MINUTES)

    while current + delta <= end:
        slot_end = current + delta
        slots.append({
            "start": current.strftime("%H:%M"),
            "end": slot_end.strftime("%H:%M"),
        })
        current = slot_end

    return slots


def _time_to_minutes(t: str) -> int:
    """Convert HH:MM to minutes since midnight."""
    h, m = t.split(":")
    return int(h) * 60 + int(m)


def _overlaps(start1: str, end1: str, start2: str, end2: str) -> bool:
    """Check if two time ranges overlap."""
    s1, e1 = _time_to_minutes(start1), _time_to_minutes(end1)
    s2, e2 = _time_to_minutes(start2), _time_to_minutes(end2)
    return s1 < e2 and s2 < e1


def _doc_to_response(doc: dict) -> UnavailabilityResponse:
    return UnavailabilityResponse(
        id=str(doc["_id"]),
        date=doc["date"],
        start_time=doc.get("start_time"),
        end_time=doc.get("end_time"),
        is_holiday=doc.get("is_holiday", False),
        reason=doc.get("reason", ""),
    )


@router.get("/slots", response_model=list[AvailableSlot])
async def get_available_slots(
    date: str = Query(..., pattern=r"^\d{4}-\d{2}-\d{2}$"),
):
    """Get available 30-min slots for a date (all slots minus unavailable and booked)."""
    db = get_db()

    # Check if entire day is a holiday
    holiday = await db.unavailability.find_one({"date": date, "is_holiday": True})
    if holiday:
        return []

    # Get unavailable periods for the date
    cursor = db.unavailability.find({"date": date, "is_holiday": False})
    unavailable = []
    async for doc in cursor:
        if doc.get("start_time") and doc.get("end_time"):
            unavailable.append((doc["start_time"], doc["end_time"]))

    # Get confirmed bookings for the date
    booking_cursor = db.bookings.find({
        "date": date,
        "status": {"$in": ["pending", "confirmed"]},
    })
    booked = []
    async for b in booking_cursor:
        start_min = _time_to_minutes(b["time_slot"])
        end_min = start_min + b.get("duration_minutes", 30)
        hours, mins = divmod(end_min, 60)
        booked.append((b["time_slot"], f"{hours:02d}:{mins:02d}"))

    # Generate all slots and filter
    all_slots = _generate_all_slots()
    available = []

    for slot in all_slots:
        blocked = False

        # Check against unavailable periods
        for u_start, u_end in unavailable:
            if _overlaps(slot["start"], slot["end"], u_start, u_end):
                blocked = True
                break

        if not blocked:
            # Check against existing bookings
            for b_start, b_end in booked:
                if _overlaps(slot["start"], slot["end"], b_start, b_end):
                    blocked = True
                    break

        if not blocked:
            available.append(AvailableSlot(start=slot["start"], end=slot["end"]))

    return available


@router.get("/unavailable", response_model=list[UnavailabilityResponse])
async def get_unavailability(
    date: str = Query(..., pattern=r"^\d{4}-\d{2}-\d{2}$"),
):
    """Get unavailable periods for a specific date."""
    db = get_db()
    cursor = db.unavailability.find({"date": date}).sort("start_time", 1)
    results = []
    async for doc in cursor:
        results.append(_doc_to_response(doc))
    return results


@router.get("/unavailable/range", response_model=list[UnavailabilityResponse])
async def get_unavailability_range(
    start: str = Query(..., pattern=r"^\d{4}-\d{2}-\d{2}$"),
    end: str = Query(..., pattern=r"^\d{4}-\d{2}-\d{2}$"),
):
    """Get unavailable periods for a date range."""
    db = get_db()
    cursor = db.unavailability.find(
        {"date": {"$gte": start, "$lte": end}}
    ).sort("date", 1)
    results = []
    async for doc in cursor:
        results.append(_doc_to_response(doc))
    return results


@router.get("/holidays", response_model=list[str])
async def get_holidays(
    start: str = Query(..., pattern=r"^\d{4}-\d{2}-\d{2}$"),
    end: str = Query(..., pattern=r"^\d{4}-\d{2}-\d{2}$"),
):
    """Get holiday dates in a range (for calendar view)."""
    db = get_db()
    cursor = db.unavailability.find(
        {"date": {"$gte": start, "$lte": end}, "is_holiday": True}
    )
    holidays = []
    async for doc in cursor:
        holidays.append(doc["date"])
    return holidays


@router.post("/unavailable", response_model=UnavailabilityResponse)
async def add_unavailability(
    data: UnavailabilityCreate,
    _admin: dict = Depends(require_admin),
):
    """Block a time period or mark a full day as holiday."""
    db = get_db()

    if data.is_holiday:
        # Full-day holiday — remove any existing entry for this date and add holiday
        existing = await db.unavailability.find_one(
            {"date": data.date, "is_holiday": True}
        )
        if existing:
            raise BadRequestError(f"{data.date} is already marked as a holiday")

        doc = {
            "date": data.date,
            "is_holiday": True,
            "reason": data.reason,
        }
    else:
        if not data.start_time or not data.end_time:
            raise BadRequestError("start_time and end_time are required for time blocks")

        if _time_to_minutes(data.start_time) >= _time_to_minutes(data.end_time):
            raise BadRequestError("start_time must be before end_time")

        doc = {
            "date": data.date,
            "start_time": data.start_time,
            "end_time": data.end_time,
            "is_holiday": False,
            "reason": data.reason,
        }

    result = await db.unavailability.insert_one(doc)
    doc["_id"] = result.inserted_id
    return _doc_to_response(doc)


@router.delete("/unavailable/{block_id}")
async def remove_unavailability(
    block_id: str,
    _admin: dict = Depends(require_admin),
):
    """Remove an unavailable period (make it available again)."""
    db = get_db()
    result = await db.unavailability.delete_one({"_id": ObjectId(block_id)})
    if result.deleted_count == 0:
        raise NotFoundError("Unavailability block not found")
    return {"message": "Removed"}
