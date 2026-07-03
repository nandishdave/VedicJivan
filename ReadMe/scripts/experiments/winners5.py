"""Verified Winners composite + candidate Rule 5 (upachaya OCCUPANCY dasha).
Rule 5 = year-weighted peak (20-50) fraction under a dasha lord SITTING in 3/6/10/11.
Compare 4-factor vs 5-factor: per-factor lift, CV count/sum AUC, matched-India cuts.
Famous(207) vs ordinary(96)."""
import json
import numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS, _get_dignity
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha

FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8"))
ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55,
       "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}
_BAD = {3, 6, 8, 12}; OCC = {3, 6, 10, 11}
FEAT = ["rahu_natal", "d60_crude", "av_10th", "av_1st", "upa_occ"]

def feats(dob, tob, lat, lon):
    c = build_muhurta_chart(dob=dob, tob=tob, lat=lat, lon=lon)
    P, lag = c["planets"], c["lagna"]; ls = lag["sign"]; by = int(dob[:4])
    dl = calc_vimshottari_dasha(P["Moon"]["longitude"], dob, tob)["dashas"]
    # rule 1 — Rahu prime-dasha years x clean-dispositor factor
    ra = next(((int(d["start_date"][:4]) - by, int(d["end_date"][:4]) - by) for d in dl if d["planet"] == "Rahu"), None)
    natal = max(0, min(ra[1], 50) - max(ra[0], 20)) if ra else 0
    dispf = 1.0 if P[SIGN_LORDS[P["Rahu"]["sign"]]]["house"] not in _BAD else 0.4
    rahu_natal = natal * dispf
    # rule 2 — crude D60 dignity of the 7
    from app.services.kundli_calculator.divisional import calc_divisional_charts
    D60 = calc_divisional_charts(P, lag)["D60"]
    d60c = float(np.mean([_DP.get(_get_dignity(p, D60[p]), 45) for p in _C]))
    # rules 3,4 — Ashtakavarga 10th / 1st
    tv = c["ashtakavarga"]["totals"]; av10 = tv[(ls + 9) % 12]; av1 = tv[ls]
    # rule 5 — peak fraction under a dasha lord SITTING in 3/6/10/11 (occupancy)
    tot = occ = 0.0
    for d in dl:
        ov = max(0, min(int(d["end_date"][:4]) - by, 50) - max(int(d["start_date"][:4]) - by, 20))
        if ov <= 0: continue
        tot += ov
        if P[d["planet"]]["house"] in OCC: occ += ov
    upa_occ = occ / tot if tot else 0.0
    return [rahu_natal, d60c, av10, av1, upa_occ], by, (68 <= lon <= 98 and 6 <= lat <= 37)

def bd(p): return (p["birth"]["date"], p["birth"]["time"], p["birth"]["lat"], p["birth"]["lon"])
FR = [feats(*bd(p)) for p in FAM]; RR = [feats(*bd(p)) for p in ORDD]
F = np.array([x[0] for x in FR]); R = np.array([x[0] for x in RR])
FY = np.array([x[1] for x in FR]); FI = np.array([x[2] for x in FR])

print(f"famous={len(F)}  ordinary={len(R)}\nlift (fam | ord | diff):")
for i, n in enumerate(FEAT):
    print(f"  {n:11} {F[:,i].mean():7.2f} {R[:,i].mean():7.2f}  {F[:,i].mean()-R[:,i].mean():+6.2f}")

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

print()
c4, s4 = cv(F[:, :4], R[:, :4]); print(f"  4-factor WINNERS (verified)      count-AUC={c4:.3f}  sum-AUC={s4:.3f}")
c5, s5 = cv(F[:, :5], R[:, :5]); print(f"  5-factor (+ upachaya occupancy)  count-AUC={c5:.3f}  sum-AUC={s5:.3f}")

print("\nmatched-India cuts — 5-factor (sum-AUC):")
for yr in (0, 1940, 1955):
    mask = (FY >= yr) & FI; Fm = F[mask]
    if len(Fm) < 20:
        print(f"  India-born >= {yr}: n={len(Fm)} (too small)"); continue
    _, s = cv(Fm[:, :5], R[:, :5])
    print(f"  India-born >= {yr:4d}   n_fam={len(Fm):3d}  avg_yr={int(FY[mask].mean())}   sum-AUC={s:.3f}")
