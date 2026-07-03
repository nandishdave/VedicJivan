"""Do D10 (Dasamsa) dignity and/or 11th-house Ashtakavarga lift the verified
7-factor fame composite? Per-factor lift + solo AUC + 7f vs +av11 vs +d10 vs
+both, full set + matched-India cuts. Famous(207) vs ordinary(96)."""
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
FEAT = ["rahu_prime", "d60", "av_10th", "av_1st", "upa_occ", "raja_late", "dhana_late", "av_11th", "d10"]

def _pw(links):
    w = {}
    for lk in links:
        for p in lk.get("planets", []):
            w[p] = w.get(p, 0.0) + lk["score"]
    return w
def _act(dl, by, wd, a, b):
    tot = acc = 0.0
    for d in dl:
        ov = max(0, min(int(d["end_date"][:4]) - by, b) - max(int(d["start_date"][:4]) - by, a))
        if ov <= 0: continue
        tot += ov; acc += wd.get(d["planet"], 0.0) * ov
    return acc / tot if tot else 0.0

def feats(dob, tob, lat, lon):
    c = build_muhurta_chart(dob=dob, tob=tob, lat=lat, lon=lon)
    P, lag = c["planets"], c["lagna"]; ls = lag["sign"]; by = int(dob[:4])
    dl = calc_vimshottari_dasha(P["Moon"]["longitude"], dob, tob)["dashas"]
    ra = next(((int(d["start_date"][:4]) - by, int(d["end_date"][:4]) - by) for d in dl if d["planet"] == "Rahu"), None)
    dispf = 1.0 if P[SIGN_LORDS[P["Rahu"]["sign"]]]["house"] not in _BAD else 0.4
    rahu = (max(0, min(ra[1], 50) - max(ra[0], 20)) if ra else 0) * dispf
    dv = calc_divisional_charts(P, lag); D60 = dv["D60"]; D10 = dv["D10"]
    d60c = float(np.mean([_DP.get(_get_dignity(p, D60[p]), 45) for p in _C]))
    d10c = float(np.mean([_DP.get(_get_dignity(p, D10[p]), 45) for p in _C]))
    tv = c["ashtakavarga"]["totals"]; av10 = tv[(ls + 9) % 12]; av1 = tv[ls]; av11 = tv[(ls + 10) % 12]
    tot = occ = 0.0
    for d in dl:
        ov = max(0, min(int(d["end_date"][:4]) - by, 50) - max(int(d["start_date"][:4]) - by, 20))
        if ov <= 0: continue
        tot += ov
        if P[d["planet"]]["house"] in OCC: occ += ov
    upa = occ / tot if tot else 0.0
    return [rahu, d60c, av10, av1, upa, _act(dl, by, _pw(raja_yoga_score(c)[1]), 50, 80),
            _act(dl, by, _pw(dhana_yoga_score(c)[1]), 50, 80), av11, d10c], by, (68 <= lon <= 98 and 6 <= lat <= 37)

def bd(p): return (p["birth"]["date"], p["birth"]["time"], p["birth"]["lat"], p["birth"]["lon"])
FR = [feats(*bd(p)) for p in FAM]; RR = [feats(*bd(p)) for p in ORDD]
F = np.array([x[0] for x in FR]); R = np.array([x[0] for x in RR])
FY = np.array([x[1] for x in FR]); FI = np.array([x[2] for x in FR])
yv = np.array([1] * len(F) + [0] * len(R), float)

def auc(sc, yy):
    pos = sc[yy == 1]; neg = sc[yy == 0]
    return float(np.mean([np.mean(p > neg) + 0.5 * np.mean(p == neg) for p in pos]))
def cv(cols, Fm=F, Rm=R):
    X = np.vstack([Fm[:, cols], Rm[:, cols]]); y = np.array([1] * len(Fm) + [0] * len(Rm), float)
    np.random.seed(7); idx = np.random.permutation(len(y)); folds = np.array_split(idx, 5)
    cvc = np.zeros(len(y)); cvs = np.zeros(len(y))
    for i in range(5):
        te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
        sg = np.sign(X[tr][y[tr] == 1].mean(0) - X[tr][y[tr] == 0].mean(0))
        m, sd = X[tr].mean(0), X[tr].std(0) + 1e-9; Z = ((X[te] - m) / sd) * sg
        cvc[te] = (Z > 0).sum(1); cvs[te] = Z.sum(1)
    return auc(cvc, y), auc(cvs, y)

print(f"famous={len(F)}  ordinary={len(R)}\nper-factor lift + solo AUC:")
for i, n in enumerate(FEAT):
    a = np.concatenate([F[:, i], R[:, i]])
    print(f"  {n:11} {F[:,i].mean():7.2f} {R[:,i].mean():7.2f}  {F[:,i].mean()-R[:,i].mean():+6.2f}  soloAUC={auc(a, yv):.3f}")
base = list(range(7))
print()
for lab, cols in [("7-factor (verified)", base), ("+ av_11th", base + [7]), ("+ d10", base + [8]), ("+ both", base + [7, 8])]:
    cc, ss = cv(cols)
    print(f"  {lab:22s} count-AUC={cc:.3f}  sum-AUC={ss:.3f}")
print("\nmatched-India cuts (sum-AUC): 7f -> +both")
for yr in (0, 1940, 1955):
    mask = (FY >= yr) & FI
    if mask.sum() < 20: continue
    _, a7 = cv(base, F[mask], R); _, ab = cv(base + [7, 8], F[mask], R)
    print(f"  India >= {yr:4d}  n={mask.sum():3d}   {a7:.3f} -> {ab:.3f}")
