"""Panchanga (Tithi, Yoga, Karan) for a given Julian Day.

Computes the lunar day, sun-moon yoga, and karana (half-tithi)
classification used by daily-muhurta and traditional chart pages.
"""

from __future__ import annotations

from ._core import TITHI_NAMES, YOGA_NAMES, _MOVABLE_KARANAS


def calc_panchanga(jd: float) -> dict:
    """Calculate Tithi, Yoga, and Karan."""
    import swisseph as swe
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags = swe.FLG_SIDEREAL

    sun, _ = swe.calc_ut(jd, swe.SUN, flags)
    moon, _ = swe.calc_ut(jd, swe.MOON, flags)
    sun_lon, moon_lon = sun[0] % 360, moon[0] % 360

    # Tithi: each 12° difference = 1 tithi (30 tithis per lunar month)
    diff = (moon_lon - sun_lon) % 360
    tithi_num = int(diff / 12) + 1  # 1–30
    tithi_name = TITHI_NAMES[min((tithi_num - 1) % 15, 14)]
    paksha = "Shukla" if tithi_num <= 15 else "Krishna"

    # Yoga: (Sun lon + Moon lon) / (360/27)
    yoga_lon = (sun_lon + moon_lon) % 360
    yoga_num = int(yoga_lon / (360 / 27))
    yoga_name = YOGA_NAMES[yoga_num % 27]

    # Karan: half-tithi (each 6° diff). There are 60 half-tithis in a lunar month,
    # 4 of which are fixed (Kimstughna at HT1, Shakuni/Chatushpada/Naga at HT58–60)
    # and the remaining 56 cycle through the 7 movable karanas (Bava … Vishti).
    half_tithi = int(diff / 6)  # 0–59
    if half_tithi == 0:
        karan_name = "Kimstughna"
    elif half_tithi == 57:
        karan_name = "Shakuni"
    elif half_tithi == 58:
        karan_name = "Chatushpada"
    elif half_tithi == 59:
        karan_name = "Naga"
    else:
        karan_name = _MOVABLE_KARANAS[(half_tithi - 1) % 7]

    return {
        "tithi_num": tithi_num,
        "tithi_name": tithi_name,
        "paksha": paksha,
        "yoga_name": yoga_name,
        "karan_name": karan_name,
    }
