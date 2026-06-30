"""Auspicious Birth-Time (Muhurta) engine.

For a given date + place, the planets are essentially fixed across the day; only
the rising ascendant (Lagna) rotates through all 12 signs (~2h each). This module
finds each sign's rising window and, for each candidate Lagna, scores the overall
chart strength and a per-life-aspect verdict using the SAME real calculators the
Kundli report uses (Swiss Ephemeris via ``build_chart`` -> Ashtakavarga, Shadbala,
dignity, graha-drishti). No value here is invented by an LLM.

Scoring weights/thresholds below are deliberate but tunable judgment calls; they
are documented in ``.local/uncertainty_log.md`` and should be revisited with
sourced rules. The numeric *inputs* (bindus, shadbala, dignity, houses) are exact.
"""
from __future__ import annotations

from app.services.kundli_calculator._core import (
    SIGN_LORDS,
    SIGN_NAMES,
    calc_planet_positions,
    get_julian_day,
)
from app.services.kundli_calculator.aspects import calc_graha_drishti
from app.services.kundli_calculator.ashtakavarga import calc_ashtakavarga
from app.services.kundli_calculator.divisional import calc_divisional_charts
from app.services.kundli_calculator.nakshatra import calc_nakshatra
from app.services.kundli_calculator.panchanga import calc_panchanga
from app.services.kundli_calculator.shadbala import calc_shadbala
from app.services.kundli_calculator.sunrise import calc_sunrise_sunset


def build_muhurta_chart(*, dob: str, tob: str, lat: float, lon: float, sun_sunset: dict | None = None) -> dict:
    """Lighter chart for muhurta scoring — only what a strength scan needs.

    Computes positions + Whole-Sign houses, Ashtakavarga, Shadbala (which itself
    uses the D2/D3/D7/D9/D12/D30 vargas), graha-drishti and panchanga. Skips the
    dashas, KP, Jaimini, yogas/doshas, gochar, varshaphal and numerology that the
    full Kundli report needs but birth-muhurta ranking does not — several times
    faster than the full ``build_chart``.
    """
    jd = get_julian_day(dob, tob, lat, lon)
    pos = calc_planet_positions(jd, lat, lon)
    planets, lagna = pos["planets"], pos["lagna"]
    # Sunrise/sunset is a date+place property (same for every window), so the
    # caller can compute it once and pass it in to avoid 12x rise_trans.
    if sun_sunset is None:
        sun_sunset = calc_sunrise_sunset(jd, lat, lon)
    divisional = calc_divisional_charts(planets, lagna)
    return {
        "lagna": lagna,
        "planets": planets,
        "nakshatra": calc_nakshatra(planets["Moon"]["longitude"]),
        "panchanga": calc_panchanga(jd),
        "graha_drishti": calc_graha_drishti(planets, lagna),
        "shadbala": calc_shadbala(planets, lagna, jd, dob, tob, divisional, sun_sunset=sun_sunset),
        "ashtakavarga": calc_ashtakavarga(planets, lagna["sign"]),
        "sunrise": sun_sunset["sunrise"],
        "sunset": sun_sunset["sunset"],
    }

# ── Life aspects → (label, group, houses[primary first], karaka planets) ──────
# Houses follow the consultation cheat-sheet mapping. Primary house is weighted
# most; karaka strength (Shadbala) is a secondary modifier.
LIFE_ASPECTS: list[tuple[str, str, str, list[int], list[str]]] = [
    ("health",    "Health & Vitality",     "Self & Body",    [1, 6, 8],  ["Sun"]),
    ("longevity", "Longevity",             "Self & Body",    [8, 1, 3],  ["Saturn"]),
    ("wealth",    "Wealth & Finances",     "Material",       [2, 11],    ["Jupiter"]),
    ("career",    "Career & Status",       "Material",       [10, 6],    ["Sun", "Saturn"]),
    ("property",  "Property & Comforts",   "Material",       [4],        ["Mars", "Venus"]),
    ("marriage",  "Marriage & Spouse",     "Relationships",  [7],        ["Venus"]),
    ("children",  "Children & Progeny",    "Relationships",  [5],        ["Jupiter"]),
    ("family",    "Family Harmony",        "Relationships",  [4, 2],     ["Moon", "Venus"]),
    ("education", "Education & Intellect",  "Mind & Growth",  [4, 5, 9],  ["Mercury", "Jupiter"]),
    ("fortune",   "Fortune & Dharma",      "Mind & Growth",  [9],        ["Jupiter", "Sun"]),
    ("foreign",   "Foreign & Travel",      "Beyond",         [12, 9, 3], ["Rahu"]),
    ("spiritual", "Spirituality",          "Beyond",         [12, 9, 5], ["Ketu", "Jupiter"]),
]

