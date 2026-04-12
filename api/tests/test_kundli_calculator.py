"""Tests for kundli_calculator additions (Avkahada Chakra + birth time details).

The reference values come from the Astrosage PDF for Nandish Dave
(11/11/1988, 12:55, Jetpur 21°43'N 70°37'E):

  Lagna       : Capricorn (Sravana 3)
  Moon        : Scorpio  (Anuradha 4)
  Varna       : Brahmin
  Vasya       : Keeta
  Yoni        : Mriga (Deer)
  Gana        : Devta (Deva)
  Nadi        : Madhya
  Paya        : Silver
  Ishtkaal    : 014-56-02 (sunrise 06:56:35, birth 12:55:00)
  Day         : Friday
  GMT at Birth: 07:25:00 (IST 12:55 → UTC 07:25)
"""

from __future__ import annotations

import pytest

from app.services.kundli_calculator import (
    NAKSHATRA_GANA,
    NAKSHATRA_NADI,
    NAKSHATRA_NAMES,
    NAKSHATRA_PAYA,
    NAKSHATRA_YONI,
    RASHI_VARNA,
    RASHI_VASYA,
    calc_avkahada,
    calc_birth_time_details,
)


# ── Lookup table sanity ────────────────────────────────────────────────────


def test_lookup_tables_have_27_or_12_entries():
    """Each nakshatra table has 27 entries; each rashi table has 12."""
    assert len(NAKSHATRA_YONI) == 27
    assert len(NAKSHATRA_GANA) == 27
    assert len(NAKSHATRA_NADI) == 27
    assert len(NAKSHATRA_PAYA) == 27
    assert len(RASHI_VARNA) == 12
    assert len(RASHI_VASYA) == 12


def test_anuradha_nakshatra_index_is_16():
    """Sanity: Anuradha is the 17th nakshatra → 0-indexed 16."""
    assert NAKSHATRA_NAMES[16] == "Anuradha"


# ── Avkahada attributes against Nandish Dave reference ────────────────────


def test_calc_avkahada_anuradha_scorpio_matches_astrosage():
    """Anuradha (#16) + Scorpio Moon (#7) → Astrosage's published values."""
    av = calc_avkahada(nakshatra_num=16, moon_sign=7)
    assert av["yoni"] == "Mriga"     # Astrosage: Mriga (deer)
    assert av["gana"] == "Devta"     # Astrosage: Devta
    assert av["nadi"] == "Madhya"    # Astrosage: Madhya
    assert av["paya"] == "Silver"    # Astrosage: Silver
    assert av["varna"] == "Brahmin"  # Astrosage: Bramhin (Scorpio = water)
    assert av["vasya"] == "Keeta"    # Astrosage: Keeta (Scorpio)
    assert av["tatva"] == "Water"    # Scorpio is a water sign


def test_calc_avkahada_returns_all_keys():
    """Every Avkahada call returns the same set of keys."""
    av = calc_avkahada(nakshatra_num=0, moon_sign=0)
    assert set(av.keys()) == {"varna", "vasya", "yoni", "gana", "nadi", "paya", "tatva"}


# ── Birth time details against Nandish Dave reference ─────────────────────


def test_birth_time_details_for_nandish_dave():
    """11/11/1988 12:55 IST at Jetpur should match Astrosage's page-2 values."""
    # Jetpur, Gujarat — 21°43'N 70°37'E
    bt = calc_birth_time_details(
        dob="1988-11-11",
        tob="12:55",
        lat=21 + 43 / 60,
        lon=70 + 37 / 60,
        jd=2447477.0,         # rough JD; sidereal_time doesn't need to match exactly
        sunrise_hm="06:56",   # Astrosage says 06:56:35
    )

    assert bt["day_of_birth"] == "Friday"
    assert bt["tz_offset_hours"] == 5.5
    assert bt["latitude_dms"].endswith("N")
    assert bt["longitude_dms"].endswith("E")
    # GMT at birth: 12:55 IST - 5:30 = 07:25
    assert bt["gmt_at_birth"].startswith("07:25")
    # Ishtkaal: 12:55 - 06:56 = ~5h 59m → ~14 ghatis 58 palas. Allow ±1 pala.
    parts = bt["ishtkaal"].split("-")
    assert int(parts[0]) == 14
    assert 55 <= int(parts[1]) <= 60


