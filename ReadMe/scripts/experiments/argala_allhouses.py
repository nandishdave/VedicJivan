# -*- coding: utf-8 -*-
"""Per-house argala sweep (R = 1..12 from Lagna): positive / negative / net,
count-based AND Shadbala-weighted. Which house's argala separates famous vs
ordinary? DIAGNOSTIC map (best house is selection-biased). (225 vs 96)"""
import json, numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS
FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8")); ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_ALL = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
ARG_PAIRS = [(2, 12), (4, 10), (5, 9), (11, 3)]
def hh(R, n): return ((R - 1 + (n - 1)) % 12) + 1
def perhouse(P, benefic, weight):
    by_house = {h: [] for h in range(1, 13)}
    for p in _ALL:
        by_house[P[p]["house"]].append(p)
    pos = np.zeros(12); neg = np.zeros(12)
    for R in range(1, 13):
        for na, nv in ARG_PAIRS:
            A, V = hh(R, na), hh(R, nv)
            wA = sum(weight[p] for p in by_house[A]); wV = sum(weight[p] for p in by_house[V])
            if wA > wV:
                signed = sum(weight[p] * benefic[p] for p in by_house[A])
                if signed > 0: pos[R - 1] += signed
                else: neg[R - 1] += -signed
    return pos, neg
def feats(p):
    b = p["birth"]; c = build_muhurta_chart(dob=b["date"], tob=b["time"], lat=b["lat"], lon=b["lon"], with_shadbala=True)
    P = c["planets"]
    elong = (P["Moon"]["longitude"] - P["Sun"]["longitude"]) % 360; bright = 72 <= elong <= 264
    benefic = {"Jupiter": 1, "Venus": 1, "Mercury": 1, "Moon": (1 if bright else -1),
               "Sun": -1, "Mars": -1, "Saturn": -1, "Rahu": -1, "Ketu": -1}
    sb = c["shadbala"]; svals = [sb[q]["total_shadbala"] for q in _C if q in sb]
    avg = float(np.mean(svals)) if svals else 1.0
    wcount = {q: 1.0 for q in _ALL}; wshad = {q: (sb[q]["total_shadbala"] if q in sb else avg) for q in _ALL}
    pc, nc = perhouse(P, benefic, wcount); ps, ns = perhouse(P, benefic, wshad)
    return pc, nc, ps, ns
FR = [feats(p) for p in FAM]; RR = [feats(p) for p in ORDD]
def stack(rows, idx): return np.array([r[idx] for r in rows])           # (n, 12)
FPc, FNc, FPs, FNs = [stack(FR, i) for i in range(4)]
RPc, RNc, RPs, RNs = [stack(RR, i) for i in range(4)]
def auc(fa, ra): return float(np.mean([np.mean(x > ra) + 0.5 * np.mean(x == ra) for x in fa]))
print(f"famous={len(FR)} ordinary={len(RR)}   argala per reference house (from Lagna)\n")
def tbl(title, F, R):
    print(title)
    print("  house |  famous   ordinary    diff   solo-AUC   (AUC>0.5 => famous-leaning)")
    for h in range(12):
        fa, ra = F[:, h], R[:, h]; a = auc(fa, ra)
        star = " *" if abs(a - 0.5) >= 0.05 else ""
        print(f"   {h+1:2d}   | {fa.mean():8.1f} {ra.mean():9.1f}  {fa.mean()-ra.mean():+7.1f}   {a:.3f}{star}")
    print()
tbl("POSITIVE (shubha) argala — Shadbala-weighted:", FPs, RPs)
tbl("NEGATIVE (paapa) argala — Shadbala-weighted:", FNs, RNs)
tbl("NET (pos - neg) argala — Shadbala-weighted:", FPs - FNs, RPs - RNs)
tbl("POSITIVE (shubha) argala — count-based:", FPc, RPc)
