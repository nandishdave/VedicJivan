from datetime import datetime, timedelta

from bson import ObjectId
from fastapi import APIRouter, Depends, Query

from app.database import get_db
from app.dependencies import require_admin
from app.models.availability import (
    AvailabilityCreate,
    AvailabilityResponse,
    BulkAvailabilityCreate,
    TimeSlot,
)
from app.utils.exceptions import NotFoundError

router = APIRouter(prefix="/api/availability", tags=["Availability"])


@router.get("", response_model=AvailabilityResponse | None)
async def get_availability(date: str = Query(..., pattern=r"^\d{4}-\d{2}-\d{2}$")):
    db = get_db()
    doc = await db.availability.find_one({"date": date})
    if not doc:
        return None
    return AvailabilityResponse(
        id=str(doc["_id"]),
        date=doc["date"],
        slots=doc["slots"],
        is_holiday=doc.get("is_holiday", False),
    )


@router.get("/range", response_model=list[AvailabilityResponse])
async def get_availability_range(
    start: str = Query(..., pattern=r"^\d{4}-\d{2}-\d{2}$"),
    end: str = Query(..., pattern=r"^\d{4}-\d{2}-\d{2}$"),
):
    db = get_db()
    cursor = db.availability.find({"date": {"$gte": start, "$lte": end}}).sort(
        "date", 1
    )
    results = []
    async for doc in cursor:
        results.append(
            AvailabilityResponse(
                id=str(doc["_id"]),
                date=doc["date"],
                slots=doc["slots"],
                is_holiday=doc.get("is_holiday", False),
            )
        )
    return results


@router.post("", response_model=AvailabilityResponse)
async def create_or_update_availability(
    data: AvailabilityCreate,
    _admin: dict = Depends(require_admin),
):
    db = get_db()

    existing = await db.availability.find_one({"date": data.date})
    doc = data.model_dump()

    if existing:
        await db.availability.update_one({"_id": existing["_id"]}, {"$set": doc})
        return AvailabilityResponse(
            id=str(existing["_id"]),
            date=doc["date"],
            slots=doc["slots"],
            is_holiday=doc["is_holiday"],
        )

    result = await db.availability.insert_one(doc)
    return AvailabilityResponse(
        id=str(result.inserted_id),
        date=doc["date"],
        slots=doc["slots"],
        is_holiday=doc["is_holiday"],
    )


@router.post("/bulk", response_model=dict)
async def create_bulk_availability(
    data: BulkAvailabilityCreate,
    _admin: dict = Depends(require_admin),
):
    db = get_db()

    start = datetime.strptime(data.start_date, "%Y-%m-%d")
    end = datetime.strptime(data.end_date, "%Y-%m-%d")

    created_count = 0
    current = start

    while current <= end:
        if current.weekday() in data.working_days:
            date_str = current.strftime("%Y-%m-%d")

            # Generate time slots
            slots = []
            slot_start = datetime.strptime(data.start_time, "%H:%M")
            slot_end_limit = datetime.strptime(data.end_time, "%H:%M")

            while slot_start + timedelta(minutes=data.slot_duration_minutes) <= slot_end_limit:
                slot_finish = slot_start + timedelta(minutes=data.slot_duration_minutes)
                slots.append(
                    TimeSlot(
                        start=slot_start.strftime("%H:%M"),
                        end=slot_finish.strftime("%H:%M"),
                        booked=False,
                    ).model_dump()
                )
                slot_start = slot_finish

            existing = await db.availability.find_one({"date": date_str})
            if not existing:
                await db.availability.insert_one(
                    {"date": date_str, "slots": slots, "is_holiday": False}
                )
                created_count += 1

        current += timedelta(days=1)

    return {"created": created_count, "message": f"Created availability for {created_count} days"}


@router.delete("/{availability_id}")
async def delete_availability(
    availability_id: str,
    _admin: dict = Depends(require_admin),
):
    db = get_db()
    result = await db.availability.delete_one({"_id": ObjectId(availability_id)})
    if result.deleted_count == 0:
        raise NotFoundError("Availability not found")
    return {"message": "Deleted"}
