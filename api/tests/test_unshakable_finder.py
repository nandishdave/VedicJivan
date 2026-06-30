"""Calibration + shape tests for the Unshakable finder.

The central guarantee still holds: the funnel's ``exceptional`` set (>= bar) is
IDENTICAL to brute force's at every bar, while doing fewer full evals. Plus the
per-day menu shape (full day for 1 day, top-N per day otherwise).

Kept small (1-2 days) because each chart runs real Shadbala.
"""
from app.services.unshakable_finder import find_unshakable

_PLACE = dict(lat=21.7333, lon=70.6167, place_name="Jetpur")


def test_funnel_matches_bruteforce_at_every_bar():
    bf = find_unshakable(start_date="2026-06-20", days=1, bar=0.0, mode="bruteforce", **_PLACE)
    actual = {(c["date"], c["time"]): c["score"] for c in bf["exceptional"]}
    assert actual  # brute force scored everything (bar 0 -> all exceptional)

    for bar in (55.0, 72.0, 90.0):
        fn = find_unshakable(start_date="2026-06-20", days=1, bar=bar, mode="funnel", **_PLACE)
        expected = {k for k, s in actual.items() if s >= bar}
        got = {(c["date"], c["time"]) for c in fn["exceptional"]}
        assert got == expected, f"funnel/bruteforce mismatch at bar={bar}"


def test_funnel_prunes_at_a_high_bar():
    fn = find_unshakable(start_date="2026-06-20", days=1, bar=95.0, mode="funnel", **_PLACE)
    assert fn["skipped"] > 0
    assert fn["exceptional_count"] == 0


def test_single_day_returns_full_ranked_menu_and_positions():
    res = find_unshakable(start_date="2026-06-20", days=1, bar=70.0, mode="bruteforce", **_PLACE)
    assert len(res["per_day"]) == 1
    charts = res["per_day"][0]["charts"]
    assert len(charts) == 12  # every rising Lagna of the day
    scores = [c["score"] for c in charts]
    assert scores == sorted(scores, reverse=True)
    assert {"time", "lagna", "score", "layers", "ayurdaya", "exceptional"} <= set(charts[0])
    # single-day search includes the planetary-positions snapshot
    assert len(res["planet_positions"]) == 12 and res["positions_time"] == "12:00"


def test_multi_day_returns_top_per_day():
    res = find_unshakable(start_date="2026-06-20", days=2, bar=70.0, mode="bruteforce",
                          top_per_day=3, **_PLACE)
    assert len(res["per_day"]) == 2
    for day in res["per_day"]:
        assert 1 <= len(day["charts"]) <= 3
        scores = [c["score"] for c in day["charts"]]
        assert scores == sorted(scores, reverse=True)
    assert "planet_positions" not in res  # only for single-day


def test_exceptional_flagged_and_ranked():
    res = find_unshakable(start_date="2026-06-20", days=1, bar=68.0, mode="bruteforce", **_PLACE)
    ex = res["exceptional"]
    assert all(c["exceptional"] and c["score"] >= 68.0 for c in ex)
    assert [c["score"] for c in ex] == sorted([c["score"] for c in ex], reverse=True)