_CLASSICAL = ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu")
_BENEFICS = {"Jupiter", "Venus", "Mercury"}
_MALEFICS = {"Saturn", "Mars", "Sun", "Rahu", "Ketu"}
_KENDRA = {1, 4, 7, 10}
_TRIKONA = {1, 5, 9}
_DUSTHANA = {6, 8, 12}
_DIGNITY_PTS = {
    "Exalted": 20, "Moolatrikona": 16, "Own Sign": 14, "Friendly Sign": 7,
    "Neutral Sign": 0, "Enemy Sign": -8, "Debilitated": -18,
}
_AVG_SAV = 28.0  # average Sarvashtakavarga bindus per sign (337/12)


_DISPLAY_ORDER = [
    "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn",
    "Rahu", "Ketu", "Uranus", "Neptune", "Pluto",
]


def _dms(deg: float) -> str:
    d = int(deg)
    m_f = (deg - d) * 60
    m = int(m_f)
    s = int(round((m_f - m) * 60))
    if s == 60:
        s, m = 0, m + 1
    if m == 60:
        m, d = 0, d + 1
    return f"{d:02d}°{m:02d}'{s:02d}\""


def _day_planet_positions(dob: str, lat: float, lon: float, tob: str = "12:00") -> list[dict]:
    """Day-level planetary positions (sign, degree, direct/retrograde) for all
    planets incl. Uranus/Neptune/Pluto. Taken at ``tob`` (default local noon as
    the day's representative; only the Moon moves materially within a day)."""
    jd = get_julian_day(dob, tob, lat, lon)
    pos = calc_planet_positions(jd, lat, lon)["planets"]
    out: list[dict] = []
    for p in _DISPLAY_ORDER:
        d = pos.get(p)
        if not d:
            continue
        out.append({
            "planet": p,
            "sign": d["sign_name"],
            "sign_num": d["sign"],
            "degree": round(d["degree_in_sign"], 2),
            "degree_dms": _dms(d["degree_in_sign"]),
            "retrograde": d.get("retrograde", False),
            "motion": "Retrograde" if d.get("retrograde") else "Direct",
        })
    return out


def _ascendant_sign(jd: float, lat: float, lon: float) -> int:
    import swisseph as swe
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    _cusps, ascmc = swe.houses_ex(jd, lat, lon, b"W", swe.FLG_SIDEREAL)
    return int((ascmc[0] % 360) / 30)


def _fmt(minutes: int) -> str:
    minutes %= 24 * 60
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def _lagna_windows(dob: str, lat: float, lon: float, step_min: int = 2) -> list[dict]:
    """One rising window per sign across the local day (00:00–24:00).

    Samples the ascendant every ``step_min`` minutes; a sign may rise in two
    pieces around midnight, so we keep the longest piece per sign.
    """
    base_jd = get_julian_day(dob, "00:00", lat, lon)  # UT JD for local midnight
    steps = (24 * 60) // step_min
    raw: list[dict] = []
    prev = None
    cur: dict | None = None
    for i in range(steps + 1):
        jd = base_jd + (i * step_min) / 1440.0
        sign = _ascendant_sign(jd, lat, lon)
        if sign != prev:
            if cur is not None:
                cur["end_min"] = i * step_min
                raw.append(cur)
            cur = {"sign": sign, "start_min": i * step_min}
            prev = sign
    if cur is not None:
        cur["end_min"] = 24 * 60
        raw.append(cur)

    # Keep the longest window per sign (handles the midnight split).
    best: dict[int, dict] = {}
    for w in raw:
        dur = w["end_min"] - w["start_min"]
        if w["sign"] not in best or dur > (best[w["sign"]]["end_min"] - best[w["sign"]]["start_min"]):
            best[w["sign"]] = w
    return [best[s] for s in sorted(best)]


