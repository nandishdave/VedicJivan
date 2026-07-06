"""Argala (Jaimini "intervention/bolt") per-house analysis for the calculator.

For each of the 12 houses this reports the Shadbala-weighted Śubha (benefic)
vs Pāpa (malefic) argala that is *effective* — i.e. the intervening house
outweighs its Virodha (counter) house — the signed strength %, and the
planets contributing on each side.

Shares its geometry with worldly_potential factor 13 (``_positive_argala``):
  ARG_PAIRS = (argala house Nth-from-reference, its virodha Nth-from-reference).
Factor 13 restricts the reference to the fame houses {2, 10, 12}; this
calculator sweeps ALL 12 houses so a reader can inspect any bhāva.

Positive vs negative is the planet's natural benefic/malefic nature, with the
Moon benefic only in the bright (Shukla) fortnight. Strength % is the
Shadbala tilt: (pos − neg) / (pos + neg) × 100, so +100 = every intervener a
strong benefic, −100 = every intervener a strong malefic, 0 = balanced/none.
"""

from __future__ import annotations

# All nine grahas can throw argala.
_ARG_PLANETS = [
    "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu",
]
# (argala house Nth-from-reference, its virodha/counter house Nth-from-reference).
# 11th (primary) is countered by the 3rd; 2nd/4th/5th by 12th/10th/9th.
_ARG_PAIRS = ((2, 12), (4, 10), (5, 9), (11, 3))
_NATURAL_BENEFIC = {"Jupiter", "Venus", "Mercury"}

# Functional (lagna-specific) benefics — the two-group scheme also used by the
# fame model (chart_strength._functional_benefics): for the ascendants
# Ta/Ge/Vi/Li/Cp/Aq, Saturn/Venus/Mercury are the functional benefics; for the
# other six, Sun/Moon/Mars/Jupiter. Rāhu/Ketu are in neither -> malefic.
_FB_A = {"Saturn", "Venus", "Mercury"}
_FB_B = {"Sun", "Moon", "Mars", "Jupiter"}
_FB_A_SIGNS = {1, 2, 5, 6, 9, 10}  # Taurus, Gemini, Virgo, Libra, Capricorn, Aquarius


def _functional_benefics(lagna_sign: int) -> set:
    return _FB_A if lagna_sign in _FB_A_SIGNS else _FB_B


def _house_from(reference: int, n: int) -> int:
    """The house that is ``n``-th (1-indexed) from ``reference`` (whole-sign)."""
    return ((reference - 1 + n - 1) % 12) + 1


def argala_analysis(chart: dict, functional: bool = False) -> dict:
    """Per-house argala table. Returns
    ``{"houses": [{house, strength, positive, negative, pos_weight, neg_weight}],
       "moon_bright": bool, "shadbala_used": bool, "functional": bool}``.

    ``functional=False`` (default) classifies interveners by NATURAL benefic/
    malefic nature (Jup/Ven/Mer + bright-fortnight Moon). ``functional=True``
    uses the lagna-specific functional-benefic scheme (paksha-independent).
    """
    P = chart["planets"]
    paksha = (chart.get("panchanga") or {}).get("paksha", "")
    moon_bright = paksha == "Shukla"

    if functional:
        fb = _functional_benefics((chart.get("lagna") or {}).get("sign", 0))

        def is_benefic(planet: str) -> bool:
            return planet in fb
    else:
        def is_benefic(planet: str) -> bool:
            if planet == "Moon":
                return moon_bright
            return planet in _NATURAL_BENEFIC

    # Shadbala weight per planet. Fall back to the classical average (or 1.0)
    # for any body without a Shadbala entry (Rahu/Ketu, or a cheap chart).
    sb = chart.get("shadbala") or {}
    classical = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    svals = [sb[q]["total_shadbala"] for q in classical if q in sb]
    avg = sum(svals) / len(svals) if svals else 1.0
    wt = {q: (sb[q]["total_shadbala"] if q in sb else avg) for q in _ARG_PLANETS}

    by_house: dict[int, list[str]] = {h: [] for h in range(1, 13)}
    for p in _ARG_PLANETS:
        by_house[P[p]["house"]].append(p)

    houses = []
    for reference in range(1, 13):
        pos = neg = 0.0
        positive: list[str] = []
        negative: list[str] = []
        for na, nv in _ARG_PAIRS:
            argala_house = _house_from(reference, na)
            virodha_house = _house_from(reference, nv)
            argala_wt = sum(wt[p] for p in by_house[argala_house])
            virodha_wt = sum(wt[p] for p in by_house[virodha_house])
            # An argala counts only if it outweighs its virodha counter.
            if argala_wt > virodha_wt:
                for p in by_house[argala_house]:
                    if is_benefic(p):
                        pos += wt[p]
                        positive.append(p)
                    else:
                        neg += wt[p]
                        negative.append(p)
        denom = pos + neg
        strength = round((pos - neg) / denom * 100, 1) if denom > 0 else 0.0
        houses.append({
            "house": reference,
            "strength": strength,           # −100..+100; sign drives the colour
            "positive": positive,           # benefic effective interveners
            "negative": negative,           # malefic effective interveners
            "pos_weight": round(pos, 3),
            "neg_weight": round(neg, 3),
        })

    return {
        "houses": houses,
        "moon_bright": moon_bright,
        "shadbala_used": bool(sb),
        "functional": functional,
    }
