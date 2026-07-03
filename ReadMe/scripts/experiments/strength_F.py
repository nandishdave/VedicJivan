# -*- coding: utf-8 -*-
"""Candidate F - BHAVA DRISHTI BALA (aspectual strength of the fame houses) as factor 16,
vs the CURRENT 15-factor model (Vimsopaka + dig_lords already in the base). We tested the
lords' strength (D) and occupants (av) — never WHO ASPECTS the 1st/10th/11th.
Graha drishti: all planets aspect the 7th (d=6); Mars +4/8 (d=3,7); Jupiter +5/9 (d=4,8);
Saturn +3/10 (d=2,9); Rahu/Ketu +5/9 (d=4,8, Jupiter-like per house convention).
benefic {J/V/Me + bright Moon}=+1, malefic {Sun/Ma/Sa/Ra/Ke + dark Moon}=-1.
Metrics: net aspect (benefic-minus-malefic) onto 1st/10th/11th, their sum, and a
Shadbala-weighted sum. Solo + factor-16 + nested/seed. (225 vs 96)"""
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
_VARGA_W = {"D1": 3.5, "D2": 1, "D3": 1, "D4": 0.5, "D7": 0.5, "D9": 3, "D10": 0.5, "D12": 0.5,
            "D16": 2, "D20": 0.5, "D24": 0.5, "D27": 0.5, "D30": 1, "D40": 0.5, "D45": 0.5, "D60": 4}
MKEYS = ["bd_1", "bd_10", "bd_11", "bd_key", "bd_keyw"]
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
def _aspects(pl_house, target, planet):
    d = (target - pl_house) % 12
    if d == 6: return True
    if planet == "Mars" and d in (3, 7): return True
    if planet == "Jupiter" and d in (4, 8): return True
    if planet == "Saturn" and d in (2, 9): return True
    if planet in ("Rahu", "Ketu") and d in (4, 8): return True
    return False
def feats(p):
    b = p["birth"]; c = build_muhurta_chart(dob=b["date"], tob=b["time"], lat=b["lat"], lon=b["lon"], with_shadbala=True)
    P, lag = c["planets"], c["lagna"]; ls = lag["sign"]; by = int(b["date"][:4]); dv = c["divisional"]
    dl = calc_vimshottari_dasha(P["Moon"]["longitude"], b["date"], b["time"])["dashas"]
    ra = next(((int(d["start_date"][:4]) - by, int(d["end_date"][:4]) - by) for d in dl if d["planet"] == "Rahu"), None)
    rahu = (max(0, min(ra[1], 50) - max(ra[0], 20)) if ra else 0) * (1.0 if P[SIGN_LORDS[P["Rahu"]["sign"]]]["house"] not in _BAD else 0.4)
    vim_avg = float(np.mean([sum(w * (_DP.get(_get_dignity(q, (P[q]["sign"] if v == "D1" else dv[v][q])), 45) / 100.0) for v, w in _VARGA_W.items()) for q in _C]))
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
    f15 = [rahu, vim_avg, av10, av1, upa, rl, dhl, av11, bright, moon_disp, moon_sav, sun_disp, arg, purna, dig_lords]
    # ---- CANDIDATE F: Bhava Drishti Bala onto 1st / 10th / 11th (from lagna) ----
    def net_aspect(target, weighted):
        s = 0.0
        for q in _ALL:
            if _aspects(P[q]["house"], target, q):
                s += benefic[q] * (wt[q] if weighted else 1.0)
        return s
    bd_1 = net_aspect(1, False); bd_10 = net_aspect(10, False); bd_11 = net_aspect(11, False)
    bd_key = bd_1 + bd_10 + bd_11
    bd_keyw = net_aspect(1, True) + net_aspect(10, True) + net_aspect(11, True)
    strength = [bd_1, bd_10, bd_11, bd_key, bd_keyw]
    return f15, [float(x) for x in strength], by, (68 <= b["lon"] <= 98 and 6 <= b["lat"] <= 37)
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
print(f"famous={len(FR)} ordinary={len(RR)}  (base = current 15-factor model)")
print("\nSolo separation (fam_mean, ord_mean, solo-AUC):")
for i, k in enumerate(MKEYS):
    print(f"  {k:9} fam={FS[:,i].mean():8.2f} ord={RS[:,i].mean():8.2f}  soloAUC={auc(FS[:,i], RS[:,i]):.3f}")
print("\nbase 15-factor:            " + "  ".join(f"{k}={cv(F[CUTS[k]],R):.3f}" for k in CUTS))
for i, k in enumerate(MKEYS):
    Fn, Rn = add([i]); print(f"+ {k:9}               " + "  ".join(f"{ck}={cv(Fn[CUTS[ck]],Rn):.3f}" for ck in CUTS))
np.random.seed(7); idx = np.random.permutation(len(Y)); folds = np.array_split(idx, 5); s = np.zeros(len(Y)); picks = []
for i in range(5):
    te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
    seps = [abs(S[tr][Y[tr] == 1, m].mean() - S[tr][Y[tr] == 0, m].mean()) / (S[tr][:, m].std() + 1e-9) for m in range(len(MKEYS))]
    bm = int(np.argmax(seps)); picks.append(MKEYS[bm])
    Xx = np.column_stack([X, S[:, bm]]); sg = np.sign(Xx[tr][Y[tr] == 1].mean(0) - Xx[tr][Y[tr] == 0].mean(0)); m_, sd_ = Xx[tr].mean(0), Xx[tr].std(0) + 1e-9
    s[te] = (((Xx[te] - m_) / sd_) * sg).sum(1)
print(f"\n+ nested best-of-5/fold (HONEST): full={auc(s[Y==1],s[Y==0]):.3f}  picks={picks}")
bi = int(np.argmax([abs(auc(FS[:, i], RS[:, i]) - 0.5) for i in range(len(MKEYS))]))
Fn, Rn = add([bi]); SEEDS = [1, 7, 42, 123, 2024]
print(f"\nper-cut seed-stability of best ({MKEYS[bi]}):")
for ck in CUTS:
    bvals = [cv(F[CUTS[ck]], R, seed=sd) for sd in SEEDS]; svals = [cv(Fn[CUTS[ck]], Rn, seed=sd) for sd in SEEDS]
    print(f"  {ck:7} base={np.mean(bvals):.3f}  new={np.mean(svals):.3f}  delta={np.mean(svals)-np.mean(bvals):+.3f}")
for i, k in enumerate(MKEYS):
    allv = np.concatenate([FS[:, i], RS[:, i]]); print(f"REF {k}: ({FS[:,i].mean():.4f}, {RS[:,i].mean():.4f}, {allv.std(ddof=1):.4f})")
