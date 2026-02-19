"""Tests for app.routers.bookings — pricing, overlap, and booking CRUD."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from bson import ObjectId

from app.routers.bookings import SERVICE_PRICES, _overlaps, _time_to_minutes, get_price
from app.utils.exceptions import BadRequestError
from tests.conftest import BOOKING_ID, MockCursor


# ═══════════════════════════════════════
# Helper function tests (no HTTP)
# ═══════════════════════════════════════


def test_get_price_valid_service_and_duration():
    assert get_price("call-consultation", 30) == 1999


def test_get_price_45_min():
    assert get_price("call-consultation", 45) == 2499


def test_get_price_unknown_service():
    with pytest.raises(BadRequestError, match="Unknown service"):
        get_price("nonexistent", 30)


def test_get_price_invalid_duration():
    with pytest.raises(BadRequestError, match="not available"):
        get_price("call-consultation", 90)


def test_get_price_report_service_any_duration():
    # Report services have "0" key — falls back to it for any duration
    assert get_price("premium-kundli", 15) == 4999


def test_get_price_all_services_have_entries():
    for slug, prices in SERVICE_PRICES.items():
        assert len(prices) > 0, f"{slug} has no price entries"


def test_time_to_minutes():
    assert _time_to_minutes("09:30") == 570


def test_overlaps_true():
    assert _overlaps(540, 600, 570, 630) is True


def test_overlaps_false():
    assert _overlaps(540, 600, 600, 660) is False


def test_overlaps_contained():
    assert _overlaps(480, 720, 540, 600) is True


# ═══════════════════════════════════════
# Endpoint tests
# ═══════════════════════════════════════

_VALID_BOOKING_DATA = {
    "service_slug": "call-consultation",
    "service_title": "Call Consultation",
    "date": "2026-03-16",  # Monday
    "time_slot": "10:00",
    "duration_minutes": 30,
    "user_name": "John Doe",
    "user_email": "john@test.com",
    "user_phone": "1234567890",
}


async def test_create_booking_success(client, mock_db):
    mock_db.unavailability.find_one = AsyncMock(return_value=None)
    mock_db.unavailability.find = MagicMock(return_value=MockCursor([]))
    mock_db.bookings.find = MagicMock(return_value=MockCursor([]))

    booking_doc = {
        "_id": BOOKING_ID,
        **_VALID_BOOKING_DATA,
        "price_inr": 1999,
        "status": "pending",
        "payment_id": None,
        "notes": "",
        "created_at": "2026-03-01T00:00:00",
    }
    mock_db.bookings.insert_one = AsyncMock(return_value=MagicMock(inserted_id=BOOKING_ID))
    mock_db.bookings.find_one = AsyncMock(return_value=booking_doc)

    resp = await client.post("/api/bookings", json=_VALID_BOOKING_DATA)
    assert resp.status_code == 200
    data = resp.json()
    assert data["price_inr"] == 1999
    assert data["status"] == "pending"


async def test_create_booking_holiday(client, mock_db):
    mock_db.unavailability.find_one = AsyncMock(
        return_value={"_id": ObjectId(), "date": "2026-03-16", "is_holiday": True}
    )

    resp = await client.post("/api/bookings", json=_VALID_BOOKING_DATA)
    assert resp.status_code == 400
    assert "holiday" in resp.json()["detail"].lower()


async def test_create_booking_unavailable_time(client, mock_db):
    mock_db.unavailability.find_one = AsyncMock(return_value=None)
    mock_db.unavailability.find = MagicMock(
        return_value=MockCursor([
            {"start_time": "09:00", "end_time": "11:00"},
        ])
    )

    resp = await client.post("/api/bookings", json=_VALID_BOOKING_DATA)
    assert resp.status_code == 400
    assert "unavailable" in resp.json()["detail"].lower()


async def test_create_booking_time_conflict(client, mock_db):
    mock_db.unavailability.find_one = AsyncMock(return_value=None)
    mock_db.unavailability.find = MagicMock(return_value=MockCursor([]))
    mock_db.bookings.find = MagicMock(
        return_value=MockCursor([
            {"time_slot": "10:00", "duration_minutes": 30, "status": "confirmed"},
        ])
    )

    resp = await client.post("/api/bookings", json=_VALID_BOOKING_DATA)
    assert resp.status_code == 400
    assert "already booked" in resp.json()["detail"].lower()


async def test_create_booking_invalid_service(client, mock_db):
    mock_db.unavailability.find_one = AsyncMock(return_value=None)
    data = {**_VALID_BOOKING_DATA, "service_slug": "nonexistent"}
    resp = await client.post("/api/bookings", json=data)
    assert resp.status_code == 400


async def test_create_booking_invalid_date_format(client, mock_db):
    data = {**_VALID_BOOKING_DATA, "date": "bad"}
    resp = await client.post("/api/bookings", json=data)
    assert resp.status_code == 422


async def test_list_bookings_admin_sees_all(client, mock_db, admin_token):
    booking_docs = [
        {
            "_id": BOOKING_ID,
            **_VALID_BOOKING_DATA,
            "price_inr": 1999,
            "status": "pending",
            "payment_id": None,
            "notes": "",
            "created_at": "2026-03-01T00:00:00",
        }
    ]
    mock_db.bookings.find = MagicMock(return_value=MockCursor(booking_docs))

    resp = await client.get(
        "/api/bookings",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 200
    assert len(resp.json()) == 1


async def test_list_bookings_user_sees_own(client, mock_db, user_token):
    mock_db.bookings.find = MagicMock(return_value=MockCursor([]))

    resp = await client.get(
        "/api/bookings",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 200
    # The query should include user_email filter — verified by mock call args
    call_args = mock_db.bookings.find.call_args[0][0]
    assert "user_email" in call_args


async def test_list_bookings_filter_by_status(client, mock_db, admin_token):
    mock_db.bookings.find = MagicMock(return_value=MockCursor([]))

    resp = await client.get(
        "/api/bookings?status=confirmed",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 200
    call_args = mock_db.bookings.find.call_args[0][0]
    assert call_args.get("status") == "confirmed"


async def test_get_booking_by_id_owner(client, mock_db, user_token, sample_booking_doc):
    mock_db.bookings.find_one = AsyncMock(return_value=sample_booking_doc)

    resp = await client.get(
        f"/api/bookings/{BOOKING_ID}",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 200


async def test_get_booking_by_id_admin(client, mock_db, admin_token, sample_booking_doc):
    mock_db.bookings.find_one = AsyncMock(return_value=sample_booking_doc)

    resp = await client.get(
        f"/api/bookings/{BOOKING_ID}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 200


async def test_get_booking_not_found(client, mock_db, user_token):
    mock_db.bookings.find_one = AsyncMock(return_value=None)
    fake_id = str(ObjectId())

    resp = await client.get(
        f"/api/bookings/{fake_id}",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 404


async def test_cancel_booking_success(client, mock_db, user_token, sample_booking_doc):
    mock_db.bookings.find_one = AsyncMock(return_value=sample_booking_doc)

    resp = await client.patch(
        f"/api/bookings/{BOOKING_ID}/cancel",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "cancelled"


async def test_cancel_booking_already_completed(client, mock_db, user_token, sample_booking_doc):
    sample_booking_doc["status"] = "completed"
    mock_db.bookings.find_one = AsyncMock(return_value=sample_booking_doc)

    resp = await client.patch(
        f"/api/bookings/{BOOKING_ID}/cancel",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 400


async def test_cancel_booking_already_cancelled(client, mock_db, user_token, sample_booking_doc):
    sample_booking_doc["status"] = "cancelled"
    mock_db.bookings.find_one = AsyncMock(return_value=sample_booking_doc)

    resp = await client.patch(
        f"/api/bookings/{BOOKING_ID}/cancel",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 400


async def test_update_status_admin(client, mock_db, admin_token, sample_booking_doc):
    mock_db.bookings.find_one = AsyncMock(return_value=sample_booking_doc)

    resp = await client.patch(
        f"/api/bookings/{BOOKING_ID}/status",
        json={"status": "confirmed"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 200


async def test_update_status_not_found(client, mock_db, admin_token):
    mock_db.bookings.find_one = AsyncMock(return_value=None)
    fake_id = str(ObjectId())

    resp = await client.patch(
        f"/api/bookings/{fake_id}/status",
        json={"status": "confirmed"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 404


async def test_update_status_requires_admin(client, mock_db, user_token, sample_booking_doc):
    mock_db.bookings.find_one = AsyncMock(return_value=sample_booking_doc)

    resp = await client.patch(
        f"/api/bookings/{BOOKING_ID}/status",
        json={"status": "confirmed"},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 403


# ═══════════════════════════════════════
# Business hours validation tests
# ═══════════════════════════════════════


async def test_create_booking_closed_day(client, mock_db):
    """Booking on a closed day (Sunday with defaults) should fail."""
    mock_db.unavailability.find_one = AsyncMock(return_value=None)

    data = {**_VALID_BOOKING_DATA, "date": "2026-03-15"}  # Sunday
    resp = await client.post("/api/bookings", json=data)
    assert resp.status_code == 400
    assert "not available on this day" in resp.json()["detail"].lower()


async def test_create_booking_outside_business_hours(client, mock_db):
    """Booking outside business hours should fail."""
    mock_db.unavailability.find_one = AsyncMock(return_value=None)
    mock_db.unavailability.find = MagicMock(return_value=MockCursor([]))
    mock_db.bookings.find = MagicMock(return_value=MockCursor([]))

    data = {**_VALID_BOOKING_DATA, "time_slot": "08:00"}  # Before 10:00
    resp = await client.post("/api/bookings", json=data)
    assert resp.status_code == 400
    assert "business hours" in resp.json()["detail"].lower()
