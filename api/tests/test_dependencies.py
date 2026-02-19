"""Tests for app.dependencies — auth middleware and role checking."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from bson import ObjectId

from app.dependencies import get_current_user, require_admin
from app.utils.exceptions import ForbiddenError, UnauthorizedError
from app.utils.security import create_access_token, create_refresh_token

from tests.conftest import USER_ID, ADMIN_ID


@pytest.fixture
def user_doc():
    return {
        "_id": USER_ID,
        "name": "Test User",
        "email": "test@example.com",
        "role": "user",
    }


@pytest.fixture
def admin_doc():
    return {
        "_id": ADMIN_ID,
        "name": "Admin User",
        "email": "admin@example.com",
        "role": "admin",
    }


# ── get_current_user ──


async def test_get_current_user_valid_token(user_doc):
    token = create_access_token({"sub": str(USER_ID)})
    mock_db = MagicMock()
    mock_db.users.find_one = AsyncMock(return_value=user_doc)

    with patch("app.dependencies.get_db", return_value=mock_db):
        result = await get_current_user(f"Bearer {token}")

    assert result["id"] == str(USER_ID)
    assert result["email"] == "test@example.com"
    assert result["role"] == "user"


async def test_get_current_user_no_bearer_prefix():
    with pytest.raises(UnauthorizedError):
        await get_current_user("Token abc123")


async def test_get_current_user_invalid_token():
    with pytest.raises(UnauthorizedError):
        await get_current_user("Bearer invalid.token.here")


async def test_get_current_user_expired_token():
    from datetime import datetime, timedelta, timezone
    from jose import jwt
    from app.config import settings

    data = {
        "sub": str(USER_ID),
        "exp": datetime.now(timezone.utc) - timedelta(hours=1),
        "type": "access",
    }
    token = jwt.encode(data, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    with pytest.raises(UnauthorizedError):
        await get_current_user(f"Bearer {token}")


async def test_get_current_user_refresh_token_rejected():
    token = create_refresh_token({"sub": str(USER_ID)})
    with pytest.raises(UnauthorizedError):
        await get_current_user(f"Bearer {token}")


async def test_get_current_user_user_not_in_db():
    token = create_access_token({"sub": str(USER_ID)})
    mock_db = MagicMock()
    mock_db.users.find_one = AsyncMock(return_value=None)

    with patch("app.dependencies.get_db", return_value=mock_db):
        with pytest.raises(UnauthorizedError):
            await get_current_user(f"Bearer {token}")


# ── require_admin ──


async def test_require_admin_admin_passes():
    admin_user = {"id": str(ADMIN_ID), "email": "admin@test.com", "name": "Admin", "role": "admin"}
    result = await require_admin(admin_user)
    assert result["role"] == "admin"


async def test_require_admin_regular_user_rejected():
    user = {"id": str(USER_ID), "email": "user@test.com", "name": "User", "role": "user"}
    with pytest.raises(ForbiddenError):
        await require_admin(user)
