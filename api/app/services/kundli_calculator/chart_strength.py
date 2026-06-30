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

_CLASSICAL = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_BENEFICS = {"Jupiter", "Venus", "Mercury"}
_KENDRA = {1, 4, 7, 10}
_TRIKONA = {1, 5, 9}
_DUSTHANA = {6, 8, 12}
_UPACHAYA = {3, 6, 10, 11}
_AVG_SAV = 28.0  # average Sarvashtakavarga bindus per sign (337 / 12 ≈ 28)

# Dignity → 0-100 strength points (classification strings from `_get_dignity`).
_DIGNITY_PTS = {
    "Exalted": 100.0, "Moolatrikona": 85.0, "Own Sign": 75.0,
    "Friendly Sign": 55.0, "Neutral Sign": 45.0, "Enemy Sign": 25.0,
    "Debilitated": 5.0,
}

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
    num = den = 0.0
    for p in _CLASSICAL:
        s = _ratio_to_score(sb.get(p, {}).get("ratio", 0.0))
        w = 2.0 if p == lord else (1.4 if p in _BENEFICS else 1.0)
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
    total = num = 0.0
    for p in _CLASSICAL:
        house = planets.get(p, {}).get("house")
        if not house:
            continue
        total += 1
        if p in _BENEFICS:
            num += (100.0 if house in (_KENDRA | _TRIKONA)
                    else 25.0 if house in _DUSTHANA else 60.0)
        else:
            num += (70.0 if house in _UPACHAYA
                    else 40.0 if house in _DUSTHANA else 55.0)
    return num / total if total else 50.0


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
