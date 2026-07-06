"""Tests for the Ashtakavarga calculator (ashtakavarga_table + endpoint).
Pure re-key logic + the classical invariants; the endpoint builds a real chart."""
import pytest

from app.services.kundli_calculator.ashtakavarga import (
    ashtakavarga_table,
    calc_ashtakavarga,
)

_7 = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_EXPECTED = {"Sun": 48, "Moon": 49, "Mars": 39, "Mercury": 54,
             "Jupiter": 56, "Venus": 52, "Saturn": 39}


def test_house_rekeying_from_lagna():
    # totals keyed by SIGN (Aries=0 -> 30 … Pisces=11 -> 41); lagna Cancer (3).
    totals = list(range(30, 42))
    bindus = {p: [1] * 12 for p in _7}
    chart = {"lagna": {"sign": 3},
             "ashtakavarga": {"totals": totals, "bindus": bindus, "grand_total": sum(totals)}}
    out = ashtakavarga_table(chart)
    # house 1 = the lagna sign (Cancer=3) -> sav = totals[3] = 33
    assert out["houses"][0] == {"house": 1, "sign": "Cancer", "sav": 33}
    # house 12 = sign (3 + 12 - 1) % 12 = 2 (Gemini) -> totals[2] = 32
    assert out["houses"][11]["sign"] == "Gemini"
    assert out["houses"][11]["sav"] == 32
    assert len(out["bav"]) == 7


def test_bav_totals_are_the_fixed_classical_values():
    planets = {p: {"sign": i} for i, p in enumerate(_7)}  # each planet in a distinct sign
    av = calc_ashtakavarga(planets, lagna_sign=0)
    out = ashtakavarga_table({"lagna": {"sign": 0}, "ashtakavarga": av})
    assert {b["planet"]: b["total"] for b in out["bav"]} == _EXPECTED
    assert out["grand_total"] == 337
    assert sum(h["sav"] for h in out["houses"]) == 337
    for b in out["bav"]:
        assert len(b["per_house"]) == 12
        assert all(0 <= x <= 8 for x in b["per_house"])  # a planet's BAV cell is 0..8


def test_prasthar_matrix_shape_and_invariants():
    planets = {p: {"sign": i} for i, p in enumerate(_7)}
    av = calc_ashtakavarga(planets, lagna_sign=0)
    out = ashtakavarga_table({"lagna": {"sign": 0}, "ashtakavarga": av})
    assert out["signs"] == ["Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]
    assert len(out["prasthar"]) == 7
    for pr in out["prasthar"]:
        assert len(pr["rows"]) == 8  # 7 planets + Lagna ("As")
        assert [r["contributor"] for r in pr["rows"]] == ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "As"]
        for r in pr["rows"]:
            assert all(v in (0, 1) for v in r["cells"])  # each cell is a single bindu
            assert r["total"] == sum(r["cells"])
        # each column total is the planet's BAV for that sign; they sum to the total
        assert sum(pr["column_totals"]) == _EXPECTED[pr["planet"]]


# ── endpoint (real ephemeris chart) ──
_DOB, _TOB, _LAT, _LON = "1988-11-11", "12:55", 21.7333, 70.6167


@pytest.mark.asyncio
async def test_ashtakavarga_endpoint(client):
    resp = await client.get(
        "/api/kundli/ashtakavarga",
        params={"dob": _DOB, "tob": _TOB, "lat": _LAT, "lon": _LON},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["grand_total"] == 337
    assert [h["house"] for h in body["houses"]] == list(range(1, 13))
    assert sum(h["sav"] for h in body["houses"]) == 337
    assert {b["planet"]: b["total"] for b in body["bav"]} == _EXPECTED


@pytest.mark.asyncio
async def test_ashtakavarga_endpoint_bad_input_returns_422(client):
    resp = await client.get(
        "/api/kundli/ashtakavarga",
        params={"dob": "not-a-date", "tob": _TOB, "lat": _LAT, "lon": _LON},
    )
    assert resp.status_code == 422
