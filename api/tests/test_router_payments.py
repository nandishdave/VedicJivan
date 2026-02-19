"""Tests for app.routers.payments — Razorpay order, verify, webhook."""

import hashlib
import hmac
import json

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from bson import ObjectId

from app.config import settings
from tests.conftest import BOOKING_ID, MockCursor


def _make_valid_signature(order_id: str, payment_id: str) -> str:
    """Generate a valid HMAC SHA256 signature for Razorpay verification."""
    message = f"{order_id}|{payment_id}"
    return hmac.new(
        settings.RAZORPAY_KEY_SECRET.encode(),
        message.encode(),
        hashlib.sha256,
    ).hexdigest()


# ── Create order ──


async def test_create_order_success(client, mock_db):
    mock_db.bookings.find_one = AsyncMock(
        return_value={"_id": BOOKING_ID, "status": "pending", "service_title": "Call"}
    )
    mock_db.payments.insert_one = AsyncMock(return_value=MagicMock(inserted_id=ObjectId()))

    mock_razorpay = MagicMock()
    mock_razorpay.order.create.return_value = {
        "id": "order_test123",
        "amount": 199900,
        "currency": "INR",
    }

    with patch("app.routers.payments.get_razorpay_client", return_value=mock_razorpay):
        resp = await client.post(
            "/api/payments/create-order",
            json={"booking_id": str(BOOKING_ID), "amount_inr": 1999},
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["order_id"] == "order_test123"
    assert data["key_id"] == settings.RAZORPAY_KEY_ID


async def test_create_order_booking_not_found(client, mock_db):
    mock_db.bookings.find_one = AsyncMock(return_value=None)

    resp = await client.post(
        "/api/payments/create-order",
        json={"booking_id": str(ObjectId()), "amount_inr": 1999},
    )
    assert resp.status_code == 404


async def test_create_order_already_confirmed(client, mock_db):
    mock_db.bookings.find_one = AsyncMock(
        return_value={"_id": BOOKING_ID, "status": "confirmed", "service_title": "Call"}
    )

    resp = await client.post(
        "/api/payments/create-order",
        json={"booking_id": str(BOOKING_ID), "amount_inr": 1999},
    )
    assert resp.status_code == 400


# ── Verify payment ──


async def test_verify_payment_valid_signature(client, mock_db):
    order_id = "order_test123"
    payment_id = "pay_test456"
    signature = _make_valid_signature(order_id, payment_id)

    mock_db.bookings.find_one = AsyncMock(
        return_value={
            "_id": BOOKING_ID,
            "user_email": "test@example.com",
            "user_name": "Test",
            "user_phone": "1234567890",
            "service_title": "Call",
            "date": "2026-03-15",
            "time_slot": "10:00",
            "duration_minutes": 30,
            "price_inr": 1999,
        }
    )

    with patch("app.routers.payments.send_booking_confirmation", new_callable=AsyncMock), \
         patch("app.routers.payments.send_admin_booking_notification", new_callable=AsyncMock):
        resp = await client.post(
            "/api/payments/verify",
            json={
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature,
                "booking_id": str(BOOKING_ID),
            },
        )

    assert resp.status_code == 200
    assert resp.json()["status"] == "success"


async def test_verify_payment_invalid_signature(client, mock_db):
    resp = await client.post(
        "/api/payments/verify",
        json={
            "razorpay_order_id": "order_123",
            "razorpay_payment_id": "pay_456",
            "razorpay_signature": "invalid_signature",
            "booking_id": str(BOOKING_ID),
        },
    )
    assert resp.status_code == 400


async def test_verify_payment_sends_emails(client, mock_db):
    order_id = "order_email_test"
    payment_id = "pay_email_test"
    signature = _make_valid_signature(order_id, payment_id)

    mock_db.bookings.find_one = AsyncMock(
        return_value={
            "_id": BOOKING_ID,
            "user_email": "test@example.com",
            "user_name": "Test",
            "user_phone": "1234567890",
            "service_title": "Call",
            "date": "2026-03-15",
            "time_slot": "10:00",
            "duration_minutes": 30,
            "price_inr": 1999,
        }
    )

    mock_confirm = AsyncMock()
    mock_admin_notify = AsyncMock()

    with patch("app.routers.payments.send_booking_confirmation", mock_confirm), \
         patch("app.routers.payments.send_admin_booking_notification", mock_admin_notify):
        await client.post(
            "/api/payments/verify",
            json={
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature,
                "booking_id": str(BOOKING_ID),
            },
        )

    mock_confirm.assert_called_once()
    mock_admin_notify.assert_called_once()


async def test_verify_payment_email_failure_does_not_break(client, mock_db):
    order_id = "order_email_fail"
    payment_id = "pay_email_fail"
    signature = _make_valid_signature(order_id, payment_id)

    mock_db.bookings.find_one = AsyncMock(
        return_value={
            "_id": BOOKING_ID,
            "user_email": "test@example.com",
            "user_name": "Test",
            "user_phone": "1234567890",
            "service_title": "Call",
            "date": "2026-03-15",
            "time_slot": "10:00",
            "duration_minutes": 30,
            "price_inr": 1999,
        }
    )

    with patch("app.routers.payments.send_booking_confirmation", AsyncMock(side_effect=Exception("SMTP error"))), \
         patch("app.routers.payments.send_admin_booking_notification", AsyncMock(side_effect=Exception("SMTP error"))):
        resp = await client.post(
            "/api/payments/verify",
            json={
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature,
                "booking_id": str(BOOKING_ID),
            },
        )

    assert resp.status_code == 200


# ── Webhook ──


async def test_webhook_payment_captured(client, mock_db):
    payload = {
        "event": "payment.captured",
        "payload": {
            "payment": {
                "entity": {"id": "pay_123", "order_id": "order_123"}
            }
        },
    }

    with patch.object(settings, "RAZORPAY_WEBHOOK_SECRET", ""):
        resp = await client.post(
            "/api/payments/webhook",
            content=json.dumps(payload),
            headers={"Content-Type": "application/json"},
        )

    assert resp.status_code == 200
    mock_db.payments.update_one.assert_called_once()


async def test_webhook_refund_created(client, mock_db):
    payload = {
        "event": "refund.created",
        "payload": {
            "refund": {
                "entity": {"payment_id": "pay_456"}
            }
        },
    }

    with patch.object(settings, "RAZORPAY_WEBHOOK_SECRET", ""):
        resp = await client.post(
            "/api/payments/webhook",
            content=json.dumps(payload),
            headers={"Content-Type": "application/json"},
        )

    assert resp.status_code == 200
    mock_db.payments.update_one.assert_called_once()


async def test_webhook_invalid_signature(client, mock_db):
    payload = {"event": "payment.captured", "payload": {}}

    with patch.object(settings, "RAZORPAY_WEBHOOK_SECRET", "webhook-secret"):
        resp = await client.post(
            "/api/payments/webhook",
            content=json.dumps(payload),
            headers={
                "Content-Type": "application/json",
                "x-razorpay-signature": "wrong-sig",
            },
        )

    assert resp.status_code == 400


async def test_webhook_unknown_event(client, mock_db):
    payload = {"event": "unknown.event", "payload": {}}

    with patch.object(settings, "RAZORPAY_WEBHOOK_SECRET", ""):
        resp = await client.post(
            "/api/payments/webhook",
            content=json.dumps(payload),
            headers={"Content-Type": "application/json"},
        )

    assert resp.status_code == 200


# ── List payments ──


async def test_list_payments_admin(client, mock_db, admin_token):
    mock_db.payments.find = MagicMock(return_value=MockCursor([]))

    resp = await client.get(
        "/api/payments",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 200


async def test_list_payments_non_admin(client, mock_db, user_token):
    resp = await client.get(
        "/api/payments",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 403
