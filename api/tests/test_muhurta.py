"""Tests + regression guards for the Auspicious Birth-Time (Muhurta) engine.

Fast unit tests use hand-built chart dicts (no ephemeris). One slow test runs
the real engine to guard the Swiss-Ephemeris integration. The key guard is
``test_house_lord_dominates_karaka`` — it locks in the design decision that each
Lagna's per-aspect verdict is driven by the Bhava + Bhava-lord (which vary by
ascendant), not the karaka (constant across all 12 Lagnas).
"""
from app.services.kundli_calculator._core import SIGN_LORDS, SIGN_NAMES
from app.services.muhurta import (
    LIFE_ASPECTS,
    _aspect_score,
    _house_strength,
    _overall_score,
    _verdict,
    analyze_birth_muhurta,
    build_muhurta_chart,
)

_ALL = [
    "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn",
    "Rahu", "Ketu", "Uranus", "Neptune", "Pluto",
]


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


async def test_birth_endpoint_returns_analysis(client, mocker):
    canned = {"date": "2026-06-20", "windows": [{"rank": 1, "lagna_name": "Aries"}], "planet_positions": []}
    mocker.patch("app.routers.muhurta.analyze_birth_muhurta", return_value=canned)
    resp = await client.post(
        "/api/muhurta/birth",
        json={"date": "2026-06-20", "lat": 21.7333, "lon": 70.6167, "place_name": "Jetpur"},
    )
    assert resp.status_code == 200
    assert resp.json()["windows"][0]["lagna_name"] == "Aries"


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
