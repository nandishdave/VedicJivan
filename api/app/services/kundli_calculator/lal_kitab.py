"""Lal Kitab Dasha — fixed 9-planet sequence, 35-year cycle.

Reverse-engineered from Astrosage's Lal Kitab section. Each MD has 3
sub-periods of equal length (MD/3) with sub-period planets per a
specific lookup table.
"""

from __future__ import annotations

from datetime import timedelta

from .vimshottari import _VIMSHOTTARI_DAYS_PER_YEAR, _birth_datetime


LAL_KITAB_DASHA_SEQUENCE = [
    "Saturn", "Rahu", "Ketu", "Jupiter", "Sun",
    "Moon", "Venus", "Mars", "Mercury",
]
LAL_KITAB_DASHA_YEARS = {
    "Saturn": 6, "Rahu": 6, "Ketu": 3, "Jupiter": 6, "Sun": 2,
    "Moon": 1, "Venus": 3, "Mars": 6, "Mercury": 2,
}
# Sub-period planets per parent MD — 3 per MD, in order.
LAL_KITAB_SUBPERIODS = {
    "Saturn":  ["Rahu", "Mars", "Mercury"],
    "Rahu":    ["Mars", "Ketu", "Saturn"],
    "Ketu":    ["Mercury", "Jupiter", "Sun"],
    "Jupiter": ["Mars", "Sun", "Moon"],
    "Sun":     ["Sun", "Moon", "Mars"],
    "Moon":    ["Sun", "Mars", "Venus"],
    "Venus":   ["Mars", "Sun", "Moon"],
    "Mars":    ["Mars", "Saturn", "Venus"],
    "Mercury": ["Moon", "Jupiter", "Sun"],
}


def calc_lal_kitab_dasha(dob: str, tob: str | None = None, n_cycles: int = 3) -> dict:
    """Compute the Lal Kitab Dasha sequence + sub-periods.

    Each cycle = 35 years. n_cycles default 3 covers ~105 years from birth.
    Sub-periods within each MD use a fixed lookup table.
    """
    birth_dt = _birth_datetime(dob, tob)
    cumulative_days = 0.0
    dashas = []
    for cycle in range(n_cycles):
        for planet in LAL_KITAB_DASHA_SEQUENCE:
            md_years = LAL_KITAB_DASHA_YEARS[planet]
            md_start_dt = birth_dt + timedelta(days=cumulative_days)
            cumulative_days += md_years * _VIMSHOTTARI_DAYS_PER_YEAR
            md_end_dt = birth_dt + timedelta(days=cumulative_days)

            # Sub-periods: 3 per MD, each = MD/3 years
            sub_planets = LAL_KITAB_SUBPERIODS[planet]
            sub_years = md_years / 3.0
            sub_periods = []
            sub_cumulative = 0.0
            for sp in sub_planets:
                sp_start_dt = md_start_dt + timedelta(days=sub_cumulative)
                sub_cumulative += sub_years * _VIMSHOTTARI_DAYS_PER_YEAR
                sp_end_dt = md_start_dt + timedelta(days=sub_cumulative)
                sub_periods.append({
                    "planet": sp,
                    "start_date": sp_start_dt.date().isoformat(),
                    "end_date": sp_end_dt.date().isoformat(),
                })

            dashas.append({
                "planet": planet,
                "years": md_years,
                "start_date": md_start_dt.date().isoformat(),
                "end_date": md_end_dt.date().isoformat(),
                "subperiods": sub_periods,
            })

    return {"dashas": dashas}
