# -*- coding: utf-8 -*-
"""Three Moon-centric tests, famous(225) vs ordinary(96):
1. Chandra Kundali: the 8 factors computed from the MOON sign as 1st house vs the Lagna.
2. Bright-Moon strength (tithi Shukla-7 .. Krishna-7 = elongation 72-264 deg).
3. Moon-nakshatra-lord / Moon-sign-dispositor connecting to Lagna / Lagnesh.
Note: factors 6/7 use a SIMPLIFIED yoga-lord activation (set membership), applied
identically to both references, so the Lagna-vs-Moon comparison is apples-to-apples
(absolute AUC differs slightly from the production graded 0.643)."""
import json
import numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS, _get_dignity
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha
from app.services.kundli_calculator.divisional import calc_divisional_charts

FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8"))
ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55,
       "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}
_BAD = {3, 6, 8, 12}; _OCC = {3, 6, 10, 11}
VIMLORD = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
def nak_of(lon): return int((lon % 360) / (360 / 27)) % 27

def eight_factors(P, dl, tv, D60, R, by):
    ra = next(((int(d["start_date"][:4]) - by, int(d["end_date"][:4]) - by) for d in dl if d["planet"] == "Rahu"), None)
    ry = max(0, min(ra[1], 50) - max(ra[0], 20)) if ra else 0
    disp = SIGN_LORDS[P["Rahu"]["sign"]]
    disp_h = ((P[disp]["sign"] - R) % 12) + 1
    rahu = ry * (1.0 if disp_h not in _BAD else 0.4)
    d60c = float(np.mean([_DP.get(_get_dignity(p, D60[p]), 45) for p in _C]))
    av10, av1, av11 = tv[(R + 9) % 12], tv[R], tv[(R + 10) % 12]
    def Lr(h): return SIGN_LORDS[(R + h - 1) % 12]
    raja_set = {Lr(h) for h in (1, 4, 7, 10)} | {Lr(h) for h in (1, 5, 9)}
    dhana_set = {Lr(h) for h in (1, 2, 11)}
    tot = occ = rl = dl2 = t2 = 0.0
    for d in dl:
        ov = max(0, min(int(d["end_date"][:4]) - by, 50) - max(int(d["start_date"][:4]) - by, 20))
        if ov > 0:
            tot += ov
            if ((P[d["planet"]]["sign"] - R) % 12) + 1 in _OCC: occ += ov
        ovl = max(0, min(int(d["end_date"][:4]) - by, 80) - max(int(d["start_date"][:4]) - by, 50))
        if ovl > 0:
            t2 += ovl
            if d["planet"] in raja_set: rl += ovl
            if d["planet"] in dhana_set: dl2 += ovl
    upa = occ / tot if tot else 0.0
    return [rahu, d60c, av10, av1, upa, rl / t2 if t2 else 0, dl2 / t2 if t2 else 0, av11]

def features(p):
    b = p["birth"]
    c = build_muhurta_chart(dob=b["date"], tob=b["time"], lat=b["lat"], lon=b["lon"], with_shadbala=False)
    P, lag = c["planets"], c["lagna"]; ls = lag["sign"]; by = int(b["date"][:4])
    dl = calc_vimshottari_dasha(P["Moon"]["longitude"], b["date"], b["time"])["dashas"]
    tv = c["ashtakavarga"]["totals"]; D60 = calc_divisional_charts(P, lag)["D60"]
    ms = P["Moon"]["sign"]
    lag8 = eight_factors(P, dl, tv, D60, ls, by)
    moon8 = eight_factors(P, dl, tv, D60, ms, by)
    # bright moon (elongation 72-264)
    elong = (P["Moon"]["longitude"] - P["Sun"]["longitude"]) % 360
    bright = 1.0 if 72 <= elong <= 264 else 0.0
    # moon nak-lord / dispositor connect to lagna/lagnesh
    asp = c["graha_drishti"]["planet_aspects"]; LL = SIGN_LORDS[ls]
    mnl = VIMLORD[nak_of(P["Moon"]["longitude"]) % 9]; mdisp = SIGN_LORDS[ms]
    def connects(X):
        if X == LL: return True
        if P[X]["house"] == P[LL]["house"]: return True
        if P[LL]["house"] in asp.get(X, []) or P[X]["house"] in asp.get(LL, []): return True
        if SIGN_LORDS[P[X]["sign"]] == LL and SIGN_LORDS[P[LL]["sign"]] == X: return True
        if P[X]["house"] == 1 or 1 in asp.get(X, []): return True
        return False
    conn = 1.0 if (connects(mnl) or connects(mdisp)) else 0.0
    return lag8, moon8, bright, conn

FR = [features(p) for p in FAM]; RR = [features(p) for p in ORDD]
yv = np.array([1] * len(FR) + [0] * len(RR), float)
def auc(sc):
    p, n = sc[yv == 1], sc[yv == 0]
    return float(np.mean([np.mean(x > n) + 0.5 * np.mean(x == n) for x in p]))
def cv(cols, F, R):
    X = np.vstack([F[:, cols], R[:, cols]]); y = yv
    np.random.seed(7); idx = np.random.permutation(len(y)); folds = np.array_split(idx, 5); cvs = np.zeros(len(y))
    for i in range(5):
        te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
        sg = np.sign(X[tr][y[tr] == 1].mean(0) - X[tr][y[tr] == 0].mean(0))
        m, s = X[tr].mean(0), X[tr].std(0) + 1e-9; cvs[te] = (((X[te] - m) / s) * sg).sum(1)
    return auc(cvs)

LAG = np.array([r[0] for r in FR + RR]); MOON = np.array([r[1] for r in FR + RR])
Flag, Rlag = LAG[:len(FR)], LAG[len(FR):]; Fm, Rm = MOON[:len(FR)], MOON[len(FR):]
print(f"famous={len(FR)} ordinary={len(RR)}")
print("\n=== 1. Chandra Kundali: 8 factors from Lagna vs from Moon (simplified yogas, apples-to-apples) ===")
print(f"  Lagna-ref 8-factor   sum-AUC={cv(list(range(8)), Flag, Rlag):.3f}")
print(f"  Moon-ref  8-factor   sum-AUC={cv(list(range(8)), Fm, Rm):.3f}")
BOTH = np.hstack([LAG, MOON]); Fb, Rb = BOTH[:len(FR)], BOTH[len(FR):]
print(f"  Lagna + Moon (16)    sum-AUC={cv(list(range(16)), Fb, Rb):.3f}")

br = np.array([r[2] for r in FR + RR]); cn = np.array([r[3] for r in FR + RR])
print("\n=== 2. Bright Moon (Shukla-7 .. Krishna-7) ===")
print(f"  famous {br[yv==1].mean()*100:.0f}%  ordinary {br[yv==0].mean()*100:.0f}%  AUC={auc(br):.3f}")
print("\n=== 3. Moon nak-lord / dispositor connects to Lagna or Lagnesh ===")
print(f"  famous {cn[yv==1].mean()*100:.0f}%  ordinary {cn[yv==0].mean()*100:.0f}%  AUC={auc(cn):.3f}")
