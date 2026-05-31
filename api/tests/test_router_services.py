"""Tests for app.routers.services — public catalogue + admin CRUD."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest
from bson import ObjectId

from tests.conftest import MockCursor


_SAMPLE_SERVICE_DOC = {
    "_id": ObjectId(),
    "slug": "call-consultation",
    "title": "Call Consultation",
    "durations": [
        {"duration_minutes": 30, "price_inr": 1999, "price_eur": 29},
        {"duration_minutes": 45, "price_inr": 2499, "price_eur": 35},
    ],
}


# ── List ──


async def test_list_services_returns_collection(client, mock_db):
    mock_db.services.find = MagicMock(return_value=MockCursor([_SAMPLE_SERVICE_DOC]))
    resp = await client.get("/api/services")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["slug"] == "call-consultation"
    assert data[0]["durations"][0]["price_inr"] == 1999


async def test_list_services_empty(client, mock_db):
    mock_db.services.find = MagicMock(return_value=MockCursor([]))
    resp = await client.get("/api/services")
    assert resp.status_code == 200
    assert resp.json() == []


# ── Get one ──


async def test_get_service_by_slug(client, mock_db):
    # The conftest already wires `services.find_one` against DEFAULT_SERVICES,
    # so this resolves to the seeded "call-consultation" entry.
    resp = await client.get("/api/services/call-consultation")
    assert resp.status_code == 200
    data = resp.json()
    assert data["slug"] == "call-consultation"
    assert any(d["duration_minutes"] == 30 for d in data["durations"])


async def test_get_service_unknown_slug_returns_404(client, mock_db):
    resp = await client.get("/api/services/does-not-exist")
    assert resp.status_code == 404


# ── Upsert (admin) ──


async def test_upsert_service_creates_new(client, mock_db, admin_token):
    mock_db.services.update_one = AsyncMock(return_value=MagicMock(upserted_id=ObjectId()))
    payload = {
        "slug": "brand-new",
        "title": "Brand New Service",
        "durations": [{"duration_minutes": 60, "price_inr": 3500, "price_eur": 42}],
    }

    async def _find(query):
        if query == {"slug": "brand-new"}:
            return {**payload, "_id": ObjectId()}
        return None

    mock_db.services.find_one = AsyncMock(side_effect=_find)

    resp = await client.put(
        "/api/services/brand-new",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 200
    assert resp.json()["slug"] == "brand-new"
    mock_db.services.update_one.assert_awaited_once()


async def test_upsert_service_slug_mismatch_returns_400(client, mock_db, admin_token):
    payload = {
        "slug": "different-slug",
        "durations": [{"duration_minutes": 30, "price_inr": 100, "price_eur": 1}],
    }
    resp = await client.put(
        "/api/services/url-slug",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 400
    assert "mismatch" in resp.json()["detail"].lower()


async def test_upsert_service_requires_admin(client, mock_db, user_token):
    payload = {
        "slug": "any",
        "durations": [{"duration_minutes": 30, "price_inr": 100, "price_eur": 1}],
    }
    resp = await client.put(
        "/api/services/any",
        json=payload,
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 403


# ── Delete (admin) ──


async def test_delete_service_success(client, mock_db, admin_token):
    mock_db.services.delete_one = AsyncMock(return_value=MagicMock(deleted_count=1))
    resp = await client.delete(
        "/api/services/call-consultation",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 200
    assert resp.json()["message"] == "Removed"


async def test_delete_service_not_found_returns_404(client, mock_db, admin_token):
    mock_db.services.delete_one = AsyncMock(return_value=MagicMock(deleted_count=0))
    resp = await client.delete(
        "/api/services/nope",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 404


async def test_delete_service_requires_admin(client, mock_db, user_token):
    resp = await client.delete(
        "/api/services/call-consultation",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 403
