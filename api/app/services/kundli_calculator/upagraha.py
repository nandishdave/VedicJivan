"""Upagrahas (sub-planets / shadow points).

Two families:
  * Kāya group (5) — fixed offsets from the Sun. Exact, purely longitudinal:
      Dhūma = Sun + 133°20′;  Vyatīpāta = 360 − Dhūma;  Parivesha = Vyatīpāta + 180;
      Indrachāpa = 360 − Parivesha;  Upaketu = Indrachāpa + 16°40′ (= Sun − 30°).
  * Kāla group (6) — the classical Parāśara "Kālavelā" method: the day (sunrise→
    sunset) or night (sunset→next sunrise) is split into 8 equal parts; the first
    seven belong to the seven grahas in weekday order (the 8th is void). Each
    upagraha is the *Ascendant rising at the start of its ruling planet's part*:
      Gulika ← Saturn (start),  Kāla ← Sun,  Mṛtyu ← Mars,
      Yamaghaṇṭaka ← Jupiter,  Arthaprahāra ← Mercury.
    Māndi = the Ascendant at the *middle* of Saturn's part (the classical
    Gulika/Māndi split is murky; mid-part keeps Māndi distinct from both Gulika
    and Kāla and happens to match Astrosage's Māndi on day charts).

Verified against Astrosage: the 5 Kāya + Gulika match to the arc-second on both a
day chart and a night chart. NOTE: Astrosage's 4 "sons" (Kāla/Mṛtyu/Arthaprahāra/
Yamaghaṇṭaka) and Māndi sit ~1.5 parts later than the classical rule by a
convention that isn't reproducible without its definition; we follow the
documented Parāśara method (see ReadMe/experiment-ledger / scratchpad diagnostics).
"""

from __future__ import annotations

from datetime import date

# Weekday → graha order (Python weekday(): Mon=0 … Sun=6; +1 mod 7 → this list).
_WD_PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

# Night parts commence from the graha this many places (weekday order) after the
# day-lord. Validated against Astrosage's Gulika on a Tuesday-night chart (Moon
# leads → Saturn lands in part 6, matching Gulika to 0.2′).
_NIGHT_OFFSET = 6

_SIGN_ABBR = ["Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]
_NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu",
    "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta",
    "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
    "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati",
]

# Display order matches Astrosage's Upagraha table.
_UPAGRAHA_ORDER = [
    "Dhuma", "Vyatipata", "Parivesha", "Indrachapa", "Upaketu",
    "Kaala", "Mrityu", "Arthaprahara", "Yamaghantaka", "Mandi", "Gulika",
]
_UPAGRAHA_LABEL = {
    "Dhuma": "Dhūma", "Vyatipata": "Vyatīpāta", "Parivesha": "Parivesha",
    "Indrachapa": "Indrachāpa", "Upaketu": "Upaketu", "Kaala": "Kāla",
    "Mrityu": "Mṛtyu", "Arthaprahara": "Arthaprahāra", "Yamaghantaka": "Yamaghaṇṭaka",
    "Mandi": "Māndi", "Gulika": "Gulika",
}
# Two-letter chart glyphs (Astrosage convention).
_UPAGRAHA_ABBR = {
    "Dhuma": "Dh", "Vyatipata": "Vp", "Parivesha": "Pv", "Indrachapa": "Ic",
    "Upaketu": "Uk", "Kaala": "Kl", "Mrityu": "Mr", "Arthaprahara": "Ap",
    "Yamaghantaka": "Yg", "Mandi": "Md", "Gulika": "Gk",
}


def _kaya_group(sun_lon: float) -> dict:
    """The 5 Sun-derived upagrahas (longitudes in 0–360)."""
    dhuma = (sun_lon + 133 + 20 / 60) % 360
    vyatipata = (360 - dhuma) % 360
    parivesha = (vyatipata + 180) % 360
    indrachapa = (360 - parivesha) % 360
    upaketu = (indrachapa + 16 + 40 / 60) % 360
    return {
        "Dhuma": dhuma, "Vyatipata": vyatipata, "Parivesha": parivesha,
        "Indrachapa": indrachapa, "Upaketu": upaketu,
    }


