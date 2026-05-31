"""Settings repository — Protocol + Mongo implementation.

Owns reads/writes against the `settings` collection. Today the collection
holds two documents — `business_hours` and `report_sections` — both with a
string `_id`. Everything that touches `db.settings` should go through this
repo.
"""

from __future__ import annotations

from typing import Any, Protocol


class SettingsRepository(Protocol):
    async def get_business_hours_doc(self) -> dict | None: ...

    async def save_business_hours_doc(self, doc: dict) -> None: ...

    async def get_report_sections_doc(self) -> dict | None: ...

    async def save_report_sections_doc(self, doc: dict) -> None: ...


# ── Mongo implementation ────────────────────────────────────────────────────


_BUSINESS_HOURS_ID = "business_hours"
_REPORT_SECTIONS_ID = "report_sections"


class MongoSettingsRepository:
    def __init__(self, db: Any) -> None:
        self._db = db

    @property
    def _coll(self):
        return self._db.settings

    async def get_business_hours_doc(self) -> dict | None:
        return await self._coll.find_one({"_id": _BUSINESS_HOURS_ID})

    async def save_business_hours_doc(self, doc: dict) -> None:
        doc["_id"] = _BUSINESS_HOURS_ID
        await self._coll.replace_one({"_id": _BUSINESS_HOURS_ID}, doc, upsert=True)

    async def get_report_sections_doc(self) -> dict | None:
        return await self._coll.find_one({"_id": _REPORT_SECTIONS_ID})

    async def save_report_sections_doc(self, doc: dict) -> None:
        doc["_id"] = _REPORT_SECTIONS_ID
        await self._coll.replace_one({"_id": _REPORT_SECTIONS_ID}, doc, upsert=True)
