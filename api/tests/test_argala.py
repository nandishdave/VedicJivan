"""Tests for the Argala calculator (argala.py + the /argala-analysis endpoint).
The unit tests are pure (synthetic chart dicts); the endpoint tests build a real
ephemeris chart."""
import pytest

from app.services.kundli_calculator.argala import argala_analysis

_ALL9 = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]


def _chart(house_of: dict, paksha: str = "Shukla", shadbala: dict | None = None) -> dict:
    """Every graha defaults to house 1 (out of the way for a house-1 reference,
    which draws argala only from houses 2/4/5/11). Override placements + weights."""
    planets = {p: {"house": house_of.get(p, 1)} for p in _ALL9}
    chart = {"planets": planets, "panchanga": {"paksha": paksha}}
    if shadbala is not None:
        chart["shadbala"] = {p: {"total_shadbala": v} for p, v in shadbala.items()}
    return chart


def _house(out: dict, n: int) -> dict:
    return next(h for h in out["houses"] if h["house"] == n)


def test_structure_all_twelve_houses_bounded():
    out = argala_analysis(_chart({}, shadbala={p: 1.0 for p in _ALL9[:7]}))
    assert [h["house"] for h in out["houses"]] == list(range(1, 13))
    for h in out["houses"]:
        assert -100.0 <= h["strength"] <= 100.0


def test_benefic_in_11th_gives_full_positive():
    # Jupiter (benefic) in the 11th from house 1, its virodha (3rd) empty.
    out = argala_analysis(_chart({"Jupiter": 11}, shadbala={"Jupiter": 2.0}))
    h1 = _house(out, 1)
    assert h1["strength"] == 100.0
    assert h1["positive"] == ["Jupiter"] and h1["negative"] == []


def test_malefic_in_11th_gives_full_negative():
    out = argala_analysis(_chart({"Mars": 11}, shadbala={"Mars": 2.0}))
    h1 = _house(out, 1)
    assert h1["strength"] == -100.0
    assert h1["negative"] == ["Mars"] and h1["positive"] == []


def test_virodha_obstructs_a_stronger_counter_house():
    # Jupiter in the 11th (wt 2.0) but Saturn in the 3rd (virodha, wt 3.0) is
    # stronger -> the argala is obstructed and does not count.
    out = argala_analysis(_chart({"Jupiter": 11, "Saturn": 3},
                                 shadbala={"Jupiter": 2.0, "Saturn": 3.0}))
    h1 = _house(out, 1)
    assert h1["strength"] == 0.0
    assert h1["positive"] == [] and h1["negative"] == []


def test_moon_benefic_only_in_bright_fortnight():
    bright = argala_analysis(_chart({"Moon": 11}, paksha="Shukla",
                                    shadbala={"Moon": 2.0}))
    dark = argala_analysis(_chart({"Moon": 11}, paksha="Krishna",
                                  shadbala={"Moon": 2.0}))
    assert _house(bright, 1)["positive"] == ["Moon"]
    assert _house(dark, 1)["negative"] == ["Moon"]
    assert bright["moon_bright"] is True and dark["moon_bright"] is False


def test_tilt_mixes_benefic_and_malefic_by_weight():
    # House 1 argala houses 11 and 2: Jupiter(2.0, +) in 11, Sun(1.0, -) in 2.
    # Both effective (their virodha houses 3 and 12 are empty).
    out = argala_analysis(_chart({"Jupiter": 11, "Sun": 2},
                                 shadbala={"Jupiter": 2.0, "Sun": 1.0}))
    h1 = _house(out, 1)
    # (2.0 - 1.0) / (2.0 + 1.0) * 100 = 33.3
    assert h1["strength"] == 33.3
    assert h1["positive"] == ["Jupiter"] and h1["negative"] == ["Sun"]


# ── endpoint (real ephemeris chart) ──
_DOB, _TOB, _LAT, _LON = "1988-11-11", "12:55", 21.7333, 70.6167


@pytest.mark.asyncio
async def test_argala_endpoint_json(client):
    resp = await client.get(
        "/api/kundli/argala-analysis",
        params={"dob": _DOB, "tob": _TOB, "lat": _LAT, "lon": _LON},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert [h["house"] for h in body["houses"]] == list(range(1, 13))
    for h in body["houses"]:
        assert -100.0 <= h["strength"] <= 100.0
        assert isinstance(h["positive"], list) and isinstance(h["negative"], list)
    assert body["shadbala_used"] is True


@pytest.mark.asyncio
async def test_argala_endpoint_bad_input_returns_422(client):
    resp = await client.get(
        "/api/kundli/argala-analysis",
        params={"dob": "not-a-date", "tob": _TOB, "lat": _LAT, "lon": _LON},
    )
    assert resp.status_code == 422
