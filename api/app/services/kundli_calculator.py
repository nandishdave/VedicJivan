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
    }
