"""Property-based tests for `kundli_calculator` using Hypothesis.

Where unit tests check "for input X, output is Y", property tests check
"for ANY valid input, this invariant always holds." Hypothesis generates
hundreds of random inputs and shrinks failing cases to a minimal example.

These guard the calculator against modular-arithmetic edge cases:
sign cusps (every 30°), nakshatra boundaries (every 13°20'), the wrap at
360°, and Convention-A partial-first-MD math at 0% and 100% nakshatra
elapsed.
"""

from __future__ import annotations

from datetime import date, timedelta

from hypothesis import given, settings, strategies as st

from app.services.kundli_calculator import (
    DASHA_SEQUENCE,
    DASHA_YEARS,
    LAL_KITAB_DASHA_SEQUENCE,
    LAL_KITAB_DASHA_YEARS,
    NAKSHATRA_LORDS,
    SIGN_NAMES,
    YOGINI_YEARS,
    _calc_baladi,
    _calc_jagradadi,
    calc_ashtakavarga,
    calc_char_dasha,
    calc_jaimini_karakas,
    calc_lal_kitab_dasha,
    calc_muntha,
    calc_panchanga,
    calc_vimshottari_dasha,
    calc_yogini_dasha,
)


# ── Reusable strategies ─────────────────────────────────────────────────────


# Float in [0, 360) — "any longitude on the zodiac"
longitude = st.floats(min_value=0.0, max_value=359.999, allow_nan=False, allow_infinity=False)
sign_index = st.integers(min_value=0, max_value=11)
deg_in_sign = st.floats(min_value=0.0, max_value=29.999, allow_nan=False, allow_infinity=False)
# DOB: any date between 1900 and 2050 — covers JD-cache boundaries
dob_strategy = st.dates(min_value=date(1900, 1, 1), max_value=date(2050, 12, 31))
tob_strategy = st.times()


# ── Vimshottari Dasha ──────────────────────────────────────────────────────


@given(moon_lon=longitude, dob=dob_strategy, tob=tob_strategy)
@settings(max_examples=100, deadline=None)
def test_vimshottari_always_returns_nine_periods(moon_lon, dob, tob):
    """Property: 9 mahadashas — always — regardless of moon position or DOB."""
    out = calc_vimshottari_dasha(moon_lon, dob.isoformat(), tob.strftime("%H:%M"))
    assert len(out["dashas"]) == 9


@given(moon_lon=longitude, dob=dob_strategy)
@settings(max_examples=100, deadline=None)
def test_vimshottari_total_years_within_120(moon_lon, dob):
    """Property: 1 partial + 8 full MDs ≤ 120 years (the full Vimshottari cycle)."""
    out = calc_vimshottari_dasha(moon_lon, dob.isoformat())
    total = sum(d["years"] for d in out["dashas"])
    assert 0 < total <= 120 + 0.01  # tolerance for float rounding


@given(moon_lon=longitude, dob=dob_strategy)
@settings(max_examples=100, deadline=None)
def test_vimshottari_planet_sequence_follows_nakshatra_lord(moon_lon, dob):
    """Property: First MD is always the moon's nakshatra lord; 8 follow in DASHA_SEQUENCE order."""
    out = calc_vimshottari_dasha(moon_lon, dob.isoformat())
    nak_num = int(moon_lon / (360 / 27))
    expected_first = NAKSHATRA_LORDS[nak_num]
    assert out["dashas"][0]["planet"] == expected_first
    first_idx = DASHA_SEQUENCE.index(expected_first)
    for i, d in enumerate(out["dashas"]):
        assert d["planet"] == DASHA_SEQUENCE[(first_idx + i) % 9]


@given(moon_lon=longitude, dob=dob_strategy)
@settings(max_examples=100, deadline=None)
def test_vimshottari_dates_chain_without_gaps_or_overlaps(moon_lon, dob):
    """Property: consecutive MDs share a boundary (no overlap, no gap).

    Discovered by Hypothesis: when the moon is in the very last fraction of
    its nakshatra (e.g. moon_lon = 359.998°), the first MD has only
    microseconds remaining and its start_date equals its end_date when
    rounded to a calendar day. So we cannot assert `start < end` strictly,
    but consecutive periods must still chain correctly.
    """
    out = calc_vimshottari_dasha(moon_lon, dob.isoformat())
    for i, d in enumerate(out["dashas"]):
        assert d["start_date"] <= d["end_date"]
        if i > 0:
            assert d["start_date"] == out["dashas"][i - 1]["end_date"]


