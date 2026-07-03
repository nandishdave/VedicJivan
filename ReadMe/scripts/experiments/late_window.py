"""(a) Rahu factor window sweep 20-50/20-70/20-80 in the 5-factor composite.
(b) Pure-late yoga activation (50-80) — Raja & Dhana.
(c) 7-factor = 5 winners + late Raja-activation + late Dhana-activation.
Full set + matched-India cuts. Famous(207) vs ordinary(96)."""
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
_BAD = {3, 6, 8, 12}; OCC = {3, 6, 10, 11}
# feat idx: 0 rahu2050 1 rahu2070 2 rahu2080 3 d60 4 av10 5 av1 6 upa_occ 7 raja_act5080 8 dhana_act5080

def pw(links):
    w = {}
    for lk in links:
        for p in lk.get("planets", []):
            w[p] = w.get(p, 0.0) + lk["score"]
    return w

def feats(dob, tob, lat, lon):
    c = build_muhurta_chart(dob=dob, tob=tob, lat=lat, lon=lon)
    P, lag = c["planets"], c["lagna"]; ls = lag["sign"]; by = int(dob[:4])
    dl = calc_vimshottari_dasha(P["Moon"]["longitude"], dob, tob)["dashas"]
    ra = next(((int(d["start_date"][:4]) - by, int(d["end_date"][:4]) - by) for d in dl if d["planet"] == "Rahu"), None)
    dispf = 1.0 if P[SIGN_LORDS[P["Rahu"]["sign"]]]["house"] not in _BAD else 0.4
    def rahu_win(a, b): return (max(0, min(ra[1], b) - max(ra[0], a)) if ra else 0) * dispf
    D60 = calc_divisional_charts(P, lag)["D60"]
    d60c = float(np.mean([_DP.get(_get_dignity(p, D60[p]), 45) for p in _C]))
    tv = c["ashtakavarga"]["totals"]; av10 = tv[(ls + 9) % 12]; av1 = tv[ls]
    tot = occ = 0.0
    for d in dl:
        ov = max(0, min(int(d["end_date"][:4]) - by, 50) - max(int(d["start_date"][:4]) - by, 20))
        if ov <= 0: continue
        tot += ov
        if P[d["planet"]]["house"] in OCC: occ += ov
    upa_occ = occ / tot if tot else 0.0
    raja_w = pw(raja_yoga_score(c)[1]); dhana_w = pw(dhana_yoga_score(c)[1])
    t2 = ra2 = da2 = 0.0
    for d in dl:
        ov = max(0, min(int(d["end_date"][:4]) - by, 80) - max(int(d["start_date"][:4]) - by, 50))
        if ov <= 0: continue
        t2 += ov; L = d["planet"]; ra2 += raja_w.get(L, 0.0) * ov; da2 += dhana_w.get(L, 0.0) * ov
    raja_act = ra2 / t2 if t2 else 0.0; dhana_act = da2 / t2 if t2 else 0.0
    return [rahu_win(20, 50), rahu_win(20, 70), rahu_win(20, 80), d60c, av10, av1, upa_occ, raja_act, dhana_act], by, (68 <= lon <= 98 and 6 <= lat <= 37)

def bd(p): return (p["birth"]["date"], p["birth"]["time"], p["birth"]["lat"], p["birth"]["lon"])
FR = [feats(*bd(p)) for p in FAM]; RR = [feats(*bd(p)) for p in ORDD]
F = np.array([x[0] for x in FR]); R = np.array([x[0] for x in RR])
FY = np.array([x[1] for x in FR]); FI = np.array([x[2] for x in FR])

def auc(sc, yy):
    pos = sc[yy == 1]; neg = sc[yy == 0]
    return float(np.mean([np.mean(p > neg) + 0.5 * np.mean(p == neg) for p in pos]))
def cv(Xf, Xr):
    X = np.vstack([Xf, Xr]); y = np.array([1] * len(Xf) + [0] * len(Xr), float)
    np.random.seed(7); idx = np.random.permutation(len(y)); folds = np.array_split(idx, 5)
    cvc = np.zeros(len(y)); cvs = np.zeros(len(y))
    for i in range(5):
        te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
        sg = np.sign(X[tr][y[tr] == 1].mean(0) - X[tr][y[tr] == 0].mean(0))
        m, s = X[tr].mean(0), X[tr].std(0) + 1e-9; Z = ((X[te] - m) / s) * sg
        cvc[te] = (Z > 0).sum(1); cvs[te] = Z.sum(1)
    return auc(cvc, y), auc(cvs, y)
def matched(cols, label):
    print(f"  {label}")
    for yr in (0, 1940, 1955):
        mask = (FY >= yr) & FI; Fm = F[mask]
        if len(Fm) < 20: continue
        _, s = cv(Fm[:, cols], R[:, cols])
        print(f"      India >= {yr:4d}  n={len(Fm):3d}   sum-AUC={s:.3f}")

print(f"famous={len(F)}  ordinary={len(R)}")
print("\n=== (a) Rahu window sweep in the 5-factor composite ===")
for wi, wn in [(0, "20-50 (current)"), (1, "20-70"), (2, "20-80")]:
    cols = [wi, 3, 4, 5, 6]
    c, s = cv(F[:, cols], R[:, cols])
    print(f"  Rahu {wn:16s} 5-factor  count-AUC={c:.3f}  sum-AUC={s:.3f}")

print("\n=== (b) Pure-late yoga activation (window 50-80) ===")
for idx, nm in [(7, "RAJA activation 50-80"), (8, "DHANA activation 50-80")]:
    fm, rm = F[:, idx].mean(), R[:, idx].mean()
    print(f"  {nm:24s} fam={fm:6.3f} ord={rm:6.3f} lift={fm-rm:+.3f}  AUC={auc(np.concatenate([F[:,idx],R[:,idx]]), np.array([1]*len(F)+[0]*len(R),float)):.3f}")

print("\n=== (c) 7-factor = 5 winners + late Raja-act + late Dhana-act ===")
for wi, wn in [(0, "Rahu 20-50"), (2, "Rahu 20-80")]:
    cols = [wi, 3, 4, 5, 6, 7, 8]
    c, s = cv(F[:, cols], R[:, cols])
    print(f"  7-factor ({wn}):  count-AUC={c:.3f}  sum-AUC={s:.3f}")
    matched(cols, f"matched cuts ({wn}):")
