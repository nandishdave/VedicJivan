"""Auth use cases — registration, login, refresh, profile.

Domain rules:
  - Email must be unique on register
  - Login compares stored bcrypt hash
  - Refresh requires a token whose `type` is `refresh`
"""

from __future__ import annotations

from app.domain.exceptions import (
    AuthenticationFailedError,
    BookingValidationError,
    EntityNotFoundError,
)
from app.models.user import UserInDB, UserResponse
from app.repositories.user_repository import UserRepository
from app.utils.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)


def _issue_tokens(user_id: str) -> tuple[str, str]:
    return (
        create_access_token({"sub": user_id}),
        create_refresh_token({"sub": user_id}),
    )


# ── RegisterUser ──────────────────────────────────────────────────────────


class RegisterUser:
    def __init__(self, user_repo: UserRepository) -> None:
        self._repo = user_repo

    async def execute(
        self, *, name: str, email: str, password: str, phone: str = ""
    ) -> tuple[str, str]:
        if await self._repo.find_by_email(email):
            raise BookingValidationError("Email already registered")
        user = UserInDB(
            name=name,
            email=email,
            password_hash=hash_password(password),
            phone=phone,
        )
        inserted_id = await self._repo.insert(user)
        return _issue_tokens(str(inserted_id))


# ── LoginUser ──────────────────────────────────────────────────────────────


class LoginUser:
    def __init__(self, user_repo: UserRepository) -> None:
        self._repo = user_repo

    async def execute(self, *, email: str, password: str) -> tuple[str, str]:
        user = await self._repo.find_by_email(email)
        if not user or not verify_password(password, user["password_hash"]):
            raise AuthenticationFailedError("Invalid email or password")
        return _issue_tokens(str(user["_id"]))


# ── RefreshTokens ─────────────────────────────────────────────────────────


class RefreshTokens:
    def __init__(self, user_repo: UserRepository) -> None:
        self._repo = user_repo

    async def execute(self, *, refresh_token: str) -> tuple[str, str]:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise AuthenticationFailedError("Invalid refresh token")
        user = await self._repo.find_by_id(payload["sub"])
        if not user:
            raise AuthenticationFailedError("User not found")
        return _issue_tokens(str(user["_id"]))


# ── GetMyProfile ──────────────────────────────────────────────────────────


class GetMyProfile:
    def __init__(self, user_repo: UserRepository) -> None:
        self._repo = user_repo

    async def execute(self, *, user_id: str) -> UserResponse:
        user = await self._repo.find_by_id(user_id)
        if not user:
            raise EntityNotFoundError("User not found")
        return UserResponse(
            id=str(user["_id"]),
            name=user["name"],
            email=user["email"],
            phone=user.get("phone", ""),
            role=user["role"],
            created_at=user["created_at"],
        )
