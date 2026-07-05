"""
Vedic astrology chart calculator using Swiss Ephemeris (pyswisseph).
All calculations use Lahiri Ayanamsa (sidereal mode) — same as AstroSage.
"""

from __future__ import annotations

import logging
from datetime import date, datetime, time, timedelta, timezone

logger = logging.getLogger(__name__)

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

# Karan names (11 karanas, each half-tithi). 7 movable + 4 fixed.
KARAN_NAMES = [
    "Bava", "Balava", "Kaulava", "Taitila", "Garija",
    "Vanija", "Vishti", "Shakuni", "Chatushpada", "Naga", "Kimstughna",
]
_MOVABLE_KARANAS = KARAN_NAMES[:7]


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
        "dignity": _get_dignity("Ketu", ketu_sign),
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
    """Return the Vedic dignity of a planet in a given sign (sign 0-11 zero-indexed).

    For Rahu/Ketu, uses the Parashara tradition: Rahu exalted in Gemini (debil.
    Sagittarius), Ketu exalted in Sagittarius (debil. Gemini). Own-sign follows
    the classical pairing — Rahu=Aquarius, Ketu=Scorpio.
    """
    if planet in ("Rahu", "Ketu", "Uranus", "Neptune", "Pluto"):
        exalt_lon_ext = _EXALTATION_EXT.get(planet)
        if exalt_lon_ext is not None:
            exalt_sign = int(exalt_lon_ext) // 30
            debil_sign = (exalt_sign + 6) % 12
            if sign == exalt_sign:
                return "Exalted"
            if sign == debil_sign:
                return "Debilitated"
        if sign in _OWN_SIGNS_EXT.get(planet, []):
            return "Own Sign"
        sign_lord = SIGN_LORDS[sign]
        if sign_lord in _PLANET_FRIENDS_EXT.get(planet, set()):
            return "Friendly Sign"
        if sign_lord in _PLANET_ENEMIES_EXT.get(planet, set()):
            return "Enemy Sign"
        return "Neutral Sign"

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
# Moved to .shadbala (calculation + Shadbala-specific constants) and .dignity
# (shared dignity tables used by yogas/friendship/avasthas). Re-imported here
# so anything outside the package that still reaches into `_core` for these
# names keeps working. `_get_dignity` above references `_EXALTATION_EXT` etc.
# — Python resolves those at call time, by which point these re-imports have
# populated `_core`'s namespace.
from .dignity import (  # noqa: E402,F401
    _COMPOUND_DIGNITY,
    _EXALTATION,
    _MOOLATRIKONA,
    _OWN_SIGNS,
    _PLANET_ENEMIES,
    _PLANET_FRIENDS,
    _compound_relationships,
)
from .shadbala import (  # noqa: E402,F401
    _BENEFIC_PAKSHA_EXT,
    _CLASSICAL_SWE_CODES,
    _DAY_PLANET_EXT,
    _DIG_STRONG_HOUSE,
    _DIG_STRONG_HOUSE_EXT,
    _EXALTATION_EXT,
    _MEAN_SPEED,
    _MEAN_SPEED_EXT,
    _MIN_SHADBALA,
    _MIN_SHADBALA_EXT,
    _NAISARGEKA,
    _NAISARGEKA_EXT,
    _NIGHT_PLANET_EXT,
    _OWN_SIGNS_EXT,
    _PLANET_ENEMIES_EXT,
    _PLANET_FRIENDS_EXT,
    _WEEKDAY_PLANETS,
    _dignity_points,
    _drik_bala,
    _graha_drishti,
    _parse_hm,
    calc_shadbala,
)


# ── Nakshatra ────────────────────────────────────────────────────────────────
# Moved to .nakshatra — re-imported here so the legacy module surface is preserved.
from .nakshatra import calc_nakshatra  # noqa: E402,F401


