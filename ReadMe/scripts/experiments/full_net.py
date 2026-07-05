# -*- coding: utf-8 -*-
"""Full auspicious/poison-degree net over 9 planets + Ascendant, famous vs ordinary.

NET = (Pushkara Navamsa + Pushkara Bhaga)  -  (Vish Navamsa + Mrityu Bhaga)

All four tables loaded from navamsa_bhaga_tables.json (single source of truth).
Reports each component + the net: lift, solo AUC, confound-matched India cut.
"""
import json
import numpy as np
from app.services.muhurta import build_muhurta_chart

TBL = json.load(open("/app/navamsa_bhaga_tables.json", encoding="utf-8"))
PUSH_NAV = {int(k): set(v) for k, v in TBL["pushkara_navamsa"].items() if k.isdigit()}
VISH_NAV = {int(k): v for k, v in TBL["vish_navamsa"].items() if k.isdigit()}
PBHAGA = {int(k): v for k, v in TBL["pushkara_bhaga"]["degrees"].items()}
PBHAGA_TOL = TBL["pushkara_bhaga"]["tolerance_deg"]
MRITYU = TBL["mrityu_bhaga"]["degrees"]
MRITYU_TOL = TBL["mrityu_bhaga"]["tolerance_deg"]

FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8"))
ORD = json.load(open("/app/normal_people.json", encoding="utf-8"))
BODIES = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
NAV = 30.0 / 9.0


def navnum(deg):
    return int(deg / NAV) + 1  # 1..9


def counts(dob, tob, lat, lon):
    c = build_muhurta_chart(dob=dob, tob=tob, lat=lat, lon=lon, with_shadbala=False)
    P, lag = c["planets"], c["lagna"]
    # (sign, degree_in_sign, mrityu-key) for each of the 10 bodies
    bodies = [(P[b]["sign"], P[b]["degree_in_sign"], b) for b in BODIES]
    bodies.append((lag["sign"], lag.get("degree", 0.0), "Lagna"))
    pkn = pkb = vsn = mrt = 0
    for s, d, key in bodies:
        if navnum(d) in PUSH_NAV[s]:
            pkn += 1
        if abs(d - PBHAGA[s]) <= PBHAGA_TOL:
            pkb += 1
        if navnum(d) == VISH_NAV[s]:
            vsn += 1
        if abs(d - MRITYU[key][s]) <= MRITYU_TOL:   # sign-varying table
            mrt += 1
    india = (68 <= lon <= 98 and 6 <= lat <= 37)
    return (pkn, pkb, vsn, mrt), int(dob[:4]), india


def _bd(p):
    b = p["birth"]; return (b["date"], b["time"], b["lat"], b["lon"])


FR = [counts(*_bd(p)) for p in FAM]; RR = [counts(*_bd(p)) for p in ORD]
Fc = np.array([x[0] for x in FR], float); Rc = np.array([x[0] for x in RR], float)
FY = np.array([x[1] for x in FR]); FI = np.array([x[2] for x in FR])
# columns: 0 pushkara_nav, 1 pushkara_bhaga, 2 vish_nav, 3 mrityu
Fben = Fc[:, 0] + Fc[:, 1]; Rben = Rc[:, 0] + Rc[:, 1]
Fmal = Fc[:, 2] + Fc[:, 3]; Rmal = Rc[:, 2] + Rc[:, 3]
Fnet = Fben - Fmal; Rnet = Rben - Rmal


def auc(s, y):
    pos, neg = s[y == 1], s[y == 0]
    return float(np.mean([np.mean(p > neg) + 0.5 * np.mean(p == neg) for p in pos]))


def screen(name, F, R):
    yf = np.array([1] * len(F) + [0] * len(R), float)
    sg = np.sign(F.mean() - R.mean()) or 1.0
    solo = auc(np.concatenate([F, R]) * sg, yf)
    m = (FY >= 1940) & FI
    Fm = F[m]; yc = np.array([1] * len(Fm) + [0] * len(R), float)
    sgc = np.sign(Fm.mean() - R.mean()) or 1.0
    cut = auc(np.concatenate([Fm, R]) * sgc, yc)
    print(f"  {name:26} fam {F.mean():5.2f}  ord {R.mean():5.2f}  lift {F.mean()-R.mean():+5.2f}   solo {solo:.3f}   >=1940 {cut:.3f}")


print(f"famous n={len(Fc)}  ordinary n={len(Rc)}  (10 bodies: 9 planets + Ascendant; Mandi not scored)\n")
print("component means + screens:")
screen("Pushkara Navamsa (+)", Fc[:, 0], Rc[:, 0])
screen("Pushkara Bhaga (+)", Fc[:, 1], Rc[:, 1])
screen("Vish Navamsa (-)", Fc[:, 2], Rc[:, 2])
screen("Mrityu Bhaga (-)", Fc[:, 3], Rc[:, 3])
print()
screen("BENEFIC sum (PkN+PkB)", Fben, Rben)
screen("MALEFIC sum (Vish+Mrityu)", Fmal, Rmal)
print()
screen("NET  (benefic - malefic)", Fnet, Rnet)
print("\n  >>> NET is the Factor-18 candidate. 0.50=chance; ~0.55+ AND clean cut holding = worth a nested test.")
