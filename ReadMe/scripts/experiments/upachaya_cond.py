"""(A) Upachaya-dasha score (peak 20-50) tested with honest AUC + 5-fold CV.
(B) Condition of the 3/6/10/11 house lords AND their dispositors:
    lord dignity (friendly/enemy sign), dispositor dignity, dispositor in
    dusthana (in trouble?), and conjunct friends vs enemies.
Famous(207) vs ordinary(96)."""
import json
import numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS, _get_dignity
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha
from app.services.kundli_calculator.friendship import _natural_relation

FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8"))
ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55,
       "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}
DUST = {6, 8, 12}; UPA_LORDS_H = [3, 6, 10, 11]

def feats(dob, tob, lat, lon):
    c = build_muhurta_chart(dob=dob, tob=tob, lat=lat, lon=lon)
    P, lag = c["planets"], c["lagna"]; ls = lag["sign"]
    def L(h): return SIGN_LORDS[(ls + h - 1) % 12]
    by = int(dob[:4])
    # --- (A) peak-dasha house fractions ---
    hf = np.zeros(12); tot = 0.0
    for d in calc_vimshottari_dasha(P["Moon"]["longitude"], dob, tob)["dashas"]:
        ov = max(0, min(int(d["end_date"][:4]) - by, 50) - max(int(d["start_date"][:4]) - by, 20))
        if ov <= 0: continue
        hf[P[d["planet"]]["house"] - 1] += ov; tot += ov
    if tot: hf /= tot
    # --- (B) condition of the 3/6/10/11 lords + dispositors ---
    lord_dig = []; disp_dig = []; disp_dusth = 0; conj_net = []
    for H in UPA_LORDS_H:
        lord = L(H)
        lord_dig.append(_DP[_get_dignity(lord, P[lord]["sign"])])
        disp = SIGN_LORDS[P[lord]["sign"]]
        disp_dig.append(_DP[_get_dignity(disp, P[disp]["sign"])])
        if P[disp]["house"] in DUST: disp_dusth += 1
        net = 0
        for q in _C:
            if q != lord and P[q]["house"] == P[lord]["house"]:
                r = _natural_relation(lord, q)
                net += 1 if r == "Friend" else -1 if r == "Enemy" else 0
        conj_net.append(net)
    return list(hf) + [np.mean(lord_dig), np.mean(disp_dig), float(disp_dusth), float(np.mean(conj_net))]

def bd(p): return (p["birth"]["date"], p["birth"]["time"], p["birth"]["lat"], p["birth"]["lon"])
F = np.array([feats(*bd(p)) for p in FAM])
R = np.array([feats(*bd(p)) for p in ORDD])
def auc(pos, neg): return float(np.mean([np.mean(p > neg) + 0.5 * np.mean(p == neg) for p in pos]))

# ---------- (A) Upachaya-dasha ----------
def col(h): return h - 1  # house -> index
def score(F, spec): return sum(w * F[:, col(h)] for h, w in spec)
print(f"famous={len(F)}  ordinary={len(R)}\n=== (A) Upachaya-dasha scores (peak 20-50) ===")
SPECS = [
    ("Pure Upachaya 3/6/10/11",           [(3, 1), (6, 1), (10, 1), (11, 1)]),
    ("Upachaya − 9th − 2nd (your spec)",  [(3, 1), (6, 1), (10, 1), (11, 1), (9, -1), (2, -1)]),
    ("Strive-only 3 + 11",                [(3, 1), (11, 1)]),
    ("3+11+1 − 9 − 2 (empirical, overfit-risk)", [(3, 1), (11, 1), (1, 1), (9, -1), (2, -1)]),
]
for name, spec in SPECS:
    Fs, Rs = score(F, spec), score(R, spec)
    print(f"  {name:44s} lift={Fs.mean()-Rs.mean():+.3f}  AUC={auc(Fs, Rs):.3f}")

# 5-fold CV upper bound over all 12 house fractions (fits sign + scaling)
X = np.vstack([F[:, :12], R[:, :12]]); y = np.array([1] * len(F) + [0] * len(R), float)
np.random.seed(7); idx = np.random.permutation(len(y)); folds = np.array_split(idx, 5); cvs = np.zeros(len(y))
for i in range(5):
    te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
    sg = np.sign(X[tr][y[tr] == 1].mean(0) - X[tr][y[tr] == 0].mean(0))
    m, s = X[tr].mean(0), X[tr].std(0) + 1e-9; cvs[te] = (((X[te] - m) / s) * sg).sum(1)
print(f"  {'CV z-composite over ALL 12 houses (upper bound)':44s}         CV-AUC={auc(cvs[y==1], cvs[y==0]):.3f}")

# ---------- (B) condition of upachaya lords + dispositors ----------
print("\n=== (B) Condition of 3/6/10/11 lords & their dispositors ===")
COMP = [(12, "Lord dignity (avg, /100)"), (13, "Dispositor dignity (avg, /100)"),
        (14, "Dispositors in dusthana (count 0-4)"), (15, "Conjunct friends−enemies (avg net)")]
for ci, label in COMP:
    fm, rm = F[:, ci].mean(), R[:, ci].mean()
    a = auc(F[:, ci], R[:, ci]) if "dusthana" not in label else auc(-F[:, ci], -R[:, ci])
    print(f"  {label:38s} famous={fm:6.2f}  ordinary={rm:6.2f}  diff={fm-rm:+6.2f}  AUC={a:.3f}")
# combined condition z-composite (dignity + disp dignity + fewer dusthana + conj)
Cix = [12, 13, 14, 15]; Xc = np.vstack([F[:, Cix], R[:, Cix]])
sg = np.sign(Xc[y == 1].mean(0) - Xc[y == 0].mean(0)); m, s = Xc.mean(0), Xc.std(0) + 1e-9
Zc = (((Xc - m) / s) * sg).sum(1)
print(f"  {'COMBINED condition score':38s} AUC={auc(Zc[y==1], Zc[y==0]):.3f}")
