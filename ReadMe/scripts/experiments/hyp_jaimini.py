"""Test the NEW techniques on AA charts vs random: Arudha Lagna, Jaimini
Karakamsa, Chara Dasha timing, D60 strength, Vargottama."""
import numpy as np
from app.services.kundli_calculator._core import (get_julian_day, calc_planet_positions,
                                                  SIGN_LORDS, _get_dignity)
from app.services.kundli_calculator.divisional import calc_divisional_charts
from app.services.kundli_calculator.jaimini import calc_jaimini_karakas
from app.services.kundli_calculator.jaimini_chara import calc_char_dasha

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
_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55,
       "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}
KEN = {1, 4, 7, 10}


def feats(dob, tob, lat, lon):
    jd = get_julian_day(dob, tob, lat, lon)
    pos = calc_planet_positions(jd, lat, lon)
    P, lag = pos["planets"], pos["lagna"]
    div = calc_divisional_charts(P, lag)
    d9, d60 = div["D9"], div["D60"]
    jai = calc_jaimini_karakas(P, lag)
    ls = lag["sign"]
    # Arudha Lagna (Pada) with the 1st/7th exception -> 10th from pada
    ll_sign = P[SIGN_LORDS[ls]]["sign"]
    al = (2 * ll_sign - ls) % 12
    if al == ls or al == (ls + 6) % 12:
        al = (al + 9) % 12
    al_prom = sum(1 for p in _C if P[p]["sign"] == al) + sum(1 for p in _C if P[p]["sign"] == (al + 9) % 12)
    # Karakamsa: planets in kendras from AK's D9 sign
    kk = jai["karakamsa_sign"]
    kk_kendra = sum(1 for p in _C if ((d9[p] - kk) % 12) + 1 in KEN)
    # Chara dasha: max planets in an active sign-dasha during ages 25-45
    by = int(dob[:4]); chara = 0
    for d in calc_char_dasha(P, lag, dob, tob)["dashas"]:
        a0, a1 = int(d["start_date"][:4]) - by, int(d["end_date"][:4]) - by
        if a1 > 20 and a0 < 50:
            chara = max(chara, sum(1 for p in _C if P[p]["sign"] == d["sign"]))
    # D60 strength (avg dignity in Shashtiamsa)
    d60_str = np.mean([_DP.get(_get_dignity(p, d60[p]), 45) for p in _C])
    # Vargottama count (same sign D1 & D9)
    vg = sum(1 for p in _C if P[p]["sign"] == d9[p])
    return [al_prom, kk_kendra, chara, d60_str, vg]


COLS = ["arudha_prom", "karakamsa_ken", "chara_2545", "d60_str", "vargottama"]
F = np.array([feats(*r) for r in AA], float)
CITIES = [(19.07, 72.87), (28.61, 77.20), (51.51, -0.13), (40.71, -74.0), (-33.45, -70.66), (35.68, 139.69)]
R = np.array([feats(f"{1930+(i*7919%80):04d}-{1+(i*13%12):02d}-{1+(i*17%28):02d}",
                    f"{(i*7)%24:02d}:{(i*11)%60:02d}", *CITIES[i % 6]) for i in range(150)], float)

print(f"AA famous={len(F)}  random={len(R)}\n{'feature':14} {'FAM':>7} {'RND':>7} {'lift':>7}")
for j, c in enumerate(COLS):
    print(f"{c:14} {F[:,j].mean():7.2f} {R[:,j].mean():7.2f} {F[:,j].mean()-R[:,j].mean():+7.2f}")

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
print(f"\nCV AUC (these 5 new features) = {auc(y, cvp):.3f}   (0.5=nothing, >0.65=real)")
print(f"CV famous-prob={cvp[y==1].mean():.2f} vs random={cvp[y==0].mean():.2f}")