# ── Yogini Dasha ───────────────────────────────────────────────────────────


@given(moon_lon=longitude, dob=dob_strategy)
@settings(max_examples=100, deadline=None)
def test_yogini_total_periods_cover_three_full_cycles(moon_lon, dob):
    """Property: 24 periods × YOGINI_YEARS sums to exactly 108 (3 × 36)."""
    out = calc_yogini_dasha(moon_lon, dob.isoformat())
    assert len(out["dashas"]) == 24
    assert sum(d["years"] for d in out["dashas"]) == 108


@given(moon_lon=longitude, dob=dob_strategy)
@settings(max_examples=100, deadline=None)
def test_yogini_first_md_displayed_start_never_precedes_birth(moon_lon, dob):
    """Property: Convention A clipping — first MD's displayed start ≥ birth date."""
    out = calc_yogini_dasha(moon_lon, dob.isoformat())
    assert out["dashas"][0]["start_date"] >= dob.isoformat()


# ── Char Dasha (K.N. Rao) ──────────────────────────────────────────────────


@st.composite
def planet_chart(draw):
    """Generate a stub planet dict with random sign placements for all 9 planets."""
    names = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
    return {
        n: {
            "sign": draw(sign_index),
            "degree_in_sign": draw(deg_in_sign),
            "longitude": draw(longitude),
        }
        for n in names
    }


@given(planets=planet_chart(), lagna=sign_index, dob=dob_strategy)
@settings(max_examples=100, deadline=None)
def test_char_dasha_always_returns_12_signs(planets, lagna, dob):
    """Property: 12 mahadasha signs, each appearing exactly once, starting at lagna."""
    out = calc_char_dasha(planets, lagna={"sign": lagna}, dob=dob.isoformat())
    assert len(out["dashas"]) == 12
    signs = [md["sign"] for md in out["dashas"]]
    assert sorted(signs) == list(range(12))  # every sign exactly once
    assert signs[0] == lagna  # starts at lagna


@given(planets=planet_chart(), lagna=sign_index, dob=dob_strategy)
@settings(max_examples=100, deadline=None)
def test_char_dasha_years_in_valid_range(planets, lagna, dob):
    """Property: K.N. Rao formula yields 1–12 years per sign (inclusive)."""
    out = calc_char_dasha(planets, lagna={"sign": lagna}, dob=dob.isoformat())
    for md in out["dashas"]:
        assert 1 <= md["years"] <= 12


# ── Lal Kitab Dasha ────────────────────────────────────────────────────────


@given(dob=dob_strategy, n_cycles=st.integers(min_value=1, max_value=5))
@settings(max_examples=50, deadline=None)
def test_lal_kitab_n_cycles_produces_n_times_nine_periods(dob, n_cycles):
    """Property: each cycle = 9 periods → n_cycles × 9 total."""
    out = calc_lal_kitab_dasha(dob.isoformat(), n_cycles=n_cycles)
    assert len(out["dashas"]) == n_cycles * 9


@given(dob=dob_strategy)
@settings(max_examples=50, deadline=None)
def test_lal_kitab_one_full_cycle_is_thirty_five_years(dob):
    """Property: each Lal Kitab cycle of 9 periods spans exactly 35 years."""
    out = calc_lal_kitab_dasha(dob.isoformat(), n_cycles=1)
    total = sum(LAL_KITAB_DASHA_YEARS[d["planet"]] for d in out["dashas"])
    assert total == 35


# ── Muntha (Varshaphal) ────────────────────────────────────────────────────


@given(natal_lagna=sign_index, age=st.integers(min_value=0, max_value=120))
def test_muntha_sign_within_zero_to_eleven(natal_lagna, age):
    """Property: muntha sign is always a valid 0–11 index, regardless of age."""
    out = calc_muntha(natal_lagna, age)
    assert 0 <= out["sign"] < 12
    assert 1 <= out["house"] <= 12
    assert out["sign_name"] == SIGN_NAMES[out["sign"]]


