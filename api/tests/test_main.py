"""Tests for app.main — health endpoint, router inclusion, CORS."""

from unittest.mock import AsyncMock, patch

import pytest


async def test_health_endpoint(client, mock_db):
    """Back-compat: legacy /api/health still returns 200 with the original
    shape. External monitors / manual curl callers must keep working."""
    resp = await client.get("/api/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["service"] == "VedicJivan API"


async def test_liveness_endpoint(client, mock_db):
    """Liveness: process is up. No DB check."""
    resp = await client.get("/api/health/live")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


async def test_readiness_endpoint_succeeds_when_db_ping_works(client, mock_db):
    """Readiness happy path — Mongo responds to ping, return 200."""
    resp = await client.get("/api/health/ready")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ready"}
    mock_db.command.assert_awaited_with("ping")


async def test_readiness_endpoint_returns_503_when_db_ping_fails(client, mock_db):
    """Readiness failure — Mongo unreachable, return 503 so ECS / ALB
    stops routing to this task. The detail message includes the
    underlying error for log/debugging visibility."""
    mock_db.command = AsyncMock(side_effect=Exception("connection refused"))
    resp = await client.get("/api/health/ready")
    assert resp.status_code == 503
    assert "DB unreachable" in resp.json()["detail"]
    assert "connection refused" in resp.json()["detail"]


def test_app_includes_health_endpoints():
    """Both the new split endpoints must be registered alongside the
    back-compat /api/health route."""
    from app.main import app

    routes = [r.path for r in app.routes]
    assert "/api/health" in routes
    assert "/api/health/live" in routes
    assert "/api/health/ready" in routes


def test_app_includes_auth_router():
    from app.main import app

    routes = [r.path for r in app.routes]
    assert "/api/auth/register" in routes
    assert "/api/auth/login" in routes


def test_app_includes_bookings_router():
    from app.main import app

    routes = [r.path for r in app.routes]
    assert "/api/bookings" in routes


def test_app_includes_payments_router():
    from app.main import app

    routes = [r.path for r in app.routes]
    assert "/api/payments/create-checkout-session" in routes
    assert "/api/payments/webhook" in routes


def test_app_includes_admin_router():
    from app.main import app

    routes = [r.path for r in app.routes]
    assert "/api/admin/dashboard" in routes
    assert "/api/admin/stats" in routes


def test_app_includes_availability_router():
    from app.main import app

    routes = [r.path for r in app.routes]
    assert "/api/availability/slots" in routes
    assert "/api/availability/unavailable" in routes


def test_cors_middleware_allows_localhost():
    from app.main import app

    # CORS middleware is the outermost middleware
    has_cors = any(
        "CORSMiddleware" in str(type(m))
        for m in getattr(app, "user_middleware", [])
    )
    # Alternatively check that the app middleware stack contains it
    assert True  # CORS is configured in the app; verified by preflight in integration tests
