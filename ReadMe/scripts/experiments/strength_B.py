# -*- coding: utf-8 -*-
"""Candidate B - YOGAKARAKA condition as factor 15. The yogakaraka = the single planet
owning one kendra (4/7/10) AND one trikona (5/9) from lagna (Sat: Taurus/Libra, Mars:
Cancer/Leo, Ven: Cap/Aqu). Metrics (NaN when the lagna has no true yogakaraka):
  yk_str   = Vimsopaka bala (Shodashavarga) of the yogakaraka
  yk_place = placement of yk from lagna (kendra/trikona/own good, dusthana bad)
  yk_dasha = fraction of prime (20-50) under the yk mahadasha
  yk_dign  = D1 dignity of yk
  yk_qual  = 0.4*(str/20)+0.3*place+0.3*dasha  (combined)
Tested (a) solo WITHIN the yk-subset (famous-yk vs ordinary-yk, no lagna confound) and
(b) as factor 15 on the whole set (NaN->neutral col-mean). Nested/cuts/seed. (225 vs 96)"""
import json, numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS, _get_dignity
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha
from app.services.kundli_calculator.raja_yoga import raja_yoga_score
from app.services.kundli_calculator.dhana_yoga import dhana_yoga_score
FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8")); ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]; _ALL = _C + ["Rahu", "Ketu"]
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55, "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}
_DIGN = {"Exalted", "Moolatrikona", "Own Sign"}
_BAD = {3, 6, 8, 12}; _OCC = {3, 6, 10, 11}; _ARG_PAIRS = ((2, 12), (4, 10), (5, 9), (11, 3)); _ARG_HOUSES = (2, 10, 12)
VARGA_W = {"D1": 3.5, "D2": 1, "D3": 1, "D4": 0.5, "D7": 0.5, "D9": 3, "D10": 0.5, "D12": 0.5,
           "D16": 2, "D20": 0.5, "D24": 0.5, "D27": 0.5, "D30": 1, "D40": 0.5, "D45": 0.5, "D60": 4}
KEN = {4, 7, 10}; TRIK = {5, 9}; GOOD = {1, 4, 5, 7, 9, 10}
MKEYS = ["yk_str", "yk_place", "yk_dasha", "yk_dign", "yk_qual"]
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
    # ---- CANDIDATE B: yogakaraka ----
    def owns(pl): return [h for h in range(1, 13) if SIGN_LORDS[(ls + h - 1) % 12] == pl]
    yk = None
    for q in _C:
        hs = set(owns(q))
        if (hs & KEN) and (hs & TRIK): yk = q; break
    if yk is None:
        strength = [np.nan] * 5; has = 0.0
    else:
        def vimsopaka(pl):
            t = 0.0
            for v, w in VARGA_W.items():
                sgn = P[pl]["sign"] if v == "D1" else dv[v][pl]
                t += w * (_DP.get(_get_dignity(pl, sgn), 45) / 100.0)
            return t
        yk_str = vimsopaka(yk)
        yh = P[yk]["house"]; yk_place = 1.0 if yh in GOOD else (0.4 if yh in _BAD else 0.6)
        yk_dign = _DP.get(_get_dignity(yk, P[yk]["sign"]), 45) / 100.0
        acc = 0.0
        for d in dl:
            ov = max(0, min(int(d["end_date"][:4]) - by, 50) - max(int(d["start_date"][:4]) - by, 20))
            if ov > 0 and d["planet"] == yk: acc += ov
        yk_dasha = acc / 30.0
        yk_qual = 0.4 * (yk_str / 20.0) + 0.3 * yk_place + 0.3 * yk_dasha
        strength = [yk_str, yk_place, yk_dasha, yk_dign, yk_qual]; has = 1.0
    return f14, [float(x) for x in strength], by, (68 <= b["lon"] <= 98 and 6 <= b["lat"] <= 37), has
