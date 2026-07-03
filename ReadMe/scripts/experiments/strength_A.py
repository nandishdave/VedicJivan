# -*- coding: utf-8 -*-
"""Candidate A - CROSS-DIVISIONAL STRENGTH as factor 15. Same 14-factor base as
the production model (with Shadbala, so argala matches), then 5 strength metrics:
  vim_lag  = Vimsopaka bala (Shodashavarga, wt-sum 20) of the D1 lagna-lord
  vim_10   = Vimsopaka bala of the D1 10th-lord
  vim_avg  = mean Vimsopaka of the 7 classical planets (overall cross-varga strength)
  vgc      = count of the 7 planets VARGOTTAMA (D1 sign == D9 sign)
  vg_key   = lagna-lord + 10th-lord vargottama (0/1/2)
Solo AUC + fixed adds + HONEST nested best-of-5/fold + seed-stability + REF. (225 vs 96)"""
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
MKEYS = ["vim_lag", "vim_10", "vim_avg", "vgc", "vg_key"]
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
    dv = c["divisional"]
    dl = calc_vimshottari_dasha(P["Moon"]["longitude"], b["date"], b["time"])["dashas"]
    ra = next(((int(d["start_date"][:4]) - by, int(d["end_date"][:4]) - by) for d in dl if d["planet"] == "Rahu"), None)
    rahu = (max(0, min(ra[1], 50) - max(ra[0], 20)) if ra else 0) * (1.0 if P[SIGN_LORDS[P["Rahu"]["sign"]]]["house"] not in _BAD else 0.4)
    D60 = dv["D60"]; d60c = float(np.mean([_DP.get(_get_dignity(x, D60[x]), 45) for x in _C]))
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
    f14 = [rahu, d60c, av10, av1, upa, rl, dhl, av11, bright, moon_disp, moon_sav, sun_disp, arg, purna]
    # ---- CANDIDATE A: cross-divisional strength ----
    def vimsopaka(pl):
        t = 0.0
        for v, w in VARGA_W.items():
            sgn = P[pl]["sign"] if v == "D1" else dv[v][pl]
            t += w * (_DP.get(_get_dignity(pl, sgn), 45) / 100.0)
        return t
    laglord = SIGN_LORDS[ls]; tenlord = SIGN_LORDS[(ls + 9) % 12]
    vim_lag = vimsopaka(laglord); vim_10 = vimsopaka(tenlord)
    vim_avg = float(np.mean([vimsopaka(q) for q in _C]))
    vgc = float(sum(1 for q in _C if P[q]["sign"] == dv["D9"][q]))
    vg_key = float((P[laglord]["sign"] == dv["D9"][laglord]) + (P[tenlord]["sign"] == dv["D9"][tenlord]))
    strength = [vim_lag, vim_10, vim_avg, vgc, vg_key]
    return f14, [float(x) for x in strength], by, (68 <= b["lon"] <= 98 and 6 <= b["lat"] <= 37)
FR = [feats(p) for p in FAM]; RR = [feats(p) for p in ORDD]
F = np.array([x[0] for x in FR]); R = np.array([x[0] for x in RR])
FS = np.array([x[1] for x in FR]); RS = np.array([x[1] for x in RR])
X = np.vstack([F, R]); S = np.vstack([FS, RS]); Y = np.array([1] * len(FR) + [0] * len(RR), float)
FY = np.array([x[2] for x in FR]); FI = np.array([x[3] for x in FR])
CUTS = {"full": np.ones(len(FR), bool), ">=1940": (FY >= 1940) & FI, ">=1955": (FY >= 1955) & FI}
def auc(fa, ra): return float(np.mean([np.mean(x > ra) + 0.5 * np.mean(x == ra) for x in fa]))
def cv(Xf, Xr, seed=7):
    Xx = np.vstack([Xf, Xr]); Yy = np.array([1] * len(Xf) + [0] * len(Xr), float)
    np.random.seed(seed); idx = np.random.permutation(len(Yy)); folds = np.array_split(idx, 5); s = np.zeros(len(Yy))
    for i in range(5):
        te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
        sg = np.sign(Xx[tr][Yy[tr] == 1].mean(0) - Xx[tr][Yy[tr] == 0].mean(0)); m, sd = Xx[tr].mean(0), Xx[tr].std(0) + 1e-9
        s[te] = (((Xx[te] - m) / sd) * sg).sum(1)
    return auc(s[Yy == 1], s[Yy == 0])
