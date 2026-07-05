"""Degree-position calculator — per-body Pushkara/Vish Navāṁśa + Pushkara/Mṛtyu
Bhāga for a birth chart. Powers ``GET /api/kundli/degree-analysis`` (+ /page).

Four classical degree categories, two auspicious and two poison:

  * **Pushkara Navāṁśa** (auspicious) — two nourishing 3°20′ navamsas per sign (by element).
  * **Pushkara Bhāga** (auspicious) — one auspicious degree per sign (±1° window).
  * **Vish Navāṁśa** (poison) — the one poison navamsa per sign.
  * **Mṛtyu Bhāga** (poison) — the fatal degree per body per sign (±1° window).

The two poison tables are reused from ``poison_degrees`` (factor 18 of the fame
model). The two Pushkara tables are display-only here (they were tested for the
fame model and are noise, ~0.50-0.53 AUC, but remain classically meaningful for a
chart reading).

Covers the 9 grahas + the three outer planets (Uranus/Neptune/Pluto) + the
Ascendant. Mṛtyu Bhāga has no classical table for the outer planets, so it is
reported as ``None`` for them.
"""
from __future__ import annotations

from app.services.kundli_calculator._core import SIGN_NAMES
from app.services.kundli_calculator.poison_degrees import (
    _MRITYU_BHAGA,
    _MRITYU_TOL,
    _NAV,
    _VISH_NAV,
)

# Pushkara Navāṁśa (auspicious) — two navamsa numbers per 0-indexed sign, by element.
_PUSHKARA_NAV: dict[int, set] = {}
for _s in (0, 4, 8):    _PUSHKARA_NAV[_s] = {7, 9}   # Fire
for _s in (1, 5, 9):    _PUSHKARA_NAV[_s] = {3, 5}   # Earth
for _s in (2, 6, 10):   _PUSHKARA_NAV[_s] = {6, 8}   # Air
for _s in (3, 7, 11):   _PUSHKARA_NAV[_s] = {1, 3}   # Water

# Pushkara Bhāga (auspicious) — one degree per 0-indexed sign; ±tol counts.
_PUSHKARA_BHAGA = {0: 21, 1: 14, 2: 18, 3: 8, 4: 19, 5: 9, 6: 24, 7: 11, 8: 23, 9: 14, 10: 19, 11: 9}
_PBHAGA_TOL = 1.0

_ORDER = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn",
          "Rahu", "Ketu", "Uranus", "Neptune", "Pluto"]


def _analyze_body(name: str, sign: int, deg: float, mrityu_key: str) -> dict:
    nav = int(deg / _NAV) + 1
    mrityu = None
    if mrityu_key in _MRITYU_BHAGA:                       # None for the outer planets
        mrityu = abs(deg - _MRITYU_BHAGA[mrityu_key][sign]) <= _MRITYU_TOL
    return {
        "body": name,
        "sign": SIGN_NAMES[sign],
        "degree": round(deg, 2),
        "navamsa": nav,
        "pushkara_navamsa": nav in _PUSHKARA_NAV[sign],
        "pushkara_bhaga": abs(deg - _PUSHKARA_BHAGA[sign]) <= _PBHAGA_TOL,
        "vish_navamsa": nav == _VISH_NAV[sign],
        "mrityu_bhaga": mrityu,
    }


def degree_analysis(chart: dict) -> dict:
    """Per-body Pushkara/Vish Navāṁśa + Pushkara/Mṛtyu Bhāga for the 12 planets +
    the Ascendant, plus category totals. Mṛtyu Bhāga is ``None`` for the outer
    planets (no classical table)."""
    P, lag = chart["planets"], chart["lagna"]
    rows = [_analyze_body(b, P[b]["sign"], P[b]["degree_in_sign"], b) for b in _ORDER if b in P]
    rows.append(_analyze_body("Ascendant", lag["sign"], lag.get("degree", 0.0), "Lagna"))
    totals = {
        key: sum(1 for r in rows if r[key])
        for key in ("pushkara_navamsa", "pushkara_bhaga", "vish_navamsa", "mrityu_bhaga")
    }
    return {"bodies": rows, "totals": totals}
