# -*- coding: utf-8 -*-
"""FINAL combined verification: original 14 (crude D60) vs matured 15 = [swap factor-2
crude-D60 -> Shodashavarga Vimsopaka vim_avg] + [add dig_lords = mean digbala(lagna-lord,
10th-lord)]. count & sum CV-AUC, full + matched cuts, per-cut seed-stability, + the two
new REF tuples. This is the honest headline for the maturation. (225 vs 96)"""
import json, numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS, _get_dignity
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha
from app.services.kundli_calculator.raja_yoga import raja_yoga_score
from app.services.kundli_calculator.dhana_yoga import dhana_yoga_score
FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8")); ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]; _ALL = _C + ["Rahu", "Ketu"]
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55, "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}
_BAD = {3, 6, 8, 12}; _OCC = {3, 6, 10, 11}; _ARG_PAIRS = ((2, 12), (4, 10), (5, 9), (11, 3)); _ARG_HOUSES = (2, 10, 12)
VARGA_W = {"D1": 3.5, "D2": 1, "D3": 1, "D4": 0.5, "D7": 0.5, "D9": 3, "D10": 0.5, "D12": 0.5,
           "D16": 2, "D20": 0.5, "D24": 0.5, "D27": 0.5, "D30": 1, "D40": 0.5, "D45": 0.5, "D60": 4}
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
    P, lag = c["planets"], c["lagna"]; ls = lag["sign"]; by = int(b["date"][:4]); dv = c["divisional"]
    dl = calc_vimshottari_dasha(P["Moon"]["longitude"], b["date"], b["time"])["dashas"]
    ra = next(((int(d["start_date"][:4]) - by, int(d["end_date"][:4]) - by) for d in dl if d["planet"] == "Rahu"), None)
    rahu = (max(0, min(ra[1], 50) - max(ra[0], 20)) if ra else 0) * (1.0 if P[SIGN_LORDS[P["Rahu"]["sign"]]]["house"] not in _BAD else 0.4)
    d60c = float(np.mean([_DP.get(_get_dignity(x, dv["D60"][x]), 45) for x in _C]))
    def vimsopaka(pl):
        t = 0.0
        for v, w in VARGA_W.items():
            sgn = P[pl]["sign"] if v == "D1" else dv[v][pl]
            t += w * (_DP.get(_get_dignity(pl, sgn), 45) / 100.0)
        return t
    vim_avg = float(np.mean([vimsopaka(q) for q in _C]))
    tv = c["ashtakavarga"]["totals"]; av10, av1, av11 = tv[(ls + 9) % 12], tv[ls], tv[(ls + 10) % 12]
    tot = occ = 0.0
    for d in dl:
        ovp = max(0, min(int(d["end_date"][:4]) - by, 50) - max(int(d["start_date"][:4]) - by, 20))
        if ovp > 0:
            tot += ovp
            if P[d["planet"]]["house"] in _OCC: occ += ovp
    upa = occ / tot if tot else 0.0
    rl = _act(dl, by, _pw(raja_yoga_score(c)[1]), 50, 80); dhl = _act(dl, by, _pw(dhana_yoga_score(c)[1]), 50, 80)
    ms = P["Moon"]["sign"]; sl, ml = P["Sun"]["longitude"], P["Moon"]["longitude"]; elong = (ml - sl) % 360
    bright = 1.0 if 72 <= elong <= 264 else 0.0
    moon_disp = 1.0 if P[SIGN_LORDS[ms]]["house"] in (1, 2, 11, 12) else 0.0
    moon_sav = tv[ms]; sun_disp = 1.0 if P[SIGN_LORDS[P["Sun"]["sign"]]]["house"] in (1, 2, 3, 4) else 0.0
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
    tithi = int(elong / 12) + 1; purna = 1.0 if (tithi - 1) % 5 == 4 else 0.0
    def db(pl): return sb[pl]["dig_bala"] if (pl in sb and "dig_bala" in sb[pl]) else 30.0
    dig_lords = (db(SIGN_LORDS[ls]) + db(SIGN_LORDS[(ls + 9) % 12])) / 2.0
    old14 = [rahu, d60c, av10, av1, upa, rl, dhl, av11, bright, moon_disp, moon_sav, sun_disp, arg, purna]
    new15 = [rahu, vim_avg, av10, av1, upa, rl, dhl, av11, bright, moon_disp, moon_sav, sun_disp, arg, purna, dig_lords]
    return old14, new15, by, (68 <= b["lon"] <= 98 and 6 <= b["lat"] <= 37)
FR = [feats(p) for p in FAM]; RR = [feats(p) for p in ORDD]
O_F = np.array([x[0] for x in FR]); O_R = np.array([x[0] for x in RR])
N_F = np.array([x[1] for x in FR]); N_R = np.array([x[1] for x in RR])
FY = np.array([x[2] for x in FR]); FI = np.array([x[3] for x in FR])
CUTS = {"full": np.ones(len(FR), bool), ">=1940": (FY >= 1940) & FI, ">=1955": (FY >= 1955) & FI}
def auc(fa, ra): return float(np.mean([np.mean(x > ra) + 0.5 * np.mean(x == ra) for x in fa]))
def cv(Xf, Xr, seed=7, mode="sum"):
    Xx = np.vstack([Xf, Xr]); Yy = np.array([1] * len(Xf) + [0] * len(Xr), float)
    np.random.seed(seed); idx = np.random.permutation(len(Yy)); folds = np.array_split(idx, 5); s = np.zeros(len(Yy))
    for i in range(5):
        te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
        sg = np.sign(Xx[tr][Yy[tr] == 1].mean(0) - Xx[tr][Yy[tr] == 0].mean(0)); m, sd = Xx[tr].mean(0), Xx[tr].std(0) + 1e-9
        Z = ((Xx[te] - m) / sd) * sg; s[te] = (Z > 0).sum(1) if mode == "count" else Z.sum(1)
    return auc(s[Yy == 1], s[Yy == 0])
SEEDS = [1, 7, 42, 123, 2024]
print(f"famous={len(FR)} ordinary={len(RR)}")
print("\n=== ORIGINAL 14 (crude D60)  vs  MATURED 15 (Vimsopaka swap + dig_lords) ===")
print(f"  {'cut':8} {'old sum(s7)':>11} {'new sum(s7)':>11} | {'old sum(5s)':>11} {'new sum(5s)':>11} {'delta':>7} | {'new count(s7)':>13}")
for ck in CUTS:
    of, orr = O_F[CUTS[ck]], O_R; nf, nr = N_F[CUTS[ck]], N_R
    os7 = cv(of, orr, 7); ns7 = cv(nf, nr, 7)
    o5 = np.mean([cv(of, orr, sd) for sd in SEEDS]); n5 = np.mean([cv(nf, nr, sd) for sd in SEEDS])
    nc7 = cv(nf, nr, 7, "count")
    print(f"  {ck:8} {os7:>11.3f} {ns7:>11.3f} | {o5:>11.3f} {n5:>11.3f} {n5-o5:>+7.3f} | {nc7:>13.3f}")
print("\nper-seed new-15 sum-AUC:")
for ck in CUTS:
    print(f"  {ck:8} {[f'{cv(N_F[CUTS[ck]],N_R,sd):.3f}' for sd in SEEDS]}")
