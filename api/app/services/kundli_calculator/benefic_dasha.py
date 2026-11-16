"""Functional-benefic dasha timing — WHEN in life the good periods fall.

The Moon's nakshatra fixes the Vimshottari mahadasha sequence; the Lagna fixes
which planets are functional benefics. This scorer counts the years, up to age
80, spent under a functional-benefic mahadasha lord and weights them by life
stage: the same benefic years are worth most in the productive prime (20-50),
less in 50-60, and least in childhood (0-20) and late life (60-80).

Rahu/Ketu rule no sign, so a node's dasha takes the functional nature of its
dispositor (the codebase-wide rule for the nodes).

This is a CLASSICAL timing judgment, not a validated predictor: the fame study
tested functional-benefic dasha strength in 20-50 and rejected it as a *fame*
factor (see ReadMe/experiment-ledger.md), so it lives in the Unshakable score as
its own labelled layer and is deliberately kept out of ``worldly_potential``.
Stage weights are tunable.
"""
from __future__ import annotations

from datetime import date

from app.services.kundli_calculator.life_domains import (
    _functional_benefics,
    _node_dispositor,
)
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha

# (key, from-age, to-age, weight per benefic year). Order of preference:
# prime > mature > childhood = late.
STAGES: tuple[tuple[str, int, int, float], ...] = (
    ("childhood", 0, 20, 0.3),
    ("prime", 20, 50, 1.0),
    ("mature", 50, 60, 0.6),
    ("late", 60, 80, 0.3),
)
_MAX_WEIGHTED = sum((b - a) * w for _k, a, b, w in STAGES)
_DAYS_PER_YEAR = 365.25


def _is_benefic_lord(chart: dict, planet: str, benefics: set) -> bool:
    if planet in ("Rahu", "Ketu"):
        planet = _node_dispositor(chart, planet)
    return planet in benefics


def benefic_dasha(chart: dict) -> dict | None:
    """0-100 score for the life-stage placement of functional-benefic dashas.

    100 = every year from birth to 80 under a functional-benefic mahadasha; a
    chart whose benefic years all fall in 20-50 scores far above one with the
    same number of years in childhood or old age. Returns ``None`` when the
    chart has no birth date (the dashas can't be timed), so callers can drop
    the layer.

    Returns ``{"score", "years", "stages": {key: {"years", "of"}}, "benefics",
    "periods": [{"planet", "from_age", "to_age"}]}`` — ``years`` is the total
    benefic years out of 80; ``periods`` lists the benefic dashas in order.
    """
    dob = chart.get("dob")
    if not dob:
        return None
    dashas = chart.get("dashas")
    if dashas is None:
        dashas = calc_vimshottari_dasha(
            chart["planets"]["Moon"]["longitude"], dob, chart.get("tob", "12:00")
        )["dashas"]

    birth = date.fromisoformat(dob)
    benefics = _functional_benefics(chart)
    stage_years = {key: 0.0 for key, _a, _b, _w in STAGES}
    periods: list[dict] = []
    for d in dashas:
        if not _is_benefic_lord(chart, d["planet"], benefics):
            continue
        start = (date.fromisoformat(d["start_date"]) - birth).days / _DAYS_PER_YEAR
        end = (date.fromisoformat(d["end_date"]) - birth).days / _DAYS_PER_YEAR
        if start >= STAGES[-1][2] or end <= 0:
            continue
        periods.append({
            "planet": d["planet"],
            "from_age": round(max(start, 0.0), 1),
            "to_age": round(min(end, STAGES[-1][2]), 1),
        })
        for key, a, b, _w in STAGES:
            stage_years[key] += max(0.0, min(end, b) - max(start, a))

    weighted = sum(stage_years[key] * w for key, _a, _b, w in STAGES)
    return {
        "score": round(weighted / _MAX_WEIGHTED * 100.0, 1),
        "years": round(sum(stage_years.values()), 1),
        "stages": {
            key: {"years": round(stage_years[key], 1), "of": b - a}
            for key, a, b, _w in STAGES
        },
        "benefics": sorted(benefics),
        "periods": periods,
    }
