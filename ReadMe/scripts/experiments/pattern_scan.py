"""Pattern scan: which features are OVER-represented in famous charts vs random?
A pattern only matters if famous_rate >> random_rate."""
import json
import statistics as st
from collections import Counter

from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_NAMES
from app.services.kundli_calculator.divisional import calc_divisional_charts
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha
from app.services.kundli_calculator.yogas import calc_yogas

with open("/app/famous_charts_computed.json", encoding="utf-8") as fh:
    GOLD = [(x["name"], x["birth"]["date"], x["birth"]["time"], x["birth"]["lat"], x["birth"]["lon"])
            for x in json.load(fh)]

_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_BEN = {"Jupiter", "Venus", "Mercury"}
KT = {1, 4, 5, 7, 9, 10}


def feats(dob, tob, lat, lon):
    c = build_muhurta_chart(dob=dob, tob=tob, lat=lat, lon=lon)
    P, lag = c["planets"], c["lagna"]
    f = {}
    f["lagna_lord"] = lag.get("sign_lord")
    f["ak"] = max(_C, key=lambda p: P[p]["degree_in_sign"])
    f["n_exalted"] = sum(1 for p in _C if P[p]["dignity"] == "Exalted")
    f["n_own_exalt"] = sum(1 for p in _C if P[p]["dignity"] in ("Exalted", "Own Sign", "Moolatrikona"))
    f["ben_in_kt"] = sum(1 for p in _BEN if P[p]["house"] in KT)
    tl = SIGN_NAMES  # noqa
    tenth_lord = lag["sign_lord"]  # placeholder; recompute properly below
    # 10th lord = lord of the sign in the 10th house
    from app.services.kundli_calculator._core import SIGN_LORDS
    tenth_sign = (lag["sign"] + 9) % 12
    tenth_lord = SIGN_LORDS[tenth_sign]
    f["tenth_lord_in_kt"] = 1 if P.get(tenth_lord, {}).get("house") in KT else 0
    yg = calc_yogas(P, lag)
    f["n_raja"] = sum(1 for y in yg if y["type"] == "raj")
    f["n_maha"] = sum(1 for y in yg if y["type"] == "mahapurusha")
    f["n_dhan"] = sum(1 for y in yg if y["type"] == "dhan")
    # dasha lords ruling any of ages 25-45
    by = int(dob[:4])
    ds = calc_vimshottari_dasha(P["Moon"]["longitude"], dob, tob)["dashas"]
    rulers = set()
    for d in ds:
        a0, a1 = int(d["start_date"][:4]) - by, int(d["end_date"][:4]) - by
        if a1 > 25 and a0 < 45:
            rulers.add(d["planet"])
    f["dasha_2545"] = rulers
    # D10 10th house occupied?
    d10 = calc_divisional_charts(P, lag)["D10"]
    d10lag = d10["Lagna"]
    f["d10_10th_occ"] = 1 if any(((d10[p] - d10lag) % 12) + 1 == 10 for p in _C) else 0
    return f


def collect(rows):
    fs = [feats(*r) for r in rows]
    out = {}
    out["lagna_lord"] = Counter(f["lagna_lord"] for f in fs)
    out["ak"] = Counter(f["ak"] for f in fs)
    out["dasha_2545"] = Counter(p for f in fs for p in f["dasha_2545"])
    for k in ("n_exalted", "n_own_exalt", "ben_in_kt", "n_raja", "n_maha", "n_dhan"):
        out[k] = st.mean(f[k] for f in fs)
    for k in ("tenth_lord_in_kt", "d10_10th_occ"):
        out[k] = sum(f[k] for f in fs) / len(fs)
    return out, len(fs)


fam, nf = collect([(d, t, la, lo) for _, d, t, la, lo in GOLD])
CITIES = [(19.07, 72.87), (28.61, 77.20), (51.51, -0.13), (40.71, -74.0), (-33.45, -70.66), (35.68, 139.69)]
rnd_rows = []
for i in range(80):
    y = 1930 + (i * 7919 % 70); mo = 1 + (i * 13 % 12); d = 1 + (i * 17 % 28)
    la, lo = CITIES[i % len(CITIES)]
    rnd_rows.append((f"{y:04d}-{mo:02d}-{d:02d}", f"{(i*7)%24:02d}:{(i*11)%60:02d}", la, lo))
rnd, nr = collect(rnd_rows)

print(f"famous n={nf}  random n={nr}\n")
print("== numeric (famous vs random mean) ==")
for k in ("n_exalted", "n_own_exalt", "ben_in_kt", "n_raja", "n_maha", "n_dhan", "tenth_lord_in_kt", "d10_10th_occ"):
    print(f"  {k:16} fam={fam[k]:.2f}  rnd={rnd[k]:.2f}  lift={fam[k]-rnd[k]:+.2f}")
for cat in ("lagna_lord", "ak", "dasha_2545"):
    print(f"\n== {cat}: famous% vs random% (lift) ==")
    keys = set(fam[cat]) | set(rnd[cat])
    rows = []
    for k in keys:
        fp, rp = 100 * fam[cat].get(k, 0) / nf, 100 * rnd[cat].get(k, 0) / nr
        rows.append((fp - rp, k, fp, rp))
    for lift, k, fp, rp in sorted(rows, reverse=True):
        print(f"  {k:9} fam={fp:4.0f}%  rnd={rp:4.0f}%  lift={lift:+4.0f}")
