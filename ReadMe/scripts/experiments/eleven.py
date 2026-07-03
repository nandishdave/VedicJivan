# -*- coding: utf-8 -*-
"""Validate the 3 Moon factors: does 8 -> 11 lift the composite? (225 vs 96)
Uses the REAL production 8 factors (graded yogas) + capture REF for the new 3."""
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
FEAT = ["rahu_prime", "d60", "av_10th", "av_1st", "upa_occ", "raja_late", "dhana_late", "av_11th",
        "bright_moon", "moon_disp_12", "moon_sav"]

def _pw(links):
    w = {}
    for lk in links:
        for p in lk.get("planets", []): w[p] = w.get(p, 0.0) + lk["score"]
    return w
def _act(dl, by, wd, a, b):
    tot = acc = 0.0
    for d in dl:
        ov = max(0, min(int(d["end_date"][:4]) - by, b) - max(int(d["start_date"][:4]) - by, a))
        if ov <= 0: continue
        tot += ov; acc += wd.get(d["planet"], 0.0) * ov
    return acc / tot if tot else 0.0

def feats(dob, tob, lat, lon):
    c = build_muhurta_chart(dob=dob, tob=tob, lat=lat, lon=lon, with_shadbala=False)
    P, lag = c["planets"], c["lagna"]; ls = lag["sign"]; by = int(dob[:4])
    dl = calc_vimshottari_dasha(P["Moon"]["longitude"], dob, tob)["dashas"]
    ra = next(((int(d["start_date"][:4]) - by, int(d["end_date"][:4]) - by) for d in dl if d["planet"] == "Rahu"), None)
    dispf = 1.0 if P[SIGN_LORDS[P["Rahu"]["sign"]]]["house"] not in _BAD else 0.4
    rahu = (max(0, min(ra[1], 50) - max(ra[0], 20)) if ra else 0) * dispf
    D60 = calc_divisional_charts(P, lag)["D60"]
    d60c = float(np.mean([_DP.get(_get_dignity(p, D60[p]), 45) for p in _C]))
    tv = c["ashtakavarga"]["totals"]; av10, av1, av11 = tv[(ls + 9) % 12], tv[ls], tv[(ls + 10) % 12]
    tot = occ = 0.0
    for d in dl:
        ov = max(0, min(int(d["end_date"][:4]) - by, 50) - max(int(d["start_date"][:4]) - by, 20))
        if ov <= 0: continue
        tot += ov
        if P[d["planet"]]["house"] in _OCC: occ += ov
    upa = occ / tot if tot else 0.0
    rl = _act(dl, by, _pw(raja_yoga_score(c)[1]), 50, 80); dhl = _act(dl, by, _pw(dhana_yoga_score(c)[1]), 50, 80)
    # --- 3 Moon factors ---
    ms = P["Moon"]["sign"]
    elong = (P["Moon"]["longitude"] - P["Sun"]["longitude"]) % 360
    bright = 1.0 if 72 <= elong <= 264 else 0.0
    moon_disp12 = 1.0 if P[SIGN_LORDS[ms]]["house"] in (1, 2) else 0.0
    moon_sav = tv[ms]
    return [rahu, d60c, av10, av1, upa, rl, dhl, av11, bright, moon_disp12, moon_sav], by, (68 <= lon <= 98 and 6 <= lat <= 37)

FR = [feats(*(p["birth"]["date"], p["birth"]["time"], p["birth"]["lat"], p["birth"]["lon"])) for p in FAM]
RR = [feats(*(p["birth"]["date"], p["birth"]["time"], p["birth"]["lat"], p["birth"]["lon"])) for p in ORDD]
F = np.array([x[0] for x in FR]); R = np.array([x[0] for x in RR])
FY = np.array([x[1] for x in FR]); FI = np.array([x[2] for x in FR])
yv = np.array([1] * len(F) + [0] * len(R), float)
def auc(sc, yy):
    p, n = sc[yy == 1], sc[yy == 0]
    return float(np.mean([np.mean(x > n) + 0.5 * np.mean(x == n) for x in p]))
def cv(cols, Fm=F, Rm=R):
    X = np.vstack([Fm[:, cols], Rm[:, cols]]); y = np.array([1] * len(Fm) + [0] * len(Rm), float)
    np.random.seed(7); idx = np.random.permutation(len(y)); folds = np.array_split(idx, 5)
    cc = np.zeros(len(y)); ss = np.zeros(len(y))
    for i in range(5):
        te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
        sg = np.sign(X[tr][y[tr] == 1].mean(0) - X[tr][y[tr] == 0].mean(0))
        m, sd = X[tr].mean(0), X[tr].std(0) + 1e-9; Z = ((X[te] - m) / sd) * sg
        cc[te] = (Z > 0).sum(1); ss[te] = Z.sum(1)
    return auc(cc, y), auc(ss, y)

print(f"famous={len(F)} ordinary={len(R)}\nnew-factor solo lift + AUC:")
for i in (8, 9, 10):
    print(f"  {FEAT[i]:12} fam={F[:,i].mean():6.2f} ord={R[:,i].mean():6.2f} lift={F[:,i].mean()-R[:,i].mean():+.2f} AUC={auc(np.concatenate([F[:,i],R[:,i]]), yv):.3f}")
print()
c8, s8 = cv(list(range(8))); print(f"  8-factor           count-AUC={c8:.3f}  sum-AUC={s8:.3f}")
c9, s9 = cv(list(range(9))); print(f"  9  (+bright)       count-AUC={c9:.3f}  sum-AUC={s9:.3f}")
c10, s10 = cv(list(range(10))); print(f"  10 (+moon_disp)    count-AUC={c10:.3f}  sum-AUC={s10:.3f}")
c11, s11 = cv(list(range(11))); print(f"  11 (+moon_sav)     count-AUC={c11:.3f}  sum-AUC={s11:.3f}")
print("\nmatched-India cuts (sum-AUC): 8f -> 11f")
for yr in (0, 1940, 1955):
    mask = (FY >= yr) & FI
    if mask.sum() < 20: continue
    _, a8 = cv(list(range(8)), F[mask], R); _, a11 = cv(list(range(11)), F[mask], R)
    print(f"  India >= {yr:4d}  n={mask.sum():3d}   {a8:.3f} -> {a11:.3f}")
ALL = np.vstack([F, R])
print("\nREF (fam_mean, ord_mean, pooled_std):")
for i in (8, 9, 10):
    print(f'  "{FEAT[i]}": ({F[:,i].mean():.4f}, {R[:,i].mean():.4f}, {ALL[:,i].std(ddof=1):.4f}),')
