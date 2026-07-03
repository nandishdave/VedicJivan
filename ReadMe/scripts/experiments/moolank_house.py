# -*- coding: utf-8 -*-
"""WHERE do the Moolank & Bhagyank planets sit in D1? House distribution
famous vs ordinary, candidate placement rules, and composite lift. (225 vs 96)"""
import json, numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS, _get_dignity
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha
from app.services.kundli_calculator.divisional import calc_divisional_charts
from app.services.kundli_calculator.raja_yoga import raja_yoga_score
from app.services.kundli_calculator.dhana_yoga import dhana_yoga_score
FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8")); ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55, "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}
_BAD = {3, 6, 8, 12}; _OCC = {3, 6, 10, 11}
NUMP = {1: "Sun", 2: "Moon", 3: "Jupiter", 4: "Rahu", 5: "Mercury", 6: "Venus", 7: "Ketu", 8: "Saturn", 9: "Mars"}
def dsum(n):
    n = int(n)
    while n > 9: n = sum(int(c) for c in str(n))
    return n
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
    b = p["birth"]; c = build_muhurta_chart(dob=b["date"], tob=b["time"], lat=b["lat"], lon=b["lon"], with_shadbala=False)
    P, lag = c["planets"], c["lagna"]; ls = lag["sign"]; by = int(b["date"][:4])
    dl = calc_vimshottari_dasha(P["Moon"]["longitude"], b["date"], b["time"])["dashas"]
    ra = next(((int(d["start_date"][:4]) - by, int(d["end_date"][:4]) - by) for d in dl if d["planet"] == "Rahu"), None)
    rahu = (max(0, min(ra[1], 50) - max(ra[0], 20)) if ra else 0) * (1.0 if P[SIGN_LORDS[P["Rahu"]["sign"]]]["house"] not in _BAD else 0.4)
    D60 = calc_divisional_charts(P, lag)["D60"]; d60c = float(np.mean([_DP.get(_get_dignity(x, D60[x]), 45) for x in _C]))
    tv = c["ashtakavarga"]["totals"]; av10, av1, av11 = tv[(ls + 9) % 12], tv[ls], tv[(ls + 10) % 12]
    tot = occ = 0.0
    for d in dl:
        ov = max(0, min(int(d["end_date"][:4]) - by, 50) - max(int(d["start_date"][:4]) - by, 20))
        if ov > 0:
            tot += ov
            if P[d["planet"]]["house"] in _OCC: occ += ov
    upa = occ / tot if tot else 0.0
    rl = _act(dl, by, _pw(raja_yoga_score(c)[1]), 50, 80); dhl = _act(dl, by, _pw(dhana_yoga_score(c)[1]), 50, 80)
    ms = P["Moon"]["sign"]; elong = (P["Moon"]["longitude"] - P["Sun"]["longitude"]) % 360
    bright = 1.0 if 72 <= elong <= 264 else 0.0
    moon_disp = 1.0 if P[SIGN_LORDS[ms]]["house"] in (1, 2, 11, 12) else 0.0
    moon_sav = tv[ms]; sun_disp = 1.0 if P[SIGN_LORDS[P["Sun"]["sign"]]]["house"] in (1, 2, 3, 4) else 0.0
    f12 = [rahu, d60c, av10, av1, upa, rl, dhl, av11, bright, moon_disp, moon_sav, sun_disp]
    date = b["date"]; moolank = dsum(int(date[8:10])); bhagyank = dsum(sum(int(ch) for ch in date if ch.isdigit()))
    mh = P[NUMP[moolank]]["house"]; bh = P[NUMP[bhagyank]]["house"]
    return f12, mh, bh, by, (68 <= b["lon"] <= 98 and 6 <= b["lat"] <= 37)
FR = [feats(p) for p in FAM]; RR = [feats(p) for p in ORDD]
F12 = np.array([x[0] for x in FR]); R12 = np.array([x[0] for x in RR])
FMH = np.array([x[1] for x in FR]); RMH = np.array([x[1] for x in RR])
FBH = np.array([x[2] for x in FR]); RBH = np.array([x[2] for x in RR])
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
print(f"famous={len(FR)} ordinary={len(RR)}\nPer-house occupancy of the numerology planets (% of charts):")
print("  house | Moolank F%  O%  diff | Bhagyank F%  O%  diff | POOLED F%  O%  diff")
for h in range(1, 13):
    mf, mo = (FMH == h).mean() * 100, (RMH == h).mean() * 100
    bf, bo = (FBH == h).mean() * 100, (RBH == h).mean() * 100
    pf = ((FMH == h).mean() + (FBH == h).mean()) / 2 * 100; po = ((RMH == h).mean() + (RBH == h).mean()) / 2 * 100
    print(f"   {h:2d}   | {mf:5.1f} {mo:5.1f} {mf-mo:+5.1f} | {bf:6.1f} {bo:5.1f} {bf-bo:+5.1f} | {pf:5.1f} {po:5.1f} {pf-po:+5.1f}")
print("\nCandidate placement rules (feature = #{Moolank,Bhagyank planets} in the set, 0-2):")
RULES = {"kendra {1,4,7,10}": {1,4,7,10}, "trikona {1,5,9}": {1,5,9}, "prominence {1,10,11}": {1,10,11},
         "upachaya {3,6,10,11}": {3,6,10,11}, "kendra+trikona {1,4,5,7,9,10}": {1,4,5,7,9,10},
         "NOT dusthana {6,8,12}": None, "{1,10,11,4,5,9}": {1,4,5,9,10,11}}
mask = (FY >= 1940) & FI
print(f"  base 12-factor:  full={cv(F12,R12):.3f}  India>=1940={cv(F12[mask],R12):.3f}")
for name, S in RULES.items():
    if S is None:
        Ff = np.array([2 - ((m in _BAD) + (b2 in _BAD)) for m, b2 in zip(FMH, FBH)], float)
        Rf = np.array([2 - ((m in _BAD) + (b2 in _BAD)) for m, b2 in zip(RMH, RBH)], float)
    else:
        Ff = np.array([(m in S) + (b2 in S) for m, b2 in zip(FMH, FBH)], float)
        Rf = np.array([(m in S) + (b2 in S) for m, b2 in zip(RMH, RBH)], float)
    F13 = np.column_stack([F12, Ff]); R13 = np.column_stack([R12, Rf])
    print(f"  {name:30} solo-AUC={auc(Ff,Rf):.3f}  |  +composite full={cv(F13,R13):.3f}  >=1940={cv(F13[mask],R13):.3f}  (REF {Ff.mean():.3f}/{Rf.mean():.3f})")