def _ascendant(jd: float, lat: float, lon: float) -> float:
    """Sidereal (Lahiri) Ascendant longitude at a Julian Day."""
    import swisseph as swe
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    _cusps, ascmc = swe.houses_ex(jd, lat, lon, b"W", swe.FLG_SIDEREAL)
    return ascmc[0] % 360


def _day_or_night_span(jd: float, lat: float, lon: float):
    """Return (start_jd, end_jd, is_day) — the day (sunrise→sunset) if the birth
    is between them, else the night (sunset→next sunrise) bracketing the birth."""
    import swisseph as swe
    geo = (lon, lat, 0)
    sr = swe.rise_trans(jd - 1, swe.SUN, swe.CALC_RISE, geo)[1][0]
    ss = swe.rise_trans(sr, swe.SUN, swe.CALC_SET, geo)[1][0]
    if sr <= jd <= ss:
        return sr, ss, True
    if jd > ss:  # born after sunset — night runs to the next sunrise
        return ss, swe.rise_trans(ss, swe.SUN, swe.CALC_RISE, geo)[1][0], False
    # born before sunrise — night runs from the previous sunset
    prev_ss = swe.rise_trans(sr - 1, swe.SUN, swe.CALC_SET, geo)[1][0]
    return prev_ss, sr, False


def _kala_group(jd: float, dob: str, lat: float, lon: float) -> dict:
    """The 6 time-based upagrahas (classical Parāśara Kālavelā method)."""
    start, end, is_day = _day_or_night_span(jd, lat, lon)
    portion = (end - start) / 8.0
    day_lord_idx = (date.fromisoformat(dob).weekday() + 1) % 7
    first = day_lord_idx if is_day else (day_lord_idx + _NIGHT_OFFSET) % 7
    # graha → its part index (0–6); 8th part is void.
    part_of = {_WD_PLANETS[(first + k) % 7]: k for k in range(7)}

    def asc_at(planet: str, frac: float) -> float:
        return _ascendant(start + (part_of[planet] + frac) * portion, lat, lon)

    return {
        "Gulika": asc_at("Saturn", 0.0),
        "Mandi": asc_at("Saturn", 0.5),
        "Kaala": asc_at("Sun", 0.0),
        "Mrityu": asc_at("Mars", 0.0),
        "Yamaghantaka": asc_at("Jupiter", 0.0),
        "Arthaprahara": asc_at("Mercury", 0.0),
    }


def calc_upagrahas(jd: float, dob: str, lat: float, lon: float, sun_lon: float) -> dict:
    """All 11 upagraha longitudes (0–360), keyed by canonical name."""
    return {**_kaya_group(sun_lon), **_kala_group(jd, dob, lat, lon)}


def _row(name: str, lon: float) -> dict:
    lon %= 360
    sign = int(lon // 30)
    deg = lon - sign * 30
    d = int(deg)
    m = int((deg - d) * 60)
    s = round((((deg - d) * 60) - m) * 60)
    if s == 60:
        s, m = 0, m + 1
    if m == 60:
        m, d = 0, d + 1
    nak = int(lon // (360 / 27)) % 27
    pada = int((lon % (360 / 27)) // (360 / 108)) + 1
    return {
        "name": name,
        "label": _UPAGRAHA_LABEL[name],
        "abbr": _UPAGRAHA_ABBR[name],
        "sign": sign,
        "sign_abbr": _SIGN_ABBR[sign],
        "degree": round(deg, 4),
        "dms": f"{d:02d}°{m:02d}′{s:02d}″",
        "nakshatra": _NAKSHATRAS[nak],
        "pada": pada,
    }


def upagraha_table(jd: float, dob: str, lat: float, lon: float,
                   sun_lon: float, lagna_sign: int) -> dict:
    """Display helper for the Upagraha calculator: one row per upagraha (in
    Astrosage's order) with sign / DMS longitude / nakshatra / pada, plus the
    per-sign grouping the North-Indian chart needs and the lagna sign."""
    ups = calc_upagrahas(jd, dob, lat, lon, sun_lon)
    rows = [_row(n, ups[n]) for n in _UPAGRAHA_ORDER]
    by_sign: dict[str, list[str]] = {}
    for r in rows:
        by_sign.setdefault(str(r["sign"]), []).append(r["abbr"])
    return {"upagrahas": rows, "by_sign": by_sign, "lagna_sign": lagna_sign}
