"""Unshakable Chart Finder — Phase 1 (structural strength).

Scans a date range for birth (date, time) moments whose chart clears a quality
bar on the Layer-1 ``structural_strength`` score. Two modes:

  - ``"bruteforce"`` — fully score every rising Lagna of every day. Ground truth.
  - ``"funnel"`` — for each Lagna, build a *cheap* chart (no Shadbala) and skip
    the expensive full eval when even an optimistic upper bound can't reach the
    bar. Provably never drops a chart the brute force would have kept (the bound
    is admissible), so the funnel's >= bar set is identical to brute force's.

Stream-and-discard: only the >= bar candidates + a running best-below-bar (for
the fallback) are held in memory, so RAM stays flat regardless of range.

This is the v1 (week-scale) engine and the calibration harness in one. For a
week, brute force is already cheap (~84 charts); the funnel exists to be
*validated* against brute force here so it can be trusted at month/year scale.
"""
from __future__ import annotations

from datetime import date as _date, timedelta

from app.services.kundli_calculator._core import get_julian_day
from app.services.kundli_calculator.chart_strength import (
    optimistic_upper_bound,
    structural_strength,
)
from app.services.kundli_calculator.sunrise import calc_sunrise_sunset


def _date_range(start: str, days: int) -> list[str]:
    y, m, d = map(int, start.split("-"))
    d0 = _date(y, m, d)
    return [(d0 + timedelta(days=i)).isoformat() for i in range(days)]


def _record(dob: str, tob: str, chart: dict, scored: dict) -> dict:
    return {
        "date": dob,
        "time": tob,
        "lagna": chart["lagna"]["sign_name"],
        "score": scored["score"],
        "components": scored["components"],
    }


def find_unshakable(
    *,
    start_date: str,
    days: int,
    lat: float,
    lon: float,
    place_name: str,
    bar: float = 90.0,
    mode: str = "funnel",
) -> dict:
    """Scan ``days`` days from ``start_date`` and return every (date, time) whose
    chart scores >= ``bar``, ranked high to low. ``mode`` is ``"funnel"`` or
    ``"bruteforce"`` (same results; funnel does fewer full evals)."""
    # Imported here to avoid a heavy import at module load and any cycle.
    from app.services.muhurta import _fmt, _lagna_windows, build_muhurta_chart

    candidates: list[dict] = []
    best_below: dict | None = None          # best fully-scored chart under the bar
    best_skipped: dict | None = None        # most promising chart we pruned (funnel)
    full_evals = skipped = 0

    for dob in _date_range(start_date, days):
        day_sun = calc_sunrise_sunset(get_julian_day(dob, "12:00", lat, lon), lat, lon)
        for w in _lagna_windows(dob, lat, lon):
            tob = _fmt((w["start_min"] + w["end_min"]) // 2)

            if mode == "funnel":
                cheap = build_muhurta_chart(
                    dob=dob, tob=tob, lat=lat, lon=lon,
                    sun_sunset=day_sun, with_shadbala=False,
                )
                bound = optimistic_upper_bound(cheap)
                if bound < bar:
                    skipped += 1
                    if best_skipped is None or bound > best_skipped["bound"]:
                        best_skipped = {"dob": dob, "tob": tob, "bound": bound, "day_sun": day_sun}
                    continue

            chart = build_muhurta_chart(dob=dob, tob=tob, lat=lat, lon=lon, sun_sunset=day_sun)
            full_evals += 1
            scored = structural_strength(chart)
            rec = _record(dob, tob, chart, scored)
            if scored["score"] >= bar:
                candidates.append(rec)
            elif best_below is None or scored["score"] > best_below["score"]:
                best_below = rec

    candidates.sort(key=lambda r: r["score"], reverse=True)
    result = {
        "start_date": start_date,
        "days": days,
        "place_name": place_name,
        "lat": lat,
        "lon": lon,
        "bar": bar,
        "mode": mode,
        "candidates": candidates,
        "count": len(candidates),
        "full_evals": full_evals,
        "skipped": skipped,
    }

    # Fallback: nothing cleared the bar -> surface the single best chart found,
    # full-evaluating the most-promising pruned window if needed (so funnel mode
    # still has an honest "best available" even when everything was skipped).
    if not candidates:
        fb = best_below
        if best_skipped is not None:
            chart = build_muhurta_chart(
                dob=best_skipped["dob"], tob=best_skipped["tob"],
                lat=lat, lon=lon, sun_sunset=best_skipped["day_sun"],
            )
            full_evals += 1
            result["full_evals"] = full_evals
            scored = structural_strength(chart)
            rec = _record(best_skipped["dob"], best_skipped["tob"], chart, scored)
            if fb is None or rec["score"] > fb["score"]:
                fb = rec
        if fb is not None:
            result["fallback"] = fb
    return result


# ── Local CLI harness (run in Docker) ────────────────────────────────────────
# python -m app.services.unshakable_finder --start 2026-06-20 --days 7 \
#     --lat 21.7333 --lon 70.6167 --place "Jetpur" --bar 90 --mode funnel
if __name__ == "__main__":  # pragma: no cover
    import argparse
    import json
    import time

    ap = argparse.ArgumentParser(description="Unshakable Chart Finder (local harness)")
    ap.add_argument("--start", required=True, help="start date YYYY-MM-DD")
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--lat", type=float, required=True)
    ap.add_argument("--lon", type=float, required=True)
    ap.add_argument("--place", default="")
    ap.add_argument("--bar", type=float, default=90.0)
    ap.add_argument("--mode", choices=["funnel", "bruteforce"], default="funnel")
    ap.add_argument("--out", default="", help="optional JSONL path for full results")
    args = ap.parse_args()

    t0 = time.monotonic()
    res = find_unshakable(
        start_date=args.start, days=args.days, lat=args.lat, lon=args.lon,
        place_name=args.place, bar=args.bar, mode=args.mode,
    )
    elapsed = time.monotonic() - t0

    print(f"\n{args.mode} | {args.start} +{args.days}d | bar={args.bar} | "
          f"{elapsed:.1f}s | full_evals={res['full_evals']} skipped={res['skipped']}")
    print(f"{res['count']} chart(s) >= {args.bar}:")
    for c in res["candidates"]:
        print(f"  {c['date']} {c['time']}  {c['lagna']:>11}  {c['score']:>5}")
    if not res["candidates"] and res.get("fallback"):
        f = res["fallback"]
        print(f"  (none >= bar) best available: {f['date']} {f['time']} "
              f"{f['lagna']} {f['score']}")
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            for c in res["candidates"]:
                fh.write(json.dumps(c) + "\n")
        print(f"wrote {res['count']} rows -> {args.out}")
