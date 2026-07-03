"""RICH D10 (Dasamsa / career chart) test — the proper significators, not crude
dignity: D10-lagna-lord condition, D10-10th-lord condition (dignity + placement),
and D10 10th-house occupants. Solo lift/AUC + does it lift the 8-factor composite?
Famous(207) vs ordinary(96). No Shadbala needed -> fast."""
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
_BAD = {3, 6, 8, 12}; _OCC = {3, 6, 10, 11}; _GOOD = {1, 4, 5, 7, 9, 10}
# 0-7 = the 8 winners; 8+ = D10-rich features
FEAT = ["rahu_prime", "d60", "av_10th", "av_1st", "upa_occ", "raja_late", "dhana_late", "av_11th",
        "d10_laglord_dig", "d10_10lord_dig", "d10_10lord_place", "d10_laglord_place", "d10_10th_occ", "d10_career"]

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
    dv = calc_divisional_charts(P, lag); D60, D10 = dv["D60"], dv["D10"]
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

    # ---- RICH D10 ----
    d10_lag = D10["Lagna"]
    laglord = SIGN_LORDS[d10_lag]
    tenth_sign = (d10_lag + 9) % 12
    tenlord = SIGN_LORDS[tenth_sign]
    def dig(pl): return _DP.get(_get_dignity(pl, D10[pl]), 45)
    def house_in_d10(pl): return ((D10[pl] - d10_lag) % 12) + 1
    def place(pl):
        h = house_in_d10(pl)
        return 100.0 if h in _GOOD else 40.0 if h in _BAD else 60.0
    d10_laglord_dig = dig(laglord)
    d10_10lord_dig = dig(tenlord)
    d10_10lord_place = place(tenlord)
    d10_laglord_place = place(laglord)
    occs = [p for p in _C if D10[p] == tenth_sign]
    d10_10th_occ = float(np.mean([dig(p) for p in occs])) if occs else 45.0
    # combined "career strength in D10": 10th-lord dignity+placement carry most
    d10_career = 0.35 * d10_10lord_dig + 0.2 * d10_10lord_place + 0.2 * d10_laglord_dig \
        + 0.1 * d10_laglord_place + 0.15 * d10_10th_occ

    return [rahu, d60c, av10, av1, upa, rl, dhl, av11,
            d10_laglord_dig, d10_10lord_dig, d10_10lord_place, d10_laglord_place, d10_10th_occ, d10_career], by, (68 <= lon <= 98 and 6 <= lat <= 37)

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

print(f"famous={len(F)}  ordinary={len(R)}\nRICH-D10 factors — lift + solo AUC:")
for i in range(8, 14):
    a = np.concatenate([F[:, i], R[:, i]])
    print(f"  {FEAT[i]:18} {F[:,i].mean():7.2f} {R[:,i].mean():7.2f}  {F[:,i].mean()-R[:,i].mean():+6.2f}  soloAUC={auc(a, yv):.3f}")
base = list(range(8))
print()
c8, s8 = cv(base); print(f"  8-factor (verified)          count-AUC={c8:.3f}  sum-AUC={s8:.3f}")
for i in range(8, 14):
    cc, ss = cv(base + [i]); print(f"  + {FEAT[i]:18}         count-AUC={cc:.3f}  sum-AUC={ss:.3f}")
print("\nmatched-India cuts (sum-AUC): 8f -> 8f+d10_career")
for yr in (0, 1940, 1955):
    mask = (FY >= yr) & FI
    if mask.sum() < 20: continue
    _, a8 = cv(base, F[mask], R); _, ac = cv(base + [13], F[mask], R)
    print(f"  India >= {yr:4d}  n={mask.sum():3d}   {a8:.3f} -> {ac:.3f}")
