"""Tests for the auspicious/poison degree calculator (degree_calculator.py).
Pure — no ephemeris; synthetic chart dicts with known degrees."""
from app.services.kundli_calculator.degree_calculator import degree_analysis


def _chart(planets, lagna_sign, lagna_deg):
    return {"planets": planets, "lagna": {"sign": lagna_sign, "degree": lagna_deg}}


def test_covers_all_bodies_and_ascendant():
    planets = {p: {"sign": 0, "degree_in_sign": 12.0} for p in
               ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn",
                "Rahu", "Ketu", "Uranus", "Neptune", "Pluto"]}
    out = degree_analysis(_chart(planets, 0, 12.0))
    names = [b["body"] for b in out["bodies"]]
    assert len(out["bodies"]) == 13
    assert names[-1] == "Ascendant"
    assert "Uranus" in names and "Pluto" in names


def test_outer_planets_have_no_mrityu_table():
    planets = {"Uranus": {"sign": 5, "degree_in_sign": 10.0}}
    out = degree_analysis(_chart(planets, 0, 5.0))
    ur = next(b for b in out["bodies"] if b["body"] == "Uranus")
    assert ur["mrityu_bhaga"] is None          # no classical table → null
    assert isinstance(ur["vish_navamsa"], bool)  # sign-based checks still apply


def test_known_poison_and_auspicious_hits():
    # Sun in Leo (sign 4) at 8° → Mṛtyu-Bhāga for Sun-Leo is 8° → hit.
    # Ascendant in Aries (sign 0) at 1° → Vish navamsa (nav 1) AND Mṛtyu Lagna-Aries 1°.
    # Mars in Sagittarius (sign 8, Fire) at 21° → nav 7 = a Pushkara navamsa.
    planets = {
        "Sun": {"sign": 4, "degree_in_sign": 8.0},
        "Mars": {"sign": 8, "degree_in_sign": 21.0},
    }
    out = degree_analysis(_chart(planets, 0, 1.0))
    by = {b["body"]: b for b in out["bodies"]}
    assert by["Sun"]["mrityu_bhaga"] is True
    assert by["Sun"]["vish_navamsa"] is False
    assert by["Mars"]["pushkara_navamsa"] is True
    asc = by["Ascendant"]
    assert asc["vish_navamsa"] is True and asc["mrityu_bhaga"] is True


def test_totals_count_hits():
    planets = {"Sun": {"sign": 4, "degree_in_sign": 8.0}}     # 1 mrityu hit
    out = degree_analysis(_chart(planets, 0, 1.0))            # ascendant: vish + mrityu
    assert out["totals"]["mrityu_bhaga"] == 2                 # Sun-Leo + Ascendant-Aries
    assert out["totals"]["vish_navamsa"] == 1                 # Ascendant only
