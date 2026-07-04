# -*- coding: utf-8 -*-
"""Refinements to the 'strongest-Vimsopaka planet's house' rule (fast, no shadbala):
(1) which HOUSE SET separates best (narrow vs wide)?  (2) does it matter whether the
strongest planet is a FUNCTIONAL BENEFIC (trikona lord)? Descriptive fam-vs-ord. (225/96)"""
import json, numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS, _get_dignity
from app.services.kundli_calculator.divisional import calc_divisional_charts
FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8")); ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55, "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}
_VARGA_W = {"D1": 3.5, "D2": 1, "D3": 1, "D4": 0.5, "D7": 0.5, "D9": 3, "D10": 0.5, "D12": 0.5,
            "D16": 2, "D20": 0.5, "D24": 0.5, "D27": 0.5, "D30": 1, "D40": 0.5, "D45": 0.5, "D60": 4}
def vimsopaka(pl, P, dv):
    return sum(w * (_DP.get(_get_dignity(pl, (P[pl]["sign"] if v == "D1" else dv[v][pl])), 45) / 100.0) for v, w in _VARGA_W.items())
def row(p):
    b = p["birth"]; c = build_muhurta_chart(dob=b["date"], tob=b["time"], lat=b["lat"], lon=b["lon"], with_shadbala=False)
    P, lag = c["planets"], c["lagna"]; ls = lag["sign"]; dv = calc_divisional_charts(P, lag)
    vp = {q: vimsopaka(q, P, dv) for q in _C}
    fb = {SIGN_LORDS[(ls + h) % 12] for h in (0, 4, 8)}       # functional benefics = trikona lords
    top = max(_C, key=lambda q: vp[q])                          # overall strongest
    top_fb = max((q for q in _C if q in fb), key=lambda q: vp[q])  # strongest functional benefic
    return {"top_house": P[top]["house"], "top_is_fb": top in fb,
            "topfb_house": P[top_fb]["house"], "topfb_vim": vp[top_fb]}
FR = [row(p) for p in FAM]; RR = [row(p) for p in ORDD]
def rate(rows, pred): return float(np.mean([1.0 if pred(r) else 0.0 for r in rows]))
def auc_bin(rows_f, rows_r, pred):
    f = np.array([1.0 if pred(r) else 0.0 for r in rows_f]); r = np.array([1.0 if pred(r_) else 0.0 for r_ in rows_r])
    return float(np.mean([np.mean(x > r) + 0.5 * np.mean(x == r) for x in f]))
SETS = {
    "{1,2,11}": {1, 2, 11}, "{1,2,10,11}": {1, 2, 10, 11}, "{1,10,11}": {1, 10, 11},
    "{1,2,4,5,9,10,11} (yours)": {1, 2, 4, 5, 9, 10, 11}, "{1,2,4,5,10,11}": {1, 2, 4, 5, 10, 11},
    "{1,4,7,10} kendra": {1, 4, 7, 10}, "{1,5,9} trikona": {1, 5, 9},
    "NOT {6,8,12} dusthana": None, "NOT {6,8}": None,
}
print("=== (1) STRONGEST planet's D1 house in <SET> — famous% vs ordinary% (higher gap = better) ===")
print(f"  {'house set':26} {'fam%':>6} {'ord%':>6} {'gap':>6} {'AUC':>6}")
for name, s in SETS.items():
    if s is None:
        excl = {6, 8, 12} if "12" in name else {6, 8}
        pred = lambda r, e=excl: r["top_house"] not in e
    else:
        pred = lambda r, ss=s: r["top_house"] in ss
    fr, rr = rate(FR, pred) * 100, rate(RR, pred) * 100
    print(f"  {name:26} {fr:5.0f}% {rr:5.0f}% {fr-rr:+5.0f}% {auc_bin(FR, RR, pred):.3f}")
print("\n=== (2) Does it matter WHICH planet is strongest — any vs functional benefic? ===")
print(f"  strongest planet IS a functional benefic:   fam {rate(FR, lambda r: r['top_is_fb'])*100:.0f}%  ord {rate(RR, lambda r: r['top_is_fb'])*100:.0f}%  AUC {auc_bin(FR,RR,lambda r: r['top_is_fb']):.3f}")
GOOD = {1, 2, 4, 5, 9, 10, 11}
p_anygood = lambda r: r["top_house"] in GOOD
p_fbgood = lambda r: r["top_is_fb"] and r["top_house"] in GOOD
p_topfbgood = lambda r: r["topfb_house"] in GOOD          # strongest FUNCTIONAL BENEFIC in a good house
print(f"  ANY strongest planet in good house:          fam {rate(FR,p_anygood)*100:.0f}%  ord {rate(RR,p_anygood)*100:.0f}%  AUC {auc_bin(FR,RR,p_anygood):.3f}")
print(f"  strongest planet in good house AND it's a FB: fam {rate(FR,p_fbgood)*100:.0f}%  ord {rate(RR,p_fbgood)*100:.0f}%  AUC {auc_bin(FR,RR,p_fbgood):.3f}")
print(f"  strongest FUNCTIONAL BENEFIC in good house:  fam {rate(FR,p_topfbgood)*100:.0f}%  ord {rate(RR,p_topfbgood)*100:.0f}%  AUC {auc_bin(FR,RR,p_topfbgood):.3f}")
