"""Tests for the /api/kundli/vimsopaka calculator endpoint + its service.

Read-only: computes per-planet Vimśopaka bala (0-20) across the 16 Shodashavarga
charts. No DB write, no gating. Behaviour, not exact magic numbers.
"""

from __future__ import annotations

import pytest

from app.services.kundli_calculator.vimsopaka import (
    VARGA_WEIGHTS,
    _band,
    compute_vimsopaka,
)

_CLASSICAL = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"}
_DOB, _TOB, _LAT, _LON = "1988-11-11", "12:55", 21.7333, 70.6167


def test_varga_weights_sum_to_twenty():
    assert abs(sum(VARGA_WEIGHTS.values()) - 20.0) < 1e-9
    assert VARGA_WEIGHTS["D60"] == 4.0 and VARGA_WEIGHTS["D1"] == 3.5 and VARGA_WEIGHTS["D9"] == 3.0


def test_band_thresholds():
    assert _band(18) == "Very strong"
    assert _band(12) == "Moderately strong"
    assert _band(7) == "Weak"
    assert _band(3) == "Very weak"


def test_compute_vimsopaka_shape_and_bounds():
    r = compute_vimsopaka(_DOB, _TOB, _LAT, _LON)
    assert set(r["planets"]) == _CLASSICAL
    for v in r["planets"].values():
        assert 0.0 <= v["vimsopaka"] <= 20.0
        assert 1 <= v["house"] <= 12
        assert len(v["vargas"]) == len(VARGA_WEIGHTS)  # 16 vargas each
    # strongest is the argmax and its flag is consistent with its house
    strongest = r["strongest"]["planet"]
    assert r["planets"][strongest]["vimsopaka"] == max(v["vimsopaka"] for v in r["planets"].values())
    assert r["strongest"]["in_prominence_seat"] == (r["strongest"]["house"] in (1, 2, 11))
    assert 0.0 <= r["average"] <= 20.0


@pytest.mark.asyncio
async def test_vimsopaka_endpoint_json(client):
    resp = await client.get(
        "/api/kundli/vimsopaka",
        params={"dob": _DOB, "tob": _TOB, "lat": _LAT, "lon": _LON},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert set(body["planets"]) == _CLASSICAL
    # default (detail=false) omits the per-varga breakdown
    assert "vargas" not in body["planets"]["Sun"]
    assert "strongest" in body and "average" in body


@pytest.mark.asyncio
async def test_vimsopaka_endpoint_detail_includes_vargas(client):
    resp = await client.get(
        "/api/kundli/vimsopaka",
        params={"dob": _DOB, "tob": _TOB, "lat": _LAT, "lon": _LON, "detail": "true"},
    )
    assert resp.status_code == 200
    assert len(resp.json()["planets"]["Jupiter"]["vargas"]) == len(VARGA_WEIGHTS)


@pytest.mark.asyncio
async def test_vimsopaka_endpoint_bad_input_returns_422(client):
    resp = await client.get(
        "/api/kundli/vimsopaka",
        params={"dob": "not-a-date", "tob": _TOB, "lat": _LAT, "lon": _LON},
    )
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_vimsopaka_page_serves_html(client):
    resp = await client.get("/api/kundli/vimsopaka/page")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]
    assert "Vimśopaka" in resp.text and "/api/kundli/vimsopaka" in resp.text
