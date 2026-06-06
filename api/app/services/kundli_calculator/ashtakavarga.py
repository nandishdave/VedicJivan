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
