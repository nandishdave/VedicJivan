"""Tests for the Layer-2 longevity component.

Locks behaviour of the band/label/Balarishta logic and the strength score, plus
a real-ephemeris smoke test. The Ayurdaya *year numbers* are simplified estimates
by design, so tests assert ordering/shape, not exact values.
"""
from app.services.kundli_calculator.longevity import (
    _band_label,
    _balarishta,
    _pindayu,
    longevity,
)
from app.services.muhurta import build_muhurta_chart

_CLASSICAL = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]


def make_chart(*, dignity="Neutral Sign", lord_house=1, paksha="Shukla", moon_house=1):
    planets = {p: {"sign": 0, "house": 1, "dignity": dignity, "degree_in_sign": 10.0}
               for p in _CLASSICAL}
    planets["Moon"]["house"] = moon_house
    planets["Mars"]["house"] = lord_house  # Mars = Aries lord
    return {
        "lagna": {"sign": 0, "degree": 10.0, "sign_name": "Aries", "sign_lord": "Mars"},
        "planets": planets,
        "ashtakavarga": {"totals": [28] * 12},
        "shadbala": {p: {"ratio": 1.0} for p in _CLASSICAL},
        "panchanga": {"paksha": paksha},
    }


def test_band_labels():
    assert _band_label(20) == "Alpayu (short)"
    assert _band_label(50) == "Madhyayu (medium)"
    assert _band_label(75) == "Purnayu (full)"
    assert _band_label(120) == "Amitayu (very long)"


def test_pindayu_rewards_dignity():
    assert _pindayu(make_chart(dignity="Exalted")) > _pindayu(make_chart(dignity="Debilitated"))


def test_balarishta_detects_waning_moon_in_dusthana():
    flags = _balarishta(make_chart(paksha="Krishna", moon_house=8))
    assert any("Waning Moon" in f for f in flags)


def test_balarishta_detects_weak_lagna_lord():
    flags = _balarishta(make_chart(lord_house=8))  # Mars (Aries lord) in 8th
    assert any("Lagna-lord" in f for f in flags)


def test_balarishta_penalises_score():
    clean = longevity(make_chart())["score"]
    afflicted = longevity(make_chart(paksha="Krishna", moon_house=8, lord_house=12))["score"]
    assert afflicted < clean


def test_shape_and_bounds():
    out = longevity(make_chart())
    assert 0.0 <= out["score"] <= 100.0
    assert set(out["ayurdaya"]) >= {"pinda", "nisarga", "amsa", "band", "label"}
    assert out["ayurdaya"]["band"][0] <= out["ayurdaya"]["band"][1]
    assert isinstance(out["balarishta"], list) and out["note"]


def test_real_chart_smoke():
    chart = build_muhurta_chart(dob="2026-06-20", tob="09:30", lat=21.7333, lon=70.6167)
    out = longevity(chart)
    assert 0.0 <= out["score"] <= 100.0
    a = out["ayurdaya"]
    assert a["pinda"] > 0 and a["nisarga"] > 0 and a["amsa"] > 0
    assert a["label"].split()[0] in {"Alpayu", "Madhyayu", "Purnayu", "Amitayu"}
