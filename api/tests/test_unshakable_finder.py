"""Calibration tests for the Unshakable funnel.

The central guarantee: the funnel's >= bar result set is IDENTICAL to brute
force's at every bar (the optimistic bound is admissible, so it never prunes a
chart that would have qualified), while doing fewer full evaluations. These tests
are the "no magical chart dropped" proof.

Kept small (1-2 days) because each chart runs real Shadbala (~0.5s).
"""
from app.services.unshakable_finder import find_unshakable

_PLACE = dict(lat=21.7333, lon=70.6167, place_name="Jetpur")


def test_funnel_matches_bruteforce_at_every_bar():
    """Score every window once (brute force), then confirm the funnel reproduces
    the exact >= bar set at several bars. (1 day keeps real-Shadbala cost down;
    days are independent so this proves the guarantee.)"""
    bf = find_unshakable(start_date="2026-06-20", days=1, bar=0.0, mode="bruteforce", **_PLACE)
    actual = {(c["date"], c["time"]): c["score"] for c in bf["candidates"]}
    assert actual  # sanity: brute force scored something

    for bar in (55.0, 70.0, 85.0):
        fn = find_unshakable(start_date="2026-06-20", days=1, bar=bar, mode="funnel", **_PLACE)
        expected = {k for k, s in actual.items() if s >= bar}
        got = {(c["date"], c["time"]) for c in fn["candidates"]}
        assert got == expected, f"funnel/bruteforce mismatch at bar={bar}"


def test_funnel_prunes_at_a_high_bar():
    """A high bar nothing can reach -> the funnel skips full evals and still
    returns an honest fallback (best available)."""
    fn = find_unshakable(start_date="2026-06-20", days=1, bar=85.0, mode="funnel", **_PLACE)
    assert fn["skipped"] > 0
    assert fn["count"] == 0
    assert fn.get("fallback") and 0 <= fn["fallback"]["score"] < 85.0


def test_funnel_does_no_more_full_evals_than_bruteforce():
    bf = find_unshakable(start_date="2026-06-20", days=1, bar=72.0, mode="bruteforce", **_PLACE)
    fn = find_unshakable(start_date="2026-06-20", days=1, bar=72.0, mode="funnel", **_PLACE)
    assert fn["full_evals"] <= bf["full_evals"]


def test_results_ranked_and_shaped():
    res = find_unshakable(start_date="2026-06-20", days=1, bar=0.0, mode="bruteforce", **_PLACE)
    scores = [c["score"] for c in res["candidates"]]
    assert scores == sorted(scores, reverse=True)
    c = res["candidates"][0]
    assert {"date", "time", "lagna", "score", "components"} <= set(c)
