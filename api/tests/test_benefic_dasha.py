"""Tests for the functional-benefic dasha-timing layer and its integration into
unshakable_score. Behaviour (ordering of life stages), not magic numbers."""
import pytest

from app.services.kundli_calculator.benefic_dasha import STAGES, benefic_dasha
from app.services.kundli_calculator.chart_strength import (
    LAYER_WEIGHTS_DATED,
    unshakable_score,
    unshakable_upper_bound,
)
from app.services.muhurta import build_muhurta_chart

_DOB, _TOB, _LAT, _LON = "1981-07-07", "12:00", 23.34, 85.31

# Aries lagna (sign 0): functional benefics are Sun / Moon / Mars / Jupiter.
_BENEFIC, _MALEFIC = "Jupiter", "Saturn"


def _chart(periods, rahu_sign=9, ketu_sign=3):
    """Synthetic dated chart. `periods` = [(planet, from_age, to_age), ...] on a
    2000-01-01 birth; gaps are simply years under no listed dasha."""
    return {
        "dob": "2000-01-01",
        "lagna": {"sign": 0},
        "planets": {"Rahu": {"sign": rahu_sign}, "Ketu": {"sign": ketu_sign}},
        "dashas": [
            {"planet": p, "start_date": f"{2000 + a}-01-01", "end_date": f"{2000 + b}-01-01"}
            for p, a, b in periods
        ],
    }


def _score(periods, **kw):
    return benefic_dasha(_chart(periods, **kw))["score"]


def test_all_benefic_scores_100_and_none_scores_0():
    full = benefic_dasha(_chart([(_BENEFIC, 0, 80)]))
    assert full["score"] == pytest.approx(100.0, abs=0.2)
    assert full["years"] == pytest.approx(80.0, abs=0.1)
    assert _score([(_MALEFIC, 0, 80)]) == 0.0


def test_same_years_are_worth_most_in_prime_then_mature_then_edges():
    childhood = _score([(_BENEFIC, 5, 15)])
    prime = _score([(_BENEFIC, 30, 40)])
    mature = _score([(_BENEFIC, 50, 60)])
    late = _score([(_BENEFIC, 65, 75)])
    assert prime > mature > childhood
    assert childhood == pytest.approx(late, abs=0.1)


def test_years_are_split_across_stage_boundaries():
    out = benefic_dasha(_chart([(_BENEFIC, 15, 55)]))
    stages = {k: v["years"] for k, v in out["stages"].items()}
    assert stages == pytest.approx({"childhood": 5, "prime": 30, "mature": 5, "late": 0}, abs=0.1)
    assert out["periods"] == [{"planet": _BENEFIC, "from_age": 15.0, "to_age": 55.0}]


def test_years_past_80_do_not_count():
    assert _score([(_BENEFIC, 70, 95)]) == pytest.approx(_score([(_BENEFIC, 70, 80)]), abs=0.1)
    assert _score([(_BENEFIC, 85, 100)]) == 0.0


def test_node_dasha_takes_its_dispositors_nature():
    # Rahu in Sagittarius (lord Jupiter, a benefic here) vs Capricorn (lord Saturn).
    assert _score([("Rahu", 20, 38)], rahu_sign=8) > 0.0
    assert _score([("Rahu", 20, 38)], rahu_sign=9) == 0.0


def test_benefic_set_follows_the_lagna():
    saturn_prime = [(_MALEFIC, 20, 39)]
    taurus = _chart(saturn_prime)
    taurus["lagna"]["sign"] = 1  # Saturn is a functional benefic for Taurus
    assert benefic_dasha(taurus)["score"] > 0.0 == _score(saturn_prime)


def test_none_without_birth_date():
    chart = _chart([(_BENEFIC, 0, 80)])
    chart.pop("dob")
    assert benefic_dasha(chart) is None


def test_stages_cover_birth_to_80_without_gaps():
    assert STAGES[0][1] == 0 and STAGES[-1][2] == 80
    assert all(STAGES[i][2] == STAGES[i + 1][1] for i in range(len(STAGES) - 1))


# ── integration with the Unshakable score ───────────────────────────────────


def test_dated_weights_sum_to_one_and_structural_dominates():
    assert abs(sum(LAYER_WEIGHTS_DATED.values()) - 1.0) < 1e-9
    assert LAYER_WEIGHTS_DATED["structural"] >= 0.5


def test_unshakable_score_carries_the_layer_for_a_dated_chart():
    chart = build_muhurta_chart(dob=_DOB, tob=_TOB, lat=_LAT, lon=_LON)
    out = unshakable_score(chart)
    bd = out["benefic_dasha"]
    assert out["layers"]["benefic_dasha"] == bd["score"]
    assert 0.0 <= bd["score"] <= 100.0
    assert bd["years"] == pytest.approx(sum(s["years"] for s in bd["stages"].values()), abs=0.3)
    expected = sum(out["layers"][k] * w for k, w in LAYER_WEIGHTS_DATED.items())
    assert out["score"] == pytest.approx(expected, abs=0.06)


def test_unshakable_score_drops_the_layer_without_birth_date():
    chart = build_muhurta_chart(dob=_DOB, tob=_TOB, lat=_LAT, lon=_LON)
    chart.pop("dob", None)
    out = unshakable_score(chart)
    assert out["benefic_dasha"] is None and "benefic_dasha" not in out["layers"]


def test_upper_bound_stays_admissible_with_the_layer():
    """The funnel's cheap bound must never fall below the true score."""
    full = build_muhurta_chart(dob=_DOB, tob=_TOB, lat=_LAT, lon=_LON)
    cheap = build_muhurta_chart(dob=_DOB, tob=_TOB, lat=_LAT, lon=_LON, with_shadbala=False)
    assert unshakable_upper_bound(cheap) >= unshakable_score(full)["score"]
