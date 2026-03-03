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
    """Calculate divisional chart positions: D2, D3, D9, D10, D12, D60."""
    charts = {}
    for chart_type in ("D2", "D3", "D9", "D10", "D12", "D60"):
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
    }
