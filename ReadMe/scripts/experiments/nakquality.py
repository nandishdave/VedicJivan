# -*- coding: utf-8 -*-
"""Nakshatra QUALITY (nature) of each planet: how many planets fall in each of the 7
qualities — Swift/Ksipra, Violent/Ugra, Mixed/Misra, Fixed/Sthira, Tender/Mridu,
Dreadful/Tikshna, Movable/Chara — famous vs ordinary. Descriptive + solo AUC. (225/96)"""
import json, numpy as np
from app.services.muhurta import build_muhurta_chart
FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8")); ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
NAK = 360.0 / 27.0
# nakshatra index 0..26 -> quality (matches the user's 27-nakshatra table)
QUAL = ["Swift","Violent","Mixed","Fixed","Tender","Dreadful","Movable","Swift","Dreadful",
        "Violent","Violent","Fixed","Swift","Tender","Movable","Mixed","Tender","Dreadful",
        "Dreadful","Violent","Fixed","Movable","Movable","Movable","Violent","Fixed","Tender"]
QORDER = ["Swift","Violent","Mixed","Fixed","Tender","Dreadful","Movable"]
def quality(lon): return QUAL[int((lon % 360) / NAK)]
def row(p):
    b = p["birth"]; c = build_muhurta_chart(dob=b["date"], tob=b["time"], lat=b["lat"], lon=b["lon"], with_shadbala=False)
    P = c["planets"]
    cnt = {q: 0 for q in QORDER}
    for q in _C:
        cnt[quality(P[q]["longitude"])] += 1
    india = (68 <= b["lon"] <= 98 and 6 <= b["lat"] <= 37)
    return [float(cnt[q]) for q in QORDER], int(b["date"][:4]), india
FR = [row(p) for p in FAM]; RR = [row(p) for p in ORDD]
F = np.array([x[0] for x in FR]); R = np.array([x[0] for x in RR])
FY = np.array([x[1] for x in FR]); FI = np.array([x[2] for x in FR])
def auc(fa, ra): return float(np.mean([np.mean(x > ra) + 0.5 * np.mean(x == ra) for x in fa]))
def report(Fm, label):
    print(f"\n=== {label}  (famous n={len(Fm)}, ordinary n={len(R)}) — avg count out of {len(_C)} ===")
    print(f"  {'quality':10} {'famous':>7} {'ordinary':>9} {'gap':>7} {'AUC':>6}")
    rows = [(q, Fm[:, i].mean(), R[:, i].mean(), Fm[:, i].mean()-R[:, i].mean(), auc(Fm[:, i], R[:, i])) for i, q in enumerate(QORDER)]
    for q, fm, om, gap, a in sorted(rows, key=lambda r: -r[3]):
        flag = " <= FAMOUS" if gap >= 0.08 else (" <= ORDINARY" if gap <= -0.08 else "")
        print(f"  {q:10} {fm:7.3f} {om:9.3f} {gap:+7.3f} {a:6.3f}{flag}")
report(F, "FULL SET (era-unmatched)")
report(F[FI & (FY >= 1940)], "CONFOUND-MATCHED: India-born famous >= 1940")
