# -*- coding: utf-8 -*-
"""Does 2nd-house Ashtakavarga (av_2nd) earn a place as factor 18?

Mirrors fame_composite.py EXACTLY (same 17 factors, same 5-fold CV, same matched
cuts), then appends av_2nd = SAV bindus on the 2nd house (dhana) as an 18th
candidate. Reports:
  - per-factor lift of av_2nd (famous mean | ordinary mean | diff)
  - solo AUC of av_2nd alone
  - 17-factor vs 18-factor composite (count + sum AUC), full set
  - the same on the confound-matched India-born cuts (>=0/1940/1955)
  - multi-seed stability of the sum-AUC delta on the full set and the clean >=1940 cut

Discipline: av_2nd only 'earns in' if it LIFTS the composite on the confound-free
cuts, seed-stably. Otherwise it's logged rejected (verified, not assumed).
"""
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
_BAD = {3, 6, 8, 12}
OCC = {3, 6, 10, 11}
_VARGA_W = {"D1": 3.5, "D2": 1.0, "D3": 1.0, "D4": 0.5, "D7": 0.5, "D9": 3.0, "D10": 0.5,
            "D12": 0.5, "D16": 2.0, "D20": 0.5, "D24": 0.5, "D27": 0.5, "D30": 1.0,
            "D40": 0.5, "D45": 0.5, "D60": 4.0}
FEAT17 = ["rahu_prime", "vimsopaka", "av_10th", "av_1st", "upa_occ", "raja_late", "dhana_late", "av_11th",
          "bright_moon", "moon_disp", "moon_sav", "sun_disp", "argala_pos", "purna_tithi", "dig_lords",
          "top_vim_seat", "nak_mridu_net"]
_MRIDU_NAK = {4, 13, 16, 26}
_TIKSHNA_NAK = {5, 8, 17, 18}
_ARG_PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
_ARG_PAIRS = ((2, 12), (4, 10), (5, 9), (11, 3))
_ARG_HOUSES = (2, 10, 12)


def _positive_argala(P, shadbala, bright_moon):
    if not shadbala:
        return 0.0
    benefic = {"Jupiter": 1, "Venus": 1, "Mercury": 1, "Moon": (1 if bright_moon else -1),
               "Sun": -1, "Mars": -1, "Saturn": -1, "Rahu": -1, "Ketu": -1}
    svals = [shadbala[q]["total_shadbala"] for q in _C if q in shadbala]
    avg = sum(svals) / len(svals) if svals else 1.0
    wt = {q: (shadbala[q]["total_shadbala"] if q in shadbala else avg) for q in _ARG_PLANETS}
    by_house = {h: [] for h in range(1, 13)}
    for p in _ARG_PLANETS:
        by_house[P[p]["house"]].append(p)
    total = 0.0
    for R in _ARG_HOUSES:
        for na, nv in _ARG_PAIRS:
            A = ((R - 1 + na - 1) % 12) + 1
            V = ((R - 1 + nv - 1) % 12) + 1
            if sum(wt[p] for p in by_house[A]) > sum(wt[p] for p in by_house[V]):
                s = sum(wt[p] * benefic[p] for p in by_house[A])
                if s > 0:
                    total += s
    return total


def _yoga_weights(links):
    w = {}
    for lk in links:
        for p in lk.get("planets", []):
            w[p] = w.get(p, 0.0) + lk["score"]
    return w


def _activation(dashas, birth_year, weights, a, b):
    tot = acc = 0.0
    for d in dashas:
        ov = max(0, min(int(d["end_date"][:4]) - birth_year, b) - max(int(d["start_date"][:4]) - birth_year, a))
        if ov <= 0:
            continue
        tot += ov
        acc += weights.get(d["planet"], 0.0) * ov
    return acc / tot if tot else 0.0


