# -*- coding: utf-8 -*-
"""Candidate D - HOUSE/BHAVA STRENGTH via total Shadbala of the key-house lords (1st,
10th, 11th) + occupant-strength proxies. Distinct from av1/av10/av11 (positional bindus)
and from C (only the digbala slice of 1st/10th lords). Adds the 11th (gains/fame).
Metrics:
  sb_1lord/sb_10lord/sb_11lord = total_shadbala of the 1st/10th/11th lords
  sb_keylords = mean of the three
  occ10/occ11 = mean total_shadbala of planets occupying the 10th/11th (bhava proxy)
Tested as factor-15 on base-14, AND (crucially) whether it adds BEYOND C's dig_lords.
Nested/cuts/seed. (225 vs 96)"""
import json, numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS, _get_dignity
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha
from app.services.kundli_calculator.raja_yoga import raja_yoga_score
from app.services.kundli_calculator.dhana_yoga import dhana_yoga_score
FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8")); ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]; _ALL = _C + ["Rahu", "Ketu"]
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55, "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}
_BAD = {3, 6, 8, 12}; _OCC = {3, 6, 10, 11}; _ARG_PAIRS = ((2, 12), (4, 10), (5, 9), (11, 3)); _ARG_HOUSES = (2, 10, 12)
MKEYS = ["sb_1lord", "sb_10lord", "sb_11lord", "sb_keylords", "occ10", "occ11"]
def hh(R, n): return ((R - 1 + n - 1) % 12) + 1
def _pw(l):
    w = {}
    for lk in l:
        for p in lk.get("planets", []): w[p] = w.get(p, 0.0) + lk["score"]
    return w
def _act(dl, by, wd, a, b):
    t = acc = 0.0
    for d in dl:
        ov = max(0, min(int(d["end_date"][:4]) - by, b) - max(int(d["start_date"][:4]) - by, a))
        if ov > 0: t += ov; acc += wd.get(d["planet"], 0.0) * ov
    return acc / t if t else 0.0
def feats(p):
    b = p["birth"]; c = build_muhurta_chart(dob=b["date"], tob=b["time"], lat=b["lat"], lon=b["lon"], with_shadbala=True)
    P, lag = c["planets"], c["lagna"]; ls = lag["sign"]; by = int(b["date"][:4]); dv = c["divisional"]
    dl = calc_vimshottari_dasha(P["Moon"]["longitude"], b["date"], b["time"])["dashas"]
    ra = next(((int(d["start_date"][:4]) - by, int(d["end_date"][:4]) - by) for d in dl if d["planet"] == "Rahu"), None)
    rahu = (max(0, min(ra[1], 50) - max(ra[0], 20)) if ra else 0) * (1.0 if P[SIGN_LORDS[P["Rahu"]["sign"]]]["house"] not in _BAD else 0.4)
    d60c = float(np.mean([_DP.get(_get_dignity(x, dv["D60"][x]), 45) for x in _C]))
    tv = c["ashtakavarga"]["totals"]; av10, av1, av11 = tv[(ls + 9) % 12], tv[ls], tv[(ls + 10) % 12]
    tot = occ = 0.0
    for d in dl:
        ovp = max(0, min(int(d["end_date"][:4]) - by, 50) - max(int(d["start_date"][:4]) - by, 20))
        if ovp > 0:
            tot += ovp
            if P[d["planet"]]["house"] in _OCC: occ += ovp
    upa = occ / tot if tot else 0.0
    rl = _act(dl, by, _pw(raja_yoga_score(c)[1]), 50, 80); dhl = _act(dl, by, _pw(dhana_yoga_score(c)[1]), 50, 80)
    ms = P["Moon"]["sign"]; sl, ml = P["Sun"]["longitude"], P["Moon"]["longitude"]; elong = (ml - sl) % 360
    bright = 1.0 if 72 <= elong <= 264 else 0.0
    moon_disp = 1.0 if P[SIGN_LORDS[ms]]["house"] in (1, 2, 11, 12) else 0.0
    moon_sav = tv[ms]; sun_disp = 1.0 if P[SIGN_LORDS[P["Sun"]["sign"]]]["house"] in (1, 2, 3, 4) else 0.0
    benefic = {"Jupiter": 1, "Venus": 1, "Mercury": 1, "Moon": (1 if bright else -1), "Sun": -1, "Mars": -1, "Saturn": -1, "Rahu": -1, "Ketu": -1}
    sb = c["shadbala"]; svals = [sb[q]["total_shadbala"] for q in _C if q in sb]; avg = float(np.mean(svals)) if svals else 1.0
    wt = {q: (sb[q]["total_shadbala"] if q in sb else avg) for q in _ALL}
    bhh = {h: [] for h in range(1, 13)}
    for pl in _ALL: bhh[P[pl]["house"]].append(pl)
    arg = 0.0
    for R in _ARG_HOUSES:
        for na, nv in _ARG_PAIRS:
            A, V = hh(R, na), hh(R, nv)
            if sum(wt[q] for q in bhh[A]) > sum(wt[q] for q in bhh[V]):
                s = sum(wt[q] * benefic[q] for q in bhh[A])
                if s > 0: arg += s
    tithi = int(elong / 12) + 1; purna = 1.0 if (tithi - 1) % 5 == 4 else 0.0
    f14 = [rahu, d60c, av10, av1, upa, rl, dhl, av11, bright, moon_disp, moon_sav, sun_disp, arg, purna]
    # ---- CANDIDATE D: house-lord total shadbala + occupant strength ----
    def tsb(pl): return sb[pl]["total_shadbala"] if (pl in sb and "total_shadbala" in sb[pl]) else avg
    l1, l10, l11 = SIGN_LORDS[ls], SIGN_LORDS[(ls + 9) % 12], SIGN_LORDS[(ls + 10) % 12]
    sb_1lord, sb_10lord, sb_11lord = tsb(l1), tsb(l10), tsb(l11)
    sb_keylords = (sb_1lord + sb_10lord + sb_11lord) / 3.0
    occ10 = float(np.mean([tsb(q) for q in bhh[10]])) if bhh[10] else avg
    occ11 = float(np.mean([tsb(q) for q in bhh[11]])) if bhh[11] else avg
    strength = [sb_1lord, sb_10lord, sb_11lord, sb_keylords, occ10, occ11]
    # also carry C's dig_lords to test D-beyond-C
    def db(pl): return sb[pl]["dig_bala"] if (pl in sb and "dig_bala" in sb[pl]) else 30.0
    dig_lords = (db(l1) + db(l10)) / 2.0
    return f14, [float(x) for x in strength], by, (68 <= b["lon"] <= 98 and 6 <= b["lat"] <= 37), float(dig_lords)
