# -*- coding: utf-8 -*-
"""Definitive 13-factor numbers: 12 + positive Shadbala argala on {2,10,12}.
count/sum CV-AUC, full + all matched cuts, + REF tuple for productionizing."""
import json, numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS, _get_dignity
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha
from app.services.kundli_calculator.raja_yoga import raja_yoga_score
from app.services.kundli_calculator.dhana_yoga import dhana_yoga_score
FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8")); ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_ALL = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55, "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}
_BAD = {3, 6, 8, 12}; _OCC = {3, 6, 10, 11}
ARG_PAIRS = [(2, 12), (4, 10), (5, 9), (11, 3)]
ARG_HOUSES = [2, 10, 12]           # reference houses (from Lagna) for the factor
def hh(R, n): return ((R - 1 + (n - 1)) % 12) + 1
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
def pos_argala(P, benefic, weight):
    bh = {h: [] for h in range(1, 13)}
    for p in _ALL: bh[P[p]["house"]].append(p)
    tot = 0.0
    for R in ARG_HOUSES:
        for na, nv in ARG_PAIRS:
            A, V = hh(R, na), hh(R, nv)
            wA = sum(weight[p] for p in bh[A]); wV = sum(weight[p] for p in bh[V])
            if wA > wV:
                s = sum(weight[p] * benefic[p] for p in bh[A])
                if s > 0: tot += s
    return tot
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
    benefic = {"Jupiter": 1, "Venus": 1, "Mercury": 1, "Moon": (1 if bright else -1),
               "Sun": -1, "Mars": -1, "Saturn": -1, "Rahu": -1, "Ketu": -1}
    sb = c["shadbala"]; svals = [sb[q]["total_shadbala"] for q in _C if q in sb]
    avg = float(np.mean(svals)) if svals else 1.0
    wshad = {q: (sb[q]["total_shadbala"] if q in sb else avg) for q in _ALL}
    arg = pos_argala(P, benefic, wshad)
    return [rahu, d60c, av10, av1, upa, rl, dhl, av11, bright, moon_disp, moon_sav, sun_disp, arg], by, (68 <= b["lon"] <= 98 and 6 <= b["lat"] <= 37)
FR = [feats(p) for p in FAM]; RR = [feats(p) for p in ORDD]
F = np.array([x[0] for x in FR]); R = np.array([x[0] for x in RR]); FY = np.array([x[1] for x in FR]); FI = np.array([x[2] for x in FR])
def auc(sc, yy):
    p, n = sc[yy == 1], sc[yy == 0]; return float(np.mean([np.mean(x > n) + 0.5 * np.mean(x == n) for x in p]))
def cv(Fm, Rm):
    X = np.vstack([Fm, Rm]); y = np.array([1] * len(Fm) + [0] * len(Rm), float)
    np.random.seed(7); idx = np.random.permutation(len(y)); folds = np.array_split(idx, 5); cc = np.zeros(len(y)); ss = np.zeros(len(y))
    for i in range(5):
        te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
        sg = np.sign(X[tr][y[tr] == 1].mean(0) - X[tr][y[tr] == 0].mean(0)); m, sd = X[tr].mean(0), X[tr].std(0) + 1e-9; Z = ((X[te] - m) / sd) * sg
        cc[te] = (Z > 0).sum(1); ss[te] = Z.sum(1)
    return auc(cc, y), auc(ss, y)
print(f"famous={len(FR)} ordinary={len(RR)}   factor 13 = positive Shadbala argala on {ARG_HOUSES}")
for lbl, cols in (("12-factor", slice(0, 12)), ("13-factor", slice(0, 13))):
    print(f"\n{lbl}:")
    for yr in (None, 0, 1940, 1955):
        mask = np.ones(len(FR), bool) if yr is None else ((FY >= yr) & FI)
        if mask.sum() < 20: continue
        cc, ss = cv(F[mask][:, cols], R[:, cols]); tag = "full" if yr is None else f"India>={yr}"
        print(f"  {tag:11} n_fam={mask.sum():3d}  count-AUC={cc:.3f}  sum-AUC={ss:.3f}")
arg_f = F[:, 12]; arg_r = R[:, 12]; allv = np.concatenate([arg_f, arg_r])
print(f"\nsolo argala AUC={auc(np.concatenate([arg_f,arg_r]), np.array([1]*len(arg_f)+[0]*len(arg_r),float)):.3f}")
print(f"REF argala_pos: ({arg_f.mean():.4f}, {arg_r.mean():.4f}, {allv.std(ddof=1):.4f})")