def feats(dob, tob, lat, lon):
    c = build_muhurta_chart(dob=dob, tob=tob, lat=lat, lon=lon, with_shadbala=True)
    P, lag = c["planets"], c["lagna"]
    ls = lag["sign"]
    by = int(dob[:4])
    dl = calc_vimshottari_dasha(P["Moon"]["longitude"], dob, tob)["dashas"]

    ra = next(((int(d["start_date"][:4]) - by, int(d["end_date"][:4]) - by) for d in dl if d["planet"] == "Rahu"), None)
    rahu_years = max(0, min(ra[1], 50) - max(ra[0], 20)) if ra else 0
    dispf = 1.0 if P[SIGN_LORDS[P["Rahu"]["sign"]]]["house"] not in _BAD else 0.4
    rahu_prime = rahu_years * dispf

    varga = calc_divisional_charts(P, lag)
    vim_pp = {}
    for p in _C:
        tot_p = 0.0
        for vname, vw in _VARGA_W.items():
            vsign = P[p]["sign"] if vname == "D1" else varga[vname][p]
            tot_p += vw * (_DP.get(_get_dignity(p, vsign), 45) / 100.0)
        vim_pp[p] = tot_p
    vimsopaka = sum(vim_pp.values()) / len(_C)

    tv = c["ashtakavarga"]["totals"]
    av_10th = tv[(ls + 9) % 12]
    av_1st = tv[ls]
    av_11th = tv[(ls + 10) % 12]
    av_2nd = tv[(ls + 1) % 12]        # <-- candidate factor 18: 2nd house (dhana)

    tot = occ = 0.0
    for d in dl:
        ov = max(0, min(int(d["end_date"][:4]) - by, 50) - max(int(d["start_date"][:4]) - by, 20))
        if ov <= 0:
            continue
        tot += ov
        if P[d["planet"]]["house"] in OCC:
            occ += ov
    upa_occ = occ / tot if tot else 0.0

    raja_late = _activation(dl, by, _yoga_weights(raja_yoga_score(c)[1]), 50, 80)
    dhana_late = _activation(dl, by, _yoga_weights(dhana_yoga_score(c)[1]), 50, 80)

    ms = P["Moon"]["sign"]
    elong = (P["Moon"]["longitude"] - P["Sun"]["longitude"]) % 360
    bright_moon = 1.0 if 72 <= elong <= 264 else 0.0
    moon_disp = 1.0 if P[SIGN_LORDS[ms]]["house"] in (1, 2, 11, 12) else 0.0
    moon_sav = tv[ms]
    sun_disp = 1.0 if P[SIGN_LORDS[P["Sun"]["sign"]]]["house"] in (1, 2, 3, 4) else 0.0

    argala_pos = _positive_argala(P, c.get("shadbala", {}), bright_moon)

    tithi = int(((P["Moon"]["longitude"] - P["Sun"]["longitude"]) % 360) / 12) + 1
    purna_tithi = 1.0 if (tithi - 1) % 5 == 4 else 0.0

    sb = c.get("shadbala", {})
    lords = (SIGN_LORDS[ls], SIGN_LORDS[(ls + 9) % 12])
    dvals = [sb[q]["dig_bala"] for q in lords if q in sb and "dig_bala" in sb[q]]
    dig_lords = float(np.mean(dvals)) if dvals else 30.0

    top_graha = max(_C, key=lambda q: vim_pp[q])
    top_vim_seat = 1.0 if P[top_graha]["house"] in (1, 2, 4, 5, 11) else 0.0

    nak_mridu_net = 0.0
    for q in _ARG_PLANETS:
        ni = int((P[q]["longitude"] % 360) / (360.0 / 27.0))
        if ni in _MRIDU_NAK:
            nak_mridu_net += 1.0
        elif ni in _TIKSHNA_NAK:
            nak_mridu_net -= 1.0

    india = (68 <= lon <= 98 and 6 <= lat <= 37)
    # 17 model factors first, av_2nd appended as index 17 (the 18th).
    return [rahu_prime, vimsopaka, av_10th, av_1st, upa_occ, raja_late, dhana_late, av_11th,
            bright_moon, moon_disp, moon_sav, sun_disp, argala_pos, purna_tithi, dig_lords,
            top_vim_seat, nak_mridu_net, av_2nd], by, india


