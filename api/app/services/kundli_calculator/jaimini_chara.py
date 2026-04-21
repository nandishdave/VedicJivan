"""Jaimini Chara Dasha — sign-based dasha system.

Each MD is a sign (not a planet). 12 signs cycle from the natal lagna.
Years per MD = K.N. Rao formula based on count from sign to its lord.
Direction depends on whether the sign is odd-1-indexed (zodiacal forward)
or even (anti-zodiacal backward).
"""

from __future__ import annotations

from datetime import timedelta

from ._core import SIGN_NAMES
from .vimshottari import _VIMSHOTTARI_DAYS_PER_YEAR, _birth_datetime


_JAIMINI_SIGN_LORDS = [
    "Mars",     # Aries
    "Venus",    # Taurus
    "Mercury",  # Gemini
    "Moon",     # Cancer
    "Sun",      # Leo
    "Mercury",  # Virgo
    "Venus",    # Libra
    "Mars",     # Scorpio (override to Ketu when Ketu is IN Scorpio)
    "Jupiter",  # Sagittarius
    "Saturn",   # Capricorn
    "Saturn",   # Aquarius (override to Rahu when Rahu is IN Aquarius)
    "Jupiter",  # Pisces
]
# Sign type: 0=Cara (movable), 1=Sthira (fixed), 2=Dvisvabhava (dual)
_JAIMINI_SIGN_TYPES = [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2]


def _char_dasha_years(sign_zero_indexed: int, planets: dict) -> int:
    """K.N. Rao Char Dasha — years for one sign.

    Direction by sign parity (1-indexed):
      Odd signs  (Ari, Gem, Leo, Lib, Sag, Aqu) → count zodiacally forward
      Even signs (Tau, Can, Vir, Sco, Cap, Pis) → count anti-zodiacally backward

    Years = inclusive count from sign to its lord, minus 1. The starting sign
    counts as 1. If the lord sits in the same sign as the dasha sign, the
    count is taken as 12 by special rule, giving 11 years.

    Lord selection (Jaimini convention):
      - Scorpio: classical lord is Mars; use Ketu *only when* Ketu itself sits
        in Scorpio.
      - Aquarius: classical lord is Saturn; use Rahu *only when* Rahu itself
        sits in Aquarius.
      - All other signs use their classical lord.
    """
    # Lord selection
    if sign_zero_indexed == 7:  # Scorpio
        lord = "Ketu" if planets.get("Ketu", {}).get("sign") == 7 else "Mars"
    elif sign_zero_indexed == 10:  # Aquarius
        lord = "Rahu" if planets.get("Rahu", {}).get("sign") == 10 else "Saturn"
    else:
        lord = _JAIMINI_SIGN_LORDS[sign_zero_indexed]

    if lord not in planets:
        return 11

    lord_sign = planets[lord]["sign"]
    if lord_sign == sign_zero_indexed:
        # Lord in own sign — count = 12, years = 11.
        return 11

    is_odd_sign = (sign_zero_indexed + 1) % 2 == 1
    if is_odd_sign:
        count_inclusive = (lord_sign - sign_zero_indexed) % 12 + 1
    else:
        count_inclusive = (sign_zero_indexed - lord_sign) % 12 + 1
    return count_inclusive - 1


def calc_char_dasha(planets: dict, lagna: dict, dob: str, tob: str | None = None) -> dict:
    """Compute the Jaimini Chara Dasha sequence + antardashas.

    - Mahadasha sequence: 12 signs starting from the natal lagna sign.
      Direction: zodiacal (forward) for odd 1-indexed lagna, anti-zodiacal
      (backward) for even.
    - Each MD's years = `_char_dasha_years` formula.
    - Antardashas within each MD: 12 signs in the SAME sequence order as the
      mahadashas, starting from the NEXT sign after the MD sign and ending
      with the MD sign itself. Each AD = MD years / 12.
    """
    birth_dt = _birth_datetime(dob, tob)
    lagna_sign = lagna["sign"]
    lagna_is_odd = (lagna_sign + 1) % 2 == 1

    sequence = []
    current = lagna_sign
    for _ in range(12):
        sequence.append(current)
        current = (current + 1) % 12 if lagna_is_odd else (current - 1) % 12

    dashas = []
    cumulative_days = 0.0
    for i, sign in enumerate(sequence):
        years = _char_dasha_years(sign, planets)
        md_start_dt = birth_dt + timedelta(days=cumulative_days)
        cumulative_days += years * _VIMSHOTTARI_DAYS_PER_YEAR
        md_end_dt = birth_dt + timedelta(days=cumulative_days)

        ad_periods = []
        ad_years = years / 12.0
        sub_cumulative = 0.0
        for k in range(12):
            ad_sign = sequence[(i + 1 + k) % 12]
            ad_start_dt = md_start_dt + timedelta(days=sub_cumulative)
            sub_cumulative += ad_years * _VIMSHOTTARI_DAYS_PER_YEAR
            ad_end_dt = md_start_dt + timedelta(days=sub_cumulative)
            ad_periods.append({
                "sign": ad_sign,
                "sign_name": SIGN_NAMES[ad_sign],
                "start_date": ad_start_dt.date().isoformat(),
                "end_date": ad_end_dt.date().isoformat(),
            })

        dashas.append({
            "sign": sign,
            "sign_name": SIGN_NAMES[sign],
            "years": years,
            "start_date": md_start_dt.date().isoformat(),
            "end_date": md_end_dt.date().isoformat(),
            "antardashas": ad_periods,
        })

    return {"dashas": dashas}
