# -*- coding: utf-8 -*-
"""(1) Per-planet Vimsopaka Bala calculator core (16 Shodashavarga, 7-tier dignity, /20).
(2) Pattern analysis: which planets carry high Vimsopaka in famous vs ordinary, and does
the PLACEMENT of high-Vimsopaka planets in specific houses form a rule? Tested vs the
current 15-factor model. (225 vs 96)"""
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
_GOOD = {1, 2, 4, 5, 9, 10, 11}; _KT = {1, 4, 5, 7, 9, 10}
_VARGA_W = {"D1": 3.5, "D2": 1, "D3": 1, "D4": 0.5, "D7": 0.5, "D9": 3, "D10": 0.5, "D12": 0.5,
            "D16": 2, "D20": 0.5, "D24": 0.5, "D27": 0.5, "D30": 1, "D40": 0.5, "D45": 0.5, "D60": 4}

def vimsopaka(pl, P, dv):
    """Vimsopaka Bala of one planet: sum over 16 vargas of weight x dignity%/100. Range 0-20."""
    t = 0.0
    for v, w in _VARGA_W.items():
        sgn = P[pl]["sign"] if v == "D1" else dv[v][pl]
        t += w * (_DP.get(_get_dignity(pl, sgn), 45) / 100.0)
    return t

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
    vp = {q: vimsopaka(q, P, dv) for q in _C}
    dl = calc_vimshottari_dasha(P["Moon"]["longitude"], b["date"], b["time"])["dashas"]
    ra = next(((int(d["start_date"][:4]) - by, int(d["end_date"][:4]) - by) for d in dl if d["planet"] == "Rahu"), None)
    rahu = (max(0, min(ra[1], 50) - max(ra[0], 20)) if ra else 0) * (1.0 if P[SIGN_LORDS[P["Rahu"]["sign"]]]["house"] not in _BAD else 0.4)
    vim_avg = float(np.mean(list(vp.values())))
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
    def db(pl): return sb[pl]["dig_bala"] if (pl in sb and "dig_bala" in sb[pl]) else 30.0
    dig_lords = (db(SIGN_LORDS[ls]) + db(SIGN_LORDS[(ls + 9) % 12])) / 2.0
    f15 = [rahu, vim_avg, av10, av1, upa, rl, dhl, av11, bright, moon_disp, moon_sav, sun_disp, arg, purna, dig_lords]
    # per-planet Vimsopaka + house
    pv = [vp[q] for q in _C]                                   # 7 per-planet Vimsopaka
    houses = {q: P[q]["house"] for q in _C}
    fb = list({SIGN_LORDS[(ls + h) % 12] for h in (0, 4, 8)})  # functional benefics (trikona lords)
    fb_vim = float(np.mean([vp[q] for q in fb]))
    top = max(_C, key=lambda q: vp[q])                          # highest-Vimsopaka planet
    top_house_good = 1.0 if houses[top] in _GOOD else 0.0
    top_house_kt = 1.0 if houses[top] in _KT else 0.0
    nstrong_good = float(sum(1 for q in _C if vp[q] > 11.0 and houses[q] in {1, 10, 11}))
    vim_10occ = float(np.mean([vp[q] for q in _C if houses[q] == 10])) if any(houses[q] == 10 for q in _C) else vim_avg
    patt = [fb_vim, top_house_good, top_house_kt, nstrong_good, vim_10occ]
    return f15, pv, patt, houses, by, (68 <= b["lon"] <= 98 and 6 <= b["lat"] <= 37), p.get("name", "?")

FR = [feats(p) for p in FAM]; RR = [feats(p) for p in ORDD]
# ---- (1) CALCULATOR DEMO: per-planet Vimsopaka for 4 sample famous charts ----
print("=== CALCULATOR DEMO — per-planet Vimsopaka Bala (0-20) ===")
print(f"  {'name':22} " + " ".join(f"{q[:3]:>5}" for q in _C) + "   top")
for x in FR[:4]:
    pv = x[1]; nm = x[6][:22]
    top = _C[int(np.argmax(pv))]
    print(f"  {nm:22} " + " ".join(f"{v:5.1f}" for v in pv) + f"   {top}")

# ---- (2) PATTERN: per-planet Vimsopaka, famous vs ordinary ----
PV_F = np.array([x[1] for x in FR]); PV_R = np.array([x[1] for x in RR])
def auc(fa, ra): return float(np.mean([np.mean(x > ra) + 0.5 * np.mean(x == ra) for x in fa]))
print("\n=== PATTERN 1 — which planet's Vimsopaka separates fame? (per-planet solo AUC) ===")
for i, q in enumerate(_C):
    print(f"  {q:8} fam={PV_F[:,i].mean():5.2f}  ord={PV_R[:,i].mean():5.2f}  diff={PV_F[:,i].mean()-PV_R[:,i].mean():+5.2f}  soloAUC={auc(PV_F[:,i], PV_R[:,i]):.3f}")

