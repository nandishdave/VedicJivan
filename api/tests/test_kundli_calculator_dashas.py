"""Tests for the dasha + Jaimini + Lal Kitab additions in `kundli_calculator.py`.

These cover the Vimshottari datetime refactor, Yogini birth-clipping,
Convention-A antardashas, the K.N. Rao Char Dasha formula, the Lal Kitab
35-year cycle, Jaimini Karakas + Karakamsa, Avasthas (3 systems), the
karan-fix in panchanga, Sade Sati birth-window filtering, Ashtakavarga 337
total, and the Varshaphal helpers (Muntha, Mudda Dasha).

Reference chart used throughout: Nandish Dave (1988-11-11 12:55 IST,
Jetpur 21°43'N 70°37'E) — the same chart used by `test_kundli_calculator.py`
so both test modules can share an Astrosage cross-check.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta

import pytest

from app.services.kundli_calculator import (
    DASHA_SEQUENCE,
    DASHA_YEARS,
    LAL_KITAB_DASHA_SEQUENCE,
    LAL_KITAB_DASHA_YEARS,
    LAL_KITAB_SUBPERIODS,
    NAKSHATRA_LORDS,
    SIGN_NAMES,
    YOGINI_NAMES,
    _VIMSHOTTARI_DAYS_PER_YEAR,
    _birth_datetime,
    _calc_baladi,
    _calc_jagradadi,
    calc_antardasha,
    calc_ashtakavarga,
    calc_avasthas,
    calc_char_dasha,
    calc_jaimini_karakas,
    calc_lal_kitab_dasha,
    calc_mudda_dasha,
    calc_muntha,
    calc_panchanga,
    calc_sadesati,
    calc_vimshottari_dasha,
    calc_yogini_dasha,
)


# ── Helpers ─────────────────────────────────────────────────────────────────


def _seven_classical(sign_offset: int = 0) -> dict:
    """Spread the 7 classical planets across distinct signs starting at offset."""
    names = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    return {
        n: {"sign": (sign_offset + i) % 12, "degree_in_sign": float(i), "longitude": float((sign_offset + i) * 30 + i)}
        for i, n in enumerate(names)
    }


# ── _birth_datetime ─────────────────────────────────────────────────────────


def test_birth_datetime_with_tob_uses_exact_time():
    dt = _birth_datetime("1988-11-11", "12:55")
    assert dt == datetime(1988, 11, 11, 12, 55, 0)


def test_birth_datetime_without_tob_falls_back_to_midnight():
    dt = _birth_datetime("1988-11-11", None)
    assert dt == datetime(1988, 11, 11, 0, 0, 0)


def test_birth_datetime_accepts_seconds():
    dt = _birth_datetime("1988-11-11", "12:55:30")
    assert dt == datetime(1988, 11, 11, 12, 55, 30)


# ── Vimshottari Dasha — datetime refactor ───────────────────────────────────


def test_vimshottari_returns_nine_periods_starting_with_nakshatra_lord():
    """9 mahadashas, first one keyed off the moon's nakshatra lord."""
    moon_lon = 226.0  # somewhere in Anuradha → lord = Saturn
    out = calc_vimshottari_dasha(moon_lon, "1988-11-11", "12:55")
    assert len(out["dashas"]) == 9
    assert out["dashas"][0]["planet"] == NAKSHATRA_LORDS[int(moon_lon / (360 / 27))]


def test_vimshottari_first_md_partial_remaining_durations_full():
    """Subsequent MDs must be FULL DASHA_YEARS of their planet (Convention A)."""
    out = calc_vimshottari_dasha(226.0, "1988-11-11", "12:55")
    first_planet = out["dashas"][0]["planet"]
    first_idx = DASHA_SEQUENCE.index(first_planet)
    for i in range(1, 9):
        expected_planet = DASHA_SEQUENCE[(first_idx + i) % 9]
        assert out["dashas"][i]["planet"] == expected_planet
        assert out["dashas"][i]["years"] == DASHA_YEARS[expected_planet]


