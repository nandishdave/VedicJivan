"""Tests + regression guards for the Auspicious Birth-Time (Muhurta) engine.

Fast unit tests use hand-built chart dicts (no ephemeris). One slow test runs
the real engine to guard the Swiss-Ephemeris integration. The key guard is
``test_house_lord_dominates_karaka`` — it locks in the design decision that each
Lagna's per-aspect verdict is driven by the Bhava + Bhava-lord (which vary by
ascendant), not the karaka (constant across all 12 Lagnas).
"""
import json

from app.dependencies import get_message_queue
from app.main import app
from app.services.kundli_calculator._core import SIGN_LORDS, SIGN_NAMES
from app.workers import kundli_lambda
from app.services.muhurta import (
    LIFE_ASPECTS,
    _aspect_score,
    _house_strength,
    _is_benefic,
    _is_malefic,
    _overall_score,
    _verdict,
    analyze_birth_muhurta,
    build_muhurta_chart,
)

_ALL = [
    "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn",
    "Rahu", "Ketu", "Uranus", "Neptune", "Pluto",
]


def _mini(lagna_sign, moon_lon=90.0, sun_lon=0.0):
    return {"lagna": {"sign": lagna_sign},
            "planets": {"Moon": {"longitude": moon_lon}, "Sun": {"longitude": sun_lon}}}


def test_hybrid_functional_benefics_with_moon_paksha():
    # Libra (6): Jupiter rules 3rd+6th -> functional MALEFIC; Venus/Saturn/Mercury benefic.
    libra = _mini(6)
    assert not _is_benefic(libra, "Jupiter") and _is_malefic(libra, "Jupiter")
    assert _is_benefic(libra, "Venus") and _is_benefic(libra, "Saturn")
    # Aries (0): Jupiter is a functional benefic; Venus is a functional malefic.
    aries = _mini(0)
    assert _is_benefic(aries, "Jupiter") and _is_malefic(aries, "Venus")
    # Moon by paksha, regardless of lagna: waxing benefic, waning malefic.
    assert _is_benefic(_mini(6, moon_lon=90.0), "Moon")       # phase 90 < 180 -> waxing
    assert _is_malefic(_mini(6, moon_lon=200.0), "Moon")      # phase 200 -> waning

def test_nodes_inherit_dispositor_functional_nature():
    # Libra lagna (Saturn/Venus/Mercury are the functional benefics).
    def chart(rahu_sign):
        return {"lagna": {"sign": 6},
                "planets": {"Moon": {"longitude": 90.0}, "Sun": {"longitude": 0.0},
                            "Rahu": {"sign": rahu_sign}}}
    # Rahu in Capricorn (dispositor Saturn = functional benefic for Libra) -> benefic.
    cap = chart(9)
    assert _is_benefic(cap, "Rahu") and not _is_malefic(cap, "Rahu")
    # Rahu in Aries (dispositor Mars = functional malefic for Libra) -> malefic.
    ari = chart(0)
    assert _is_malefic(ari, "Rahu") and not _is_benefic(ari, "Rahu")


def make_chart(*, lagna_sign=0, totals=None, overrides=None, ratios=None, aspected_by=None):
    """Minimal chart dict the scoring helpers accept. Planets default to house 11
    (out of the way) so a test controls occupants explicitly."""
    planets = {
        p: {
            "longitude": 100.0, "sign": 10, "sign_name": "Aquarius", "sign_lord": "Saturn",
            "degree_in_sign": 10.0, "house": 11, "retrograde": False, "dignity": "Neutral Sign",
        }
        for p in _ALL
    }
    for p, o in (overrides or {}).items():
        planets[p].update(o)
    return {
        "lagna": {"sign": lagna_sign, "sign_name": SIGN_NAMES[lagna_sign], "sign_lord": SIGN_LORDS[lagna_sign]},
        "planets": planets,
        "ashtakavarga": {"totals": totals or [28] * 12},
        "shadbala": {p: {"ratio": (ratios or {}).get(p, 1.0)} for p in _ALL[:9]},
        "graha_drishti": {"house_aspected_by": aspected_by or {str(h): [] for h in range(1, 13)}},
        "nakshatra": {"name": "Rohini"},
        "panchanga": {"tithi_name": "Dvitiya", "yoga_name": "Priti", "paksha": "Shukla"},
    }


def test_verdict_bands():
    assert _verdict(75) == "good"
    assert _verdict(50) == "moderate"
    assert _verdict(30) == "challenging"


def test_house_strength_tracks_ashtakavarga():
    lo = make_chart(totals=[18] + [28] * 11)  # sign 0 weak
    hi = make_chart(totals=[40] + [28] * 11)  # sign 0 strong
    assert _house_strength(hi, 1) > _house_strength(lo, 1)  # house 1 = sign 0 for Aries lagna


def test_house_lord_dominates_karaka():
    """A change in the house-lord must move the aspect score far more than the
    same change in the (constant-across-Lagnas) karaka. This is the core design."""
    # Aspect "children" = 5th house; from Aries lagna the 5th is Leo, lord Sun. Karaka Jupiter.
    strong_lord = make_chart(overrides={"Sun": {"dignity": "Exalted", "house": 5}})
    weak_lord = make_chart(overrides={"Sun": {"dignity": "Debilitated", "house": 6}})
    lord_swing = _aspect_score(strong_lord, [5], ["Jupiter"]) - _aspect_score(weak_lord, [5], ["Jupiter"])

    strong_kar = make_chart(ratios={"Jupiter": 2.5})
    weak_kar = make_chart(ratios={"Jupiter": 0.1})
    kar_swing = _aspect_score(strong_kar, [5], ["Jupiter"]) - _aspect_score(weak_kar, [5], ["Jupiter"])

    assert lord_swing > 0 and kar_swing > 0
    assert lord_swing > 2 * kar_swing


