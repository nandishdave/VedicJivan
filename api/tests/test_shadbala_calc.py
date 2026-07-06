"""Tests for the Shadbala calculator (shadbala_table + endpoint). Pure reshape
+ Virupa→Rupa conversion; the endpoint builds a real chart."""
import pytest

from app.services.kundli_calculator.shadbala import shadbala_table

_7 = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_12 = _7 + ["Rahu", "Ketu", "Uranus", "Neptune", "Pluto"]


def _planet(rupas=5.7, req=5.0, ratio=1.14, rank=1):
    # Virupa values for the six balas + their sub-parts.
    return {
        "sthan_bala": 120, "dig_bala": 60, "kala_bala": 90, "chesta_bala": 30,
        "naisargeka_bala": 30, "drik_bala": 12,
        "ochcha_bala": 20, "saptavargaja_bala": 50, "ojayugma_bala": 15,
        "kendra_bala": 30, "drekkana_bala": 5,
        "nathonnatha_bala": 10, "paksha_bala": 20, "thribhaga_bala": 60,
        "abda_bala": 0, "masa_bala": 0, "vara_bala": 0, "hora_bala": 0,
        "ayana_bala": 0, "yuddha_bala": 0,
        "shadbala_rupas": rupas, "min_requirement": req, "ratio": ratio, "rank": rank,
    }


def test_reshape_and_virupa_to_rupa():
    out = shadbala_table({"shadbala": {"Sun": _planet()}})
    row = out["planets"][0]
    assert row["planet"] == "Sun"
    assert row["balas"]["sthana"] == 2.0   # 120 virupa / 60
    assert row["balas"]["drik"] == 0.2     # 12 / 60
    assert set(row["balas"]) == {"sthana", "dig", "kala", "cheshta", "naisargika", "drik"}
    assert row["total"] == 5.7 and row["required"] == 5.0 and row["ratio"] == 1.14
    assert row["sufficient"] is True
    assert len(row["sthana_parts"]) == 5 and len(row["kala_parts"]) == 9


def test_insufficient_ratio_flagged():
    out = shadbala_table({"shadbala": {"Saturn": _planet(rupas=4.0, req=5.0, ratio=0.8)}})
    assert out["planets"][0]["sufficient"] is False


def test_planets_in_classical_order():
    sb = {p: _planet(rank=i + 1) for i, p in enumerate(_7)}
    out = shadbala_table({"shadbala": sb})
    assert [p["planet"] for p in out["planets"]] == _7


def test_method_tags_classical_adapted_dispositor():
    sb = {p: _planet() for p in _7 + ["Rahu", "Uranus"]}
    out = shadbala_table({"shadbala": sb}, node_via={"Rahu": "Saturn"})
    by = {p["planet"]: p for p in out["planets"]}
    assert by["Sun"]["method"] == "classical" and by["Sun"]["via"] is None
    assert by["Uranus"]["method"] == "adapted" and by["Uranus"]["via"] is None
    assert by["Rahu"]["method"] == "dispositor" and by["Rahu"]["via"] == "Saturn"


# ── endpoint (real ephemeris chart) ──
_DOB, _TOB, _LAT, _LON = "1988-11-11", "12:55", 21.7333, 70.6167


@pytest.mark.asyncio
async def test_shadbala_endpoint(client):
    resp = await client.get(
        "/api/kundli/shadbala",
        params={"dob": _DOB, "tob": _TOB, "lat": _LAT, "lon": _LON},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert [p["planet"] for p in body["planets"]] == _12  # 7 + nodes + 3 outer
    by = {p["planet"]: p for p in body["planets"]}
    # Rahu/Ketu via the dispositor method; outer planets adapted; rest classical.
    assert by["Rahu"]["method"] == "dispositor" and by["Rahu"]["via"] in _7
    assert by["Ketu"]["method"] == "dispositor" and by["Ketu"]["via"] in _7
    assert by["Uranus"]["method"] == "adapted"
    assert by["Sun"]["method"] == "classical"
    for p in body["planets"]:
        # the six balas should sum to the total (within rounding)
        assert abs(sum(p["balas"].values()) - p["total"]) < 0.6
        assert isinstance(p["sufficient"], bool)
        assert p["ratio"] == round(p["total"] / p["required"], 2)


@pytest.mark.asyncio
async def test_shadbala_endpoint_bad_input_returns_422(client):
    resp = await client.get(
        "/api/kundli/shadbala",
        params={"dob": "not-a-date", "tob": _TOB, "lat": _LAT, "lon": _LON},
    )
    assert resp.status_code == 422