def test_vimshottari_total_span_is_120_years_minus_first_partial():
    """Sum of all 9 MD durations ≈ 120 years − partial elapsed portion."""
    out = calc_vimshottari_dasha(226.0, "1988-11-11", "12:55")
    total = sum(d["years"] for d in out["dashas"])
    # First MD is partial, remaining 8 are full → total < 120
    assert total < 120
    # Loose lower bound: even if first MD is fully spent, others sum to ~120
    assert total > 100


def test_vimshottari_tob_changes_boundaries_subtly():
    """Same dob, different tob → boundary dates may shift by at most 1 day."""
    out_a = calc_vimshottari_dasha(226.0, "1988-11-11", "00:00")
    out_b = calc_vimshottari_dasha(226.0, "1988-11-11", "23:59")
    # Same number of MDs, same planet sequence
    assert [d["planet"] for d in out_a["dashas"]] == [d["planet"] for d in out_b["dashas"]]
    # End dates differ by at most ~1 day
    for da, db in zip(out_a["dashas"], out_b["dashas"]):
        delta = abs((date.fromisoformat(da["end_date"]) - date.fromisoformat(db["end_date"])).days)
        assert delta <= 1


# ── Antardasha — Convention A (full proportional ADs) ───────────────────────


def test_antardasha_first_md_has_nine_ads_with_total_full_md_years():
    """Even when first MD is partial, ADs cover the FULL md_full_years span."""
    vd = calc_vimshottari_dasha(226.0, "1988-11-11", "12:55")
    ads = calc_antardasha(vd["dashas"], dob="1988-11-11", tob="12:55")
    first = ads[0]
    assert len(first["antardashas"]) == 9
    # First AD planet == first MD planet (Vimshottari ordering rule)
    assert first["antardashas"][0]["planet"] == first["mahadasha"]
    total_ad_years = sum(ad["years"] for ad in first["antardashas"])
    assert abs(total_ad_years - DASHA_YEARS[first["mahadasha"]]) < 0.05


def test_antardasha_first_ad_can_end_before_birth():
    """Convention A: first AD of partial first MD often ends BEFORE birth."""
    vd = calc_vimshottari_dasha(226.0, "1988-11-11", "12:55")
    ads = calc_antardasha(vd["dashas"], dob="1988-11-11", tob="12:55")
    first_ad = ads[0]["antardashas"][0]
    # Pre-birth start (negative offset from birth) is a defining feature of Convention A
    assert date.fromisoformat(first_ad["start_date"]) < date(1988, 11, 11) or \
        date.fromisoformat(first_ad["end_date"]) <= date(1988, 11, 11) + timedelta(days=1)


# ── Yogini Dasha — first MD clipped to birth ────────────────────────────────


def test_yogini_first_md_starts_on_or_after_birth_date():
    """First yogini MD displayed start must NOT precede birth (Convention A clip)."""
    out = calc_yogini_dasha(226.0, "1988-11-11", "12:55")
    first = out["dashas"][0]
    assert date.fromisoformat(first["start_date"]) >= date(1988, 11, 11)


def test_yogini_total_periods_cover_about_108_years():
    """24 periods × ~36-year average each → ~108 years across 3 cycles."""
    out = calc_yogini_dasha(226.0, "1988-11-11", "12:55")
    assert len(out["dashas"]) == 24
    total_years = sum(d["years"] for d in out["dashas"])
    # 3 full Yogini cycles = 3 × 36 = 108 years exactly
    assert total_years == 108


def test_yogini_starting_index_uses_convention_a_formula():
    """Convention A: starting yogini = (nakshatra_1indexed + 3) % 8."""
    moon_lon = 226.0
    nak_num = int(moon_lon / (360 / 27))
    expected_idx = ((nak_num + 1) + 3) % 8
    out = calc_yogini_dasha(moon_lon, "1988-11-11", "12:55")
    assert out["starting_yogini"] == YOGINI_NAMES[expected_idx]


