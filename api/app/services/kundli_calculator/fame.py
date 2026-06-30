"""Name & Fame (Yaśa) — Layer-2 "greatness" component of the Unshakable score.

There is no single classical "fame score", so this is the most openly HEURISTIC
component (labelled indicative). It blends the recognised fame significators:
  - 10th house (Karma/status) Ashtakavarga strength,
  - the 10th lord's Shadbala,
  - the Sun (Karaka of authority/fame) Shadbala + a bonus for sitting in a kendra
    (especially the 10th, where it gets Dig Bala),
  - the Atmakaraka (Jaimini "soul significator" = highest-degree planet) strength.

Tests lock behaviour, not the magic numbers.
"""
from __future__ import annotations

from app.services.kundli_calculator._core import SIGN_LORDS

_CLASSICAL = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_KENDRA = {1, 4, 7, 10}


def _ratio_to_score(ratio: float) -> float:
    return max(0.0, min(ratio / 1.5, 1.0)) * 100.0


def _norm_sav(sav: int) -> float:
    return max(0.0, min((sav - 18.0) / (40.0 - 18.0), 1.0)) * 100.0


def _atmakaraka(chart: dict) -> str:
    """Jaimini Atmakaraka — the planet at the highest degree within its sign
    (among the 7 classical grahas)."""
    planets = chart["planets"]
    return max(_CLASSICAL, key=lambda p: planets.get(p, {}).get("degree_in_sign", 0.0))


def fame(chart: dict) -> dict:
    """0-100 fame (Yaśa) heuristic + its components and the Atmakaraka."""
    totals = chart.get("ashtakavarga", {}).get("totals") or [28] * 12
    ls = chart["lagna"]["sign"]
    sb = chart.get("shadbala", {})

    tenth_sav = _norm_sav(totals[(ls + 9) % 12])
    tenth_lord = SIGN_LORDS[(ls + 9) % 12]
    tenth_lord_sb = _ratio_to_score(sb.get(tenth_lord, {}).get("ratio", 1.0))

    sun = chart["planets"].get("Sun", {})
    sun_sb = _ratio_to_score(sb.get("Sun", {}).get("ratio", 1.0))
    sun_house = sun.get("house", 0)
    sun_bonus = 100.0 if sun_house == 10 else 75.0 if sun_house in _KENDRA else 50.0
    sun_score = 0.6 * sun_sb + 0.4 * sun_bonus

    ak = _atmakaraka(chart)
    ak_sb = _ratio_to_score(sb.get(ak, {}).get("ratio", 1.0))

    comps = {
        "tenth_house": round(tenth_sav, 1),
        "tenth_lord": round(tenth_lord_sb, 1),
        "sun": round(sun_score, 1),
        "atmakaraka": round(ak_sb, 1),
    }
    score = 0.30 * tenth_sav + 0.25 * tenth_lord_sb + 0.25 * sun_score + 0.20 * ak_sb
    return {"score": round(score, 1), "components": comps, "atmakaraka": ak}
