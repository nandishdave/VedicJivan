"""Payment repository — Protocol interface + Mongo implementation.

Mirrors the booking repository pattern. Use cases depend on the Protocol;
production wires `MongoPaymentRepository`. The repo encapsulates ALL Mongo
query construction for the `payments` collection — anything outside this
module that touches `db.payments.*` is a smell.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Protocol

from app.models.payment import PaymentInDB, PaymentStatus


class PaymentRepository(Protocol):
    """Storage interface for payments — implemented by MongoPaymentRepository."""

    async def insert(self, payment: PaymentInDB) -> None: ...

    async def find_by_session_id(self, session_id: str) -> dict | None: ...

    async def mark_captured(
        self,
        session_id: str,
        *,
        payment_intent_id: str | None,
    ) -> int: ...

    async def mark_expired(self, session_id: str) -> int: ...

    async def mark_refunded(self, payment_intent_id: str) -> int: ...

    async def list_recent(self, limit: int = 100) -> list[dict]: ...

    async def count_captured(self) -> int: ...

    async def total_captured_amount(self) -> int: ...

    async def aggregate_daily_captured_amount(
        self, since: datetime
    ) -> dict[str, int]: ...


# ── Mongo implementation ────────────────────────────────────────────────────


class MongoPaymentRepository:
    """Production repository — wraps the `payments` collection on Motor."""

    def __init__(self, db: Any) -> None:
        self._db = db

    @property
    def _payments(self):
        return self._db.payments

    async def insert(self, payment: PaymentInDB) -> None:
        await self._payments.insert_one(payment.model_dump())

    async def find_by_session_id(self, session_id: str) -> dict | None:
        return await self._payments.find_one({"stripe_session_id": session_id})

    async def mark_captured(
        self,
        session_id: str,
        *,
        payment_intent_id: str | None,
    ) -> int:
        result = await self._payments.update_one(
            {"stripe_session_id": session_id},
            {
                "$set": {
                    "stripe_payment_intent_id": payment_intent_id,
                    "status": PaymentStatus.CAPTURED,
                }
            },
        )
        return result.modified_count

    async def mark_expired(self, session_id: str) -> int:
        result = await self._payments.update_one(
            {"stripe_session_id": session_id},
            {"$set": {"status": PaymentStatus.EXPIRED}},
        )
        return result.modified_count

    async def mark_refunded(self, payment_intent_id: str) -> int:
        result = await self._payments.update_one(
            {"stripe_payment_intent_id": payment_intent_id},
            {"$set": {"status": PaymentStatus.REFUNDED}},
        )
        return result.modified_count

    async def list_recent(self, limit: int = 100) -> list[dict]:
        cursor = self._payments.find().sort("created_at", -1).limit(limit)
        return [doc async for doc in cursor]

    async def count_captured(self) -> int:
        return await self._payments.count_documents({"status": "captured"})

    async def total_captured_amount(self) -> int:
        # Legacy field name `amount_inr` matches the existing aggregation in
        # routers/admin.py — keep until the data is migrated to `amount`.
        pipeline = [
            {"$match": {"status": "captured"}},
            {"$group": {"_id": None, "total": {"$sum": "$amount_inr"}}},
        ]
        result = await self._payments.aggregate(pipeline).to_list(1)
        return result[0]["total"] if result else 0

    async def aggregate_daily_captured_amount(
        self, since: datetime
    ) -> dict[str, int]:
        pipeline = [
            {
                "$match": {
                    "status": "captured",
                    "created_at": {"$gte": since},
                }
            },
            {
                "$group": {
                    "_id": {
                        "$dateToString": {
                            "format": "%Y-%m-%d",
                            "date": "$created_at",
                        }
                    },
                    "revenue": {"$sum": "$amount_inr"},
                }
            },
            {"$sort": {"_id": 1}},
        ]
        result: dict[str, int] = {}
        async for doc in self._payments.aggregate(pipeline):
            result[doc["_id"]] = doc["revenue"]
        return result
