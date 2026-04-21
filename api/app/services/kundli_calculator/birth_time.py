"""Birth time details — LMT, GMT, ishtkaal, sidereal time, weekday.

Computes the time-related fields shown on the Astrosage page-2
basic-details panel: day of birth, timezone offset, latitude/longitude
in DMS, LMT/GMT/local correction, ishtkaal (time from sunrise in
ghati-pala-vipala), and sidereal time at GMT.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone


def _hms(total_seconds: float) -> str:
    """Format a positive seconds count as HH:MM:SS."""
    s = int(round(total_seconds))
    return f"{s // 3600:02d}:{(s % 3600) // 60:02d}:{s % 60:02d}"


def _signed_hms(seconds: float) -> str:
    """Format a possibly-negative seconds count as ±HH:MM:SS."""
    sign = "-" if seconds < 0 else "+"
    return sign + _hms(abs(seconds))


def calc_birth_time_details(dob: str, tob: str, lat: float, lon: float, jd: float, sunrise_hm: str) -> dict:
    """Compute the time-related fields shown on the Astrosage page-2 basic-details panel.

    Returns weekday, time zone, latitude/longitude DMS strings, LMT/GMT/local
    correction, ishtkaal (time from sunrise in ghati-pala-vipala), and the
    sidereal time at GMT.
    """
    from timezonefinder import TimezoneFinder
    from zoneinfo import ZoneInfo
    import swisseph as swe

    tf = TimezoneFinder()
    tz_name = tf.timezone_at(lat=lat, lng=lon) or "UTC"
    tz = ZoneInfo(tz_name)

    birth_date = date.fromisoformat(dob)
    h, m = map(int, tob.split(":"))
    local_dt = datetime(birth_date.year, birth_date.month, birth_date.day, h, m, tzinfo=tz)
    utc_dt = local_dt.astimezone(timezone.utc)

    # Time zone offset in hours (e.g. 5.5 for IST)
    tz_offset_hours = local_dt.utcoffset().total_seconds() / 3600

    # Local Mean Time at the birth longitude (LMT) — UTC + (lon / 15) hours
    lmt_offset_seconds = lon / 15 * 3600
    lmt_dt = utc_dt + timedelta(seconds=lmt_offset_seconds)
    # Local time correction = LMT minus civil zone time at the same instant
    local_correction_seconds = lmt_offset_seconds - (tz_offset_hours * 3600)

    # Ishtkaal — time elapsed from local sunrise to birth, expressed in
    # ghati-pala-vipala (1 ghati = 24 min, 1 pala = 24 sec, 1 vipala = 0.4 sec).
    # Falls back to "—" when sunrise can't be computed (e.g. swisseph error).
    ishtkaal = "—"
    try:
        if sunrise_hm and sunrise_hm != "N/A" and ":" in sunrise_hm:
            parts = sunrise_hm.split(":")
            sr_h = int(parts[0])
            sr_m = int(parts[1])
            sr_s = int(parts[2]) if len(parts) > 2 else 0
            sunrise_seconds = sr_h * 3600 + sr_m * 60 + sr_s
            birth_seconds = h * 3600 + m * 60
            elapsed = birth_seconds - sunrise_seconds
            if elapsed < 0:
                elapsed += 86400  # birth before sunrise → previous day's count
            ghatis = int(elapsed // 1440)
            pala_remainder = elapsed - ghatis * 1440
            palas = int(pala_remainder // 24)
            vipalas = int(round((pala_remainder - palas * 24) / 0.4))
            ishtkaal = f"{ghatis:03d}-{palas:02d}-{vipalas:02d}"
    except (ValueError, IndexError):
        pass

    # Sidereal time at Greenwich for the birth instant (in hours)
    try:
        sidereal_hours = swe.sidtime(jd) % 24
        sidereal_str = _hms(sidereal_hours * 3600)
    except Exception:
        sidereal_str = "—"

    # Latitude and longitude as DMS strings
    def _dms(value: float, pos: str, neg: str) -> str:
        hemi = pos if value >= 0 else neg
        v = abs(value)
        deg = int(v)
        minutes = int((v - deg) * 60)
        return f"{deg:02d}:{minutes:02d}:{hemi}"

    return {
        "day_of_birth": local_dt.strftime("%A"),
        "tz_name": tz_name,
        "tz_offset_hours": round(tz_offset_hours, 2),
        "latitude_dms": _dms(lat, "N", "S"),
        "longitude_dms": _dms(lon, "E", "W"),
        "lmt_at_birth": _hms((lmt_dt.hour * 3600) + (lmt_dt.minute * 60) + lmt_dt.second),
        "gmt_at_birth": _hms((utc_dt.hour * 3600) + (utc_dt.minute * 60) + utc_dt.second),
        "local_time_correction": _signed_hms(local_correction_seconds),
        "ishtkaal": ishtkaal,
        "sidereal_time": sidereal_str,
    }
