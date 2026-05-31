"""Antardasha (sub-period) + Pratyantar (sub-sub-period) computation.

Both follow the classical Parashara proportional formula
(`md_full × ad_planet_yr / 120`). Datetime-based accumulation preserves
sub-day precision across multi-decade chains, matching Astrosage and
Jagannatha Hora.
"""

from __future__ import annotations

from datetime import date, datetime, time, timedelta

from ._core import DASHA_SEQUENCE, DASHA_YEARS
from .vimshottari import _VIMSHOTTARI_DAYS_PER_YEAR, _birth_datetime


def calc_antardasha(dashas: list[dict], dob: str | None = None, tob: str | None = None) -> list[dict]:
    """Calculate Antardasha (sub-periods) for each Mahadasha.

    Uses the classical Parashara approach (Convention A, also used by Astrosage
    and Jagannatha Hora): each antardasha runs its FULL proportional duration
    `md_full × ad_planet_yr / 120` regardless of whether the parent MD is
    partial. For the first MD (which is partially elapsed at birth) the actual
    MD start is computed as `birth_dt - elapsed_before_birth` (sub-day
    precision when `tob` is supplied), and all antardashas run from there
    with their full durations. The first antardasha may therefore end before
    birth — expected and matches Astrosage/Jagannatha Hora.
    """
    # When dob is supplied we can chain ALL MD starts from birth_dt instead
    # of relying on the displayed start date string (which has lost sub-day
    # precision). This keeps every AD boundary aligned with birth-time math.
    birth_dt = _birth_datetime(dob, tob) if dob else None

    result = []
    cumulative_birth_days = 0.0  # days from birth to current MD's actual start
    for md_idx, dasha in enumerate(dashas):
        planet = dasha["planet"]
        md_full_years = DASHA_YEARS[planet]
        md_partial_years = dasha["years"]

        # actual_md_start_dt: precise datetime for this MD's actual cycle start.
        if birth_dt is not None:
            if md_idx == 0:
                # First MD started before birth by `elapsed_before` years.
                elapsed_before = max(0.0, md_full_years - md_partial_years)
                actual_md_start_dt = birth_dt - timedelta(days=elapsed_before * _VIMSHOTTARI_DAYS_PER_YEAR)
                cumulative_birth_days = -elapsed_before * _VIMSHOTTARI_DAYS_PER_YEAR
            else:
                actual_md_start_dt = birth_dt + timedelta(days=cumulative_birth_days)
            cumulative_birth_days += md_full_years * _VIMSHOTTARI_DAYS_PER_YEAR
        else:
            # Legacy fallback: no birth_dt, use date-only math from displayed start.
            md_displayed_start = date.fromisoformat(dasha["start_date"])
            elapsed_before = max(0.0, md_full_years - md_partial_years)
            actual_md_start_dt = datetime.combine(
                md_displayed_start - timedelta(days=int(round(elapsed_before * _VIMSHOTTARI_DAYS_PER_YEAR))),
                time(0),
            )

        lord_idx = DASHA_SEQUENCE.index(planet)
        sub_periods = []
        cumulative_days = 0.0
        for i in range(9):
            ad_planet = DASHA_SEQUENCE[(lord_idx + i) % 9]
            ad_years = (md_full_years * DASHA_YEARS[ad_planet]) / 120
            start_dt = actual_md_start_dt + timedelta(days=cumulative_days)
            cumulative_days += ad_years * _VIMSHOTTARI_DAYS_PER_YEAR
            end_dt = actual_md_start_dt + timedelta(days=cumulative_days)
            sub_periods.append({
                "planet": ad_planet,
                "start_date": start_dt.date().isoformat(),
                "end_date": end_dt.date().isoformat(),
                "years": round(ad_years, 2),
            })

        result.append({
            "mahadasha": planet,
            "mahadasha_years": md_full_years,
            "start_date": dasha["start_date"],
            "end_date": dasha["end_date"],
            "antardashas": sub_periods,
        })
    return result


def calc_pratyantar(antardasha_data: list[dict], current_md_planet: str | None = None) -> list[dict]:
    """Calculate Pratyantar Dasha (3rd-level sub-sub-periods) for each Antardasha.

    Same proportional formula as Antardasha but one level deeper:
    PD duration = (AD_years × planet_years) / 120.

    Uses datetime-based accumulation from each AD's start so sub-day precision
    is preserved across the chain of pratyantars (no per-step day rounding).

    If current_md_planet is provided, only computes Pratyantars for that
    Mahadasha (keeps the report from bloating to 46+ pages of tables).
    """
    result = []
    for md in antardasha_data:
        if current_md_planet and md["mahadasha"] != current_md_planet:
            continue
        for ad in md["antardashas"]:
            ad_planet = ad["planet"]
            ad_years = ad["years"]
            ad_start_dt = datetime.combine(date.fromisoformat(ad["start_date"]), time(0))
            lord_idx = DASHA_SEQUENCE.index(ad_planet)

            sub_periods = []
            cumulative_days = 0.0
            for i in range(9):
                pd_planet = DASHA_SEQUENCE[(lord_idx + i) % 9]
                pd_years = (ad_years * DASHA_YEARS[pd_planet]) / 120
                pd_start_dt = ad_start_dt + timedelta(days=cumulative_days)
                cumulative_days += pd_years * _VIMSHOTTARI_DAYS_PER_YEAR
                pd_end_dt = ad_start_dt + timedelta(days=cumulative_days)
                sub_periods.append({
                    "planet": pd_planet,
                    "start_date": pd_start_dt.date().isoformat(),
                    "end_date": pd_end_dt.date().isoformat(),
                    "days": int(round(pd_years * _VIMSHOTTARI_DAYS_PER_YEAR)),
                })

            result.append({
                "mahadasha": md["mahadasha"],
                "antardasha": ad_planet,
                "start_date": ad["start_date"],
                "end_date": ad["end_date"],
                "pratyantars": sub_periods,
            })
    return result
