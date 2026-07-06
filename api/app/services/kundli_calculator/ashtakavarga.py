"""Ashtakavarga — Bhinna + Sarva benefic-points distribution.

Classical Parashara rules. For each of the 7 planets, lists — for each
of 8 contributors (Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn,
Lagna) — the house positions *from the contributor* that grant one
bindu (benefic point) to the planet.

Each planet's expected total across the 12 signs:
  Sun=48, Moon=49, Mars=39, Mercury=54, Jupiter=56, Venus=52, Saturn=39
  → grand total 337.
"""

from __future__ import annotations


# Classical per-planet bindu totals across all 12 signs (Parashara). These are
# fixed invariants: each planet's own Bhinnashtakavarga always sums to exactly
# this, and the seven sum to 337 (Sarvashtakavarga). Used as a runtime guard so
# any future edit to ASHTAKAVARGA_RULES that breaks a total fails loudly instead
# of silently shipping wrong numbers that wouldn't match Astrosage/classical.
EXPECTED_PLANET_TOTALS: dict[str, int] = {
    "Sun": 48, "Moon": 49, "Mars": 39, "Mercury": 54,
    "Jupiter": 56, "Venus": 52, "Saturn": 39,
}
EXPECTED_GRAND_TOTAL = 337  # sum(EXPECTED_PLANET_TOTALS) — Sarvashtakavarga


ASHTAKAVARGA_RULES: dict[str, list[set[int]]] = {
    "Sun":     [{1,2,4,7,8,9,10,11}, {3,6,10,11}, {1,2,4,7,8,9,10,11}, {3,5,6,9,10,11,12}, {5,6,9,11}, {6,7,12}, {1,2,4,7,8,9,10,11}, {3,4,6,10,11,12}],
    "Moon":    [{3,6,7,8,10,11}, {1,3,6,7,10,11}, {2,3,5,6,9,10,11}, {1,3,4,5,7,8,10,11}, {1,4,7,8,10,11,12}, {3,4,5,7,9,10,11}, {3,5,6,11}, {3,6,10,11}],
    "Mars":    [{3,5,6,10,11}, {3,6,11}, {1,2,4,7,8,10,11}, {3,5,6,11}, {6,10,11,12}, {6,8,11,12}, {1,4,7,8,9,10,11}, {1,3,6,10,11}],
    "Mercury": [{5,6,9,11,12}, {2,4,6,8,10,11}, {1,2,4,7,8,9,10,11}, {1,3,5,6,9,10,11,12}, {6,8,11,12}, {1,2,3,4,5,8,9,11}, {1,2,4,7,8,9,10,11}, {1,2,4,6,8,10,11}],
    "Jupiter": [{1,2,3,4,7,8,9,10,11}, {2,5,7,9,11}, {1,2,4,7,8,10,11}, {1,2,4,5,6,9,10,11}, {1,2,3,4,7,8,10,11}, {2,5,6,9,10,11}, {3,5,6,12}, {1,2,4,5,6,7,9,10,11}],
    "Venus":   [{8,11,12}, {1,2,3,4,5,8,9,11,12}, {3,5,6,9,11,12}, {3,5,6,9,11}, {5,8,9,10,11}, {1,2,3,4,5,8,9,10,11}, {3,4,5,8,9,10,11}, {1,2,3,4,5,8,9,11}],
    "Saturn":  [{1,2,4,7,8,10,11}, {3,6,11}, {3,5,6,10,11,12}, {6,8,9,10,11,12}, {5,6,11,12}, {6,11,12}, {3,5,6,11}, {1,3,4,6,10,11}],
}


# The 8 contributors, in classical order, that each grant bindus to a planet.
CONTRIBUTORS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Lagna"]


