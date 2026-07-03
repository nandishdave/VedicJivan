"""Does gating the 3/6/10/11-lord Mahadasha on a LAGNA link sharpen the famous tilt?
Peak window 20-50, year-weighted fractions. Famous(207) vs ordinary(96).

base   = frac peak years under a MD whose lord rules 3/6/10/11
rule1  = same, AND that MD lord connects to Lagna (1st) and/or Lagna lord
rule2a = base * (lagna-lord dignity /100)          [continuous interaction]
rule2b = base, counted only if Lagna lord is very strong (dignity>=75)
"""
import json
import numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS, _get_dignity
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha

FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8"))
ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55,
       "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}
UPA = {3, 6, 10, 11}

def feats(dob, tob, lat, lon):
    c = build_muhurta_chart(dob=dob, tob=tob, lat=lat, lon=lon)
    P, lag = c["planets"], c["lagna"]; ls = lag["sign"]
    asp = c["graha_drishti"]["planet_aspects"]
    def L(h): return SIGN_LORDS[(ls + h - 1) % 12]
    ll = L(1); ll_dig = _DP[_get_dignity(ll, P[ll]["sign"])]
    upa_lords = {L(h) for h in UPA}
    def connects_lagna(D):
        if D == ll: return True                                  # is the lagna lord
        if P[D]["house"] == P[ll]["house"]: return True          # conjunct lagna lord
        if P[ll]["house"] in asp.get(D, []) or P[D]["house"] in asp.get(ll, []): return True  # aspect
        if SIGN_LORDS[P[D]["sign"]] == ll and SIGN_LORDS[P[ll]["sign"]] == D: return True      # exchange
        if P[D]["house"] == 1 or 1 in asp.get(D, []): return True  # in/aspects 1st house
        return False
    by = int(dob[:4]); tot = base = r1 = 0.0
    for d in calc_vimshottari_dasha(P["Moon"]["longitude"], dob, tob)["dashas"]:
        ov = max(0, min(int(d["end_date"][:4]) - by, 50) - max(int(d["start_date"][:4]) - by, 20))
        if ov <= 0: continue
        tot += ov; D = d["planet"]
        if D in upa_lords:
            base += ov
            if connects_lagna(D): r1 += ov
    base = base / tot if tot else 0.0
    r1 = r1 / tot if tot else 0.0
    r2a = base * (ll_dig / 100.0)
    r2b = base if ll_dig >= 75 else 0.0
    return [base, r1, r2a, r2b, ll_dig]

def bd(p): return (p["birth"]["date"], p["birth"]["time"], p["birth"]["lat"], p["birth"]["lon"])
F = np.array([feats(*bd(p)) for p in FAM])
R = np.array([feats(*bd(p)) for p in ORDD])
def auc(pos, neg): return float(np.mean([np.mean(p > neg) + 0.5 * np.mean(p == neg) for p in pos]))

names = ["base  (3/6/10/11-lord MD)",
         "rule1 (+ Lagna/Lagna-lord connection)",
         "rule2a(+ Lagna-lord dignity, continuous)",
         "rule2b(+ Lagna lord very strong >=75)",
         "[Lagna-lord dignity alone]"]
print(f"famous={len(F)}  ordinary={len(R)}\n")
for i, n in enumerate(names):
    fm, rm = F[:, i].mean(), R[:, i].mean()
    print(f"  {n:42s} fam={fm:6.3f}  ord={rm:6.3f}  lift={fm-rm:+.3f}  AUC={auc(F[:, i], R[:, i]):.3f}")

# combined rule1+rule2a as a 2-feature CV composite (honest)
y = np.array([1] * len(F) + [0] * len(R), float)
X = np.vstack([F[:, [1, 2]], R[:, [1, 2]]])
np.random.seed(7); idx = np.random.permutation(len(y)); folds = np.array_split(idx, 5); cvs = np.zeros(len(y))
for i in range(5):
    te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
    sg = np.sign(X[tr][y[tr] == 1].mean(0) - X[tr][y[tr] == 0].mean(0))
    m, s = X[tr].mean(0), X[tr].std(0) + 1e-9; cvs[te] = (((X[te] - m) / s) * sg).sum(1)
print(f"\n  {'rule1 + rule2a  (2-feature CV composite)':42s}                      CV-AUC={auc(cvs[y==1], cvs[y==0]):.3f}")
