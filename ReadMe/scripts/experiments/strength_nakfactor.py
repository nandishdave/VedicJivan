# -*- coding: utf-8 -*-
"""Factor 17 candidates from nakshatra QUALITY (9 bodies). Tests vs the 16-factor model:
  A = Mridu count           B = Mridu - Tikshna         A+B together
  C = Mridu + Swift         D = (Mridu+Swift) - (Tikshna+Movable)
Solo AUC (full + matched), composite lift (full/1940/1955 + 5-seed), nested for A/B. (225/96)"""
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
SEAT = {1, 2, 4, 5, 11}; NAK = 360.0 / 27.0
QUAL = ["Swift","Violent","Mixed","Fixed","Tender","Dreadful","Movable","Swift","Dreadful",
        "Violent","Violent","Fixed","Swift","Tender","Movable","Mixed","Tender","Dreadful",
        "Dreadful","Violent","Fixed","Movable","Movable","Movable","Violent","Fixed","Tender"]
def quality(lon): return QUAL[int((lon % 360) / NAK)]
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
    vim = {q: sum(w * (_DP.get(_get_dignity(q, (P[q]["sign"] if v == "D1" else dv[v][q])), 45) / 100.0) for v, w in _VARGA_W.items()) for q in _C}
    vim_avg = float(np.mean(list(vim.values())))
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
    top = max(_C, key=lambda q: vim[q]); top_seat = 1.0 if P[top]["house"] in SEAT else 0.0
    f16 = [rahu, vim_avg, av10, av1, upa, rl, dhl, av11, bright, moon_disp, moon_sav, sun_disp, arg, purna, dig_lords, top_seat]
    # quality counts over 9 bodies
    qc = {"Swift": 0, "Violent": 0, "Mixed": 0, "Fixed": 0, "Tender": 0, "Dreadful": 0, "Movable": 0}
    for q in _ALL: qc[quality(P[q]["longitude"])] += 1
    mridu, tikshna, swift, movable = qc["Tender"], qc["Dreadful"], qc["Swift"], qc["Movable"]
    A = mridu; B = mridu - tikshna; Cc = mridu + swift; D = (mridu + swift) - (tikshna + movable)
    extra = [A, B, Cc, D]
    return f16, [float(x) for x in extra], by, (68 <= b["lon"] <= 98 and 6 <= b["lat"] <= 37)
FR = [feats(p) for p in FAM]; RR = [feats(p) for p in ORDD]
F = np.array([x[0] for x in FR]); R = np.array([x[0] for x in RR])
E_F = np.array([x[1] for x in FR]); E_R = np.array([x[1] for x in RR])
X = np.vstack([F, R]); Y = np.array([1] * len(FR) + [0] * len(RR), float)
FY = np.array([x[2] for x in FR]); FI = np.array([x[3] for x in FR])
CUTS = {"full": np.ones(len(FR), bool), ">=1940": (FI & (FY >= 1940)), ">=1955": (FI & (FY >= 1955))}
EK = {"A": 0, "B": 1, "C": 2, "D": 3}
def auc(fa, ra): return float(np.mean([np.mean(x > ra) + 0.5 * np.mean(x == ra) for x in fa]))
def cv(cols, cut, seed=7):
    Ff = np.column_stack([F[cut]] + [E_F[cut, EK[k]] for k in cols]); Rr = np.column_stack([R] + [E_R[:, EK[k]] for k in cols])
    Xx = np.vstack([Ff, Rr]); y = np.array([1]*len(Ff)+[0]*len(Rr), float)
    np.random.seed(seed); idx = np.random.permutation(len(y)); folds = np.array_split(idx, 5); s = np.zeros(len(y))
    for i in range(5):
        te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
        sg = np.sign(Xx[tr][y[tr]==1].mean(0) - Xx[tr][y[tr]==0].mean(0)); m, sd = Xx[tr].mean(0), Xx[tr].std(0)+1e-9
        s[te] = (((Xx[te]-m)/sd)*sg).sum(1)
    return auc(s[y==1], s[y==0])
def base_cv(cut, seed=7):
    Ff = F[cut]; Xx = np.vstack([Ff, R]); y = np.array([1]*len(Ff)+[0]*len(R), float)
    np.random.seed(seed); idx = np.random.permutation(len(y)); folds = np.array_split(idx, 5); s = np.zeros(len(y))
    for i in range(5):
        te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
        sg = np.sign(Xx[tr][y[tr]==1].mean(0) - Xx[tr][y[tr]==0].mean(0)); m, sd = Xx[tr].mean(0), Xx[tr].std(0)+1e-9
        s[te] = (((Xx[te]-m)/sd)*sg).sum(1)
    return auc(s[y==1], s[y==0])
SEEDS = [1, 7, 42, 123, 2024]
mcut = CUTS[">=1940"]
print(f"famous={len(FR)} ordinary={len(RR)}")
print("\nsolo AUC (full | India>=1940 matched):")
for k in ["A", "B", "C", "D"]:
    print(f"  {k}: full={auc(E_F[:,EK[k]],E_R[:,EK[k]]):.3f}   matched={auc(E_F[mcut,EK[k]],E_R[:,EK[k]]):.3f}")
print("\n=== model variants (sum-AUC seed7 | 5-seed full) ===")
print(f"  base 16-factor:              full={base_cv(CUTS['full']):.3f}  >=1940={base_cv(CUTS['>=1940']):.3f}  >=1955={base_cv(CUTS['>=1955']):.3f}   5seed={np.mean([base_cv(CUTS['full'],sd) for sd in SEEDS]):.3f}")
for name, cols in [("+A (Mridu)", ["A"]), ("+B (Mridu-Tikshna)", ["B"]), ("+A+B (both)", ["A","B"]), ("+C (Mridu+Swift)", ["C"]), ("+D (broad net)", ["D"])]:
    print(f"  {name:22} full={cv(cols,CUTS['full']):.3f}  >=1940={cv(cols,CUTS['>=1940']):.3f}  >=1955={cv(cols,CUTS['>=1955']):.3f}   5seed={np.mean([cv(cols,CUTS['full'],sd) for sd in SEEDS]):.3f}")
print("\n=== per-cut seed-stability (pre-registered A, B) ===")
for name, cols in [("A (Mridu)", ["A"]), ("B (Mridu-Tikshna)", ["B"])]:
    print(f"  +{name}:")
    for ck in CUTS:
        bvals = [base_cv(CUTS[ck], sd) for sd in SEEDS]; svals = [cv(cols, CUTS[ck], sd) for sd in SEEDS]
        print(f"     {ck:7} base={np.mean(bvals):.3f} new={np.mean(svals):.3f} delta={np.mean(svals)-np.mean(bvals):+.3f}")
    allv = np.concatenate([E_F[:, EK[cols[0]]], E_R[:, EK[cols[0]]]]); print(f"     REF {name}: ({E_F[:,EK[cols[0]]].mean():.4f}, {E_R[:,EK[cols[0]]].mean():.4f}, {allv.std(ddof=1):.4f})")
