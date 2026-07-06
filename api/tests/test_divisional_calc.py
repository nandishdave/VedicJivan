"""Tests for the Divisional Charts calculator (divisional_table + endpoint)."""
import pytest

from app.services.kundli_calculator.divisional import divisional_table

_ABBR = ["Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]


def test_d1_is_the_natal_sign_and_shape():
    planets = {
        "Sun": {"sign": 0, "degree_in_sign": 5.0},   # Aries
        "Moon": {"sign": 6, "degree_in_sign": 10.0},  # Libra
    }
    lagna = {"sign": 9, "degree": 12.0}  # Capricorn
    out = divisional_table(planets, lagna)
    assert [v["key"] for v in out["vargas"]][0] == "D1"
    assert len(out["vargas"]) == 19  # D1 + 18 computed vargas
    by = {b["body"]: b for b in out["bodies"]}
    # first column (D1) = the natal sign
    assert by["Ascendant"]["signs"][0] == "Cp"
    assert by["Sun"]["signs"][0] == "Ar"
    assert by["Moon"]["signs"][0] == "Li"
    # every cell is a valid sign abbreviation
    for b in out["bodies"]:
        assert len(b["signs"]) == 19
        assert all(s in _ABBR for s in b["signs"])


def test_ascendant_first_then_grahas():
    planets = {p: {"sign": 0, "degree_in_sign": 1.0} for p in
               ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn",
                "Rahu", "Ketu", "Uranus", "Neptune", "Pluto"]}
    out = divisional_table(planets, {"sign": 0, "degree": 1.0})
    bodies = [b["body"] for b in out["bodies"]]
    assert bodies[0] == "Ascendant"
    assert "Uranus" in bodies and "Pluto" in bodies and "Rahu" in bodies


# ── endpoint (real ephemeris chart) ──
_DOB, _TOB, _LAT, _LON = "1988-11-11", "12:55", 21.7333, 70.6167


@pytest.mark.asyncio
async def test_divisional_endpoint(client):
    resp = await client.get(
        "/api/kundli/divisional-charts",
        params={"dob": _DOB, "tob": _TOB, "lat": _LAT, "lon": _LON},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert [v["key"] for v in body["vargas"]][:2] == ["D1", "D2"]
    assert body["vargas"][-1]["key"] == "D60"
    assert body["bodies"][0]["body"] == "Ascendant"
    for b in body["bodies"]:
        assert len(b["signs"]) == len(body["vargas"])


@pytest.mark.asyncio
async def test_divisional_endpoint_bad_input_returns_422(client):
    resp = await client.get(
        "/api/kundli/divisional-charts",
        params={"dob": "not-a-date", "tob": _TOB, "lat": _LAT, "lon": _LON},
    )
    assert resp.status_code == 422
