"""Tests for app.routers.auth — register, login, refresh, me."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from bson import ObjectId

from app.utils.security import create_access_token, create_refresh_token, hash_password
from tests.conftest import ADMIN_ID, USER_ID


async def test_register_success(client, mock_db):
    mock_db.users.find_one = AsyncMock(return_value=None)
    mock_db.users.insert_one = AsyncMock(return_value=MagicMock(inserted_id=ObjectId()))

    resp = await client.post(
        "/api/auth/register",
        json={
            "name": "New User",
            "email": "new@test.com",
            "password": "Password123",
            "phone": "1234567890",
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


async def test_register_duplicate_email(client, mock_db, sample_user_doc):
    mock_db.users.find_one = AsyncMock(return_value=sample_user_doc)

    resp = await client.post(
        "/api/auth/register",
        json={
            "name": "Duplicate",
            "email": "test@example.com",
            "password": "Password123",
        },
    )
    assert resp.status_code == 400
    assert "already registered" in resp.json()["detail"].lower()


async def test_register_invalid_email(client, mock_db):
    resp = await client.post(
        "/api/auth/register",
        json={"name": "Bad", "email": "invalid", "password": "Password123"},
    )
    assert resp.status_code == 422


async def test_register_short_password(client, mock_db):
    resp = await client.post(
        "/api/auth/register",
        json={"name": "User", "email": "a@b.com", "password": "short"},
    )
    assert resp.status_code == 422


async def test_register_short_name(client, mock_db):
    resp = await client.post(
        "/api/auth/register",
        json={"name": "A", "email": "a@b.com", "password": "Password123"},
    )
    assert resp.status_code == 422


async def test_login_success(client, mock_db, sample_user_doc):
    # find_one for login returns the user doc
    mock_db.users.find_one = AsyncMock(return_value=sample_user_doc)

    resp = await client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "Password123"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data


async def test_login_wrong_password(client, mock_db, sample_user_doc):
    mock_db.users.find_one = AsyncMock(return_value=sample_user_doc)

    resp = await client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "WrongPass123"},
    )
    assert resp.status_code == 401


async def test_login_nonexistent_email(client, mock_db):
    mock_db.users.find_one = AsyncMock(return_value=None)

    resp = await client.post(
        "/api/auth/login",
        json={"email": "nobody@test.com", "password": "Password123"},
    )
    assert resp.status_code == 401


async def test_refresh_success(client, mock_db, sample_user_doc):
    token = create_refresh_token({"sub": str(USER_ID)})
    mock_db.users.find_one = AsyncMock(return_value=sample_user_doc)

    resp = await client.post(
        "/api/auth/refresh",
        json={"refresh_token": token},
    )
    assert resp.status_code == 200
    assert "access_token" in resp.json()


async def test_refresh_with_access_token_fails(client, mock_db):
    token = create_access_token({"sub": str(USER_ID)})

    resp = await client.post(
        "/api/auth/refresh",
        json={"refresh_token": token},
    )
    assert resp.status_code == 401


async def test_refresh_with_invalid_token(client, mock_db):
    resp = await client.post(
        "/api/auth/refresh",
        json={"refresh_token": "invalid.token"},
    )
    assert resp.status_code == 401


async def test_refresh_user_deleted(client, mock_db):
    token = create_refresh_token({"sub": str(ObjectId())})
    mock_db.users.find_one = AsyncMock(return_value=None)

    resp = await client.post(
        "/api/auth/refresh",
        json={"refresh_token": token},
    )
    assert resp.status_code == 401


async def test_get_me_authenticated(client, mock_db, user_token, sample_user_doc):
    resp = await client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"
    assert data["role"] == "user"


async def test_get_me_no_token(client, mock_db):
    resp = await client.get("/api/auth/me")
    assert resp.status_code == 422
