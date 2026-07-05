# -*- coding: utf-8 -*-
"""ACID test for B (Mridu - Tikshna) vs A (Mridu), side by side. Per fold, re-derive:
  A: the single best-separating quality (add its count)
  B: the most famous-leaning quality (good) MINUS the most ordinary-leaning (bad)
score held-out. If (Tender,Dreadful) reproduce and the net lifts unseen charts, B survives.
(225/96, base = 16-factor)"""
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
QORDER = ["Swift","Violent","Mixed","Fixed","Tender","Dreadful","Movable"]
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
    qc = {q: 0 for q in QORDER}
    for q in _ALL: qc[quality(P[q]["longitude"])] += 1
    return f16, [float(qc[q]) for q in QORDER], by, (68 <= b["lon"] <= 98 and 6 <= b["lat"] <= 37)
FR = [feats(p) for p in FAM]; RR = [feats(p) for p in ORDD]
F = np.array([x[0] for x in FR]); R = np.array([x[0] for x in RR])
QF = np.array([x[1] for x in FR]); QR = np.array([x[1] for x in RR])
X = np.vstack([F, R]); Q = np.vstack([QF, QR]); Y = np.array([1]*len(FR)+[0]*len(RR), float)
def auc(fa, ra): return float(np.mean([np.mean(x > ra) + 0.5 * np.mean(x == ra) for x in fa]))
def base_cv(seed):
    Xx = X; y = Y
    np.random.seed(seed); idx = np.random.permutation(len(y)); folds = np.array_split(idx, 5); s = np.zeros(len(y))
    for i in range(5):
        te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
        sg = np.sign(Xx[tr][y[tr]==1].mean(0)-Xx[tr][y[tr]==0].mean(0)); m,sd=Xx[tr].mean(0),Xx[tr].std(0)+1e-9
        s[te]=(((Xx[te]-m)/sd)*sg).sum(1)
    return auc(s[y==1], s[y==0])
def nested(seed, mode):
    y = Y
    np.random.seed(seed); idx = np.random.permutation(len(y)); folds = np.array_split(idx, 5); s = np.zeros(len(y)); picks=[]
    for i in range(5):
        te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
        gap = [Q[tr][y[tr]==1,m].mean()-Q[tr][y[tr]==0,m].mean() for m in range(7)]
        if mode == "A":
            bm = int(np.argmax([abs(g)/(Q[tr][:,m].std()+1e-9) for m,g in enumerate(gap)]))
            feat = Q[:,bm]; picks.append(QORDER[bm])
        else:  # B: good (max gap) minus bad (min gap)
            good = int(np.argmax(gap)); bad = int(np.argmin(gap))
            feat = Q[:,good] - Q[:,bad]; picks.append((QORDER[good], QORDER[bad]))
        Xx = np.column_stack([X, feat]); sg=np.sign(Xx[tr][y[tr]==1].mean(0)-Xx[tr][y[tr]==0].mean(0))
        m,sd=Xx[tr].mean(0),Xx[tr].std(0)+1e-9; s[te]=(((Xx[te]-m)/sd)*sg).sum(1)
    return auc(s[y==1], s[y==0]), picks
SEEDS=[1,7,42,123,2024]
base = np.mean([base_cv(sd) for sd in SEEDS])
print(f"famous={len(FR)} ordinary={len(RR)}\n  base full (5-seed): {base:.3f}")
for mode, label in [("A","A = single best quality (Mridu)"), ("B","B = best-good MINUS worst-bad (Mridu-Tikshna)")]:
    vals=[nested(sd,mode)[0] for sd in SEEDS]
    _,pk7 = nested(7, mode)
    print(f"\n  {label}")
    print(f"    nested full (5-seed): {np.mean(vals):.3f}  {[f'{v:.3f}' for v in vals]}  delta={np.mean(vals)-base:+.3f}")
    print(f"    per-fold picks (seed7): {pk7}")