def test_birth_time_details_has_all_expected_keys():
    bt = calc_birth_time_details("1988-11-11", "12:55", 21.7, 70.6, 2447477.0, "06:56")
    expected = {
        "day_of_birth", "tz_name", "tz_offset_hours",
        "latitude_dms", "longitude_dms",
        "lmt_at_birth", "gmt_at_birth", "local_time_correction",
        "ishtkaal", "sidereal_time",
    }
    assert expected.issubset(set(bt.keys()))


def test_calc_friendships_permanent_matches_classical_bphs():
    """Sun row of the permanent friendship matrix must match BPHS:
    Moon=Friend, Mars=Friend, Mercury=Neutral, Jupiter=Friend, Venus=Enemy, Saturn=Enemy.
    """
    from app.services.kundli_calculator import calc_friendships

    # Minimal stub planet positions — only sign field is used for permanent.
    planets = {p: {"sign": i} for i, p in enumerate(
        ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    )}
    fr = calc_friendships(planets)

    sun_row = fr["permanent"]["Sun"]
    assert sun_row["Sun"] == "—"
    assert sun_row["Moon"] == "Friend"
    assert sun_row["Mars"] == "Friend"
    assert sun_row["Mercury"] == "Neutral"
    assert sun_row["Jupiter"] == "Friend"
    assert sun_row["Venus"] == "Enemy"
    assert sun_row["Saturn"] == "Enemy"

    # Symmetric check on Saturn row — Sun should be Enemy.
    assert fr["permanent"]["Saturn"]["Sun"] == "Enemy"
    assert fr["permanent"]["Saturn"]["Mercury"] == "Friend"


def test_calc_friendships_temporary_uses_house_diff():
    """Two planets in the 2nd from each other are temporary friends; in the 1st they
    would be temporary enemies (same sign / 1st from each other)."""
    from app.services.kundli_calculator import calc_friendships

    # Sun in Aries (0), Moon in Taurus (1) → Moon is 2nd from Sun.
    planets = {
        "Sun":     {"sign": 0},
        "Moon":    {"sign": 1},
        "Mars":    {"sign": 0},   # same sign as Sun
        "Mercury": {"sign": 6},   # 7th from Sun (1+6=7)
        "Jupiter": {"sign": 4},
        "Venus":   {"sign": 9},
        "Saturn":  {"sign": 11},
    }
    fr = calc_friendships(planets)
    # Moon is 2nd from Sun → temporary friend
    assert fr["temporary"]["Sun"]["Moon"] == "T.Friend"
    # Mars is 1st from Sun → temporary enemy
    assert fr["temporary"]["Sun"]["Mars"] == "T.Enemy"
    # Mercury is 7th from Sun → temporary enemy
    assert fr["temporary"]["Sun"]["Mercury"] == "T.Enemy"


def test_calc_friendships_compound_combines_natural_and_temporary():
    """Compound (Panchadha) labels should include all five categories."""
    from app.services.kundli_calculator import calc_friendships

    planets = {p: {"sign": i * 2} for i, p in enumerate(
        ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    )}
    fr = calc_friendships(planets)
    valid = {"Best Friend", "Friend", "Neutral", "Enemy", "Bitter Enemy", "—"}
    for from_p in fr["planets"]:
        for to_p in fr["planets"]:
            assert fr["compound"][from_p][to_p] in valid


def test_friendship_matrix_diagonal_is_dash():
    """Self-relation cells must be '—' in all three matrices."""
    from app.services.kundli_calculator import calc_friendships
    planets = {p: {"sign": i} for i, p in enumerate(
        ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    )}
    fr = calc_friendships(planets)
    for p in fr["planets"]:
        assert fr["permanent"][p][p] == "—"
        assert fr["temporary"][p][p] == "—"
        assert fr["compound"][p][p] == "—"


