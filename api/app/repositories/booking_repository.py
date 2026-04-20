"""Booking repository — Protocol interface + Mongo implementation.

Use cases depend on the Protocol (`BookingRepository`), not the concrete
class. Tests can pass an in-memory fake; production wires `MongoBookingRepository`
via FastAPI `Depends()`.

Why a Protocol and not an ABC: Protocols are structural — any class with
matching method signatures satisfies the interface, no inheritance required.
That makes it cheap to write a fake in a single test file without importing
the production class.

The repository owns ALL Mongo query construction for the bookings collection.
Any code outside this module that touches `db.bookings.find(...)` is a smell.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Protocol

from bson import ObjectId

from app.models.booking import PENDING_EXPIRY_MINUTES, BookingInDB, BookingStatus


class BookingRepository(Protocol):
    """Storage interface for bookings — implemented by MongoBookingRepository.

    All methods return raw `dict` rows (or None / lists thereof) — the
    use case is responsible for constructing response models. We don't
    return Pydantic models from the repo because the same row can shape
    into BookingResponse, BookingInDB, or any other view at the use-case
    layer.
    """

    async def insert(self, booking: BookingInDB) -> ObjectId: ...

    async def find_by_id(self, booking_id: str | ObjectId) -> dict | None: ...

    async def list_for_user(
        self,
        *,
        user_email: str | None = None,
        status: BookingStatus | None = None,
        date: str | None = None,
        limit: int = 100,
    ) -> list[dict]: ...

    async def update_status(
        self,
        booking_id: str | ObjectId,
        status: BookingStatus | str,
    ) -> int: ...

    async def update_schedule(
        self,
        booking_id: str | ObjectId,
        *,
        date: str,
        time_slot: str,
        duration_minutes: int,
    ) -> int: ...

    async def find_active_on_date(
        self,
        booking_date: str,
        *,
        exclude_id: ObjectId | None = None,
    ) -> list[dict]: ...

    async def count_for_email_since(
        self,
        email: str,
        since: datetime,
    ) -> int: ...

    async def count_total(self) -> int: ...

    async def count_for_date(self, booking_date: str) -> int: ...

    async def count_upcoming_confirmed(self, from_date: str) -> int: ...

    async def aggregate_status_counts(self) -> dict[str, int]: ...

    async def aggregate_revenue_by_service(self) -> list[dict]: ...

    async def aggregate_daily_counts(
        self, start_date: str, end_date: str
    ) -> dict[str, int]: ...


# ── Mongo implementation ────────────────────────────────────────────────────


def _to_object_id(value: str | ObjectId) -> ObjectId:
    """Coerce string IDs to ObjectId. Raises bson.errors.InvalidId on garbage —
    the use case should catch that and raise EntityNotFoundError."""
    return value if isinstance(value, ObjectId) else ObjectId(value)


class MongoBookingRepository:
    """Production repository — wraps the `bookings` collection on Motor."""

    def __init__(self, db: Any) -> None:
        # `db` is a Motor `AsyncIOMotorDatabase`; typed as Any so the domain
        # layer doesn't grow a Motor import.
        self._db = db

    @property
    def _bookings(self):
        return self._db.bookings

    async def insert(self, booking: BookingInDB) -> ObjectId:
        result = await self._bookings.insert_one(booking.model_dump())
        return result.inserted_id

    async def find_by_id(self, booking_id: str | ObjectId) -> dict | None:
        return await self._bookings.find_one({"_id": _to_object_id(booking_id)})

    async def list_for_user(
        self,
        *,
        user_email: str | None = None,
        status: BookingStatus | None = None,
        date: str | None = None,
        limit: int = 100,
    ) -> list[dict]:
        query: dict[str, Any] = {}
        if user_email is not None:
            query["user_email"] = user_email
        if status is not None:
            query["status"] = status.value if isinstance(status, BookingStatus) else status
        if date is not None:
            query["date"] = date

        cursor = self._bookings.find(query).sort("created_at", -1).limit(limit)
        return [doc async for doc in cursor]

    async def update_status(
        self,
        booking_id: str | ObjectId,
        status: BookingStatus | str,
    ) -> int:
        status_value = status.value if isinstance(status, BookingStatus) else status
        result = await self._bookings.update_one(
            {"_id": _to_object_id(booking_id)},
            {"$set": {"status": status_value}},
        )
        return result.modified_count

    async def update_schedule(
        self,
        booking_id: str | ObjectId,
        *,
        date: str,
        time_slot: str,
        duration_minutes: int,
    ) -> int:
        result = await self._bookings.update_one(
            {"_id": _to_object_id(booking_id)},
            {"$set": {
                "date": date,
                "time_slot": time_slot,
                "duration_minutes": duration_minutes,
                "reminder_sent": False,
            }},
        )
        return result.modified_count

    async def find_active_on_date(
        self,
        booking_date: str,
        *,
        exclude_id: ObjectId | None = None,
    ) -> list[dict]:
        """Bookings on `booking_date` that count for slot-conflict checks:
        confirmed, plus pending bookings still inside the expiry grace window."""
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=PENDING_EXPIRY_MINUTES)
        query: dict[str, Any] = {
            "date": booking_date,
            "$or": [
                {"status": "confirmed"},
                {"status": "pending", "created_at": {"$gte": cutoff}},
            ],
        }
        if exclude_id is not None:
            query["_id"] = {"$ne": exclude_id}
        cursor = self._bookings.find(query)
        return [doc async for doc in cursor]

    async def count_for_email_since(
        self,
        email: str,
        since: datetime,
    ) -> int:
        return await self._bookings.count_documents(
            {"user_email": email, "created_at": {"$gte": since}}
        )

    async def count_total(self) -> int:
        return await self._bookings.count_documents({})

    async def count_for_date(self, booking_date: str) -> int:
        return await self._bookings.count_documents({"date": booking_date})

    async def count_upcoming_confirmed(self, from_date: str) -> int:
        return await self._bookings.count_documents(
            {"date": {"$gte": from_date}, "status": "confirmed"}
        )

    async def aggregate_status_counts(self) -> dict[str, int]:
        pipeline = [{"$group": {"_id": "$status", "count": {"$sum": 1}}}]
        result: dict[str, int] = {}
        async for doc in self._bookings.aggregate(pipeline):
            result[doc["_id"]] = doc["count"]
        return result

    async def aggregate_revenue_by_service(self) -> list[dict]:
        pipeline = [
            {"$match": {"status": {"$in": ["confirmed", "completed"]}}},
            {
                "$group": {
                    "_id": "$service_title",
                    "count": {"$sum": 1},
                    "revenue": {"$sum": "$price_inr"},
                }
            },
            {"$sort": {"revenue": -1}},
        ]
        return [doc async for doc in self._bookings.aggregate(pipeline)]

    async def aggregate_daily_counts(
        self, start_date: str, end_date: str
    ) -> dict[str, int]:
        pipeline = [
            {"$match": {"date": {"$gte": start_date, "$lte": end_date}}},
            {"$group": {"_id": "$date", "count": {"$sum": 1}}},
            {"$sort": {"_id": 1}},
        ]
        result: dict[str, int] = {}
        async for doc in self._bookings.aggregate(pipeline):
            result[doc["_id"]] = doc["count"]
        return result
