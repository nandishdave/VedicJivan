"""Vimśopaka Bala calculator — per-planet cross-divisional strength (0-20).

Vimśopaka bala grades a planet's dignity across the sixteen Shodashavarga
divisional charts, weighted so the karma varga (D60), the rāśi (D1) and the
navāṁśa (D9) dominate (the weights sum to 20). It is the classical answer to
"does the planet's strength *hold up* across the vargas?" — a single strong
placement in the D1 that collapses in the D9/D10 is flash, not depth.

This module is the standalone calculator behind ``GET /api/kundli/vimsopaka``.
It shares its weights and dignity scale with factor 2 of ``worldly_potential``
(that factor is simply the mean of the seven values this returns).
"""

from __future__ import annotations

from app.services.kundli_calculator._core import (
    SIGN_NAMES,
    _get_dignity,
    calc_planet_positions,
    get_julian_day,
)
# Shared weights + dignity scale — one source of truth (dignity.py). Re-exported
# here so existing `from ...vimsopaka import VARGA_WEIGHTS/DIGNITY_PCT` still work.
from app.services.kundli_calculator.dignity import (  # noqa: F401  (re-export)
    DIGNITY_PCT,
    VARGA_WEIGHTS,
)
from app.services.kundli_calculator.divisional import calc_divisional_charts

# The seven classical grahas — the strength framework (Shadbala/Vimśopaka) is planet-
# centric, so the average and the strongest-planet pick use these seven only.
_CLASSICAL = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
# Rāhu/Ketu are shown for reference using the Parāśara node-dignity scheme (Rāhu exalted
# Gemini / own Aquarius, Ketu exalted Sagittarius / own Scorpio). They are NOT part of
# classical 7-graha Vimśopaka and NOT part of the fame model — including them was tested
# and does not help (it dilutes factor 2 and is neutral-to-reversed for factor 16).
_NODES = ["Rahu", "Ketu"]

_DEFAULT_PCT = 45  # unknown dignity → neutral


def _band(v: float) -> str:
    """Interpretation band for a single planet's Vimśopaka (0-20)."""
    if v >= 15.0:
        return "Very strong"
    if v >= 10.0:
        return "Moderately strong"
    if v >= 5.0:
        return "Weak"
    return "Very weak"


def planet_vimsopaka(planet: str, planets: dict, divisional: dict) -> dict:
    """Vimśopaka bala of one planet with its per-varga breakdown."""
    total = 0.0
    vargas = []
    for vname, weight in VARGA_WEIGHTS.items():
        sign = planets[planet]["sign"] if vname == "D1" else divisional[vname][planet]
        dignity = _get_dignity(planet, sign)
        pct = DIGNITY_PCT.get(dignity, _DEFAULT_PCT)
        contribution = weight * pct / 100.0
        total += contribution
        vargas.append({
            "varga": vname,
            "sign": SIGN_NAMES[sign],
            "dignity": dignity,
            "weight": weight,
            "contribution": round(contribution, 3),
        })
    return {
        "vimsopaka": round(total, 2),
        "max": 20.0,
        "band": _band(total),
        "vargas": vargas,
    }


def compute_vimsopaka(dob: str, tob: str, lat: float, lon: float) -> dict:
    """Full per-planet Vimśopaka report for a birth moment.

    Returns ``{"lagna", "planets": {name: {vimsopaka, band, vargas}}, "strongest",
    "average"}``. ``strongest`` is the planet with the highest Vimśopaka and the
    house it occupies (the basis of factor 16 in the worldly-potential model).
    """
    jd = get_julian_day(dob, tob, lat, lon)
    pos = calc_planet_positions(jd, lat, lon)
    planets, lagna = pos["planets"], pos["lagna"]
    divisional = calc_divisional_charts(planets, lagna)

    # Nodes computed for display only; average + strongest use the 7 classical grahas.
    per_planet = {p: planet_vimsopaka(p, planets, divisional) for p in _CLASSICAL + _NODES}
    strongest = max(_CLASSICAL, key=lambda p: per_planet[p]["vimsopaka"])
    avg = sum(per_planet[p]["vimsopaka"] for p in _CLASSICAL) / len(_CLASSICAL)

    return {
        "lagna": SIGN_NAMES[lagna["sign"]],
        "planets": {
            p: {
                "vimsopaka": per_planet[p]["vimsopaka"],
                "band": per_planet[p]["band"],
                "house": planets[p]["house"],
                "sign": SIGN_NAMES[planets[p]["sign"]],
                "is_node": p in _NODES,  # display-only; excluded from average + strongest
                "vargas": per_planet[p]["vargas"],
            }
            for p in _CLASSICAL + _NODES
        },
        "strongest": {
            "planet": strongest,
            "vimsopaka": per_planet[strongest]["vimsopaka"],
            "house": planets[strongest]["house"],
            # prominence seat = factor 16 of the worldly-potential model
            "in_prominence_seat": planets[strongest]["house"] in (1, 2, 4, 5, 11),
        },
        "average": round(avg, 2),
    }
