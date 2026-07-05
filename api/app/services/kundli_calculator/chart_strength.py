"""Composite chart-strength scoring for the Unshakable Chart Finder.

Layer 1 (this module, for now) — **structural strength**: a 0-100 score built
purely from the *rigorous* classical metrics we already compute (Shadbala,
Ashtakavarga, dignity, Lagna-lord, benefic placement). No heuristics yet — the
"greatness" layer (yoga strength, longevity, fame) is added in Phase 2.

All weights and the score-mapping curves are deliberately a **first pass** and
are meant to be tuned. The unit tests lock *behaviour* (a stronger chart scores
higher), not the exact magic numbers, so the curves can move freely.

Input: a chart dict as produced by `build_muhurta_chart`/`build_chart` — it must
carry ``shadbala`` (per-planet ``ratio``), ``ashtakavarga`` (``totals`` per
sign), ``planets`` (each with ``dignity``/``house``) and ``lagna`` (``sign`` +
``sign_lord``).
"""
from __future__ import annotations

# Shared 0-100 dignity scale + average-SAV constant — one source of truth (dignity.py).
from app.services.kundli_calculator.dignity import (
    AVG_SAV as _AVG_SAV,
    DIGNITY_PCT as _DIGNITY_PTS,
)

_CLASSICAL = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_BENEFICS = {"Jupiter", "Venus", "Mercury"}  # natural benefics (kept for reference)

# Functional benefics are lagna-specific — a natural benefic can be a functional
# malefic (e.g. Jupiter rules 3rd+6th for Libra → malefic). Two-group scheme:
# Saturn/Venus/Mercury benefic for Ta,Ge,Vi,Li,Cp,Aq; Sun/Moon/Mars/Jupiter for
# Ar,Cn,Le,Sc,Sg,Pi. (Same scheme used across the codebase.)
_FB_A = {"Saturn", "Venus", "Mercury"}
_FB_B = {"Sun", "Moon", "Mars", "Jupiter"}
_FB_A_SIGNS = {1, 2, 5, 6, 9, 10}  # Taurus, Gemini, Virgo, Libra, Capricorn, Aquarius


def _functional_benefics(chart: dict) -> set:
    """The functional benefics for this chart's ascendant (lagna-specific)."""
    return _FB_A if chart["lagna"]["sign"] in _FB_A_SIGNS else _FB_B
_KENDRA = {1, 4, 7, 10}
_TRIKONA = {1, 5, 9}
_DUSTHANA = {6, 8, 12}
_UPACHAYA = {3, 6, 10, 11}
# _AVG_SAV (28.0) and _DIGNITY_PTS (0-100 dignity scale) are imported from dignity.py.

# Component weights — must sum to 1.0. First-pass; tune freely.
WEIGHTS = {
    "shadbala": 0.35,
    "ashtakavarga": 0.25,
    "dignity": 0.15,
    "lagna_lord": 0.15,
    "placement": 0.10,
}


def _ratio_to_score(ratio: float) -> float:
    """Shadbala ratio (rupas / min-requirement) → 0-100. ratio 1.0 (meets the
    classical minimum) maps to ~67; ratio >= 1.5 saturates at 100."""
    return max(0.0, min(ratio / 1.5, 1.0)) * 100.0


def _shadbala_score(chart: dict) -> float:
    """Weighted-average planetary strength, leaning on the Lagna-lord + benefics
    (the planets that most carry a chart)."""
    sb = chart.get("shadbala", {})
    lord = chart["lagna"].get("sign_lord")
    benefics = _functional_benefics(chart)
    num = den = 0.0
    for p in _CLASSICAL:
        s = _ratio_to_score(sb.get(p, {}).get("ratio", 0.0))
        w = 2.0 if p == lord else (1.4 if p in benefics else 1.0)
        num += s * w
        den += w
    return num / den if den else 0.0


def _ashtakavarga_score(chart: dict) -> float:
    """Average SAV bindus across the chart's strongest houses (Lagna + kendras +
    trikonas), normalised: 18 bindus -> 0, ~28 (avg) -> ~45, 40+ -> 100."""
    totals = chart.get("ashtakavarga", {}).get("totals") or [int(_AVG_SAV)] * 12
    lagna_sign = chart["lagna"]["sign"]
    key_houses = {1, 4, 5, 7, 9, 10}  # kendras ∪ trikonas (1 shared)
    sav = [totals[(lagna_sign + h - 1) % 12] for h in key_houses]
    avg = sum(sav) / len(sav)
    return max(0.0, min((avg - 18.0) / (40.0 - 18.0), 1.0)) * 100.0


def _dignity_score(chart: dict) -> float:
    planets = chart.get("planets", {})
    pts = [_DIGNITY_PTS.get(planets.get(p, {}).get("dignity", "Neutral Sign"), 45.0)
           for p in _CLASSICAL]
    return sum(pts) / len(pts)