# high-Vimsopaka planets: which HOUSE do they sit in? (famous vs ordinary)
print("\n=== PATTERN 2 — house of each chart's HIGHEST-Vimsopaka planet (share of charts) ===")
def top_house_dist(rows):
    d = np.zeros(13)
    for x in rows:
        pv = x[1]; top = _C[int(np.argmax(pv))]; d[x[3][top]] += 1
    return d / len(rows)
tf, tr = top_house_dist(FR), top_house_dist(RR)
print("  house:   " + " ".join(f"{h:>5}" for h in range(1, 13)))
print("  famous:  " + " ".join(f"{tf[h]*100:4.0f}%" for h in range(1, 13)))
print("  ordnry:  " + " ".join(f"{tr[h]*100:4.0f}%" for h in range(1, 13)))

# ---- (3) PATTERN as candidate factor-16 vs the 15-factor model ----
PKEYS = ["fb_vim", "top_house_good", "top_house_kt", "nstrong_good", "vim_10occ"]
F = np.array([x[0] for x in FR]); R = np.array([x[0] for x in RR])
PS_F = np.array([x[2] for x in FR]); PS_R = np.array([x[2] for x in RR])
X = np.vstack([F, R]); S = np.vstack([PS_F, PS_R]); Y = np.array([1]*len(FR)+[0]*len(RR), float)
FY = np.array([x[4] for x in FR]); FI = np.array([x[5] for x in FR])
CUTS = {"full": np.ones(len(FR), bool), ">=1940": (FY >= 1940) & FI, ">=1955": (FY >= 1955) & FI}
def cv(Xf, Xr, seed=7):
    Xx = np.vstack([Xf, Xr]); Yy = np.array([1]*len(Xf)+[0]*len(Xr), float)
    np.random.seed(seed); idx = np.random.permutation(len(Yy)); folds = np.array_split(idx, 5); s = np.zeros(len(Yy))
    for i in range(5):
        te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
        sg = np.sign(Xx[tr][Yy[tr]==1].mean(0) - Xx[tr][Yy[tr]==0].mean(0)); m, sd = Xx[tr].mean(0), Xx[tr].std(0)+1e-9
        s[te] = (((Xx[te]-m)/sd)*sg).sum(1)
    return auc(s[Yy==1], s[Yy==0])
print("\n=== PATTERN 3 — placement rules tested as factor 16 (base = 15-factor) ===")
for i, k in enumerate(PKEYS):
    print(f"  {k:14} fam={PS_F[:,i].mean():6.2f} ord={PS_R[:,i].mean():6.2f}  soloAUC={auc(PS_F[:,i],PS_R[:,i]):.3f}")
print("\nbase 15-factor:            " + "  ".join(f"{k}={cv(F[CUTS[k]],R):.3f}" for k in CUTS))
for i, k in enumerate(PKEYS):
    Fn = np.column_stack([F, PS_F[:, i]]); Rn = np.column_stack([R, PS_R[:, i]])
    print(f"+ {k:14}          " + "  ".join(f"{ck}={cv(Fn[CUTS[ck]],Rn):.3f}" for ck in CUTS))
np.random.seed(7); idx = np.random.permutation(len(Y)); folds = np.array_split(idx, 5); s = np.zeros(len(Y)); picks = []
for i in range(5):
    te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
    seps = [abs(S[tr][Y[tr]==1, m].mean() - S[tr][Y[tr]==0, m].mean())/(S[tr][:, m].std()+1e-9) for m in range(len(PKEYS))]
    bm = int(np.argmax(seps)); picks.append(PKEYS[bm])
    Xx = np.column_stack([X, S[:, bm]]); sg = np.sign(Xx[tr][Y[tr]==1].mean(0)-Xx[tr][Y[tr]==0].mean(0)); m_, sd_ = Xx[tr].mean(0), Xx[tr].std(0)+1e-9
    s[te] = (((Xx[te]-m_)/sd_)*sg).sum(1)
print(f"\n+ nested best-of-5/fold (HONEST): full={auc(s[Y==1],s[Y==0]):.3f}  picks={picks}")

# ---- DECIDING: per-cut seed-stability of the pre-committed rules ----
SEEDS = [1, 7, 42, 123, 2024]
print("\n=== DECIDING: per-cut seed-stability (pre-committed, 5 seeds) ===")
for name, i in [("top_house_good", 1), ("nstrong_good", 3)]:
    Fn = np.column_stack([F, PS_F[:, i]]); Rn = np.column_stack([R, PS_R[:, i]])
    print(f"  +{name}:")
    for ck in CUTS:
        bvals = [cv(F[CUTS[ck]], R, seed=sd) for sd in SEEDS]
        svals = [cv(Fn[CUTS[ck]], Rn, seed=sd) for sd in SEEDS]
        print(f"     {ck:7} base={np.mean(bvals):.3f}  new={np.mean(svals):.3f}  delta={np.mean(svals)-np.mean(bvals):+.3f}  {[f'{v:.3f}' for v in svals]}")
    allv = np.concatenate([PS_F[:, i], PS_R[:, i]]); print(f"     REF {name}: ({PS_F[:,i].mean():.4f}, {PS_R[:,i].mean():.4f}, {allv.std(ddof=1):.4f})")
