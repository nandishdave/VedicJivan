# -*- coding: utf-8 -*-
"""HONEST test: nested CV. The famous-leaning house-set is re-selected INSIDE
each training fold and scored on held-out charts -> removes the selection
leakage in the fixed {1,2,3,5,10} rule. Compares base / fixed-set / nested."""
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
FIXED = {1, 2, 3, 5, 10}
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
    return f12, P[NUMP[moolank]]["house"], P[NUMP[bhagyank]]["house"], by, (68 <= b["lon"] <= 98 and 6 <= b["lat"] <= 37)
FR = [feats(p) for p in FAM]; RR = [feats(p) for p in ORDD]
F12 = np.array([x[0] for x in FR]); R12 = np.array([x[0] for x in RR])
MH = np.array([x[1] for x in FR] + [x[1] for x in RR]); BH = np.array([x[2] for x in FR] + [x[2] for x in RR])
X12 = np.vstack([F12, R12]); Y = np.array([1] * len(FR) + [0] * len(RR), float)
def auc(fa, ra): return float(np.mean([np.mean(x > ra) + 0.5 * np.mean(x == ra) for x in fa]))
def count_in(sel): return np.array([(m in sel) + (b in sel) for m, b in zip(MH, BH)], float)

def cv_scores(Xextra):
    """5-fold; returns held-out composite scores for [12 factors (+ Xextra col)]."""
    X = X12 if Xextra is None else np.column_stack([X12, Xextra])
    np.random.seed(7); idx = np.random.permutation(len(Y)); folds = np.array_split(idx, 5); s = np.zeros(len(Y))
    for i in range(5):
        te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
        sg = np.sign(X[tr][Y[tr] == 1].mean(0) - X[tr][Y[tr] == 0].mean(0)); m, sd = X[tr].mean(0), X[tr].std(0) + 1e-9
        s[te] = (((X[te] - m) / sd) * sg).sum(1)
    return s

def cv_nested(topk=None):
    """Houses re-selected per training fold (positive famous-lean; or top-k)."""
    np.random.seed(7); idx = np.random.permutation(len(Y)); folds = np.array_split(idx, 5); s = np.zeros(len(Y))
    picks = []
    for i in range(5):
        te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
        # per-house pooled famous-minus-ordinary occupancy, TRAIN ONLY
        diffs = {}
        for h in range(1, 13):
            occ = ((MH == h).astype(float) + (BH == h).astype(float)) / 2.0
            diffs[h] = occ[tr][Y[tr] == 1].mean() - occ[tr][Y[tr] == 0].mean()
        if topk:
            sel = set(sorted(diffs, key=diffs.get, reverse=True)[:topk])
        else:
            sel = {h for h, d in diffs.items() if d > 0}
        picks.append(sorted(sel))
        feat = np.array([(m in sel) + (b in sel) for m, b in zip(MH, BH)], float)
        X = np.column_stack([X12, feat]); sg = np.sign(X[tr][Y[tr] == 1].mean(0) - X[tr][Y[tr] == 0].mean(0))
        m, sd = X[tr].mean(0), X[tr].std(0) + 1e-9
        s[te] = (((X[te] - m) / sd) * sg).sum(1)
    return s, picks
base = cv_scores(None); print(f"famous={len(FR)} ordinary={len(RR)}")
print(f"base 12-factor                         full-AUC={auc(base[Y==1],base[Y==0]):.3f}")
fx = cv_scores(count_in(FIXED)); print(f"+ fixed {sorted(FIXED)} (IN-SAMPLE)      full-AUC={auc(fx[Y==1],fx[Y==0]):.3f}")
ns, p1 = cv_nested(None); print(f"+ nested (positive-lean houses/fold)   full-AUC={auc(ns[Y==1],ns[Y==0]):.3f}   HONEST")
ns5, p5 = cv_nested(5); print(f"+ nested (top-5 houses/fold)           full-AUC={auc(ns5[Y==1],ns5[Y==0]):.3f}   HONEST")
print("per-fold house picks (positive-lean):", p1)
print("per-fold house picks (top-5):        ", p5)
