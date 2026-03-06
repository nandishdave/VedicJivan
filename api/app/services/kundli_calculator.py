"""
Vedic astrology chart calculator using Swiss Ephemeris (pyswisseph).
All calculations use Lahiri Ayanamsa (sidereal mode) — same as AstroSage.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

# ── Constants ────────────────────────────────────────────────────────────────

SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]

SIGN_LORDS = [
    "Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
    "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter",
]

NAKSHATRA_NAMES = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishtha",
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati",
]

NAKSHATRA_LORDS = [
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu",
    "Jupiter", "Saturn", "Mercury", "Ketu", "Venus", "Sun",
    "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu",
    "Jupiter", "Saturn", "Mercury",
]

# Vimshottari Dasha: planet → years
DASHA_YEARS = {
    "Ketu": 7, "Venus": 20, "Sun": 6, "Moon": 10, "Mars": 7,
    "Rahu": 18, "Jupiter": 16, "Saturn": 19, "Mercury": 17,
}
DASHA_SEQUENCE = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]

# Nakshatra → dasha lord mapping (0-indexed)
NAKSHATRA_DASHA_LORD = NAKSHATRA_LORDS  # same order

# Planet codes for pyswisseph
SWE_PLANETS = {
    "Sun": 0,      # swe.SUN
    "Moon": 1,     # swe.MOON
    "Mars": 4,     # swe.MARS
    "Mercury": 2,  # swe.MERCURY
    "Jupiter": 5,  # swe.JUPITER
    "Venus": 3,    # swe.VENUS
    "Saturn": 6,   # swe.SATURN
    "Rahu": 11,    # swe.MEAN_NODE (North Node)
    "Uranus": 7,   # swe.URANUS
    "Neptune": 8,  # swe.NEPTUNE
    "Pluto": 9,    # swe.PLUTO
}

# Tithi names
TITHI_NAMES = [
    "Pratipada", "Dvitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima/Amavasya",
]

# Yoga names
YOGA_NAMES = [
    "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana",
    "Atiganda", "Sukarman", "Dhriti", "Shoola", "Ganda",
    "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra",
    "Siddhi", "Vyatipata", "Variyan", "Parigha", "Shiva",
    "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma",
    "Indra", "Vaidhriti",
]

# Karan names (11 karanas, each half-tithi)
KARAN_NAMES = [
    "Bava", "Balava", "Kaulava", "Taitila", "Garija",
    "Vanija", "Vishti", "Shakuni", "Chatushpada", "Naga", "Kimstughna",
]


# ── Julian Day helper ────────────────────────────────────────────────────────

def get_julian_day(dob: str, tob: str, lat: float, lon: float) -> float:
    """Convert local birth datetime to Julian Day (UT) using timezone from coordinates."""
    from timezonefinder import TimezoneFinder
    from zoneinfo import ZoneInfo

    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lat=lat, lng=lon) or "UTC"
    tz = ZoneInfo(tz_name)

    birth_date = date.fromisoformat(dob)
    h, m = map(int, tob.split(":"))
    local_dt = datetime(birth_date.year, birth_date.month, birth_date.day, h, m, tzinfo=tz)
    utc_dt = local_dt.astimezone(timezone.utc)

    # Julian Day calculation (astronomical formula)
    y, mo, d = utc_dt.year, utc_dt.month, utc_dt.day
    ut = utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0
    if mo <= 2:
        y -= 1
        mo += 12
    A = int(y / 100)
    B = 2 - A + int(A / 4)
    jd = int(365.25 * (y + 4716)) + int(30.6001 * (mo + 1)) + d + B - 1524.5 + ut / 24.0
    return jd


# ── Planet positions ─────────────────────────────────────────────────────────

def calc_planet_positions(jd: float, lat: float, lon: float) -> dict:
    """Calculate sidereal (Lahiri) planetary positions and house placements.
    Uses Whole Sign house system (standard in Vedic astrology):
    each house = one entire sign, house 1 = Ascendant sign.
    """
    import swisseph as swe

    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags = swe.FLG_SIDEREAL | swe.FLG_SPEED

    # Ascendant longitude (sidereal) — only need ascmc, not Placidus cusps
    _cusps, ascmc = swe.houses_ex(jd, lat, lon, b"W", swe.FLG_SIDEREAL)
    # b"W" = Whole Sign system; ascmc[0] = Ascendant longitude
    asc_lon = ascmc[0] % 360
    lagna_sign = int(asc_lon / 30)

    planets = {}
    for name, code in SWE_PLANETS.items():
        result, _ = swe.calc_ut(jd, code, flags)
        lon_deg = result[0] % 360
        speed = result[3]
        sign = int(lon_deg / 30)
        degree_in_sign = lon_deg % 30
        house = _whole_sign_house(sign, lagna_sign)
        planets[name] = {
            "longitude": round(lon_deg, 4),
            "sign": sign,
            "sign_name": SIGN_NAMES[sign],
            "sign_lord": SIGN_LORDS[sign],
            "degree_in_sign": round(degree_in_sign, 4),
            "house": house,
            "retrograde": speed < 0,
            "speed": round(speed, 6),
            "dignity": _get_dignity(name, sign),
        }

    # Ketu = Rahu + 180°
    rahu_lon = planets["Rahu"]["longitude"]
    ketu_lon = (rahu_lon + 180) % 360
    ketu_sign = int(ketu_lon / 30)
    planets["Ketu"] = {
        "longitude": round(ketu_lon, 4),
        "sign": ketu_sign,
        "sign_name": SIGN_NAMES[ketu_sign],
        "sign_lord": SIGN_LORDS[ketu_sign],
        "degree_in_sign": round(ketu_lon % 30, 4),
        "house": _whole_sign_house(ketu_sign, lagna_sign),
        "retrograde": True,  # Rahu/Ketu always retrograde
        "dignity": "",
    }
    planets["Rahu"]["retrograde"] = True

    return {
        "planets": planets,
        "lagna": {
            "longitude": round(asc_lon, 4),
            "sign": lagna_sign,
            "sign_name": SIGN_NAMES[lagna_sign],
            "sign_lord": SIGN_LORDS[lagna_sign],
            "degree": round(asc_lon % 30, 4),
        },
    }


def _whole_sign_house(planet_sign: int, lagna_sign: int) -> int:
    """Whole Sign house: house 1 = Lagna sign, house 2 = next sign, etc."""
    return ((planet_sign - lagna_sign) % 12) + 1


def _get_dignity(planet: str, sign: int) -> str:
    """Return the Vedic dignity of a planet in a given sign (sign 0-11 zero-indexed)."""
    if planet in ("Rahu", "Ketu", "Uranus", "Neptune", "Pluto"):
        return ""
    exalt_lon = _EXALTATION.get(planet)
    if exalt_lon is not None:
        exalt_sign = int(exalt_lon) // 30
        debil_sign = (exalt_sign + 6) % 12
        if sign == exalt_sign:
            return "Exalted"
        if sign == debil_sign:
            return "Debilitated"
    mt_sign = _MOOLATRIKONA.get(planet)
    if mt_sign is not None and sign == mt_sign:
        return "Moolatrikona"
    if sign in _OWN_SIGNS.get(planet, []):
        return "Own Sign"
    sign_lord = SIGN_LORDS[sign]
    if sign_lord in _PLANET_FRIENDS.get(planet, set()):
        return "Friendly Sign"
    if sign_lord in _PLANET_ENEMIES.get(planet, set()):
        return "Enemy Sign"
    return "Neutral Sign"


# ── Shadbala (Six-fold Planetary Strength) ───────────────────────────────────

# Exaltation degrees (sidereal, 0–359°)
_EXALTATION = {"Sun": 10, "Moon": 33, "Mars": 298, "Mercury": 165, "Jupiter": 95, "Venus": 357, "Saturn": 200}
_MOOLATRIKONA = {"Sun": 4, "Moon": 3, "Mars": 0, "Mercury": 5, "Jupiter": 8, "Venus": 6, "Saturn": 10}
_OWN_SIGNS = {
    "Sun": [4], "Moon": [3], "Mars": [0, 7], "Mercury": [2, 5],
    "Jupiter": [8, 11], "Venus": [1, 6], "Saturn": [9, 10],
}
_PLANET_FRIENDS = {
    "Sun": {"Moon", "Mars", "Jupiter"}, "Moon": {"Sun", "Mercury"},
    "Mars": {"Sun", "Moon", "Jupiter"}, "Mercury": {"Sun", "Venus"},
    "Jupiter": {"Sun", "Moon", "Mars"}, "Venus": {"Mercury", "Saturn"},
    "Saturn": {"Mercury", "Venus"},
}
_PLANET_ENEMIES = {
    "Sun": {"Venus", "Saturn"}, "Moon": set(), "Mars": {"Mercury"},
    "Mercury": {"Moon"}, "Jupiter": {"Mercury", "Venus"},
    "Venus": {"Sun", "Moon"}, "Saturn": {"Sun", "Moon", "Mars"},
}
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


def _compound_relationships(planets: dict) -> dict:
    """Compute Panchadha (5-fold compound) relationships between all classical planet pairs.

    Temporal friendship: planet in houses 2,3,4,10,11,12 from another = temporal friend; else enemy.
    Compound = natural + temporal:
        Friend+Friend → Adhi Mitra (22.5)  |  Friend+Enemy → Sama (7.5)
        Neutral+Friend → Mitra (15)        |  Neutral+Enemy → Shatru (3.75)
        Enemy+Friend → Sama (7.5)          |  Enemy+Enemy → Adhi Shatru (1.875)
    """
    _CLASSICAL = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    result = {}
    for p in _CLASSICAL:
        if p not in planets:
            continue
        p_sign = planets[p]["sign"]
        for q in _CLASSICAL:
            if q == p or q not in planets:
                continue
            q_sign = planets[q]["sign"]
            # Temporal: houses 2,3,4,10,11,12 (diffs 1,2,3,9,10,11) = friend; else enemy
            diff = (q_sign - p_sign) % 12
            temporal = "friend" if diff in (1, 2, 3, 9, 10, 11) else "enemy"
            # Natural
            if q in _PLANET_FRIENDS.get(p, set()):
                natural = "friend"
            elif q in _PLANET_ENEMIES.get(p, set()):
                natural = "enemy"
            else:
                natural = "neutral"
            # Compound
            if natural == "friend":
                compound = "adhi_mitra" if temporal == "friend" else "sama"
            elif natural == "enemy":
                compound = "sama" if temporal == "friend" else "adhi_shatru"
            else:  # neutral
                compound = "mitra" if temporal == "friend" else "shatru"
            result[(p, q)] = compound
    return result


# Compound (Panchadha) dignity scale — BPHS / B.V. Raman
_COMPOUND_DIGNITY = {
    "adhi_mitra": 22.5,   # intimate friend
    "mitra": 15.0,        # friend
    "sama": 7.5,          # neutral
    "shatru": 3.75,       # enemy
    "adhi_shatru": 1.875, # bitter enemy
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
    """Parse HH:MM string to float hours."""
    h, m = map(int, t.split(":"))
    return h + m / 60.0






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


# ── Nakshatra ────────────────────────────────────────────────────────────────

def calc_nakshatra(moon_lon: float) -> dict:
    """Calculate birth Nakshatra and Pada from Moon's sidereal longitude."""
    nak_size = 360 / 27  # 13°20' each
    pada_size = nak_size / 4
    nak_num = int(moon_lon / nak_size)  # 0–26
    pada = int((moon_lon % nak_size) / pada_size) + 1  # 1–4
    return {
        "num": nak_num,
        "name": NAKSHATRA_NAMES[nak_num],
        "lord": NAKSHATRA_LORDS[nak_num],
        "pada": pada,
        "degree_in_nak": round(moon_lon % nak_size, 4),
    }


