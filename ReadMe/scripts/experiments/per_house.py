# -*- coding: utf-8 -*-
"""Per-HOUSE breakdown (not combined): for each D1 house 1-12, what share of famous vs
ordinary charts have their STRONGEST-Vimsopaka planet there? Sorted by gap. Lets us pick
the house set from evidence, not pre-combined. (225 vs 96, fast)"""
import json, numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS, _get_dignity
from app.services.kundli_calculator.divisional import calc_divisional_charts
FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8")); ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55, "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}
_VARGA_W = {"D1": 3.5, "D2": 1, "D3": 1, "D4": 0.5, "D7": 0.5, "D9": 3, "D10": 0.5, "D12": 0.5,
            "D16": 2, "D20": 0.5, "D24": 0.5, "D27": 0.5, "D30": 1, "D40": 0.5, "D45": 0.5, "D60": 4}
def vim(pl, P, dv): return sum(w * (_DP.get(_get_dignity(pl, (P[pl]["sign"] if v == "D1" else dv[v][pl])), 45) / 100.0) for v, w in _VARGA_W.items())
def top_house(p):
    b = p["birth"]; c = build_muhurta_chart(dob=b["date"], tob=b["time"], lat=b["lat"], lon=b["lon"], with_shadbala=False)
    P, lag = c["planets"], c["lagna"]; dv = calc_divisional_charts(P, lag)
    vp = {q: vim(q, P, dv) for q in _C}; top = max(_C, key=lambda q: vp[q])
    return P[top]["house"]
HF = [top_house(p) for p in FAM]; HR = [top_house(p) for p in ORDD]
nF, nR = len(HF), len(HR)
HOUSE_NAME = {1: "self/body", 2: "wealth/face", 3: "courage", 4: "home/heart", 5: "creativity", 6: "enemies/debt",
              7: "partner", 8: "crisis/occult", 9: "fortune/dharma", 10: "career/status", 11: "gains/network", 12: "loss/moksha"}
print(f"famous={nF} ordinary={nR}")
print("\n=== STRONGEST-Vimsopaka planet's D1 house — per house, sorted by gap ===")
print(f"  {'house':>2} {'meaning':13} {'fam n':>6} {'fam%':>6} {'ord%':>6} {'gap':>7}")
rows = []
for h in range(1, 13):
    fpct = 100.0 * sum(1 for x in HF if x == h) / nF
    opct = 100.0 * sum(1 for x in HR if x == h) / nR
    rows.append((h, sum(1 for x in HF if x == h), fpct, opct, fpct - opct))
for h, fn, fp, op, gap in sorted(rows, key=lambda r: -r[4]):
    flag = " <= strong+" if gap >= 8 else (" <= NEGATIVE" if gap <= -4 else "")
    print(f"  {h:>2} {HOUSE_NAME[h]:13} {fn:>6} {fp:5.1f}% {op:5.1f}% {gap:+6.1f}%{flag}")
# cumulative: adding houses greedily by gap
print("\n=== cumulative separation as you add houses (greedy by gap) ===")
order = [r[0] for r in sorted(rows, key=lambda r: -r[4])]
cum = set()
for h in order:
    cum.add(h)
    fpct = 100.0 * sum(1 for x in HF if x in cum) / nF
    opct = 100.0 * sum(1 for x in HR if x in cum) / nR
    if rows[h-1][4] < -1: break  # stop once we hit clearly-negative houses
    print(f"  + house {h:>2} ({HOUSE_NAME[h]:11}) -> set {sorted(cum)}:  fam {fpct:4.0f}%  ord {opct:4.0f}%  gap {fpct-opct:+4.0f}%")
