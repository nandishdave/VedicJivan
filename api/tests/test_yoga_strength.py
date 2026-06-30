"""Behavioural tests for the Layer-2 yoga-strength component.

Yoga detection is driven by `calc_yogas`; here we patch it to inject known yogas
and lock the *weighting* behaviour (type ranking, Shadbala boost, penalties),
plus one real-ephemeris smoke test.
"""
from app.services.kundli_calculator import yoga_strength as ys_mod
from app.services.kundli_calculator.yoga_strength import yoga_strength
from app.services.muhurta import build_muhurta_chart

_PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]


def make_chart(ratio=1.0):
    return {
        "lagna": {"sign": 0, "sign_name": "Aries", "sign_lord": "Mars"},
        "planets": {p: {"sign": 0, "house": 1, "longitude": 10.0} for p in _PLANETS},
        "shadbala": {p: {"ratio": ratio} for p in _PLANETS},
    }


def test_no_yogas_scores_zero(mocker):
    mocker.patch.object(ys_mod, "calc_yogas", return_value=[])
    assert yoga_strength(make_chart())["score"] == 0.0


def test_mahapurusha_outweighs_dhana(mocker):
    maha = [{"name": "Hamsa", "type": "mahapurusha", "planets": ["Jupiter"]}]
    dhan = [{"name": "X", "type": "dhan", "planets": ["Jupiter"]}]
    mocker.patch.object(ys_mod, "calc_yogas", return_value=maha)
    hi = yoga_strength(make_chart())["score"]
    mocker.patch.object(ys_mod, "calc_yogas", return_value=dhan)
    lo = yoga_strength(make_chart())["score"]
    assert hi > lo


def test_strong_forming_planets_boost_the_yoga(mocker):
    y = [{"name": "Ruchaka", "type": "mahapurusha", "planets": ["Mars"]}]
    mocker.patch.object(ys_mod, "calc_yogas", return_value=y)
    strong = yoga_strength(make_chart(ratio=1.6))["score"]
    weak = yoga_strength(make_chart(ratio=0.3))["score"]
    assert strong > weak


def test_challenging_yoga_is_not_positive(mocker):
    mocker.patch.object(ys_mod, "calc_yogas",
                        return_value=[{"name": "Kemadruma", "type": "challenging", "planets": ["Moon"]}])
    assert yoga_strength(make_chart())["score"] == 0.0  # clamped at 0


def test_score_bounded_and_shaped(mocker):
    many = [{"name": f"R{i}", "type": "raj", "planets": ["Jupiter", "Venus"]} for i in range(8)]
    mocker.patch.object(ys_mod, "calc_yogas", return_value=many)
    out = yoga_strength(make_chart(ratio=1.5))
    assert 0.0 <= out["score"] < 100.0  # diminishing-returns curve never hits exactly 100
    assert out["score"] > 90.0          # but 8 strong raja yogas still score very high
    assert len(out["yogas"]) == 8


def test_real_chart_smoke():
    chart = build_muhurta_chart(dob="2026-06-20", tob="09:30", lat=21.7333, lon=70.6167)
    out = yoga_strength(chart)
    assert 0.0 <= out["score"] <= 100.0
    assert isinstance(out["yogas"], list)
