"""Payment repository — Protocol interface + Mongo implementation.

Mirrors the booking repository pattern. Use cases depend on the Protocol;
production wires `MongoPaymentRepository`. The repo encapsulates ALL Mongo
query construction for the `payments` collection — anything outside this
module that touches `db.payments.*` is a smell.
"""

from __future__ import annotations

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
