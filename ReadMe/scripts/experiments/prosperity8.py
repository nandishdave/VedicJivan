"""Prosperity yoga (5th/9th fortune links): static score + dasha activation
(prime 20-50 vs late 50-80), and whether it lifts the 7-factor to an 8-factor.
7-factor = Rahu(20-50) + D60 + av10 + av1 + upa_occ + late-Raja-act + late-Dhana-act.
Famous(207) vs ordinary(96)."""
import json
import numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS, _get_dignity
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha
from app.services.kundli_calculator.divisional import calc_divisional_charts
from app.services.kundli_calculator.raja_yoga import raja_yoga_score
from app.services.kundli_calculator.dhana_yoga import dhana_yoga_score, prosperity_yoga_score

FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8"))
ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55,
       "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}
_BAD = {3, 6, 8, 12}; OCC = {3, 6, 10, 11}
# idx: 0 rahu2050 1 d60 2 av10 3 av1 4 upa_occ 5 raja_act5080 6 dhana_act5080
#      7 prosp_static 8 prosp_act5080 9 prosp_act2050

def pw(links):
    w = {}
    for lk in links:
        for p in lk.get("planets", []):
            w[p] = w.get(p, 0.0) + lk["score"]
    return w
def act(dl, by, wdict, a, b):
    tot = acc = 0.0
    for d in dl:
        ov = max(0, min(int(d["end_date"][:4]) - by, b) - max(int(d["start_date"][:4]) - by, a))
        if ov <= 0: continue
        tot += ov; acc += wdict.get(d["planet"], 0.0) * ov
    return acc / tot if tot else 0.0

def feats(dob, tob, lat, lon):
    c = build_muhurta_chart(dob=dob, tob=tob, lat=lat, lon=lon)
    P, lag = c["planets"], c["lagna"]; ls = lag["sign"]; by = int(dob[:4])
    dl = calc_vimshottari_dasha(P["Moon"]["longitude"], dob, tob)["dashas"]
    ra = next(((int(d["start_date"][:4]) - by, int(d["end_date"][:4]) - by) for d in dl if d["planet"] == "Rahu"), None)
    dispf = 1.0 if P[SIGN_LORDS[P["Rahu"]["sign"]]]["house"] not in _BAD else 0.4
    rahu = (max(0, min(ra[1], 50) - max(ra[0], 20)) if ra else 0) * dispf
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
    prosp_score, prosp_links = prosperity_yoga_score(c); prosp_w = pw(prosp_links)
    return [rahu, d60c, av10, av1, upa_occ,
            act(dl, by, raja_w, 50, 80), act(dl, by, dhana_w, 50, 80),
            prosp_score, act(dl, by, prosp_w, 50, 80), act(dl, by, prosp_w, 20, 50)], by, (68 <= lon <= 98 and 6 <= lat <= 37)

def bd(p): return (p["birth"]["date"], p["birth"]["time"], p["birth"]["lat"], p["birth"]["lon"])
FR = [feats(*bd(p)) for p in FAM]; RR = [feats(*bd(p)) for p in ORDD]
F = np.array([x[0] for x in FR]); R = np.array([x[0] for x in RR])
FY = np.array([x[1] for x in FR]); FI = np.array([x[2] for x in FR])
yv = np.array([1] * len(F) + [0] * len(R), float)

def auc(sc, yy):
    pos = sc[yy == 1]; neg = sc[yy == 0]
    return float(np.mean([np.mean(p > neg) + 0.5 * np.mean(p == neg) for p in pos]))
def cv(cols):
    X = np.vstack([F[:, cols], R[:, cols]]); y = yv
    np.random.seed(7); idx = np.random.permutation(len(y)); folds = np.array_split(idx, 5)
    cvc = np.zeros(len(y)); cvs = np.zeros(len(y))
    for i in range(5):
        te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
        sg = np.sign(X[tr][y[tr] == 1].mean(0) - X[tr][y[tr] == 0].mean(0))
        m, s = X[tr].mean(0), X[tr].std(0) + 1e-9; Z = ((X[te] - m) / s) * sg
        cvc[te] = (Z > 0).sum(1); cvs[te] = Z.sum(1)
    return auc(cvc, y), auc(cvs, y)

print(f"famous={len(F)}  ordinary={len(R)}\n=== Prosperity yoga solo ===")
for idx, nm in [(7, "Prosperity STATIC"), (9, "Prosperity act 20-50 (prime)"), (8, "Prosperity act 50-80 (late)")]:
    fm, rm = F[:, idx].mean(), R[:, idx].mean()
    print(f"  {nm:30s} fam={fm:6.3f} ord={rm:6.3f} lift={fm-rm:+.3f}  AUC={auc(np.concatenate([F[:,idx],R[:,idx]]), yv):.3f}")

c7, s7 = cv([0, 1, 2, 3, 4, 5, 6])
print(f"\n=== composite ===\n  7-factor (baseline)             count-AUC={c7:.3f}  sum-AUC={s7:.3f}")
for idx, nm in [(7, "+ Prosperity STATIC"), (9, "+ Prosperity act 20-50"), (8, "+ Prosperity act 50-80")]:
    c8, s8 = cv([0, 1, 2, 3, 4, 5, 6, idx])
    print(f"  8-factor {nm:24s} count-AUC={c8:.3f}  sum-AUC={s8:.3f}")

print("\n=== matched-India cuts: 7-factor -> best 8-factor (+Prosperity act 50-80) ===")
for yr in (0, 1940, 1955):
    mask = (FY >= yr) & FI
    if mask.sum() < 20: continue
    Fm = F[mask]
    def cvm(cols):
        X = np.vstack([Fm[:, cols], R[:, cols]]); y = np.array([1] * len(Fm) + [0] * len(R), float)
        np.random.seed(7); idx = np.random.permutation(len(y)); folds = np.array_split(idx, 5); cvs = np.zeros(len(y))
        for i in range(5):
            te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
            sg = np.sign(X[tr][y[tr] == 1].mean(0) - X[tr][y[tr] == 0].mean(0))
            m, s = X[tr].mean(0), X[tr].std(0) + 1e-9; cvs[te] = (((X[te] - m) / s) * sg).sum(1)
        return auc(cvs, y)
    print(f"  India >= {yr:4d}  n={mask.sum():3d}   7f={cvm([0,1,2,3,4,5,6]):.3f}  ->  8f={cvm([0,1,2,3,4,5,6,8]):.3f}")
