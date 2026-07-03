# -*- coding: utf-8 -*-
"""Panchanga Nitya-Yoga (27) + Tithi 5-group (Nanda/Bhadra/Jaya/Rikta/Purna):
distribution famous vs ordinary, and do they add over the 13-factor model?"""
import json, numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS, _get_dignity
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha
from app.services.kundli_calculator.raja_yoga import raja_yoga_score
from app.services.kundli_calculator.dhana_yoga import dhana_yoga_score
FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8")); ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_ALL = _C + ["Rahu", "Ketu"]
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55, "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}
_BAD = {3, 6, 8, 12}; _OCC = {3, 6, 10, 11}
_ARG_PAIRS = ((2, 12), (4, 10), (5, 9), (11, 3)); _ARG_HOUSES = (2, 10, 12)
YOGA_NAMES = ["Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda", "Sukarma", "Dhriti",
              "Shula", "Ganda", "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra", "Siddhi", "Vyatipata",
              "Variyana", "Parigha", "Shiva", "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma", "Indra", "Vaidhriti"]
MALEFIC_YOGA = {0, 5, 8, 9, 12, 14, 16, 18, 26}  # the 9 inauspicious nitya yogas
TITHI_GRP = ["Nanda", "Bhadra", "Jaya", "Rikta", "Purna"]
def hh(R, n): return ((R - 1 + n - 1) % 12) + 1
def _pw(l):
    w = {}
    for lk in l:
        for p in lk.get("planets", []): w[p] = w.get(p, 0.0) + lk["score"]
    return w
def _act(dl, by, wd, a, b):
    t = acc = 0.0
    for d in dl:
        ov = max(0, min(int(d["end_date"][:4]) - by, b) - max(int(d["start_date"][:4]) - by, a))
        if ov > 0: t += ov; acc += wd.get(d["planet"], 0.0) * ov
    return acc / t if t else 0.0
def feats(p):
    b = p["birth"]; c = build_muhurta_chart(dob=b["date"], tob=b["time"], lat=b["lat"], lon=b["lon"], with_shadbala=True)
    P, lag = c["planets"], c["lagna"]; ls = lag["sign"]; by = int(b["date"][:4])
    dl = calc_vimshottari_dasha(P["Moon"]["longitude"], b["date"], b["time"])["dashas"]
    ra = next(((int(d["start_date"][:4]) - by, int(d["end_date"][:4]) - by) for d in dl if d["planet"] == "Rahu"), None)
    rahu = (max(0, min(ra[1], 50) - max(ra[0], 20)) if ra else 0) * (1.0 if P[SIGN_LORDS[P["Rahu"]["sign"]]]["house"] not in _BAD else 0.4)
    D60 = c["divisional"]["D60"]; d60c = float(np.mean([_DP.get(_get_dignity(x, D60[x]), 45) for x in _C]))
    tv = c["ashtakavarga"]["totals"]; av10, av1, av11 = tv[(ls + 9) % 12], tv[ls], tv[(ls + 10) % 12]
    tot = occ = 0.0
    for d in dl:
        ovp = max(0, min(int(d["end_date"][:4]) - by, 50) - max(int(d["start_date"][:4]) - by, 20))
        if ovp > 0:
            tot += ovp
            if P[d["planet"]]["house"] in _OCC: occ += ovp
    upa = occ / tot if tot else 0.0
    rl = _act(dl, by, _pw(raja_yoga_score(c)[1]), 50, 80); dhl = _act(dl, by, _pw(dhana_yoga_score(c)[1]), 50, 80)
    ms = P["Moon"]["sign"]; sl, ml = P["Sun"]["longitude"], P["Moon"]["longitude"]
    elong = (ml - sl) % 360
    bright = 1.0 if 72 <= elong <= 264 else 0.0
    moon_disp = 1.0 if P[SIGN_LORDS[ms]]["house"] in (1, 2, 11, 12) else 0.0
    moon_sav = tv[ms]; sun_disp = 1.0 if P[SIGN_LORDS[P["Sun"]["sign"]]]["house"] in (1, 2, 3, 4) else 0.0
    # factor 13 argala
    benefic = {"Jupiter": 1, "Venus": 1, "Mercury": 1, "Moon": (1 if bright else -1), "Sun": -1, "Mars": -1, "Saturn": -1, "Rahu": -1, "Ketu": -1}
    sb = c["shadbala"]; svals = [sb[q]["total_shadbala"] for q in _C if q in sb]; avg = float(np.mean(svals)) if svals else 1.0
    wt = {q: (sb[q]["total_shadbala"] if q in sb else avg) for q in _ALL}
    bhh = {h: [] for h in range(1, 13)}
    for pl in _ALL: bhh[P[pl]["house"]].append(pl)
    arg = 0.0
    for R in _ARG_HOUSES:
        for na, nv in _ARG_PAIRS:
            A, V = hh(R, na), hh(R, nv)
            if sum(wt[q] for q in bhh[A]) > sum(wt[q] for q in bhh[V]):
                s = sum(wt[q] * benefic[q] for q in bhh[A])
                if s > 0: arg += s
    f13 = [rahu, d60c, av10, av1, upa, rl, dhl, av11, bright, moon_disp, moon_sav, sun_disp, arg]
    yoga = int(((sl + ml) % 360) / (360 / 27))
    tithi = int(elong / 12) + 1
    tgrp = (tithi - 1) % 5
    return f13, yoga, tgrp, by, (68 <= b["lon"] <= 98 and 6 <= b["lat"] <= 37)