def _moon_waxing(chart: dict) -> bool:
    phase = (chart["planets"]["Moon"]["longitude"] - chart["planets"]["Sun"]["longitude"]) % 360
    return phase < 180


def _is_benefic(chart: dict, p: str) -> bool:
    if p in _BENEFICS:
        return True
    return p == "Moon" and _moon_waxing(chart)


def _is_malefic(chart: dict, p: str) -> bool:
    if p in _MALEFICS:
        return True
    return p == "Moon" and not _moon_waxing(chart)


def _house_strength(chart: dict, house: int) -> float:
    """0–100 strength of one Whole-Sign house from real chart signals."""
    lagna_sign = chart["lagna"]["sign"]
    sign = (lagna_sign + house - 1) % 12
    score = 50.0
    # Sarvashtakavarga bindus for the sign (the strongest "is this house strong" signal).
    sav = chart["ashtakavarga"]["totals"][sign]
    score += (sav - _AVG_SAV) * 1.6
    # House-lord dignity + placement — the key Lagna-specific signal (the sign
    # in this house, and therefore its lord, changes with every ascendant).
    lord = SIGN_LORDS[sign]
    lp = chart["planets"].get(lord)
    if lp:
        score += _DIGNITY_PTS.get(lp["dignity"], 0) * 0.9
        lh = lp["house"]
        if lh in _TRIKONA:
            score += 10
        elif lh in _KENDRA:
            score += 7
        elif lh in _DUSTHANA:
            score -= 12
    # Occupants of the house.
    for pname, pdata in chart["planets"].items():
        if pname not in _CLASSICAL:
            continue
        if pdata["house"] == house:
            if _is_benefic(chart, pname):
                score += 8
            elif _is_malefic(chart, pname):
                score -= 8
    # Graha-drishti onto the house.
    for asp in chart["graha_drishti"]["house_aspected_by"].get(str(house), []):
        if _is_benefic(chart, asp):
            score += 4
        elif _is_malefic(chart, asp):
            score -= 4
    return max(0.0, min(100.0, score))


def _karaka_strength(chart: dict, karakas: list[str]) -> float:
    """0–100 from Shadbala ratio (preferred) or dignity fallback."""
    vals: list[float] = []
    sb = chart.get("shadbala", {})
    for k in karakas:
        if k in sb and "ratio" in sb[k]:
            vals.append(max(0.0, min(100.0, 50 + (sb[k]["ratio"] - 1.0) * 40)))
        elif k in chart["planets"]:
            vals.append(max(0.0, min(100.0, 50 + _DIGNITY_PTS.get(chart["planets"][k]["dignity"], 0))))
    return sum(vals) / len(vals) if vals else 50.0


def _aspect_score(chart: dict, houses: list[int], karakas: list[str]) -> float:
    # Bhava + bhava-lord dominate (they vary by Lagna → the per-window signal);
    # the karaka is the SAME across all 12 Lagnas, so it's only a light day-level
    # modifier — heavy karaka weight would wrongly flatten a whole column.
    h_scores = [_house_strength(chart, h) for h in houses]
    primary = h_scores[0]
    secondary = sum(h_scores[1:]) / len(h_scores[1:]) if len(h_scores) > 1 else primary
    karaka = _karaka_strength(chart, karakas)
    return round(primary * 0.62 + secondary * 0.23 + karaka * 0.15, 1)


def _verdict(score: float) -> str:
    if score >= 60:
        return "good"
    if score >= 45:
        return "moderate"
    return "challenging"


def _overall_score(chart: dict) -> float:
    """Overall Lagna strength — driven by Lagna-lord Shadbala + Lagna Ashtakavarga."""
    lagna = chart["lagna"]
    lord = lagna["sign_lord"]
    score = 50.0
    sb = chart.get("shadbala", {})
    if lord in sb and "ratio" in sb[lord]:
        score += (sb[lord]["ratio"] - 1.0) * 30
    lp = chart["planets"].get(lord)
    if lp:
        score += _DIGNITY_PTS.get(lp["dignity"], 0) * 0.5
        if lp["house"] in _TRIKONA:
            score += 8
        elif lp["house"] in _KENDRA:
            score += 5
        elif lp["house"] in _DUSTHANA:
            score -= 12
    score += (chart["ashtakavarga"]["totals"][lagna["sign"]] - _AVG_SAV) * 1.2
    for pname, pdata in chart["planets"].items():
        if pname not in _CLASSICAL:
            continue
        if pdata["house"] == 1:
            if _is_benefic(chart, pname):
                score += 7
            elif _is_malefic(chart, pname):
                score -= 7
    return max(0.0, min(100.0, round(score, 1)))


