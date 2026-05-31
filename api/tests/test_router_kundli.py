"""Tests for the Kundli router (SQS-enqueue pattern).

The endpoint inserts a `pending` record + enqueues an SQS message, then
returns 202. The Lambda worker (covered by `test_workers_kundli_lambda`)
picks up the message and runs the heavy work.

These tests cover:

1. Happy path returns 202 with the "being generated" message.
2. Rate limit returns 429 when 10 records already exist for this email.
3. A pending record is inserted before the 202 response.
4. The pending record carries an `expires_at` ~24h in the future
   (TTL fallback if SQS / Lambda never processes it).
5. The SQS payload contains record_id + the full request fields.
6. SQS enqueue failure → 500 (and the orphan pending row is left for
   the TTL index to reap).
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest
from bson import ObjectId

from app.dependencies import get_message_queue
from app.main import app


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


@pytest.fixture(autouse=True)
def override_queue(fake_queue):
    """Every kundli router test gets the FakeMessageQueue injected."""
    app.dependency_overrides[get_message_queue] = lambda: fake_queue
    yield fake_queue
    app.dependency_overrides.pop(get_message_queue, None)


# ── Endpoint tests ─────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_generate_returns_202_immediately(client, mock_db, fake_queue):
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
    # SQS enqueue happened — exactly one message in the fake queue.
    assert len(fake_queue.sent) == 1


@pytest.mark.asyncio
async def test_generate_rate_limit_returns_429(client, mock_db, fake_queue):
    """10 records in the last 24h → 429, no insert, no enqueue."""
    mock_db.kundlis.count_documents = AsyncMock(return_value=10)

    resp = await client.post("/api/kundli/generate", json=SAMPLE_REQUEST)

    assert resp.status_code == 429
    assert "maximum" in resp.json()["detail"].lower()
    mock_db.kundlis.insert_one.assert_not_awaited()
    assert len(fake_queue.sent) == 0


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
async def test_pending_record_carries_24h_expires_at(client, mock_db):
    """TTL safety net: the pending insert sets expires_at = now + 24h."""
    mock_db.kundlis.count_documents = AsyncMock(return_value=0)
    mock_db.kundlis.insert_one = AsyncMock(
        return_value=MagicMock(inserted_id=ObjectId())
    )

    before = datetime.now(timezone.utc)
    resp = await client.post("/api/kundli/generate", json=SAMPLE_REQUEST)
    after = datetime.now(timezone.utc)

    assert resp.status_code == 202
    inserted_doc = mock_db.kundlis.insert_one.call_args.args[0]
    expires_at = inserted_doc["expires_at"]
    assert expires_at is not None
    # Allow ±5s of slack on each side for the call latency.
    assert before + timedelta(hours=24, seconds=-5) <= expires_at
    assert expires_at <= after + timedelta(hours=24, seconds=5)


@pytest.mark.asyncio
async def test_generate_enqueues_payload_with_record_id_and_fields(
    client, mock_db, fake_queue
):
    inserted_id = ObjectId()
    mock_db.kundlis.count_documents = AsyncMock(return_value=0)
    mock_db.kundlis.insert_one = AsyncMock(
        return_value=MagicMock(inserted_id=inserted_id)
    )

    resp = await client.post("/api/kundli/generate", json=SAMPLE_REQUEST)
    assert resp.status_code == 202

    assert len(fake_queue.sent) == 1
    payload = fake_queue.sent[0]
    assert payload["record_id"] == str(inserted_id)
    # The request fields all round-trip into the message body.
    for key, value in SAMPLE_REQUEST.items():
        assert payload[key] == value


@pytest.mark.asyncio
async def test_generate_returns_500_on_enqueue_failure(client, mock_db, fake_queue):
    """SQS error → 500. Pending row stays — TTL reaps it within 24h."""
    fake_queue.raise_on_send = RuntimeError("SQS unavailable")
    mock_db.kundlis.count_documents = AsyncMock(return_value=0)
    mock_db.kundlis.insert_one = AsyncMock(
        return_value=MagicMock(inserted_id=ObjectId())
    )

    resp = await client.post("/api/kundli/generate", json=SAMPLE_REQUEST)

    assert resp.status_code == 500
    assert "queue your kundli" in resp.json()["detail"].lower()
    # Insert still happened — the orphan will TTL out.
    mock_db.kundlis.insert_one.assert_awaited_once()


@pytest.mark.asyncio
async def test_invalid_email_returns_422(client, mock_db, fake_queue):
    """Pydantic validation rejects invalid emails before any DB call."""
    bad = dict(SAMPLE_REQUEST)
    bad["email"] = "not-an-email"

    resp = await client.post("/api/kundli/generate", json=bad)

    assert resp.status_code == 422
    mock_db.kundlis.insert_one.assert_not_awaited()
    assert len(fake_queue.sent) == 0
