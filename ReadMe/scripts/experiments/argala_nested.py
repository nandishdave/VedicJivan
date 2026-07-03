# -*- coding: utf-8 -*-
"""Factor-13 candidate: net (and positive) Shadbala-weighted argala on {2,3,10,12}.
Fixed in-sample (all cuts) + HONEST nested CV (houses re-picked per training
fold). Is the lift real or selection bias? (225 vs 96)"""
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
def hh(R, n): return ((R - 1 + (n - 1)) % 12) + 1
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
def perhouse(P, benefic, weight):
    bh = {h: [] for h in range(1, 13)}
    for p in _ALL: bh[P[p]["house"]].append(p)
    pos = np.zeros(12); neg = np.zeros(12)
    for R in range(1, 13):
        for na, nv in ARG_PAIRS:
            A, V = hh(R, na), hh(R, nv)
            wA = sum(weight[p] for p in bh[A]); wV = sum(weight[p] for p in bh[V])
            if wA > wV:
                s = sum(weight[p] * benefic[p] for p in bh[A])
                if s > 0: pos[R - 1] += s
                else: neg[R - 1] += -s
    return pos, neg
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
    benefic = {"Jupiter": 1, "Venus": 1, "Mercury": 1, "Moon": (1 if bright else -1),
               "Sun": -1, "Mars": -1, "Saturn": -1, "Rahu": -1, "Ketu": -1}
    sb = c["shadbala"]; svals = [sb[q]["total_shadbala"] for q in _C if q in sb]
    avg = float(np.mean(svals)) if svals else 1.0
    wshad = {q: (sb[q]["total_shadbala"] if q in sb else avg) for q in _ALL}
    pos, neg = perhouse(P, benefic, wshad)
    return f12, (pos - neg), pos, by, (68 <= b["lon"] <= 98 and 6 <= b["lat"] <= 37)
FR = [feats(p) for p in FAM]; RR = [feats(p) for p in ORDD]
F12 = np.array([x[0] for x in FR]); R12 = np.array([x[0] for x in RR])
FNET = np.array([x[1] for x in FR]); RNET = np.array([x[1] for x in RR])
FPOS = np.array([x[2] for x in FR]); RPOS = np.array([x[2] for x in RR])
X12 = np.vstack([F12, R12]); Y = np.array([1] * len(FR) + [0] * len(RR), float)
FY = np.array([x[3] for x in FR]); FI = np.array([x[4] for x in FR])
IDX = {"full": np.ones(len(FR), bool), ">=0": FI, ">=1940": (FY >= 1940) & FI, ">=1955": (FY >= 1955) & FI}
SEL = [1, 2, 9, 11]  # houses 2,3,10,12 (0-indexed)
def auc(fa, ra): return float(np.mean([np.mean(x > ra) + 0.5 * np.mean(x == ra) for x in fa]))
def cv(F, R):
    X = np.vstack([F, R]); y = np.array([1] * len(F) + [0] * len(R), float)
    np.random.seed(7); idx = np.random.permutation(len(y)); folds = np.array_split(idx, 5); s = np.zeros(len(y))
    for i in range(5):
        te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
        sg = np.sign(X[tr][y[tr] == 1].mean(0) - X[tr][y[tr] == 0].mean(0)); m, sd = X[tr].mean(0), X[tr].std(0) + 1e-9
        s[te] = (((X[te] - m) / sd) * sg).sum(1)
    return auc(s[y == 1], s[y == 0])
def cv_nested(PH, topk=4, positive=False):
    """Houses re-selected per training fold from PH (N,12). Full set only."""
    np.random.seed(7); idx = np.random.permutation(len(Y)); folds = np.array_split(idx, 5); s = np.zeros(len(Y)); picks = []
    for i in range(5):
        te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
        diffs = PH[tr][Y[tr] == 1].mean(0) - PH[tr][Y[tr] == 0].mean(0)
        sel = [h for h in range(12) if diffs[h] > 0] if positive else list(np.argsort(diffs)[::-1][:topk])
        picks.append(sorted(h + 1 for h in sel))
        feat = PH[:, sel].sum(1)
        X = np.column_stack([X12, feat]); sg = np.sign(X[tr][Y[tr] == 1].mean(0) - X[tr][Y[tr] == 0].mean(0))
        m, sd = X[tr].mean(0), X[tr].std(0) + 1e-9; s[te] = (((X[te] - m) / sd) * sg).sum(1)
    return auc(s[Y == 1], s[Y == 0]), picks
print(f"famous={len(FR)} ordinary={len(RR)}   argala factor on houses 2,3,10,12")
print("base 12-factor:      " + "  ".join(f"{k}={cv(F12[IDX[k]],R12):.3f}" for k in IDX))
for tag, FM, RM in (("NET", FNET, RNET), ("POSITIVE", FPOS, RPOS)):
    Ff = FM[:, SEL].sum(1); Rf = RM[:, SEL].sum(1)
    line = "  ".join(f"{k}={cv(np.column_stack([F12,Ff])[IDX[k]], np.column_stack([R12,Rf])):.3f}" for k in IDX)
    print(f"+ {tag} fixed{{2,3,10,12}} (IN-SAMPLE):  {line}   solo-AUC={auc(Ff,Rf):.3f}")
PHN = np.vstack([FNET, RNET]); PHP = np.vstack([FPOS, RPOS])
a4, p4 = cv_nested(PHN, topk=4); ap, pp = cv_nested(PHN, positive=True)
a4p, p4p = cv_nested(PHP, topk=4)
print(f"\nHONEST nested (full-set):")
print(f"+ NET nested top-4/fold:        full-AUC={a4:.3f}   picks={p4}")
print(f"+ NET nested positive-diff:     full-AUC={ap:.3f}   picks={pp}")
print(f"+ POSITIVE nested top-4/fold:   full-AUC={a4p:.3f}   picks={p4p}")
