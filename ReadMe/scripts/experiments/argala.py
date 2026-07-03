# -*- coding: utf-8 -*-
"""Argala on the 1st/2nd/10th/11th houses (from Lagna). Positive (benefic) vs
negative (malefic) argala, effective only if it beats its virodha (counter).
Count-based AND Shadbala-weighted. Famous vs ordinary + composite lift. (225/96)"""
import json, numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS, _get_dignity
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha
from app.services.kundli_calculator.divisional import calc_divisional_charts
from app.services.kundli_calculator.raja_yoga import raja_yoga_score
from app.services.kundli_calculator.dhana_yoga import dhana_yoga_score
FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8")); ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_ALL = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55, "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}
_BAD = {3, 6, 8, 12}; _OCC = {3, 6, 10, 11}
# argala house (Nth from R) -> its virodha (counter) house (Nth from R)
ARG_PAIRS = [(2, 12), (4, 10), (5, 9), (11, 3)]
REF_HOUSES = [1, 2, 10, 11]
def hh(R, n): return ((R - 1 + (n - 1)) % 12) + 1   # absolute house = Nth from R
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
def argala(P, benefic, weight):
    """Return (net, pos, neg) argala aggregated over REF_HOUSES.
    weight: dict planet->magnitude (1.0 for count, shadbala for weighted)."""
    by_house = {h: [] for h in range(1, 13)}
    for p in _ALL:
        by_house[P[p]["house"]].append(p)
    net = pos = neg = 0.0
    for R in REF_HOUSES:
        for na, nv in ARG_PAIRS:
            A, V = hh(R, na), hh(R, nv)
            wA = sum(weight[p] for p in by_house[A]); wV = sum(weight[p] for p in by_house[V])
            if wA > wV:  # effective (unobstructed)
                signed = sum(weight[p] * benefic[p] for p in by_house[A])
                net += signed
                if signed > 0: pos += signed
                else: neg += -signed
    return net, pos, neg
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
    ms = P["Moon"]["sign"]; elong = (P["Moon"]["longitude"] - P["Sun"]["longitude"]) % 360
    bright = 1.0 if 72 <= elong <= 264 else 0.0
    moon_disp = 1.0 if P[SIGN_LORDS[ms]]["house"] in (1, 2, 11, 12) else 0.0
    moon_sav = tv[ms]; sun_disp = 1.0 if P[SIGN_LORDS[P["Sun"]["sign"]]]["house"] in (1, 2, 3, 4) else 0.0
    f12 = [rahu, d60c, av10, av1, upa, rl, dhl, av11, bright, moon_disp, moon_sav, sun_disp]
    # benefic map: J/V/Me benefic; Moon benefic if bright; Sun/Ma/Sa/Ra/Ke malefic
    benefic = {"Jupiter": 1, "Venus": 1, "Mercury": 1, "Moon": (1 if bright else -1),
               "Sun": -1, "Mars": -1, "Saturn": -1, "Rahu": -1, "Ketu": -1}
    sb = c["shadbala"]; svals = [sb[p]["total_shadbala"] for p in _C if p in sb]
    avg = float(np.mean(svals)) if svals else 1.0
    wcount = {p: 1.0 for p in _ALL}
    wshad = {p: (sb[p]["total_shadbala"] if p in sb else avg) for p in _ALL}
    nc, pc, ngc = argala(P, benefic, wcount)
    ns, ps, ngs = argala(P, benefic, wshad)
    return f12, (nc, pc, ngc), (ns, ps, ngs), by, (68 <= b["lon"] <= 98 and 6 <= b["lat"] <= 37)
FR = [feats(p) for p in FAM]; RR = [feats(p) for p in ORDD]
F12 = np.array([x[0] for x in FR]); R12 = np.array([x[0] for x in RR])
FY = np.array([x[3] for x in FR]); FI = np.array([x[4] for x in FR])
def col(rows, idx, sub): return np.array([r[idx][sub] for r in rows], float)
def auc(fa, ra): return float(np.mean([np.mean(x > ra) + 0.5 * np.mean(x == ra) for x in fa]))
def cv(F, R):
    X = np.vstack([F, R]); y = np.array([1] * len(F) + [0] * len(R), float)
    np.random.seed(7); idx = np.random.permutation(len(y)); folds = np.array_split(idx, 5); s = np.zeros(len(y))
    for i in range(5):
        te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
        sg = np.sign(X[tr][y[tr] == 1].mean(0) - X[tr][y[tr] == 0].mean(0)); m, sd = X[tr].mean(0), X[tr].std(0) + 1e-9
        s[te] = (((X[te] - m) / sd) * sg).sum(1)
    return auc(s[y == 1], s[y == 0])
mask40 = (FY >= 1940) & FI; mask55 = (FY >= 1955) & FI; mask0 = FI
print(f"famous={len(FR)} ordinary={len(RR)}   argala on houses {REF_HOUSES} from Lagna")
print(f"base 12-factor:  full={cv(F12,R12):.3f}  >=0={cv(F12[mask0],R12):.3f}  >=1940={cv(F12[mask40],R12):.3f}  >=1955={cv(F12[mask55],R12):.3f}\n")
for tag, ci in (("COUNT-based", 1), ("SHADBALA-weighted", 2)):
    print(f"--- {tag} ---")
    for lbl, sub in (("net (pos-neg)", 0), ("positive only", 1), ("negative only", 2)):
        Ff = col(FR, ci, sub); Rf = col(RR, ci, sub)
        F13 = np.column_stack([F12, Ff]); R13 = np.column_stack([R12, Rf])
        print(f"  {lbl:14} famous {Ff.mean():8.1f}  ord {Rf.mean():8.1f}  solo-AUC={auc(Ff,Rf):.3f}  | +comp full={cv(F13,R13):.3f} >=1940={cv(F13[mask40],R13):.3f} >=1955={cv(F13[mask55],R13):.3f}")
    print()
