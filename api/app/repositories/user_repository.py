"""User repository — Protocol + Mongo implementation."""

from __future__ import annotations

from typing import Any, Protocol

from bson import ObjectId
from bson.errors import InvalidId

from app.models.user import UserInDB


class UserRepository(Protocol):
    async def find_by_email(self, email: str) -> dict | None: ...

    async def find_by_id(self, user_id: str | ObjectId) -> dict | None: ...

    async def insert(self, user: UserInDB) -> ObjectId: ...

    async def count(self) -> int: ...

    async def ensure_indexes(self) -> None: ...


# ── Mongo implementation ────────────────────────────────────────────────────


def _to_object_id(value: str | ObjectId) -> ObjectId | None:
    if isinstance(value, ObjectId):
        return value
    try:
        return ObjectId(value)
    except (InvalidId, TypeError):
        return None


class MongoUserRepository:
    def __init__(self, db: Any) -> None:
        self._db = db

    @property
    def _users(self):
        return self._db.users

    async def find_by_email(self, email: str) -> dict | None:
        return await self._users.find_one({"email": email})

    async def find_by_id(self, user_id: str | ObjectId) -> dict | None:
        oid = _to_object_id(user_id)
        if oid is None:
            return None
        return await self._users.find_one({"_id": oid})

    async def insert(self, user: UserInDB) -> ObjectId:
        result = await self._users.insert_one(user.model_dump())
        return result.inserted_id

    async def count(self) -> int:
        return await self._users.count_documents({})

    async def ensure_indexes(self) -> None:
        # UNIQUE on email — login lookup + duplicate-account prevention.
        await self._users.create_index([("email", 1)], unique=True)
