"""Yoga strength — Layer-2 "greatness" component of the Unshakable score.

Turns the binary yoga list from ``calc_yogas`` into a 0-100 "yoga power" number
by weighting each yoga by (a) a base greatness value for its type and (b) the
Shadbala of the planets forming it — a Raja yoga cast by *weak* planets is far
less potent than one cast by strong ones.

HEURISTIC (labelled indicative): base weights are first-pass and tunable. Full
classical cancellation (bhanga) is only *partially* modelled — through the
strength multiplier (weak/debilitated forming planets discount the yoga) plus
the Neecha-Bhanga that ``calc_yogas`` already detects. Tests lock behaviour, not
the magic numbers.
"""
from __future__ import annotations

import math

from app.services.kundli_calculator.yogas import calc_yogas

# Diminishing-returns curve: a few strong yogas no longer all flatten at 100.
# Spreads the mid-range and approaches 100 only asymptotically, so the yoga
# layer actually *discriminates* instead of saturating on yoga-rich days.
_SAT_K = 80.0


def _saturate(raw: float) -> float:
    return 100.0 * (1.0 - math.exp(-max(raw, 0.0) / _SAT_K))

# Base greatness points per yoga type. Mahapurusha (a "great personage" yoga) and
# Raja (power/status) yogas are the real greatness markers; Dhana = wealth;
# Chandra (lunar) yogas are supportive; "challenging" (e.g. Kemadruma) pulls down.
_BASE = {
    "mahapurusha": 30.0,
    "raj": 22.0,
    "dhan": 12.0,
    "chandra": 8.0,
    "challenging": -18.0,
}
_MULT_MIN, _MULT_MAX = 0.4, 1.6  # forming-planet Shadbala-ratio multiplier clamp


def yoga_strength(chart: dict) -> dict:
    """0-100 yoga-power score + the per-yoga contributions.

    Reads ``chart['planets']``, ``chart['lagna']`` and (for weighting)
    ``chart['shadbala']`` (per-planet ``ratio``). Missing Shadbala -> neutral
    multiplier of 1.0, so the score still works on a cheap chart.
    """
    yogas = calc_yogas(chart["planets"], chart["lagna"])
    sb = chart.get("shadbala", {})
    contributions: list[dict] = []
    total = 0.0
    for y in yogas:
        base = _BASE.get(y.get("type"), 5.0)
        ratios = [sb[p]["ratio"] for p in y.get("planets", [])
                  if p in sb and "ratio" in sb[p]]
        mult = (max(_MULT_MIN, min(sum(ratios) / len(ratios), _MULT_MAX))
                if ratios else 1.0)
        pts = round(base * mult, 1)
        total += pts
        contributions.append({"name": y.get("name"), "type": y.get("type"), "points": pts})
    return {"score": round(_saturate(total), 1), "raw": round(total, 1), "yogas": contributions}


def upper_bound(chart: dict) -> float:
    """Max yoga score this chart could reach with a perfect (max-multiplier)
    Shadbala — admissible bound for the funnel. Yoga *detection* needs no
    Shadbala, so this works on a cheap chart: positive yogas take the max
    multiplier, negative (challenging) ones take the min (least penalty)."""
    yogas = calc_yogas(chart["planets"], chart["lagna"])
    total = 0.0
    for y in yogas:
        base = _BASE.get(y.get("type"), 5.0)
        total += base * (_MULT_MAX if base > 0 else _MULT_MIN)
    return _saturate(total)
