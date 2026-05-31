"""Completeness tests for the static datasets in `kundli_data.py`.

Each renderer downstream assumes a dataset has every key it indexes by — a
single missing entry blanks a section in the PDF without an obvious error.
These tests guard the schemas so a regression is caught at test-time rather
than at PDF-render-time.
"""

from __future__ import annotations

import pytest

from app.services.kundli_data import (
    BHAVA_DATA,
    FAVOURABLE,
    GHATAK,
    LAGNA_DATA,
    LAL_KITAB_DATA,
    MUDDA_DASHA_BHAV_DATA,
    MUNTHA_HOUSE_DATA,
    NAKSHATRA_DATA,
    NAKSHATRA_PADA_DATA,
    PLANET_IN_HOUSE,
)


SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]
NINE_PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]


# ── LAGNA_DATA ─────────────────────────────────────────────────────────────


def test_lagna_data_has_all_twelve_signs():
    assert set(LAGNA_DATA.keys()) == set(SIGNS)


def test_lagna_data_education_field_filled_for_every_sign():
    """`education` was added for all 12 signs in the recent commit — guard it."""
    for sign in SIGNS:
        edu = LAGNA_DATA[sign].get("education", "")
        assert edu and len(edu) > 30, f"{sign}.education is missing or too short"


def test_lagna_data_has_consistent_field_set():
    """Every sign should expose the same field keys — renderers index by name."""
    reference_keys = set(LAGNA_DATA["Aries"].keys())
    for sign in SIGNS:
        assert set(LAGNA_DATA[sign].keys()) == reference_keys, \
            f"{sign} has divergent fields: {set(LAGNA_DATA[sign].keys()) ^ reference_keys}"


# ── NAKSHATRA_PADA_DATA (108 entries: 27 nakshatras × 4 padas) ─────────────


def test_nakshatra_pada_data_covers_all_27_nakshatras():
    assert len(NAKSHATRA_PADA_DATA) == 27
    assert set(NAKSHATRA_PADA_DATA.keys()) == set(range(27))


def test_nakshatra_pada_data_has_four_padas_per_nakshatra():
    for nak_idx, padas in NAKSHATRA_PADA_DATA.items():
        assert set(padas.keys()) == {1, 2, 3, 4}, f"Nakshatra {nak_idx} missing pada(s)"


def test_nakshatra_pada_data_text_is_non_empty():
    """Smoke check — all 108 pada strings should be non-trivial."""
    empty = []
    for nak_idx, padas in NAKSHATRA_PADA_DATA.items():
        for pada_num, text in padas.items():
            if not text or len(text) < 20:
                empty.append((nak_idx, pada_num, text))
    assert not empty, f"Empty/short pada texts: {empty[:5]}"


# ── MUNTHA_HOUSE_DATA (12 bhav entries) ────────────────────────────────────


def test_muntha_house_data_has_12_houses():
    assert set(MUNTHA_HOUSE_DATA.keys()) == set(range(1, 13))


def test_muntha_house_data_text_is_non_empty():
    for h, text in MUNTHA_HOUSE_DATA.items():
        assert text and len(text) > 30, f"Muntha house {h} text missing/short"


# ── MUDDA_DASHA_BHAV_DATA (9 planets × 12 houses = 108 entries) ────────────


def test_mudda_dasha_bhav_data_has_nine_planets():
    assert set(MUDDA_DASHA_BHAV_DATA.keys()) == set(NINE_PLANETS)


def test_mudda_dasha_bhav_data_has_twelve_houses_per_planet():
    for planet, houses in MUDDA_DASHA_BHAV_DATA.items():
        assert set(houses.keys()) == set(range(1, 13)), \
            f"{planet} missing house(s) in MUDDA_DASHA_BHAV_DATA"


def test_mudda_dasha_bhav_data_total_is_108_entries():
    total = sum(len(h) for h in MUDDA_DASHA_BHAV_DATA.values())
    assert total == 9 * 12 == 108


# ── LAL_KITAB_DATA (108 entries: 9 planets × 12 houses) ────────────────────


def test_lal_kitab_data_has_nine_planets():
    assert set(LAL_KITAB_DATA.keys()) == set(NINE_PLANETS)


def test_lal_kitab_data_has_twelve_houses_per_planet():
    for planet, houses in LAL_KITAB_DATA.items():
        assert set(houses.keys()) == set(range(1, 13)), \
            f"{planet} missing house(s) in LAL_KITAB_DATA"


def test_lal_kitab_entries_have_prediction_and_remedies():
    """Every (planet, house) entry must expose a prediction + non-empty remedy list."""
    for planet, houses in LAL_KITAB_DATA.items():
        for h, entry in houses.items():
            assert "prediction" in entry, f"{planet} H{h} missing prediction"
            assert "remedies" in entry, f"{planet} H{h} missing remedies"
            assert isinstance(entry["remedies"], list), f"{planet} H{h} remedies not a list"
            assert len(entry["remedies"]) >= 1, f"{planet} H{h} has no remedies"
            assert len(entry["prediction"]) > 30, f"{planet} H{h} prediction too short"


# ── Existing dataset sanity (PLANET_IN_HOUSE / NAKSHATRA_DATA / BHAVA_DATA) ─


def test_planet_in_house_has_nine_planets_and_twelve_houses():
    assert set(PLANET_IN_HOUSE.keys()) == set(NINE_PLANETS)
    for planet, houses in PLANET_IN_HOUSE.items():
        assert set(houses.keys()) == set(range(1, 13)), f"{planet} missing house"


def test_nakshatra_data_has_27_entries():
    assert len(NAKSHATRA_DATA) == 27


def test_bhava_data_has_12_houses():
    assert set(BHAVA_DATA.keys()) == set(range(1, 13))


# ── FAVOURABLE / GHATAK already covered in test_kundli_calculator.py ───────
# (Sanity counts only here — the deep field-by-field check lives there.)


def test_favourable_and_ghatak_have_all_12_signs():
    assert set(FAVOURABLE.keys()) == set(SIGNS)
    assert set(GHATAK.keys()) == set(SIGNS)
