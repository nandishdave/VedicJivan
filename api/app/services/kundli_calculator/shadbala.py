"""Shadbala — six-fold planetary strength (BPHS Ch.27-29).

Composes six strength categories per planet:
  Sthana Bala  — positional (exaltation, dignity, varga, gender, kendra, drekkana)
  Dig Bala     — directional (cardinal house preference per planet)
  Kala Bala    — temporal (nathonnatha, paksha, thribhaga, abda, masa, vara, hora, ayana, yuddha)
  Chesta Bala  — motional (retrograde / synodic arc)
  Naisargeka Bala — natural (fixed per planet)
  Drik Bala    — aspectual (benefic minus malefic Graha Drishti)

Outputs per-planet rupas (1 rupa = 60 virupas) plus the classical
minimum-Shadbala threshold per planet.

Extended planets (Rahu, Ketu, Uranus, Neptune, Pluto) use adapted
modern conventions — see the `_*_EXT` constants below.
"""

from __future__ import annotations

from ._core import SIGN_LORDS
from .dignity import (
    _COMPOUND_DIGNITY,
    _EXALTATION,
    _MOOLATRIKONA,
    _OWN_SIGNS,
    _PLANET_ENEMIES,
    _PLANET_FRIENDS,
    _compound_relationships,
)


_NAISARGEKA = {"Sun": 60, "Moon": 51.43, "Venus": 42.86, "Jupiter": 34.28, "Mercury": 25.71, "Mars": 17.14, "Saturn": 8.57}
_MIN_SHADBALA = {"Sun": 5, "Moon": 6, "Mars": 5, "Mercury": 7, "Jupiter": 6.5, "Venus": 5.5, "Saturn": 5}
_WEEKDAY_PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_DIG_STRONG_HOUSE = {"Sun": 10, "Jupiter": 10, "Moon": 4, "Venus": 4, "Mars": 7, "Saturn": 7, "Mercury": 1}
_MEAN_SPEED = {"Mars": 0.524, "Mercury": 1.383, "Jupiter": 0.083, "Venus": 1.2, "Saturn": 0.034}
_CLASSICAL_SWE_CODES = {"Sun": 0, "Moon": 1, "Mars": 4, "Mercury": 2, "Jupiter": 5, "Venus": 3, "Saturn": 6}


# ── Extended Shadbala parameters for Rahu, Ketu & outer planets ──────────────
# Based on adapted Vedic conventions — not classical texts but a modern extension.
# Rahu exalted in Gemini; Ketu in Sagittarius (Parashara tradition).
# Outer planet exaltations follow contemporary Jyotish research.
_EXALTATION_EXT = {"Rahu": 60, "Ketu": 240, "Uranus": 220, "Neptune": 95, "Pluto": 10}
_OWN_SIGNS_EXT = {
    "Rahu": [10],   # Aquarius only — Gemini is exaltation, kept separate
    "Ketu": [7],    # Scorpio only — Sagittarius is exaltation, kept separate
    "Uranus": [10],    # Aquarius (modern ruler)
    "Neptune": [11],   # Pisces (modern ruler)
    "Pluto": [7],      # Scorpio (modern ruler)
}
# Directional strength: Rahu/Saturn-like (west/7th), Ketu/Mars-like (east/1st),
# Uranus (west like Saturn), Neptune (north like Moon), Pluto (south like Sun)
_DIG_STRONG_HOUSE_EXT = {"Rahu": 7, "Ketu": 1, "Uranus": 7, "Neptune": 4, "Pluto": 10}
# Naisargeka: Rahu/Ketu midway between Saturn and Moon; outer planets below Saturn
_NAISARGEKA_EXT = {"Rahu": 12.86, "Ketu": 12.86, "Uranus": 7.14, "Neptune": 5.71, "Pluto": 4.29}
# Minimum strength requirements (adapted — roughly proportional to natural strength)
_MIN_SHADBALA_EXT = {"Rahu": 4.5, "Ketu": 4.5, "Uranus": 4.0, "Neptune": 3.5, "Pluto": 3.0}
# Day/night affinity: Rahu=night, Ketu=day, Uranus=neutral, Neptune=night, Pluto=day
_DAY_PLANET_EXT = {"Ketu": True, "Pluto": True}
_NIGHT_PLANET_EXT = {"Rahu": True, "Neptune": True}
# Paksha affinity: all malefic (strong in Krishna paksha = waning moon)
_BENEFIC_PAKSHA_EXT: set[str] = set()  # none — all treated as malefic
# Mean speeds for Chesta Bala (deg/day)
_MEAN_SPEED_EXT = {"Uranus": 0.012, "Neptune": 0.006, "Pluto": 0.004}

