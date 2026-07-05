"""Availability repository — Protocol + Mongo implementation.

Owns every write to the legacy `availability` collection (per-date slot
documents shaped `{date, slots: [{start, booked, ...}]}`). This is a DIFFERENT
collection from `unavailability` (admin holidays/blocks, which has its own
repository) — the two were never unified. Before this repository existed the
payments use case reached into `db.availability` directly; that raw access is
the boundary leak this module closes.

Kept intentionally minimal: only the writes the domain currently needs live
here. The public availability *read* path still lives elsewhere and can be
folded in when the slot model is unified.
"""

from __future__ import annotations

from typing import Any, Protocol


class AvailabilityRepository(Protocol):
    async def mark_slot_booked(self, booking_date: str, time_slot: str) -> int: ...


# ── Mongo implementation ────────────────────────────────────────────────────


class MongoAvailabilityRepository:
    def __init__(self, db: Any) -> None:
        self._db = db

    @property
    def _coll(self):
        return self._db.availability

    async def mark_slot_booked(self, booking_date: str, time_slot: str) -> int:
        """Flag the matching slot as booked on the day's availability document.

        No-op (returns 0) if the day/slot isn't present — the slot map is a
        display convenience, not the source of truth for conflicts.
        """
        result = await self._coll.update_one(
            {"date": booking_date, "slots.start": time_slot},
            {"$set": {"slots.$.booked": True}},
        )
        return result.modified_count
