"""Tests for app.routers.availability — slot generation, unavailability CRUD."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from bson import ObjectId

from app.routers.availability import (
    _generate_all_slots,
    _overlaps,
    _time_to_minutes,
)
from tests.conftest import MockAggregationCursor, MockCursor


# ═══════════════════════════════════════
# Helper function tests (no HTTP)
# ═══════════════════════════════════════


def test_generate_all_slots_count():
    assert len(_generate_all_slots()) == 48


def test_generate_all_slots_first_slot():
    slots = _generate_all_slots()
    assert slots[0] == {"start": "00:00", "end": "00:30"}


def test_generate_all_slots_last_slot():
    slots = _generate_all_slots()
    assert slots[-1] == {"start": "23:30", "end": "00:00"}


def test_time_to_minutes_midnight():
    assert _time_to_minutes("00:00") == 0


def test_time_to_minutes_noon():
    assert _time_to_minutes("12:00") == 720


def test_time_to_minutes_end_of_day():
    assert _time_to_minutes("23:59") == 1439


def test_time_to_minutes_with_half_hour():
    assert _time_to_minutes("09:30") == 570


def test_overlaps_true():
    assert _overlaps("09:00", "10:00", "09:30", "10:30") is True


def test_overlaps_false_adjacent():
    assert _overlaps("09:00", "10:00", "10:00", "11:00") is False


def test_overlaps_contained():
    assert _overlaps("08:00", "12:00", "09:00", "10:00") is True


def test_overlaps_no_overlap():
    assert _overlaps("09:00", "10:00", "11:00", "12:00") is False


def test_overlaps_reverse_containment():
    assert _overlaps("09:00", "10:00", "08:00", "12:00") is True


# ═══════════════════════════════════════
# Endpoint tests (HTTP with mocked DB)
# ═══════════════════════════════════════


async def test_get_available_slots_no_blocks(client, mock_db):
    """With no unavailability and no bookings, all 48 slots returned."""
    mock_db.unavailability.find_one = AsyncMock(return_value=None)
    mock_db.unavailability.find = MagicMock(return_value=MockCursor([]))
    mock_db.bookings.find = MagicMock(return_value=MockCursor([]))

    resp = await client.get("/api/availability/slots?date=2026-03-15")
    assert resp.status_code == 200
    assert len(resp.json()) == 48


async def test_get_available_slots_holiday(client, mock_db):
    """If the date is a holiday, return empty list."""
    mock_db.unavailability.find_one = AsyncMock(
        return_value={"_id": ObjectId(), "date": "2026-03-15", "is_holiday": True}
    )

    resp = await client.get("/api/availability/slots?date=2026-03-15")
    assert resp.status_code == 200
    assert resp.json() == []


async def test_get_available_slots_with_unavailable_block(client, mock_db):
    """Slots overlapping an unavailable block are removed."""
    mock_db.unavailability.find_one = AsyncMock(return_value=None)
    mock_db.unavailability.find = MagicMock(
        return_value=MockCursor([
            {"start_time": "10:00", "end_time": "12:00", "is_holiday": False},
        ])
    )
    mock_db.bookings.find = MagicMock(return_value=MockCursor([]))

    resp = await client.get("/api/availability/slots?date=2026-03-15")
    assert resp.status_code == 200
    slots = resp.json()
    start_times = [s["start"] for s in slots]
    # 10:00, 10:30, 11:00, 11:30 should be removed (overlap with 10:00-12:00)
    assert "10:00" not in start_times
    assert "10:30" not in start_times
    assert "11:00" not in start_times
    assert "11:30" not in start_times
    assert "09:30" in start_times
    assert "12:00" in start_times


async def test_get_available_slots_with_booking(client, mock_db):
    """Slots overlapping an existing booking are removed."""
    mock_db.unavailability.find_one = AsyncMock(return_value=None)
    mock_db.unavailability.find = MagicMock(return_value=MockCursor([]))
    mock_db.bookings.find = MagicMock(
        return_value=MockCursor([
            {"time_slot": "14:00", "duration_minutes": 60, "status": "confirmed"},
        ])
    )

    resp = await client.get("/api/availability/slots?date=2026-03-15")
    assert resp.status_code == 200
    slots = resp.json()
    start_times = [s["start"] for s in slots]
    # 14:00 and 14:30 should be removed (booking covers 14:00-15:00)
    assert "14:00" not in start_times
    assert "14:30" not in start_times
    assert "13:30" in start_times
    assert "15:00" in start_times


async def test_get_available_slots_invalid_date(client, mock_db):
    resp = await client.get("/api/availability/slots?date=bad-date")
    assert resp.status_code == 422


async def test_get_holidays(client, mock_db):
    mock_db.unavailability.find = MagicMock(
        return_value=MockCursor([
            {"date": "2026-03-01"},
            {"date": "2026-03-15"},
        ])
    )

    resp = await client.get("/api/availability/holidays?start=2026-03-01&end=2026-03-31")
    assert resp.status_code == 200
    assert resp.json() == ["2026-03-01", "2026-03-15"]


async def test_get_unavailability(client, mock_db):
    doc = {
        "_id": ObjectId(),
        "date": "2026-03-15",
        "start_time": "10:00",
        "end_time": "12:00",
        "is_holiday": False,
        "reason": "Meeting",
    }
    mock_db.unavailability.find = MagicMock(return_value=MockCursor([doc]))

    resp = await client.get("/api/availability/unavailable?date=2026-03-15")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["start_time"] == "10:00"
    assert data[0]["reason"] == "Meeting"


async def test_get_unavailability_range(client, mock_db):
    docs = [
        {"_id": ObjectId(), "date": "2026-03-10", "is_holiday": True, "reason": "Holiday"},
        {"_id": ObjectId(), "date": "2026-03-15", "start_time": "09:00", "end_time": "10:00", "is_holiday": False, "reason": ""},
    ]
    mock_db.unavailability.find = MagicMock(return_value=MockCursor(docs))

    resp = await client.get("/api/availability/unavailable/range?start=2026-03-01&end=2026-03-31")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


async def test_add_unavailability_holiday(client, mock_db, admin_token):
    mock_db.unavailability.find_one = AsyncMock(return_value=None)
    mock_db.unavailability.insert_one = AsyncMock(
        return_value=MagicMock(inserted_id=ObjectId())
    )

    resp = await client.post(
        "/api/availability/unavailable",
        json={"date": "2026-03-20", "is_holiday": True, "reason": "Holi"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 200
    assert resp.json()["is_holiday"] is True
    assert resp.json()["reason"] == "Holi"


async def test_add_unavailability_duplicate_holiday(client, mock_db, admin_token):
    mock_db.unavailability.find_one = AsyncMock(
        return_value={"_id": ObjectId(), "date": "2026-03-20", "is_holiday": True}
    )

    resp = await client.post(
        "/api/availability/unavailable",
        json={"date": "2026-03-20", "is_holiday": True},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 400


async def test_add_unavailability_time_block(client, mock_db, admin_token):
    mock_db.unavailability.insert_one = AsyncMock(
        return_value=MagicMock(inserted_id=ObjectId())
    )

    resp = await client.post(
        "/api/availability/unavailable",
        json={"date": "2026-03-20", "start_time": "09:00", "end_time": "12:00"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 200
    assert resp.json()["start_time"] == "09:00"


async def test_add_unavailability_missing_times(client, mock_db, admin_token):
    resp = await client.post(
        "/api/availability/unavailable",
        json={"date": "2026-03-20"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 400


async def test_add_unavailability_start_after_end(client, mock_db, admin_token):
    resp = await client.post(
        "/api/availability/unavailable",
        json={"date": "2026-03-20", "start_time": "14:00", "end_time": "10:00"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 400


async def test_add_unavailability_requires_admin(client, mock_db, user_token):
    resp = await client.post(
        "/api/availability/unavailable",
        json={"date": "2026-03-20", "is_holiday": True},
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 403


async def test_remove_unavailability_success(client, mock_db, admin_token):
    block_id = str(ObjectId())
    mock_db.unavailability.delete_one = AsyncMock(
        return_value=MagicMock(deleted_count=1)
    )

    resp = await client.delete(
        f"/api/availability/unavailable/{block_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 200
    assert resp.json()["message"] == "Removed"


async def test_remove_unavailability_not_found(client, mock_db, admin_token):
    block_id = str(ObjectId())
    mock_db.unavailability.delete_one = AsyncMock(
        return_value=MagicMock(deleted_count=0)
    )

    resp = await client.delete(
        f"/api/availability/unavailable/{block_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 404


async def test_remove_unavailability_requires_admin(client, mock_db, user_token):
    block_id = str(ObjectId())
    resp = await client.delete(
        f"/api/availability/unavailable/{block_id}",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 403
