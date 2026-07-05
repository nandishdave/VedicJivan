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
from app.services.kundli_calculator.dhana_yoga import (
    dhana_yoga_score,
    prosperity_yoga_score,
)
from app.services.kundli_calculator.divisional import calc_divisional_charts
from app.services.kundli_calculator.worldly_potential import worldly_potential
from app.services.kundli_calculator.raja_yoga import raja_yoga_score
from app.services.kundli_calculator.nakshatra import calc_nakshatra
from app.services.kundli_calculator.panchanga import calc_panchanga
from app.services.kundli_calculator.shadbala import calc_shadbala
from app.services.kundli_calculator.sunrise import calc_sunrise_sunset
# The 13-domain life analysis + Balanced-Life score now live in one shared leaf
# module (used by both this engine and the Unshakable finder). Re-exported here so
# existing callers/tests keep importing them from ``app.services.muhurta``.
from app.services.kundli_calculator.life_domains import (  # noqa: F401  (re-export)
    LIFE_ASPECTS,
    _AVG_SAV,
    _DIGNITY_PTS,
    _DUSTHANA,
    _KENDRA,
    _TRIKONA,
    _aspect_score,
    _house_strength,
    _is_benefic,
    _is_malefic,
    _verdict,
    balanced_life,
    domain_scores,
)


def build_muhurta_chart(
    *, dob: str, tob: str, lat: float, lon: float,
    sun_sunset: dict | None = None, with_shadbala: bool = True,
) -> dict:
    """Lighter chart for muhurta scoring — only what a strength scan needs.

    Computes positions + Whole-Sign houses, Ashtakavarga, Shadbala (which itself
    uses the D2/D3/D7/D9/D12/D30 vargas), graha-drishti and panchanga. Skips the
    dashas, KP, Jaimini, yogas/doshas, gochar, varshaphal and numerology that the
    full Kundli report needs but birth-muhurta ranking does not — several times
    faster than the full ``build_chart``.

    ``with_shadbala=False`` skips the Shadbala (and the divisional charts it
    needs) — by far the most expensive step — leaving positions + Ashtakavarga +
    panchanga + drishti. The Unshakable funnel uses this *cheap* chart to compute
    an optimistic upper bound before deciding whether a full (Shadbala) eval is
    worth it.
    """
    jd = get_julian_day(dob, tob, lat, lon)
    pos = calc_planet_positions(jd, lat, lon)
    planets, lagna = pos["planets"], pos["lagna"]
    # Sunrise/sunset is a date+place property (same for every window), so the
    # caller can compute it once and pass it in to avoid 12x rise_trans.
    if sun_sunset is None:
        sun_sunset = calc_sunrise_sunset(jd, lat, lon)
    chart = {
        "lagna": lagna,
        "planets": planets,
        "nakshatra": calc_nakshatra(planets["Moon"]["longitude"]),
        "panchanga": calc_panchanga(jd),
        "graha_drishti": calc_graha_drishti(planets, lagna),
        "ashtakavarga": calc_ashtakavarga(planets, lagna["sign"]),
        "sunrise": sun_sunset["sunrise"],
        "sunset": sun_sunset["sunset"],
        # Birth moment — lets downstream scorers (e.g. worldly_potential) time the
        # Vimshottari dashas without re-threading dob/tob through every call.
        "dob": dob,
        "tob": tob,
    }
    if with_shadbala:
        divisional = calc_divisional_charts(planets, lagna)
        # Keep the divisional charts on the chart (already computed for Shadbala)
        # so D60-based scoring is free rather than recomputed.
        chart["divisional"] = divisional
        chart["shadbala"] = calc_shadbala(
            planets, lagna, jd, dob, tob, divisional, sun_sunset=sun_sunset
        )
    return chart

_CLASSICAL = ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu")
# The life-domain scoring constants (_DIGNITY_PTS, _AVG_SAV, _KENDRA/_TRIKONA/
# _DUSTHANA, the functional-benefic scheme) + the aspect/house/verdict helpers now
# live in kundli_calculator.life_domains and are imported at the top of this file.


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
    optimize_prominence: bool = False,
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
        # Graded yogas for this Lagna (lords change per ascendant). Dhana = the
        # tight wealth yoga (lords of 1/2/11); Prosperity = the wider fortune
        # extension (links touching the 5th/9th), kept separate.
        dy_score, dy_links = dhana_yoga_score(chart)
        pr_score, pr_links = prosperity_yoga_score(chart)
        rj_score, rj_links = raja_yoga_score(chart)
        # The 13-domain life reading (shared with the Unshakable finder) — each
        # domain 0-100 with the wealth/fortune/career graded-yoga blends applied.
        aspects = domain_scores(chart)
        # Roll the 13 domains into ONE "how complete is this life" % (weakest-links)
        # + the 2-3 weakest domains as concern areas. Passing the same `aspects`
        # keeps the % consistent with the per-domain columns shown to the user.
        balanced = balanced_life(chart, aspects)
        overall = _overall_score(chart)
        # Validated worldly-potential readout (0-100) for this Lagna — a faint
        # (~0.63 AUC) tilt toward prominence markers. Display always; optionally
        # blended into the ranking below. None if the chart lacks a birth date.
        wp = worldly_potential(chart)
        if priorities:
            picked = [aspects[k]["score"] for k in priorities if k in aspects]
            base = round(sum(picked) / len(picked), 1) if picked else overall
        else:
            base = overall
        # "Prominence" mode blends worldly-potential into the rank without letting
        # it dominate — auspiciousness (health/longevity/etc.) still leads at 0.6.
        if optimize_prominence and wp is not None:
            rank_score = round(0.6 * base + 0.4 * wp["score"], 1)
        else:
            rank_score = base
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
            "worldly_potential": wp,
            "balanced_life": balanced,
            "dhana_yoga": {"score": dy_score, "links": dy_links},
            "prosperity_yoga": {"score": pr_score, "links": pr_links},
            "raja_yoga": {"score": rj_score, "links": rj_links},
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
        "optimize_prominence": optimize_prominence,
        "planet_positions": _day_planet_positions(dob, lat, lon, tob=positions_time),
        "positions_time": positions_time,
        "query_time": time,
        "highlight_lagna": SIGN_NAMES[highlight_sign] if highlight_sign is not None else None,
        "aspects_config": [
            {"key": k, "label": label, "group": group}
            for k, label, group, _h, _kar, _v in LIFE_ASPECTS
        ],
        "windows": results,
    }
