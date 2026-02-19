from datetime import date

from bson import ObjectId
from fastapi import APIRouter, Depends, Query

from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.models.booking import (
    BookingCreate,
    BookingInDB,
    BookingResponse,
    BookingStatus,
    BookingStatusUpdate,
)
from app.services.settings import get_business_hours
from app.utils.exceptions import BadRequestError, ForbiddenError, NotFoundError

router = APIRouter(prefix="/api/bookings", tags=["Bookings"])

# Service pricing (INR in paise-friendly integers)
SERVICE_PRICES = {
    "call-consultation": {"30": 1999, "45": 2499, "60": 2999},
    "video-consultation": {"30": 2499, "45": 2999, "60": 3999},
    "premium-kundli": {"0": 4999},
    "numerology-report": {"0": 1499},
    "vastu-consultation": {"30": 2499, "45": 2999, "60": 3499},
    "matchmaking": {"0": 2499},
    "astrological-consulting": {"30": 2499, "45": 2999, "60": 3499},
    "personal-growth-coaching": {"30": 3499, "45": 3999, "60": 4999},
    "therapeutic-healing": {"45": 4499, "60": 4999, "75": 5999},
}


def get_price(service_slug: str, duration_minutes: int) -> int:
    prices = SERVICE_PRICES.get(service_slug)
    if not prices:
        raise BadRequestError(f"Unknown service: {service_slug}")

    price = prices.get(str(duration_minutes))
    if price is None:
        available = ", ".join(f"{k} min" for k in prices.keys() if k != "0")
        if "0" in prices:
            return prices["0"]
        raise BadRequestError(
            f"Duration {duration_minutes} min not available for this service. Options: {available}"
        )
    return price


def _time_to_minutes(t: str) -> int:
    h, m = t.split(":")
    return int(h) * 60 + int(m)


def _overlaps(s1: int, e1: int, s2: int, e2: int) -> bool:
    return s1 < e2 and s2 < e1


@router.post("", response_model=BookingResponse)
async def create_booking(data: BookingCreate):
    db = get_db()

    # Validate price
    price = get_price(data.service_slug, data.duration_minutes)

    # Check if date is a holiday
    holiday = await db.unavailability.find_one({"date": data.date, "is_holiday": True})
    if holiday:
        raise BadRequestError("This date is a holiday")

    # Calculate booking time range
    booking_start = _time_to_minutes(data.time_slot)
    booking_end = booking_start + max(data.duration_minutes, 30)

    # Check business hours for the day
    bh_settings = await get_business_hours()
    requested_date = date.fromisoformat(data.date)
    day_of_week = requested_date.weekday()

    day_config = next((d for d in bh_settings.weekly_hours if d.day == day_of_week), None)
    if not day_config or not day_config.is_open:
        raise BadRequestError("Bookings are not available on this day")

    bh_open = _time_to_minutes(day_config.open_time)
    bh_close = _time_to_minutes(day_config.close_time)
    if booking_start < bh_open or booking_end > bh_close:
        raise BadRequestError(
            f"Booking must be within business hours ({day_config.open_time} - {day_config.close_time})"
        )

    # Check against unavailable periods
    cursor = db.unavailability.find({"date": data.date, "is_holiday": False})
    async for block in cursor:
        if block.get("start_time") and block.get("end_time"):
            block_start = _time_to_minutes(block["start_time"])
            block_end = _time_to_minutes(block["end_time"])
            if _overlaps(booking_start, booking_end, block_start, block_end):
                raise BadRequestError("This time slot is unavailable")

    # Check against existing bookings
    existing_cursor = db.bookings.find({
        "date": data.date,
        "status": {"$in": ["pending", "confirmed"]},
    })
    async for existing in existing_cursor:
        ex_start = _time_to_minutes(existing["time_slot"])
        ex_end = ex_start + existing.get("duration_minutes", 30)
        if _overlaps(booking_start, booking_end, ex_start, ex_end):
            raise BadRequestError("This time slot is already booked")

    booking = BookingInDB(
        user_name=data.user_name,
        user_email=data.user_email,
        user_phone=data.user_phone,
        service_slug=data.service_slug,
        service_title=data.service_title,
        date=data.date,
        time_slot=data.time_slot,
        duration_minutes=data.duration_minutes,
        price_inr=price,
        notes=data.notes,
        date_of_birth=data.date_of_birth,
        time_of_birth=data.time_of_birth,
        birth_time_unknown=data.birth_time_unknown,
        place_of_birth=data.place_of_birth,
        birth_latitude=data.birth_latitude,
        birth_longitude=data.birth_longitude,
    )

    result = await db.bookings.insert_one(booking.model_dump())

    doc = await db.bookings.find_one({"_id": result.inserted_id})
    return _to_response(doc)


