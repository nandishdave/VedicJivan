"""Multivariate test: can a COMBINATION of all features separate famous from
random? Honest 5-fold cross-validation (the model is tested on charts it never
trained on). CV-AUC ~0.5 = no real pattern; >0.75 = a real, usable combination.
Train-AUC >> CV-AUC = overfitting (memorising, not learning)."""
import json
import numpy as np

from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS
from app.services.kundli_calculator.chart_strength import unshakable_score
from app.services.kundli_calculator.divisional import calc_divisional_charts
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha
from app.services.kundli_calculator.yogas import calc_yogas
from app.services.kundli_calculator._core import _get_dignity

with open("/app/famous_charts_computed.json", encoding="utf-8") as fh:
    GOLD = [(x["birth"]["date"], x["birth"]["time"], x["birth"]["lat"], x["birth"]["lon"])
            for x in json.load(fh)]

_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_ALL = _C + ["Rahu", "Ketu"]
_BEN = {"Jupiter", "Venus", "Mercury"}
KT = {1, 4, 5, 7, 9, 10}
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55,
       "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}


def featvec(dob, tob, lat, lon):
    c = build_muhurta_chart(dob=dob, tob=tob, lat=lat, lon=lon)
    P, lag = c["planets"], c["lagna"]
    L = unshakable_score(c)["layers"]
    f = [L["structural"], L["yoga"], L["longevity"], L["fame"]]
    f += [sum(1 for p in _C if P[p]["dignity"] == "Exalted"),
          sum(1 for p in _C if P[p]["dignity"] in ("Exalted", "Own Sign", "Moolatrikona")),
          sum(1 for p in _BEN if P[p]["house"] in KT),
          sum(1 for y in calc_yogas(P, lag) if y["type"] == "raj"),
          sum(1 for y in calc_yogas(P, lag) if y["type"] == "mahapurusha")]
    tenth_lord = SIGN_LORDS[(lag["sign"] + 9) % 12]
    f.append(1 if P.get(tenth_lord, {}).get("house") in KT else 0)
    # D10 strength
    d10 = calc_divisional_charts(P, lag)["D10"]
    dl = d10["Lagna"]
    f.append(np.mean([_DP.get(_get_dignity(p, d10[p]), 45) for p in _C]))
    # dasha rulers at 25-45 (binary per planet)
    by = int(dob[:4])
    rulers = set()
    for d in calc_vimshottari_dasha(P["Moon"]["longitude"], dob, tob)["dashas"]:
        a0, a1 = int(d["start_date"][:4]) - by, int(d["end_date"][:4]) - by
        if a1 > 25 and a0 < 45:
            rulers.add(d["planet"])
    f += [1 if p in rulers else 0 for p in _ALL]
    # AK one-hot + lagna-lord one-hot
    ak = max(_C, key=lambda p: P[p]["degree_in_sign"])
    f += [1 if ak == p else 0 for p in _C]
    f += [1 if lag.get("sign_lord") == p else 0 for p in _C]
    return f


X = [featvec(*r) for r in GOLD]
y = [1] * len(GOLD)
CITIES = [(19.07, 72.87), (28.61, 77.20), (51.51, -0.13), (40.71, -74.0), (-33.45, -70.66), (35.68, 139.69)]
for i in range(90):
    yr = 1930 + (i * 7919 % 70); mo = 1 + (i * 13 % 12); d = 1 + (i * 17 % 28)
    la, lo = CITIES[i % len(CITIES)]
    X.append(featvec(f"{yr:04d}-{mo:02d}-{d:02d}", f"{(i*7)%24:02d}:{(i*11)%60:02d}", la, lo))
    y.append(0)

X = np.array(X, float); y = np.array(y, float)


def fit(Xtr, ytr, l2=2.0, lr=0.2, it=3000):
    w = np.zeros(Xtr.shape[1]); b = 0.0
    for _ in range(it):
        p = 1 / (1 + np.exp(-(Xtr @ w + b)))
        w -= lr * (Xtr.T @ (p - ytr) / len(ytr) + l2 * w / len(ytr))
        b -= lr * np.mean(p - ytr)
    return w, b


def auc(yt, p):
    pos, neg = p[yt == 1], p[yt == 0]
    return ((pos[:, None] > neg[None, :]).sum() + 0.5 * (pos[:, None] == neg[None, :]).sum()) / (len(pos) * len(neg))


np.random.seed(7)
idx = np.random.permutation(len(y))
folds = np.array_split(idx, 5)
cv_pred = np.zeros(len(y))
for i in range(5):
    te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
    mu, sd = X[tr].mean(0), X[tr].std(0) + 1e-9
    w, b = fit((X[tr] - mu) / sd, y[tr])
    cv_pred[te] = 1 / (1 + np.exp(-(((X[te] - mu) / sd) @ w + b)))

mu, sd = X.mean(0), X.std(0) + 1e-9
w, b = fit((X - mu) / sd, y)
train_pred = 1 / (1 + np.exp(-(((X - mu) / sd) @ w + b)))

print(f"features={X.shape[1]}  famous={int(y.sum())}  random={int((1-y).sum())}")
print(f"TRAIN AUC = {auc(y, train_pred):.3f}   (in-sample; high is expected)")
print(f"CV    AUC = {auc(y, cv_pred):.3f}   <-- the honest number (0.5=no pattern, >0.75=real)")
print(f"\nCV famous-prob mean = {cv_pred[y==1].mean():.2f}  vs random = {cv_pred[y==0].mean():.2f}")
