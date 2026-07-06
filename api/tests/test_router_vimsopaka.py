"""Tests for the /api/kundli/vimsopaka calculator endpoint + its service.

Read-only: computes per-planet Vimśopaka bala (0-20) across the 16 Shodashavarga
charts. No DB write, no gating. Behaviour, not exact magic numbers.
"""

from __future__ import annotations

import pytest

from app.services.kundli_calculator.dignity import DIGNITY_PCT
from app.services.kundli_calculator.vimsopaka import (
    VARGA_WEIGHTS,
    _band,
    compute_vimsopaka,
    planet_vimsopaka,
)


def test_planet_vimsopaka_contribution_is_weight_times_pct():
    """Each varga's contribution is exactly weight * dignity_pct / 100, and the
    total is their sum. Previously only the bounds/sum were checked — this pins
    the per-varga contribution field itself. Pure: synthetic sign maps."""
    # Sun placed in the same sign across every varga -> one dignity throughout.
    planets = {"Sun": {"sign": 4}}
    divisional = {v: {"Sun": 4} for v in VARGA_WEIGHTS}
    out = planet_vimsopaka("Sun", planets, divisional)
    total = 0.0
    for row in out["vargas"]:
        expected = round(row["weight"] * DIGNITY_PCT[row["dignity"]] / 100.0, 3)
        assert row["contribution"] == expected
        total += row["weight"] * DIGNITY_PCT[row["dignity"]] / 100.0
    assert out["vimsopaka"] == round(total, 2)
    assert out["max"] == 20.0

_CLASSICAL = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"}
_NODES = {"Rahu", "Ketu"}
_OUTER = {"Uranus", "Neptune", "Pluto"}
_ALL = _CLASSICAL | _NODES | _OUTER
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
    # 7 classical grahas + Rāhu/Ketu (display only)
    assert set(r["planets"]) == _ALL
    for v in r["planets"].values():
        assert 0.0 <= v["vimsopaka"] <= 20.0
        assert 1 <= v["house"] <= 12
        assert len(v["vargas"]) == len(VARGA_WEIGHTS)  # 16 vargas each
    assert r["planets"]["Rahu"]["is_node"] and not r["planets"]["Sun"]["is_node"]
    # strongest + average use the 7 classical grahas only (nodes excluded)
    strongest = r["strongest"]["planet"]
    assert strongest in _CLASSICAL
    assert r["planets"][strongest]["vimsopaka"] == max(r["planets"][p]["vimsopaka"] for p in _CLASSICAL)
    assert r["strongest"]["in_prominence_seat"] == (r["strongest"]["house"] in (1, 2, 4, 5, 11))
    expected_avg = round(sum(r["planets"][p]["vimsopaka"] for p in _CLASSICAL) / 7, 2)
    assert r["average"] == pytest.approx(expected_avg, abs=0.01)


@pytest.mark.asyncio
async def test_vimsopaka_endpoint_json(client):
    resp = await client.get(
        "/api/kundli/vimsopaka",
        params={"dob": _DOB, "tob": _TOB, "lat": _LAT, "lon": _LON},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert set(body["planets"]) == _ALL  # 7 classical + nodes + 3 outer
    assert body["strongest"]["planet"] in _CLASSICAL  # nodes/outer excluded from the pick
    # nodes + outer planets are flagged display-only
    assert all(body["planets"][p]["is_node"] for p in _NODES)
    assert all(body["planets"][p]["is_outer"] for p in _OUTER)
    assert not body["planets"]["Sun"]["is_node"] and not body["planets"]["Sun"]["is_outer"]
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
