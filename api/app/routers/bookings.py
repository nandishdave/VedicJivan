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


@router.post("", response_model=BookingResponse)
async def create_booking(data: BookingCreate):
    db = get_db()

    # Validate price
    price = get_price(data.service_slug, data.duration_minutes)

    # Check slot availability
    avail = await db.availability.find_one({"date": data.date})
    if not avail:
        raise BadRequestError("No availability on this date")

    if avail.get("is_holiday"):
        raise BadRequestError("This date is a holiday")

    slot_found = False
    for slot in avail["slots"]:
        if slot["start"] == data.time_slot:
            if slot["booked"]:
                raise BadRequestError("This time slot is already booked")
            slot_found = True
            break

    if not slot_found:
        raise BadRequestError("Time slot not available")

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

    # Free up the time slot
    await db.availability.update_one(
        {"date": doc["date"], "slots.start": doc["time_slot"]},
        {"$set": {"slots.$.booked": False}},
    )

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
    )
