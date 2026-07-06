"""Tests for the Argala calculator (argala.py + the /argala-analysis endpoint).

The quality model scores each effective argala by ① the giver's dignity toward
the house it locks, ② its natural-nature/house-type fit, weighted by ③ Shadbala.
Unit tests assert at the intervener level (deterministic regardless of the other
grahas); the endpoint test builds a real ephemeris chart. Aries lagna = sign 0.
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


def _iv(out: dict, house: int, planet: str):
    return next((i for i in _house(out, house)["interveners"] if i["planet"] == planet), None)


def test_structure_all_twelve_houses_bounded():
    out = argala_analysis(_chart({}, shadbala={p: 1.0 for p in _ALL9[:7]}))
    assert [h["house"] for h in out["houses"]] == list(range(1, 13))
    for h in out["houses"]:
        assert -100.0 <= h["strength"] <= 100.0
        assert isinstance(h["interveners"], list)


def test_exalted_malefic_reads_positive():
    # Aries lagna; Saturn in the 11th throws (5th-)argala on the 7th house (Libra),
    # where Saturn is EXALTED. Despite being a malefic, dignity +2 -> positive.
    out = argala_analysis(_chart({"Saturn": 11}, lagna_sign=0, shadbala={"Saturn": 2.0}))
    iv = _iv(out, 7, "Saturn")
    assert iv is not None
    assert iv["dignity"] == "Exalted" and iv["dignity_score"] == 2.0
    assert iv["polarity"] > 0
    assert "Saturn" in _house(out, 7)["positive"]


def test_malefic_role_fit_by_house_type():
    # A malefic helps upachaya houses and harms dusthana houses.
    # Saturn in the 1st is the 2nd from the 12th -> (2nd-)argala on the 12th
    # (dusthana): role_fit -1.
    on_dusthana = argala_analysis(_chart({"Saturn": 1}, lagna_sign=0, shadbala={"Saturn": 2.0}))
    assert _iv(on_dusthana, 12, "Saturn")["role_fit"] == -1.0
    # Saturn in the 3rd is the 5th from the 11th -> (5th-)argala on the 11th
    # (upachaya): role_fit +1.
    on_upachaya = argala_analysis(_chart({"Saturn": 3}, lagna_sign=0, shadbala={"Saturn": 2.0}))
    assert _iv(on_upachaya, 11, "Saturn")["role_fit"] == 1.0


def test_functional_benefic_in_enemy_sign_softens_to_positive():
    # Taurus lagna (Saturn is a functional benefic). Saturn in the 2nd throws
    # (11th-)argala on the 4th house (Leo) — Saturn's ENEMY sign — but as a
    # functional benefic the dignity score is +0.5, not -1.
    out = argala_analysis(_chart({"Saturn": 2}, lagna_sign=1, shadbala={"Saturn": 2.0}))
    iv = _iv(out, 4, "Saturn")
    assert iv is not None
    assert iv["dignity"] == "Enemy Sign" and iv["dignity_score"] == 0.5


def test_virodha_obstruction_drops_the_intervener():
    # Jupiter in the 11th would throw argala on the 1st, but Saturn in the 3rd
    # (its virodha) is stronger -> the argala is obstructed and Jupiter is not
    # listed as an intervener on the 1st.
    out = argala_analysis(_chart({"Jupiter": 11, "Saturn": 3}, lagna_sign=0,
                                 default_house=7,
                                 shadbala={"Jupiter": 1.0, "Saturn": 3.0}))
    assert _iv(out, 1, "Jupiter") is None
    assert _house(out, 1)["interveners"] == []


def test_contribution_is_shadbala_times_polarity():
    out = argala_analysis(_chart({"Saturn": 11}, lagna_sign=0, shadbala={"Saturn": 2.0}))
    iv = _iv(out, 7, "Saturn")
    assert iv["contribution"] == round(iv["shadbala"] * iv["polarity"], 3)


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
        assert isinstance(h["interveners"], list)
        for iv in h["interveners"]:
            assert {"planet", "dignity", "dignity_score", "role_fit",
                    "shadbala", "polarity", "contribution"} <= set(iv)
    assert body["shadbala_used"] is True


@pytest.mark.asyncio
async def test_argala_endpoint_bad_input_returns_422(client):
    resp = await client.get(
        "/api/kundli/argala-analysis",
        params={"dob": "not-a-date", "tob": _TOB, "lat": _LAT, "lon": _LON},
    )
    assert resp.status_code == 422
