"""Tests for app.routers.admin — dashboard and stats endpoints."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from tests.conftest import MockAggregationCursor, MockCursor


async def test_dashboard_returns_today_bookings(client, mock_db, admin_token):
    mock_db.bookings.count_documents = AsyncMock(return_value=5)
    mock_db.payments.aggregate = MagicMock(return_value=MockAggregationCursor([]))
    mock_db.bookings.aggregate = MagicMock(return_value=MockAggregationCursor([]))
    mock_db.bookings.find = MagicMock(return_value=MockCursor([]))

    resp = await client.get(
        "/api/admin/dashboard",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "today_bookings" in data


async def test_dashboard_returns_total_revenue(client, mock_db, admin_token):
    mock_db.bookings.count_documents = AsyncMock(return_value=0)
    mock_db.payments.aggregate = MagicMock(
        return_value=MockAggregationCursor([{"_id": None, "total": 15000}])
    )
    mock_db.bookings.aggregate = MagicMock(return_value=MockAggregationCursor([]))
    mock_db.bookings.find = MagicMock(return_value=MockCursor([]))

    resp = await client.get(
        "/api/admin/dashboard",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 200
    assert resp.json()["total_revenue"] == 15000


async def test_dashboard_revenue_zero_when_no_payments(client, mock_db, admin_token):
    mock_db.bookings.count_documents = AsyncMock(return_value=0)
    mock_db.payments.aggregate = MagicMock(return_value=MockAggregationCursor([]))
    mock_db.bookings.aggregate = MagicMock(return_value=MockAggregationCursor([]))
    mock_db.bookings.find = MagicMock(return_value=MockCursor([]))

    resp = await client.get(
        "/api/admin/dashboard",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.json()["total_revenue"] == 0


async def test_dashboard_returns_bookings_by_status(client, mock_db, admin_token):
    mock_db.bookings.count_documents = AsyncMock(return_value=0)
    mock_db.payments.aggregate = MagicMock(return_value=MockAggregationCursor([]))
    mock_db.bookings.aggregate = MagicMock(
        return_value=MockAggregationCursor([
            {"_id": "pending", "count": 3},
            {"_id": "confirmed", "count": 7},
        ])
    )
    mock_db.bookings.find = MagicMock(return_value=MockCursor([]))

    resp = await client.get(
        "/api/admin/dashboard",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    data = resp.json()
    assert data["bookings_by_status"]["pending"] == 3
    assert data["bookings_by_status"]["confirmed"] == 7


async def test_dashboard_returns_recent_bookings(client, mock_db, admin_token):
    from bson import ObjectId

    mock_db.bookings.count_documents = AsyncMock(return_value=0)
    mock_db.payments.aggregate = MagicMock(return_value=MockAggregationCursor([]))
    mock_db.bookings.aggregate = MagicMock(return_value=MockAggregationCursor([]))
    mock_db.bookings.find = MagicMock(
        return_value=MockCursor([
            {
                "_id": ObjectId(),
                "user_name": "John",
                "service_title": "Call",
                "date": "2026-03-15",
                "time_slot": "10:00",
                "status": "pending",
                "price_inr": 1999,
            }
        ])
    )

    resp = await client.get(
        "/api/admin/dashboard",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    data = resp.json()
    assert len(data["recent_bookings"]) == 1
    assert data["recent_bookings"][0]["user_name"] == "John"


async def test_dashboard_requires_admin(client, mock_db, user_token):
    resp = await client.get(
        "/api/admin/dashboard",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 403


async def test_dashboard_no_auth(client, mock_db):
    resp = await client.get("/api/admin/dashboard")
    assert resp.status_code == 422


async def test_stats_returns_totals(client, mock_db, admin_token):
    mock_db.users.count_documents = AsyncMock(return_value=10)
    mock_db.bookings.count_documents = AsyncMock(return_value=25)
    mock_db.payments.count_documents = AsyncMock(return_value=20)
    mock_db.bookings.aggregate = MagicMock(side_effect=[
        MockAggregationCursor([]),  # revenue_by_service
        MockAggregationCursor([]),  # daily_bookings
    ])
    mock_db.payments.aggregate = MagicMock(
        return_value=MockAggregationCursor([])  # daily_revenue
    )

    resp = await client.get(
        "/api/admin/stats",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_users"] == 10
    assert data["total_bookings"] == 25
    assert data["total_payments"] == 20
    assert len(data["daily_bookings"]) == 30
    assert len(data["daily_revenue"]) == 30


async def test_stats_returns_revenue_by_service(client, mock_db, admin_token):
    mock_db.users.count_documents = AsyncMock(return_value=0)
    mock_db.bookings.count_documents = AsyncMock(return_value=0)
    mock_db.payments.count_documents = AsyncMock(return_value=0)
    mock_db.bookings.aggregate = MagicMock(side_effect=[
        MockAggregationCursor([
            {"_id": "Call Consultation", "count": 5, "revenue": 9995},
        ]),  # revenue_by_service
        MockAggregationCursor([]),  # daily_bookings
    ])
    mock_db.payments.aggregate = MagicMock(
        return_value=MockAggregationCursor([])  # daily_revenue
    )

    resp = await client.get(
        "/api/admin/stats",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    services = resp.json()["revenue_by_service"]
    assert len(services) == 1
    assert services[0]["service"] == "Call Consultation"
    assert services[0]["revenue"] == 9995


async def test_stats_returns_daily_bookings_with_data(client, mock_db, admin_token):
    mock_db.users.count_documents = AsyncMock(return_value=0)
    mock_db.bookings.count_documents = AsyncMock(return_value=0)
    mock_db.payments.count_documents = AsyncMock(return_value=0)
    mock_db.bookings.aggregate = MagicMock(side_effect=[
        MockAggregationCursor([]),  # revenue_by_service
        MockAggregationCursor([
            {"_id": "2026-02-19", "count": 3},
        ]),  # daily_bookings
    ])
    mock_db.payments.aggregate = MagicMock(
        return_value=MockAggregationCursor([
            {"_id": "2026-02-19", "revenue": 5997},
        ])  # daily_revenue
    )

    resp = await client.get(
        "/api/admin/stats",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    data = resp.json()
    # Should have 30 days, with most being 0 and one being 3
    assert len(data["daily_bookings"]) == 30
    matching = [d for d in data["daily_bookings"] if d["bookings"] == 3]
    assert len(matching) == 1
    # Revenue series should also have 30 days
    assert len(data["daily_revenue"]) == 30
    rev_matching = [d for d in data["daily_revenue"] if d["revenue"] == 5997]
    assert len(rev_matching) == 1


async def test_stats_requires_admin(client, mock_db, user_token):
    resp = await client.get(
        "/api/admin/stats",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert resp.status_code == 403