# Friendship / enmity for the shadow and outer planets. Classical texts don't
# assign these relations, so the mapping below follows the widely-used modern
# Jyotish convention (Rahu/Ketu) and the "higher octave" reasoning for the outer
# planets: Uranus → octave of Mercury / co-ruler with Saturn, Neptune → octave
# of Venus/Jupiter, Pluto → octave of Mars.
_PLANET_FRIENDS_EXT = {
    "Rahu":    {"Venus", "Saturn", "Mercury"},
    "Ketu":    {"Mars", "Venus", "Saturn", "Jupiter"},
    "Uranus":  {"Saturn", "Mercury", "Venus"},
    "Neptune": {"Jupiter", "Moon", "Venus"},
    "Pluto":   {"Mars", "Saturn", "Sun", "Jupiter"},
}
_PLANET_ENEMIES_EXT = {
    "Rahu":    {"Sun", "Moon", "Mars"},
    "Ketu":    {"Sun", "Moon"},
    "Uranus":  {"Sun", "Moon", "Mars"},
    "Neptune": {"Mercury", "Saturn", "Mars"},
    "Pluto":   {"Venus", "Moon", "Mercury"},
}


def _dignity_points(planet: str, sign: int, compound_rels: dict | None = None) -> float:
    """Return dignity points (0–45) for a planet in a given sign (Saptavargaja component).

    If compound_rels is provided, uses Panchadha (5-fold) relationship for the sign lord.
    Otherwise falls back to natural friendship only (used for extended planets).
    """
    # Extended planets use their own exaltation/own-sign tables
    if planet in _EXALTATION_EXT:
        exalt_sign = int(_EXALTATION_EXT[planet] / 30)
        debit_sign = (exalt_sign + 6) % 12
        if sign == exalt_sign:
            return 45.0
        if sign in _OWN_SIGNS_EXT.get(planet, []):
            return 30.0
        if sign == debit_sign:
            return 1.875
        return 7.5  # neutral (no classical friendship table for these)

    exalt_sign = int(_EXALTATION[planet] / 30)
    debit_sign = (exalt_sign + 6) % 12
    if sign == exalt_sign:
        return 45.0
    if sign == _MOOLATRIKONA.get(planet, -1):
        return 37.5
    if sign in _OWN_SIGNS.get(planet, []):
        return 30.0
    if sign == debit_sign:
        return 1.875
    lord = SIGN_LORDS[sign]
    if lord == planet:
        return 30.0  # own sign (safety — should be caught by _OWN_SIGNS above)
    # Use compound relationship if available
    if compound_rels and (planet, lord) in compound_rels:
        return _COMPOUND_DIGNITY.get(compound_rels[(planet, lord)], 7.5)
    # Fallback: natural friendship only
    if lord in _PLANET_FRIENDS.get(planet, set()):
        return 22.5
    if lord in _PLANET_ENEMIES.get(planet, set()):
        return 7.5
    return 7.5  # neutral (without compound = sama level)


