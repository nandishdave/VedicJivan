# -*- coding: utf-8 -*-
"""HONEST test of the Purna-tithi factor: nested CV (tithi group re-picked per
fold) + redundancy check vs bright-Moon (factor 9). Earns factor 14 or not."""
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
TG = ["Nanda", "Bhadra", "Jaya", "Rikta", "Purna"]
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
    f13 = [rahu, d60c, av10, av1, upa, rl, dhl, av11, bright, moon_disp, moon_sav, sun_disp, arg]
    tithi = int(elong / 12) + 1
    return f13, (tithi - 1) % 5, bright, by, (68 <= b["lon"] <= 98 and 6 <= b["lat"] <= 37)
FR = [feats(p) for p in FAM]; RR = [feats(p) for p in ORDD]
F13 = np.array([x[0] for x in FR]); R13 = np.array([x[0] for x in RR])
TG_ALL = np.array([x[1] for x in FR] + [x[1] for x in RR]); BR_ALL = np.array([x[2] for x in FR] + [x[2] for x in RR])
X13 = np.vstack([F13, R13]); Y = np.array([1] * len(FR) + [0] * len(RR), float)
FY = np.array([x[3] for x in FR]); FI = np.array([x[4] for x in FR])
IDX = {"full": np.ones(len(FR), bool), ">=1940": (FY >= 1940) & FI, ">=1955": (FY >= 1955) & FI}
def auc(fa, ra): return float(np.mean([np.mean(x > ra) + 0.5 * np.mean(x == ra) for x in fa]))
def cv(F, R):
    X = np.vstack([F, R]); y = np.array([1] * len(F) + [0] * len(R), float)
    np.random.seed(7); idx = np.random.permutation(len(y)); folds = np.array_split(idx, 5); s = np.zeros(len(y))
    for i in range(5):
        te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
        sg = np.sign(X[tr][y[tr] == 1].mean(0) - X[tr][y[tr] == 0].mean(0)); m, sd = X[tr].mean(0), X[tr].std(0) + 1e-9
        s[te] = (((X[te] - m) / sd) * sg).sum(1)
    return auc(s[y == 1], s[y == 0])
def cv_nested(topk=1):
    np.random.seed(7); idx = np.random.permutation(len(Y)); folds = np.array_split(idx, 5); s = np.zeros(len(Y)); picks = []
    for i in range(5):
        te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
        diffs = np.array([ (TG_ALL[tr][Y[tr]==1]==g).mean() - (TG_ALL[tr][Y[tr]==0]==g).mean() for g in range(5)])
        sel = set(np.argsort(diffs)[::-1][:topk]) if topk else {g for g in range(5) if diffs[g] > 0}
        picks.append([TG[g] for g in sorted(sel)])
        feat = np.array([1.0 if t in sel else 0.0 for t in TG_ALL])
        X = np.column_stack([X13, feat]); sg = np.sign(X[tr][Y[tr]==1].mean(0) - X[tr][Y[tr]==0].mean(0)); m, sd = X[tr].mean(0), X[tr].std(0)+1e-9
        s[te] = (((X[te]-m)/sd)*sg).sum(1)
    return auc(s[Y==1], s[Y==0]), picks
purna = (TG_ALL == 4).astype(float); Fp, Rp = purna[:len(FR)], purna[len(FR):]
print(f"famous={len(FR)} ordinary={len(RR)}")
print("base 13-factor:      " + "  ".join(f"{k}={cv(F13[IDX[k]],R13):.3f}" for k in IDX))
F14 = np.column_stack([F13, Fp]); R14 = np.column_stack([R13, Rp])
print("+ Purna fixed (IN-SAMPLE): " + "  ".join(f"{k}={cv(F14[IDX[k]],R14):.3f}" for k in IDX))
a1, p1 = cv_nested(1); a2, p2 = cv_nested(0)
print(f"+ Purna nested top-1/fold (HONEST):  full={a1:.3f}   picks={p1}")
print(f"+ Purna nested positive-diff (HONEST): full={a2:.3f}   picks={p2}")
print("\n=== redundancy vs bright-Moon (factor 9) ===")
print(f"  corr(Purna, bright) = {np.corrcoef(purna, BR_ALL)[0,1]:.3f}")
for bval, lbl in ((0.0, "dark-Moon"), (1.0, "bright-Moon")):
    m = BR_ALL == bval; fm = m[:len(FR)]; rm = m[len(FR):]
    fp = Fp[fm]; rp = Rp[rm]
    print(f"  Purna separation among {lbl:11} charts: famous {fp.mean()*100:4.1f}% vs ord {rp.mean()*100:4.1f}%  (n_fam={fm.sum()}, n_ord={rm.sum()})")
