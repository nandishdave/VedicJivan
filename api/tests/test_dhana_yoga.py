"""Tests for the graded Dhana-yoga scorer (app.services.kundli_calculator.dhana_yoga).

Charts are built synthetically (no ephemeris) so the grading logic is exercised
deterministically. Aries lagna → money-lords 1=Mars, 2=Venus, 5=Sun, 9=Jupiter,
11=Saturn; Leo lagna → Mercury owns both 2 and 11.
"""
from app.services.kundli_calculator.dhana_yoga import (
    dhana_yoga_normalized,
    dhana_yoga_score,
)


def _chart(lagna_sign, planets, aspects=None):
    return {
        "lagna": {"sign": lagna_sign},
        "planets": planets,
        "graha_drishti": {"planet_aspects": aspects or {}},
    }


# Aries money-lords each in their OWN sign + distinct houses = no association.
_NO_YOGA = {
    "Mars": {"house": 1, "sign": 0, "dignity": "Own Sign"},
    "Venus": {"house": 2, "sign": 1, "dignity": "Own Sign"},
    "Sun": {"house": 5, "sign": 4, "dignity": "Own Sign"},
    "Jupiter": {"house": 9, "sign": 8, "dignity": "Own Sign"},
    "Saturn": {"house": 11, "sign": 10, "dignity": "Own Sign"},
}


def test_no_connection_scores_zero():
    score, links = dhana_yoga_score(_chart(0, _NO_YOGA))
    assert score == 0.0
    assert links == []


def test_conjunction_of_two_core_lords():
    # 1L Mars + 2L Venus conjunct in house 1, both Own Sign (0.8), good house (1.0).
    planets = dict(_NO_YOGA, Venus={"house": 1, "sign": 1, "dignity": "Own Sign"})
    score, links = dhana_yoga_score(_chart(0, planets))
    # conjunction(8) x both-core(1.0) x avg-dignity(0.8) x house-1(1.0) = 6.4
    assert abs(score - 6.4) < 0.01
    assert len(links) == 1 and links[0]["type"] == "conjunction"


def test_dignity_dilutes_the_yoga():
    strong = dict(_NO_YOGA, Venus={"house": 1, "sign": 1, "dignity": "Own Sign"})
    weak = dict(_NO_YOGA, Venus={"house": 1, "sign": 1, "dignity": "Debilitated"})
    assert dhana_yoga_score(_chart(0, weak))[0] < dhana_yoga_score(_chart(0, strong))[0]


def test_bad_house_dilutes_the_yoga():
    good = {**_NO_YOGA,
            "Mars": {"house": 5, "sign": 0, "dignity": "Own Sign"},
            "Venus": {"house": 5, "sign": 1, "dignity": "Own Sign"}}   # conj in 5th (good)
    bad = {**_NO_YOGA,
           "Mars": {"house": 6, "sign": 0, "dignity": "Own Sign"},
           "Venus": {"house": 6, "sign": 1, "dignity": "Own Sign"}}    # conj in 6th (dusthana)
    assert dhana_yoga_score(_chart(0, bad))[0] < dhana_yoga_score(_chart(0, good))[0]


def test_single_planet_owning_2_and_11_is_an_inherent_link():
    # Leo lagna: Mercury lords both 2 (Virgo) and 11 (Gemini) — the case the old
    # crude wealth flag was blind to.
    planets = {
        "Sun": {"house": 1, "sign": 4, "dignity": "Own Sign"},
        "Mercury": {"house": 2, "sign": 5, "dignity": "Own Sign"},
        "Jupiter": {"house": 5, "sign": 8, "dignity": "Own Sign"},
        "Mars": {"house": 9, "sign": 0, "dignity": "Own Sign"},
    }
    score, links = dhana_yoga_score(_chart(4, planets))
    # inherent(7) x both-core(1.0) x Mercury Own(0.8) x house-2(1.0) = 5.6
    assert abs(score - 5.6) < 0.01
    assert any(link["type"] == "inherent" for link in links)


def test_parivartana_outranks_one_way_aspect():
    # exchange: Mars in Venus's sign (Taurus) and Venus in Mars's sign (Aries).
    exch = {**_NO_YOGA,
            "Mars": {"house": 2, "sign": 1, "dignity": "Own Sign"},
            "Venus": {"house": 1, "sign": 0, "dignity": "Own Sign"}}
    score, links = dhana_yoga_score(_chart(0, exch))
    assert links[0]["type"] == "parivartana"
    assert score > 6.4  # a parivartana (10) beats the conjunction (8) baseline


def test_normalized_is_bounded_0_100():
    assert dhana_yoga_normalized(_chart(0, _NO_YOGA)) == 0.0
    n = dhana_yoga_normalized(_chart(0, dict(_NO_YOGA, Venus={"house": 1, "sign": 1, "dignity": "Own Sign"})))
    assert 0.0 <= n <= 100.0
