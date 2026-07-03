"""Final fair test: 5 curated classical features on AA-ONLY famous charts,
cross-validated. Low feature count -> low overfit risk -> the CV-AUC is trustworthy."""
import numpy as np

from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha

# AA-rated only (birth-certificate / official record)
AA = [
    ("1961-08-04", "19:24", 21.3069, -157.8583), ("1946-06-14", "10:54", 40.7020, -73.8060),
    ("1917-05-29", "15:00", 42.3318, -71.1212), ("1947-10-26", "20:02", 41.85, -87.65),
    ("1946-08-19", "08:51", 33.67, -93.59), ("1946-07-06", "07:26", 41.31, -72.92),
    ("1911-02-06", "02:04", 41.63, -89.79), ("1889-04-20", "18:30", 48.2585, 13.0333),
    ("1874-11-30", "01:30", 51.8517, -1.3520), ("1926-04-21", "02:40", 51.5074, -0.1278),
    ("1948-11-14", "21:14", 51.5074, -0.1278), ("1961-07-01", "19:45", 52.8312, 0.5152),
    ("1982-06-21", "21:03", 51.5074, -0.1278), ("1984-09-15", "16:20", 51.5074, -0.1278),
    ("1926-06-01", "09:30", 34.0522, -118.2437), ("1935-01-08", "04:35", 34.2576, -88.7034),
    ("1958-08-29", "23:53", 41.5934, -87.3464), ("1958-08-16", "07:05", 43.5945, -83.8889),
    ("1954-01-29", "04:30", 33.0576, -89.5887), ("1989-12-13", "05:17", 40.3356, -75.9269),
    ("1975-06-04", "09:09", 34.05, -118.24), ("1943-12-08", "11:55", 28.08, -80.61),
    ("1967-02-20", "19:38", 46.98, -123.82), ("1879-03-14", "11:30", 48.3984, 9.9916),
    ("1875-07-26", "19:32", 47.60, 9.30), ("1856-05-06", "18:30", 49.64, 18.15),
    ("1809-02-12", "03:00", 52.71, -2.75), ("1856-07-10", "00:00", 44.5811, 15.3144),
    ("1942-01-17", "18:35", 38.2527, -85.7585), ("1940-10-09", "18:30", 53.4084, -2.9916),
    ("1942-06-18", "14:00", 53.4084, -2.9916), ("1942-11-27", "10:15", 47.61, -122.33),
]
_BEN = {"Jupiter", "Venus", "Mercury"}
KT = {1, 4, 5, 7, 9, 10}
TRINE_HOUSES = [1, 2, 3, 5, 6, 7, 9, 10, 11]


def samb(a, b, P, asp):
    if a == b:
        return True
    if P[a]["house"] == P[b]["house"]:
        return True
    if P[b]["house"] in asp.get(a, []) or P[a]["house"] in asp.get(b, []):
        return True
    return SIGN_LORDS[P[a]["sign"]] == b and SIGN_LORDS[P[b]["sign"]] == a


def five(dob, tob, lat, lon):
    c = build_muhurta_chart(dob=dob, tob=tob, lat=lat, lon=lon)
    P, lag, sb = c["planets"], c["lagna"], c["shadbala"]
    asp = c["graha_drishti"]["planet_aspects"]
    ls = lag["sign"]
    def L(h): return SIGN_LORDS[(ls + h - 1) % 12]
    # 1) dasha timing (strength-weighted lords over ages 18-50)
    by = int(dob[:4]); acc = tot = 0.0
    for d in calc_vimshottari_dasha(P["Moon"]["longitude"], dob, tob)["dashas"]:
        ov = max(0, min(int(d["end_date"][:4]) - by, 50) - max(int(d["start_date"][:4]) - by, 18))
        if ov <= 0:
            continue
        p = d["planet"]; s = min(sb.get(p, {}).get("ratio", 1.0) / 1.5, 1.0) * 100
        if p in _BEN or p == L(1):
            s = min(s * 1.15, 100)
        acc += s * ov; tot += ov
    f_dasha = acc / tot if tot else 50
    # 2) 2-11 wealth axis (graded count)
    l2, l11 = L(2), L(11)
    f_wealth = sum([
        l2 != l11 and SIGN_LORDS[P[l2]["sign"]] == l11 and SIGN_LORDS[P[l11]["sign"]] == l2,
        l2 != l11 and P[l2]["house"] == P[l11]["house"],
        P[l2]["house"] == 11, P[l11]["house"] == 2,
        P[l2]["house"] == P["Rahu"]["house"] or P[l11]["house"] == P["Rahu"]["house"],
    ])
    # 3) trikona-lord cluster size
    tri = list({L(1), L(5), L(9)})
    par = {p: p for p in tri}
    def fnd(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    for i in range(len(tri)):
        for j in range(i + 1, len(tri)):
            if samb(tri[i], tri[j], P, asp):
                par[fnd(tri[i])] = fnd(tri[j])
    sz = {}
    for p in tri:
        sz[fnd(p)] = sz.get(fnd(p), 0) + 1
    f_trikona = max(sz.values())
    # 4) Ashtakavarga: max SAV among trine houses
    tot_av = c["ashtakavarga"]["totals"]
    f_av = max(tot_av[(ls + h - 1) % 12] for h in TRINE_HOUSES)
    # 5) Rahu/Ketu on wealth axis
    keylords = {L(1), L(5), L(9), l2, l11}
    f_rk = 0
    for node in ("Rahu", "Ketu"):
        if P[node]["house"] in (2, 11) and any(samb(node, k, P, asp) for k in keylords):
            f_rk = 1
    return [f_dasha, f_wealth, f_trikona, f_av, f_rk]


COLS = ["dasha", "wealth_2_11", "trikona", "av_maxSAV", "rahu_2_11"]
F = np.array([five(*r) for r in AA], float)
CITIES = [(19.07, 72.87), (28.61, 77.20), (51.51, -0.13), (40.71, -74.0), (-33.45, -70.66), (35.68, 139.69)]
R = np.array([five(f"{1930+(i*7919%80):04d}-{1+(i*13%12):02d}-{1+(i*17%28):02d}",
                   f"{(i*7)%24:02d}:{(i*11)%60:02d}", *CITIES[i % 6]) for i in range(150)], float)

print(f"AA famous={len(F)}  random={len(R)}\n{'feature':12} {'FAM':>7} {'RND':>7} {'lift':>7}")
for j, c in enumerate(COLS):
    print(f"{c:12} {F[:,j].mean():7.2f} {R[:,j].mean():7.2f} {F[:,j].mean()-R[:,j].mean():+7.2f}")

X = np.vstack([F, R]); y = np.array([1] * len(F) + [0] * len(R), float)


def fit(Xt, yt, l2=1.0, lr=0.2, it=3000):
    w = np.zeros(Xt.shape[1]); b = 0.0
    for _ in range(it):
        p = 1 / (1 + np.exp(-(Xt @ w + b)))
        w -= lr * (Xt.T @ (p - yt) / len(yt) + l2 * w / len(yt)); b -= lr * np.mean(p - yt)
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
mu, sd = X.mean(0), X.std(0) + 1e-9
w, b = fit((X - mu) / sd, y); trp = 1 / (1 + np.exp(-(((X - mu) / sd) @ w + b)))
print(f"\nTRAIN AUC = {auc(y, trp):.3f}")
print(f"CV    AUC = {auc(y, cvp):.3f}   <-- honest verdict (0.5=nothing, >0.65=real)")
print(f"CV famous-prob={cvp[y==1].mean():.2f} vs random={cvp[y==0].mean():.2f}")