def test_overall_score_rewards_strong_lagna_lord():
    weak = make_chart(lagna_sign=0, ratios={"Mars": 0.2})  # Aries lord Mars weak
    strong = make_chart(
        lagna_sign=0,
        ratios={"Mars": 2.0},
        overrides={"Mars": {"dignity": "Exalted", "house": 1}},
    )
    assert _overall_score(strong) > _overall_score(weak)


async def test_birth_endpoint_enqueues_muhurta_job(client, fake_queue):
    """POST returns 202 immediately and enqueues a `type: muhurta` job (the heavy
    analysis runs on the Lambda worker, not in the request)."""
    app.dependency_overrides[get_message_queue] = lambda: fake_queue
    try:
        resp = await client.post(
            "/api/muhurta/birth",
            json={
                "date": "2026-06-20", "lat": 21.7333, "lon": 70.6167,
                "place_name": "Jetpur", "email": "test@example.com",
            },
        )
        assert resp.status_code == 202
        assert len(fake_queue.sent) == 1
        payload = fake_queue.sent[0]
        assert payload["type"] == "muhurta"
        assert payload["email"] == "test@example.com"
        assert payload["date"] == "2026-06-20"
    finally:
        app.dependency_overrides.pop(get_message_queue, None)


async def test_birth_endpoint_requires_email(client, fake_queue):
    app.dependency_overrides[get_message_queue] = lambda: fake_queue
    try:
        resp = await client.post(
            "/api/muhurta/birth",
            json={"date": "2026-06-20", "lat": 21.7333, "lon": 70.6167, "place_name": "Jetpur"},
        )
        assert resp.status_code == 422  # missing email
        assert len(fake_queue.sent) == 0
    finally:
        app.dependency_overrides.pop(get_message_queue, None)


async def test_lambda_routes_muhurta_message(mocker):
    """The shared Kundli Lambda routes a `type: muhurta` SQS message to the
    muhurta worker (and kundli messages, which have no type, are untouched)."""
    captured = {}
    mocker.patch.object(kundli_lambda, "_run_muhurta_sync", lambda body: captured.update(body))
    await kundli_lambda._process_record({
        "body": json.dumps({
            "type": "muhurta", "date": "2026-06-20", "lat": 21.7, "lon": 70.6,
            "place_name": "X", "email": "a@b.com",
        })
    })
    assert captured["email"] == "a@b.com" and captured["type"] == "muhurta"


def test_engine_real_output_structure():
    """Real-ephemeris regression guard: 12 ranked windows, every aspect present,
    planetary positions include the outer planets."""
    res = analyze_birth_muhurta(
        dob="2026-06-20", lat=21.7333, lon=70.6167, place_name="Jetpur",
        chart_fn=build_muhurta_chart,
    )
    assert len(res["windows"]) == 12
    assert {w["lagna_sign"] for w in res["windows"]} == set(range(12))
    scores = [w["rank_score"] for w in res["windows"]]
    assert scores == sorted(scores, reverse=True)
    expected = {k for k, *_ in LIFE_ASPECTS}
    for w in res["windows"]:
        assert set(w["aspects"]) == expected
        assert all(a["verdict"] in ("good", "moderate", "challenging") for a in w["aspects"].values())
    names = {p["planet"] for p in res["planet_positions"]}
    assert {"Uranus", "Neptune", "Pluto", "Rahu", "Ketu"} <= names
    assert len(res["planet_positions"]) == 12


def test_no_time_defaults_to_noon_and_no_highlight():
    res = analyze_birth_muhurta(
        dob="2026-06-20", lat=21.7333, lon=70.6167, place_name="Jetpur",
        chart_fn=build_muhurta_chart,
    )
    assert res["positions_time"] == "12:00"
    assert res["query_time"] is None
    assert res["highlight_lagna"] is None
    assert all(w["highlighted"] is False for w in res["windows"])


def test_given_time_highlights_the_rising_lagna():
    """An already-born birth time flags exactly the Lagna rising then, and takes
    the positions snapshot at that time."""
    res = analyze_birth_muhurta(
        dob="2026-06-20", lat=21.7333, lon=70.6167, place_name="Jetpur",
        chart_fn=build_muhurta_chart, time="09:30",
    )
    assert res["positions_time"] == "09:30"
    assert res["query_time"] == "09:30"
    highlighted = [w for w in res["windows"] if w["highlighted"]]
    assert len(highlighted) == 1  # exactly one Lagna rises at a given instant
    assert res["highlight_lagna"] == highlighted[0]["lagna_name"]


def test_worldly_potential_present_and_prominence_blends_ranking():
    """Every window carries a worldly-potential readout; opting into prominence
    blends it into the rank (0.6 base + 0.4 potential) without breaking the sort."""
    common = dict(dob="2026-06-20", lat=21.7333, lon=70.6167, place_name="Jetpur",
                  chart_fn=build_muhurta_chart)
    base = analyze_birth_muhurta(**common)
    assert base["optimize_prominence"] is False
    for w in base["windows"]:
        wp = w["worldly_potential"]
        assert wp is not None and 0.0 <= wp["score"] <= 100.0 and wp["note"]
        assert w["rank_score"] == w["overall"]  # default ranking = overall

    prom = analyze_birth_muhurta(**common, optimize_prominence=True)
    assert prom["optimize_prominence"] is True
    for w in prom["windows"]:
        expected = round(0.6 * w["overall"] + 0.4 * w["worldly_potential"]["score"], 1)
        assert w["rank_score"] == expected
    scores = [w["rank_score"] for w in prom["windows"]]
    assert scores == sorted(scores, reverse=True)
