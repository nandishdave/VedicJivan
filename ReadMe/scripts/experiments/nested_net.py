# -*- coding: utf-8 -*-
"""Acid test: does the auspicious/poison-degree factor earn Factor 18?

Two candidates appended to the validated 17-factor model:
  A = full NET  = (Pushkara Nav + Pushkara Bhaga) - (Vish Nav + Mrityu Bhaga)
  B = MALEFIC   = -(Vish Nav + Mrityu Bhaga)   [poison-degree count, screened stronger]

17 factors sourced from worldly_potential.factor_values (single source of truth).
For each candidate: 17 vs 18 composite (count + sum AUC), full + matched cuts + 5 seeds.
"""
import json
import numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha
from app.services.kundli_calculator.worldly_potential import factor_values

TBL = json.load(open("/app/navamsa_bhaga_tables.json", encoding="utf-8"))
PUSH_NAV = {int(k): set(v) for k, v in TBL["pushkara_navamsa"].items() if k.isdigit()}
VISH_NAV = {int(k): v for k, v in TBL["vish_navamsa"].items() if k.isdigit()}
PBHAGA = {int(k): v for k, v in TBL["pushkara_bhaga"]["degrees"].items()}
PBTOL = TBL["pushkara_bhaga"]["tolerance_deg"]
MRT = TBL["mrityu_bhaga"]["degrees"]
MRTOL = TBL["mrityu_bhaga"]["tolerance_deg"]

FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8"))
ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
FEAT = ["rahu_prime", "vimsopaka", "av_10th", "av_1st", "upa_occ", "raja_late", "dhana_late", "av_11th",
        "bright_moon", "moon_disp", "moon_sav", "sun_disp", "argala_pos", "purna_tithi", "dig_lords",
        "top_vim_seat", "nak_mridu_net"]
BODIES = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
NAV = 30.0 / 9.0


def degree_counts(chart):
    P, lag = chart["planets"], chart["lagna"]
    bodies = [(P[b]["sign"], P[b]["degree_in_sign"], b) for b in BODIES]
    bodies.append((lag["sign"], lag.get("degree", 0.0), "Lagna"))
    pkn = pkb = vsn = mrt = 0
    for s, d, key in bodies:
        nav = int(d / NAV) + 1
        if nav in PUSH_NAV[s]:
            pkn += 1
        if abs(d - PBHAGA[s]) <= PBTOL:
            pkb += 1
        if nav == VISH_NAV[s]:
            vsn += 1
        if abs(d - MRT[key][s]) <= MRTOL:
            mrt += 1
    net = (pkn + pkb) - (vsn + mrt)
    malefic = -(vsn + mrt)
    return net, malefic


def feats(dob, tob, lat, lon):
    c = build_muhurta_chart(dob=dob, tob=tob, lat=lat, lon=lon, with_shadbala=True)
    by = int(dob[:4])
    dl = calc_vimshottari_dasha(c["planets"]["Moon"]["longitude"], dob, tob)["dashas"]
    fv = factor_values(c, dl, by)
    net, malefic = degree_counts(c)
    india = (68 <= lon <= 98 and 6 <= lat <= 37)
    return [fv[k] for k in FEAT] + [net, malefic], by, india


def _bd(p):
    b = p["birth"]; return (b["date"], b["time"], b["lat"], b["lon"])


FR = [feats(*_bd(p)) for p in FAM]; RR = [feats(*_bd(p)) for p in ORDD]
F = np.array([x[0] for x in FR]); R = np.array([x[0] for x in RR])
FY = np.array([x[1] for x in FR]); FI = np.array([x[2] for x in FR])
I_NET, I_MAL = 17, 18


def auc(s, y):
    pos, neg = s[y == 1], s[y == 0]
    return float(np.mean([np.mean(p > neg) + 0.5 * np.mean(p == neg) for p in pos]))


def cv(Xf, Xr, seed=7):
    X = np.vstack([Xf, Xr]); y = np.array([1] * len(Xf) + [0] * len(Xr), float)
    np.random.seed(seed); idx = np.random.permutation(len(y)); folds = np.array_split(idx, 5)
    cvc = np.zeros(len(y)); cvs = np.zeros(len(y))
    for i in range(5):
        te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
        sg = np.sign(X[tr][y[tr] == 1].mean(0) - X[tr][y[tr] == 0].mean(0))
        m, s = X[tr].mean(0), X[tr].std(0) + 1e-9
        Z = ((X[te] - m) / s) * sg
        cvc[te] = (Z > 0).sum(1); cvs[te] = Z.sum(1)
    return auc(cvc, y), auc(cvs, y)


F17, R17 = F[:, :17], R[:, :17]
print(f"famous={len(F)} ordinary={len(R)}")
c17, s17 = cv(F17, R17)
print(f"\n17-factor baseline: count {c17:.3f}  sum {s17:.3f}")


def test(name, col):
    Fx = np.column_stack([F17, F[:, col]]); Rx = np.column_stack([R17, R[:, col]])
    c, s = cv(Fx, Rx)
    print(f"\n=== +{name} (factor 18) ===")
    print(f"  lift: fam {F[:, col].mean():+.2f} ord {R[:, col].mean():+.2f} diff {F[:, col].mean()-R[:, col].mean():+.2f}")
    print(f"  FULL: count {c17:.3f}->{c:.3f}  sum {s17:.3f}->{s:.3f}  (sum-delta {s-s17:+.3f})")
    for yr in (0, 1940, 1955):
        mask = (FY >= yr) & FI
        _, a = cv(F17[mask], R17); _, b = cv(Fx[mask], Rx)
        print(f"    India>={yr:4d} n={int(mask.sum()):3d}  {a:.3f} -> {b:.3f}  ({b-a:+.3f})")
    for lbl, mask in (("full", np.ones(len(F), bool)), (">=1940", (FY >= 1940) & FI)):
        ds = []
        for sd in (1, 7, 42, 123, 2024):
            _, a = cv(F17[mask], R17, sd); _, b = cv(Fx[mask], Rx, sd)
            ds.append(b - a)
        print(f"    seed-stability {lbl:7} {['%+.3f'%d for d in ds]} mean {np.mean(ds):+.3f}")


test("full NET (PkN+PkB-Vish-Mrityu)", I_NET)
test("MALEFIC only (-(Vish+Mrityu))", I_MAL)
print("\n(earns in only if the clean-cut delta is positive AND seed-stable)")