# ── Panchanga (Tithi, Yoga, Karan) ──────────────────────────────────────────

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

    # Karan: half-tithi (each 6° diff)
    karan_num = int(diff / 6) % 11
    karan_name = KARAN_NAMES[karan_num]

    return {
        "tithi_num": tithi_num,
        "tithi_name": tithi_name,
        "paksha": paksha,
        "yoga_name": yoga_name,
        "karan_name": karan_name,
    }


# ── Vimshottari Dasha ────────────────────────────────────────────────────────

def calc_vimshottari_dasha(moon_lon: float, dob: str) -> dict:
    """Calculate full Vimshottari Dasha sequence from birth."""
    nak_size = 360 / 27
    nak_num = int(moon_lon / nak_size)
    fraction_elapsed = (moon_lon % nak_size) / nak_size

    lord = NAKSHATRA_LORDS[nak_num]
    lord_idx = DASHA_SEQUENCE.index(lord)
    years_remaining = DASHA_YEARS[lord] * (1 - fraction_elapsed)

    birth_date = date.fromisoformat(dob)
    dashas = []
    current_date = birth_date

    # First dasha (partial)
    end_date = _add_years(current_date, years_remaining)
    dashas.append({
        "planet": lord,
        "start_date": current_date.isoformat(),
        "end_date": end_date.isoformat(),
        "years": round(years_remaining, 2),
    })
    current_date = end_date

    # Subsequent dashas (full)
    for i in range(1, 9):
        planet = DASHA_SEQUENCE[(lord_idx + i) % 9]
        years = DASHA_YEARS[planet]
        end_date = _add_years(current_date, years)
        dashas.append({
            "planet": planet,
            "start_date": current_date.isoformat(),
            "end_date": end_date.isoformat(),
            "years": years,
        })
        current_date = end_date

    # Find current dasha
    today = date.today()
    current_dasha = next(
        (d for d in dashas if date.fromisoformat(d["start_date"]) <= today <= date.fromisoformat(d["end_date"])),
        dashas[0],
    )

    return {"dashas": dashas, "current_dasha": current_dasha}


def _add_years(d: date, years: float) -> date:
    """Add fractional years to a date."""
    days = years * 365.25
    return d + timedelta(days=days)


