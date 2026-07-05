"""Shared planetary-dignity tables — used by Shadbala AND several
sibling modules (yogas, friendship, avasthas).

Lives in its own module so the back-import direction is sane: every
module that needs these constants imports from `.dignity` directly
instead of going through `._core` (which would create a back-import
chain once `shadbala.py` itself imports from `_core`).

Classical 7-planet Vedic conventions (BPHS / B.V. Raman). Extended
constants for Rahu/Ketu/outer planets live in `shadbala.py` where
the only consumer is.
"""

from __future__ import annotations


# Exaltation degrees (sidereal, 0–359°). Sign of exaltation = int(value / 30).
_EXALTATION = {"Sun": 10, "Moon": 33, "Mars": 298, "Mercury": 165, "Jupiter": 95, "Venus": 357, "Saturn": 200}

# Moolatrikona sign (0-indexed) for each classical planet.
_MOOLATRIKONA = {"Sun": 4, "Moon": 3, "Mars": 0, "Mercury": 5, "Jupiter": 8, "Venus": 6, "Saturn": 10}

# Own signs (0-indexed) for each classical planet.
_OWN_SIGNS = {
    "Sun": [4], "Moon": [3], "Mars": [0, 7], "Mercury": [2, 5],
    "Jupiter": [8, 11], "Venus": [1, 6], "Saturn": [9, 10],
}

# Naisargika (permanent / inborn) friendships.
_PLANET_FRIENDS = {
    "Sun": {"Moon", "Mars", "Jupiter"}, "Moon": {"Sun", "Mercury"},
    "Mars": {"Sun", "Moon", "Jupiter"}, "Mercury": {"Sun", "Venus"},
    "Jupiter": {"Sun", "Moon", "Mars"}, "Venus": {"Mercury", "Saturn"},
    "Saturn": {"Mercury", "Venus"},
}

# Naisargika (permanent / inborn) enmities.
_PLANET_ENEMIES = {
    "Sun": {"Venus", "Saturn"}, "Moon": set(), "Mars": {"Mercury"},
    "Mercury": {"Moon"}, "Jupiter": {"Mercury", "Venus"},
    "Venus": {"Sun", "Moon"}, "Saturn": {"Sun", "Moon", "Mars"},
}


# Compound (Panchadha) dignity scale — BPHS / B.V. Raman.
# Used by Shadbala's Saptavargaja Bala calculation.
_COMPOUND_DIGNITY = {
    "adhi_mitra": 22.5,   # intimate friend
    "mitra": 15.0,        # friend
    "sama": 7.5,          # neutral
    "shatru": 3.75,       # enemy
    "adhi_shatru": 1.875, # bitter enemy
}


# ── Shared fame-model / strength tables ──────────────────────────────────────
# Single source of truth for constants that were previously copied byte-for-byte
# across worldly_potential, vimsopaka, chart_strength, life_domains and
# fame_composite. Importing them from here keeps the fame calibration and the
# strength scores from silently drifting apart.

# 7-tier dignity → 0-100 strength percent (Nandish-confirmed scale). Used for
# Vimśopaka bala (factor 2) and the various dignity sub-scores.
DIGNITY_PCT: dict[str, int] = {
    "Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55,
    "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5,
}

# Shodashavarga weights (sum = 20) for Vimśopaka bala. "D1" is the natal rāśi
# sign itself; D60/D1/D9 carry the most.
VARGA_WEIGHTS: dict[str, float] = {
    "D1": 3.5, "D2": 1.0, "D3": 1.0, "D4": 0.5, "D7": 0.5, "D9": 3.0, "D10": 0.5,
    "D12": 0.5, "D16": 2.0, "D20": 0.5, "D24": 0.5, "D27": 0.5, "D30": 1.0,
    "D40": 0.5, "D45": 0.5, "D60": 4.0,
}

# Average Sarvashtakavarga bindus per sign (337 / 12 ≈ 28).
AVG_SAV = 28.0


def _compound_relationships(planets: dict) -> dict:
    """Compute Panchadha (5-fold compound) relationships between all classical planet pairs.

    Temporal friendship: planet in houses 2,3,4,10,11,12 from another = temporal friend; else enemy.
    Compound = natural + temporal:
        Friend+Friend → Adhi Mitra (22.5)  |  Friend+Enemy → Sama (7.5)
        Neutral+Friend → Mitra (15)        |  Neutral+Enemy → Shatru (3.75)
        Enemy+Friend → Sama (7.5)          |  Enemy+Enemy → Adhi Shatru (1.875)
    """
    _CLASSICAL = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    result = {}
    for p in _CLASSICAL:
        if p not in planets:
            continue
        p_sign = planets[p]["sign"]
        for q in _CLASSICAL:
            if q == p or q not in planets:
                continue
            q_sign = planets[q]["sign"]
            # Temporal: houses 2,3,4,10,11,12 (diffs 1,2,3,9,10,11) = friend; else enemy
            diff = (q_sign - p_sign) % 12
            temporal = "friend" if diff in (1, 2, 3, 9, 10, 11) else "enemy"
            # Natural
            if q in _PLANET_FRIENDS.get(p, set()):
                natural = "friend"
            elif q in _PLANET_ENEMIES.get(p, set()):
                natural = "enemy"
            else:
                natural = "neutral"
            # Compound
            if natural == "friend":
                compound = "adhi_mitra" if temporal == "friend" else "sama"
            elif natural == "enemy":
                compound = "sama" if temporal == "friend" else "adhi_shatru"
            else:  # neutral
                compound = "mitra" if temporal == "friend" else "shatru"
            result[(p, q)] = compound
    return result
