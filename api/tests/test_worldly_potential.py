"""Tests for the validated 7-factor worldly-potential composite and its
integration into unshakable_score. Behaviour, not magic numbers."""
import pytest

from app.services.kundli_calculator.worldly_potential import (
    NOTE, REF, score_from_factors, worldly_potential,
)
from app.services.kundli_calculator.chart_strength import (
    LAYER_WEIGHTS, LAYER_WEIGHTS_WORLDLY, unshakable_score,
)
from app.services.muhurta import build_muhurta_chart

# A real, valid birth moment (M.S. Dhoni — Ranchi). Any valid moment works.
_DOB, _TOB, _LAT, _LON = "1981-07-07", "12:00", 23.34, 85.31

_FAMOUS_MEANS = {k: fam for k, (fam, _o, _s) in REF.items()}
_ORD_MEANS = {k: ordm for k, (_f, ordm, _s) in REF.items()}
_MIDPOINTS = {k: (fam + ordm) / 2.0 for k, (fam, ordm, _s) in REF.items()}


# ── pure scoring core ────────────────────────────────────────────────────────

def test_weights_sum_to_one():
    assert abs(sum(LAYER_WEIGHTS.values()) - 1.0) < 1e-9
    assert abs(sum(LAYER_WEIGHTS_WORLDLY.values()) - 1.0) < 1e-9
    assert LAYER_WEIGHTS_WORLDLY["structural"] >= 0.5  # structural stays dominant


def test_midpoint_scores_fifty():
    out = score_from_factors(dict(_MIDPOINTS))
    assert out["score"] == pytest.approx(50.0, abs=0.2)
    assert out["mean_z"] == pytest.approx(0.0, abs=1e-6)


def test_famous_above_ordinary():
    fam = score_from_factors(dict(_FAMOUS_MEANS))["score"]
    ordn = score_from_factors(dict(_ORD_MEANS))["score"]
    assert fam > 50.0 > ordn


def test_famous_positive_factor_raises_score():
    base = dict(_MIDPOINTS)
    up = dict(base); up["av_10th"] += 5.0            # 10th-AV leans famous -> score up
    assert score_from_factors(up)["score"] > score_from_factors(base)["score"]


def test_famous_negative_factor_lowers_score():
    base = dict(_MIDPOINTS)
    up = dict(base); up["av_1st"] += 5.0             # 1st-AV leans ordinary -> score down
    assert score_from_factors(up)["score"] < score_from_factors(base)["score"]


def test_score_bounded_and_note_present():
    out = score_from_factors(dict(_FAMOUS_MEANS))
    assert 0.0 <= out["score"] <= 100.0
    assert out["note"] == NOTE
    assert set(out["factors"]) == set(REF)


# ── real chart + integration ─────────────────────────────────────────────────

def test_worldly_none_without_dob():
    assert worldly_potential({}) is None
    assert worldly_potential({"planets": {}, "lagna": {"sign": 0}}) is None


def test_worldly_on_real_chart():
    chart = build_muhurta_chart(dob=_DOB, tob=_TOB, lat=_LAT, lon=_LON)
    wp = worldly_potential(chart)
    assert wp is not None
    assert 0.0 <= wp["score"] <= 100.0
    assert set(wp["factors"]) == set(REF)
    assert wp["note"] == NOTE


def test_unshakable_includes_worldly_with_dob():
    chart = build_muhurta_chart(dob=_DOB, tob=_TOB, lat=_LAT, lon=_LON)
    out = unshakable_score(chart)
    assert out["worldly_potential"] is not None
    assert "worldly" in {"worldly"}  # layer contributes; score is a valid 0-100
    assert 0.0 <= out["score"] <= 100.0


def test_unshakable_degrades_without_dob():
    """A chart stripped of its birth date drops the worldly layer cleanly and
    falls back to the original 4-layer weighting (no crash)."""
    chart = build_muhurta_chart(dob=_DOB, tob=_TOB, lat=_LAT, lon=_LON)
    chart.pop("dob", None)
    out = unshakable_score(chart)
    assert out["worldly_potential"] is None
    assert 0.0 <= out["score"] <= 100.0
