# -*- coding: utf-8 -*-
"""Pushkara Navamsa (benefic) + the two-sided net (Pushkara - Vish) over the 9
planets + Ascendant, famous vs ordinary. Tables user-provided (authoritative).

Pushkara navamsa numbers by element:
  Fire  (Ar,Le,Sg): 7,9    Earth (Ta,Vi,Cp): 3,5
  Air   (Ge,Li,Aq): 6,8    Water (Cn,Sc,Pi): 1,3
Vish navamsa number by sign group:
  {Ar,Ta,Vi,Sg}:1   {Ge,Le,Li,Aq}:5   {Cn,Sc,Cp,Pi}:9
"""
import json
import numpy as np
from app.services.muhurta import build_muhurta_chart

FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8"))
ORD = json.load(open("/app/normal_people.json", encoding="utf-8"))
BODIES = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
NAV = 30.0 / 9.0

# 0-indexed sign -> set of Pushkara navamsa numbers (by element)
PUSH = {}
for s in (0, 4, 8):    PUSH[s] = {7, 9}   # Fire
for s in (1, 5, 9):    PUSH[s] = {3, 5}   # Earth
for s in (2, 6, 10):   PUSH[s] = {6, 8}   # Air
for s in (3, 7, 11):   PUSH[s] = {1, 3}   # Water
# 0-indexed sign -> the single Vish navamsa number
VISH = {}
for s in (0, 1, 5, 8):    VISH[s] = 1
for s in (2, 4, 6, 10):   VISH[s] = 5
for s in (3, 7, 9, 11):   VISH[s] = 9


def navnum(deg):
    return int(deg / NAV) + 1  # 1..9


def counts(dob, tob, lat, lon):
    c = build_muhurta_chart(dob=dob, tob=tob, lat=lat, lon=lon, with_shadbala=False)
    P, lag = c["planets"], c["lagna"]
    bodies = [(P[b]["sign"], P[b]["degree_in_sign"]) for b in BODIES]
    bodies.append((lag["sign"], lag.get("degree", 0.0)))  # Ascendant
    pk = sum(1 for s, d in bodies if navnum(d) in PUSH[s])
    vs = sum(1 for s, d in bodies if navnum(d) == VISH[s])
    india = (68 <= lon <= 98 and 6 <= lat <= 37)
    return pk, vs, int(dob[:4]), india


def _bd(p):
    b = p["birth"]; return (b["date"], b["time"], b["lat"], b["lon"])


FR = [counts(*_bd(p)) for p in FAM]; RR = [counts(*_bd(p)) for p in ORD]
Fpk = np.array([x[0] for x in FR], float); Rpk = np.array([x[0] for x in RR], float)
Fvs = np.array([x[1] for x in FR], float); Rvs = np.array([x[1] for x in RR], float)
FY = np.array([x[2] for x in FR]); FI = np.array([x[3] for x in FR])
Fnet = Fpk - Fvs; Rnet = Rpk - Rvs


def auc(s, y):
    pos, neg = s[y == 1], s[y == 0]
    return float(np.mean([np.mean(p > neg) + 0.5 * np.mean(p == neg) for p in pos]))


def screen(name, F, R, note=""):
    yf = np.array([1] * len(F) + [0] * len(R), float)
    sg = np.sign(F.mean() - R.mean()) or 1.0
    solo = auc(np.concatenate([F, R]) * sg, yf)
    m = (FY >= 1940) & FI
    Fm = F[m]; yc = np.array([1] * len(Fm) + [0] * len(R), float)
    sgc = np.sign(Fm.mean() - R.mean()) or 1.0
    cut = auc(np.concatenate([Fm, R]) * sgc, yc)
    print(f"{name:22} fam {F.mean():5.2f}  ord {R.mean():5.2f}  lift {F.mean()-R.mean():+5.2f}"
          f"   solo {solo:.3f}   >=1940 {cut:.3f}   {note}")


print(f"famous n={len(Fpk)}  ordinary n={len(Rpk)}  (10 bodies: 9 planets + Ascendant)\n")
print(f"{'factor':22} {'famous':>7} {'ord':>7} {'lift':>6}   soloAUC  cleanCut")
screen("Pushkara (benefic)", Fpk, Rpk, "expect famous higher")
screen("Vish (malefic)", Fvs, Rvs, "expect famous lower")
screen("NET (Pushkara-Vish)", Fnet, Rnet, "<- the two-sided factor")
print("\n(0.50 = chance; ~0.55+ AND holding on the clean cut = worth a nested test)")
