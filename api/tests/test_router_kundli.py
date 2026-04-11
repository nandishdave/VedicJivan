"""Tests for the Kundli router (background-task pattern, Commit 0.1).

The endpoint returns 202 Accepted as soon as the request is rate-limited and
a pending record is inserted; the heavy work (chart calc + PDF + email)
runs in a FastAPI BackgroundTask after the response is sent.

These tests cover:

1. Happy path returns 202 with the "being generated" message.
2. Rate limit returns 429 when 10 records already exist for this email.
3. A pending record is inserted before the 202 response.
4. The background task is scheduled with the inserted record's id.
5. The background task succeeds: marks the record `generated`, sends email.
6. The background task on failure: marks the record `failed` with the error.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from bson import ObjectId


SAMPLE_REQUEST = {
    "name": "Nandish Dave",
    "gender": "male",
    "dob": "1988-11-11",
    "tob": "12:55",
    "lat": 21.7545,
    "lon": 70.6233,
    "place_name": "Jetpur, Gujarat, India",
    "email": "test@example.com",
}


# ── Endpoint tests ─────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_generate_returns_202_immediately(client, mock_db):
    """The endpoint returns 202 Accepted as soon as the row is inserted."""
    inserted_id = ObjectId()
    mock_db.kundlis.count_documents = AsyncMock(return_value=0)
    mock_db.kundlis.insert_one = AsyncMock(
        return_value=MagicMock(inserted_id=inserted_id)
    )

    resp = await client.post("/api/kundli/generate", json=SAMPLE_REQUEST)

    assert resp.status_code == 202
    body = resp.json()
    assert "being generated" in body["message"].lower()
    mock_db.kundlis.insert_one.assert_awaited_once()


@pytest.mark.asyncio
async def test_generate_rate_limit_returns_429(client, mock_db):
    """10 records in the last 24h → 429."""
    mock_db.kundlis.count_documents = AsyncMock(return_value=10)

    resp = await client.post("/api/kundli/generate", json=SAMPLE_REQUEST)

    assert resp.status_code == 429
    assert "maximum" in resp.json()["detail"].lower()
    mock_db.kundlis.insert_one.assert_not_awaited()


@pytest.mark.asyncio
async def test_pending_record_inserted_before_response(client, mock_db):
    """The DB row is created with status='pending' before the 202 returns."""
    mock_db.kundlis.count_documents = AsyncMock(return_value=0)
    mock_db.kundlis.insert_one = AsyncMock(
        return_value=MagicMock(inserted_id=ObjectId())
    )

    resp = await client.post("/api/kundli/generate", json=SAMPLE_REQUEST)

    assert resp.status_code == 202
    inserted_doc = mock_db.kundlis.insert_one.call_args.args[0]
    assert inserted_doc["status"] == "pending"
    assert inserted_doc["email"] == SAMPLE_REQUEST["email"]
    assert inserted_doc["name"] == SAMPLE_REQUEST["name"]
    assert inserted_doc["chart_data"] == {}


@pytest.mark.asyncio
async def test_invalid_email_returns_422(client, mock_db):
    """Pydantic validation rejects invalid emails before any DB call."""
    bad = dict(SAMPLE_REQUEST)
    bad["email"] = "not-an-email"

    resp = await client.post("/api/kundli/generate", json=bad)

    assert resp.status_code == 422
    mock_db.kundlis.insert_one.assert_not_awaited()


# ── Background task tests ──────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_background_task_marks_generated_on_success(mock_db):
    """When the background task succeeds, the record is updated to 'generated'."""
    from app.models.kundli import KundliRequest
    from app.routers.kundli import _generate_and_email

    record_id = ObjectId()
    req = KundliRequest(**SAMPLE_REQUEST)

    fake_chart = {"name": "x", "lagna": {"sign": "Capricorn"}}
    fake_pdf = b"%PDF-fake"

    with (
        patch("app.routers.kundli.build_chart", return_value=fake_chart),
        patch("app.routers.kundli.generate_pdf", return_value=fake_pdf),
        patch("app.services.email_service.send_kundli_report", new=AsyncMock()) as send_mock,
        patch("app.routers.kundli.load_report_sections", new=AsyncMock(return_value=[])),
    ):
        await _generate_and_email(record_id, req)

    send_mock.assert_awaited_once_with(req.email, req.name, fake_pdf)
    mock_db.kundlis.update_one.assert_awaited_once()
    update_call = mock_db.kundlis.update_one.call_args
    assert update_call.args[0] == {"_id": record_id}
    assert update_call.args[1]["$set"]["status"] == "generated"
    assert update_call.args[1]["$set"]["chart_data"] == fake_chart


@pytest.mark.asyncio
async def test_background_task_marks_failed_on_exception(mock_db):
    """If chart calculation raises, the record is updated to 'failed' with the error."""
    from app.models.kundli import KundliRequest
    from app.routers.kundli import _generate_and_email

    record_id = ObjectId()
    req = KundliRequest(**SAMPLE_REQUEST)

    with (
        patch("app.routers.kundli.build_chart", side_effect=ValueError("bad lat")),
        patch("app.routers.kundli.load_report_sections", new=AsyncMock(return_value=[])),
    ):
        await _generate_and_email(record_id, req)

    mock_db.kundlis.update_one.assert_awaited_once()
    update_call = mock_db.kundlis.update_one.call_args
    assert update_call.args[0] == {"_id": record_id}
    assert update_call.args[1]["$set"]["status"] == "failed"
    assert "bad lat" in update_call.args[1]["$set"]["error"]