# ── Manglik Dosha ────────────────────────────────────────────────────────────

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


# ── Sade Sati ────────────────────────────────────────────────────────────────

def calc_sadesati(moon_sign: int) -> list[dict]:
    """
    Calculate Saturn's Sade Sati periods (past and future) from 1950 to 2100.
    Sade Sati = Saturn transiting 12th, 1st, 2nd house from Moon sign (7.5 years total).
    Saturn average transit per sign ≈ 2.46 years.
    """
    # Saturn approximate entry dates per sign (Vedic/sidereal)
    # Dates based on Lahiri ayanamsa Saturn transits
    SATURN_TRANSITS = [
        # (sign_num 0-11, entry_date)
        (8,  date(1987, 12, 17)),  # Sagittarius
        (9,  date(1990,  5, 21)),  # Capricorn
        (10, date(1993,  1, 26)),  # Aquarius
        (11, date(1995,  6, 23)),  # Pisces
        (0,  date(1998,  4, 29)),  # Aries
        (1,  date(2000,  8,  8)),  # Taurus
        (2,  date(2002, 11,  8)),  # Gemini
        (3,  date(2004,  9, 16)),  # Cancer
        (4,  date(2007, 12, 16)),  # Leo
        (5,  date(2009,  9, 11)),  # Virgo
        (6,  date(2011, 11, 15)),  # Libra
        (7,  date(2014, 11,  2)),  # Scorpio
        (8,  date(2017,  1, 26)),  # Sagittarius
        (9,  date(2020,  1, 24)),  # Capricorn
        (10, date(2022,  4, 29)),  # Aquarius
        (11, date(2025,  3, 29)),  # Pisces
        (0,  date(2027,  6,  5)),  # Aries
        (1,  date(2029,  9,  2)),  # Taurus
        (2,  date(2032,  1, 10)),  # Gemini
        (3,  date(2034,  8, 10)),  # Cancer
        (4,  date(2036, 10, 21)),  # Leo
        (5,  date(2039,  8,  3)),  # Virgo
        (6,  date(2041, 10, 13)),  # Libra
        (7,  date(2044, 10,  1)),  # Scorpio
        (8,  date(2046, 12,  5)),  # Sagittarius
    ]

    sadesati_signs = {
        (moon_sign - 1) % 12: "Rising",
        moon_sign: "Peak",
        (moon_sign + 1) % 12: "Setting",
    }

    periods = []
    for i, (sign, entry) in enumerate(SATURN_TRANSITS):
        if sign in sadesati_signs:
            # End = next transit entry (or estimate 2.46 years later)
            if i + 1 < len(SATURN_TRANSITS):
                exit_date = SATURN_TRANSITS[i + 1][1]
            else:
                exit_date = _add_years(entry, 2.46)
            periods.append({
                "phase": sadesati_signs[sign],
                "rashi": SIGN_NAMES[sign],
                "start_date": entry.isoformat(),
                "end_date": exit_date.isoformat(),
            })

    return sorted(periods, key=lambda p: p["start_date"])


# ── Divisional Charts (Vargas) ────────────────────────────────────────────────

def calc_divisional_charts(planets: dict, lagna: dict) -> dict:
    """Calculate divisional chart positions: D2, D3, D7, D9, D10, D12, D30, D60."""
    charts = {}
    for chart_type in ("D2", "D3", "D7", "D9", "D10", "D12", "D30", "D60"):
        chart = {}
        for name, info in planets.items():
            chart[name] = _calc_varga_sign(info["sign"], info["degree_in_sign"], chart_type)
        # Also calculate Lagna position in each varga
        chart["Lagna"] = _calc_varga_sign(lagna["sign"], lagna["degree"], chart_type)
        charts[chart_type] = chart
    return charts


def _calc_varga_sign(sign: int, degree: float, chart_type: str) -> int:
    """Calculate the resulting sign (0–11) for a planet in a divisional chart."""
    is_odd = sign % 2 == 0  # 0-indexed: Aries(0)=odd, Taurus(1)=even

    if chart_type == "D2":
        # Hora: 2 parts per sign (15° each)
        # Odd sign: 0-15° → Leo(4), 15-30° → Cancer(3)
        # Even sign: 0-15° → Cancer(3), 15-30° → Leo(4)
        half = 0 if degree < 15 else 1
        if is_odd:
            return 4 if half == 0 else 3
        else:
            return 3 if half == 0 else 4

    elif chart_type == "D3":
        # Drekkana: 3 parts (10° each)
        # 1st (0-10°): same sign, 2nd (10-20°): 5th from sign, 3rd (20-30°): 9th from sign
        part = min(int(degree / 10), 2)
        offsets = [0, 4, 8]
        return (sign + offsets[part]) % 12

    elif chart_type == "D9":
        # Navamsa: 9 parts (3°20' each)
        # Fire signs (0,4,8): start from Aries(0)
        # Earth signs (1,5,9): start from Capricorn(9)
        # Air signs (2,6,10): start from Libra(6)
        # Water signs (3,7,11): start from Cancer(3)
        element = sign % 4
        starts = {0: 0, 1: 9, 2: 6, 3: 3}
        part = min(int(degree / (30 / 9)), 8)
        return (starts[element] + part) % 12

    elif chart_type == "D10":
        # Dasamsa: 10 parts (3° each)
        # Odd sign: start from same sign
        # Even sign: start from 9th sign (sign + 8)
        part = min(int(degree / 3), 9)
        start = sign if is_odd else (sign + 8) % 12
        return (start + part) % 12

    elif chart_type == "D12":
        # Dwadasamsa: 12 parts (2°30' each), start from same sign
        part = min(int(degree / 2.5), 11)
        return (sign + part) % 12

    elif chart_type == "D7":
        # Saptamsa: 7 equal parts of 4°17' each
        # Odd signs: start from same sign; Even signs: start from 7th sign
        part = min(int(degree / (30 / 7)), 6)
        start = sign if is_odd else (sign + 6) % 12
        return (start + part) % 12

    elif chart_type == "D30":
        # Trimshamsa: unequal parts (no portion for 0° boundary planet)
        # Odd signs: Mars(0-5)→Aries, Saturn(5-10)→Aquarius,
        #   Jupiter(10-18)→Sagittarius, Mercury(18-25)→Gemini, Venus(25-30)→Libra
        # Even signs: Venus(0-5)→Taurus, Mercury(5-12)→Virgo,
        #   Jupiter(12-20)→Pisces, Saturn(20-25)→Capricorn, Mars(25-30)→Scorpio
        if is_odd:
            if degree < 5:    return 0   # Aries
            elif degree < 10: return 10  # Aquarius
            elif degree < 18: return 8   # Sagittarius
            elif degree < 25: return 2   # Gemini
            else:             return 6   # Libra
        else:
            if degree < 5:    return 1   # Taurus
            elif degree < 12: return 5   # Virgo
            elif degree < 20: return 11  # Pisces
            elif degree < 25: return 9   # Capricorn
            else:             return 7   # Scorpio

    elif chart_type == "D60":
        # Shastiamsa: 60 parts (0°30' each), start from same sign
        part = min(int(degree / 0.5), 59)
        return (sign + part) % 12

    return sign