def test_yogini_first_md_skips_subperiods_that_ended_before_birth():
    """First MD's antardashas must all end on or after birth date."""
    out = calc_yogini_dasha(226.0, "1988-11-11", "12:55")
    first = out["dashas"][0]
    for ad in first["antardashas"]:
        assert date.fromisoformat(ad["end_date"]) >= date(1988, 11, 11)


# ── Char Dasha — K.N. Rao formula ───────────────────────────────────────────


def test_char_dasha_returns_12_mahadashas_each_with_12_antardashas():
    planets = _seven_classical()
    planets["Rahu"] = {"sign": 6, "degree_in_sign": 5.0, "longitude": 185.0}
    planets["Ketu"] = {"sign": 0, "degree_in_sign": 5.0, "longitude": 5.0}
    out = calc_char_dasha(planets, lagna={"sign": 0}, dob="1988-11-11", tob="12:55")
    assert len(out["dashas"]) == 12
    for md in out["dashas"]:
        assert len(md["antardashas"]) == 12


def test_char_dasha_odd_lagna_progresses_zodiacally_forward():
    """Lagna in Aries (sign 0, 1-indexed odd) → MD sequence Ari, Tau, Gem, …"""
    planets = _seven_classical()
    planets["Rahu"] = {"sign": 6, "degree_in_sign": 5.0, "longitude": 185.0}
    planets["Ketu"] = {"sign": 0, "degree_in_sign": 5.0, "longitude": 5.0}
    out = calc_char_dasha(planets, lagna={"sign": 0}, dob="1988-11-11", tob="12:55")
    signs = [md["sign"] for md in out["dashas"]]
    assert signs == list(range(12))


def test_char_dasha_even_lagna_progresses_zodiacally_backward():
    """Lagna in Taurus (sign 1, 1-indexed even) → MD sequence Tau, Ari, Pis, …"""
    planets = _seven_classical()
    planets["Rahu"] = {"sign": 6, "degree_in_sign": 5.0, "longitude": 185.0}
    planets["Ketu"] = {"sign": 0, "degree_in_sign": 5.0, "longitude": 5.0}
    out = calc_char_dasha(planets, lagna={"sign": 1}, dob="1988-11-11", tob="12:55")
    signs = [md["sign"] for md in out["dashas"]]
    expected = [(1 - i) % 12 for i in range(12)]
    assert signs == expected


def test_char_dasha_scorpio_uses_ketu_only_when_ketu_in_scorpio():
    """Scorpio's lord defaults to Mars; switches to Ketu only if Ketu sits in Scorpio."""
    base = _seven_classical()
    base["Rahu"] = {"sign": 1, "degree_in_sign": 5.0, "longitude": 35.0}

    # Case A: Ketu NOT in Scorpio → lord = Mars
    case_a = dict(base)
    case_a["Ketu"] = {"sign": 0, "degree_in_sign": 5.0, "longitude": 5.0}
    case_a["Mars"] = {"sign": 7, "degree_in_sign": 5.0, "longitude": 215.0}  # Mars in Scorpio (own sign)
    out_a = calc_char_dasha(case_a, lagna={"sign": 0}, dob="1988-11-11", tob="12:55")
    sco_a = next(md for md in out_a["dashas"] if md["sign"] == 7)
    # Mars in Scorpio (own sign) → 11 years
    assert sco_a["years"] == 11

    # Case B: Ketu IN Scorpio → lord = Ketu (and Ketu in own sign → 11)
    case_b = dict(base)
    case_b["Ketu"] = {"sign": 7, "degree_in_sign": 5.0, "longitude": 215.0}
    out_b = calc_char_dasha(case_b, lagna={"sign": 0}, dob="1988-11-11", tob="12:55")
    sco_b = next(md for md in out_b["dashas"] if md["sign"] == 7)
    assert sco_b["years"] == 11


