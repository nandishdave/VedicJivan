# -*- coding: utf-8 -*-
"""Vish Navamsa screen: do famous vs ordinary differ in how many of the 9 planets
+ Ascendant fall in a Vish (poison) navamsa? Table (user-provided, authoritative):
  signs 1,2,6,9  -> navamsa 1 (0-3.20)
  signs 3,5,7,11 -> navamsa 5 (13.20-16.40)
  signs 4,8,10,12-> navamsa 9 (26.40-30)
Malefic factor, so expect famous to lean LOWER (tested both ways).
"""
import json
import numpy as np
from app.services.muhurta import build_muhurta_chart

FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8"))
ORD = json.load(open("/app/normal_people.json", encoding="utf-8"))
BODIES = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
NAV = 30.0 / 9.0  # 3.333 deg per navamsa

# 0-indexed sign -> the Vish navamsa number (1-9)
VISH_NAV = {}
for s in (0, 1, 5, 8):    # Aries, Taurus, Virgo, Sagittarius
    VISH_NAV[s] = 1
for s in (2, 4, 6, 10):   # Gemini, Leo, Libra, Aquarius
    VISH_NAV[s] = 5
for s in (3, 7, 9, 11):   # Cancer, Scorpio, Capricorn, Pisces
    VISH_NAV[s] = 9


def in_vish(sign, deg_in_sign):
    nav = int(deg_in_sign / NAV) + 1     # 1..9
    return nav == VISH_NAV[sign]


def count_vish(dob, tob, lat, lon):
    c = build_muhurta_chart(dob=dob, tob=tob, lat=lat, lon=lon, with_shadbala=False)
    P, lag = c["planets"], c["lagna"]
    n = 0
    for b in BODIES:
        if in_vish(P[b]["sign"], P[b]["degree_in_sign"]):
            n += 1
    if in_vish(lag["sign"], lag.get("degree", 0.0)):   # Ascendant
        n += 1
    india = (68 <= lon <= 98 and 6 <= lat <= 37)
    return n, int(dob[:4]), india


def _bd(p):
    b = p["birth"]
    return (b["date"], b["time"], b["lat"], b["lon"])


FR = [count_vish(*_bd(p)) for p in FAM]
RR = [count_vish(*_bd(p)) for p in ORD]
F = np.array([x[0] for x in FR], float); R = np.array([x[0] for x in RR], float)
FY = np.array([x[1] for x in FR]); FI = np.array([x[2] for x in FR])


def auc(s, y):
    pos, neg = s[y == 1], s[y == 0]
    return float(np.mean([np.mean(p > neg) + 0.5 * np.mean(p == neg) for p in pos]))


yf = np.array([1] * len(F) + [0] * len(R), float)
sg = np.sign(F.mean() - R.mean()) or 1.0
solo = auc(np.concatenate([F, R]) * sg, yf)
m = (FY >= 1940) & FI
Fm = F[m]; yc = np.array([1] * len(Fm) + [0] * len(R), float)
sgc = np.sign(Fm.mean() - R.mean()) or 1.0
cut = auc(np.concatenate([Fm, R]) * sgc, yc)

print(f"famous n={len(F)}  ordinary n={len(R)}")
print(f"\nVish-navamsa count (of 9 planets + Ascendant = 10 bodies):")
print(f"  famous  : mean {F.mean():.2f}  (range {F.min():.0f}-{F.max():.0f})")
print(f"  ordinary: mean {R.mean():.2f}  (range {R.min():.0f}-{R.max():.0f})")
print(f"  lift (famous - ordinary): {F.mean() - R.mean():+.2f}   (malefic: negative = famous cleaner)")
print(f"\n  solo AUC = {solo:.3f}   |   AUC on >=1940 India cut = {cut:.3f}")
print("  (0.50 = chance; worth pursuing only if ~0.55+ AND holds on the clean cut)")
print("\ndistribution (how many charts have exactly k bodies in Vish):")
for k in range(0, int(max(F.max(), R.max())) + 1):
    print(f"  k={k}: famous {int((F==k).sum()):3d}   ordinary {int((R==k).sum()):3d}")
