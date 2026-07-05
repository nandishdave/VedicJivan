"""Poison-degree count — factor 18 of the worldly-potential fame model.

Counts how many of the 9 grahas + the Ascendant fall on a classically "poison"
degree, either of two kinds:

  * **Vish Navāṁśa** — the body sits in its sign's poison navamsa (an inauspicious
    3°20′ span; the navamsa number depends only on the sign group).
  * **Mṛtyu Bhāga** — the body is within ±1° of its *fatal degree* for that sign
    (the classical sign-varying planet×sign table).

Fewer poison-degree bodies marks the more prominent chart: over 225 famous vs 96
ordinary charts the famous averaged 1.64 such hits, the ordinary 2.01 (solo AUC
0.57, ~0.577 on the confound-clean cut; lifts the 17-factor composite's clean cut
0.809 → 0.816, seed-stable). The value is a raw count and is oriented
famous-negative by the REF in worldly_potential (fewer → higher score).

The auspicious counterpart tables (Pushkara Navāṁśa / Pushkara Bhāga) were tested
alongside and were near-noise (solo ~0.50-0.53) — they only diluted the signal, so
only the two *poison* tables feed the factor. See ReadMe/methodology.html.

Mṛtyu-Bhāga table (sign-varying) supplied + verified by Nandish, 2026-07-05.
"""
from __future__ import annotations

_NAV = 30.0 / 9.0                 # one navamsa = 3°20′
_MRITYU_TOL = 1.0                 # a body within this many degrees of its Mṛtyu degree counts
_BODIES = ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu")

# Vish (poison) navamsa number (1-9) per 0-indexed sign.
#   {Ar,Ta,Vi,Sg}→1   {Ge,Le,Li,Aq}→5   {Cn,Sc,Cp,Pi}→9
_VISH_NAV = {0: 1, 1: 1, 5: 1, 8: 1, 2: 5, 4: 5, 6: 5, 10: 5, 3: 9, 7: 9, 9: 9, 11: 9}

# Mṛtyu Bhāga fatal degree per body per sign — body → [12 degrees, sign order
# Aries..Pisces]. The Ascendant uses "Lagna". "Mandi" (Gulika) is kept for
# reference/future use but is NOT scored (we don't compute Mandi's position).
_MRITYU_BHAGA = {
    "Sun":     [20, 9, 12, 6, 8, 24, 16, 17, 22, 2, 3, 23],
    "Moon":    [26, 12, 13, 25, 24, 11, 26, 14, 13, 25, 5, 12],
    "Mars":    [19, 28, 25, 23, 29, 28, 14, 21, 2, 15, 11, 6],
    "Mercury": [15, 14, 13, 12, 8, 18, 20, 10, 21, 22, 7, 5],
    "Jupiter": [19, 29, 11, 27, 6, 4, 13, 6, 17, 11, 15, 28],
    "Venus":   [28, 15, 11, 17, 10, 13, 4, 19, 27, 12, 29, 19],
    "Saturn":  [10, 4, 7, 9, 12, 16, 3, 18, 28, 14, 13, 15],
    "Rahu":    [14, 13, 12, 11, 24, 23, 22, 21, 10, 10, 18, 8],
    "Ketu":    [8, 18, 20, 10, 21, 22, 23, 24, 11, 10, 13, 14],
    "Mandi":   [23, 24, 11, 12, 13, 8, 8, 18, 20, 20, 21, 20],
    "Lagna":   [1, 9, 22, 22, 25, 4, 4, 23, 18, 20, 24, 10],
}


def _hits(sign: int, deg: float, mrityu_key: str) -> int:
    """Poison hits for one body: +1 if in the sign's Vish navamsa, +1 if within
    ±tol of its Mṛtyu-Bhāga degree for that sign (a body may score both)."""
    n = 0
    if int(deg / _NAV) + 1 == _VISH_NAV[sign]:
        n += 1
    if abs(deg - _MRITYU_BHAGA[mrityu_key][sign]) <= _MRITYU_TOL:
        n += 1
    return n


def poison_degree_count(chart: dict) -> float:
    """Factor 18 — total poison-degree hits over the 9 grahas + the Ascendant.
    Lower = more prominent (oriented famous-negative in the REF)."""
    P, lag = chart["planets"], chart["lagna"]
    total = sum(_hits(P[b]["sign"], P[b]["degree_in_sign"], b) for b in _BODIES)
    total += _hits(lag["sign"], lag.get("degree", 0.0), "Lagna")   # Ascendant
    return float(total)
