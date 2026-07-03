# -*- coding: utf-8 -*-
"""KP (Krishnamurti Paddhati) Cuspal Sub-Lord fame checks. Self-contained KP
engine (Placidus + KP ayanamsa + sub-lords + significators). Do the CSLs of the
success houses signify 2/6/10/11 more often in famous? Lift over 14-factor."""
import json, numpy as np, swisseph as swe
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import get_julian_day, SIGN_LORDS, _get_dignity
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha
from app.services.kundli_calculator.raja_yoga import raja_yoga_score
from app.services.kundli_calculator.dhana_yoga import dhana_yoga_score
FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8")); ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]; _ALL = _C + ["Rahu", "Ketu"]
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55, "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}
_BAD = {3, 6, 8, 12}; _OCC = {3, 6, 10, 11}; _ARG_PAIRS = ((2, 12), (4, 10), (5, 9), (11, 3)); _ARG_HOUSES = (2, 10, 12)
VIM = [("Ketu", 7), ("Venus", 20), ("Sun", 6), ("Moon", 10), ("Mars", 7), ("Rahu", 18), ("Jupiter", 16), ("Saturn", 19), ("Mercury", 17)]
NAK = 360.0 / 27.0; PLC = [("Sun", swe.SUN), ("Moon", swe.MOON), ("Mars", swe.MARS), ("Mercury", swe.MERCURY), ("Jupiter", swe.JUPITER), ("Venus", swe.VENUS), ("Saturn", swe.SATURN), ("Rahu", swe.MEAN_NODE)]
SUCCESS = {2, 6, 10, 11}; NAME = {1, 10, 11}
def star_lord(L): return VIM[int(L / NAK) % 9][0]
def sub_lord(L):
    nak = int(L / NAK); off = L - nak * NAK; start = nak % 9; acc = 0.0
    for i in range(9):
        idx = (start + i) % 9; span = VIM[idx][1] / 120.0 * NAK
        if off < acc + span: return VIM[idx][0]
        acc += span
    return VIM[(start + 8) % 9][0]
def kp_significators(dob, tob, lat, lon):
    """Return dict: for each cusp/planet sub-lord, the set of houses it signifies."""
    jd = get_julian_day(dob, tob, lat, lon)
    swe.set_sid_mode(swe.SIDM_KRISHNAMURTI); flags = swe.FLG_SIDEREAL | swe.FLG_SPEED
    cusps, _ascmc = swe.houses_ex(jd, lat, lon, b"P", swe.FLG_SIDEREAL); cusps = list(cusps)
    plon = {}
    for nm, code in PLC:
        res, _ = swe.calc_ut(jd, code, flags); plon[nm] = res[0] % 360
    plon["Ketu"] = (plon["Rahu"] + 180) % 360
    def house_of(L):
        for h in range(12):
            a = cusps[h]; span = (cusps[(h + 1) % 12] - a) % 360
            if (L - a) % 360 < span: return h + 1
        return 12
    occ = {p: house_of(plon[p]) for p in _ALL}                       # planet -> house occupied
    owned = {p: set() for p in _ALL}
    for h in range(12):
        lord = SIGN_LORDS[int(cusps[h] / 30)]
        if lord in owned: owned[lord].add(h + 1)
    def signifies(planet):                                            # houses a planet signifies
        sl = star_lord(plon[planet]); hs = {occ[sl]} | owned[sl] | {occ[planet]} | owned[planet]
        if planet in ("Rahu", "Ketu"):
            sd = SIGN_LORDS[int(plon[planet] / 30)]; hs |= {occ[sd]} | owned[sd]
        return hs
    return cusps, plon, signifies
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
    P, lag = c["planets"], c["lagna"]; ls = lag["sign"]; by = int(b["date"][:4])
    dl = calc_vimshottari_dasha(P["Moon"]["longitude"], b["date"], b["time"])["dashas"]
    ra = next(((int(d["start_date"][:4]) - by, int(d["end_date"][:4]) - by) for d in dl if d["planet"] == "Rahu"), None)
    rahu = (max(0, min(ra[1], 50) - max(ra[0], 20)) if ra else 0) * (1.0 if P[SIGN_LORDS[P["Rahu"]["sign"]]]["house"] not in _BAD else 0.4)
    D60 = c["divisional"]["D60"]; d60c = float(np.mean([_DP.get(_get_dignity(x, D60[x]), 45) for x in _C]))
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
    # ---- KP cuspal sub-lord checks ----
    cusps, plon, sig = kp_significators(b["date"], b["time"], b["lat"], b["lon"])
    csl = lambda cusp_idx: sub_lord(cusps[cusp_idx])   # cusp_idx 0-based (0=1st)
    s10 = 1.0 if sig(csl(9)) & SUCCESS else 0.0
    s11 = 1.0 if sig(csl(10)) & SUCCESS else 0.0
    s2 = 1.0 if sig(csl(1)) & SUCCESS else 0.0
    n1 = 1.0 if sig(csl(0)) & NAME else 0.0
    s6 = 1.0 if sig(csl(5)) & {6, 10, 11} else 0.0
    cnt = s10 + s11 + s2 + n1
    sun_sub = 1.0 if sub_lord(plon["Sun"]) and (sig_of := sig(sub_lord(plon["Sun"]))) and (sig_of & NAME) else 0.0
    moon_sub = 1.0 if sig(sub_lord(plon["Moon"])) & SUCCESS else 0.0
    kp = {"csl10": s10, "csl11": s11, "csl2": s2, "csl1_name": n1, "csl6": s6, "csl_count": cnt, "sun_sub": sun_sub, "moon_sub": moon_sub}
    return f14, kp, by, (68 <= b["lon"] <= 98 and 6 <= b["lat"] <= 37)