@given(natal_lagna=sign_index, age=st.integers(min_value=0, max_value=120))
def test_muntha_advances_one_per_year(natal_lagna, age):
    """Property: muntha at age N is exactly N signs ahead of the natal lagna."""
    out = calc_muntha(natal_lagna, age)
    assert out["sign"] == (natal_lagna + age) % 12


# ── Panchanga ──────────────────────────────────────────────────────────────


@given(jd=st.floats(min_value=2400000.0, max_value=2500000.0,
                    allow_nan=False, allow_infinity=False))
@settings(max_examples=30, deadline=None)
def test_panchanga_always_returns_required_keys(jd):
    """Property: any JD produces a fully populated panchanga dict."""
    out = calc_panchanga(jd)
    required = {"tithi_num", "tithi_name", "paksha", "yoga_name", "karan_name"}
    assert required.issubset(out.keys())
    assert 1 <= out["tithi_num"] <= 30
    assert out["paksha"] in {"Shukla", "Krishna"}


# ── Ashtakavarga ───────────────────────────────────────────────────────────


@given(planets=planet_chart(), lagna=sign_index)
@settings(max_examples=100, deadline=None)
def test_ashtakavarga_grand_total_invariant(planets, lagna):
    """Property: Sarvashtakavarga grand total is exactly 337 — Parashara."""
    # calc_ashtakavarga only consumes the 7 classical planets
    classical = {n: planets[n] for n in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]}
    out = calc_ashtakavarga(classical, lagna)
    assert out["grand_total"] == 337
    assert sum(out["totals"]) == 337


@given(planets=planet_chart(), lagna=sign_index)
@settings(max_examples=100, deadline=None)
def test_ashtakavarga_prasthar_matrix_consistent(planets, lagna):
    """Property: the Prastharashtakavarga detail matrix is consistent with the
    Bhinnashtakavarga totals — each planet's 8 contributor rows column-sum to
    that planet's `bindus`, and every cell is 0 or 1."""
    from app.services.kundli_calculator.ashtakavarga import (
        CONTRIBUTORS,
        EXPECTED_PLANET_TOTALS,
    )

    classical = {n: planets[n] for n in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]}
    out = calc_ashtakavarga(classical, lagna)

    for planet, expected_total in EXPECTED_PLANET_TOTALS.items():
        rows = out["prasthar"][planet]
        assert set(rows.keys()) == set(CONTRIBUTORS)
        # every cell is a single bindu (0 or 1)
        for contributor in CONTRIBUTORS:
            assert all(v in (0, 1) for v in rows[contributor])
        # column sums == the planet's Bhinnashtakavarga row
        col_sums = [sum(rows[c][s] for c in CONTRIBUTORS) for s in range(12)]
        assert col_sums == out["bindus"][planet]
        # whole matrix sums to the fixed classical per-planet total
        assert sum(sum(rows[c]) for c in CONTRIBUTORS) == expected_total


# ── Avastha helpers ────────────────────────────────────────────────────────


@given(sign=sign_index, deg=deg_in_sign)
def test_baladi_returns_one_of_five_states(sign, deg):
    """Property: Baladi always one of {Bala, Kumar, Yuva, Vradha, Mrat}."""
    assert _calc_baladi(sign, deg) in {"Bala", "Kumar", "Yuva", "Vradha", "Mrat"}


@given(
    planet=st.sampled_from(["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]),
    sign=sign_index,
    dignity=st.sampled_from(["", "Exalted", "Debilitated", "Own Sign", "Moolatrikona", "Friendly Sign", "Enemy Sign"]),
)
def test_jagradadi_returns_one_of_three_states(planet, sign, dignity):
    """Property: Jagradadi always one of {Jagrat, Swapna, Susupta}."""
    assert _calc_jagradadi(planet, sign, dignity) in {"Jagrat", "Swapna", "Susupta"}


# ── Jaimini Karakas ────────────────────────────────────────────────────────


@given(planets=planet_chart(), lagna=sign_index)
@settings(max_examples=50, deadline=None)
def test_jaimini_assigns_seven_distinct_karaka_roles(planets, lagna):
    """Property: 7 chara karakas, each a distinct planet from the 7 classical."""
    out = calc_jaimini_karakas(planets, lagna={"sign": lagna})
    chara = out["chara"]
    classical = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"}
    assigned = {role["planet"] for role in chara.values()}
    assert assigned.issubset(classical)
    assert len(chara) == 7  # 7 roles
