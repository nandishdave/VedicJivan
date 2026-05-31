"""Tests for app.routers.payments — Stripe Checkout session, webhook, list."""

import json

import pytest
import stripe
from unittest.mock import AsyncMock, MagicMock, patch

from bson import ObjectId

from tests.conftest import BOOKING_ID, MockCursor


SAMPLE_BOOKING = {
    "_id": BOOKING_ID,
    "status": "pending",
    "service_title": "Call Consultation",
    "user_email": "test@example.com",
    "user_name": "Test User",
    "user_phone": "1234567890",
    "date": "2026-03-15",
    "time_slot": "10:00",
    "duration_minutes": 30,
    "price_inr": 1999,
}


def _make_stripe_event(event_type: str, data_object: dict, event_id: str | None = None) -> dict:
    return {
        "id": event_id or f"evt_test_{event_type.replace('.', '_')}",
        "type": event_type,
        "data": {"object": data_object},
    }


# ── Create checkout session ──


async def test_create_checkout_session_success(client, mock_db):
    mock_db.bookings.find_one = AsyncMock(return_value=SAMPLE_BOOKING)
    mock_db.payments.insert_one = AsyncMock(return_value=MagicMock(inserted_id=ObjectId()))

    mock_session = MagicMock()
    mock_session.id = "cs_test_abc123"
    mock_session.url = "https://checkout.stripe.com/pay/cs_test_abc123"

    with patch("stripe.checkout.Session.create", return_value=mock_session):
        resp = await client.post(
            "/api/payments/create-checkout-session",
            json={"booking_id": str(BOOKING_ID)},
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["checkout_url"] == "https://checkout.stripe.com/pay/cs_test_abc123"
    mock_db.payments.insert_one.assert_called_once()


async def test_create_checkout_session_booking_not_found(client, mock_db):
    mock_db.bookings.find_one = AsyncMock(return_value=None)

    resp = await client.post(
        "/api/payments/create-checkout-session",
        json={"booking_id": str(ObjectId())},
    )
    assert resp.status_code == 404


async def test_create_checkout_session_already_confirmed(client, mock_db):
    mock_db.bookings.find_one = AsyncMock(
        return_value={**SAMPLE_BOOKING, "status": "confirmed"}
    )

    resp = await client.post(
        "/api/payments/create-checkout-session",
        json={"booking_id": str(BOOKING_ID)},
    )
    assert resp.status_code == 400


# ── Webhook: checkout.session.completed ──


async def test_webhook_checkout_completed(client, mock_db):
    event = _make_stripe_event(
        "checkout.session.completed",
        {
            "id": "cs_test_abc123",
            "payment_intent": "pi_test_xyz",
            "metadata": {"booking_id": str(BOOKING_ID)},
        },
    )

    mock_db.bookings.find_one = AsyncMock(return_value=SAMPLE_BOOKING)

    with patch("stripe.Webhook.construct_event", return_value=event), \
         patch("app.routers.payments.send_booking_confirmation", new_callable=AsyncMock), \
         patch("app.routers.payments.send_admin_booking_notification", new_callable=AsyncMock):
        resp = await client.post(
            "/api/payments/webhook",
            content=json.dumps(event),
            headers={"Content-Type": "application/json", "stripe-signature": "sig"},
        )

    assert resp.status_code == 200
    assert mock_db.payments.update_one.call_count >= 1
    assert mock_db.bookings.update_one.call_count >= 1


async def test_webhook_checkout_completed_sends_emails(client, mock_db):
    event = _make_stripe_event(
        "checkout.session.completed",
        {
            "id": "cs_test_email",
            "payment_intent": "pi_test_email",
            "metadata": {"booking_id": str(BOOKING_ID)},
        },
    )

    mock_db.bookings.find_one = AsyncMock(return_value=SAMPLE_BOOKING)
    mock_confirm = AsyncMock()
    mock_admin_notify = AsyncMock()

    with patch("stripe.Webhook.construct_event", return_value=event), \
         patch("app.routers.payments.send_booking_confirmation", mock_confirm), \
         patch("app.routers.payments.send_admin_booking_notification", mock_admin_notify):
        await client.post(
            "/api/payments/webhook",
            content=json.dumps(event),
            headers={"Content-Type": "application/json", "stripe-signature": "sig"},
        )

    mock_confirm.assert_called_once()
    mock_admin_notify.assert_called_once()


async def test_webhook_email_failure_does_not_break(client, mock_db):
    event = _make_stripe_event(
        "checkout.session.completed",
        {
            "id": "cs_test_efail",
            "payment_intent": "pi_test_efail",
            "metadata": {"booking_id": str(BOOKING_ID)},
        },
    )

    mock_db.bookings.find_one = AsyncMock(return_value=SAMPLE_BOOKING)

    with patch("stripe.Webhook.construct_event", return_value=event), \
         patch("app.routers.payments.send_booking_confirmation", AsyncMock(side_effect=Exception("SMTP error"))), \
         patch("app.routers.payments.send_admin_booking_notification", AsyncMock(side_effect=Exception("SMTP error"))):
        resp = await client.post(
            "/api/payments/webhook",
            content=json.dumps(event),
            headers={"Content-Type": "application/json", "stripe-signature": "sig"},
        )

    assert resp.status_code == 200


# ── Webhook: checkout.session.expired ──


async def test_webhook_session_expired(client, mock_db):
    event = _make_stripe_event(
        "checkout.session.expired",
        {"id": "cs_test_expired"},
    )

    with patch("stripe.Webhook.construct_event", return_value=event):
        resp = await client.post(
            "/api/payments/webhook",
            content=json.dumps(event),
            headers={"Content-Type": "application/json", "stripe-signature": "sig"},
        )

    assert resp.status_code == 200
    mock_db.payments.update_one.assert_called_once()


# ── Webhook: charge.refunded ──


async def test_webhook_charge_refunded(client, mock_db):
    event = _make_stripe_event(
        "charge.refunded",
        {"payment_intent": "pi_test_refund"},
    )

    with patch("stripe.Webhook.construct_event", return_value=event):
        resp = await client.post(
            "/api/payments/webhook",
            content=json.dumps(event),
            headers={"Content-Type": "application/json", "stripe-signature": "sig"},
        )

    assert resp.status_code == 200
    mock_db.payments.update_one.assert_called_once()


# ── Webhook: invalid signature ──


async def test_webhook_invalid_signature(client, mock_db):
    with patch(
        "stripe.Webhook.construct_event",
        side_effect=stripe.SignatureVerificationError("bad sig", "sig_header"),
    ):
        resp = await client.post(
            "/api/payments/webhook",
            content=json.dumps({"type": "test"}),
            headers={"Content-Type": "application/json", "stripe-signature": "bad"},
        )

    assert resp.status_code == 400


# ── Webhook: unknown event ──


async def test_webhook_unknown_event(client, mock_db):
    event = _make_stripe_event("unknown.event", {})

    with patch("stripe.Webhook.construct_event", return_value=event):
        resp = await client.post(
            "/api/payments/webhook",
            content=json.dumps(event),
            headers={"Content-Type": "application/json", "stripe-signature": "sig"},
        )

    assert resp.status_code == 200


# ── Session status ──


async def test_get_session_status(client, mock_db):
    mock_db.payments.find_one = AsyncMock(
        return_value={"stripe_session_id": "cs_test_abc", "status": "captured"}
    )
    mock_db.bookings.find_one = AsyncMock(
        return_value={
            "_id": BOOKING_ID,
            "status": "confirmed",
            "service_title": "Call Consultation",
            "date": "2026-03-15",
            "time_slot": "10:00",
            "duration_minutes": 30,
            "price_inr": 1999,
            "user_name": "John Doe",
            "user_email": "john@test.com",
        }
    )

    resp = await client.get(
        f"/api/payments/session-status?session_id=cs_test_abc&booking_id={BOOKING_ID}"
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["payment_status"] == "captured"
    assert data["booking_status"] == "confirmed"
    assert data["booking"]["service_title"] == "Call Consultation"
    assert data["booking"]["date"] == "2026-03-15"
    assert data["booking"]["price_inr"] == 1999
    assert data["booking"]["user_name"] == "John Doe"


async def test_get_session_status_not_found(client, mock_db):
    mock_db.payments.find_one = AsyncMock(return_value=None)

    resp = await client.get(
        f"/api/payments/session-status?session_id=cs_nonexistent&booking_id={BOOKING_ID}"
    )
    assert resp.status_code == 404


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


# ═══════════════════════════════════════════════════════════════════════════
# Stripe webhook signature contract tests
# ───────────────────────────────────────────────────────────────────────────
# These use the REAL `stripe` SDK to sign + verify a payload — no mocking of
# `construct_event`. They cover the actual signature-verification code path
# that a real Stripe delivery would hit. The shared secret is the test value
# `whsec_test_fake_secret` set in conftest.py via STRIPE_WEBHOOK_SECRET.
#
# Reference: https://stripe.com/docs/webhooks/signatures
# ═══════════════════════════════════════════════════════════════════════════


def _sign_stripe_payload(payload: bytes, secret: str, timestamp: int | None = None) -> str:
    """Build a Stripe-Signature header for a given payload + shared secret.

    Uses the v1 scheme: HMAC-SHA256 over `{timestamp}.{payload}`.
    """
    import hashlib
    import hmac
    import time
    ts = timestamp if timestamp is not None else int(time.time())
    signed_payload = f"{ts}.".encode() + payload
    sig = hmac.new(secret.encode(), signed_payload, hashlib.sha256).hexdigest()
    return f"t={ts},v1={sig}"


async def test_webhook_accepts_validly_signed_session_expired(client, mock_db):
    """Happy path: payload signed with the real Stripe HMAC scheme passes
    verification and the `checkout.session.expired` handler runs."""
    payload = json.dumps({
        "id": "evt_test_signed",
        "object": "event",
        "type": "checkout.session.expired",
        "data": {"object": {"id": "cs_test_signed"}},
    }).encode()
    sig_header = _sign_stripe_payload(payload, "whsec_test_fake_secret")

    resp = await client.post(
        "/api/payments/webhook",
        content=payload,
        headers={"Content-Type": "application/json", "stripe-signature": sig_header},
    )
    assert resp.status_code == 200
    mock_db.payments.update_one.assert_awaited()
    update_call = mock_db.payments.update_one.call_args
    assert update_call.args[0] == {"stripe_session_id": "cs_test_signed"}


async def test_webhook_charge_refunded_uses_bracket_access_not_dot_get(client, mock_db):
    """REGRESSION TEST. Stripe SDK v15+ returns StripeObject (NOT a dict).
    Calling `.get()` on it raises AttributeError. The router previously did
    `charge.get("payment_intent")` which would crash on every real refund
    delivery. This test exercises the post-fix bracket-access code path with
    a real signed payload to ensure prod can survive a refund."""
    payload = json.dumps({
        "id": "evt_refund_real",
        "object": "event",
        "type": "charge.refunded",
        "data": {"object": {"id": "ch_x", "payment_intent": "pi_refund_real"}},
    }).encode()
    sig_header = _sign_stripe_payload(payload, "whsec_test_fake_secret")

    resp = await client.post(
        "/api/payments/webhook",
        content=payload,
        headers={"Content-Type": "application/json", "stripe-signature": sig_header},
    )
    assert resp.status_code == 200
    mock_db.payments.update_one.assert_awaited()
    update_call = mock_db.payments.update_one.call_args
    assert update_call.args[0] == {"stripe_payment_intent_id": "pi_refund_real"}


async def test_webhook_rejects_payload_with_wrong_secret(client, mock_db):
    """A payload signed with a *different* secret must be rejected with 400."""
    payload = json.dumps({"id": "evt", "object": "event", "type": "charge.refunded", "data": {"object": {}}}).encode()
    sig_header = _sign_stripe_payload(payload, "whsec_someone_else")

    resp = await client.post(
        "/api/payments/webhook",
        content=payload,
        headers={"Content-Type": "application/json", "stripe-signature": sig_header},
    )
    assert resp.status_code == 400
    assert "signature" in resp.json()["detail"].lower()


async def test_webhook_rejects_payload_with_tampered_body(client, mock_db):
    """If the body is changed after signing, signature verification fails."""
    original = json.dumps({"id": "evt", "object": "event", "type": "charge.refunded", "data": {"object": {}}}).encode()
    sig_header = _sign_stripe_payload(original, "whsec_test_fake_secret")
    tampered = original.replace(b"refunded", b"succeeded")

    resp = await client.post(
        "/api/payments/webhook",
        content=tampered,
        headers={"Content-Type": "application/json", "stripe-signature": sig_header},
    )
    assert resp.status_code == 400
    assert "signature" in resp.json()["detail"].lower()


async def test_webhook_rejects_replay_with_old_timestamp(client, mock_db):
    """Stripe's SDK enforces a default 5-minute tolerance window. A payload
    signed with a 10-minute-old timestamp must be rejected as a replay."""
    payload = json.dumps({"id": "evt", "object": "event", "type": "charge.refunded", "data": {"object": {}}}).encode()
    import time
    old_ts = int(time.time()) - 600
    sig_header = _sign_stripe_payload(payload, "whsec_test_fake_secret", timestamp=old_ts)

    resp = await client.post(
        "/api/payments/webhook",
        content=payload,
        headers={"Content-Type": "application/json", "stripe-signature": sig_header},
    )
    assert resp.status_code == 400
    assert "signature" in resp.json()["detail"].lower()


async def test_webhook_rejects_missing_signature_header(client, mock_db):
    """A request with no stripe-signature header at all → 400."""
    payload = json.dumps({"id": "evt", "object": "event", "type": "charge.refunded", "data": {"object": {}}}).encode()

    resp = await client.post(
        "/api/payments/webhook",
        content=payload,
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 400


# ═══════════════════════════════════════════════════════════════════════════
# Stripe webhook idempotency
# ───────────────────────────────────────────────────────────────────────────
# Stripe redelivers the same event id on network timeout / scheduled retry /
# manual replay. Without dedupe, every side effect re-fires (duplicate emails,
# duplicate calendar events, duplicate booking confirmations).
#
# The dedupe primitive lives in `ProcessedEventRepository.mark_processed`:
# an atomic insert keyed by `_id = event["id"]`. The second insert raises
# `DuplicateKeyError` → returns False → use case skips dispatch.
# ═══════════════════════════════════════════════════════════════════════════


def _duplicate_key_error():
    """Build a Mongo DuplicateKeyError matching what Motor raises on the
    second insert with the same `_id`."""
    from pymongo.errors import DuplicateKeyError
    return DuplicateKeyError("E11000 duplicate key error", {"code": 11000})


async def test_webhook_dedupes_repeated_checkout_completed(client, mock_db):
    """Same `checkout.session.completed` event id sent twice: side effects
    fire on the first delivery only. Second delivery returns 200 silently."""
    from tests.conftest import BOOKING_ID

    # Booking lookup must succeed so the email/calendar branch is reached on
    # the first delivery (otherwise it short-circuits before any side effect).
    mock_db.bookings.find_one = AsyncMock(return_value={
        **SAMPLE_BOOKING,
        "_id": BOOKING_ID,
    })

    # Second insert raises DuplicateKeyError → mark_processed returns False.
    mock_db.stripe_events.insert_one = AsyncMock(side_effect=[
        MagicMock(inserted_id="evt_dup_completed"),
        _duplicate_key_error(),
    ])

    payload = json.dumps({
        "id": "evt_dup_completed",
        "object": "event",
        "type": "checkout.session.completed",
        "data": {"object": {
            "id": "cs_dup_completed",
            "payment_intent": "pi_dup_completed",
            "metadata": {"booking_id": str(BOOKING_ID)},
        }},
    }).encode()
    sig = _sign_stripe_payload(payload, "whsec_test_fake_secret")
    headers = {"Content-Type": "application/json", "stripe-signature": sig}

    with patch(
        "app.routers.payments.send_booking_confirmation", new_callable=AsyncMock
    ) as mock_send_conf, patch(
        "app.routers.payments.send_admin_booking_notification", new_callable=AsyncMock
    ) as mock_send_admin, patch(
        "app.routers.payments.create_booking_event", return_value="gcal_evt_1"
    ) as mock_calendar:
        resp1 = await client.post("/api/payments/webhook", content=payload, headers=headers)
        resp2 = await client.post("/api/payments/webhook", content=payload, headers=headers)

    assert resp1.status_code == 200
    assert resp2.status_code == 200

    # Two attempts to record the event → only the first inserts.
    assert mock_db.stripe_events.insert_one.call_count == 2

    # mark_captured fires once on `payments.update_one` against session id.
    captured_calls = [
        c for c in mock_db.payments.update_one.call_args_list
        if c.args and c.args[0] == {"stripe_session_id": "cs_dup_completed"}
    ]
    assert len(captured_calls) == 1

    # Side effects fire exactly once each.
    assert mock_send_conf.call_count == 1
    assert mock_send_admin.call_count == 1
    assert mock_calendar.call_count == 1


async def test_webhook_dedupes_repeated_session_expired(client, mock_db):
    """Same `checkout.session.expired` event id sent twice → mark_expired
    fires once."""
    mock_db.stripe_events.insert_one = AsyncMock(side_effect=[
        MagicMock(inserted_id="evt_dup_expired"),
        _duplicate_key_error(),
    ])

    payload = json.dumps({
        "id": "evt_dup_expired",
        "object": "event",
        "type": "checkout.session.expired",
        "data": {"object": {"id": "cs_dup_expired"}},
    }).encode()
    sig = _sign_stripe_payload(payload, "whsec_test_fake_secret")
    headers = {"Content-Type": "application/json", "stripe-signature": sig}

    resp1 = await client.post("/api/payments/webhook", content=payload, headers=headers)
    resp2 = await client.post("/api/payments/webhook", content=payload, headers=headers)

    assert resp1.status_code == 200
    assert resp2.status_code == 200

    expired_calls = [
        c for c in mock_db.payments.update_one.call_args_list
        if c.args and c.args[0] == {"stripe_session_id": "cs_dup_expired"}
    ]
    assert len(expired_calls) == 1


async def test_webhook_dedupes_repeated_charge_refunded(client, mock_db):
    """Same `charge.refunded` event id sent twice → mark_refunded fires once."""
    mock_db.stripe_events.insert_one = AsyncMock(side_effect=[
        MagicMock(inserted_id="evt_dup_refunded"),
        _duplicate_key_error(),
    ])

    payload = json.dumps({
        "id": "evt_dup_refunded",
        "object": "event",
        "type": "charge.refunded",
        "data": {"object": {"id": "ch_dup", "payment_intent": "pi_dup_refunded"}},
    }).encode()
    sig = _sign_stripe_payload(payload, "whsec_test_fake_secret")
    headers = {"Content-Type": "application/json", "stripe-signature": sig}

    resp1 = await client.post("/api/payments/webhook", content=payload, headers=headers)
    resp2 = await client.post("/api/payments/webhook", content=payload, headers=headers)

    assert resp1.status_code == 200
    assert resp2.status_code == 200

    refunded_calls = [
        c for c in mock_db.payments.update_one.call_args_list
        if c.args and c.args[0] == {"stripe_payment_intent_id": "pi_dup_refunded"}
    ]
    assert len(refunded_calls) == 1


# ═══════════════════════════════════════════════════════════════════════════
# create-checkout-session edge cases (cover remaining payments.py branches)
# ═══════════════════════════════════════════════════════════════════════════


async def test_checkout_session_404_when_booking_missing(client, mock_db):
    mock_db.bookings.find_one = AsyncMock(return_value=None)
    resp = await client.post(
        "/api/payments/create-checkout-session",
        json={"booking_id": str(ObjectId()), "currency": "INR"},
    )
    assert resp.status_code == 404


async def test_checkout_session_400_when_booking_already_confirmed(client, mock_db):
    from app.models.booking import BookingStatus
    mock_db.bookings.find_one = AsyncMock(return_value={
        "_id": ObjectId(),
        "status": BookingStatus.CONFIRMED,
        "price_inr": 1999,
        "price_eur": 29,
        "service_title": "Call",
        "user_email": "u@test.com",
        "date": "2026-05-01",
        "time_slot": "10:00",
        "duration_minutes": 30,
    })
    resp = await client.post(
        "/api/payments/create-checkout-session",
        json={"booking_id": str(ObjectId()), "currency": "INR"},
    )
    assert resp.status_code == 400
    assert "already paid" in resp.json()["detail"].lower()
