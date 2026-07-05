"""Rate-limit repository — Protocol interface + Mongo implementation.

A tiny per-email request ledger for the public, unauthenticated async endpoints
(muhurta, unshakable) that persist no domain record of their own but still
enqueue real compute onto SQS. Each accepted request writes one lightweight
``rate_limits`` doc; the daily cap is enforced by counting recent docs for the
same (email, action). Docs self-expire via a TTL index, so the collection never
grows unbounded and needs no cleanup ritual.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Protocol


class RateLimitRepository(Protocol):
    async def count_since(self, email: str, action: str, since: datetime) -> int: ...

    async def record(self, email: str, action: str, *, ttl_hours: int) -> None: ...

    async def ensure_indexes(self) -> None: ...


# ── Mongo implementation ────────────────────────────────────────────────────


class MongoRateLimitRepository:
    def __init__(self, db: Any) -> None:
        self._db = db

    @property
    def _col(self):
        return self._db.rate_limits

    async def count_since(self, email: str, action: str, since: datetime) -> int:
        return await self._col.count_documents(
            {"email": email, "action": action, "created_at": {"$gte": since}}
        )

    async def record(self, email: str, action: str, *, ttl_hours: int) -> None:
        now = datetime.now(timezone.utc)
        await self._col.insert_one(
            {
                "email": email,
                "action": action,
                "created_at": now,
                # TTL field: the doc is reaped once now > expires_at, so the
                # ledger only ever holds the current rate-limit window.
                "expires_at": now + timedelta(hours=ttl_hours),
            }
        )

    async def ensure_indexes(self) -> None:
        # {email, action, created_at desc} — the per-email count lookup.
        await self._col.create_index(
            [("email", 1), ("action", 1), ("created_at", -1)]
        )
        # TTL on expires_at (expireAfterSeconds=0 → delete once now > value).
        await self._col.create_index([("expires_at", 1)], expireAfterSeconds=0)