def _graha_drishti(aspecting: str, angle: float) -> float:
    """Graha Drishti (aspect) strength for forward angle from aspecting planet.

    Returns 0–60 virupas. Linearly interpolated between house cusps (every 30°).
    Base: 3rd/10th=15(¼), 4th/8th=45(¾), 5th/9th=30(½), 7th=60(full), others=0.
    Special: Mars 4th/8th=60, Jupiter 5th/9th=60, Saturn 3rd/10th=60.
    """
    base = [0, 0, 15, 45, 30, 0, 60, 45, 30, 15, 0, 0]
    if aspecting == "Mars":
        base[3] = 60    # 4th house full
        base[7] = 60    # 8th house full
    elif aspecting == "Jupiter":
        base[4] = 60    # 5th house full
        base[8] = 60    # 9th house full
    elif aspecting == "Saturn":
        base[2] = 60    # 3rd house full
        base[9] = 60    # 10th house full

    angle = angle % 360
    idx = angle / 30.0
    lower = int(idx) % 12
    upper = (lower + 1) % 12
    frac = idx - int(idx)
    return base[lower] + (base[upper] - base[lower]) * frac


def _drik_bala(planet: str, planet_lon: float, planets: dict) -> float:
    """Drik Bala — aspectual strength from benefic/malefic Graha Drishti (BPHS).

    Formula: (sum of benefic Drishti on planet − sum of malefic Drishti on planet) / 4
    Benefics: Jupiter, Venus, Mercury, waxing Moon.  Malefics: Sun, Mars, Saturn.
    """
    _BENEFICS = {"Jupiter", "Venus", "Mercury"}
    _MALEFICS = {"Sun", "Mars", "Saturn"}

    # Moon: benefic when waxing (phase < 180°), malefic when waning
    moon_phase = (planets["Moon"]["longitude"] - planets["Sun"]["longitude"]) % 360
    moon_benefic = moon_phase < 180

    benefic_sum = 0.0
    malefic_sum = 0.0

    for other, od in planets.items():
        if other == planet:
            continue
        is_benefic = other in _BENEFICS or (other == "Moon" and moon_benefic)
        is_malefic = other in _MALEFICS or (other == "Moon" and not moon_benefic)
        if not is_benefic and not is_malefic:
            continue

        # Angle from aspecting planet (other) to target (planet) — forward
        angle = (planet_lon - od["longitude"]) % 360
        drishti = _graha_drishti(other, angle)

        if is_benefic:
            benefic_sum += drishti
        else:
            malefic_sum += drishti

    return round((benefic_sum - malefic_sum) / 4, 2)


def _parse_hm(t: str) -> float:
    """Parse HH:MM or HH:MM:SS string to float hours."""
    parts = t.split(":")
    h = int(parts[0])
    m = int(parts[1]) if len(parts) > 1 else 0
    s = int(parts[2]) if len(parts) > 2 else 0
    return h + m / 60.0 + s / 3600.0


