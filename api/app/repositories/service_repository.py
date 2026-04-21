"""Service repository — Protocol + Mongo implementation.

Owns the `services` collection. Documents use `slug` as the natural key.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Protocol

from app.models.service import Service, ServiceInDB


class ServiceRepository(Protocol):
    async def list_all(self) -> list[Service]: ...

    async def find_by_slug(self, slug: str) -> Service | None: ...

    async def upsert(self, service: Service) -> None: ...

    async def delete_by_slug(self, slug: str) -> int: ...

    async def seed_if_empty(self, defaults: list[Service]) -> int: ...

    async def ensure_indexes(self) -> None: ...


# ── Mongo implementation ────────────────────────────────────────────────────


def _doc_to_service(doc: dict) -> Service:
    return Service(
        slug=doc["slug"],
        title=doc.get("title"),
        durations=doc.get("durations", []),
    )


class MongoServiceRepository:
    def __init__(self, db: Any) -> None:
        self._db = db

    @property
    def _coll(self):
        return self._db.services

    async def list_all(self) -> list[Service]:
        cursor = self._coll.find().sort("slug", 1)
        return [_doc_to_service(doc) async for doc in cursor]

    async def find_by_slug(self, slug: str) -> Service | None:
        doc = await self._coll.find_one({"slug": slug})
        return _doc_to_service(doc) if doc else None

    async def upsert(self, service: Service) -> None:
        now = datetime.now(timezone.utc)
        record = ServiceInDB(**service.model_dump()).model_dump()
        record["updated_at"] = now
        await self._coll.update_one(
            {"slug": service.slug},
            {
                "$set": {
                    "slug": record["slug"],
                    "title": record.get("title"),
                    "durations": record["durations"],
                    "updated_at": now,
                },
                "$setOnInsert": {"created_at": now},
            },
            upsert=True,
        )

    async def delete_by_slug(self, slug: str) -> int:
        result = await self._coll.delete_one({"slug": slug})
        return result.deleted_count

    async def seed_if_empty(self, defaults: list[Service]) -> int:
        """Insert the default catalogue iff the collection is empty.

        Returns the number of documents inserted (0 if already populated).
        Idempotent — safe to call on every boot.
        """
        existing = await self._coll.count_documents({})
        if existing > 0:
            return 0
        now = datetime.now(timezone.utc)
        docs = [
            {
                **ServiceInDB(**s.model_dump()).model_dump(),
                "created_at": now,
                "updated_at": now,
            }
            for s in defaults
        ]
        if not docs:
            return 0
        result = await self._coll.insert_many(docs)
        return len(result.inserted_ids)

    async def ensure_indexes(self) -> None:
        # UNIQUE on slug — natural key, looked up on every booking-create.
        await self._coll.create_index([("slug", 1)], unique=True)
