"""Argala (Jaimini "intervention/bolt") per-house analysis for the calculator.

For each of the 12 houses this reports a SIGNED quality score — not just the
benefic/malefic nature of the interveners, but whether the intervention
actually helps that house — plus a per-planet breakdown.

Geometry (shared with worldly_potential factor 13): planets in the 2nd/4th/5th/
11th from a house give it argala; an argala counts only if its house outweighs
its Virodha counter (12th/10th/9th/3rd). Restricted to the fame houses in the
fame model; here we sweep all 12.

Quality of each planet G's effective argala on house H (sign S) — a signed
polarity × the giver's Shadbala magnitude:

  (1) Dignity toward the house it locks — dignity(G, S):
        Exalted +2 · Own/Moolatrikona +1.5 · Friend +1 · Neutral 0 ·
        Debilitated -2 · Enemy: +0.5 if G is a functional benefic else -1.
  (2) Role-fit — natural nature × the house type of H:
        natural benefic on kendra/trikona/2/11 +1, on 8/12 neutral (0);
        natural malefic on upachaya (3/6/10/11) +1, on 8/12 -1.
  polarity = (1) + (2);  contribution = Shadbala(G) × polarity.

House strength % = Shadbala-and-polarity-weighted tilt of all contributions.
"""

from __future__ import annotations

from app.services.kundli_calculator._core import SIGN_NAMES, _get_dignity

# All nine grahas can throw argala.
_ARG_PLANETS = [
    "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu",
]
# (argala house Nth-from-reference, its virodha/counter house Nth-from-reference).
_ARG_PAIRS = ((2, 12), (4, 10), (5, 9), (11, 3))

_NATURAL_BENEFIC = {"Jupiter", "Venus", "Mercury"}
# Functional (lagna-specific) benefics — the two-group scheme the fame model uses.
_FB_A = {"Saturn", "Venus", "Mercury"}
_FB_B = {"Sun", "Moon", "Mars", "Jupiter"}
_FB_A_SIGNS = {1, 2, 5, 6, 9, 10}  # Ta, Ge, Vi, Li, Cp, Aq

# House-type groups (house numbers 1..12 from the lagna).
_KENDRA = {1, 4, 7, 10}
_TRIKONA = {1, 5, 9}
_UPACHAYA = {3, 6, 10, 11}
_DUSTHANA = {8, 12}
_GOOD_FOR_BENEFIC = _KENDRA | _TRIKONA | {2, 11}

_DIGNITY_SCORE = {
    "Exalted": 2.0,
    "Moolatrikona": 1.5,
    "Own Sign": 1.5,
    "Friendly Sign": 1.0,
    "Neutral Sign": 0.0,
    "Enemy Sign": -1.0,   # overridden by functional nature below
    "Debilitated": -2.0,
}


def _functional_benefics(lagna_sign: int) -> set:
    return _FB_A if lagna_sign in _FB_A_SIGNS else _FB_B


def _house_from(reference: int, n: int) -> int:
    return ((reference - 1 + n - 1) % 12) + 1


def argala_analysis(chart: dict) -> dict:
    """Per-house argala quality table with a per-planet breakdown. Returns
    ``{"houses": [{house, strength, positive, negative, pos_weight, neg_weight,
    interveners:[...]}], "shadbala_used": bool, "lagna_sign": int}``."""
    P = chart["planets"]
    lagna_sign = (chart.get("lagna") or {}).get("sign", 0)
    paksha = (chart.get("panchanga") or {}).get("paksha", "")
    moon_benefic = paksha == "Shukla"
    fb = _functional_benefics(lagna_sign)

    def is_natural_benefic(planet: str) -> bool:
        if planet == "Moon":
            return moon_benefic
        return planet in _NATURAL_BENEFIC

    def role_fit(planet: str, house: int) -> float:
        if is_natural_benefic(planet):
            if house in _GOOD_FOR_BENEFIC:
                return 1.0
            return 0.0  # incl. neutral on 8/12 (layer 9)
        # natural malefic
        if house in _UPACHAYA:
            return 1.0
        if house in _DUSTHANA:
            return -1.0
        return 0.0

    def dignity_score(planet: str, dignity: str) -> float:
        if dignity == "Enemy Sign":
            return 0.5 if planet in fb else -1.0
        return _DIGNITY_SCORE.get(dignity, 0.0)

    # Shadbala magnitude (fallback to the classical average / 1.0 when absent).
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
        ref_sign = (lagna_sign + reference - 1) % 12
        interveners = []
        for na, nv in _ARG_PAIRS:
            argala_house = _house_from(reference, na)
            virodha_house = _house_from(reference, nv)
            argala_wt = sum(wt[p] for p in by_house[argala_house])
            virodha_wt = sum(wt[p] for p in by_house[virodha_house])
            if argala_wt <= virodha_wt:
                continue  # obstructed by its virodha
            for p in by_house[argala_house]:
                dig = _get_dignity(p, ref_sign)
                d = dignity_score(p, dig)
                r = role_fit(p, reference)
                polarity = d + r
                interveners.append({
                    "planet": p,
                    "from_house": na,           # sits in the 2/4/5/11 from here
                    "sign": SIGN_NAMES[ref_sign],
                    "dignity": dig,
                    "dignity_score": round(d, 2),
                    "role_fit": round(r, 2),
                    "shadbala": round(wt[p], 3),
                    "polarity": round(polarity, 2),
                    "contribution": round(wt[p] * polarity, 3),
                })

        pos = sum(iv["contribution"] for iv in interveners if iv["polarity"] > 0)
        neg = sum(-iv["contribution"] for iv in interveners if iv["polarity"] < 0)
        denom = pos + neg
        strength = round((pos - neg) / denom * 100, 1) if denom > 0 else 0.0
        houses.append({
            "house": reference,
            "strength": strength,
            "positive": [iv["planet"] for iv in interveners if iv["polarity"] > 0],
            "negative": [iv["planet"] for iv in interveners if iv["polarity"] < 0],
            "pos_weight": round(pos, 3),
            "neg_weight": round(neg, 3),
            "interveners": interveners,
        })

    return {"houses": houses, "shadbala_used": bool(sb), "lagna_sign": lagna_sign}