# ── Antardasha (Sub-periods) ─────────────────────────────────────────────────

def calc_antardasha(dashas: list[dict]) -> list[dict]:
    """Calculate Antardasha (sub-periods) for each Mahadasha."""
    result = []
    for dasha in dashas:
        planet = dasha["planet"]
        md_years = dasha["years"]
        md_start = date.fromisoformat(dasha["start_date"])
        lord_idx = DASHA_SEQUENCE.index(planet)

        sub_periods = []
        current = md_start
        for i in range(9):
            ad_planet = DASHA_SEQUENCE[(lord_idx + i) % 9]
            ad_years = (md_years * DASHA_YEARS[ad_planet]) / 120
            ad_end = _add_years(current, ad_years)
            sub_periods.append({
                "planet": ad_planet,
                "start_date": current.isoformat(),
                "end_date": ad_end.isoformat(),
                "years": round(ad_years, 2),
            })
            current = ad_end

        result.append({
            "mahadasha": planet,
            "mahadasha_years": md_years,
            "start_date": dasha["start_date"],
            "end_date": dasha["end_date"],
            "antardashas": sub_periods,
        })
    return result


# ── Sunrise / Sunset ─────────────────────────────────────────────────────────

def _get_local_tz(lat: float, lon: float):
    """Get ZoneInfo timezone for given coordinates."""
    from timezonefinder import TimezoneFinder
    from zoneinfo import ZoneInfo
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lat=lat, lng=lon) or "UTC"
    return ZoneInfo(tz_name)


