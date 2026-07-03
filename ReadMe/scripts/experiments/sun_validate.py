# -*- coding: utf-8 -*-
"""Clean Sun-dispositor validation: solo AUC (correct) + does a Sun factor lift
the 11-factor composite to 12? Tests house-sets and the Lagna/Lagnesh connection.
Checks independence from the existing moon_disp factor. (225 vs 96)"""
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
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55, "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}
_BAD = {3, 6, 8, 12}; _OCC = {3, 6, 10, 11}; MDISP = {1, 2, 11, 12}

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
    bright = 1.0 if 72 <= elong <= 264 else 0.0
    moon_disp = 1.0 if P[SIGN_LORDS[ms]]["house"] in MDISP else 0.0
    moon_sav = tv[ms]
    f11 = [rahu, d60c, av10, av1, upa, rl, dhl, av11, bright, moon_disp, moon_sav]
    # Sun extras
    ss = P["Sun"]["sign"]; sdisp = SIGN_LORDS[ss]; sdh = P[sdisp]["house"]
    asp = c["graha_drishti"]["planet_aspects"]; LL = SIGN_LORDS[ls]
    def conn(X):
        if X == LL or P[X]["house"] == P[LL]["house"]: return True
        if P[LL]["house"] in asp.get(X, []) or P[X]["house"] in asp.get(LL, []): return True
        if SIGN_LORDS[P[X]["sign"]] == LL and SIGN_LORDS[P[LL]["sign"]] == X: return True
        return P[X]["house"] == 1 or 1 in asp.get(X, [])
    return f11, sdh, (1.0 if conn(sdisp) else 0.0), (68 <= b["lon"] <= 98 and 6 <= b["lat"] <= 37)

FR = [feats(p) for p in FAM]; RR = [feats(p) for p in ORDD]
F11 = np.array([x[0] for x in FR]); R11 = np.array([x[0] for x in RR])
Fh = np.array([x[1] for x in FR]); Rh = np.array([x[1] for x in RR])
Fc = np.array([x[2] for x in FR]); Rc = np.array([x[2] for x in RR])
FY = np.array([int(p["birth"]["date"][:4]) for p in FAM])
FI = np.array([x[3] for x in FR])
yv = np.array([1] * len(FR) + [0] * len(RR), float)
def auc(fa, ra): return float(np.mean([np.mean(x > ra) + 0.5 * np.mean(x == ra) for x in fa]))
def cv(F, R):
    X = np.vstack([F, R]); y = np.array([1] * len(F) + [0] * len(R), float)
    np.random.seed(7); idx = np.random.permutation(len(y)); folds = np.array_split(idx, 5); s = np.zeros(len(y))
    for i in range(5):
        te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
        sg = np.sign(X[tr][y[tr] == 1].mean(0) - X[tr][y[tr] == 0].mean(0)); m, sd = X[tr].mean(0), X[tr].std(0) + 1e-9
        s[te] = (((X[te] - m) / sd) * sg).sum(1)
    return auc(s[y == 1], s[y == 0])

base_full = cv(F11, R11); mask = (FY >= 1940) & FI; base_1940 = cv(F11[mask], R11)
print(f"11-factor baseline: full={base_full:.3f}  >=1940={base_1940:.3f}\n")
print(f"  {'candidate':22} fam%  ord%  solo   12f-full  12f>=1940")
def test(name, ff, rf):
    solo = auc(ff, rf)  # ff = famous flags, rf = ordinary flags
    F12 = np.column_stack([F11, ff]); R12 = np.column_stack([R11, rf])
    print(f"  {name:22} {ff.mean()*100:4.0f}  {rf.mean()*100:4.0f}  {solo:.3f}  {cv(F12,R12):.3f}     {cv(F12[mask],R12):.3f}")
for S in [{1}, {1, 3, 4}, {1, 2, 3, 4}]:
    test(f"sun_disp in {sorted(S)}", np.array([1.0 if h in S else 0.0 for h in Fh]), np.array([1.0 if h in S else 0.0 for h in Rh]))
test("sun_disp connects L/LL", Fc, Rc)