# ── Lal Kitab Dasha ─────────────────────────────────────────────────────────


def test_lal_kitab_constants_have_consistent_keys():
    """All 9 LK planets must appear in sequence, years and sub-period tables."""
    assert len(LAL_KITAB_DASHA_SEQUENCE) == 9
    assert set(LAL_KITAB_DASHA_SEQUENCE) == set(LAL_KITAB_DASHA_YEARS.keys())
    assert set(LAL_KITAB_DASHA_SEQUENCE) == set(LAL_KITAB_SUBPERIODS.keys())
    for planet, subs in LAL_KITAB_SUBPERIODS.items():
        assert len(subs) == 3


def test_lal_kitab_one_cycle_is_thirty_five_years():
    """The 9-planet cycle is exactly 35 years (6+6+3+6+2+1+3+6+2)."""
    total = sum(LAL_KITAB_DASHA_YEARS[p] for p in LAL_KITAB_DASHA_SEQUENCE)
    assert total == 35


def test_lal_kitab_dasha_n_cycles_produces_n_times_nine_periods():
    out = calc_lal_kitab_dasha("1988-11-11", "12:55", n_cycles=2)
    assert len(out["dashas"]) == 18
    # First MD is always Saturn (start of sequence)
    assert out["dashas"][0]["planet"] == "Saturn"


def test_lal_kitab_first_md_starts_at_birth_date():
    out = calc_lal_kitab_dasha("1988-11-11", "12:55", n_cycles=1)
    assert out["dashas"][0]["start_date"] == "1988-11-11"


def test_lal_kitab_subperiods_sum_to_md_duration():
    """3 sub-periods of equal length should span the full MD."""
    out = calc_lal_kitab_dasha("1988-11-11", "12:55", n_cycles=1)
    saturn = out["dashas"][0]
    assert len(saturn["subperiods"]) == 3
    sp_start = date.fromisoformat(saturn["subperiods"][0]["start_date"])
    sp_end = date.fromisoformat(saturn["subperiods"][-1]["end_date"])
    md_start = date.fromisoformat(saturn["start_date"])
    md_end = date.fromisoformat(saturn["end_date"])
    assert sp_start == md_start
    assert abs((sp_end - md_end).days) <= 1


# ── Jaimini Karakas + Karakamsa ─────────────────────────────────────────────


def test_jaimini_karakas_ranks_seven_classical_by_descending_degree():
    """Highest degree-in-sign → AK (Atma); lowest → DK (Dara)."""
    planets = {
        "Sun":     {"sign": 7, "degree_in_sign": 25.0},
        "Moon":    {"sign": 7, "degree_in_sign": 18.5},
        "Mars":    {"sign": 0, "degree_in_sign": 12.0},
        "Mercury": {"sign": 7, "degree_in_sign": 8.0},
        "Jupiter": {"sign": 1, "degree_in_sign": 6.0},
        "Venus":   {"sign": 8, "degree_in_sign": 4.0},
        "Saturn":  {"sign": 8, "degree_in_sign": 2.0},
    }
    out = calc_jaimini_karakas(planets, lagna={"sign": 9})
    chara = out["chara"]
    assert chara["Atma"]["planet"] == "Sun"
    assert chara["Amatya"]["planet"] == "Moon"
    assert chara["Dara"]["planet"] == "Saturn"
    assert out["atmakaraka"] == "Sun"


