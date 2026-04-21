"""Unavailability repository — Protocol + Mongo implementation.

Owns every read/write to the `unavailability` collection (admin holidays
and time blocks). The collection serves both the booking-validator path
(slot conflicts) and the public availability lookup endpoints.
"""

from __future__ import annotations

from typing import Any, Protocol

from bson import ObjectId
from bson.errors import InvalidId


class UnavailabilityRepository(Protocol):
    async def list_for_date(self, booking_date: str) -> list[dict]: ...

    async def list_for_range(self, start: str, end: str) -> list[dict]: ...

    async def list_holiday_dates_in_range(
        self, start: str, end: str
    ) -> list[str]: ...

    async def find_holiday(self, booking_date: str) -> dict | None: ...

    async def insert(self, doc: dict) -> ObjectId: ...

    async def delete_by_id(self, block_id: str | ObjectId) -> int: ...

    async def ensure_indexes(self) -> None: ...


# ── Mongo implementation ────────────────────────────────────────────────────


def _to_object_id(value: str | ObjectId) -> ObjectId:
    return value if isinstance(value, ObjectId) else ObjectId(value)


class MongoUnavailabilityRepository:
    def __init__(self, db: Any) -> None:
        self._db = db

    @property
    def _coll(self):
        return self._db.unavailability

    async def list_for_date(self, booking_date: str) -> list[dict]:
        cursor = self._coll.find({"date": booking_date}).sort("start_time", 1)
        return [doc async for doc in cursor]

    async def list_for_range(self, start: str, end: str) -> list[dict]:
        cursor = self._coll.find({"date": {"$gte": start, "$lte": end}}).sort("date", 1)
        return [doc async for doc in cursor]

    async def list_holiday_dates_in_range(self, start: str, end: str) -> list[str]:
        cursor = self._coll.find(
            {"date": {"$gte": start, "$lte": end}, "is_holiday": True}
        )
        return [doc["date"] async for doc in cursor]

    async def find_holiday(self, booking_date: str) -> dict | None:
        return await self._coll.find_one(
            {"date": booking_date, "is_holiday": True}
        )

    async def list_blocks_for_date(self, booking_date: str) -> list[dict]:
        """Time blocks (not full-day holidays) for a date — used by slot lookup."""
        cursor = self._coll.find({"date": booking_date, "is_holiday": False})
        return [doc async for doc in cursor]

    async def insert(self, doc: dict) -> ObjectId:
        result = await self._coll.insert_one(doc)
        return result.inserted_id

    async def delete_by_id(self, block_id: str | ObjectId) -> int:
        try:
            oid = _to_object_id(block_id)
        except (InvalidId, TypeError):
            return 0
        result = await self._coll.delete_one({"_id": oid})
        return result.deleted_count

    async def ensure_indexes(self) -> None:
        # {date, is_holiday} — slot/holiday lookup on a date.
        await self._coll.create_index([("date", 1), ("is_holiday", 1)])
