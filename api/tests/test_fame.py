"""Behavioural tests for the Layer-2 fame (Yaśa) heuristic."""
from app.services.kundli_calculator.fame import _atmakaraka, fame
from app.services.muhurta import build_muhurta_chart

_CLASSICAL = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]


def make_chart(*, sav=28, ratio=1.0, sun_house=1, degrees=None):
    planets = {p: {"sign": 0, "house": 1, "degree_in_sign": (degrees or {}).get(p, 10.0)}
               for p in _CLASSICAL}
    planets["Sun"]["house"] = sun_house
    return {
        "lagna": {"sign": 0, "sign_name": "Aries", "sign_lord": "Mars"},
        "planets": planets,
        "ashtakavarga": {"totals": [sav] * 12},
        "shadbala": {p: {"ratio": ratio} for p in _CLASSICAL},
    }


def test_atmakaraka_is_highest_degree_planet():
    ak = _atmakaraka(make_chart(degrees={"Venus": 29.0}))
    assert ak == "Venus"


def test_score_bounded():
    s = fame(make_chart())["score"]
    assert 0.0 <= s <= 100.0


def test_strong_tenth_lifts_fame():
    hi = fame(make_chart(sav=42, ratio=1.6))["score"]
    lo = fame(make_chart(sav=18, ratio=0.3))["score"]
    assert hi > lo


def test_sun_in_tenth_beats_sun_in_dusthana():
    hi = fame(make_chart(sun_house=10))["score"]
    lo = fame(make_chart(sun_house=6))["score"]
    assert hi > lo


def test_components_and_ak_present():
    out = fame(make_chart(degrees={"Jupiter": 28.0}))
    assert set(out["components"]) == {"tenth_house", "tenth_lord", "sun", "atmakaraka"}
    assert out["atmakaraka"] == "Jupiter"


def test_real_chart_smoke():
    chart = build_muhurta_chart(dob="2026-06-20", tob="09:30", lat=21.7333, lon=70.6167)
    out = fame(chart)
    assert 0.0 <= out["score"] <= 100.0
    assert out["atmakaraka"] in _CLASSICAL