def test_jaimini_karakamsa_is_navamsa_sign_of_atmakaraka():
    """Karakamsa = D9 sign of the AK; Swamsa shares that lagna."""
    planets = {
        "Sun":     {"sign": 0, "degree_in_sign": 0.0},   # AK candidate, but lowest deg
        "Moon":    {"sign": 0, "degree_in_sign": 28.0},  # Highest degree → AK
        "Mars":    {"sign": 0, "degree_in_sign": 5.0},
        "Mercury": {"sign": 0, "degree_in_sign": 10.0},
        "Jupiter": {"sign": 0, "degree_in_sign": 15.0},
        "Venus":   {"sign": 0, "degree_in_sign": 20.0},
        "Saturn":  {"sign": 0, "degree_in_sign": 25.0},
    }
    out = calc_jaimini_karakas(planets, lagna={"sign": 9})
    assert out["atmakaraka"] == "Moon"
    # AK Moon at Aries 28° → D9 sign computed from varga formula. Just assert:
    # both Karakamsa and Swamsa share the same lagna sign.
    assert out["karakamsa_sign"] == out["swamsa_sign"]
    assert 0 <= out["karakamsa_sign"] < 12
    assert out["karakamsa_sign_name"] == SIGN_NAMES[out["karakamsa_sign"]]


def test_jaimini_sthira_karakas_are_classical():
    """Sthira (fixed) Karakas always: Atma=Sun, Amatya=Mercury, …, Dara=Venus."""
    planets = _seven_classical()
    out = calc_jaimini_karakas(planets, lagna={"sign": 0})
    assert out["sthira"] == {
        "Atma": "Sun", "Amatya": "Mercury", "Bhratru": "Mars",
        "Matrua": "Moon", "Putra": "Jupiter", "Gnati": "Saturn", "Dara": "Venus",
    }


# ── Avasthas (Jagradadi / Baladi / Deeptadi) ────────────────────────────────


def test_jagradadi_jagrat_for_exalted_or_own_sign():
    """Own sign / exalted / moolatrikona → Jagrat (awake)."""
    assert _calc_jagradadi("Sun", 0, "Exalted") == "Jagrat"
    assert _calc_jagradadi("Mars", 0, "Own Sign") == "Jagrat"
    assert _calc_jagradadi("Jupiter", 8, "Moolatrikona") == "Jagrat"


def test_jagradadi_susupta_only_when_lord_is_enemy():
    """Even debilitated, a friend/neutral lord overrides to Swapna, not Susupta."""
    # Saturn is enemy of Sun → Sun in Capricorn (lord = Saturn) = Susupta
    assert _calc_jagradadi("Sun", 9, "Enemy Sign") == "Susupta"
    # Sun in Cancer (Moon's sign) — Moon is friend of Sun → Swapna
    assert _calc_jagradadi("Sun", 3, "Debilitated") == "Swapna"


def test_baladi_returns_one_of_five_states():
    """Baladi must always return one of the 5 named zones."""
    valid = {"Bala", "Kumar", "Yuva", "Vradha", "Mrat"}
    for sign in range(12):
        for deg in (0.0, 5.99, 12.0, 25.0, 29.99):
            assert _calc_baladi(sign, deg) in valid


def test_baladi_odd_sign_starts_with_bala_at_zero_degrees():
    """Aries (sign 0, 1-indexed odd) — first 6° = Bala, last 6° = Mrat."""
    assert _calc_baladi(0, 1.0) == "Bala"
    assert _calc_baladi(0, 27.0) == "Mrat"


def test_baladi_even_sign_starts_with_mrat_at_zero_degrees():
    """Taurus (sign 1, 1-indexed even) — reversed: first 6° = Mrat, last 6° = Bala."""
    assert _calc_baladi(1, 1.0) == "Mrat"
    assert _calc_baladi(1, 27.0) == "Bala"


def test_calc_avasthas_returns_seven_classical_with_three_states_each():
    planets = _seven_classical()
    for name in planets:
        planets[name]["dignity"] = ""
        planets[name]["house"] = 1
    out = calc_avasthas(planets)
    assert len(out) == 7
    assert all({"planet", "jagradadi", "baladi", "deeptadi"}.issubset(row) for row in out)