def analyze_birth_muhurta(
    *,
    dob: str,
    lat: float,
    lon: float,
    place_name: str,
    chart_fn=build_muhurta_chart,
    priorities: list[str] | None = None,
    time: str | None = None,
) -> dict:
    """Rank the day's rising Lagnas with a per-life-aspect verdict for each.

    ``chart_fn(dob, tob, lat, lon)`` returns the (lighter) chart dict; injected so
    tests can substitute a fake. ``priorities`` is an optional list of aspect keys;
    when given, windows are ranked by the average of those aspects instead of
    overall Lagna strength.

    ``time`` (HH:MM) is optional. When given (e.g. an already-born person), the
    Lagna actually rising at that instant is flagged ``highlighted`` and scored at
    the exact moment, and the planetary-positions table is taken at that time.
    When omitted, nothing is highlighted and positions default to local noon.
    """
    windows = _lagna_windows(dob, lat, lon)
    # Compute sunrise/sunset once for the whole day and reuse across windows.
    day_sun = calc_sunrise_sunset(get_julian_day(dob, "12:00", lat, lon), lat, lon)
    positions_time = time or "12:00"
    # If a birth time is given, find which Lagna was actually rising then.
    highlight_sign = (
        _ascendant_sign(get_julian_day(dob, time, lat, lon), lat, lon) if time else None
    )
    results: list[dict] = []
    for w in windows:
        is_highlighted = time is not None and w["sign"] == highlight_sign
        mid = (w["start_min"] + w["end_min"]) // 2
        # Score the highlighted Lagna at the exact birth moment; the rest at the
        # window midpoint as the sign's representative time.
        tob = time if is_highlighted else _fmt(mid)
        chart = chart_fn(dob=dob, tob=tob, lat=lat, lon=lon, sun_sunset=day_sun)
        aspects = {
            key: {
                "label": label, "group": group,
                "score": (sc := _aspect_score(chart, houses, karakas)),
                "verdict": _verdict(sc),
            }
            for key, label, group, houses, karakas in LIFE_ASPECTS
        }
        overall = _overall_score(chart)
        if priorities:
            picked = [aspects[k]["score"] for k in priorities if k in aspects]
            rank_score = round(sum(picked) / len(picked), 1) if picked else overall
        else:
            rank_score = overall
        lord = SIGN_LORDS[w["sign"]]
        results.append({
            "lagna_sign": w["sign"],
            "lagna_name": SIGN_NAMES[w["sign"]],
            "lagna_lord": lord,
            "lord_retrograde": chart["planets"].get(lord, {}).get("retrograde", False),
            "window": {"start": _fmt(w["start_min"]), "end": _fmt(w["end_min"]), "mid": _fmt(mid)},
            "highlighted": is_highlighted,
            "overall": overall,
            "rank_score": rank_score,
            "panchanga": {
                "nakshatra": chart["nakshatra"]["name"],
                "tithi": chart["panchanga"]["tithi_name"],
                "yoga": chart["panchanga"]["yoga_name"],
                "paksha": chart["panchanga"]["paksha"],
            },
            "aspects": aspects,
        })

    results.sort(key=lambda r: r["rank_score"], reverse=True)
    for i, r in enumerate(results, 1):
        r["rank"] = i

    return {
        "date": dob,
        "place_name": place_name,
        "lat": lat,
        "lon": lon,
        "priorities": priorities or [],
        "planet_positions": _day_planet_positions(dob, lat, lon, tob=positions_time),
        "positions_time": positions_time,
        "query_time": time,
        "highlight_lagna": SIGN_NAMES[highlight_sign] if highlight_sign is not None else None,
        "aspects_config": [
            {"key": k, "label": label, "group": group}
            for k, label, group, _h, _kar in LIFE_ASPECTS
        ],
        "windows": results,
    }