def _lagna_lord_score(chart: dict) -> float:
    """The Lagna-lord deserves its own component — a weak/afflicted ascendant
    lord undercuts an otherwise strong chart. Blends its Shadbala + dignity +
    house placement."""
    lord = chart["lagna"].get("sign_lord")
    p = chart.get("planets", {}).get(lord, {})
    sb = _ratio_to_score(chart.get("shadbala", {}).get(lord, {}).get("ratio", 0.0))
    dig = _DIGNITY_PTS.get(p.get("dignity", "Neutral Sign"), 45.0)
    house = p.get("house", 0)
    place = (100.0 if house in _TRIKONA else 80.0 if house in _KENDRA
             else 20.0 if house in _DUSTHANA else 55.0)
    return 0.40 * sb + 0.35 * dig + 0.25 * place


def _placement_score(chart: dict) -> float:
    """Benefics thrive in kendras/trikonas; malefics do their best work in the
    upachaya houses (3/6/10/11). First-pass placement quality, 0-100."""
    planets = chart.get("planets", {})
    benefics = _functional_benefics(chart)
    total = num = 0.0
    for p in _CLASSICAL:
        house = planets.get(p, {}).get("house")
        if not house:
            continue
        total += 1
        if p in benefics:
            num += (100.0 if house in (_KENDRA | _TRIKONA)
                    else 25.0 if house in _DUSTHANA else 60.0)
        else:
            num += (70.0 if house in _UPACHAYA
                    else 40.0 if house in _DUSTHANA else 55.0)
    return num / total if total else 50.0


# Composite "Unshakable" score = Layer-1 structural (rigorous, ~65%) + Layer-2
# greatness (yoga/longevity/fame, heuristic, ~35%). Tunable.
LAYER_WEIGHTS = {"structural": 0.65, "yoga": 0.15, "longevity": 0.12, "fame": 0.08}
# When the chart carries a birth date (so the validated worldly-potential layer
# can be computed), it takes a small slot and the others make room. The
# structural anchor stays dominant. Falls back to LAYER_WEIGHTS otherwise, so
# dob-less callers keep their exact prior behaviour.
LAYER_WEIGHTS_WORLDLY = {"structural": 0.60, "yoga": 0.13, "longevity": 0.11, "fame": 0.06, "worldly": 0.10}


def unshakable_score(chart: dict) -> dict:
    """Full 0-100 Unshakable score for a chart: Layer-1 structural strength plus
    the Layer-2 greatness markers (yoga power, longevity strength, fame). Returns
    the blended score, the per-layer scores, and the display extras (Ayurdaya
    band, Balarishta flags, detected yogas, Atmakaraka)."""
    from app.services.kundli_calculator.dhana_yoga import (
        dhana_yoga_normalized, dhana_yoga_score,
        prosperity_yoga_normalized, prosperity_yoga_score,
    )
    from app.services.kundli_calculator.fame import fame
    from app.services.kundli_calculator.longevity import longevity
    from app.services.kundli_calculator.raja_yoga import (
        raja_yoga_normalized, raja_yoga_score,
    )
    from app.services.kundli_calculator.yoga_strength import yoga_strength
    from app.services.kundli_calculator.worldly_potential import worldly_potential
    from app.services.kundli_calculator.life_domains import balanced_life

    s = structural_strength(chart)
    y = yoga_strength(chart)
    lon = longevity(chart)
    fm = fame(chart)
    layers = {"structural": s["score"], "yoga": y["score"],
              "longevity": lon["score"], "fame": fm["score"]}
    # Validated worldly-potential layer — only when the chart has a birth date to
    # time the dashas. Absent -> keep the original 4-layer weights (unchanged behaviour).
    wp = worldly_potential(chart)
    if wp is not None:
        layers["worldly"] = wp["score"]
        weights = LAYER_WEIGHTS_WORLDLY
    else:
        weights = LAYER_WEIGHTS
    score = sum(layers[k] * weights[k] for k in weights)

    # Balanced-Life reading — the SECOND, orthogonal axis to worldly-potential:
    # "does this chart carry a whole, rounded life?" (health, marriage, children,
    # parents, siblings, wealth, career…), with the 2-3 weakest domains named as
    # concern areas. Does not feed the unshakable score — it is a separate lens.
    balanced = balanced_life(chart)

    # Graded classical yogas (separate from the tuned score) — shown per moment.
    dh_s, dh_l = dhana_yoga_score(chart)
    pr_s, pr_l = prosperity_yoga_score(chart)
    rj_s, rj_l = raja_yoga_score(chart)
    # Composite strength stack: how many of 8 strength factors are notably strong
    # (>60/100). A co-occurrence readout oriented to auspiciousness (all "higher=better").
    comp = s["components"]
    _labels = ["Shadbala", "Ashtakavarga", "Dignity", "Lagna-lord", "Placement",
               "Dhana", "Prosperity", "Raja"]
    strength_factors = [
        comp["shadbala"], comp["ashtakavarga"], comp["dignity"],
        comp["lagna_lord"], comp["placement"],
        dhana_yoga_normalized(chart), prosperity_yoga_normalized(chart),
        raja_yoga_normalized(chart),
    ]
    strong = [_labels[i] for i, f in enumerate(strength_factors) if f > 60.0]
    return {
        "score": round(score, 1),
        "layers": layers,
        "structural": s["components"],
        "yogas": y["yogas"],
        "ayurdaya": lon["ayurdaya"],
        "balarishta": lon["balarishta"],
        "atmakaraka": fm["atmakaraka"],
        "dhana": {"score": dh_s, "links": dh_l},
        "prosperity": {"score": pr_s, "links": pr_l},
        "raja": {"score": rj_s, "links": rj_l},
        "strength_stack": {"count": len(strong), "of": len(strength_factors), "strong": strong},
        "worldly_potential": wp,  # None when the chart has no birth date
        "balanced_life": balanced,  # {score, band, concerns, domains} — the whole-life axis
    }