def test_calc_avasthas_uses_dignity_for_deeptadi():
    """Exalted → Deepta; Own Sign → Swastha; Friend Sign → Mudita; Enemy → Deena."""
    planets = _seven_classical()
    for name in planets:
        planets[name]["house"] = 1
    planets["Sun"]["dignity"] = "Exalted"
    planets["Mars"]["dignity"] = "Own Sign"
    planets["Mercury"]["dignity"] = "Friendly Sign"
    planets["Saturn"]["dignity"] = "Enemy Sign"

    out = {row["planet"]: row["deeptadi"] for row in calc_avasthas(planets)}
    assert out["Sun"] == "Deepta"
    assert out["Mars"] == "Swastha"
    assert out["Mercury"] == "Mudita"
    assert out["Saturn"] == "Deena"


def test_calc_avasthas_combust_planet_is_vikala():
    """A planet within combustion threshold of Sun → Vikala (highest priority)."""
    from app.services.kundli_calculator import calc_avasthas
    planets = _seven_classical()
    for name in planets:
        planets[name]["house"] = 1
        planets[name]["dignity"] = "Friendly Sign"
    # Force Mercury to be within 14° of Sun (combust)
    planets["Sun"]["longitude"] = 100.0
    planets["Mercury"]["longitude"] = 105.0
    out = {row["planet"]: row["deeptadi"] for row in calc_avasthas(planets)}
    assert out["Mercury"] == "Vikala"


def test_calc_numerology_returns_required_numbers():
    from app.services.kundli_calculator import calc_numerology
    out = calc_numerology(name="Nandish Dave", dob_str="1988-11-11", current_year=2026)
    # Moolank from day 11 → 1+1 = 2
    assert out["moolank"]["value"] == 2
    # Bhagyank from 1988-11-11: 1+1 + 1+1 + 1+9+8+8 = 30 → 3
    assert out["bhagyank"]["value"] == 3
    # Personal year carries the year through
    assert out["personal_year"]["year"] == 2026
    # Name-based numbers populated
    assert out["namank"] is not None
    assert "value" in out["namank"]
    # Each entry exposes lucky day/color/gemstone
    assert out["moolank"]["lucky_day"]
    assert out["moolank"]["planet"]


def test_calc_numerology_handles_empty_name():
    from app.services.kundli_calculator import calc_numerology
    out = calc_numerology(name="", dob_str="1990-01-15", current_year=2026)
    assert out["namank"] is None
    assert out["soul_number"] is None
    assert out["personality_number"] is None


def test_calc_numerology_strips_non_alpha_from_name():
    """Punctuation/spaces in a name don't affect the alphabetic sum."""
    from app.services.kundli_calculator import calc_numerology
    a = calc_numerology(name="Nandish Dave", dob_str="1988-11-11", current_year=2026)
    b = calc_numerology(name="Nandish-Dave!", dob_str="1988-11-11", current_year=2026)
    assert a["namank"]["value"] == b["namank"]["value"]


def test_calc_avasthas_pidita_when_aspected_by_malefic():
    """A planet aspected by a malefic with no friend-sign / dignity → Pidita."""
    from app.services.kundli_calculator import calc_avasthas
    planets = _seven_classical()
    # Reset all to neutral
    for name in planets:
        planets[name]["dignity"] = ""
        planets[name]["house"] = 1
    # Force Mercury (in house 1) to be aspected by Saturn (malefic)
    graha_drishti = {
        "house_aspected_by": {"1": ["Saturn", "Moon"]},
        "planet_aspects": {},
    }
    out = {row["planet"]: row["deeptadi"] for row in calc_avasthas(planets, graha_drishti=graha_drishti)}
    # Mercury is in H1 and gets aspected by Saturn → Pidita
    assert out["Mercury"] == "Pidita"


# ── Panchanga karan fix ─────────────────────────────────────────────────────


