"""Varshaphal (Tajik / annual horoscope) — solar return chart + Mudda Dasha.

Computes the exact solar-return moment (sidereal Sun returns to natal
longitude), Muntha (advances one sign per year of age), and Mudda
Dasha (Vimshottari pattern compressed into a single tropical year).

Threading the solar-return DATETIME (not just date) through Mudda
Dasha keeps sub-day precision in the SR moment.
"""

from __future__ import annotations

from datetime import date, datetime, time, timedelta

from ._core import (
    DASHA_SEQUENCE,
    DASHA_YEARS,
    NAKSHATRA_LORDS,
    SIGN_LORDS,
    SIGN_NAMES,
    calc_planet_positions,
)
from .vimshottari import _VIMSHOTTARI_DAYS_PER_YEAR


def calc_solar_return_jd(natal_sun_lon: float, target_year: int) -> float:
    """Find the Julian Day (UT) when the Sun returns to its natal sidereal
    longitude in `target_year`. Uses Swiss Ephemeris with binary refinement to
    minute-level precision.
    """
    import swisseph as swe
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags = swe.FLG_SIDEREAL

    def sun_lon(jd: float) -> float:
        pos, _ = swe.calc_ut(jd, swe.SUN, flags)
        return pos[0] % 360

    # Sun moves ~1°/day. Walk daily through target_year until we cross natal_sun_lon.
    # diff_signed = (sun_lon - natal_sun_lon + 180) % 360 - 180  → range (-180, 180]
    jd = swe.julday(target_year, 1, 1, 0)
    end_jd = swe.julday(target_year + 1, 1, 31, 0)
    prev_signed = (sun_lon(jd) - natal_sun_lon + 180) % 360 - 180
    while jd < end_jd:
        jd += 1
        cur_signed = (sun_lon(jd) - natal_sun_lon + 180) % 360 - 180
        # Crossing happens when prev was negative and current became positive (Sun passed natal lon).
        if prev_signed < 0 and cur_signed >= 0:
            break
        prev_signed = cur_signed

    # Binary-refine to ~1 minute precision.
    lo, hi = jd - 1, jd
    while (hi - lo) > 1.0 / 1440.0:
        mid = (lo + hi) / 2.0
        mid_signed = (sun_lon(mid) - natal_sun_lon + 180) % 360 - 180
        if mid_signed < 0:
            lo = mid
        else:
            hi = mid
    return hi


def calc_muntha(natal_lagna_sign: int, age_years: int) -> dict:
    """Muntha advances one sign per completed year of age, starting from the
    natal Lagna sign at age 0. Returns sign (0–11), house number (1–12) from
    the natal Lagna and the sign name.
    """
    sign = (natal_lagna_sign + age_years) % 12
    house = (age_years % 12) + 1
    return {
        "sign": sign,
        "sign_name": SIGN_NAMES[sign],
        "house": house,
    }


def calc_mudda_dasha(annual_moon_lon: float, solar_return_dt: datetime | date) -> dict:
    """Compute the Mudda (annual) Dasha sequence — Vimshottari pattern scaled
    so the full 120-year cycle compresses into a single tropical year.

    Accepts either a `datetime` (preferred — preserves solar-return time of
    day for sub-day precision) or a `date` (treated as midnight) for the
    solar-return moment.

    Sequence starts from the lord of the Moon's nakshatra at solar return.
    The first period is partial (the *balance* of the starting lord based on
    the Moon's position inside its nakshatra), then subsequent periods run
    their full Mudda durations. Because the first period is partial, the 9-
    planet cycle is short by exactly the elapsed portion — so the cycle wraps
    around at the end, with the starting lord resuming for the remainder
    until the full ~365 days are filled. Result is one complete year of
    sub-periods with no gap.
    """
    if isinstance(solar_return_dt, datetime):
        sr_dt = solar_return_dt
    else:
        sr_dt = datetime.combine(solar_return_dt, time(0))

    nak_size = 360.0 / 27.0
    nak_num = int(annual_moon_lon / nak_size)
    fraction_elapsed = (annual_moon_lon % nak_size) / nak_size

    lord = NAKSHATRA_LORDS[nak_num]
    lord_idx = DASHA_SEQUENCE.index(lord)
    cycle_days = _VIMSHOTTARI_DAYS_PER_YEAR

    full_days = {p: (DASHA_YEARS[p] / 120.0) * cycle_days for p in DASHA_SEQUENCE}

    periods: list[dict] = []
    cumulative_days = 0.0
    i = 0
    while cumulative_days < cycle_days - 0.5:
        planet = DASHA_SEQUENCE[(lord_idx + i) % 9]
        if i == 0:
            period_days = full_days[planet] * (1 - fraction_elapsed)
        else:
            period_days = full_days[planet]
        remaining = cycle_days - cumulative_days
        period_days = min(period_days, remaining)

        start_dt = sr_dt + timedelta(days=cumulative_days)
        cumulative_days += period_days
        end_dt = sr_dt + timedelta(days=cumulative_days)
        periods.append({
            "planet": planet,
            "start_date": start_dt.date().isoformat(),
            "end_date": end_dt.date().isoformat(),
            "days": int(round(period_days)),
        })
        i += 1

    today = date.today()
    current = next(
        (p for p in periods if p["start_date"] <= today.isoformat() <= p["end_date"]),
        periods[0],
    )
    return {"periods": periods, "current": current}


def calc_varshaphal(
    natal_sun_lon: float,
    natal_lagna_sign: int,
    dob: str,
    lat: float,
    lon: float,
    target_year: int,
) -> dict:
    """Build the Varshaphal (annual chart) bundle for a given solar year.

    Includes solar return moment, the annual chart (planets + lagna at solar
    return cast for the birthplace), Muntha's sign/house, and the Mudda Dasha
    sequence for the year.
    """
    sr_jd = calc_solar_return_jd(natal_sun_lon, target_year)

    # Solar return civil date — UT to local using birth coordinates.
    from timezonefinder import TimezoneFinder
    from zoneinfo import ZoneInfo
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lat=lat, lng=lon) or "UTC"
    tz = ZoneInfo(tz_name)

    import swisseph as swe
    y, m, d_, h = swe.revjul(sr_jd)
    sr_dt_utc = datetime(int(y), int(m), int(d_), int(h), int((h - int(h)) * 60))
    sr_dt_utc = sr_dt_utc.replace(tzinfo=ZoneInfo("UTC"))
    sr_local = sr_dt_utc.astimezone(tz)
    solar_return_date = sr_local.date()

    annual = calc_planet_positions(sr_jd, lat, lon)
    annual_lagna = annual["lagna"]
    annual_planets = annual["planets"]

    birth_year = int(dob.split("-")[0])
    age_years = target_year - birth_year
    muntha = calc_muntha(natal_lagna_sign, age_years)
    # Muntha's lord (sign lord) — used for general muntha-effect interpretation.
    muntha["lord"] = SIGN_LORDS[muntha["sign"]]

    # Pass the precise local solar-return datetime (not just date) so the
    # Mudda Dasha sequence inherits sub-day precision from the SR moment.
    mudda = calc_mudda_dasha(annual_planets["Moon"]["longitude"], sr_local.replace(tzinfo=None))

    return {
        "target_year": target_year,
        "age_years": age_years,
        "solar_return_date": solar_return_date.isoformat(),
        "solar_return_local_time": sr_local.strftime("%H:%M:%S"),
        "annual_lagna": annual_lagna,
        "annual_planets": annual_planets,
        "muntha": muntha,
        "mudda_dasha": mudda,
    }
