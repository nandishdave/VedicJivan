"""Tests for the Argala calculator (argala.py + the /argala-analysis endpoint).

Each house scores its effective argalas by ① dignity toward the house, ②
natural-nature/house-type fit, weighted by ③ Shadbala AND reduced by the
Virodha counter (survive fraction). Unit tests assert at the argala-row level
(deterministic regardless of the other grahas). Aries lagna = sign 0.
"""
import pytest

from app.services.kundli_calculator.argala import argala_analysis

_ALL9 = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]


def _chart(house_of: dict, lagna_sign: int = 0, paksha: str = "Shukla",
           shadbala: dict | None = None, default_house: int = 1) -> dict:
    planets = {p: {"house": house_of.get(p, default_house)} for p in _ALL9}
    chart = {"planets": planets, "panchanga": {"paksha": paksha},
             "lagna": {"sign": lagna_sign}}
    if shadbala is not None:
        chart["shadbala"] = {p: {"total_shadbala": v} for p, v in shadbala.items()}
    return chart


def _house(out: dict, n: int) -> dict:
    return next(h for h in out["houses"] if h["house"] == n)


def _arg_row(out: dict, house: int, planet: str):
    for pair in _house(out, house)["pairs"]:
        for r in pair["argala"]:
            if r["planet"] == planet:
                return r
    return None


def test_structure_all_twelve_houses_bounded():
    out = argala_analysis(_chart({}, shadbala={p: 1.0 for p in _ALL9[:7]}))
    assert [h["house"] for h in out["houses"]] == list(range(1, 13))
    for h in out["houses"]:
        assert -100.0 <= h["strength"] <= 100.0
        assert h["verdict"] in {"null", "neutral", "positive", "negative"}
        assert isinstance(h["pairs"], list)


def test_exalted_malefic_reads_positive():
    # Aries lagna; Saturn in the 11th throws (5th-)argala on the 7th (Libra),
    # where Saturn is EXALTED — unopposed (survive 1) -> positive.
    out = argala_analysis(_chart({"Saturn": 11}, lagna_sign=0, shadbala={"Saturn": 2.0}))
    row = _arg_row(out, 7, "Saturn")
    assert row is not None
    assert row["dignity"] == "Exalted" and row["dignity_score"] == 2.0
    assert row["contribution"] == 4.0  # 2.0 SB × polarity 2 × survive 1
    assert _house(out, 7)["verdict"] == "positive" and "Saturn" in _house(out, 7)["positive"]


def test_malefic_role_fit_by_house_type():
    on_dusthana = argala_analysis(_chart({"Saturn": 1}, lagna_sign=0, shadbala={"Saturn": 2.0}))
    assert _arg_row(on_dusthana, 12, "Saturn")["role_fit"] == -1.0
    on_upachaya = argala_analysis(_chart({"Saturn": 3}, lagna_sign=0, shadbala={"Saturn": 2.0}))
    assert _arg_row(on_upachaya, 11, "Saturn")["role_fit"] == 1.0


def test_functional_benefic_in_enemy_sign_softens_to_positive():
    # Taurus lagna (Saturn is a functional benefic); Saturn in the 2nd throws
    # (11th-)argala on the 4th (Leo, Saturn's enemy) -> dignity +0.5 not -1.
    out = argala_analysis(_chart({"Saturn": 2}, lagna_sign=1, shadbala={"Saturn": 2.0}))
    row = _arg_row(out, 4, "Saturn")
    assert row is not None
    assert row["dignity"] == "Enemy Sign" and row["dignity_score"] == 0.5


def test_virodha_obstruction_neutralises_not_drops():
    # Jupiter in the 11th throws argala on the 1st, but Saturn in the 3rd (its
    # virodha) is stronger -> survive 0 -> the pair still APPEARS, Jupiter's
    # contribution is 0, and the house verdict is NEUTRAL (not dropped/null).
    out = argala_analysis(_chart({"Jupiter": 11, "Saturn": 3}, lagna_sign=0,
                                 default_house=7,
                                 shadbala={"Jupiter": 1.0, "Saturn": 3.0}))
    h1 = _house(out, 1)
    row = _arg_row(out, 1, "Jupiter")
    assert row is not None and row["contribution"] == 0.0  # obstructed, still shown
    pair = next(p for p in h1["pairs"] if p["argala_from"] == 11)
    assert pair["survive"] == 0.0
    assert any(v["planet"] == "Saturn" for v in pair["virodha"])  # counter is visible
    assert h1["verdict"] == "neutral" and h1["strength"] == 0.0


def test_no_argala_is_null():
    # All grahas in the 1st -> for the 1st house its 2/4/5/11 (and 12/10/9/3)
    # are all empty -> nothing intervenes -> verdict null.
    out = argala_analysis(_chart({p: 1 for p in _ALL9}, shadbala={p: 1.0 for p in _ALL9[:7]}))
    h1 = _house(out, 1)
    assert h1["verdict"] == "null" and h1["strength"] == 0.0 and h1["pairs"] == []


def test_contribution_is_shadbala_times_polarity_times_survive():
    out = argala_analysis(_chart({"Saturn": 11}, lagna_sign=0, shadbala={"Saturn": 2.0}))
    pair = next(p for p in _house(out, 7)["pairs"] for r in p["argala"] if r["planet"] == "Saturn")
    row = _arg_row(out, 7, "Saturn")
    assert row["contribution"] == round(row["shadbala"] * row["polarity"] * pair["survive"], 3)


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
        assert h["verdict"] in {"null", "neutral", "positive", "negative"}
        for pair in h["pairs"]:
            assert {"argala_from", "virodha_from", "survive", "argala", "virodha"} <= set(pair)
    assert body["shadbala_used"] is True


@pytest.mark.asyncio
async def test_argala_endpoint_bad_input_returns_422(client):
    resp = await client.get(
        "/api/kundli/argala-analysis",
        params={"dob": "not-a-date", "tob": _TOB, "lat": _LAT, "lon": _LON},
    )
    assert resp.status_code == 422
