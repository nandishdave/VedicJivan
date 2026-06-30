"""Unshakable Chart Finder.

Scans a date range and returns a ranked **menu** of birth (date, time) moments by
the composite ``unshakable_score``, with the ones clearing the quality ``bar``
flagged ``exceptional``:

  - 1-day search  -> every rising Lagna of the day, ranked, + a planetary-
    positions snapshot (like the muhurta report).
  - multi-day search -> the top ``top_per_day`` charts of each day.

Two modes:
  - ``"bruteforce"`` (default) — fully score every rising Lagna. Needed to build
    the complete ranked menu; cheap enough for day/week.
  - ``"funnel"`` — skip the expensive full eval on Lagnas that can't reach the
    bar (admissible bound, so the ``exceptional`` set is identical to brute
    force). Used for the month/year scale, where only the exceptional charts
    matter and full ranking of every day is too costly.
"""
from __future__ import annotations

from datetime import date as _date, timedelta

from app.services.kundli_calculator._core import get_julian_day
from app.services.kundli_calculator.chart_strength import (
    unshakable_score,
    unshakable_upper_bound,
)
from app.services.kundli_calculator.sunrise import calc_sunrise_sunset


def _date_range(start: str, days: int) -> list[str]:
    y, m, d = map(int, start.split("-"))
    d0 = _date(y, m, d)
    return [(d0 + timedelta(days=i)).isoformat() for i in range(days)]


def _record(dob: str, tob: str, chart: dict, scored: dict, bar: float) -> dict:
    return {
        "date": dob,
        "time": tob,
        "lagna": chart["lagna"]["sign_name"],
        "score": scored["score"],
        "layers": scored["layers"],
        "ayurdaya": scored["ayurdaya"],
        "balarishta": scored["balarishta"],
        "yogas": [y["name"] for y in scored["yogas"]],
        "atmakaraka": scored["atmakaraka"],
        "exceptional": scored["score"] >= bar,
    }


def find_unshakable(
    *,
    start_date: str,
    days: int,
    lat: float,
    lon: float,
    place_name: str,
    bar: float = 90.0,
    mode: str = "bruteforce",
    top_per_day: int = 3,
) -> dict:
    """Rank the range's birth moments. Returns a per-day menu (all Lagnas for a
    single day, top ``top_per_day`` per day otherwise), the ``exceptional`` set
    (>= bar across the range), and — for a single day — a noon planetary table."""
    from app.services.muhurta import (
        _day_planet_positions,
        _fmt,
        _lagna_windows,
        build_muhurta_chart,
    )

    per_day: list[dict] = []
    exceptional: list[dict] = []
    full_evals = skipped = 0

    for dob in _date_range(start_date, days):
        day_sun = calc_sunrise_sunset(get_julian_day(dob, "12:00", lat, lon), lat, lon)
        day_charts: list[dict] = []
        for w in _lagna_windows(dob, lat, lon):
            tob = _fmt((w["start_min"] + w["end_min"]) // 2)

            if mode == "funnel":
                cheap = build_muhurta_chart(
                    dob=dob, tob=tob, lat=lat, lon=lon,
                    sun_sunset=day_sun, with_shadbala=False,
                )
                if unshakable_upper_bound(cheap) < bar:
                    skipped += 1
                    continue

            chart = build_muhurta_chart(dob=dob, tob=tob, lat=lat, lon=lon, sun_sunset=day_sun)
            full_evals += 1
            rec = _record(dob, tob, chart, unshakable_score(chart), bar)
            day_charts.append(rec)
            if rec["exceptional"]:
                exceptional.append(rec)

        day_charts.sort(key=lambda r: r["score"], reverse=True)
        keep = day_charts if days == 1 else day_charts[:top_per_day]
        per_day.append({"date": dob, "charts": keep})

    exceptional.sort(key=lambda r: r["score"], reverse=True)
    result = {
        "start_date": start_date,
        "days": days,
        "place_name": place_name,
        "lat": lat,
        "lon": lon,
        "bar": bar,
        "mode": mode,
        "per_day": per_day,
        "exceptional": exceptional,
        "exceptional_count": len(exceptional),
        "full_evals": full_evals,
        "skipped": skipped,
    }
    if days == 1:
        result["planet_positions"] = _day_planet_positions(start_date, lat, lon)
        result["positions_time"] = "12:00"
    return result


# ── Local CLI harness (run in Docker) ────────────────────────────────────────
# python -m app.services.unshakable_finder --start 2026-06-20 --days 7 \
#     --lat 21.7333 --lon 70.6167 --place "Jetpur" --bar 90 --mode bruteforce
if __name__ == "__main__":  # pragma: no cover
    import argparse
    import time

    ap = argparse.ArgumentParser(description="Unshakable Chart Finder (local harness)")
    ap.add_argument("--start", required=True)
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--lat", type=float, required=True)
    ap.add_argument("--lon", type=float, required=True)
    ap.add_argument("--place", default="")
    ap.add_argument("--bar", type=float, default=90.0)
    ap.add_argument("--mode", choices=["bruteforce", "funnel"], default="bruteforce")
    args = ap.parse_args()

    t0 = time.monotonic()
    res = find_unshakable(
        start_date=args.start, days=args.days, lat=args.lat, lon=args.lon,
        place_name=args.place, bar=args.bar, mode=args.mode,
    )
    elapsed = time.monotonic() - t0
    print(f"\n{args.mode} | {args.start} +{args.days}d | bar={args.bar} | {elapsed:.1f}s | "
          f"full_evals={res['full_evals']} skipped={res['skipped']} | "
          f"exceptional={res['exceptional_count']}")
    for day in res["per_day"]:
        print(f"\n{day['date']}:")
        for c in day["charts"]:
            star = " *" if c["exceptional"] else "  "
            print(f"  {star}{c['time']}  {c['lagna']:>11}  {c['score']:>5}")
