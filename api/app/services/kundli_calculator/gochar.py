"""Gochar (transits) — current planetary positions over the natal chart.

Computes house-from-Lagna and house-from-Moon for all 9 grahas at a
given date, classifies each as favorable / challenging per BPHS, and
flags special transits (Sade Sati, Gurubala, Ashtama Shani, etc.) plus
a Dasha-Gochar correlation note.

Reference: BPHS Ch.45-46, Phaladeepika Ch.26.
"""

from __future__ import annotations


# Classical favorable houses from natal Moon per transiting planet
# (BPHS / Phaladeepika).
_GOCHAR_FAVORABLE: dict[str, set[int]] = {
    "Sun":     {3, 6, 10, 11},
    "Moon":    {1, 3, 6, 7, 10, 11},
    "Mars":    {3, 6, 11},
    "Mercury": {2, 4, 6, 8, 10, 11},
    "Jupiter": {2, 5, 7, 9, 11},
    "Venus":   {1, 2, 3, 4, 5, 8, 9, 11, 12},
    "Saturn":  {3, 6, 11},
    "Rahu":    {3, 6, 10, 11},
    "Ketu":    {3, 6, 10, 11},
}

_SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]


def calc_gochar(
    natal_planets: dict,
    natal_lagna: dict,
    dasha: dict,
    current_jd: float | None = None,
) -> dict:
    """Compute current planetary transits (Gochar) over the natal chart.

    Args:
        natal_planets: planet dict from build_chart()
        natal_lagna: lagna dict from build_chart()
        dasha: dasha dict from calc_vimshottari_dasha() — for Dasha-Gochar note
        current_jd: Julian Day for transit date (default = today)

    Returns dict with:
        computed_for_date, transits (per planet), special_periods, dasha_gochar_note

    Reference: BPHS Ch.45-46, Phaladeepika Ch.26, B.V. Raman "Hindu Predictive Astrology"
    """
    import math
    import swisseph as swe
    from datetime import date as date_cls

    swe.set_sid_mode(swe.SIDM_LAHIRI)

    if current_jd is None:
        today = date_cls.today()
        # Noon UTC for today
        current_jd = swe.julday(today.year, today.month, today.day, 12.0)

    transit_date = swe.revjul(current_jd)
    computed_date = f"{int(transit_date[0])}-{int(transit_date[1]):02d}-{int(transit_date[2]):02d}"

    natal_moon_sign = natal_planets["Moon"]["sign"]   # 0-indexed
    natal_lagna_sign = natal_lagna["sign"]            # 0-indexed

    _SWE_CODES = {
        "Sun": swe.SUN, "Moon": swe.MOON, "Mars": swe.MARS,
        "Mercury": swe.MERCURY, "Jupiter": swe.JUPITER,
        "Venus": swe.VENUS, "Saturn": swe.SATURN,
        "Rahu": swe.MEAN_NODE,
    }

    transits: dict[str, dict] = {}
    special_periods: list[dict] = []

    for planet, code in _SWE_CODES.items():
        r, _ = swe.calc_ut(current_jd, code, swe.FLG_SIDEREAL | swe.FLG_SPEED)
        raw_lon = r[0] % 360
        # Ketu = Rahu + 180
        if planet == "Rahu" and r[3] > 0:
            raw_lon = r[0] % 360  # mean node can be direct in some ephemeris versions
        current_sign = int(raw_lon / 30)      # 0-indexed
        current_degree = round(raw_lon % 30, 2)

        # House from natal Lagna (Whole Sign)
        house_from_lagna = ((current_sign - natal_lagna_sign) % 12) + 1
        # House from natal Moon (Whole Sign)
        house_from_moon = ((current_sign - natal_moon_sign) % 12) + 1

        favorable_houses = _GOCHAR_FAVORABLE.get(planet, set())
        moon_favorable = house_from_moon in favorable_houses

        # Lagna-based — generally favorable if Kendra (1,4,7,10) or Trikona (1,5,9) for benefics
        benefics = {"Jupiter", "Venus", "Mercury", "Moon"}
        if planet in benefics:
            lagna_favorable = house_from_lagna in {1, 2, 3, 5, 9, 11}
        else:
            lagna_favorable = house_from_lagna in {3, 6, 10, 11}

        moon_label = "Favorable" if moon_favorable else "Challenging"
        lagna_label = "Favorable" if lagna_favorable else "Neutral"

        # Special named transits
        special: str | None = None
        if planet == "Jupiter":
            if house_from_moon in {2, 5, 7, 9, 11}:
                special = "Gurubala"
                special_periods.append({"name": "Gurubala", "planet": "Jupiter", "house_from_moon": house_from_moon})
            elif house_from_moon == 8:
                special = "Ashtama Guru (Kantaka)"
        elif planet == "Saturn":
            if house_from_moon in {12, 1, 2}:
                phase = {12: "Phase 1 (Rising)", 1: "Phase 2 (Peak)", 2: "Phase 3 (Setting)"}[house_from_moon]
                special = f"Sade Sati — {phase}"
                special_periods.append({"name": "Sade Sati", "planet": "Saturn", "phase": phase, "house_from_moon": house_from_moon})
            elif house_from_moon in {4, 8}:
                special = "Ashtama Shani"
                special_periods.append({"name": "Ashtama Shani", "planet": "Saturn", "house_from_moon": house_from_moon})
            elif house_from_moon in {3, 6, 11}:
                special = "Favorable Saturn Transit"

        transits[planet] = {
            "current_sign": current_sign,
            "current_sign_name": _SIGN_NAMES[current_sign],
            "current_degree": current_degree,
            "house_from_lagna": house_from_lagna,
            "house_from_moon": house_from_moon,
            "moon_transit_favorable": moon_favorable,
            "moon_transit_label": moon_label,
            "lagna_transit_label": lagna_label,
            "special": special,
        }

    # Add Ketu (always opposite Rahu)
    if "Rahu" in transits:
        rahu = transits["Rahu"]
        ketu_sign = (rahu["current_sign"] + 6) % 12
        ketu_house_lagna = ((ketu_sign - natal_lagna_sign) % 12) + 1
        ketu_house_moon = ((ketu_sign - natal_moon_sign) % 12) + 1
        ketu_favorable_houses = _GOCHAR_FAVORABLE.get("Ketu", set())
        ketu_favorable = ketu_house_moon in ketu_favorable_houses
        transits["Ketu"] = {
            "current_sign": ketu_sign,
            "current_sign_name": _SIGN_NAMES[ketu_sign],
            "current_degree": round((rahu["current_degree"] + 180) % 360 % 30, 2),
            "house_from_lagna": ketu_house_lagna,
            "house_from_moon": ketu_house_moon,
            "moon_transit_favorable": ketu_favorable,
            "moon_transit_label": "Favorable" if ketu_favorable else "Challenging",
            "lagna_transit_label": "Neutral",
            "special": None,
        }

    # ── Dasha-Gochar correlation note ─────────────────────────────────────────
    dasha_gochar_note = ""
    try:
        current_md = dasha.get("current_mahadasha", {})
        current_ad = dasha.get("current_antardasha", {})
        md_planet = current_md.get("planet", "")
        ad_planet = current_ad.get("planet", "")

        if md_planet and md_planet in transits:
            md_transit = transits[md_planet]
            md_favorable = md_transit["moon_transit_favorable"]
            md_house = md_transit["house_from_moon"]
            md_special = md_transit.get("special")

            # Dasha lord + transit quality
            if md_special and "Gurubala" in (md_special or ""):
                dasha_gochar_note = (
                    f"You are in {md_planet} Mahadasha and {md_planet} is currently in "
                    f"Gurubala (transiting {md_house}th from Moon) — this is a rare peak of "
                    f"Jupiter's blessings. Major positive life events are highly supported now."
                )
            elif md_special and "Sade Sati" in (md_special or ""):
                dasha_gochar_note = (
                    f"You are in {md_planet} Mahadasha and Saturn is simultaneously in Sade Sati "
                    f"({md_special}). This is a period of profound karmic reckoning — demands patience, "
                    f"discipline, and humility. Steady effort will yield results after the cycle ends."
                )
            elif md_special and "Ashtama Shani" in (md_special or ""):
                dasha_gochar_note = (
                    f"You are in {md_planet} Mahadasha during Ashtama Shani (Saturn transiting "
                    f"the {md_house}th from Moon). This doubles the challenge of the Saturn period. "
                    f"Focus on health, avoid risky decisions, and prioritise long-term stability."
                )
            elif md_favorable:
                dasha_gochar_note = (
                    f"You are in {md_planet} Mahadasha. {md_planet} is currently transiting the "
                    f"{md_house}th house from your Moon (favorable) — the Mahadasha lord is "
                    f"actively supporting this period. Good time for initiatives related to "
                    f"{md_planet}'s significations."
                )
            else:
                dasha_gochar_note = (
                    f"You are in {md_planet} Mahadasha. {md_planet} is currently transiting the "
                    f"{md_house}th house from your Moon (challenging) — the Mahadasha lord faces "
                    f"resistance in transit. Steady effort and caution are advised; avoid major "
                    f"new commitments until the transit improves."
                )

            # Add Antardasha note if different and also in transit
            if ad_planet and ad_planet != md_planet and ad_planet in transits:
                ad_transit = transits[ad_planet]
                ad_favorable = ad_transit["moon_transit_favorable"]
                ad_house = ad_transit["house_from_moon"]
                if ad_favorable:
                    dasha_gochar_note += (
                        f" Additionally, the Antardasha lord {ad_planet} is favorably transiting "
                        f"the {ad_house}th from Moon — a secondary wave of support in this period."
                    )
    except Exception:
        pass  # Non-critical — don't break chart if dasha data is malformed

    return {
        "computed_for_date": computed_date,
        "transits": transits,
        "special_periods": special_periods,
        "dasha_gochar_note": dasha_gochar_note,
    }
