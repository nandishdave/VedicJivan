"""Behavioural tests for the Layer-1 structural-strength score.

These lock *behaviour* (a stronger chart scores higher; the score stays in
0-100) rather than exact numbers, so the first-pass weights/curves in
`chart_strength.py` can be retuned without churning the tests.
"""
from app.services.kundli_calculator.chart_strength import (
    WEIGHTS,
    _functional_benefics,
    structural_strength,
    unshakable_score,
    unshakable_upper_bound,
)
from app.services.kundli_calculator._core import SIGN_LORDS, SIGN_NAMES
from app.services.muhurta import analyze_birth_muhurta, build_muhurta_chart

_CLASSICAL = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]


def make_chart(*, lagna_sign=0, ratio=1.0, dignity="Neutral Sign", sav=28, house=11):
    """Minimal chart dict the scorer accepts, with uniform knobs so a test can
    dial one factor up/down."""
    return {
        "lagna": {"sign": lagna_sign, "sign_name": SIGN_NAMES[lagna_sign],
                  "sign_lord": SIGN_LORDS[lagna_sign]},
        "planets": {p: {"sign": 10, "house": house, "dignity": dignity} for p in _CLASSICAL},
        "shadbala": {p: {"ratio": ratio} for p in _CLASSICAL},
        "ashtakavarga": {"totals": [sav] * 12},
    }


def test_weights_sum_to_one():
    assert abs(sum(WEIGHTS.values()) - 1.0) < 1e-9


def test_functional_benefics_are_lagna_specific():
    # Libra (sign 6): Jupiter rules 3rd+6th -> functional MALEFIC, not a benefic.
    libra = _functional_benefics(make_chart(lagna_sign=6))
    assert libra == {"Saturn", "Venus", "Mercury"} and "Jupiter" not in libra
    # Aries (sign 0): Jupiter (5th+... trikona lord) IS a functional benefic.
    aries = _functional_benefics(make_chart(lagna_sign=0))
    assert "Jupiter" in aries and "Venus" not in aries


def test_score_bounded():
    s = structural_strength(make_chart())["score"]
    assert 0.0 <= s <= 100.0


def test_strong_chart_scores_high():
    strong = structural_strength(make_chart(
        ratio=1.8, dignity="Exalted", sav=42, house=1,  # benefics in kendra/trikona
    ))["score"]
    assert strong > 75


def test_weak_chart_scores_low():
    weak = structural_strength(make_chart(
        ratio=0.3, dignity="Debilitated", sav=18, house=8,
    ))["score"]
    assert weak < 40


def test_shadbala_is_monotonic():
    lo = structural_strength(make_chart(ratio=0.4))["score"]
    hi = structural_strength(make_chart(ratio=1.6))["score"]
    assert hi > lo


def test_ashtakavarga_is_monotonic():
    lo = structural_strength(make_chart(sav=20))["score"]
    hi = structural_strength(make_chart(sav=40))["score"]
    assert hi > lo


def test_dignity_is_monotonic():
    lo = structural_strength(make_chart(dignity="Debilitated"))["score"]
    hi = structural_strength(make_chart(dignity="Exalted"))["score"]
    assert hi > lo


def test_components_present():
    out = structural_strength(make_chart())
    assert set(out["components"]) == set(WEIGHTS)
    assert out["layer"] == "structural"


def test_real_chart_smoke():
    """Runs on a real ephemeris chart: the score is a sane 0-100 and every
    component is populated."""
    # Reuse the muhurta engine to get a real, fully-populated chart.
    res = analyze_birth_muhurta(
        dob="2026-06-20", lat=21.7333, lon=70.6167, place_name="Jetpur",
        chart_fn=build_muhurta_chart, time="09:30",
    )
    # Rebuild the highlighted Lagna's chart and score it.
    chart = build_muhurta_chart(dob="2026-06-20", tob="09:30", lat=21.7333, lon=70.6167)
    out = structural_strength(chart)
    assert 0.0 <= out["score"] <= 100.0
    assert all(0.0 <= v <= 100.0 for v in out["components"].values())
    assert res["highlight_lagna"]  # sanity: the engine still highlights


def test_unshakable_composite_and_admissible_bound():
    """The composite is well-shaped, and the cheap upper bound is >= the true
    full-chart score (the funnel's safety guarantee, checked on a real chart)."""
    args = dict(dob="2026-06-20", tob="03:01", lat=21.7333, lon=70.6167)
    full = build_muhurta_chart(**args)
    cheap = build_muhurta_chart(**args, with_shadbala=False)

    out = unshakable_score(full)
    assert 0.0 <= out["score"] <= 100.0
    assert set(out["layers"]) == {"structural", "yoga", "longevity", "fame"}
    assert "band" in out["ayurdaya"] and "atmakaraka" in out
    # Graded yogas + composite strength-stack surfaced for the report.
    for k in ("dhana", "prosperity", "raja"):
        assert out[k]["score"] >= 0.0 and isinstance(out[k]["links"], list)
    assert out["strength_stack"]["of"] == 8
    assert 0 <= out["strength_stack"]["count"] <= 8

    # Admissibility: the bound (from the cheap, no-Shadbala chart) never under-
    # states the true composite score -> the funnel can't drop a qualifying chart.
    assert unshakable_upper_bound(cheap) >= out["score"] - 1e-6
