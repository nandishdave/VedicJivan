"""Sunrise / sunset for a given Julian Day at a given location.

Self-contained — only depends on swisseph, timezonefinder, and stdlib.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


def _get_local_tz(lat: float, lon: float):
    """Get ZoneInfo timezone for given coordinates."""
    from timezonefinder import TimezoneFinder
    from zoneinfo import ZoneInfo
    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lat=lat, lng=lon) or "UTC"
    return ZoneInfo(tz_name)


def calc_sunrise_sunset(jd: float, lat: float, lon: float) -> dict:
    """Calculate sunrise and sunset times for the birth date (local time).

    Uses the modern pyswisseph rise_trans signature (tjd, body, rsmi, geopos).
    The previous code passed the legacy 8-argument form which silently raised
    on pyswisseph 2.10+, leaving sunrise as N/A in production.
    """
    import swisseph as swe
    try:
        geopos = (lon, lat, 0)  # (longitude, latitude, altitude)
        sr_ret = swe.rise_trans(jd - 1, swe.SUN, swe.CALC_RISE, geopos)
        ss_ret = swe.rise_trans(jd - 1, swe.SUN, swe.CALC_SET, geopos)
        sr_jd = sr_ret[1][0] if isinstance(sr_ret, tuple) and len(sr_ret) > 1 else sr_ret
        ss_jd = ss_ret[1][0] if isinstance(ss_ret, tuple) and len(ss_ret) > 1 else ss_ret

        local_tz = _get_local_tz(lat, lon)

        def jd_to_local_hms(j):
            """Convert Julian Day (UT) to local HH:MM:SS string."""
            # JD epoch is noon UT on Jan 1, 4713 BC; +0.5 puts midnight UT at integer.
            # We don't need the exact date here — just the time-of-day — because
            # rise/set always lands on the requested civil date.
            jd_int = int(j + 0.5)
            frac = (j + 0.5) - jd_int
            total_seconds = round(frac * 86400)
            h, rem = divmod(total_seconds, 3600)
            mi, s = divmod(rem, 60)
            utc_dt = datetime(2000, 1, 1, h % 24, mi, s, tzinfo=timezone.utc)
            local_dt = utc_dt.astimezone(local_tz)
            return f"{local_dt.hour:02d}:{local_dt.minute:02d}:{local_dt.second:02d}"

        return {"sunrise": jd_to_local_hms(sr_jd), "sunset": jd_to_local_hms(ss_jd)}
    except Exception:
        logger.warning(
            "Sunrise/sunset calculation failed (jd=%s, lat=%s, lon=%s); "
            "returning N/A — check pyswisseph rise_trans signature/ephemeris.",
            jd, lat, lon, exc_info=True,
        )
        return {"sunrise": "N/A", "sunset": "N/A"}
