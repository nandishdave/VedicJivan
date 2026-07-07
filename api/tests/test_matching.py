"""Tests for Ashtakoota (Guna Milap) horoscope matching — pinned to four
AstroSage reports (every koota, total and Mangal-Dosha grade)."""
import pytest

from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator.matching import compute_matching, mangal_dosha

_KN = ["Varna", "Vasya", "Tara", "Yoni", "Maitri", "Gana", "Bhakoot", "Nadi"]

# (label, boy(dob,tob,lat,lon), girl(...), per-koota points, total, boy/girl Mangal)
_CASES = [
    ("Praveen&Sonali", ("1985-09-19", "14:10", 16.383, 74.0),
     ("1988-05-14", "12:40", 20.55, 74.517),
     [1, 1, 1.5, 3, 5, 6, 0, 8], 25.5, "No", "Low"),
    ("Kushal&Sneha", ("1988-04-22", "16:15", 23.033, 72.583),
     ("1988-09-24", "12:45", 19.067, 72.867),
     [1, 2, 3, 3, 4, 0, 0, 0], 13, "Low", "Low"),
    ("Dhruv&Jigisha", ("1987-11-24", "07:55", 20.783, 70.7),
     ("1993-06-08", "11:35", 21.617, 71.217),
     [1, 2, 3, 2, 3, 6, 0, 8], 25, "Low", "High"),
    ("Rupal&Rupal", ("1997-05-23", "18:20", 23.8, 80.917),
     ("1998-09-25", "11:30", 22.967, 76.067),
     [1, 1, 1.5, 1, 3, 6, 0, 8], 21.5, "No", "No"),
]


def _chart(t):
    return build_muhurta_chart(dob=t[0], tob=t[1], lat=t[2], lon=t[3], with_shadbala=False)


@pytest.mark.parametrize("label,boy,girl,pts,total,bm,gm", _CASES)
def test_matching_reproduces_astrosage(label, boy, girl, pts, total, bm, gm):
    r = compute_matching(_chart(boy), _chart(girl))
    got = [k["points"] for k in r["kootas"]]
    assert got == pts, f"{label}: per-koota {got} != {pts}"
    assert r["total"] == total
    assert r["boy_mangal"] == bm and r["girl_mangal"] == gm


def test_result_shape():
    r = compute_matching(_chart(_CASES[0][1]), _chart(_CASES[0][2]))
    assert [k["koota"] for k in r["kootas"]] == _KN
    assert r["max_total"] == 36
    assert all("interpretation" in k and k["interpretation"] for k in r["kootas"])
    assert isinstance(r["verdict"], str) and r["verdict"]


def test_mangal_hits_structure():
    m = mangal_dosha(_chart(_CASES[2][2]))  # Jigisha — High, all three refs hit
    assert m["grade"] == "High"
    assert {"Lagna", "Moon", "Venus"} <= set(m["hits"])