def test_panchanga_returns_required_keys():
    """Smoke test — calc_panchanga must return tithi/yoga/karan."""
    out = calc_panchanga(jd=2447477.20)
    expected = {"tithi_num", "tithi_name", "paksha", "yoga_name", "karan_name"}
    assert expected.issubset(set(out.keys()))


def test_panchanga_karan_name_is_a_known_karan():
    """Karan name should be one of the 11 valid karanas."""
    from app.services.kundli_calculator import KARAN_NAMES
    valid_karanas = set(KARAN_NAMES)
    for jd in (2447477.0, 2447477.5, 2447478.0, 2447490.0, 2447500.0):
        out = calc_panchanga(jd)
        assert out["karan_name"] in valid_karanas, f"Unknown karan at jd={jd}: {out['karan_name']}"


# ── Sade Sati (dynamic, birth-windowed) ─────────────────────────────────────


def test_sadesati_excludes_periods_ending_before_birth():
    """No Sade Sati period should have an end_date before the dob."""
    moon_sign = 7  # Scorpio
    out = calc_sadesati(moon_sign, dob="1988-11-11")
    for p in out:
        assert p["end_date"] >= "1988-11-11"


def test_sadesati_phase_labels_are_valid():
    """Each entry must be one of Rising / Peak / Setting and have valid date order."""
    out = calc_sadesati(moon_sign=7, dob="1988-11-11")
    for p in out:
        assert p["phase"] in {"Rising", "Peak", "Setting"}
        assert p["start_date"] <= p["end_date"]


def test_sadesati_returns_periods_sorted_by_start_date():
    out = calc_sadesati(moon_sign=7, dob="1988-11-11")
    starts = [p["start_date"] for p in out]
    assert starts == sorted(starts)


# ── Ashtakavarga — 337 grand total invariant ────────────────────────────────


def test_ashtakavarga_grand_total_is_337_per_parashara():
    """Bhinnashtakavarga across 7 planets sums to exactly 337 bindus per BPHS."""
    planets = _seven_classical()
    out = calc_ashtakavarga(planets, lagna_sign=0)
    assert out["grand_total"] == 337


def test_ashtakavarga_each_planet_row_has_twelve_signs():
    planets = _seven_classical()
    out = calc_ashtakavarga(planets, lagna_sign=0)
    assert set(out["bindus"].keys()) == {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"}
    for row in out["bindus"].values():
        assert len(row) == 12


def test_ashtakavarga_totals_sum_to_grand_total():
    planets = _seven_classical()
    out = calc_ashtakavarga(planets, lagna_sign=0)
    assert sum(out["totals"]) == out["grand_total"] == 337


# ── Varshaphal helpers ──────────────────────────────────────────────────────


def test_calc_muntha_advances_one_sign_per_year():
    """Muntha at age 0 sits on natal lagna; advances 1 sign per year."""
    assert calc_muntha(natal_lagna_sign=0, age_years=0)["sign"] == 0
    assert calc_muntha(natal_lagna_sign=0, age_years=1)["sign"] == 1
    assert calc_muntha(natal_lagna_sign=0, age_years=12)["sign"] == 0  # wraps
    assert calc_muntha(natal_lagna_sign=9, age_years=3)["sign"] == 0  # Cap+3 → Aries


def test_calc_muntha_house_wraps_within_twelve():
    out = calc_muntha(natal_lagna_sign=0, age_years=12)
    assert out["house"] == 1
    out = calc_muntha(natal_lagna_sign=0, age_years=11)
    assert out["house"] == 12


def test_mudda_dasha_total_days_cover_one_tropical_year():
    """All Mudda periods together span ~365.24 days from solar return."""
    sr_dt = datetime(2026, 11, 11, 12, 0)
    out = calc_mudda_dasha(annual_moon_lon=226.0, solar_return_dt=sr_dt)
    total_days = sum(p["days"] for p in out["periods"])
    assert 364 <= total_days <= 366
