"""Processed-event repository — Stripe webhook idempotency primitive.

Stripe re-delivers webhooks on network timeout / scheduled retry / manual
replay. Without dedupe, each delivery re-fires every side effect (duplicate
emails, duplicate calendar events, duplicate booking confirmations).

`mark_processed` is a race-safe insert: an atomic `insert_one` with the
event id as `_id` either succeeds (newly seen) or raises `DuplicateKeyError`
(already seen). Two concurrent retries on the same event will see exactly
one True return; the other gets False and skips dispatch.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Protocol

from pymongo.errors import DuplicateKeyError


# 90 days. Stripe's own retry window is 3 days; this gives ample audit
# headroom while keeping the collection bounded.
_TTL_SECONDS = 60 * 60 * 24 * 90


class ProcessedEventRepository(Protocol):
    """Storage interface for the dedupe ledger."""

    async def mark_processed(self, event_id: str, event_type: str) -> bool: ...

    async def ensure_indexes(self) -> None: ...


# ── Mongo implementation ────────────────────────────────────────────────────


class MongoProcessedEventRepository:
    """Production repo — wraps the `stripe_events` collection on Motor."""

    def __init__(self, db: Any) -> None:
        self._db = db

    @property
    def _events(self):
        return self._db.stripe_events

    async def mark_processed(self, event_id: str, event_type: str) -> bool:
        try:
            await self._events.insert_one(
                {
                    "_id": event_id,
                    "type": event_type,
                    "received_at": datetime.now(timezone.utc),
                }
            )
            return True
        except DuplicateKeyError:
            return False

    async def ensure_indexes(self) -> None:
        # `_id` is implicitly unique; the TTL index drives audit cleanup.
        await self._events.create_index(
            [("received_at", 1)], expireAfterSeconds=_TTL_SECONDS
        )