FR = [feats(p) for p in FAM]; RR = [feats(p) for p in ORDD]
F14 = np.array([x[0] for x in FR]); R14 = np.array([x[0] for x in RR])
FY = np.array([x[2] for x in FR]); FI = np.array([x[3] for x in FR])
IDX = {"full": np.ones(len(FR), bool), ">=1940": (FY >= 1940) & FI, ">=1955": (FY >= 1955) & FI}
def colk(rows, k): return np.array([r[1][k] for r in rows], float)
def auc(fa, ra): return float(np.mean([np.mean(x > ra) + 0.5 * np.mean(x == ra) for x in fa]))
def cv(F, R):
    X = np.vstack([F, R]); y = np.array([1] * len(F) + [0] * len(R), float)
    np.random.seed(7); idx = np.random.permutation(len(y)); folds = np.array_split(idx, 5); s = np.zeros(len(y))
    for i in range(5):
        te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
        sg = np.sign(X[tr][y[tr] == 1].mean(0) - X[tr][y[tr] == 0].mean(0)); m, sd = X[tr].mean(0), X[tr].std(0) + 1e-9
        s[te] = (((X[te] - m) / sd) * sg).sum(1)
    return auc(s[y == 1], s[y == 0])
print(f"famous={len(FR)} ordinary={len(RR)}   [KP: Placidus + Krishnamurti ayanamsa]")
print(f"base 14-factor:  " + "  ".join(f"{k}={cv(F14[IDX[k]],R14):.3f}" for k in IDX))
LB = {"csl10": "10th CSL->2/6/10/11", "csl11": "11th CSL->2/6/10/11", "csl2": "2nd CSL->2/6/10/11",
      "csl1_name": "1st CSL->1/10/11", "csl6": "6th CSL->6/10/11", "csl_count": "count of 1/2/10/11 CSL",
      "sun_sub": "Sun sub->1/10/11", "moon_sub": "Moon sub->2/6/10/11"}
print(f"{'metric':22} {'fam%':>6} {'ord%':>6} {'diff':>6}  solo-AUC  |  +composite (full/>=1940/>=1955)")
for k in ["csl10", "csl11", "csl2", "csl1_name", "csl6", "csl_count", "sun_sub", "moon_sub"]:
    Ff = colk(FR, k); Rf = colk(RR, k); F = np.column_stack([F14, Ff]); R = np.column_stack([R14, Rf])
    comp = "  ".join(f"{c}={cv(F[IDX[c]],R):.3f}" for c in IDX)
    sc = 100 if k != "csl_count" else 1
    print(f"  {LB[k]:22} {Ff.mean()*sc:6.1f} {Rf.mean()*sc:6.1f} {(Ff.mean()-Rf.mean())*sc:+6.1f}  {auc(Ff,Rf):.3f}   |  {comp}")
