"""Tests for the upagraha (sub-planet) calculator — behaviour + Astrosage-verified
anchors (the 5 Kāya group and Gulika)."""
import pytest

from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import get_julian_day
from app.services.kundli_calculator.upagraha import (
    calc_upagrahas, upagraha_table, _kaya_group,
)

# Nandish — a day birth verified against Astrosage's Upagraha table.
_DOB, _TOB, _LAT, _LON = "1988-11-11", "12:55", 21.7333, 70.6167
_ALL = {"Dhuma", "Vyatipata", "Parivesha", "Indrachapa", "Upaketu",
        "Kaala", "Mrityu", "Arthaprahara", "Yamaghantaka", "Mandi", "Gulika"}


def _ctx():
    chart = build_muhurta_chart(dob=_DOB, tob=_TOB, lat=_LAT, lon=_LON, with_shadbala=False)
    jd = get_julian_day(_DOB, _TOB, _LAT, _LON)
    sun = chart["planets"]["Sun"]["longitude"]
    return calc_upagrahas(jd, _DOB, _LAT, _LON, sun), chart, jd, sun


def _sign(lon):
    return int((lon % 360) // 30)


def test_all_eleven_present_and_bounded():
    ups, *_ = _ctx()
    assert set(ups) == _ALL
    assert all(0.0 <= v < 360.0 for v in ups.values())


def test_kaya_group_matches_astrosage():
    """The 5 Sun-derived upagrahas — exact classical formulas (verified <2' vs Astrosage)."""
    ups, *_ = _ctx()
    assert _sign(ups["Dhuma"]) == 11                                  # Pisces 8°46'
    assert ups["Dhuma"] % 30 == pytest.approx(8.76, abs=0.05)
    assert _sign(ups["Indrachapa"]) == 5                              # Virgo 8°46'
    assert _sign(ups["Upaketu"]) == 5                                 # Virgo 25°26'


def test_upaketu_is_sun_minus_30():
    ups, _chart, _jd, sun = _ctx()
    assert ups["Upaketu"] == pytest.approx((sun - 30) % 360, abs=1e-6)


def test_kaya_formula_chain():
    k = _kaya_group(205.435)  # Sun at Libra 25°26'
    assert k["Dhuma"] == pytest.approx((205.435 + 133 + 20 / 60) % 360, abs=1e-9)
    assert k["Vyatipata"] == pytest.approx((360 - k["Dhuma"]) % 360, abs=1e-9)
    assert k["Parivesha"] == pytest.approx((k["Vyatipata"] + 180) % 360, abs=1e-9)


def test_gulika_matches_astrosage():
    """Gulika = Ascendant at the start of Saturn's day-portion — Scorpio ~12.8° (Astrosage)."""
    ups, *_ = _ctx()
    assert _sign(ups["Gulika"]) == 7                                 # Scorpio
    assert ups["Gulika"] % 30 == pytest.approx(12.79, abs=0.1)


def test_mandi_distinct_from_gulika_and_kaala():
    ups, *_ = _ctx()
    assert ups["Mandi"] != ups["Gulika"]
    assert ups["Mandi"] != ups["Kaala"]


def test_table_shape():
    _ups, chart, jd, sun = _ctx()
    t = upagraha_table(jd, _DOB, _LAT, _LON, sun, chart["lagna"]["sign"])
    assert len(t["upagrahas"]) == 11
    assert t["lagna_sign"] == chart["lagna"]["sign"]
    row = t["upagrahas"][0]
    assert set(row) >= {"name", "label", "abbr", "sign", "sign_abbr",
                        "degree", "dms", "nakshatra", "pada"}
    assert sum(len(v) for v in t["by_sign"].values()) == 11
