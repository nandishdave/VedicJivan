"""Test the user's hypothesis: interconnection (sambandha) of the 1/2/10/11 house
lords + Rahu/Ketu involvement. Univariate lift + cross-validated model.
Sambandha = conjunction | mutual/one-way graha-drishti | exchange (parivartana)."""
import json
import statistics as st
import numpy as np

from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS

with open("/app/famous_charts_computed.json", encoding="utf-8") as fh:
    BASE = [(x["birth"]["date"], x["birth"]["time"], x["birth"]["lat"], x["birth"]["lon"])
            for x in json.load(fh)]
NEW = [
    ("1947-10-26", "20:02", 41.85, -87.65), ("1946-08-19", "08:51", 33.67, -93.59),
    ("1946-07-06", "07:26", 41.31, -72.92), ("1911-02-06", "02:04", 41.63, -89.79),
    ("1975-06-04", "09:09", 34.05, -118.24), ("1943-12-08", "11:55", 28.08, -80.61),
    ("1967-02-20", "19:38", 46.98, -123.82), ("1875-07-26", "19:32", 47.60, 9.30),
    ("1856-05-06", "18:30", 49.64, 18.15), ("1809-02-12", "03:00", 52.71, -2.75),
    ("1942-11-27", "10:15", 47.61, -122.33),
]
FAMOUS = BASE + NEW


def sambandha(a, b, P, asp):
    if a == b:
        return True
    ha, hb = P[a]["house"], P[b]["house"]
    if ha == hb:
        return True  # conjunction
    if hb in asp.get(a, []) or ha in asp.get(b, []):
        return True  # (mutual/one-way) graha drishti
    if SIGN_LORDS[P[a]["sign"]] == b and SIGN_LORDS[P[b]["sign"]] == a:
        return True  # exchange
    return False


def feats(dob, tob, lat, lon):
    c = build_muhurta_chart(dob=dob, tob=tob, lat=lat, lon=lon)
    P, lag = c["planets"], c["lagna"]
    asp = c["graha_drishti"]["planet_aspects"]
    lords = list({SIGN_LORDS[(lag["sign"] + h - 1) % 12] for h in (1, 2, 10, 11)})
    # connected pairs among the unique key lords
    pairs = [(lords[i], lords[j]) for i in range(len(lords)) for j in range(i + 1, len(lords))]
    conn = sum(1 for a, b in pairs if sambandha(a, b, P, asp))
    conn_frac = conn / len(pairs) if pairs else 1.0
    # largest connected cluster (union-find style, tiny)
    parent = {p: p for p in lords}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for a, b in pairs:
        if sambandha(a, b, P, asp):
            parent[find(a)] = find(b)
    sizes = {}
    for p in lords:
        sizes[find(p)] = sizes.get(find(p), 0) + 1
    cluster = max(sizes.values())
    # Rahu/Ketu involvement with the key lords or houses 1/2/10/11
    rk = 0
    for node in ("Rahu", "Ketu"):
        hn = P[node]["house"]
        if hn in (1, 2, 10, 11):
            rk = 1
        for kl in lords:
            if sambandha(node, kl, P, asp):
                rk = 1
    key_strong = sum(1 for kl in lords if P[kl]["house"] in {1, 4, 5, 7, 9, 10})
    return [conn, conn_frac, cluster, rk, key_strong]


COLS = ["conn_pairs", "conn_frac", "cluster", "rk_involved", "key_strong"]
fam = [feats(*r) for r in FAMOUS]
CITIES = [(19.07, 72.87), (28.61, 77.20), (51.51, -0.13), (40.71, -74.0), (-33.45, -70.66), (35.68, 139.69)]
rnd = []
for i in range(120):
    yr = 1930 + (i * 7919 % 80); mo = 1 + (i * 13 % 12); d = 1 + (i * 17 % 28)
    la, lo = CITIES[i % len(CITIES)]
    rnd.append(feats(f"{yr:04d}-{mo:02d}-{d:02d}", f"{(i*7)%24:02d}:{(i*11)%60:02d}", la, lo))

F, R = np.array(fam, float), np.array(rnd, float)
print(f"famous n={len(F)}  random n={len(R)}\n== univariate (famous vs random mean) ==")
for j, c in enumerate(COLS):
    print(f"  {c:12} fam={F[:,j].mean():.2f}  rnd={R[:,j].mean():.2f}  lift={F[:,j].mean()-R[:,j].mean():+.2f}")

# cross-validated model on JUST these features
X = np.vstack([F, R]); y = np.array([1] * len(F) + [0] * len(R), float)


def fit(Xtr, ytr, l2=2.0, lr=0.2, it=3000):
    w = np.zeros(Xtr.shape[1]); b = 0.0
    for _ in range(it):
        p = 1 / (1 + np.exp(-(Xtr @ w + b)))
        w -= lr * (Xtr.T @ (p - ytr) / len(ytr) + l2 * w / len(ytr)); b -= lr * np.mean(p - ytr)
    return w, b


def auc(yt, p):
    a, b = p[yt == 1], p[yt == 0]
    return ((a[:, None] > b[None, :]).sum() + 0.5 * (a[:, None] == b[None, :]).sum()) / (len(a) * len(b))


np.random.seed(7)
idx = np.random.permutation(len(y)); folds = np.array_split(idx, 5); cvp = np.zeros(len(y))
for i in range(5):
    te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
    mu, sd = X[tr].mean(0), X[tr].std(0) + 1e-9
    w, b = fit((X[tr] - mu) / sd, y[tr]); cvp[te] = 1 / (1 + np.exp(-(((X[te] - mu) / sd) @ w + b)))
print(f"\n== model on your 5 features ==\nCV AUC = {auc(y, cvp):.3f}   (0.5=no pattern, >0.75=real)")
print(f"CV famous-prob = {cvp[y==1].mean():.2f}  vs random = {cvp[y==0].mean():.2f}")