FR = [feats(p) for p in FAM]; RR = [feats(p) for p in ORDD]
F13 = np.array([x[0] for x in FR]); R13 = np.array([x[0] for x in RR])
FYo = np.array([x[1] for x in FR]); RYo = np.array([x[1] for x in RR])
FTg = np.array([x[2] for x in FR]); RTg = np.array([x[2] for x in RR])
FY = np.array([x[3] for x in FR]); FI = np.array([x[4] for x in FR])
def auc(fa, ra): return float(np.mean([np.mean(x > ra) + 0.5 * np.mean(x == ra) for x in fa]))
def cv(F, R):
    X = np.vstack([F, R]); y = np.array([1] * len(F) + [0] * len(R), float)
    np.random.seed(7); idx = np.random.permutation(len(y)); folds = np.array_split(idx, 5); s = np.zeros(len(y))
    for i in range(5):
        te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
        sg = np.sign(X[tr][y[tr] == 1].mean(0) - X[tr][y[tr] == 0].mean(0)); m, sd = X[tr].mean(0), X[tr].std(0) + 1e-9
        s[te] = (((X[te] - m) / sd) * sg).sum(1)
    return auc(s[y == 1], s[y == 0])
IDX = {"full": np.ones(len(FR), bool), ">=1940": (FY >= 1940) & FI, ">=1955": (FY >= 1955) & FI}
print(f"famous={len(FR)} ordinary={len(RR)}\n=== TITHI 5-group (share of each) ===")
for g in range(5):
    print(f"  {TITHI_GRP[g]:7} famous {(FTg==g).mean()*100:5.1f}%   ordinary {(RTg==g).mean()*100:5.1f}%   diff {((FTg==g).mean()-(RTg==g).mean())*100:+5.1f}")
print("\n=== NITYA YOGA — benefic vs malefic ===")
fm = np.array([1.0 if y not in MALEFIC_YOGA else 0.0 for y in FYo]); rm = np.array([1.0 if y not in MALEFIC_YOGA else 0.0 for y in RYo])
print(f"  born in a BENEFIC yoga:  famous {fm.mean()*100:.1f}%   ordinary {rm.mean()*100:.1f}%")
print("  top famous-leaning yogas (min 6 famous):")
for y in range(27):
    ff, oo = (FYo==y).sum(), (RYo==y).sum()
    if ff >= 6:
        d = (FYo==y).mean()*100 - (RYo==y).mean()*100
        if abs(d) >= 2.0: print(f"    {YOGA_NAMES[y]:11} fam {ff:2d} ({(FYo==y).mean()*100:4.1f}%)  ord {oo:2d} ({(RYo==y).mean()*100:4.1f}%)  {d:+5.1f}")
print(f"\nbase 13-factor:  " + "  ".join(f"{k}={cv(F13[IDX[k]],R13):.3f}" for k in IDX))
def test(name, Ff, Rf):
    F14 = np.column_stack([F13, Ff]); R14 = np.column_stack([R13, Rf])
    line = "  ".join(f"{k}={cv(F14[IDX[k]],R14):.3f}" for k in IDX)
    print(f"+ {name:26} solo-AUC={auc(Ff,Rf):.3f}  |  {line}")
test("yoga_benefic", fm, rm)
test("tithi: not Rikta", (FTg!=3).astype(float), (RTg!=3).astype(float))
test("tithi: Purna", (FTg==4).astype(float), (RTg==4).astype(float))
test("tithi: Jaya", (FTg==2).astype(float), (RTg==2).astype(float))
test("tithi: Nanda", (FTg==0).astype(float), (RTg==0).astype(float))