# ── Panchanga (Tithi, Yoga, Karan) ──────────────────────────────────────────
# Moved to .panchanga — re-imported here.
from .panchanga import calc_panchanga  # noqa: E402,F401


# ── Vimshottari Dasha ────────────────────────────────────────────────────────
# Moved to .vimshottari — re-imported here. Includes _add_years +
# _birth_datetime helpers (used by sadesati and other dasha sections) and
# _VIMSHOTTARI_DAYS_PER_YEAR (re-exported via __init__.py for tests).
from .vimshottari import (  # noqa: E402,F401
    _VIMSHOTTARI_DAYS_PER_YEAR,
    _add_years,
    _birth_datetime,
    calc_vimshottari_dasha,
)


# ── Manglik Dosha ────────────────────────────────────────────────────────────
# Moved to .manglik — re-imported here.
from .manglik import calc_manglik  # noqa: E402,F401


# ── Sade Sati ────────────────────────────────────────────────────────────────
# Moved to .sadesati — re-imported here. _compute_saturn_transits and
# _collapse_retrograde_transits are kept on the legacy surface in case any
# tests patch them directly.
from .sadesati import (  # noqa: E402,F401
    _collapse_retrograde_transits,
    _compute_saturn_transits,
    calc_sadesati,
)


# ── Divisional Charts (Vargas) ────────────────────────────────────────────────

# Moved to .divisional — re-imported here. _calc_varga_sign is reused by
# the Jaimini Karakamsa calculation below.
from .divisional import _calc_varga_sign, calc_divisional_charts  # noqa: E402,F401


# ── Antardasha (Sub-periods) ─────────────────────────────────────────────────
# Moved to .antardasha — re-imported here.
from .antardasha import calc_antardasha, calc_pratyantar  # noqa: E402,F401


# ── Sunrise / Sunset ─────────────────────────────────────────────────────────
# Moved to .sunrise — re-exported here.
from .sunrise import calc_sunrise_sunset, _get_local_tz  # noqa: E402,F401


# ── Yoga Detection ───────────────────────────────────────────────────────────

# Moved to .yogas — re-imported here.
from .yogas import calc_yogas  # noqa: E402,F401


# ── Dosha Detection ──────────────────────────────────────────────────────────

# Moved to .doshas — re-imported here.
from .doshas import calc_doshas  # noqa: E402,F401


# ── Gochar (Transits) ─────────────────────────────────────────────────────────
# Moved to .gochar — re-imported here.
from .gochar import calc_gochar  # noqa: E402,F401


# ── Numerology ────────────────────────────────────────────────────────────────
# Moved to .numerology — re-exported here to preserve the legacy module surface.
from .numerology import (  # noqa: E402,F401
    calc_numerology,
    _numerology_entry,
    _reduce_chaldean,
    _sum_digits,
)


# ── Yogini Dasha (36-year cycle, 8 yoginis) ─────────────────────────────────
# Moved to .yogini — re-imported here. Constants (YOGINI_NAMES, YOGINI_YEARS,
# YOGINI_ABBR, YOGINI_PLANETS) are public surface used by tests.
from .yogini import (  # noqa: E402,F401
    YOGINI_ABBR,
    YOGINI_NAMES,
    YOGINI_PLANETS,
    YOGINI_YEARS,
    calc_yogini_dasha,
)


# ── Vedic Graha Drishti + Western Aspects ──────────────────────────────────
# Moved to .aspects — re-exported here.
from .aspects import (  # noqa: E402,F401
    WESTERN_ASPECTS,
    calc_graha_drishti,
    calc_western_aspects,
)


# ── Friendship Tables (Naisargika + Tatkalika + Panchadha) ─────────────────
# Moved to .friendship — re-imported here. _CLASSICAL_PLANETS stays on the
# legacy surface for any code that imports it.
from .friendship import _CLASSICAL_PLANETS, calc_friendships  # noqa: E402,F401