@router.get("", response_model=list[BookingResponse])
async def list_bookings(
    status: BookingStatus | None = None,
    date: str | None = Query(None, pattern=r"^\d{4}-\d{2}-\d{2}$"),
    current_user: dict = Depends(get_current_user),
):
    db = get_db()

    query = {}
    if current_user["role"] != "admin":
        query["user_email"] = current_user["email"]
    if status:
        query["status"] = status.value
    if date:
        query["date"] = date

    cursor = db.bookings.find(query).sort("created_at", -1).limit(100)
    results = []
    async for doc in cursor:
        results.append(_to_response(doc))
    return results


@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(booking_id: str, current_user: dict = Depends(get_current_user)):
    db = get_db()
    doc = await db.bookings.find_one({"_id": ObjectId(booking_id)})
    if not doc:
        raise NotFoundError("Booking not found")

    if current_user["role"] != "admin" and doc.get("user_email") != current_user["email"]:
        raise ForbiddenError("Access denied")

    return _to_response(doc)


@router.patch("/{booking_id}/cancel", response_model=BookingResponse)
async def cancel_booking(booking_id: str, current_user: dict = Depends(get_current_user)):
    db = get_db()
    doc = await db.bookings.find_one({"_id": ObjectId(booking_id)})
    if not doc:
        raise NotFoundError("Booking not found")

    if current_user["role"] != "admin" and doc.get("user_email") != current_user["email"]:
        raise ForbiddenError("Access denied")

    if doc["status"] in [BookingStatus.COMPLETED, BookingStatus.CANCELLED]:
        raise BadRequestError(f"Cannot cancel a {doc['status']} booking")

    await db.bookings.update_one(
        {"_id": ObjectId(booking_id)},
        {"$set": {"status": BookingStatus.CANCELLED}},
    )

    doc["status"] = BookingStatus.CANCELLED
    return _to_response(doc)


@router.patch("/{booking_id}/status", response_model=BookingResponse)
async def update_booking_status(
    booking_id: str,
    data: BookingStatusUpdate,
    _admin: dict = Depends(require_admin),
):
    db = get_db()
    doc = await db.bookings.find_one({"_id": ObjectId(booking_id)})
    if not doc:
        raise NotFoundError("Booking not found")

    await db.bookings.update_one(
        {"_id": ObjectId(booking_id)},
        {"$set": {"status": data.status.value}},
    )

    doc["status"] = data.status.value
    return _to_response(doc)


def _to_response(doc: dict) -> BookingResponse:
    return BookingResponse(
        id=str(doc["_id"]),
        user_name=doc["user_name"],
        user_email=doc["user_email"],
        user_phone=doc["user_phone"],
        service_slug=doc["service_slug"],
        service_title=doc["service_title"],
        date=doc["date"],
        time_slot=doc["time_slot"],
        duration_minutes=doc["duration_minutes"],
        price_inr=doc["price_inr"],
        status=doc["status"],
        payment_id=doc.get("payment_id"),
        notes=doc.get("notes", ""),
        created_at=doc["created_at"],
        date_of_birth=doc.get("date_of_birth", ""),
        time_of_birth=doc.get("time_of_birth"),
        birth_time_unknown=doc.get("birth_time_unknown", False),
        place_of_birth=doc.get("place_of_birth", ""),
        birth_latitude=doc.get("birth_latitude", 0.0),
        birth_longitude=doc.get("birth_longitude", 0.0),
    )