def calc_ashtakavarga(planets: dict, lagna_sign: int) -> dict:
    """Return Bhinnashtakavarga (per-planet bindus per sign), the per-contributor
    Prastharashtakavarga matrix, and Sarvashtakavarga totals.

    Output shape:
      {
        "bindus":     {planet: [b_sign1, ..., b_sign12]},   # 7 planets (column totals)
        "prasthar":   {planet: {contributor: [0/1 per sign]}},  # 7×8×12 detail
        "totals":     [t_sign1, ..., t_sign12],             # Sarvashtakavarga
        "grand_total": int,                                 # 337
      }

    `prasthar[planet][contributor][sign]` is 1 if that contributor grants a
    bindu to `planet` in that sign, else 0 — the detailed matrix Astrosage
    prints as its Prastharashtakavarga tables. `bindus[planet][sign]` is the
    column sum over the 8 contributors.
    """
    planet_order = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    contrib_signs = [planets[name]["sign"] for name in planet_order] + [lagna_sign]

    bindus: dict[str, list[int]] = {}
    prasthar: dict[str, dict[str, list[int]]] = {}
    totals = [0] * 12
    for planet, rules in ASHTAKAVARGA_RULES.items():
        row = [0] * 12
        prasthar[planet] = {}
        for contributor, contrib_sign, benefic_houses in zip(
            CONTRIBUTORS, contrib_signs, rules
        ):
            contrib_row = [0] * 12
            for target_sign in range(12):
                house_from_contrib = ((target_sign - contrib_sign) % 12) + 1
                if house_from_contrib in benefic_houses:
                    contrib_row[target_sign] = 1
                    row[target_sign] += 1
            prasthar[planet][contributor] = contrib_row
        bindus[planet] = row
        for i in range(12):
            totals[i] += row[i]
        # Per-planet invariant: this planet's bindus must sum to its fixed
        # classical total regardless of chart. A mismatch means the rules table
        # (or chart input) is corrupt — fail loudly rather than ship bad data.
        assert sum(row) == EXPECTED_PLANET_TOTALS[planet], (
            f"Ashtakavarga: {planet} bindus sum to {sum(row)}, "
            f"expected {EXPECTED_PLANET_TOTALS[planet]} (Parashara invariant)"
        )

    grand_total = sum(totals)
    assert grand_total == EXPECTED_GRAND_TOTAL, (
        f"Sarvashtakavarga grand total {grand_total} != {EXPECTED_GRAND_TOTAL}"
    )
    return {
        "bindus": bindus,
        "prasthar": prasthar,
        "totals": totals,
        "grand_total": grand_total,
    }


# ── Display transform for the calculator ────────────────────────────────────
# Local SIGN_NAMES so this stays a leaf module (_core imports calc_ashtakavarga,
# so importing SIGN_NAMES from _core here would be a cycle).
_SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]
_SIGN_ABBR = ["Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]
_AV_PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
# The 8 contributors (7 planets + Lagna) with the short labels the tables print.
_CONTRIB_ABBR = [
    ("Sun", "Su"), ("Moon", "Mo"), ("Mars", "Ma"), ("Mercury", "Me"),
    ("Jupiter", "Ju"), ("Venus", "Ve"), ("Saturn", "Sa"), ("Lagna", "As"),
]


def ashtakavarga_table(chart: dict) -> dict:
    """House-based Sarva + Bhinna Ashtakavarga for the calculator, from the
    chart's already-computed ``ashtakavarga`` block. The engine keys bindus by
    SIGN (Aries=0); here we re-key by HOUSE from the lagna so a reader sees
    which *house* each score lands on.

    Returns ``{lagna_sign, grand_total,
      houses: [{house, sign, sav}],                       # Sarvashtakavarga
      bav:    [{planet, total, per_house: [b1..b12]}]}``  # Bhinnashtakavarga
    """
    av = chart.get("ashtakavarga") or {}
    totals = av.get("totals") or [0] * 12
    bindus = av.get("bindus") or {}
    lagna_sign = (chart.get("lagna") or {}).get("sign", 0)

    def sign_of(house: int) -> int:
        return (lagna_sign + house - 1) % 12

    houses = [
        {"house": h, "sign": _SIGN_NAMES[sign_of(h)], "sav": totals[sign_of(h)]}
        for h in range(1, 13)
    ]
    bav = []
    for planet in _AV_PLANETS:
        row = bindus.get(planet, [0] * 12)
        bav.append({
            "planet": planet,
            "total": sum(row),
            "per_house": [row[sign_of(h)] for h in range(1, 13)],
        })

    # Prastharashtakavarga — the per-planet 8×12 audit matrix (by SIGN, the
    # classical layout): rows = the 8 contributors, columns = Aries…Pisces.
    prasthar_src = av.get("prasthar", {})
    prasthar = []
    for planet in _AV_PLANETS:
        pdata = prasthar_src.get(planet, {})
        rows = []
        col_totals = [0] * 12
        for contrib, abbr in _CONTRIB_ABBR:
            cells = pdata.get(contrib, [0] * 12)
            rows.append({"contributor": abbr, "cells": cells, "total": sum(cells)})
            col_totals = [col_totals[i] + cells[i] for i in range(12)]
        prasthar.append({"planet": planet, "rows": rows, "column_totals": col_totals})

    return {
        "lagna_sign": lagna_sign,
        "grand_total": av.get("grand_total", sum(totals)),
        "signs": _SIGN_ABBR,
        "houses": houses,
        "bav": bav,
        "prasthar": prasthar,
    }
