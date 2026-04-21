"""Friendship tables — Naisargika + Tatkalika + Panchadha (compound).

Computes the three classical friendship matrices for the seven
traditional planets. The compound (5-fold) matrix combines the
Naisargika (permanent, lookup-based) and Tatkalika (temporary,
sign-position-based) relationships per BPHS / Raman.
"""

from __future__ import annotations

from .dignity import _PLANET_ENEMIES, _PLANET_FRIENDS, _compound_relationships


_CLASSICAL_PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]


def _natural_relation(p: str, q: str) -> str:
    """Naisargika (permanent / inborn) relationship between two classical planets."""
    if q in _PLANET_FRIENDS.get(p, set()):
        return "Friend"
    if q in _PLANET_ENEMIES.get(p, set()):
        return "Enemy"
    return "Neutral"


def _temporal_relation(p_sign: int, q_sign: int) -> str:
    """Tatkalika (temporary) relationship — based on house difference between two planets.

    A planet sitting in the 2nd, 3rd, 4th, 10th, 11th or 12th from another is a
    temporary friend; in the 1st, 5th, 6th, 7th, 8th or 9th it's a temporary enemy.
    """
    diff = (q_sign - p_sign) % 12
    return "T.Friend" if diff in (1, 2, 3, 9, 10, 11) else "T.Enemy"


_COMPOUND_LABELS = {
    "adhi_mitra": "Best Friend",
    "mitra": "Friend",
    "sama": "Neutral",
    "shatru": "Enemy",
    "adhi_shatru": "Bitter Enemy",
}


def calc_friendships(planets: dict) -> dict:
    """Compute the three classical friendship matrices for the seven traditional planets.

    Returns a dict with three 7×7 matrices (dict-of-dicts keyed by planet name):

      permanent : Naisargika (inborn) — static lookup, same for every chart.
      temporary : Tatkalika — chart-specific, derived from current sign positions.
      compound  : Panchadha (5-fold) — combination of the above per BPHS / Raman.

    Self-relation cells are rendered as "—". The display labels match what
    Astrosage and other Jyotish software show.
    """
    permanent: dict[str, dict[str, str]] = {}
    temporary: dict[str, dict[str, str]] = {}
    compound: dict[str, dict[str, str]] = {}

    rels = _compound_relationships(planets)

    for p in _CLASSICAL_PLANETS:
        permanent[p] = {}
        temporary[p] = {}
        compound[p] = {}
        for q in _CLASSICAL_PLANETS:
            if q == p:
                permanent[p][q] = "—"
                temporary[p][q] = "—"
                compound[p][q] = "—"
                continue
            permanent[p][q] = _natural_relation(p, q)
            if p in planets and q in planets:
                temporary[p][q] = _temporal_relation(planets[p]["sign"], planets[q]["sign"])
                compound_key = rels.get((p, q), "sama")
                compound[p][q] = _COMPOUND_LABELS.get(compound_key, "Neutral")
            else:
                temporary[p][q] = "—"
                compound[p][q] = "—"

    return {
        "planets": list(_CLASSICAL_PLANETS),
        "permanent": permanent,
        "temporary": temporary,
        "compound": compound,
    }
