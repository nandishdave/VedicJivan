"""Vimshottari Dasha — 120-year planetary period system.

Computes the Mahadasha sequence from birth based on Moon's nakshatra
position. Includes the date-math helpers (`_birth_datetime`,
`_add_years`) that other dasha-related sections (Sade Sati, Antardasha)
reuse.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta

from ._core import DASHA_SEQUENCE, DASHA_YEARS, NAKSHATRA_LORDS

# Tropical year — matches Astrosage's dasha math. Used by every
# multi-year cumulative computation in this module + sadesati.
_VIMSHOTTARI_DAYS_PER_YEAR = 365.2425


def _add_years(d: date, years: float) -> date:
    """Add fractional years to a date using the tropical year length."""
    days = years * _VIMSHOTTARI_DAYS_PER_YEAR
    return d + timedelta(days=days)


def _birth_datetime(dob: str, tob: str | None) -> datetime:
    """Build a birth datetime from date + optional time-of-birth string.

    Threading the exact birth time through dasha math avoids the ~1-2 day
    drift that midnight-anchored arithmetic introduces over multi-year cycles.
    """
    if tob:
        # Accept "HH:MM" or "HH:MM:SS"
        time_part = tob if len(tob) > 5 else f"{tob}:00"
        return datetime.fromisoformat(f"{dob}T{time_part}")
    return datetime.fromisoformat(f"{dob}T00:00:00")


def calc_vimshottari_dasha(moon_lon: float, dob: str, tob: str | None = None) -> dict:
    """Calculate full Vimshottari Dasha sequence from birth.

    `tob` (HH:MM or HH:MM:SS) anchors all date math to the exact birth
    moment, eliminating the ~1-2 day drift that midnight-anchored arithmetic
    introduces over multi-year cycles. If omitted, falls back to midnight.
    """
    nak_size = 360 / 27
    nak_num = int(moon_lon / nak_size)
    fraction_elapsed = (moon_lon % nak_size) / nak_size

    lord = NAKSHATRA_LORDS[nak_num]
    lord_idx = DASHA_SEQUENCE.index(lord)
    years_remaining = DASHA_YEARS[lord] * (1 - fraction_elapsed)

    birth_dt = _birth_datetime(dob, tob)
    dashas = []

    # Accumulate in float days from birth datetime; convert each MD's start/end
    # moment to its containing calendar date for display. Using datetime keeps
    # sub-day precision throughout, so the displayed date is the calendar day
    # that actually contains the boundary moment.
    cumulative_days = 0.0
    durations = [years_remaining] + [
        float(DASHA_YEARS[DASHA_SEQUENCE[(lord_idx + i) % 9]]) for i in range(1, 9)
    ]
    planet_seq = [lord] + [DASHA_SEQUENCE[(lord_idx + i) % 9] for i in range(1, 9)]

    for planet, years in zip(planet_seq, durations):
        start_dt = birth_dt + timedelta(days=cumulative_days)
        cumulative_days += years * _VIMSHOTTARI_DAYS_PER_YEAR
        end_dt = birth_dt + timedelta(days=cumulative_days)
        dashas.append({
            "planet": planet,
            "start_date": start_dt.date().isoformat(),
            "end_date": end_dt.date().isoformat(),
            "years": round(years, 2) if years != int(years) else years,
        })

    # Find current dasha
    today = date.today()
    current_dasha = next(
        (d for d in dashas if date.fromisoformat(d["start_date"]) <= today <= date.fromisoformat(d["end_date"])),
        dashas[0],
    )

    return {"dashas": dashas, "current_dasha": current_dasha}
