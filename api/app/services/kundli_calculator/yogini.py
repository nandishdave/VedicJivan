"""Yogini Dasha — 36-year cycle, 8 yoginis (Convention A, Astrosage parity).

Each yogini's mahadasha is partially elapsed at birth; the displayed MD
start is clipped to birth datetime so the user only sees the visible
balance window. Antardashas run their full proportional durations from
the actual cycle start; for the first MD, ADs that fully ended before
birth are skipped and the AD containing birth is clipped to start at birth.
"""

from __future__ import annotations

from datetime import datetime, timedelta

from .vimshottari import _VIMSHOTTARI_DAYS_PER_YEAR, _birth_datetime


YOGINI_NAMES = ["Sankata", "Mangala", "Pingala", "Dhanya", "Bhramari", "Bhadrika", "Ulka", "Siddha"]
YOGINI_YEARS = [8, 1, 2, 3, 4, 5, 6, 7]
YOGINI_ABBR = ["Sn", "Ma", "Pi", "Dh", "Br", "Ba", "Ul", "Si"]
# Each yogini's ruling planet (for sub-period calculation and interpretation)
YOGINI_PLANETS = ["Saturn", "Moon", "Sun", "Jupiter", "Mars", "Venus", "Mercury", "Rahu"]


def calc_yogini_dasha(moon_lon: float, dob: str, tob: str | None = None) -> dict:
    """Calculate Yogini Dasha sequence from birth (Convention A — Astrosage parity).

    Formula: yogini_index = (nakshatra_1indexed + 3) % 8.
    The first Yogini Mahadasha is partially elapsed at birth — its actual
    cycle start sits *before* birth. The MD's *displayed* start is clipped
    to the birth datetime so the user sees only the visible balance window
    (matches Astrosage). Within each MD, antardashas run their full
    proportional durations from the actual cycle start; for the first MD,
    ADs that fully ended before birth are skipped and the AD containing
    birth is clipped to start at birth.

    `tob` (HH:MM or HH:MM:SS) anchors all date math to the exact birth
    moment — fall back to midnight if not provided.
    """
    nak_size = 360 / 27
    nak_num = int(moon_lon / nak_size)
    nak_1indexed = nak_num + 1
    degree_in_nak = moon_lon - nak_num * nak_size
    fraction_elapsed = degree_in_nak / nak_size

    start_idx = (nak_1indexed + 3) % 8
    yogini_years_total = YOGINI_YEARS[start_idx]
    balance = yogini_years_total * (1 - fraction_elapsed)

    birth_dt = _birth_datetime(dob, tob)
    elapsed_days_float = fraction_elapsed * yogini_years_total * _VIMSHOTTARI_DAYS_PER_YEAR
    actual_first_md_start_dt = birth_dt - timedelta(days=elapsed_days_float)

    dashas = []
    cumulative_days = 0.0
    idx = start_idx
    for i in range(24):  # 24 periods ≈ 3 full 36-year cycles, ~108 years
        years = YOGINI_YEARS[idx]
        md_start_actual_dt = actual_first_md_start_dt + timedelta(days=cumulative_days)
        cumulative_days += years * _VIMSHOTTARI_DAYS_PER_YEAR
        md_end_dt = actual_first_md_start_dt + timedelta(days=cumulative_days)
        # Clip the first MD's *displayed* start to birth.
        md_start_display_dt = birth_dt if i == 0 else md_start_actual_dt
        dashas.append({
            "yogini": YOGINI_NAMES[idx],
            "abbr": YOGINI_ABBR[idx],
            "planet": YOGINI_PLANETS[idx],
            "years": years,
            "start_date": md_start_display_dt.date().isoformat(),
            "end_date": md_end_dt.date().isoformat(),
            "_actual_start_dt": md_start_actual_dt.isoformat(),
        })
        idx = (idx + 1) % 8

    # Antardashas — full proportional durations within each MD, datetime math.
    for md_idx, dasha_entry in enumerate(dashas):
        actual_start_dt = datetime.fromisoformat(dasha_entry.pop("_actual_start_dt"))
        d_years = dasha_entry["years"]
        d_idx = YOGINI_NAMES.index(dasha_entry["yogini"])

        sub_periods = []
        sub_cumulative = 0.0
        for i in range(8):
            sub_idx = (d_idx + i) % 8
            sub_years = (d_years * YOGINI_YEARS[sub_idx]) / 36
            sub_start_dt = actual_start_dt + timedelta(days=sub_cumulative)
            sub_cumulative += sub_years * _VIMSHOTTARI_DAYS_PER_YEAR
            sub_end_dt = actual_start_dt + timedelta(days=sub_cumulative)
            if md_idx == 0:
                if sub_end_dt <= birth_dt:
                    continue
                if sub_start_dt < birth_dt:
                    sub_start_dt = birth_dt
            sub_periods.append({
                "yogini": YOGINI_NAMES[sub_idx],
                "abbr": YOGINI_ABBR[sub_idx],
                "start_date": sub_start_dt.date().isoformat(),
                "end_date": sub_end_dt.date().isoformat(),
            })
        dasha_entry["antardashas"] = sub_periods

    return {
        "starting_yogini": YOGINI_NAMES[start_idx],
        "balance_years": round(balance, 2),
        "dashas": dashas,
    }