def add(cols):
    Fn = np.column_stack([F] + [FS[:, i] for i in cols]); Rn = np.column_stack([R] + [RS[:, i] for i in cols])
    return Fn, Rn
print(f"famous={len(FR)} ordinary={len(RR)}")
print("\nSolo separation of each strength metric (fam_mean, ord_mean, solo-AUC):")
for i, k in enumerate(MKEYS):
    print(f"  {k:10} fam={FS[:,i].mean():7.3f} ord={RS[:,i].mean():7.3f}  soloAUC={auc(FS[:,i], RS[:,i]):.3f}")
print("\nbase 14-factor:            " + "  ".join(f"{k}={cv(F[CUTS[k]],R):.3f}" for k in CUTS))
for i, k in enumerate(MKEYS):
    Fn, Rn = add([i]); print(f"+ {k:10}              " + "  ".join(f"{ck}={cv(Fn[CUTS[ck]],Rn):.3f}" for ck in CUTS))
# HONEST nested best-of-5 per fold
np.random.seed(7); idx = np.random.permutation(len(Y)); folds = np.array_split(idx, 5); s = np.zeros(len(Y)); picks = []
for i in range(5):
    te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
    seps = [abs(S[tr][Y[tr] == 1, m].mean() - S[tr][Y[tr] == 0, m].mean()) / (S[tr][:, m].std() + 1e-9) for m in range(len(MKEYS))]
    bm = int(np.argmax(seps)); picks.append(MKEYS[bm])
    Xx = np.column_stack([X, S[:, bm]]); sg = np.sign(Xx[tr][Y[tr] == 1].mean(0) - Xx[tr][Y[tr] == 0].mean(0)); m_, sd_ = Xx[tr].mean(0), Xx[tr].std(0) + 1e-9
    s[te] = (((Xx[te] - m_) / sd_) * sg).sum(1)
print(f"\n+ nested best-of-5/fold (HONEST): full={auc(s[Y==1],s[Y==0]):.3f}  picks={picks}")
# seed-stability of the best fixed single add
best_i = int(np.argmax([auc(FS[:, i], RS[:, i]) if auc(FS[:, i], RS[:, i]) >= 0.5 else 1 - auc(FS[:, i], RS[:, i]) for i in range(len(MKEYS))]))
Fn, Rn = add([best_i]); print(f"seed-stability +{MKEYS[best_i]} full-AUC:", [f"{cv(Fn,Rn,seed=sd):.3f}" for sd in [1,7,42,123,2024]])
for i, k in enumerate(MKEYS):
    allv = np.concatenate([FS[:, i], RS[:, i]]); print(f"REF {k}: ({FS[:,i].mean():.4f}, {RS[:,i].mean():.4f}, {allv.std(ddof=1):.4f})")
# SWAP TEST: replace crude D60 (factor index 1) with full-Shodashavarga vim_avg (strength index 2)
print("\n--- SWAP: crude D60 (factor 2) -> Vimsopaka vim_avg ---")
solo_d60 = auc(F[:, 1], R[:, 1]); print(f"solo crude-D60 AUC={solo_d60:.3f}   solo vim_avg AUC={auc(FS[:,2],RS[:,2]):.3f}")
Fsw = F.copy(); Rsw = R.copy(); Fsw[:, 1] = FS[:, 2]; Rsw[:, 1] = RS[:, 2]
print("base (crude D60):      " + "  ".join(f"{k}={cv(F[CUTS[k]],R):.3f}" for k in CUTS))
print("swap (vim_avg for D60):" + "  ".join(f"{k}={cv(Fsw[CUTS[k]],Rsw):.3f}" for k in CUTS))
print("seed-stability swap full:", [f"{cv(Fsw,Rsw,seed=sd):.3f}" for sd in [1,7,42,123,2024]])
print("\n--- per-cut seed-stability, base vs swap (the deciding test) ---")
SEEDS = [1, 7, 42, 123, 2024]
for ck in CUTS:
    bvals = [cv(F[CUTS[ck]], R, seed=sd) for sd in SEEDS]
    svals = [cv(Fsw[CUTS[ck]], Rsw, seed=sd) for sd in SEEDS]
    print(f"  {ck:7} base mean={np.mean(bvals):.3f} {[f'{v:.3f}' for v in bvals]}")
    print(f"  {ck:7} swap mean={np.mean(svals):.3f} {[f'{v:.3f}' for v in svals]}  delta={np.mean(svals)-np.mean(bvals):+.3f}")