def calc_shadbala(planets: dict, lagna: dict, jd: float, dob: str, tob: str,
                  divisional_charts: dict, sun_sunset: dict | None = None) -> dict:
    """Calculate Shadbala (six-fold planetary strength) for the 7 classical Vedic planets."""
    import math
    import swisseph as swe
    from datetime import date as date_cls

    SHADBALA_PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

    birth_date = date_cls.fromisoformat(dob)
    birth_h, birth_m = map(int, tob.split(":"))
    birth_time = birth_h + birth_m / 60.0

    moon_phase = (planets["Moon"]["longitude"] - planets["Sun"]["longitude"]) % 360

    # Compound (Panchadha) relationships from D1 positions — used for Saptavargaja
    compound_rels = _compound_relationships(planets)

    # Solar noon from actual sunrise/sunset (needed for Hora + Nathonnatha)
    if sun_sunset and sun_sunset.get("sunrise") not in (None, "N/A"):
        sr_h = _parse_hm(sun_sunset["sunrise"])
        ss_h = _parse_hm(sun_sunset["sunset"])
        solar_noon = (sr_h + ss_h) / 2
        day_half = (ss_h - sr_h) / 2
    else:
        sr_h, ss_h, solar_noon, day_half = 6.0, 18.0, 12.0, 6.0

    # Temporal lords
    vara_planet = _WEEKDAY_PLANETS[(birth_date.weekday() + 1) % 7]
    # Abda & Masa lords via Ahargana (B.V. Raman / BPHS method)
    # Epoch: July 10, 1951 (Tuesday). Ahargana = days from epoch to birth.
    _AHARGANA_EPOCH = date_cls(1951, 7, 10)
    _ABDA_PLANETS = ["Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Sun", "Moon"]
    ahargana = (birth_date - _AHARGANA_EPOCH).days
    # Year lord: (years * 3 + 1) % 7, where years = ahargana // 360
    year_planet = _ABDA_PLANETS[(ahargana // 360 * 3 + 1) % 7]
    # Month lord: (months * 2 + 1) % 7, where months = ahargana // 30
    month_planet = _ABDA_PLANETS[(ahargana // 30 * 2 + 1) % 7]
    # Hora lord uses Chaldean order (descending orbital period), NOT weekday order
    _CHALDEAN = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"]
    hora_num = max(0, int(birth_time - sr_h) if birth_time >= sr_h else int(birth_time + 24 - sr_h))
    hora_planet = _CHALDEAN[(_CHALDEAN.index(vara_planet) + hora_num) % 7]
    if sr_h <= birth_time <= ss_h:
        third = (ss_h - sr_h) / 3
        thribhaga_planet = ["Jupiter", "Sun", "Saturn"][min(int((birth_time - sr_h) / third), 2)]
    else:
        third = (24 - (ss_h - sr_h)) / 3
        thribhaga_planet = ["Moon", "Venus", "Mars"][min(int(((birth_time - ss_h) % 24) / third), 2)]

    # Tropical longitudes and celestial latitudes for Ayana Bala
    obliquity = math.radians(23.4397)
    tropical_lons = {}
    celestial_lats = {}
    for name, code in _CLASSICAL_SWE_CODES.items():
        r, _ = swe.calc_ut(jd, code, swe.FLG_SPEED)
        tropical_lons[name] = r[0] % 360
        celestial_lats[name] = r[1]  # celestial latitude in degrees

    # noon_frac: 1.0 at solar noon, 0.0 at sunrise/sunset — triangle function
    noon_frac = max(0.0, 1.0 - abs(birth_time - solar_noon) / day_half) if day_half > 0 else 0.0

    # moon_phase_frac: 0=new moon, 1=full moon
    moon_phase_frac = moon_phase / 180
    if moon_phase_frac > 1:
        moon_phase_frac = 2 - moon_phase_frac
    moon_phase_frac = max(0, min(1, moon_phase_frac))

    # Planet gender for Drekkana Bala
    _MALE_PLANETS = {"Sun", "Mars", "Jupiter"}
    _FEMALE_PLANETS = {"Moon", "Venus"}

    result = {}
    for planet in SHADBALA_PLANETS:
        if planet not in planets:
            continue
        pd = planets[planet]
        plon, psign, pdeg, phouse = pd["longitude"], pd["sign"], pd["degree_in_sign"], pd["house"]

        # ── Sthana Bala ──
        dist = abs(plon - _EXALTATION[planet])
        if dist > 180:
            dist = 360 - dist
        ochcha_bala = round((180 - dist) / 3, 2)

        # Saptavargaja: sum dignity across all 7 vargas (D1,D2,D3,D7,D9,D12,D30)
        # Uses compound (Panchadha) friendship for sign lord relationships
        sv = _dignity_points(planet, psign, compound_rels)  # D1
        for _v in ("D2", "D3", "D7", "D9", "D12", "D30"):
            if _v in divisional_charts and planet in divisional_charts[_v]:
                sv += _dignity_points(planet, divisional_charts[_v][planet], compound_rels)
        saptavargaja_bala = round(sv, 2)

        # Ojayugmarasyamsa: Oja (Rasi) + Yugma (Navamsa), each 15 max
        # Male planets (Sun,Mars,Mercury,Jupiter,Saturn) prefer odd signs
        # Female planets (Moon,Venus) prefer even signs
        rasi_odd = psign % 2 == 0  # 0-indexed: Aries(0)=odd, Taurus(1)=even
        nav_sign = divisional_charts.get("D9", {}).get(planet, psign)
        nav_odd = nav_sign % 2 == 0
        if planet in ("Moon", "Venus"):  # female — prefer even
            oja_rasi = 15 if not rasi_odd else 0
            oja_nav = 15 if not nav_odd else 0
        else:  # Sun, Mars, Mercury, Jupiter, Saturn — male/prefer odd
            oja_rasi = 15 if rasi_odd else 0
            oja_nav = 15 if nav_odd else 0
        ojayugma_bala = oja_rasi + oja_nav

        kendra_bala = 60 if phouse in (1, 4, 7, 10) else 30 if phouse in (2, 5, 8, 11) else 15

        # Drekkana Bala: 15 if planet is in its gender-appropriate drekkana, else 0
        drekkana_pos = int(pdeg / 10)  # 0=1st(0-10°), 1=2nd(10-20°), 2=3rd(20-30°)
        if planet in _MALE_PLANETS:
            drekkana_bala = 15 if drekkana_pos == 0 else 0
        elif planet in _FEMALE_PLANETS:
            drekkana_bala = 15 if drekkana_pos == 2 else 0
        else:  # Mercury, Saturn — neuter, strong in 2nd drekkana
            drekkana_bala = 15 if drekkana_pos == 1 else 0

        sthan_bala = round(ochcha_bala + saptavargaja_bala + ojayugma_bala + kendra_bala + drekkana_bala, 2)

        # ── Dig Bala ──
        strong_lon = (lagna["longitude"] + (_DIG_STRONG_HOUSE[planet] - 1) * 30) % 360
        diff = abs(plon - strong_lon)
        if diff > 180:
            diff = 360 - diff
        dig_bala = round((180 - diff) / 3, 2)

        # ── Kala Bala ──
        # Nathonnatha: day planets peak at solar noon, night planets peak at midnight
        if planet in ("Sun", "Jupiter", "Venus"):
            nathonnatha_bala = round(60 * noon_frac, 2)
        elif planet in ("Moon", "Mars", "Saturn"):
            nathonnatha_bala = round(60 * (1 - noon_frac), 2)
        else:
            nathonnatha_bala = 30

        if planet in ("Jupiter", "Venus"):  # only natural benefics
            paksha_bala = round(60 * moon_phase_frac, 2)
        else:  # Sun, Moon, Mars, Mercury, Saturn — malefic/conditional
            paksha_bala = round(60 * (1 - moon_phase_frac), 2)

        thribhaga_bala = 60 if (planet == thribhaga_planet or planet == "Jupiter") else 0
        abda_bala = 15 if planet == year_planet else 0
        masa_bala = 30 if planet == month_planet else 0
        vara_bala = 45 if planet == vara_planet else 0
        hora_bala = 60 if planet == hora_planet else 0

        trop_lon = tropical_lons.get(planet, plon)
        cel_lat = math.radians(celestial_lats.get(planet, 0.0))
        # Declination with celestial latitude: sin(d) = sin(lat)cos(obl) + cos(lat)sin(obl)sin(lon)
        sin_dec = (math.sin(cel_lat) * math.cos(obliquity) +
                   math.cos(cel_lat) * math.sin(obliquity) * math.sin(math.radians(trop_lon)))
        dec = math.degrees(math.asin(max(-1, min(1, sin_dec))))
        max_dec = 23.4397
        if planet in ("Moon", "Mercury", "Venus", "Saturn"):  # south-favoring
            ayana_bala = max(0, min(60, round(30 - (30 * dec / max_dec), 2)))
        else:  # Sun, Mars, Jupiter — north-favoring
            ayana_bala = max(0, min(60, round(30 + (30 * dec / max_dec), 2)))

        yuddha_bala = 0  # planetary war — requires close conjunction check

        kala_bala = round(nathonnatha_bala + paksha_bala + thribhaga_bala + abda_bala +
                          masa_bala + vara_bala + hora_bala + ayana_bala + yuddha_bala, 2)

        # Chesta Bala
        if planet == "Sun":
            # Solar anomaly (Manda Kendra): CK = tropical_sun - apogee
            sun_apogee = 103.0  # degrees, modern epoch approximate
            ck = math.radians(tropical_lons.get("Sun", plon) - sun_apogee)
            chesta_bala = round(max(0, min(60, (1 + math.cos(ck)) * 30)), 2)
        elif planet == "Moon":
            # Moon Chesta = brightness = Paksha Bala (benefic formula)
            chesta_bala = round(60 * moon_phase_frac, 2)
        elif pd["retrograde"]:
            chesta_bala = 60
        else:
            # Star planets: synodic arc (elongation from Sun) / 3
            sun_trop = tropical_lons.get("Sun", planets["Sun"]["longitude"])
            planet_trop = tropical_lons.get(planet, plon)
            elong = abs(planet_trop - sun_trop)
            if elong > 180:
                elong = 360 - elong
            chesta_bala = round(max(0, min(60, elong / 3)), 2)

        # ── Naisargeka Bala ──
        naisargeka_bala = _NAISARGEKA[planet]

        # ── Drik Bala ──
        drik = _drik_bala(planet, plon, planets)

        total = round(sthan_bala + dig_bala + kala_bala + chesta_bala + naisargeka_bala + drik, 2)
        rupas = round(total / 60, 2)
        min_req = _MIN_SHADBALA[planet]

        result[planet] = {
            "ochcha_bala": ochcha_bala, "saptavargaja_bala": saptavargaja_bala,
            "ojayugma_bala": ojayugma_bala, "kendra_bala": kendra_bala,
            "drekkana_bala": drekkana_bala, "sthan_bala": sthan_bala,
            "dig_bala": dig_bala,
            "nathonnatha_bala": nathonnatha_bala, "paksha_bala": paksha_bala,
            "thribhaga_bala": thribhaga_bala, "abda_bala": abda_bala,
            "masa_bala": masa_bala, "vara_bala": vara_bala, "hora_bala": hora_bala,
            "ayana_bala": ayana_bala, "yuddha_bala": yuddha_bala, "kala_bala": kala_bala,
            "chesta_bala": chesta_bala, "naisargeka_bala": naisargeka_bala,
            "drik_bala": drik,
            "total_shadbala": total, "shadbala_rupas": rupas,
            "min_requirement": min_req, "ratio": round(rupas / min_req, 2),
        }

    # Classical ranks
    classical = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    sorted_classical = sorted([p for p in classical if p in result],
                               key=lambda p: result[p]["total_shadbala"], reverse=True)
    for rank, p in enumerate(sorted_classical, 1):
        result[p]["rank"] = rank
        result[p]["is_extended"] = False

    # ── Extended planets: Rahu, Ketu, Uranus, Neptune, Pluto ──────────────────
    EXT_PLANETS = ["Rahu", "Ketu", "Uranus", "Neptune", "Pluto"]
    for planet in EXT_PLANETS:
        if planet not in planets:
            continue
        pd = planets[planet]
        plon, psign, pdeg, phouse = pd["longitude"], pd["sign"], pd["degree_in_sign"], pd["house"]

        # Ochcha Bala
        exalt_lon = _EXALTATION_EXT[planet]
        dist = abs(plon - exalt_lon)
        if dist > 180:
            dist = 360 - dist
        ochcha_bala = round((180 - dist) / 3, 2)

        # Saptavargaja (D1 only for extended — no classical vargas defined)
        saptavargaja_bala = round(_dignity_points(planet, psign), 2)

        # Ojayugmarasyamsa — neutral for all extended planets
        ojayugma_bala = 15

        kendra_bala = 60 if phouse in (1, 4, 7, 10) else 30 if phouse in (2, 5, 8, 11) else 15
        # Drekkana Bala: Uranus/Pluto=male, Neptune=female, Rahu/Ketu=neutral
        drekkana_pos = int(pdeg / 10)
        if planet in ("Uranus", "Pluto"):
            drekkana_bala = 15 if drekkana_pos == 0 else 0
        elif planet == "Neptune":
            drekkana_bala = 15 if drekkana_pos == 2 else 0
        else:  # Rahu, Ketu — neutral
            drekkana_bala = 15 if drekkana_pos == 1 else 0
        sthan_bala = round(ochcha_bala + saptavargaja_bala + ojayugma_bala + kendra_bala + drekkana_bala, 2)

        # Dig Bala
        strong_house = _DIG_STRONG_HOUSE_EXT[planet]
        strong_lon = (lagna["longitude"] + (strong_house - 1) * 30) % 360
        diff = abs(plon - strong_lon)
        if diff > 180:
            diff = 360 - diff
        dig_bala = round((180 - diff) / 3, 2)

        # Nathonnatha Bala (same noon_frac logic as classical)
        if planet in _DAY_PLANET_EXT:
            nathonnatha_bala = round(60 * noon_frac, 2)
        elif planet in _NIGHT_PLANET_EXT:
            nathonnatha_bala = round(60 * (1 - noon_frac), 2)
        else:
            nathonnatha_bala = 30  # Uranus: neutral

        # Paksha Bala — all extended treated as malefic (strong in Krishna)
        paksha_bala = round(60 * (1 - moon_phase_frac), 2)

        # Temporal lords: extended planets are not weekday/hora lords
        thribhaga_bala = 0
        abda_bala = 0
        masa_bala = 0
        vara_bala = 0
        hora_bala = 0

        # Ayana Bala from tropical declination (with celestial latitude)
        trop_lon = tropical_lons.get(planet, plon)
        cel_lat = math.radians(celestial_lats.get(planet, 0.0))
        sin_dec = (math.sin(cel_lat) * math.cos(obliquity) +
                   math.cos(cel_lat) * math.sin(obliquity) * math.sin(math.radians(trop_lon)))
        dec = math.degrees(math.asin(max(-1, min(1, sin_dec))))
        max_dec = 23.4397
        # Neptune: south-favoring; others: north-favoring
        if planet == "Neptune":
            ayana_bala = max(0, min(60, round(30 - (30 * dec / max_dec), 2)))
        else:
            ayana_bala = max(0, min(60, round(30 + (30 * dec / max_dec), 2)))

        yuddha_bala = 0

        kala_bala = round(nathonnatha_bala + paksha_bala + thribhaga_bala +
                          abda_bala + masa_bala + vara_bala + hora_bala + ayana_bala, 2)

        # Chesta Bala — Rahu/Ketu always retrograde = 60
        if planet in ("Rahu", "Ketu"):
            chesta_bala = 60
        elif pd["retrograde"]:
            chesta_bala = 60
        else:
            mean = _MEAN_SPEED_EXT.get(planet, 0.01)
            chesta_bala = round(min(60, 30 * abs(pd.get("speed", 0)) / mean), 2)

        naisargeka_bala = _NAISARGEKA_EXT[planet]
        drik = _drik_bala(planet, plon, planets)

        total = round(sthan_bala + dig_bala + kala_bala + chesta_bala + naisargeka_bala + drik, 2)
        rupas = round(total / 60, 2)
        min_req = _MIN_SHADBALA_EXT[planet]

        result[planet] = {
            "ochcha_bala": ochcha_bala, "saptavargaja_bala": saptavargaja_bala,
            "ojayugma_bala": ojayugma_bala, "kendra_bala": kendra_bala,
            "drekkana_bala": drekkana_bala, "sthan_bala": sthan_bala,
            "dig_bala": dig_bala,
            "nathonnatha_bala": nathonnatha_bala, "paksha_bala": paksha_bala,
            "thribhaga_bala": thribhaga_bala, "abda_bala": abda_bala,
            "masa_bala": masa_bala, "vara_bala": vara_bala, "hora_bala": hora_bala,
            "ayana_bala": ayana_bala, "yuddha_bala": yuddha_bala, "kala_bala": kala_bala,
            "chesta_bala": chesta_bala, "naisargeka_bala": naisargeka_bala,
            "drik_bala": drik,
            "total_shadbala": total, "shadbala_rupas": rupas,
            "min_requirement": min_req, "ratio": round(rupas / min_req, 2),
            "is_extended": True,
        }

    # Extended ranks (separate from classical)
    sorted_ext = sorted([p for p in EXT_PLANETS if p in result],
                        key=lambda p: result[p]["total_shadbala"], reverse=True)
    for rank, p in enumerate(sorted_ext, 1):
        result[p]["rank"] = rank

    return result


# ── Display transform for the calculator ────────────────────────────────────
_SB_ORDER = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]


def _rupa(virupa: float) -> float:
    """Virūpa (Ṣaṣṭiāṁśa) → Rūpa. 1 Rūpa = 60 Virūpas."""
    return round(virupa / 60.0, 2)


def shadbala_table(chart: dict) -> dict:
    """The six-fold strength per planet for the calculator, from the chart's
    ``shadbala`` block. All values in Rūpas (the six balas sum to Total, which
    is compared to the classical minimum requirement). Returns
    ``{planets: [{planet, rank, balas{sthana,dig,kala,cheshta,naisargika,drik},
      total, required, ratio, sufficient, sthana_parts{...}, kala_parts{...}}]}``.
    """
    sb = chart.get("shadbala") or {}
    planets = []
    for p in _SB_ORDER:
        d = sb.get(p)
        if not d:
            continue
        planets.append({
            "planet": p,
            "rank": d.get("rank"),
            "balas": {
                "sthana": _rupa(d["sthan_bala"]),
                "dig": _rupa(d["dig_bala"]),
                "kala": _rupa(d["kala_bala"]),
                "cheshta": _rupa(d["chesta_bala"]),
                "naisargika": _rupa(d["naisargeka_bala"]),
                "drik": _rupa(d["drik_bala"]),
            },
            "total": d["shadbala_rupas"],
            "required": d["min_requirement"],
            "ratio": d["ratio"],
            "sufficient": d["ratio"] >= 1.0,
            "sthana_parts": {
                "Uccha (exaltation)": _rupa(d["ochcha_bala"]),
                "Saptavargaja (dignity)": _rupa(d["saptavargaja_bala"]),
                "Ojayugma (odd/even)": _rupa(d["ojayugma_bala"]),
                "Kendradi (angularity)": _rupa(d["kendra_bala"]),
                "Drekkana (decanate)": _rupa(d["drekkana_bala"]),
            },
            "kala_parts": {
                "Nathonnatha (day/night)": _rupa(d["nathonnatha_bala"]),
                "Paksha (fortnight)": _rupa(d["paksha_bala"]),
                "Tribhaga (day-third)": _rupa(d["thribhaga_bala"]),
                "Abda (year lord)": _rupa(d["abda_bala"]),
                "Masa (month lord)": _rupa(d["masa_bala"]),
                "Vara (weekday lord)": _rupa(d["vara_bala"]),
                "Hora (hour lord)": _rupa(d["hora_bala"]),
                "Ayana (declination)": _rupa(d["ayana_bala"]),
                "Yuddha (planetary war)": _rupa(d["yuddha_bala"]),
            },
        })
    return {"planets": planets}
