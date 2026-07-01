"""Tests for the graded Raja-yoga scorer.

Synthetic charts (no ephemeris). Aries lagna → kendra lords 1=Mars, 4=Moon,
7=Venus, 10=Saturn; trikona lords 1=Mars, 5=Sun, 9=Jupiter. Longitudes are set
only to control combustion (Sun at 100°; 280° = far/not-combust, ~101° = combust).
"""
from app.services.kundli_calculator.raja_yoga import (
    raja_yoga_normalized,
    raja_yoga_score,
)


def _chart(lagna_sign, planets, aspects=None):
    return {
        "lagna": {"sign": lagna_sign},
        "planets": planets,
        "graha_drishti": {"planet_aspects": aspects or {}},
    }


def _aries(**overrides):
    p = {
        "Mars":    {"house": 1, "sign": 0, "dignity": "Own Sign", "longitude": 280},
        "Moon":    {"house": 4, "sign": 3, "dignity": "Own Sign", "longitude": 280},
        "Sun":     {"house": 5, "sign": 4, "dignity": "Neutral Sign", "longitude": 100},
        "Venus":   {"house": 7, "sign": 6, "dignity": "Own Sign", "longitude": 280},
        "Jupiter": {"house": 9, "sign": 8, "dignity": "Own Sign", "longitude": 280},
        "Saturn":  {"house": 10, "sign": 9, "dignity": "Own Sign", "longitude": 280},
        "Mercury": {"house": 3, "sign": 2, "dignity": "Neutral Sign", "longitude": 280},
    }
    p.update(overrides)
    return p


def test_no_association_scores_zero():
    score, links = raja_yoga_score(_chart(0, _aries()))
    assert score == 0.0 and links == []


def test_kendra_trikona_conjunction_is_a_raja_yoga():
    # 4th lord Moon + 9th lord Jupiter conjunct in the 4th (kendra).
    p = _aries(Jupiter={"house": 4, "sign": 8, "dignity": "Own Sign", "longitude": 280})
    score, links = raja_yoga_score(_chart(0, p))
    # conj(8) x grade 1.0 x dignity 0.8 x house-4 kendra(1.0) = 6.4
    assert abs(score - 6.4) < 0.01
    assert len(links) == 1 and links[0]["type"] == "conjunction"


def test_two_kendra_lords_is_not_a_raja_yoga():
    # 4th lord Moon + 7th lord Venus conjunct — both kendra, no trikona role.
    p = _aries(Venus={"house": 4, "sign": 6, "dignity": "Own Sign", "longitude": 280})
    assert raja_yoga_score(_chart(0, p))[0] == 0.0


def test_dharma_karmadhipati_outranks_a_plain_raja_yoga():
    plain = _aries(Jupiter={"house": 4, "sign": 8, "dignity": "Own Sign", "longitude": 280})   # 4L+9L
    dk = _aries(Jupiter={"house": 10, "sign": 8, "dignity": "Own Sign", "longitude": 280})      # 9L+10L
    assert raja_yoga_score(_chart(0, dk))[0] > raja_yoga_score(_chart(0, plain))[0]


def test_combustion_reduces_the_yoga():
    far = _aries(Jupiter={"house": 4, "sign": 8, "dignity": "Own Sign", "longitude": 280})
    combust = _aries(Jupiter={"house": 4, "sign": 8, "dignity": "Own Sign", "longitude": 101})  # ~1° from Sun
    s_far = raja_yoga_score(_chart(0, far))[0]
    s_combust, links = raja_yoga_score(_chart(0, combust))
    assert s_combust < s_far
    assert links[0]["combust"] is True


def test_debilitation_reduces_the_yoga():
    strong = _aries(Jupiter={"house": 4, "sign": 8, "dignity": "Own Sign", "longitude": 280})
    weak = _aries(Jupiter={"house": 4, "sign": 8, "dignity": "Debilitated", "longitude": 280})
    assert raja_yoga_score(_chart(0, weak))[0] < raja_yoga_score(_chart(0, strong))[0]


def test_dusthana_placement_reduces_the_yoga():
    kendra = _aries(Jupiter={"house": 4, "sign": 8, "dignity": "Own Sign", "longitude": 280})
    dusthana = _aries(
        Moon={"house": 6, "sign": 3, "dignity": "Own Sign", "longitude": 280},
        Jupiter={"house": 6, "sign": 8, "dignity": "Own Sign", "longitude": 280},
    )  # same yoga forming in the 6th
    assert raja_yoga_score(_chart(0, dusthana))[0] < raja_yoga_score(_chart(0, kendra))[0]


def test_raja_yoga_karaka_single_planet():
    # Capricorn: Venus owns the 5th (trikona) AND 10th (kendra) — a raja-yoga karaka.
    p = {
        "Saturn":  {"house": 1, "sign": 9, "dignity": "Own Sign", "longitude": 280},
        "Jupiter": {"house": 3, "sign": 11, "dignity": "Own Sign", "longitude": 280},
        "Mars":    {"house": 4, "sign": 0, "dignity": "Own Sign", "longitude": 280},
        "Venus":   {"house": 10, "sign": 6, "dignity": "Own Sign", "longitude": 280},
        "Mercury": {"house": 6, "sign": 2, "dignity": "Neutral Sign", "longitude": 280},
        "Moon":    {"house": 7, "sign": 3, "dignity": "Neutral Sign", "longitude": 280},
        "Sun":     {"house": 8, "sign": 4, "dignity": "Neutral Sign", "longitude": 100},
    }
    score, links = raja_yoga_score(_chart(9, p))
    assert score > 0.0
    assert any(link["type"] == "raja_karaka" for link in links)


def test_normalized_is_bounded_0_100():
    assert raja_yoga_normalized(_chart(0, _aries())) == 0.0
    n = raja_yoga_normalized(_chart(0, _aries(Jupiter={"house": 4, "sign": 8, "dignity": "Own Sign", "longitude": 280})))
    assert 0.0 <= n <= 100.0