FR = [feats(p) for p in FAM]; RR = [feats(p) for p in ORDD]
F = np.array([x[0] for x in FR]); R = np.array([x[0] for x in RR])
FS = np.array([x[1] for x in FR]); RS = np.array([x[1] for x in RR])
FD = np.array([x[4] for x in FR]); RD = np.array([x[4] for x in RR])
X = np.vstack([F, R]); S = np.vstack([FS, RS]); Y = np.array([1] * len(FR) + [0] * len(RR), float)
FY = np.array([x[2] for x in FR]); FI = np.array([x[3] for x in FR])
CUTS = {"full": np.ones(len(FR), bool), ">=1940": (FY >= 1940) & FI, ">=1955": (FY >= 1955) & FI}
def auc(fa, ra): return float(np.mean([np.mean(x > ra) + 0.5 * np.mean(x == ra) for x in fa]))
def cv(Xf, Xr, seed=7):
    Xx = np.vstack([Xf, Xr]); Yy = np.array([1] * len(Xf) + [0] * len(Xr), float)
    np.random.seed(seed); idx = np.random.permutation(len(Yy)); folds = np.array_split(idx, 5); s = np.zeros(len(Yy))
    for i in range(5):
        te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
        sg = np.sign(Xx[tr][Yy[tr] == 1].mean(0) - Xx[tr][Yy[tr] == 0].mean(0)); m, sd = Xx[tr].mean(0), Xx[tr].std(0) + 1e-9
        s[te] = (((Xx[te] - m) / sd) * sg).sum(1)
    return auc(s[Yy == 1], s[Yy == 0])
print(f"famous={len(FR)} ordinary={len(RR)}")
print("\nSolo separation (fam_mean, ord_mean, solo-AUC):")
for i, k in enumerate(MKEYS):
    print(f"  {k:12} fam={FS[:,i].mean():8.1f} ord={RS[:,i].mean():8.1f}  soloAUC={auc(FS[:,i], RS[:,i]):.3f}")
print("\nbase 14-factor:            " + "  ".join(f"{k}={cv(F[CUTS[k]],R):.3f}" for k in CUTS))
for i, k in enumerate(MKEYS):
    Fn = np.column_stack([F, FS[:, i]]); Rn = np.column_stack([R, RS[:, i]])
    print(f"+ {k:12}            " + "  ".join(f"{ck}={cv(Fn[CUTS[ck]],Rn):.3f}" for ck in CUTS))
# best single by |AUC-0.5|
bi = int(np.argmax([abs(auc(FS[:, i], RS[:, i]) - 0.5) for i in range(len(MKEYS))]))
SEEDS = [1, 7, 42, 123, 2024]
print(f"\n--- deciding: per-cut seed-stability of best metric ({MKEYS[bi]}) ---")
Fn = np.column_stack([F, FS[:, bi]]); Rn = np.column_stack([R, RS[:, bi]])
for ck in CUTS:
    bvals = [cv(F[CUTS[ck]], R, seed=sd) for sd in SEEDS]; svals = [cv(Fn[CUTS[ck]], Rn, seed=sd) for sd in SEEDS]
    print(f"  {ck:7} base={np.mean(bvals):.3f}  new={np.mean(svals):.3f}  delta={np.mean(svals)-np.mean(bvals):+.3f}")
# D BEYOND C: base+dig_lords  vs  base+dig_lords+sb_keylords
print(f"\n--- does D add BEYOND C? (base + dig_lords + sb_keylords) ---  corr(sb_keylords,dig_lords)={np.corrcoef(np.concatenate([FS[:,3],RS[:,3]]),np.concatenate([FD,RD]))[0,1]:+.3f}")
Fc = np.column_stack([F, FD]); Rc = np.column_stack([R, RD])                      # base + C
Fcd = np.column_stack([F, FD, FS[:, 3]]); Rcd = np.column_stack([R, RD, RS[:, 3]])  # base + C + D
for ck in CUTS:
    c_only = np.mean([cv(Fc[CUTS[ck]], Rc, seed=sd) for sd in SEEDS])
    c_d = np.mean([cv(Fcd[CUTS[ck]], Rcd, seed=sd) for sd in SEEDS])
    print(f"  {ck:7} base+C={c_only:.3f}  base+C+D={c_d:.3f}  delta_D={c_d-c_only:+.3f}")
for i, k in enumerate(MKEYS):
    allv = np.concatenate([FS[:, i], RS[:, i]]); print(f"REF {k}: ({FS[:,i].mean():.4f}, {RS[:,i].mean():.4f}, {allv.std(ddof=1):.4f})")
