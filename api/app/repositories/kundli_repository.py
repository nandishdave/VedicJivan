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

    async def ensure_indexes(self) -> None: ...


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
        # `$unset: expires_at` so the TTL index doesn't reap successful records.
        result = await self._kundlis.update_one(
            {"_id": record_id},
            {
                "$set": {"chart_data": chart_data, "status": "generated"},
                "$unset": {"expires_at": ""},
            },
        )
        return result.modified_count

    async def mark_failed(self, record_id: ObjectId, *, error: str) -> int:
        # Failed records also persist (admin needs them visible) — same $unset.
        result = await self._kundlis.update_one(
            {"_id": record_id},
            {
                "$set": {"status": "failed", "error": error[:500]},
                "$unset": {"expires_at": ""},
            },
        )
        return result.modified_count

    async def count_for_email_since(self, email: str, since: datetime) -> int:
        return await self._kundlis.count_documents(
            {"email": email, "created_at": {"$gte": since}}
        )

    async def ensure_indexes(self) -> None:
        # {email, created_at desc} — per-email rate-limit count_documents lookup.
        await self._kundlis.create_index(
            [("email", 1), ("created_at", -1)]
        )
        # TTL on `expires_at`. Mongo treats the indexed field's value as the
        # absolute expiry time when expireAfterSeconds=0, deleting the doc
        # once now > expires_at. Docs without the field are skipped — the
        # `$unset` in mark_generated / mark_failed disables expiry on
        # successful runs.
        await self._kundlis.create_index(
            [("expires_at", 1)], expireAfterSeconds=0
        )