# ── Avkahada Chakra (traditional Vedic chart attributes) ───────────────────
# Moved to .avkahada — re-imported here. All constants stay public.
from .avkahada import (  # noqa: E402,F401
    NAKSHATRA_GANA,
    NAKSHATRA_NADI,
    NAKSHATRA_PAYA,
    NAKSHATRA_YONI,
    RASHI_TATVA,
    RASHI_VARNA,
    RASHI_VASYA,
    SIGN_NAMES_EN,
    calc_avkahada,
)


# ── Birth time details (LMT, GMT, ishtkaal, sidereal time, weekday) ────────
# Moved to .birth_time — re-imported here.
from .birth_time import calc_birth_time_details  # noqa: E402,F401


# ── Ashtakavarga ─────────────────────────────────────────────────────────────
# Moved to .ashtakavarga — re-imported here.
from .ashtakavarga import ASHTAKAVARGA_RULES, calc_ashtakavarga  # noqa: E402,F401


# ── Avasthas — Baladi / Jagradadi / Deeptadi planet-state classification ───
# Moved to .avasthas — re-imported here. Underscore-prefixed _calc_baladi and
# _calc_jagradadi are part of the package surface (re-exported via __init__.py
# for tests).
from .avasthas import (  # noqa: E402,F401
    _calc_baladi,
    _calc_deeptadi,
    _calc_jagradadi,
    calc_avasthas,
)


# ── Jaimini System — Chara Karakas + Karakamsa ─────────────────────────────
# Moved to .jaimini — re-imported here.
from .jaimini import (  # noqa: E402,F401
    JAIMINI_CHARA_ROLES,
    JAIMINI_STHIRA_KARAKAS,
    calc_jaimini_karakas,
)


# ── Lal Kitab Dasha ─────────────────────────────────────────────────────────
# Moved to .lal_kitab — re-imported here. Constants are public surface.
from .lal_kitab import (  # noqa: E402,F401
    LAL_KITAB_DASHA_SEQUENCE,
    LAL_KITAB_DASHA_YEARS,
    LAL_KITAB_SUBPERIODS,
    calc_lal_kitab_dasha,
)


# ── Jaimini Chara Dasha ─────────────────────────────────────────────────────
# Moved to .jaimini_chara — re-imported here. Underscore-prefixed names
# (_JAIMINI_SIGN_LORDS, _JAIMINI_SIGN_TYPES, _char_dasha_years) are
# re-imported in case any tests patch them.
from .jaimini_chara import (  # noqa: E402,F401
    _JAIMINI_SIGN_LORDS,
    _JAIMINI_SIGN_TYPES,
    _char_dasha_years,
    calc_char_dasha,
)