# variant: strongest planet NOT in a dusthana {6,8,12} (tighter, principled)
def notdus(rows):
    out = []
    for x in rows:
        pv = x[1]; top = _C[int(np.argmax(pv))]; out.append(1.0 if x[3][top] not in (6, 8, 12) else 0.0)
    return np.array(out)
ndF, ndR = notdus(FR), notdus(RR)
print(f"\n  variant 'top NOT in dusthana 6/8/12': fam={ndF.mean():.3f} ord={ndR.mean():.3f} soloAUC={auc(ndF,ndR):.3f}")
Fn = np.column_stack([F, ndF]); Rn = np.column_stack([R, ndR])
for ck in CUTS:
    svals = [cv(Fn[CUTS[ck]], Rn, seed=sd) for sd in SEEDS]
    bvals = [cv(F[CUTS[ck]], R, seed=sd) for sd in SEEDS]
    print(f"     {ck:7} base={np.mean(bvals):.3f}  new={np.mean(svals):.3f}  delta={np.mean(svals)-np.mean(bvals):+.3f}")

# ---- ACID TEST: nested house-set re-derivation (good_set learned per TRAIN fold only) ----
THF = np.array([x[3][_C[int(np.argmax(x[1]))]] for x in FR])  # strongest-planet house, famous
THR = np.array([x[3][_C[int(np.argmax(x[1]))]] for x in RR])
def nested_tophouse(seed):
    Xx = np.vstack([F, R]); TH = np.concatenate([THF, THR]); yy = Y
    np.random.seed(seed); idx = np.random.permutation(len(yy)); folds = np.array_split(idx, 5); s = np.zeros(len(yy))
    picks = []
    for i in range(5):
        te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
        good = set()
        for h in range(1, 13):
            fr = np.mean(TH[tr][yy[tr] == 1] == h); orr = np.mean(TH[tr][yy[tr] == 0] == h)
            if fr > orr: good.add(h)
        picks.append(tuple(sorted(good)))
        feat = np.array([1.0 if TH[k] in good else 0.0 for k in range(len(yy))])
        Xa = np.column_stack([Xx, feat]); sg = np.sign(Xa[tr][yy[tr] == 1].mean(0) - Xa[tr][yy[tr] == 0].mean(0))
        m, sd = Xa[tr].mean(0), Xa[tr].std(0) + 1e-9; s[te] = (((Xa[te] - m) / sd) * sg).sum(1)
    return auc(s[yy == 1], s[yy == 0]), picks
print("\n=== ACID TEST: nested house-set re-derived per fold (the honest number) ===")
base_full = np.mean([cv(F, R, seed=sd) for sd in SEEDS])
vals = []
for sd in SEEDS:
    a, pk = nested_tophouse(sd); vals.append(a)
print(f"  base full (5-seed): {base_full:.3f}")
print(f"  nested top-house full (5-seed): {np.mean(vals):.3f}  {[f'{v:.3f}' for v in vals]}  delta={np.mean(vals)-base_full:+.3f}")
_, pk7 = nested_tophouse(7); print(f"  per-fold good-sets (seed 7): {pk7}")

# ---- CONFIRM the refined rule: strongest planet in {1,2,11} (any planet) ----
print("\n=== CONFIRM refined rule: strongest-Vimsopaka planet in {1,2,11} ===")
for setname, hs in [("{1,2,11}", {1, 2, 11}), ("{1,2,4,5,10,11}", {1, 2, 4, 5, 10, 11})]:
    fF = np.array([1.0 if h in hs else 0.0 for h in THF]); fR = np.array([1.0 if h in hs else 0.0 for h in THR])
    Fn = np.column_stack([F, fF]); Rn = np.column_stack([R, fR])
    print(f"  top in {setname}  (solo AUC {auc(fF, fR):.3f}):")
    for ck in CUTS:
        bvals = [cv(F[CUTS[ck]], R, seed=sd) for sd in SEEDS]; svals = [cv(Fn[CUTS[ck]], Rn, seed=sd) for sd in SEEDS]
        print(f"     {ck:7} base={np.mean(bvals):.3f}  new={np.mean(svals):.3f}  delta={np.mean(svals)-np.mean(bvals):+.3f}  {[f'{v:.3f}' for v in svals]}")
    allv = np.concatenate([fF, fR]); print(f"     REF: ({fF.mean():.4f}, {fR.mean():.4f}, {allv.std(ddof=1):.4f})")
