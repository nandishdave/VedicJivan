"""Planetary aspects — Vedic graha drishti + Western angular aspects.

Self-contained: pure dict / list arithmetic, no swisseph or DB.
"""

from __future__ import annotations


# ── Vedic Graha Drishti (classical planetary aspects) ──────────────────────
# Every planet has a full (100%) aspect on the 7th house from itself.
# Mars, Jupiter, Saturn, Rahu and Ketu have additional special aspects.
#
# Offsets are (n-1) because Vedic counting is inclusive: "7th from H1" = H7,
# so offset = 6.  Formula: target = ((house - 1 + offset) % 12) + 1.
_SPECIAL_ASPECT_OFFSETS = {
    "Mars":    [3, 7],      # 4th and 8th from self
    "Jupiter": [4, 8],      # 5th and 9th from self
    "Saturn":  [2, 9],      # 3rd and 10th from self
    "Rahu":    [4, 8],      # Jupiter-like (Parashari tradition)
    "Ketu":    [4, 8],      # Jupiter-like (Parashari tradition)
}


def calc_graha_drishti(planets: dict, lagna: dict) -> dict:
    """Compute Vedic graha drishti (planetary aspects) for the birth chart.

    Returns two views:
      planet_aspects : {planet_name: [list of house numbers 1-12 the planet aspects]}
      house_aspected_by : {house_num: [list of planet names aspecting that house]}
    """
    planet_aspects: dict[str, list[int]] = {}
    house_aspected_by: dict[str, list[str]] = {str(h): [] for h in range(1, 13)}

    for name, info in planets.items():
        planet_house = info.get("house")
        if planet_house is None:
            continue

        aspected_offsets = [6]  # 7th from self
        if name in _SPECIAL_ASPECT_OFFSETS:
            aspected_offsets.extend(_SPECIAL_ASPECT_OFFSETS[name])

        resolved = []
        for offset in aspected_offsets:
            target = ((planet_house - 1 + offset) % 12) + 1
            resolved.append(target)
            house_aspected_by[str(target)].append(name)

        planet_aspects[name] = sorted(resolved)

    return {
        "planet_aspects": planet_aspects,
        "house_aspected_by": house_aspected_by,
    }


# ── Western Planetary Aspects ───────────────────────────────────────────────
# Angular relationships between planets using Western (Ptolemaic + minor) aspects.
# Each aspect is defined by its exact angle and a maximum orb tolerance.

WESTERN_ASPECTS = [
    {"name": "Conjunction", "abbr": "CONJ", "angle": 0,   "orb": 15, "weight": 10},
    {"name": "Opposition",  "abbr": "OPPN", "angle": 180, "orb": 15, "weight": 10},
    {"name": "Trine",       "abbr": "TRIN", "angle": 120, "orb": 6,  "weight": 3},
    {"name": "Square",      "abbr": "SQUR", "angle": 90,  "orb": 6,  "weight": 3},
    {"name": "Sextile",     "abbr": "SEXT", "angle": 60,  "orb": 6,  "weight": 3},
    {"name": "Nonile",      "abbr": "NONL", "angle": 40,  "orb": 1,  "weight": 1},
    {"name": "Quintile",    "abbr": "QUIN", "angle": 72,  "orb": 1,  "weight": 1},
    {"name": "Semi-Square", "abbr": "SSQU", "angle": 45,  "orb": 1,  "weight": 1},
    {"name": "Sesquiquadrate", "abbr": "SQQD", "angle": 135, "orb": 1, "weight": 1},
    {"name": "Quincunx",    "abbr": "QCUN", "angle": 150, "orb": 1,  "weight": 1},
]

_ALL_ASPECT_PLANETS = [
    "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn",
    "Rahu", "Ketu", "Uranus", "Neptune", "Pluto",
]


def best_western_aspect(lon_a: float, lon_b: float) -> dict | None:
    """Tightest Western aspect between two longitudes, or None if none within orb.

    Folds the separation to 0–180° and returns the closest-orb match from
    ``WESTERN_ASPECTS`` as ``{"abbr", "orb", "weight"}``. Shared by the
    planet-planet matrix here and the KP cusp-aspect grid in ``kp.py``.
    """
    diff = abs(lon_a - lon_b) % 360
    if diff > 180:
        diff = 360 - diff
    best = None
    for asp in WESTERN_ASPECTS:
        orb = abs(diff - asp["angle"])
        if orb <= asp["orb"] and (best is None or orb < best["orb"]):
            best = {"abbr": asp["abbr"], "orb": round(orb, 2), "weight": asp["weight"]}
    return best


def calc_western_aspects(planets: dict) -> dict:
    """Compute Western-style angular aspects between all planet pairs.

    Returns a dict with:
      planets : ordered list of planet names included (only those present in chart).
      matrix  : dict-of-dicts keyed by (from, to) with value:
                  {"abbr": "CONJ", "orb": 1.23} or None if no aspect within orb.
    """
    active = [p for p in _ALL_ASPECT_PLANETS if p in planets]
    matrix: dict[str, dict[str, dict | None]] = {}

    for p in active:
        matrix[p] = {}
        p_lon = planets[p]["longitude"]
        for q in active:
            if q == p:
                matrix[p][q] = None
                continue
            q_lon = planets[q]["longitude"]
            matrix[p][q] = best_western_aspect(p_lon, q_lon)

    return {"planets": active, "matrix": matrix}