def calc_sunrise_sunset(jd: float, lat: float, lon: float) -> dict:
    """Calculate sunrise and sunset times for the birth date (local time)."""
    import swisseph as swe
    try:
        geopos = (lon, lat, 0)  # (longitude, latitude, altitude)
        sunrise_jd = swe.rise_trans(jd - 1, swe.SUN, "", 0, swe.CALC_RISE, geopos, 0, 0)
        sunset_jd = swe.rise_trans(jd - 1, swe.SUN, "", 0, swe.CALC_SET, geopos, 0, 0)
        sr_jd = sunrise_jd[0] if isinstance(sunrise_jd, tuple) else sunrise_jd
        ss_jd = sunset_jd[0] if isinstance(sunset_jd, tuple) else sunset_jd

        local_tz = _get_local_tz(lat, lon)

        def jd_to_local_hm(j):
            """Convert Julian Day to local HH:MM string."""
            # JD → UTC datetime
            frac = (j + 0.5) % 1.0
            total_minutes_utc = round(frac * 24 * 60)
            utc_dt = datetime(2000, 1, 1, total_minutes_utc // 60, total_minutes_utc % 60, tzinfo=timezone.utc)
            # Convert to local
            local_dt = utc_dt.astimezone(local_tz)
            return f"{local_dt.hour:02d}:{local_dt.minute:02d}"

        return {"sunrise": jd_to_local_hm(sr_jd), "sunset": jd_to_local_hm(ss_jd)}
    except Exception:
        return {"sunrise": "N/A", "sunset": "N/A"}


# ── Yoga Detection ───────────────────────────────────────────────────────────

def calc_yogas(planets: dict, lagna: dict) -> list[dict]:
    """Detect classical Vedic yogas present in the birth chart.

    Returns a list of present yogas. Each entry has:
      name, type, description, planets (list), house (int|None)

    Types: mahapurusha | raj | dhan | chandra | challenging
    Reference: BPHS Ch.36, Phaladeepika Ch.6-7, B.V. Raman "300 Important Combinations"
    """
    CLASSICAL = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    BENEFICS = {"Jupiter", "Venus", "Mercury"}
    yogas: list[dict] = []
    lagna_sign = lagna["sign"]

    # ── Helpers ──────────────────────────────────────────────────────────────

    def psign(p: str) -> int:
        return planets[p]["sign"] if p in planets else -1

    def phouse(p: str) -> int | None:
        return planets[p]["house"] if p in planets else None

    def sign_lord(sign_idx: int) -> str:
        return SIGN_LORDS[sign_idx % 12]

    def house_lord(n: int) -> str:
        return sign_lord(lagna_sign + n - 1)

    def in_kendra(p: str) -> bool:
        return phouse(p) in (1, 4, 7, 10)

    def in_trikona(p: str) -> bool:
        return phouse(p) in (1, 5, 9)

    def in_kendra_or_trikona(p: str) -> bool:
        return phouse(p) in (1, 4, 5, 7, 9, 10)

    def in_dusthana(p: str) -> bool:
        return phouse(p) in (6, 8, 12)

    def in_own_sign(p: str) -> bool:
        s = psign(p)
        return s in _OWN_SIGNS.get(p, []) or s == _MOOLATRIKONA.get(p, -1)

    def in_exaltation(p: str) -> bool:
        return psign(p) == int(_EXALTATION[p] / 30) if p in _EXALTATION else False

    def in_debilitation(p: str) -> bool:
        if p not in _EXALTATION:
            return False
        return psign(p) == (int(_EXALTATION[p] / 30) + 6) % 12

    def in_dignity(p: str) -> bool:
        return in_own_sign(p) or in_exaltation(p)

    def same_sign(p1: str, p2: str) -> bool:
        return p1 in planets and p2 in planets and psign(p1) == psign(p2)

    def aspects(aspector: str, target: str) -> bool:
        """Graha Drishti — sign-based aspect (house count forward from aspector)."""
        if aspector not in planets or target not in planets:
            return False
        diff = round(((planets[target]["longitude"] - planets[aspector]["longitude"]) % 360) / 30)
        if diff == 7:
            return True
        if aspector == "Mars" and diff in (4, 8):
            return True
        if aspector == "Jupiter" and diff in (5, 9):
            return True
        if aspector == "Saturn" and diff in (3, 10):
            return True
        return False

    # ── 1. Pancha Mahapurusha Yogas ──────────────────────────────────────────
    for yoga_name, planet, desc in [
        ("Ruchaka", "Mars",    "Mars strong in Kendra → courage, leadership, physical strength, warrior spirit."),
        ("Bhadra",  "Mercury", "Mercury strong in Kendra → sharp intellect, eloquence, business acumen, scholarship."),
        ("Hamsa",   "Jupiter", "Jupiter strong in Kendra → wisdom, spirituality, dharmic authority, teaching ability."),
        ("Malavya", "Venus",   "Venus strong in Kendra → luxury, arts, beauty, refined pleasures, marital happiness."),
        ("Sasa",    "Saturn",  "Saturn strong in Kendra → discipline, mass following, endurance, administrative power."),
    ]:
        if planet in planets and in_dignity(planet) and in_kendra(planet):
            yogas.append({
                "name": f"{yoga_name} Yoga",
                "type": "mahapurusha",
                "description": desc,
                "planets": [planet],
                "house": phouse(planet),
            })

    # ── 2. Gaja Kesari Yoga ───────────────────────────────────────────────────
    if "Jupiter" in planets and "Moon" in planets:
        diff = (psign("Jupiter") - psign("Moon")) % 12
        if diff in (0, 3, 6, 9) and not in_debilitation("Jupiter"):
            yogas.append({
                "name": "Gaja Kesari Yoga",
                "type": "raj",
                "description": "Jupiter in Kendra from Moon → wisdom, fame, prosperity, noble character, leadership.",
                "planets": ["Jupiter", "Moon"],
                "house": phouse("Jupiter"),
            })

    # ── 3. Budhaditya Yoga ────────────────────────────────────────────────────
    if same_sign("Sun", "Mercury") and not in_debilitation("Mercury"):
        yogas.append({
            "name": "Budhaditya Yoga",
            "type": "raj",
            "description": "Sun and Mercury conjunct → sharp analytical mind, articulate communication, success in intellectual or government roles.",
            "planets": ["Sun", "Mercury"],
            "house": phouse("Sun"),
        })

    # ── 4. Chandra Mangala Yoga ───────────────────────────────────────────────
    if same_sign("Moon", "Mars"):
        yogas.append({
            "name": "Chandra Mangala Yoga",
            "type": "dhan",
            "description": "Moon and Mars conjunct → financial gains through bold action, entrepreneurial drive, strong willpower.",
            "planets": ["Moon", "Mars"],
            "house": phouse("Moon"),
        })

    # ── 5. Moon Yogas: Sunapha / Anapha / Durudhara / Kemdrum ────────────────
    moon_sign = psign("Moon")
    second_from_moon  = (moon_sign + 1) % 12
    twelfth_from_moon = (moon_sign - 1) % 12
    p2  = [p for p in CLASSICAL if p not in ("Sun", "Moon") and psign(p) == second_from_moon]
    p12 = [p for p in CLASSICAL if p not in ("Sun", "Moon") and psign(p) == twelfth_from_moon]

    if p2 and not p12:
        yogas.append({
            "name": "Sunapha Yoga",
            "type": "chandra",
            "description": "Planet(s) in 2nd from Moon (none in 12th) → self-made wealth, intelligence, confident nature.",
            "planets": ["Moon"] + p2,
            "house": None,
        })
    elif p12 and not p2:
        yogas.append({
            "name": "Anapha Yoga",
            "type": "chandra",
            "description": "Planet(s) in 12th from Moon (none in 2nd) → charisma, comfortable life, spiritual inclination.",
            "planets": ["Moon"] + p12,
            "house": None,
        })
    elif p2 and p12:
        yogas.append({
            "name": "Durudhara Yoga",
            "type": "chandra",
            "description": "Planets in both 2nd and 12th from Moon → abundant wealth, recognition, well-rounded prosperous life.",
            "planets": ["Moon"] + p2 + p12,
            "house": None,
        })
    else:
        yogas.append({
            "name": "Kemdrum Yoga",
            "type": "challenging",
            "description": "No planets in 2nd or 12th from Moon → emotional instability, need for self-reliance. Effect reduced if Moon or benefics are in Kendra.",
            "planets": ["Moon"],
            "house": None,
        })

    # ── 6. Dharma Karmadhipati Yoga ───────────────────────────────────────────
    lord_9  = house_lord(9)
    lord_10 = house_lord(10)
    if lord_9 != lord_10 and lord_9 in planets and lord_10 in planets:
        if same_sign(lord_9, lord_10) or aspects(lord_9, lord_10) or aspects(lord_10, lord_9):
            yogas.append({
                "name": "Dharma Karmadhipati Yoga",
                "type": "raj",
                "description": (
                    f"Lords of 9th ({lord_9}) and 10th ({lord_10}) are conjunct or in mutual aspect "
                    f"→ highly successful career, dharmic profession, authority, government recognition."
                ),
                "planets": [lord_9, lord_10],
                "house": None,
            })

    # ── 7. Viparita Raja Yoga (Harsha / Sarala / Vimala) ─────────────────────
    lord_6  = house_lord(6)
    lord_8  = house_lord(8)
    lord_12 = house_lord(12)
    for label, variant, lord in [
        ("6th",  "Harsha",  lord_6),
        ("8th",  "Sarala",  lord_8),
        ("12th", "Vimala",  lord_12),
    ]:
        if lord in planets and phouse(lord) in (6, 8, 12):
            yogas.append({
                "name": f"Viparita Raja Yoga — {variant}",
                "type": "raj",
                "description": (
                    f"Lord of {label} house ({lord}) placed in a dusthana (6/8/12) "
                    f"→ rise after adversity, hidden strength, victory over enemies."
                ),
                "planets": [lord],
                "house": phouse(lord),
            })

    # ── 8. Neecha Bhanga Raja Yoga ────────────────────────────────────────────
    for p in CLASSICAL:
        if p not in planets or not in_debilitation(p):
            continue
        debit_sign = psign(p)
        debit_lord = sign_lord(debit_sign)
        exalt_lord = sign_lord(int(_EXALTATION[p] / 30))
        reasons: list[str] = []

        if debit_lord in planets and in_kendra(debit_lord):
            reasons.append(f"{debit_lord} (lord of debilitation sign) in Kendra")
        if exalt_lord in planets and in_kendra(exalt_lord):
            reasons.append(f"{exalt_lord} (lord of exaltation sign) in Kendra")
        if same_sign(p, debit_lord):
            reasons.append(f"conjunct its sign lord {debit_lord}")

        if reasons:
            yogas.append({
                "name": f"Neecha Bhanga Raja Yoga ({p})",
                "type": "raj",
                "description": (
                    f"{p} is debilitated but cancellation occurs ({'; '.join(reasons)}) "
                    f"→ weakness converts to strength, rise from adversity."
                ),
                "planets": [p],
                "house": phouse(p),
            })

    # ── 9. Amala Yoga ─────────────────────────────────────────────────────────
    tenth_planets = [p for p in CLASSICAL if phouse(p) == 10]
    if tenth_planets and all(p in BENEFICS for p in tenth_planets):
        yogas.append({
            "name": "Amala Yoga",
            "type": "raj",
            "description": "Only benefics in 10th house → spotless reputation, fame through ethical means, respected career.",
            "planets": tenth_planets,
            "house": 10,
        })

    # ── 10. Lakshmi Yoga ──────────────────────────────────────────────────────
    if lord_9 in planets and in_dignity(lord_9) and "Venus" in planets and in_kendra_or_trikona("Venus"):
        yogas.append({
            "name": "Lakshmi Yoga",
            "type": "dhan",
            "description": (
                f"9th lord ({lord_9}) in own/exaltation sign + Venus in Kendra/Trikona "
                f"→ great wealth, luxury, blessings of Lakshmi, material abundance."
            ),
            "planets": [lord_9, "Venus"],
            "house": None,
        })

    # ── 11. Adhi Yoga ─────────────────────────────────────────────────────────
    adhi_planets = [
        p for p in ("Jupiter", "Venus", "Mercury")
        if p in planets and (psign(p) - moon_sign) % 12 in (5, 6, 7)
    ]
    if len(adhi_planets) >= 2:
        yogas.append({
            "name": "Adhi Yoga",
            "type": "raj",
            "description": (
                f"Benefics ({', '.join(adhi_planets)}) in 6th/7th/8th from Moon "
                f"→ leadership, authority, noble environment, victory over enemies."
            ),
            "planets": adhi_planets,
            "house": None,
        })

    return yogas


# ── Dosha Detection ──────────────────────────────────────────────────────────

def calc_doshas(planets: dict, lagna: dict) -> list[dict]:
    """Detect classical Vedic doshas (afflictions) in the birth chart.

    Returns a list of present doshas. Each entry has:
      name, type, description, planets (list), house (int|None)
      + optional severity (for Kaal Sarp only)

    Note: Mangal Dosha and Sade Sati are handled by calc_manglik() and
    calc_sadesati() separately — they are NOT duplicated here.

    Types: kaal_sarp | pitra | guru_chandal | grahan | angarak | vish | shakat
    Reference: BPHS, Phaladeepika, B.V. Raman "300 Important Combinations"
    """
    CLASSICAL = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    _KAAL_SARP_NAMES = [
        "Anant", "Kulik", "Vasuki", "Shankhapal", "Padma", "Mahapadma",
        "Takshak", "Karkotak", "Shankachood", "Ghatak", "Vishdhar", "Sheshnag",
    ]
    doshas: list[dict] = []

    def psign(p: str) -> int:
        return planets[p]["sign"] if p in planets else -1

    def phouse(p: str) -> int | None:
        return planets[p]["house"] if p in planets else None

    def plon(p: str) -> float:
        return planets[p]["longitude"] if p in planets else 0.0

    def same_sign(p1: str, p2: str) -> bool:
        return p1 in planets and p2 in planets and psign(p1) == psign(p2)

    # ── 1. Kaal Sarp Dosha ───────────────────────────────────────────────────
    if "Rahu" in planets and "Ketu" in planets:
        rahu_lon = plon("Rahu")
        present_classical = [p for p in CLASSICAL if p in planets]
        arcs = [(plon(p) - rahu_lon) % 360 for p in present_classical]

        planets_between = sum(1 for a in arcs if a < 180)
        planets_outside = sum(1 for a in arcs if a > 180)
        total = len(present_classical)

        if planets_between == total:
            rahu_house = phouse("Rahu") or 1
            variant = _KAAL_SARP_NAMES[rahu_house - 1]
            doshas.append({
                "name": f"Kaal Sarp Dosha — {variant}",
                "type": "kaal_sarp",
                "description": (
                    f"All planets are hemmed between Rahu ({rahu_house}th house) and Ketu. "
                    f"{variant} variant — challenges related to the {rahu_house}th house significations. "
                    f"Indicates karmic restriction of life force by the serpent axis."
                ),
                "planets": ["Rahu", "Ketu"] + present_classical,
                "house": rahu_house,
                "severity": "full",
            })
        elif planets_outside == total:
            doshas.append({
                "name": "Kaal Amrit Yoga",
                "type": "kaal_sarp",
                "description": (
                    "All planets are on the Ketu-to-Rahu arc (reverse Kaal Sarp). "
                    "Associated with spiritual depth, fame after hardship, and liberation energy."
                ),
                "planets": ["Rahu", "Ketu"] + present_classical,
                "house": phouse("Ketu"),
                "severity": "reverse",
            })
        elif planets_between >= 5:
            rahu_house = phouse("Rahu") or 1
            variant = _KAAL_SARP_NAMES[rahu_house - 1]
            doshas.append({
                "name": f"Partial Kaal Sarp Dosha — {variant}",
                "type": "kaal_sarp",
                "description": (
                    f"{planets_between} of {total} planets hemmed between Rahu and Ketu. "
                    f"Partial {variant} Kaal Sarp — milder effect than full dosha."
                ),
                "planets": ["Rahu", "Ketu"],
                "house": rahu_house,
                "severity": "partial",
            })

    # ── 2. Pitra Dosha ───────────────────────────────────────────────────────
    pitra_reasons: list[str] = []
    pitra_planets: list[str] = ["Sun"]

    if same_sign("Sun", "Rahu"):
        pitra_reasons.append("Sun conjunct Rahu — ancestral confusion")
        pitra_planets.append("Rahu")
    if same_sign("Sun", "Ketu"):
        pitra_reasons.append("Sun conjunct Ketu — detachment from paternal lineage")
        if "Ketu" not in pitra_planets:
            pitra_planets.append("Ketu")
    if "Rahu" in planets and phouse("Rahu") == 9:
        pitra_reasons.append("Rahu in 9th house — affliction to house of father/dharma")
        if "Rahu" not in pitra_planets:
            pitra_planets.append("Rahu")
    if "Ketu" in planets and phouse("Ketu") == 9:
        pitra_reasons.append("Ketu in 9th house — ancestral karmic debt")
        if "Ketu" not in pitra_planets:
            pitra_planets.append("Ketu")
    if "Sun" in planets and "Saturn" in planets and same_sign("Sun", "Saturn") and phouse("Sun") == 9:
        pitra_reasons.append("Sun and Saturn conjunct in 9th — severe father-karma burden")
        if "Saturn" not in pitra_planets:
            pitra_planets.append("Saturn")

    if pitra_reasons:
        doshas.append({
            "name": "Pitra Dosha",
            "type": "pitra",
            "description": (
                "Ancestral debt indicated: " + "; ".join(pitra_reasons) + ". "
                "Challenges with father, paternal lineage, or receiving ancestral blessings. "
                "Remedy: Pitru Tarpan, Shradh rituals, charity on Amavasya."
            ),
            "planets": pitra_planets,
            "house": phouse("Sun"),
        })

    # ── 3. Guru Chandal Dosha ────────────────────────────────────────────────
    if same_sign("Jupiter", "Rahu"):
        doshas.append({
            "name": "Guru Chandal Dosha",
            "type": "guru_chandal",
            "description": (
                "Jupiter conjunct Rahu — Rahu corrupts Jupiter's wisdom and dharma. "
                "May manifest as misguided beliefs, unorthodox spirituality, or guru-related issues. "
                "Can also produce unconventional brilliance and esoteric inclination."
            ),
            "planets": ["Jupiter", "Rahu"],
            "house": phouse("Jupiter"),
        })
    elif same_sign("Jupiter", "Ketu"):
        doshas.append({
            "name": "Guru Chandal Dosha (Ketu)",
            "type": "guru_chandal",
            "description": (
                "Jupiter conjunct Ketu — spiritual detachment from conventional wisdom. "
                "Past-life spiritual karma, inclination toward moksha, or disconnection from dharmic guidance."
            ),
            "planets": ["Jupiter", "Ketu"],
            "house": phouse("Jupiter"),
        })

    # ── 4. Grahan Dosha ──────────────────────────────────────────────────────
    if same_sign("Sun", "Rahu") or same_sign("Sun", "Ketu"):
        afflicting = "Rahu" if same_sign("Sun", "Rahu") else "Ketu"
        doshas.append({
            "name": "Surya Grahan Dosha",
            "type": "grahan",
            "description": (
                f"Sun conjunct {afflicting} — solar eclipse pattern in natal chart. "
                "Identity confusion, authority challenges, difficulties with father. "
                "Soul's expression is partially eclipsed."
            ),
            "planets": ["Sun", afflicting],
            "house": phouse("Sun"),
        })

    if same_sign("Moon", "Rahu") or same_sign("Moon", "Ketu"):
        afflicting = "Rahu" if same_sign("Moon", "Rahu") else "Ketu"
        doshas.append({
            "name": "Chandra Grahan Dosha",
            "type": "grahan",
            "description": (
                f"Moon conjunct {afflicting} — lunar eclipse pattern in natal chart. "
                "Emotional instability, anxiety, difficult relationship with mother. "
                "Mind is susceptible to obsessive patterns."
            ),
            "planets": ["Moon", afflicting],
            "house": phouse("Moon"),
        })

    # ── 5. Angarak Dosha ─────────────────────────────────────────────────────
    if same_sign("Mars", "Rahu"):
        doshas.append({
            "name": "Angarak Dosha",
            "type": "angarak",
            "description": (
                "Mars conjunct Rahu — Rahu amplifies Mars's aggression to explosive levels. "
                "Risk of accidents, legal trouble, or impulsive outbursts. "
                "Can produce extraordinary ambition when channelled constructively."
            ),
            "planets": ["Mars", "Rahu"],
            "house": phouse("Mars"),
        })

    # ── 6. Vish Yoga ─────────────────────────────────────────────────────────
    if same_sign("Saturn", "Moon"):
        doshas.append({
            "name": "Vish Yoga",
            "type": "vish",
            "description": (
                "Saturn and Moon conjunct — Saturn suppresses Moon's emotional warmth. "
                "Tendency toward depression, emotional coldness, or difficult relationship with mother. "
                "Severity depends on Moon's sign strength."
            ),
            "planets": ["Saturn", "Moon"],
            "house": phouse("Moon"),
        })

    # ── 7. Shakat Yoga ───────────────────────────────────────────────────────
    if "Jupiter" in planets and "Moon" in planets:
        diff = (psign("Jupiter") - psign("Moon")) % 12
        if diff in (5, 7):
            doshas.append({
                "name": "Shakat Yoga",
                "type": "shakat",
                "description": (
                    "Jupiter in 6th or 8th from Moon — opposite of Gaja Kesari. "
                    "Fluctuating fortune, instability in career and finances, recurring obstacles. "
                    "Reduced if Jupiter is strong or in Kendra from Lagna."
                ),
                "planets": ["Jupiter", "Moon"],
                "house": phouse("Jupiter"),
            })

    return doshas


# ── Gochar (Transits) ─────────────────────────────────────────────────────────

# Classical favorable houses from natal Moon per transiting planet (BPHS / Phaladeepika)
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


# ── Numerology ────────────────────────────────────────────────────────────────

_CHALDEAN: dict[str, int] = {
    'A': 1, 'I': 1, 'J': 1, 'Q': 1, 'Y': 1,
    'B': 2, 'K': 2, 'R': 2,
    'C': 3, 'G': 3, 'L': 3, 'S': 3,
    'D': 4, 'M': 4, 'T': 4,
    'E': 5, 'H': 5, 'N': 5, 'X': 5,
    'O': 6, 'U': 6, 'V': 6, 'W': 6,
    'P': 7, 'Z': 7,
    'F': 8,
}

_VOWELS = frozenset("AEIOU")

_NUMBER_INFO: dict[int, dict] = {
    1:  {"planet": "Sun",     "lucky_day": "Sunday",    "lucky_color": "Gold / Orange",    "lucky_gemstone": "Ruby"},
    2:  {"planet": "Moon",    "lucky_day": "Monday",    "lucky_color": "White / Silver",   "lucky_gemstone": "Pearl"},
    3:  {"planet": "Jupiter", "lucky_day": "Thursday",  "lucky_color": "Yellow",           "lucky_gemstone": "Yellow Sapphire"},
    4:  {"planet": "Rahu",    "lucky_day": "Saturday",  "lucky_color": "Dark Blue",        "lucky_gemstone": "Hessonite (Gomed)"},
    5:  {"planet": "Mercury", "lucky_day": "Wednesday", "lucky_color": "Green",            "lucky_gemstone": "Emerald"},
    6:  {"planet": "Venus",   "lucky_day": "Friday",    "lucky_color": "White / Pink",     "lucky_gemstone": "Diamond"},
    7:  {"planet": "Ketu",    "lucky_day": "Tuesday",   "lucky_color": "Brown / Tan",      "lucky_gemstone": "Cat's Eye (Lehsunia)"},
    8:  {"planet": "Saturn",  "lucky_day": "Saturday",  "lucky_color": "Black / Dark Blue","lucky_gemstone": "Blue Sapphire"},
    9:  {"planet": "Mars",    "lucky_day": "Tuesday",   "lucky_color": "Red",              "lucky_gemstone": "Red Coral"},
    11: {"planet": "Sun / Moon (Master)",    "lucky_day": "Sunday",   "lucky_color": "Silver / Gold",  "lucky_gemstone": "Pearl / Ruby"},
    22: {"planet": "Moon / Saturn (Master)", "lucky_day": "Saturday", "lucky_color": "Dark Blue",      "lucky_gemstone": "Blue Sapphire"},
    33: {"planet": "Jupiter / Saturn (Master)", "lucky_day": "Thursday", "lucky_color": "Yellow / Black", "lucky_gemstone": "Yellow Sapphire"},
}

_NUMBER_MEANING: dict[int, str] = {
    1:  "Leadership, individuality, pioneering spirit, and ambition. You are a natural initiator who thrives when forging your own path.",
    2:  "Intuition, sensitivity, and cooperation. You excel in partnerships and have a deep emotional intelligence that draws others to you.",
    3:  "Creativity, self-expression, and optimism. You have a gift for communication and inspiring others with your natural enthusiasm and wisdom.",
    4:  "Discipline, hard work, and building solid foundations. Life asks you to work systematically — patience and persistence are your greatest tools.",
    5:  "Freedom, adaptability, and communication. You thrive on variety, travel, and intellectual stimulation — routine stifles your spirit.",
    6:  "Harmony, responsibility, and nurturing. Home, family, and relationships are your deepest sources of meaning and fulfilment.",
    7:  "Spirituality, introspection, and analytical depth. You are drawn to the mysteries of life and find truth through solitude and contemplation.",
    8:  "Power, material success, and karmic perseverance. You are built for achievement — the universe tests you before rewarding you greatly.",
    9:  "Compassion, completion, and universal service. Your path involves giving back, releasing the past, and serving something larger than yourself.",
    11: "Master Number — Illumination and inspiration. You carry heightened intuition and a calling toward spiritual leadership and visionary work.",
    22: "Master Number — The Master Builder. You have the rare ability to turn grand dreams into tangible reality through disciplined effort.",
    33: "Master Number — The Master Teacher. You are called to selfless service, spiritual guidance, and uplifting humanity through compassion and wisdom.",
}

_PERSONAL_YEAR_MEANING: dict[int, str] = {
    1: "A year of fresh starts and new beginnings. Plant seeds now — initiatives launched this year carry long-term momentum.",
    2: "A year of patience, cooperation, and relationships. Focus on partnerships rather than solo ambition.",
    3: "A year of creative expression, socialising, and joy. Opportunities come through self-expression and networking.",
    4: "A year of hard work and building foundations. Discipline and persistence are rewarded — focus on structure.",
    5: "A year of change, freedom, and unexpected opportunities. Stay adaptable — rigid plans will be disrupted.",
    6: "A year of home, family, and responsibility. Nurturing relationships and fulfilling obligations brings deep satisfaction.",
    7: "A year of reflection, spirituality, and inner growth. Step back from the external world — answers come from within.",
    8: "A year of achievement, ambition, and abundance. Material efforts are rewarded — step into your power.",
    9: "A year of completion, release, and humanitarianism. Let go of what no longer serves you — endings open new cycles.",
}


def _reduce_chaldean(n: int) -> int:
    """Reduce to single digit, preserving master numbers 11, 22, 33."""
    while n > 9:
        if n in (11, 22, 33):
            break
        n = sum(int(d) for d in str(n))
    return n


def _sum_digits(n: int) -> int:
    return sum(int(d) for d in str(n))


def _numerology_entry(value: int, label: str, extra: dict | None = None) -> dict:
    info = _NUMBER_INFO.get(value, _NUMBER_INFO.get(((value - 1) % 9) + 1, _NUMBER_INFO[1]))
    entry = {
        "value": value,
        "planet": info["planet"],
        "label": label,
        "meaning": _NUMBER_MEANING.get(value, ""),
        "lucky_day": info["lucky_day"],
        "lucky_color": info["lucky_color"],
        "lucky_gemstone": info["lucky_gemstone"],
    }
    if extra:
        entry.update(extra)
    return entry


def calc_numerology(name: str, dob_str: str, current_year: int) -> dict:
    """
    Calculate Chaldean numerology numbers from name and date of birth.

    Args:
        name: Full name (spaces/punctuation ignored; only alpha characters used).
        dob_str: Date of birth as 'YYYY-MM-DD'.
        current_year: Year to use for Personal Year calculation.
    """
    from datetime import date as _date
    dob = _date.fromisoformat(dob_str)

    # ── Moolank (Birth Number) ──────────────────────────────────────────────
    moolank_raw = _sum_digits(dob.day)
    moolank = _reduce_chaldean(moolank_raw)

    # ── Bhagyank (Destiny / Life Path) ──────────────────────────────────────
    bhagyank_raw = _sum_digits(dob.day) + _sum_digits(dob.month) + _sum_digits(dob.year)
    bhagyank = _reduce_chaldean(bhagyank_raw)

    # ── Personal Year ───────────────────────────────────────────────────────
    py_raw = _sum_digits(dob.day) + _sum_digits(dob.month) + _sum_digits(current_year)
    personal_year_val = _reduce_chaldean(py_raw)

    result: dict = {
        "moolank":     _numerology_entry(moolank, "Birth Number (Moolank)"),
        "bhagyank":    _numerology_entry(bhagyank, "Destiny Number (Bhagyank)"),
        "personal_year": {
            **_numerology_entry(personal_year_val, f"Personal Year {current_year}"),
            "year": current_year,
            "meaning": _PERSONAL_YEAR_MEANING.get(personal_year_val, ""),
        },
    }

    # ── Name-based numbers (optional — only if name provided) ──────────────
    alpha = [c.upper() for c in name if c.isalpha()] if name else []

    if alpha:
        # Namank (all letters)
        namank_raw = sum(_CHALDEAN.get(c, 0) for c in alpha)
        namank = _reduce_chaldean(namank_raw)

        # Soul Number (vowels)
        soul_raw = sum(_CHALDEAN.get(c, 0) for c in alpha if c in _VOWELS)
        soul = _reduce_chaldean(soul_raw) if soul_raw else None

        # Personality Number (consonants)
        pers_raw = sum(_CHALDEAN.get(c, 0) for c in alpha if c not in _VOWELS)
        personality = _reduce_chaldean(pers_raw) if pers_raw else None

        result["namank"] = _numerology_entry(namank, "Name Number (Namank)")
        if soul is not None:
            result["soul_number"] = _numerology_entry(soul, "Soul Number")
        if personality is not None:
            result["personality_number"] = _numerology_entry(personality, "Personality Number")
    else:
        result["namank"] = None
        result["soul_number"] = None
        result["personality_number"] = None

    return result


# ── Master builder ───────────────────────────────────────────────────────────

def build_chart(name: str, gender: str, dob: str, tob: str, lat: float, lon: float, place_name: str) -> dict:
    """Build the full chart_data dict for a Kundli."""
    jd = get_julian_day(dob, tob, lat, lon)
    position_data = calc_planet_positions(jd, lat, lon)
    planets = position_data["planets"]
    lagna = position_data["lagna"]

    moon_lon = planets["Moon"]["longitude"]
    nakshatra = calc_nakshatra(moon_lon)
    panchanga = calc_panchanga(jd)
    dasha = calc_vimshottari_dasha(moon_lon, dob)
    manglik = calc_manglik(planets, lagna["sign"])
    sadesati = calc_sadesati(planets["Moon"]["sign"])
    sun_sunset = calc_sunrise_sunset(jd, lat, lon)
    divisional = calc_divisional_charts(planets, lagna)
    antardasha = calc_antardasha(dasha["dashas"])
    shadbala = calc_shadbala(planets, lagna, jd, dob, tob, divisional, sun_sunset=sun_sunset)
    yogas = calc_yogas(planets, lagna)
    doshas = calc_doshas(planets, lagna)
    gochar = calc_gochar(planets, lagna, dasha)

    from datetime import date as _today
    current_year = _today.today().year
    numerology = calc_numerology(name, dob, current_year)

    # Ayanamsa value
    import swisseph as swe
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    ayanamsa = swe.get_ayanamsa_ut(jd)

    return {
        "name": name,
        "gender": gender,
        "dob": dob,
        "tob": tob,
        "lat": lat,
        "lon": lon,
        "place_name": place_name,
        "julian_day": round(jd, 5),
        "ayanamsa": round(ayanamsa, 4),
        "lagna": lagna,
        "planets": planets,
        "nakshatra": nakshatra,
        "panchanga": panchanga,
        "dasha": dasha,
        "manglik": manglik,
        "sadesati": sadesati,
        "sunrise": sun_sunset["sunrise"],
        "sunset": sun_sunset["sunset"],
        "divisional_charts": divisional,
        "antardasha": antardasha,
        "shadbala": shadbala,
        "yogas": yogas,
        "doshas": doshas,
        "gochar": gochar,
        "numerology": numerology,
    }