def _bd(p):
    return (p["birth"]["date"], p["birth"]["time"], p["birth"]["lat"], p["birth"]["lon"])


FR = [feats(*_bd(p)) for p in FAM]
RR = [feats(*_bd(p)) for p in ORDD]
F = np.array([x[0] for x in FR])
R = np.array([x[0] for x in RR])
FY = np.array([x[1] for x in FR])
FI = np.array([x[2] for x in FR])


def auc(scores, labels):
    pos = scores[labels == 1]
    neg = scores[labels == 0]
    return float(np.mean([np.mean(p > neg) + 0.5 * np.mean(p == neg) for p in pos]))


def cv(Xf, Xr, seed=7):
    X = np.vstack([Xf, Xr])
    y = np.array([1] * len(Xf) + [0] * len(Xr), float)
    np.random.seed(seed)
    idx = np.random.permutation(len(y))
    folds = np.array_split(idx, 5)
    cvc = np.zeros(len(y)); cvs = np.zeros(len(y))
    for i in range(5):
        te = folds[i]
        tr = np.concatenate([folds[j] for j in range(5) if j != i])
        sg = np.sign(X[tr][y[tr] == 1].mean(0) - X[tr][y[tr] == 0].mean(0))
        m, s = X[tr].mean(0), X[tr].std(0) + 1e-9
        Z = ((X[te] - m) / s) * sg
        cvc[te] = (Z > 0).sum(1); cvs[te] = Z.sum(1)
    return auc(cvc, y), auc(cvs, y)


I2 = 17   # index of av_2nd
print(f"famous={len(F)}  ordinary={len(R)}")
print(f"\nav_2nd per-factor lift:  famous={F[:, I2].mean():.2f}  ordinary={R[:, I2].mean():.2f}  "
      f"diff={F[:, I2].mean() - R[:, I2].mean():+.2f}")
print(f"(compare av_11th={F[:, 7].mean() - R[:, 7].mean():+.2f}, av_10th={F[:, 2].mean() - R[:, 2].mean():+.2f}, "
      f"av_1st={F[:, 3].mean() - R[:, 3].mean():+.2f})")

# solo AUC of av_2nd (orient famous-positive)
sg2 = np.sign(F[:, I2].mean() - R[:, I2].mean())
solo = auc(np.concatenate([F[:, I2], R[:, I2]]) * sg2, np.array([1]*len(F) + [0]*len(R), float))
print(f"av_2nd solo AUC = {solo:.3f}")

F17, F18 = F[:, :17], F
R17, R18 = R[:, :17], R
c17, s17 = cv(F17, R17); c18, s18 = cv(F18, R18)
print(f"\nFULL SET:")
print(f"  17-factor   count={c17:.3f}  sum={s17:.3f}")
print(f"  +av_2nd(18) count={c18:.3f}  sum={s18:.3f}   sum-delta={s18 - s17:+.3f}")

print("\nconfound-matched India-born cuts (sum-AUC, 17 -> +av_2nd):")
for yr in (0, 1940, 1955):
    mask = (FY >= yr) & FI
    if mask.sum() < 20:
        continue
    _, s17m = cv(F17[mask], R17); _, s18m = cv(F18[mask], R18)
    print(f"  India >= {yr:4d}  n_fam={int(mask.sum()):3d}  {s17m:.3f} -> {s18m:.3f}   delta={s18m - s17m:+.3f}")

print("\nseed stability of sum-AUC delta (want consistently >0 to earn in):")
for label, (Ff, Rf17, Rf18) in {
    "full":       (np.ones(len(F), bool), R17, R18),
    ">=1940 cut": ((FY >= 1940) & FI, R17, R18),
}.items():
    ds = []
    for sd in (1, 7, 42, 123, 2024):
        _, a = cv(F17[Ff], Rf17, sd); _, b = cv(F18[Ff], Rf18, sd)
        ds.append(b - a)
    print(f"  {label:11} deltas={['%+.3f' % d for d in ds]}  mean={np.mean(ds):+.3f}")