# ── Varshaphal (Tajik / Annual Horoscope) ───────────────────────────────────
# Moved to .varshaphal — re-imported here. calc_muntha and calc_mudda_dasha
# are part of the public surface (tests import them directly).
from .varshaphal import (  # noqa: E402,F401
    calc_mudda_dasha,
    calc_muntha,
    calc_solar_return_jd,
    calc_varshaphal,
)


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
    dasha = calc_vimshottari_dasha(moon_lon, dob, tob=tob)
    manglik = calc_manglik(planets, lagna["sign"])
    sadesati = calc_sadesati(planets["Moon"]["sign"], dob=dob)
    sun_sunset = calc_sunrise_sunset(jd, lat, lon)
    avkahada = calc_avkahada(nakshatra["num"], planets["Moon"]["sign"])
    birth_time = calc_birth_time_details(dob, tob, lat, lon, jd, sun_sunset["sunrise"])
    friendships = calc_friendships(planets)
    western_aspects = calc_western_aspects(planets)
    graha_drishti = calc_graha_drishti(planets, lagna)
    yogini_dasha = calc_yogini_dasha(moon_lon, dob, tob=tob)
    divisional = calc_divisional_charts(planets, lagna)
    antardasha = calc_antardasha(dasha["dashas"], dob=dob, tob=tob)
    current_md_planet = dasha["current_dasha"]["planet"]
    pratyantar = calc_pratyantar(antardasha, current_md_planet=current_md_planet)
    shadbala = calc_shadbala(planets, lagna, jd, dob, tob, divisional, sun_sunset=sun_sunset)
    yogas = calc_yogas(planets, lagna)
    doshas = calc_doshas(planets, lagna)
    gochar = calc_gochar(planets, lagna, dasha)

    from datetime import date as _today
    current_year = _today.today().year
    numerology = calc_numerology(name, dob, current_year)
    ashtakavarga = calc_ashtakavarga(planets, lagna["sign"])
    # KP (Krishnamurti Paddhati) sub-lords + Placidus cusps (its own ayanamsa).
    from .kp import calc_kp, placidus_cusps
    try:
        kp_cusps = placidus_cusps(jd, lat, lon)
    except Exception:
        logger.warning(
            "Placidus cusp calculation failed (jd=%s, lat=%s, lon=%s); "
            "KP sub-lords will fall back to sign-based cusps.",
            jd, lat, lon, exc_info=True,
        )
        kp_cusps = None
    kp = calc_kp(planets, kp_cusps, lagna["longitude"], moon_lon)
    jaimini = calc_jaimini_karakas(planets, lagna)
    jaimini["avasthas"] = calc_avasthas(planets, graha_drishti=graha_drishti, shadbala=shadbala)
    char_dasha = calc_char_dasha(planets, lagna, dob, tob=tob)
    lal_kitab_dasha = calc_lal_kitab_dasha(dob, tob=tob)
    # Build BOTH the current Varshaphal year and the upcoming one. Whether
    # `current_year`'s solar return has already happened decides which calendar
    # year anchors each: if SR for `current_year` is in the past, current
    # Varshaphal = current_year; if it's still in the future, current
    # Varshaphal actually started at last year's SR.
    varshaphal: list[dict] = []
    try:
        sr_jd_this = calc_solar_return_jd(planets["Sun"]["longitude"], current_year)
        import swisseph as _swe
        _y, _m, _d_, _ = _swe.revjul(sr_jd_this)
        sr_date_this = date(int(_y), int(_m), int(_d_))
        today = date.today()
        if sr_date_this <= today:
            current_target, upcoming_target = current_year, current_year + 1
        else:
            current_target, upcoming_target = current_year - 1, current_year
        for label, yr in (("current", current_target), ("upcoming", upcoming_target)):
            try:
                v = calc_varshaphal(
                    natal_sun_lon=planets["Sun"]["longitude"],
                    natal_lagna_sign=lagna["sign"],
                    dob=dob,
                    lat=lat,
                    lon=lon,
                    target_year=yr,
                )
                v["label"] = label
                varshaphal.append(v)
            except Exception:
                logger.warning(
                    "Varshaphal build failed for %s year %s; omitting that annual chart.",
                    label, yr, exc_info=True,
                )
    except Exception:
        logger.warning(
            "Varshaphal solar-return anchor failed for year %s; "
            "no annual charts will be produced.",
            current_year, exc_info=True,
        )
        varshaphal = []

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
        "avkahada": avkahada,
        "birth_time": birth_time,
        "friendships": friendships,
        "western_aspects": western_aspects,
        "graha_drishti": graha_drishti,
        "yogini_dasha": yogini_dasha,
        "divisional_charts": divisional,
        "antardasha": antardasha,
        "pratyantar": pratyantar,
        "shadbala": shadbala,
        "yogas": yogas,
        "doshas": doshas,
        "gochar": gochar,
        "numerology": numerology,
        "ashtakavarga": ashtakavarga,
        "kp": kp,
        "jaimini": jaimini,
        "char_dasha": char_dasha,
        "lal_kitab_dasha": lal_kitab_dasha,
        "varshaphal": varshaphal,
    }
