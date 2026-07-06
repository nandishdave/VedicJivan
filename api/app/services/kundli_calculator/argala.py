"""Argala (Jaimini "intervention/bolt") per-house analysis for the calculator.

For each of the 12 houses this reports a SIGNED quality score — whether the
net intervention helps that house — plus a per-pair breakdown of the argala
vs its Virodha (counter).

Geometry (shared with worldly_potential factor 13): planets in the 2nd/4th/5th/
11th from a house give it argala; each is countered by its Virodha (12th/10th/
9th/3rd). Rather than dropping an obstructed argala, we keep BOTH sides and let
the counter reduce the argala's magnitude:

  survive = clamp((argala_shadbala - virodha_shadbala) / argala_shadbala, 0, 1)

so an unopposed argala survives fully, and one matched/beaten by its counter
survives at 0 (obstructed -> neutral, still shown).

Quality of each surviving argala (planet G on house H, sign S) — a signed
polarity, magnitude = Shadbala × survive:
  (1) Dignity toward the house — dignity(G, S): Exalted +2 · Own/Moola +1.5 ·
      Friend +1 · Neutral 0 · Debilitated -2 · Enemy +0.5 if G a functional
      benefic else -1.
  (2) Role-fit — natural nature × house type: natural benefic on
      kendra/trikona/2/11 +1, on 8/12 neutral; natural malefic on upachaya
      (3/6/10/11) +1, on 8/12 -1.
  polarity = (1) + (2);  contribution = Shadbala(G) × polarity × survive.

Verdict per house: null (nothing intervenes) · neutral (all obstructed / net
zero) · positive · negative.
"""

from __future__ import annotations

from app.services.kundli_calculator._core import SIGN_NAMES, _get_dignity

_ARG_PLANETS = [
    "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu",
]
# (argala house Nth-from-reference, its virodha/counter house Nth-from-reference).
_ARG_PAIRS = ((2, 12), (4, 10), (5, 9), (11, 3))

_NATURAL_BENEFIC = {"Jupiter", "Venus", "Mercury"}
_FB_A = {"Saturn", "Venus", "Mercury"}
_FB_B = {"Sun", "Moon", "Mars", "Jupiter"}
_FB_A_SIGNS = {1, 2, 5, 6, 9, 10}  # Ta, Ge, Vi, Li, Cp, Aq

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
    "Enemy Sign": -1.0,
    "Debilitated": -2.0,
}


def _functional_benefics(lagna_sign: int) -> set:
    return _FB_A if lagna_sign in _FB_A_SIGNS else _FB_B


def _house_from(reference: int, n: int) -> int:
    return ((reference - 1 + n - 1) % 12) + 1


def argala_analysis(chart: dict) -> dict:
    """Per-house argala quality with an argala-vs-virodha pair breakdown."""
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
            return 1.0 if house in _GOOD_FOR_BENEFIC else 0.0
        if house in _UPACHAYA:
            return 1.0
        if house in _DUSTHANA:
            return -1.0
        return 0.0

    def dignity_score(planet: str, dignity: str) -> float:
        if dignity == "Enemy Sign":
            return 0.5 if planet in fb else -1.0
        return _DIGNITY_SCORE.get(dignity, 0.0)

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
        pairs = []
        pos = neg = 0.0
        positive: list[str] = []
        negative: list[str] = []
        has_argala = False

        for na, nv in _ARG_PAIRS:
            argala_house = _house_from(reference, na)
            virodha_house = _house_from(reference, nv)
            arg_planets = by_house[argala_house]
            vir_planets = by_house[virodha_house]
            if not arg_planets and not vir_planets:
                continue  # empty pair — nothing to show
            if arg_planets:
                has_argala = True

            arg_sb = sum(wt[p] for p in arg_planets)
            vir_sb = sum(wt[p] for p in vir_planets)
            survive = 0.0 if arg_sb <= 0 else max(0.0, min(1.0, (arg_sb - vir_sb) / arg_sb))

            argala_rows = []
            for p in arg_planets:
                dig = _get_dignity(p, ref_sign)
                d = dignity_score(p, dig)
                r = role_fit(p, reference)
                polarity = d + r
                contribution = wt[p] * polarity * survive
                argala_rows.append({
                    "planet": p,
                    "from_house": na,
                    "sign": SIGN_NAMES[ref_sign],
                    "dignity": dig,
                    "dignity_score": round(d, 2),
                    "role_fit": round(r, 2),
                    "shadbala": round(wt[p], 3),
                    "polarity": round(polarity, 2),
                    "contribution": round(contribution, 3),
                })
                if contribution > 0:
                    pos += contribution
                    positive.append(p)
                elif contribution < 0:
                    neg += -contribution
                    negative.append(p)

            pairs.append({
                "argala_from": na,
                "virodha_from": nv,
                "argala_shadbala": round(arg_sb, 3),
                "virodha_shadbala": round(vir_sb, 3),
                "survive": round(survive, 3),
                "argala": argala_rows,
                "virodha": [{"planet": p, "shadbala": round(wt[p], 3)} for p in vir_planets],
            })

        denom = pos + neg
        strength = round((pos - neg) / denom * 100, 1) if denom > 0 else 0.0
        if not has_argala:
            verdict = "null"
        elif strength > 0:
            verdict = "positive"
        elif strength < 0:
            verdict = "negative"
        else:
            verdict = "neutral"

        houses.append({
            "house": reference,
            "strength": strength,
            "verdict": verdict,
            "positive": positive,
            "negative": negative,
            "pos_weight": round(pos, 3),
            "neg_weight": round(neg, 3),
            "pairs": pairs,
        })

    return {"houses": houses, "shadbala_used": bool(sb), "lagna_sign": lagna_sign}
