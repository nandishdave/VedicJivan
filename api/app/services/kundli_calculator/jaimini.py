"""Jaimini System — Chara Karakas + Karakamsa.

Computes the 7 classical planets ranked by degree-within-sign (highest
= Atmakaraka), producing the Chara Karaka roles Atma/Amatya/Bhratru/
Matrua/Putra/Gnati/Dara. Also computes the Karakamsa (AK's D9 sign) —
used as the lagna of the Jaimini-derived dharma chart.
"""

from __future__ import annotations

from ._core import SIGN_NAMES
from .divisional import _calc_varga_sign


# Sthira (fixed) Karakas — classical assignment, used as a reference baseline
# alongside the chart-specific Chara Karakas.
JAIMINI_STHIRA_KARAKAS = {
    "Atma":    "Sun",
    "Amatya":  "Mercury",
    "Bhratru": "Mars",
    "Matrua":  "Moon",
    "Putra":   "Jupiter",
    "Gnati":   "Saturn",
    "Dara":    "Venus",
}

# Chara Karaka role names in descending-degree order (highest = AK).
JAIMINI_CHARA_ROLES = ["Atma", "Amatya", "Bhratru", "Matrua", "Putra", "Gnati", "Dara"]


def calc_jaimini_karakas(planets: dict, lagna: dict) -> dict:
    """Compute Jaimini Chara Karakas and the Karakamsa (D9 sign of Atmakaraka).

    Chara (movable) Karakas: 7 classical planets ranked by their degree-within-
    sign in DESCENDING order. The highest-degree planet is the Atmakaraka (AK,
    soul indicator), followed by Amatyakaraka, Bhratrukaraka, Matrukaraka,
    Putrakaraka, Gnatikaraka and Darakaraka.

    Karakamsa = the navamsa (D9) sign occupied by the Atmakaraka. In Jaimini,
    this sign is treated as the lagna of a derived chart used for soul-purpose
    and dharma readings.
    """
    classical = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    ranked = sorted(
        ((p, planets[p]["degree_in_sign"]) for p in classical if p in planets),
        key=lambda kv: kv[1],
        reverse=True,
    )
    chara = {}
    for role, (planet_name, deg) in zip(JAIMINI_CHARA_ROLES, ranked):
        chara[role] = {"planet": planet_name, "degree": round(deg, 2)}

    # Karakamsa = AK's navamsa sign. Re-use the divisional varga formula to
    # compute that, independent of whether the divisional bundle is around.
    ak_planet = chara["Atma"]["planet"]
    ak_sign = planets[ak_planet]["sign"]
    ak_degree = planets[ak_planet]["degree_in_sign"]
    karakamsa_sign = _calc_varga_sign(ak_sign, ak_degree, "D9")

    # Both Karakamsa and Swamsa charts use the SAME lagna — the navamsa sign
    # occupied by the Atmakaraka. The difference is which base chart's planet
    # placements are shown:
    #   - Karakamsa Chart = the D1 (Rasi) chart rotated so AK's D9 sign = 1st
    #   - Swamsa Chart    = the D9 (Navamsa) chart rotated so AK's D9 sign = 1st
    swamsa_sign = karakamsa_sign

    return {
        "chara": chara,
        "sthira": dict(JAIMINI_STHIRA_KARAKAS),
        "atmakaraka": ak_planet,
        "karakamsa_sign": karakamsa_sign,
        "karakamsa_sign_name": SIGN_NAMES[karakamsa_sign],
        "swamsa_sign": swamsa_sign,
        "swamsa_sign_name": SIGN_NAMES[swamsa_sign],
    }