def unshakable_upper_bound(chart: dict) -> float:
    """Admissible upper bound for ``unshakable_score`` from a *cheap* chart (no
    Shadbala): each layer is bounded with a perfect Shadbala, so the composite
    bound is always >= the true composite score. Below the bar -> safe to skip."""
    from app.services.kundli_calculator.fame import upper_bound as _fame_ub
    from app.services.kundli_calculator.longevity import upper_bound as _lon_ub
    from app.services.kundli_calculator.yoga_strength import upper_bound as _yoga_ub

    # Match the weight scheme the real score will use: if the chart has a birth
    # date, the worldly layer is present, so the bound must include it (bounded by
    # its max of 100 — we don't compute it here, to keep the pre-filter cheap).
    has_dob = bool(chart.get("dob"))
    w = LAYER_WEIGHTS_WORLDLY if has_dob else LAYER_WEIGHTS
    bound = (w["structural"] * optimistic_upper_bound(chart)
             + w["yoga"] * _yoga_ub(chart)
             + w["longevity"] * _lon_ub(chart)
             + w["fame"] * _fame_ub(chart))
    if has_dob:
        bound += w["worldly"] * 100.0
    return bound


def optimistic_upper_bound(chart: dict) -> float:
    """Highest `structural_strength` score this chart could *possibly* reach if
    its (not-yet-computed) Shadbala were perfect.

    Admissible bound: every term except Shadbala uses the chart's real cheap
    value; the Shadbala component (and the Shadbala part of the Lagna-lord
    component) are set to their maximum (100). So the bound is always >= the true
    score. If the bound is below the bar, the real score is too — the funnel can
    safely skip the expensive full eval without ever dropping a qualifying chart.

    Accepts a *cheap* chart (no ``shadbala`` key needed) — it reads only
    ashtakavarga, planet dignities/houses and the Lagna.
    """
    av = _ashtakavarga_score(chart)
    dig = _dignity_score(chart)
    place = _placement_score(chart)
    lord = chart["lagna"].get("sign_lord")
    p = chart.get("planets", {}).get(lord, {})
    dig_lord = _DIGNITY_PTS.get(p.get("dignity", "Neutral Sign"), 45.0)
    house = p.get("house", 0)
    place_lord = (100.0 if house in _TRIKONA else 80.0 if house in _KENDRA
                  else 20.0 if house in _DUSTHANA else 55.0)
    ll_max = 0.40 * 100.0 + 0.35 * dig_lord + 0.25 * place_lord  # Shadbala part maxed
    return (WEIGHTS["shadbala"] * 100.0
            + WEIGHTS["ashtakavarga"] * av
            + WEIGHTS["dignity"] * dig
            + WEIGHTS["lagna_lord"] * ll_max
            + WEIGHTS["placement"] * place)


def structural_strength(chart: dict) -> dict:
    """Layer-1 structural-strength score for one chart.

    Returns ``{"score": 0-100, "components": {...}, "layer": "structural"}``.
    """
    comps = {
        "shadbala": _shadbala_score(chart),
        "ashtakavarga": _ashtakavarga_score(chart),
        "dignity": _dignity_score(chart),
        "lagna_lord": _lagna_lord_score(chart),
        "placement": _placement_score(chart),
    }
    score = sum(comps[k] * w for k, w in WEIGHTS.items())
    return {
        "score": round(score, 1),
        "components": {k: round(v, 1) for k, v in comps.items()},
        "layer": "structural",
    }
