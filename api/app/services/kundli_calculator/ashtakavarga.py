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


ASHTAKAVARGA_RULES: dict[str, list[set[int]]] = {
    "Sun":     [{1,2,4,7,8,9,10,11}, {3,6,10,11}, {1,2,4,7,8,9,10,11}, {3,5,6,9,10,11,12}, {5,6,9,11}, {6,7,12}, {1,2,4,7,8,9,10,11}, {3,4,6,10,11,12}],
    "Moon":    [{3,6,7,8,10,11}, {1,3,6,7,10,11}, {2,3,5,6,9,10,11}, {1,3,4,5,7,8,10,11}, {1,4,7,8,10,11,12}, {3,4,5,7,9,10,11}, {3,5,6,11}, {3,6,10,11}],
    "Mars":    [{3,5,6,10,11}, {3,6,11}, {1,2,4,7,8,10,11}, {3,5,6,11}, {6,10,11,12}, {6,8,11,12}, {1,4,7,8,9,10,11}, {1,3,6,10,11}],
    "Mercury": [{5,6,9,11,12}, {2,4,6,8,10,11}, {1,2,4,7,8,9,10,11}, {1,3,5,6,9,10,11,12}, {6,8,11,12}, {1,2,3,4,5,8,9,11}, {1,2,4,7,8,9,10,11}, {1,2,4,6,8,10,11}],
    "Jupiter": [{1,2,3,4,7,8,9,10,11}, {2,5,7,9,11}, {1,2,4,7,8,10,11}, {1,2,4,5,6,9,10,11}, {1,2,3,4,7,8,10,11}, {2,5,6,9,10,11}, {3,5,6,12}, {1,2,4,5,6,7,9,10,11}],
    "Venus":   [{8,11,12}, {1,2,3,4,5,8,9,11,12}, {3,5,6,9,11,12}, {3,5,6,9,11}, {5,8,9,10,11}, {1,2,3,4,5,8,9,10,11}, {3,4,5,8,9,10,11}, {1,2,3,4,5,8,9,11}],
    "Saturn":  [{1,2,4,7,8,10,11}, {3,6,11}, {3,5,6,10,11,12}, {6,8,9,10,11,12}, {5,6,11,12}, {6,11,12}, {3,5,6,11}, {1,3,4,6,10,11}],
}


def calc_ashtakavarga(planets: dict, lagna_sign: int) -> dict:
    """Return Bhinnashtakavarga (per-planet bindus per sign) and Sarvashtakavarga totals.

    Output shape:
      {
        "bindus":     {planet: [b_sign1, b_sign2, ..., b_sign12]},  # 7 planets
        "totals":     [t_sign1, ..., t_sign12],                     # Sarvashtakavarga
        "grand_total": int,                                         # should be 337
      }
    """
    planet_order = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    contrib_signs = [planets[name]["sign"] for name in planet_order] + [lagna_sign]

    bindus: dict[str, list[int]] = {}
    totals = [0] * 12
    for planet, rules in ASHTAKAVARGA_RULES.items():
        row = [0] * 12
        for contrib_sign, benefic_houses in zip(contrib_signs, rules):
            for target_sign in range(12):
                house_from_contrib = ((target_sign - contrib_sign) % 12) + 1
                if house_from_contrib in benefic_houses:
                    row[target_sign] += 1
        bindus[planet] = row
        for i in range(12):
            totals[i] += row[i]

    return {"bindus": bindus, "totals": totals, "grand_total": sum(totals)}
