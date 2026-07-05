"""Tests for the 13-domain life analysis + Balanced-Life score (life_domains.py).

Pure-logic tests (aggregation, concerns, structure, kartari) need no ephemeris;
the varga integration test builds a real chart and runs where swisseph is present
(the container / CI), like the other muhurta ephemeris tests.
"""
import pytest

from app.services.kundli_calculator._core import SIGN_LORDS, SIGN_NAMES
from app.services.kundli_calculator.life_domains import (
    LIFE_ASPECTS,
    _bhava_score,
    _bhavesh_score,
    balanced_life,
    domain_scores,
)

_ALL = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]


def _domsL(pairs):
    """pairs: list of (label, score) → a domain_scores-shaped dict."""
    return {f"k{i}": {"label": lbl, "group": "X", "score": s, "verdict": "good"}
            for i, (lbl, s) in enumerate(pairs)}


def make_chart(*, lagna_sign=0, totals=None, overrides=None, ratios=None, aspected_by=None):
    """Minimal chart dict the scoring helpers accept (no divisional → 3-factor)."""
    planets = {
        p: {"longitude": 100.0, "sign": 10, "sign_name": "Aquarius", "sign_lord": "Saturn",
            "degree_in_sign": 10.0, "house": 11, "retrograde": False, "dignity": "Neutral Sign"}
        for p in _ALL
    }
    for p, o in (overrides or {}).items():
        planets[p].update(o)
    return {
        "lagna": {"sign": lagna_sign, "sign_name": SIGN_NAMES[lagna_sign], "sign_lord": SIGN_LORDS[lagna_sign]},
        "planets": planets,
        "ashtakavarga": {"totals": totals or [28] * 12},
        "shadbala": {p: {"ratio": (ratios or {}).get(p, 1.0)} for p in _ALL},
        "graha_drishti": {"house_aspected_by": aspected_by or {str(h): [] for h in range(1, 13)}},
    }


# ── Structure ────────────────────────────────────────────────────────────────
def test_thirteen_domains_include_siblings():
    keys = [a[0] for a in LIFE_ASPECTS]
    assert len(LIFE_ASPECTS) == 13
    assert "siblings" in keys
    sib = next(a for a in LIFE_ASPECTS if a[0] == "siblings")
    _key, _label, _group, houses, karakas, vargas = sib
    assert houses == [3] and "Mars" in karakas and vargas == ["D3"]


def test_varga_mapping_present_for_key_domains():
    vmap = {a[0]: a[5] for a in LIFE_ASPECTS}
    assert vmap["career"] == ["D10"]
    assert vmap["marriage"] == ["D9"]
    assert vmap["children"] == ["D7"]
    assert vmap["property"] == ["D4", "D16"]   # two vargas
    assert vmap["longevity"] == ["D8"]
    assert vmap["foreign"] == []               # no clean varga → 3-factor


# ── Balanced-Life aggregation (weakest-links) ────────────────────────────────
def test_all_strong_reads_high_and_no_concerns():
    r = balanced_life({}, _domsL([(f"d{i}", 80.0) for i in range(13)]))
    assert r["score"] == pytest.approx(80.0, abs=0.1)
    assert r["band"] == "Very complete"
    assert r["concerns"] == []


def test_one_null_domain_drags_the_score():
    """A chart strong in 12 areas but empty in one must NOT read as a great life."""
    strong = balanced_life({}, _domsL([(f"d{i}", 80.0) for i in range(13)]))
    with_gap = balanced_life(
        {}, _domsL([("Marriage & Spouse", 5.0)] + [(f"d{i}", 80.0) for i in range(12)])
    )
    assert with_gap["score"] < strong["score"] - 20      # the gap bites hard
    assert with_gap["score"] < 65                         # not ~80 despite 12 strong areas
    assert with_gap["concerns"][0] == "Marriage & Spouse"


def test_weakest_links_below_plain_mean():
    pairs = [("A", 90.0), ("B", 20.0)] + [(f"d{i}", 60.0) for i in range(11)]
    mean = sum(s for _, s in pairs) / len(pairs)
    r = balanced_life({}, _domsL(pairs))
    assert r["score"] < mean   # the weak domain pulls it below a naive average


def test_concerns_are_the_weakest_below_bar_max_three():
    pairs = [("Career", 70.0), ("Marriage", 30.0), ("Wealth", 45.0),
             ("Health", 80.0), ("Children", 20.0)] + [(f"d{i}", 75.0) for i in range(8)]
    r = balanced_life({}, _domsL(pairs))
    # below 50, ascending, capped at 3: Children(20) < Marriage(30) < Wealth(45)
    assert r["concerns"] == ["Children", "Marriage", "Wealth"]


# ── Four-fold scoring (synthetic charts, no ephemeris) ───────────────────────
def test_papa_kartari_penalises_the_bhava():
    """A house hemmed by two functional malefics scores lower than an un-hemmed one."""
    base = make_chart(lagna_sign=0)  # all planets parked in house 11
    # Aries lagna: Saturn & Mercury are functional malefics. Flank the 5th (houses 4 & 6).
    hemmed = make_chart(lagna_sign=0, overrides={"Saturn": {"house": 4}, "Mercury": {"house": 6}})
    assert _bhava_score(hemmed, 5) < _bhava_score(base, 5)


def test_bhavesh_rewards_dignified_well_placed_lord():
    """The house-lord factor rises with the lord's dignity + placement."""
    # Aries lagna → 5th house is Leo, lord Sun.
    weak = make_chart(lagna_sign=0, overrides={"Sun": {"dignity": "Debilitated", "house": 6}})
    strong = make_chart(lagna_sign=0, overrides={"Sun": {"dignity": "Exalted", "house": 5}})
    assert _bhavesh_score(strong, 5) > _bhavesh_score(weak, 5) + 30


# ── Integration: the varga actually contributes (needs the real engine) ──────
def test_varga_changes_domain_scores_on_real_chart():
    from app.services.muhurta import build_muhurta_chart
    from app.services.kundli_calculator.life_domains import _aspect_score

    chart = build_muhurta_chart(dob="1990-06-20", tob="09:30", lat=21.75, lon=70.6)
    ds = domain_scores(chart)
    assert len(ds) == 13
    assert all(0.0 <= v["score"] <= 100.0 for v in ds.values())
    # career (D10) with vs without its varga should differ → the varga is used.
    with_varga = _aspect_score(chart, [10, 6], ["Sun", "Saturn"], ["D10"])
    no_varga = _aspect_score(chart, [10, 6], ["Sun", "Saturn"], None)
    assert with_varga != no_varga
    # balanced_life rolls up the same 13 domains.
    bl = balanced_life(chart, ds)
    assert 0.0 <= bl["score"] <= 100.0 and bl["band"] in {"Very complete", "Well-rounded", "Mixed", "Uneven"}