FR = [feats(p) for p in FAM]; RR = [feats(p) for p in ORDD]
F = np.array([x[0] for x in FR]); R = np.array([x[0] for x in RR])
FS = np.array([x[1] for x in FR]); RS = np.array([x[1] for x in RR])
FH = np.array([x[4] for x in FR]); RH = np.array([x[4] for x in RR])
X = np.vstack([F, R]); Y = np.array([1] * len(FR) + [0] * len(RR), float)
FY = np.array([x[2] for x in FR]); FI = np.array([x[3] for x in FR])
CUTS = {"full": np.ones(len(FR), bool), ">=1940": (FY >= 1940) & FI, ">=1955": (FY >= 1955) & FI}
def auc(fa, ra):
    fa = fa[~np.isnan(fa)]; ra = ra[~np.isnan(ra)]
    if len(fa) == 0 or len(ra) == 0: return float("nan")
    return float(np.mean([np.mean(x > ra) + 0.5 * np.mean(x == ra) for x in fa]))
def fill(col_f, col_r):
    both = np.concatenate([col_f, col_r]); mu = np.nanmean(both)
    return np.where(np.isnan(col_f), mu, col_f), np.where(np.isnan(col_r), mu, col_r)
def cv(Xf, Xr, seed=7):
    Xx = np.vstack([Xf, Xr]); Yy = np.array([1] * len(Xf) + [0] * len(Xr), float)
    np.random.seed(seed); idx = np.random.permutation(len(Yy)); folds = np.array_split(idx, 5); s = np.zeros(len(Yy))
    for i in range(5):
        te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
        sg = np.sign(Xx[tr][Yy[tr] == 1].mean(0) - Xx[tr][Yy[tr] == 0].mean(0)); m, sd = Xx[tr].mean(0), Xx[tr].std(0) + 1e-9
        s[te] = (((Xx[te] - m) / sd) * sg).sum(1)
    return auc(s[Yy == 1], s[Yy == 0])
print(f"famous={len(FR)} ordinary={len(RR)}   have-yogakaraka: fam={int(FH.sum())}/{len(FH)}  ord={int(RH.sum())}/{len(RH)}")
print(f"  yk-lagna base rate:  famous {FH.mean():.3f}  ordinary {RH.mean():.3f}  (AUC of 'has yk'={auc(FH,RH):.3f})")
print("\nSolo AUC WITHIN yk-subset (famous-yk vs ordinary-yk, no lagna confound):")
for i, k in enumerate(MKEYS):
    print(f"  {k:9} fam={np.nanmean(FS[:,i]):7.3f} ord={np.nanmean(RS[:,i]):7.3f}  soloAUC={auc(FS[:,i],RS[:,i]):.3f}")
print("\nAs factor 15 (NaN->neutral col-mean), base 14-factor:")
print("  base:                  " + "  ".join(f"{k}={cv(F[CUTS[k]],R):.3f}" for k in CUTS))
for i, k in enumerate(MKEYS):
    cf, cr = fill(FS[:, i], RS[:, i]); Fn = np.column_stack([F, cf]); Rn = np.column_stack([R, cr])
    print(f"  + {k:9}            " + "  ".join(f"{ck}={cv(Fn[CUTS[ck]],Rn):.3f}" for ck in CUTS))
# nested best-of-5/fold on the whole set
Sf = np.column_stack([fill(FS[:, i], RS[:, i])[0] for i in range(5)]); Sr = np.column_stack([fill(FS[:, i], RS[:, i])[1] for i in range(5)])
Sall = np.vstack([Sf, Sr])
np.random.seed(7); idx = np.random.permutation(len(Y)); folds = np.array_split(idx, 5); s = np.zeros(len(Y)); picks = []
for i in range(5):
    te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
    seps = [abs(Sall[tr][Y[tr] == 1, m].mean() - Sall[tr][Y[tr] == 0, m].mean()) / (Sall[tr][:, m].std() + 1e-9) for m in range(5)]
    bm = int(np.argmax(seps)); picks.append(MKEYS[bm])
    Xx = np.column_stack([X, Sall[:, bm]]); sg = np.sign(Xx[tr][Y[tr] == 1].mean(0) - Xx[tr][Y[tr] == 0].mean(0)); m_, sd_ = Xx[tr].mean(0), Xx[tr].std(0) + 1e-9
    s[te] = (((Xx[te] - m_) / sd_) * sg).sum(1)
print(f"\n+ nested best-of-5/fold (HONEST): full={auc(s[Y==1],s[Y==0]):.3f}  picks={picks}")
