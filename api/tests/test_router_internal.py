"""Tests for app.routers.internal — booking reminder endpoint."""

import os
from datetime import date, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from bson import ObjectId

from tests.conftest import MockAggregationCursor

# Set INTERNAL_SECRET before app imports
os.environ["INTERNAL_SECRET"] = "test-secret-123"


TOMORROW = (date.today() + timedelta(days=1)).isoformat()

CONFIRMED_BOOKING = {
    "_id": ObjectId("507f1f77bcf86cd799439099"),
    "user_name": "Test User",
    "user_email": "test@example.com",
    "service_title": "Call Consultation",
    "date": TOMORROW,
    "time_slot": "10:00",
    "duration_minutes": 30,
    "price_inr": 1999,
    "status": "confirmed",
    "reminder_sent": False,
}


async def test_send_reminders_requires_secret(client):
    resp = await client.post("/api/internal/send-reminders")
    assert resp.status_code == 403


async def test_send_reminders_wrong_secret(client):
    resp = await client.post(
        "/api/internal/send-reminders",
        headers={"X-Internal-Secret": "wrong-secret"},
    )
    assert resp.status_code == 403


async def test_send_reminders_no_bookings(client, mock_db):
    mock_db.bookings.find = MagicMock(return_value=MockAggregationCursor([]))

    with patch("app.config.settings.INTERNAL_SECRET", "test-secret-123"):
        resp = await client.post(
            "/api/internal/send-reminders",
            headers={"X-Internal-Secret": "test-secret-123"},
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["sent"] == 0
    assert data["date"] == TOMORROW


async def test_send_reminders_sends_email_and_marks_sent(client, mock_db):
    mock_db.bookings.find = MagicMock(
        return_value=MockAggregationCursor([CONFIRMED_BOOKING])
    )
    mock_db.bookings.update_one = AsyncMock(return_value=MagicMock(modified_count=1))

    with patch("app.config.settings.INTERNAL_SECRET", "test-secret-123"), patch(
        "app.routers.internal.send_booking_reminder", new_callable=AsyncMock
    ) as mock_send:
        resp = await client.post(
            "/api/internal/send-reminders",
            headers={"X-Internal-Secret": "test-secret-123"},
        )

    assert resp.status_code == 200
    assert resp.json()["sent"] == 1
    mock_send.assert_awaited_once()
    mock_db.bookings.update_one.assert_awaited_once()


async def test_send_reminders_continues_on_email_failure(client, mock_db):
    """If one email fails, the endpoint should still return 200 with sent=0."""
    mock_db.bookings.find = MagicMock(
        return_value=MockAggregationCursor([CONFIRMED_BOOKING])
    )

    with patch("app.config.settings.INTERNAL_SECRET", "test-secret-123"), patch(
        "app.routers.internal.send_booking_reminder",
        new_callable=AsyncMock,
        side_effect=Exception("SMTP error"),
    ):
        resp = await client.post(
            "/api/internal/send-reminders",
            headers={"X-Internal-Secret": "test-secret-123"},
        )

    assert resp.status_code == 200
    assert resp.json()["sent"] == 0


async def test_send_reminders_response_includes_date(client, mock_db):
    mock_db.bookings.find = MagicMock(return_value=MockAggregationCursor([]))

    with patch("app.config.settings.INTERNAL_SECRET", "test-secret-123"):
        resp = await client.post(
            "/api/internal/send-reminders",
            headers={"X-Internal-Secret": "test-secret-123"},
        )

    assert resp.json()["date"] == TOMORROW
