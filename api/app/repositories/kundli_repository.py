"""Kundli repository — Protocol interface + Mongo implementation.

Encapsulates every read/write to the `kundlis` collection. The free-tier
report flow goes:
  insert_pending -> (background task) -> mark_generated | mark_failed
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Protocol

from bson import ObjectId

from app.models.kundli import KundliInDB


class KundliRepository(Protocol):
    async def insert_pending(self, kundli: KundliInDB) -> ObjectId: ...

    async def mark_generated(
        self, record_id: ObjectId, *, chart_data: dict
    ) -> int: ...

    async def mark_failed(self, record_id: ObjectId, *, error: str) -> int: ...

    async def count_for_email_since(self, email: str, since: datetime) -> int: ...


# ── Mongo implementation ────────────────────────────────────────────────────


class MongoKundliRepository:
    def __init__(self, db: Any) -> None:
        self._db = db

    @property
    def _kundlis(self):
        return self._db.kundlis

    async def insert_pending(self, kundli: KundliInDB) -> ObjectId:
        result = await self._kundlis.insert_one(kundli.model_dump())
        return result.inserted_id

    async def mark_generated(
        self, record_id: ObjectId, *, chart_data: dict
    ) -> int:
        result = await self._kundlis.update_one(
            {"_id": record_id},
            {"$set": {"chart_data": chart_data, "status": "generated"}},
        )
        return result.modified_count

    async def mark_failed(self, record_id: ObjectId, *, error: str) -> int:
        result = await self._kundlis.update_one(
            {"_id": record_id},
            {"$set": {"status": "failed", "error": error[:500]}},
        )
        return result.modified_count

    async def count_for_email_since(self, email: str, since: datetime) -> int:
        return await self._kundlis.count_documents(
            {"email": email, "created_at": {"$gte": since}}
        )
