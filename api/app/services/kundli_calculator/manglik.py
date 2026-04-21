"""Manglik Dosha — Mars-in-bad-house check (1, 2, 4, 7, 8, 12).

Pure: dict math only, no I/O. Uses Whole Sign houses for both Lagna
and Moon as anchor points (per Parashara tradition).
"""

from __future__ import annotations


def calc_manglik(planets: dict, lagna_sign: int) -> dict:
    """
    Manglik = Mars in houses 1, 2, 4, 7, 8, or 12 from Lagna or Moon.
    Mars in 2nd is included per Parashara tradition.
    Uses Whole Sign houses for both Lagna and Moon.
    """
    MANGLIK_HOUSES = {1, 2, 4, 7, 8, 12}
    mars_sign = planets["Mars"]["sign"]
    moon_sign = planets["Moon"]["sign"]
    mars_house_lagna = ((mars_sign - lagna_sign) % 12) + 1
    mars_house_from_moon = ((mars_sign - moon_sign) % 12) + 1

    from_lagna = mars_house_lagna in MANGLIK_HOUSES
    from_moon = mars_house_from_moon in MANGLIK_HOUSES
    is_manglik = from_lagna or from_moon

    return {
        "is_manglik": is_manglik,
        "from_lagna": from_lagna,
        "from_moon": from_moon,
        "mars_house_lagna": mars_house_lagna,
        "mars_house_moon": mars_house_from_moon,
    }
