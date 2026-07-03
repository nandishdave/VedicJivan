# -*- coding: utf-8 -*-
"""Moon-dispositor by ALL houses + test which house-set for factor 10 is best.
225 vs 96. Computes the 10 other factors once, varies only the disp-house set."""
import json
import numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS, _get_dignity
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha
from app.services.kundli_calculator.divisional import calc_divisional_charts
from app.services.kundli_calculator.raja_yoga import raja_yoga_score
from app.services.kundli_calculator.dhana_yoga import dhana_yoga_score

FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8"))
ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55,
       "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}
_BAD = {3, 6, 8, 12}; _OCC = {3, 6, 10, 11}

def _pw(links):
    w = {}
    for lk in links:
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
    bright = 1.0 if 72 <= elong <= 264 else 0.0; moon_sav = tv[ms]
    disp_house = P[SIGN_LORDS[ms]]["house"]
    india = (68 <= b["lon"] <= 98 and 6 <= b["lat"] <= 37)
    # 10 fixed factors (moon_disp inserted later), + raw disp_house
    return [rahu, d60c, av10, av1, upa, rl, dhl, av11, bright, moon_sav], disp_house, by, india

FR = [feats(p) for p in FAM]; RR = [feats(p) for p in ORDD]
F10 = np.array([x[0] for x in FR]); R10 = np.array([x[0] for x in RR])
Fh = np.array([x[1] for x in FR]); Rh = np.array([x[1] for x in RR])
FY = np.array([x[2] for x in FR]); FI = np.array([x[3] for x in FR])
yv = np.array([1] * len(FR) + [0] * len(RR), float)

print("=== Moon-dispositor by house (famous% | ordinary% | diff) — 225 vs 96 ===")
for h in range(1, 13):
    fa = np.mean(Fh == h) * 100; ra = np.mean(Rh == h) * 100
    print(f"  house {h:2}: {fa:4.1f}% | {ra:4.1f}%  ({fa-ra:+4.1f})" + ("  <-- famous" if fa - ra > 2 else "  <-- ordinary" if fa - ra < -2 else ""))

def auc(sc, yy):
    p, n = sc[yy == 1], sc[yy == 0]; return float(np.mean([np.mean(x > n) + 0.5 * np.mean(x == n) for x in p]))
def cv(F, R):
    X = np.vstack([F, R]); y = np.array([1] * len(F) + [0] * len(R), float)
    np.random.seed(7); idx = np.random.permutation(len(y)); folds = np.array_split(idx, 5); ss = np.zeros(len(y))
    for i in range(5):
        te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
        sg = np.sign(X[tr][y[tr] == 1].mean(0) - X[tr][y[tr] == 0].mean(0)); m, sd = X[tr].mean(0), X[tr].std(0) + 1e-9
        ss[te] = (((X[te] - m) / sd) * sg).sum(1)
    return auc(ss, y)

print("\n=== which house-set for factor 10? (solo AUC | 11-factor full | matched >=1940) ===")
for S in [{1, 2}, {1, 2, 11}, {1, 2, 12}, {1, 2, 11, 12}, {1, 2, 8, 11, 12}]:
    ff = np.array([1.0 if h in S else 0.0 for h in Fh]); rf = np.array([1.0 if h in S else 0.0 for h in Rh])
    solo = auc(np.concatenate([ff, rf]), yv)
    F11 = np.column_stack([F10, ff]); R11 = np.column_stack([R10, rf])
    full = cv(F11, R11)
    mask = (FY >= 1940) & FI; m1940 = cv(F11[mask], R11)
    fpct, opct = ff.mean() * 100, rf.mean() * 100
    print(f"  {str(sorted(S)):18} fam {fpct:4.0f}% ord {opct:4.0f}%  solo={solo:.3f}  full={full:.3f}  >=1940={m1940:.3f}")
