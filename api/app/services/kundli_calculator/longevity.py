"""Longevity — Layer-2 "greatness" component of the Unshakable score.

Two deliberately-separated outputs:

  - ``score`` (0-100): a **robust longevity-strength** signal built from the
    rigorous metrics we trust — 8th-house (Ayushsthana) + Lagna Ashtakavarga,
    Saturn (Ayushkaraka) Shadbala, and the Lagna-lord — minus a Balarishta
    penalty. THIS is what feeds the composite ranking.

  - ``ayurdaya`` band: three **simplified** classical Ayurdaya year-estimates
    (Pinda / Nisarga / Amsa) shown as a min-max BAND + a classical label. These
    are *indicative display estimates only* — the classical methods openly
    disagree and involve many reduction (harana) rules not all modelled here, so
    we surface a range, never a single "prediction". The ranking does NOT depend
    on them.

HEURISTIC / labelled indicative. Tests lock behaviour, not magic numbers.
"""
from __future__ import annotations

from app.services.kundli_calculator._core import _get_dignity
from app.services.kundli_calculator.divisional import calc_divisional_charts

_CLASSICAL = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_DUSTHANA = {6, 8, 12}

# Classical full-year contribution per planet (max), shared by the methods.
_FULL_YEARS = {
    "Sun": 19, "Moon": 25, "Mars": 15, "Mercury": 12,
    "Jupiter": 15, "Venus": 21, "Saturn": 20,
}
# Dignity -> contribution fraction (proxy for the rashmana / harana reductions).
# Tuned so a balanced chart lands in the realistic Madhya/Purna-ayu range.
_DIGNITY_FRAC = {
    "Exalted": 0.90, "Moolatrikona": 0.82, "Own Sign": 0.78, "Friendly Sign": 0.65,
    "Neutral Sign": 0.55, "Enemy Sign": 0.42, "Debilitated": 0.30,
}


def _ratio_to_score(ratio: float) -> float:
    return max(0.0, min(ratio / 1.5, 1.0)) * 100.0


def _norm_sav(sav: int) -> float:
    return max(0.0, min((sav - 18.0) / (40.0 - 18.0), 1.0)) * 100.0


def _band_label(years: float) -> str:
    """Classical Ayu bands."""
    if years < 33:
        return "Alpayu (short)"
    if years < 66:
        return "Madhyayu (medium)"
    if years < 100:
        return "Purnayu (full)"
    return "Amitayu (very long)"


def _pindayu(chart: dict) -> float:
    """Strength-scaled: each planet's full years x its dignity fraction."""
    planets = chart["planets"]
    return sum(_FULL_YEARS[p] * _DIGNITY_FRAC.get(planets.get(p, {}).get("dignity", "Neutral Sign"), 0.55)
               for p in _CLASSICAL)


def _nisargayu(chart: dict) -> float:
    """Natural lifespan: full years lightly reduced when a planet sits in a
    dusthana (6/8/12)."""
    planets = chart["planets"]
    return sum(_FULL_YEARS[p] * (0.45 if planets.get(p, {}).get("house") in _DUSTHANA else 0.62)
               for p in _CLASSICAL)


def _amsayu(chart: dict) -> float:
    """Navamsa-based: full years x the planet's dignity fraction in its D9 sign."""
    d9 = calc_divisional_charts(chart["planets"], chart["lagna"]).get("D9", {})
    total = 0.0
    for p in _CLASSICAL:
        nav_sign = d9.get(p)
        frac = _DIGNITY_FRAC.get(_get_dignity(p, nav_sign), 0.55) if nav_sign is not None else 0.55
        total += _FULL_YEARS[p] * frac
    return total


def _balarishta(chart: dict) -> list[str]:
    """A few well-known infant-mortality (Balarishta) indicators. NOT exhaustive
    and ignores Balarishta-bhanga (cancellations); advisory only — they lower the
    longevity score and flag reduced confidence."""
    flags: list[str] = []
    planets = chart["planets"]
    paksha = chart.get("panchanga", {}).get("paksha")
    moon_h = planets.get("Moon", {}).get("house")
    if paksha == "Krishna" and moon_h in _DUSTHANA:
        flags.append("Waning Moon in a dusthana (6/8/12)")
    lord = chart["lagna"].get("sign_lord")
    lp = planets.get(lord, {})
    if lp.get("dignity") == "Debilitated" or lp.get("house") in _DUSTHANA:
        flags.append("Lagna-lord debilitated or in a dusthana")
    return flags


def _structural_score(chart: dict) -> float:
    totals = chart.get("ashtakavarga", {}).get("totals") or [28] * 12
    ls = chart["lagna"]["sign"]
    sb = chart.get("shadbala", {})
    eighth = _norm_sav(totals[(ls + 7) % 12])  # 8th = Ayushsthana
    first = _norm_sav(totals[ls])              # 1st = vitality
    saturn = _ratio_to_score(sb.get("Saturn", {}).get("ratio", 1.0))  # Ayushkaraka
    lord = _ratio_to_score(sb.get(chart["lagna"].get("sign_lord"), {}).get("ratio", 1.0))
    return 0.30 * eighth + 0.25 * first + 0.25 * saturn + 0.20 * lord


def longevity(chart: dict) -> dict:
    """Longevity strength score (0-100) + an indicative Ayurdaya year-band."""
    methods = {
        "pinda": round(_pindayu(chart), 1),
        "nisarga": round(_nisargayu(chart), 1),
        "amsa": round(_amsayu(chart), 1),
    }
    lo, hi = min(methods.values()), max(methods.values())
    flags = _balarishta(chart)
    score = max(0.0, _structural_score(chart) - 12.0 * len(flags))
    return {
        "score": round(score, 1),
        "ayurdaya": {**methods, "band": [round(lo, 1), round(hi, 1)],
                     "label": _band_label((lo + hi) / 2)},
        "balarishta": flags,
        "note": ("Simplified Ayurdaya estimates; classical methods disagree and "
                 "many harana reductions are not modelled — indicative band, not a prediction."),
    }


def upper_bound(chart: dict) -> float:
    """Max longevity score with a perfect Saturn + Lagna-lord Shadbala and no
    Balarishta penalty — admissible bound for the funnel (uses only the cheap
    Ashtakavarga)."""
    totals = chart.get("ashtakavarga", {}).get("totals") or [28] * 12
    ls = chart["lagna"]["sign"]
    eighth = _norm_sav(totals[(ls + 7) % 12])
    first = _norm_sav(totals[ls])
    return 0.30 * eighth + 0.25 * first + 0.25 * 100.0 + 0.20 * 100.0
