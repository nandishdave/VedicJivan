"""Tests for the /api/kundli/preview endpoint and the production gating.

The preview endpoint is meant for development iteration only — it returns the
generated PDF directly with no email, no DB write, no rate limit. It must
return 404 in production so it can never accidentally render PDFs without
the rate-limited / audited path.
"""

from __future__ import annotations

import os
from unittest.mock import AsyncMock, patch

import pytest


@pytest.mark.asyncio
async def test_preview_returns_pdf_inline_in_non_production(client):
    """Non-production: returns 200 with PDF body and inline content-disposition."""
    fake_chart = {"name": "Test", "lagna": {"sign": "Capricorn"}}
    fake_pdf = b"%PDF-fake-preview"

    with (
        patch.dict(os.environ, {"APP_ENV": "staging"}),
        patch("app.routers.kundli.build_chart", return_value=fake_chart),
        patch("app.routers.kundli.generate_pdf", return_value=fake_pdf),
        patch("app.routers.kundli.load_report_sections", new=AsyncMock(return_value=[])),
    ):
        resp = await client.get("/api/kundli/preview")

    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/pdf"
    assert "inline" in resp.headers["content-disposition"]
    assert resp.content == fake_pdf


@pytest.mark.asyncio
async def test_preview_disabled_in_production(client):
    """APP_ENV=production → 404 so the unauthenticated endpoint can't leak."""
    with patch.dict(os.environ, {"APP_ENV": "production"}):
        resp = await client.get("/api/kundli/preview")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_preview_returns_500_when_calculation_fails(client):
    """A swisseph or PDF failure surfaces as a 500 with the error truncated."""
    with (
        patch.dict(os.environ, {"APP_ENV": "staging"}),
        patch("app.routers.kundli.build_chart", side_effect=ValueError("bad lat 999")),
        patch("app.routers.kundli.load_report_sections", new=AsyncMock(return_value=[])),
    ):
        resp = await client.get("/api/kundli/preview")
    assert resp.status_code == 500
    assert "bad lat 999" in resp.json()["detail"]


@pytest.mark.asyncio
async def test_preview_passes_query_args_to_chart(client):
    """Custom query parameters are forwarded to build_chart() and generate_pdf()."""
    fake_chart = {"name": "Custom", "lagna": {"sign": "Aries"}}

    with (
        patch.dict(os.environ, {"APP_ENV": "dev"}),
        patch("app.routers.kundli.build_chart", return_value=fake_chart) as build_mock,
        patch("app.routers.kundli.generate_pdf", return_value=b"%PDF-fake"),
        patch("app.routers.kundli.load_report_sections", new=AsyncMock(return_value=[])),
    ):
        resp = await client.get(
            "/api/kundli/preview",
            params={
                "name": "Test User",
                "dob": "1990-05-15",
                "tob": "08:30",
                "lat": 19.076,
                "lon": 72.8777,
                "place_name": "Mumbai",
                "timezone": "Asia/Kolkata",
            },
        )

    assert resp.status_code == 200
    build_mock.assert_called_once()
    kwargs = build_mock.call_args.kwargs
    assert kwargs["name"] == "Test User"
    assert kwargs["dob"] == "1990-05-15"
    assert kwargs["lat"] == 19.076


@pytest.mark.asyncio
async def test_preview_filters_sections_by_is_paid_false(client):
    """Only `is_paid=False` admin-enabled sections are passed to generate_pdf."""
    sections = [
        type("S", (), {"id": "free_section", "is_paid": False, "enabled": True,
                       "model_dump": lambda self: {"id": "free_section", "is_paid": False, "enabled": True}})(),
        type("S", (), {"id": "paid_section", "is_paid": True, "enabled": True,
                       "model_dump": lambda self: {"id": "paid_section", "is_paid": True, "enabled": True}})(),
        type("S", (), {"id": "off_section", "is_paid": False, "enabled": False,
                       "model_dump": lambda self: {"id": "off_section", "is_paid": False, "enabled": False}})(),
    ]

    with (
        patch.dict(os.environ, {"APP_ENV": "dev"}),
        patch("app.routers.kundli.build_chart", return_value={"name": "x"}),
        patch("app.routers.kundli.generate_pdf", return_value=b"%PDF") as pdf_mock,
        patch("app.routers.kundli.load_report_sections", new=AsyncMock(return_value=sections)),
    ):
        await client.get("/api/kundli/preview")

    passed = pdf_mock.call_args.kwargs["sections"]
    ids = [s["id"] for s in passed]
    assert ids == ["free_section"]
