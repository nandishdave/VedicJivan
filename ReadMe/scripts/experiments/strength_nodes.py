# -*- coding: utf-8 -*-
"""Does including Rahu/Ketu in Vimsopaka (factor 2 mean) and/or the strongest-planet
pick (factor 16 seat) help the fame model? Compare 7-graha (current) vs 9-graha variants
vs the same base-14. Also: how often is a node the strongest, famous vs ordinary? (225/96)"""
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
SEAT = {1, 2, 4, 5, 11}
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
    vim = {q: sum(w * (_DP.get(_get_dignity(q, (P[q]["sign"] if v == "D1" else dv[v][q])), 45) / 100.0) for v, w in _VARGA_W.items()) for q in _ALL}
    vim7 = float(np.mean([vim[q] for q in _C])); vim9 = float(np.mean([vim[q] for q in _ALL]))
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
    base14 = [rahu, av10, av1, upa, rl, dhl, av11, bright, moon_disp, moon_sav, sun_disp, arg, purna, dig_lords]
    top7 = max(_C, key=lambda q: vim[q]); top9 = max(_ALL, key=lambda q: vim[q])
    seat7 = 1.0 if P[top7]["house"] in SEAT else 0.0; seat9 = 1.0 if P[top9]["house"] in SEAT else 0.0
    node_is_top = 1.0 if top9 in ("Rahu", "Ketu") else 0.0
    extra = [vim7, vim9, seat7, seat9, node_is_top]
    return base14, [float(x) for x in extra], by, (68 <= b["lon"] <= 98 and 6 <= b["lat"] <= 37)
FR = [feats(p) for p in FAM]; RR = [feats(p) for p in ORDD]
B_F = np.array([x[0] for x in FR]); B_R = np.array([x[0] for x in RR])
E_F = np.array([x[1] for x in FR]); E_R = np.array([x[1] for x in RR])
FY = np.array([x[2] for x in FR]); FI = np.array([x[3] for x in FR])
CUTS = {"full": np.ones(len(FR), bool), ">=1940": (FY >= 1940) & FI, ">=1955": (FY >= 1955) & FI}
EK = {"vim7": 0, "vim9": 1, "seat7": 2, "seat9": 3, "node_top": 4}
def auc(fa, ra): return float(np.mean([np.mean(x > ra) + 0.5 * np.mean(x == ra) for x in fa]))
def cv(cols, cut, seed=7):
    Ff = np.column_stack([B_F[cut]] + [E_F[cut, EK[k]] for k in cols]); Rr = np.column_stack([B_R] + [E_R[:, EK[k]] for k in cols])
    X = np.vstack([Ff, Rr]); y = np.array([1]*len(Ff)+[0]*len(Rr), float)
    np.random.seed(seed); idx = np.random.permutation(len(y)); folds = np.array_split(idx, 5); s = np.zeros(len(y))
    for i in range(5):
        te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
        sg = np.sign(X[tr][y[tr]==1].mean(0) - X[tr][y[tr]==0].mean(0)); m, sd = X[tr].mean(0), X[tr].std(0)+1e-9
        s[te] = (((X[te]-m)/sd)*sg).sum(1)
    return auc(s[y==1], s[y==0])
SEEDS = [1, 7, 42, 123, 2024]
def line(name, cols):
    row = "  ".join(f"{k}={cv(cols, CUTS[k]):.3f}" for k in CUTS)
    m5 = np.mean([cv(cols, CUTS['full'], seed=sd) for sd in SEEDS])
    print(f"  {name:44} {row}   full-5seed={m5:.3f}")
print(f"famous={len(FR)} ordinary={len(RR)}")
print("\n=== descriptive: is a NODE the strongest-Vimsopaka planet (of 9)? ===")
print(f"  node is strongest: famous {E_F[:,EK['node_top']].mean()*100:.0f}%  ordinary {E_R[:,EK['node_top']].mean()*100:.0f}%  AUC {auc(E_F[:,EK['node_top']],E_R[:,EK['node_top']]):.3f}")
print(f"  mean Vimsopaka: 7-graha fam {E_F[:,0].mean():.2f}/ord {E_R[:,0].mean():.2f} (AUC {auc(E_F[:,0],E_R[:,0]):.3f}) | 9-graha fam {E_F[:,1].mean():.2f}/ord {E_R[:,1].mean():.2f} (AUC {auc(E_F[:,1],E_R[:,1]):.3f})")
print(f"  seat (strongest in 1/2/4/5/11): 7-graha AUC {auc(E_F[:,2],E_R[:,2]):.3f} | 9-graha AUC {auc(E_F[:,3],E_R[:,3]):.3f}")
print("\n=== model variants (sum-AUC, seed 7 + 5-seed full) ===")
line("A  vim7 + seat7  (CURRENT, 7-graha)", ["vim7", "seat7"])
line("B  vim7 + seat9  (nodes eligible for strongest)", ["vim7", "seat9"])
line("C  vim9 + seat9  (nodes in mean + strongest)", ["vim9", "seat9"])
line("D  vim9 + seat7  (nodes in mean only)", ["vim9", "seat7"])