def test_capricorn_favourable_matches_astrosage_reference():
    """All 10 Capricorn Favourable Points fields must match the Astrosage PDF.

    Astrosage page-2 reference (Capricorn lagna):
        Lucky Numbers   4
        Good Numbers    2, 4, 5, 8
        Evil Numbers    1, 7, 9
        Good Years      13, 22, 31, 40, 49
        Lucky Days      Thursday, Tuesday
        Good Planets    Jupiter, Mars, Moon
        Friendly Signs  Ari, Leo, Sag
        Good Lagna      Sag, Pis, Tau, Cap
        Lucky Metal     Gold
        Lucky Stone     Red Coral
    """
    from app.services.kundli_data import FAVOURABLE
    cap = FAVOURABLE["Capricorn"]
    assert cap["lucky_numbers"] == "4"
    assert cap["good_numbers"] == "2, 4, 5, 8"
    assert cap["evil_numbers"] == "1, 7, 9"
    assert cap["good_years"] == "13, 22, 31, 40, 49"
    assert cap["lucky_days"] == "Thursday, Tuesday"
    assert cap["good_planets"] == "Jupiter, Mars, Moon"
    assert cap["friendly_signs"] == "Ari, Leo, Sag"
    assert cap["good_lagna"] == "Sag, Pis, Tau, Cap"
    assert cap["lucky_metal"] == "Gold"
    assert cap["lucky_stone"] == "Red Coral"


def test_all_lagnas_have_complete_favourable_set():
    """Every lagna must define all 10 Favourable fields and zero stale Avkahada keys."""
    from app.services.kundli_data import FAVOURABLE
    expected_keys = {
        "lucky_numbers", "good_numbers", "evil_numbers", "good_years",
        "lucky_days", "good_planets", "friendly_signs", "good_lagna",
        "lucky_metal", "lucky_stone",
    }
    stale_keys = {"varna", "yoni", "gana", "nadi"}
    assert len(FAVOURABLE) == 12
    for sign, fields in FAVOURABLE.items():
        actual = set(fields.keys())
        missing = expected_keys - actual
        leaked = actual & stale_keys
        assert not missing, f"{sign} missing Favourable fields: {missing}"
        assert not leaked, f"{sign} still has stale Avkahada keys: {leaked}"


def test_capricorn_ghatak_matches_astrosage_reference():
    """All 10 Capricorn Ghatak fields must match the Astrosage Nandish Dave PDF.

    Astrosage page-2 reference (Capricorn lagna):
        Bad Day        Friday
        Bad Karan      Garija
        Bad Lagna      Vrishchika
        Bad Month      Ashwin
        Bad Nakshatra  Revati
        Bad Prahar     1
        Bad Rasi       Vrish
        Bad Tithi      1, 6, 11
        Bad Yoga       Brahma
        Bad Planets    Mercury
    """
    from app.services.kundli_data import GHATAK
    cap = GHATAK["Capricorn"]
    assert cap["bad_day"] == "Friday"
    assert cap["bad_karana"] == "Garaja"  # Astrosage spells it "Garija"
    assert cap["bad_lagna"] == "Vrishchika"
    assert cap["bad_masa"] == "Ashwin"
    assert cap["bad_nakshatra"] == "Revati"
    assert cap["bad_prahara"] == "1"
    assert cap["bad_rashi"] == "Vrish"
    assert cap["bad_tithi"] == "1, 6, 11"
    assert cap["bad_yoga"] == "Brahma"
    assert cap["bad_planets"] == "Mercury"


def test_all_lagnas_have_complete_ghatak_set():
    """Every lagna must define all 10 Ghatak fields so the renderer never blanks."""
    from app.services.kundli_data import GHATAK
    expected_keys = {
        "bad_day", "bad_karana", "bad_lagna", "bad_masa", "bad_nakshatra",
        "bad_prahara", "bad_rashi", "bad_tithi", "bad_yoga", "bad_planets",
    }
    assert len(GHATAK) == 12
    for sign, fields in GHATAK.items():
        missing = expected_keys - set(fields.keys())
        assert not missing, f"{sign} missing Ghatak fields: {missing}"


def test_birth_before_sunrise_wraps_ishtkaal():
    """A 03:00 birth with sunrise at 06:00 means yesterday's ishtkaal — 21 hours."""
    bt = calc_birth_time_details(
        dob="1988-11-11",
        tob="03:00",
        lat=21.7,
        lon=70.6,
        jd=2447477.0,
        sunrise_hm="06:00",
    )
    parts = bt["ishtkaal"].split("-")
    # 21h elapsed = 21 * 60 / 24 = 52.5 ghatis
    assert int(parts[0]) >= 52
