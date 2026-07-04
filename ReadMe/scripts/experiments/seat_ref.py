# -*- coding: utf-8 -*-
"""REF (famous_mean, ordinary_mean, pooled_std) for the strongest-Vimsopaka planet
seated in {1,2,4,5,11}. Fast (no shadbala)."""
import json, numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import _get_dignity
from app.services.kundli_calculator.divisional import calc_divisional_charts
FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8")); ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55, "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}
_VARGA_W = {"D1": 3.5, "D2": 1, "D3": 1, "D4": 0.5, "D7": 0.5, "D9": 3, "D10": 0.5, "D12": 0.5,
            "D16": 2, "D20": 0.5, "D24": 0.5, "D27": 0.5, "D30": 1, "D40": 0.5, "D45": 0.5, "D60": 4}
SEAT = {1, 2, 4, 5, 11}
def seat(p):
    b = p["birth"]; c = build_muhurta_chart(dob=b["date"], tob=b["time"], lat=b["lat"], lon=b["lon"], with_shadbala=False)
    P, lag = c["planets"], c["lagna"]; dv = calc_divisional_charts(P, lag)
    vim = {q: sum(w * (_DP.get(_get_dignity(q, (P[q]["sign"] if v == "D1" else dv[v][q])), 45) / 100.0) for v, w in _VARGA_W.items()) for q in _C}
    top = max(_C, key=lambda q: vim[q])
    return 1.0 if P[top]["house"] in SEAT else 0.0
F = np.array([seat(p) for p in FAM]); R = np.array([seat(p) for p in ORDD])
allv = np.concatenate([F, R])
print(f"seat{{1,2,4,5,11}}: fam={F.mean():.4f}  ord={R.mean():.4f}  pooled_std={allv.std(ddof=1):.4f}")
print(f"REF tuple: ({F.mean():.4f}, {R.mean():.4f}, {allv.std(ddof=1):.4f})")
