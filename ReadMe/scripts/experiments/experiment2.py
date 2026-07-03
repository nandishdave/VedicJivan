# -*- coding: utf-8 -*-
"""Experiment 2: per-domain. Fit the 14-factor model on all 321 (standard 5-fold),
then measure AUC per fame domain (Film/Politics/Sports/Business/...) vs the same
ordinary control. Which kinds of fame does the chart detect best? Also India-only
per domain where n allows."""
import json, numpy as np
from collections import Counter
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS, _get_dignity
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha
from app.services.kundli_calculator.raja_yoga import raja_yoga_score
from app.services.kundli_calculator.dhana_yoga import dhana_yoga_score
FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8")); ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]; _ALL = _C + ["Rahu", "Ketu"]
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55, "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}
_BAD = {3, 6, 8, 12}; _OCC = {3, 6, 10, 11}; _ARG_PAIRS = ((2, 12), (4, 10), (5, 9), (11, 3)); _ARG_HOUSES = (2, 10, 12)
def domain(cat):
    c = (cat or "").lower()
    if any(w in c for w in ["actor", "actress", "filmmaker", "comedian", "dancer", "model", "animator"]): return "Film"
    if any(w in c for w in ["musician", "singer", "composer"]): return "Music"
    if any(w in c for w in ["cricket", "tennis", "badminton", "boxer", "golf", "foot", "sprint", "basketball", "f1", "shooter", "chess", "racing", "billiards", "sport"]): return "Sports"
    if any(w in c for w in ["president", "prime minister", "politic", "freedom", "monarch", "chancellor", "emperor", "independence", "revolution", "dictator", "pm ", "duke", "prince", "princess", "wales", "1st pm"]): return "Politics"
    if any(w in c for w in ["industrialist", "entrepreneur", "executive", "investor", "business", "mogul"]): return "Business"
    if any(w in c for w in ["scientist", "physicist", "economist", "mathematic", "astronom", "naturalist", "inventor", "psycho", "philosoph", "author", "poet", "laureate"]): return "Science/Lit"
    if any(w in c for w in ["spiritual", "yogi", "sage", "yoga", "religious", "humanitarian"]): return "Spiritual"
    return "Other"
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
    return [rahu, d60c, av10, av1, upa, rl, dhl, av11, bright, moon_disp, moon_sav, sun_disp, arg, purna]
FR = [(feats(p), domain(p.get("category"))) for p in FAM]; RR = [feats(p) for p in ORDD]
F = np.array([x[0] for x in FR]); DOM = np.array([x[1] for x in FR]); R = np.array(RR)
X = np.vstack([F, R]); Y = np.array([1] * len(FR) + [0] * len(RR), float)
def auc(fa, ra): return float(np.mean([np.mean(x > ra) + 0.5 * np.mean(x == ra) for x in fa]))
# standard 5-fold on ALL 321 -> held-out sum-z score for everyone
np.random.seed(7); idx = np.random.permutation(len(Y)); folds = np.array_split(idx, 5); S = np.zeros(len(Y))
for i in range(5):
    te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
    sg = np.sign(X[tr][Y[tr] == 1].mean(0) - X[tr][Y[tr] == 0].mean(0)); m, sd = X[tr].mean(0), X[tr].std(0) + 1e-9
    S[te] = (((X[te] - m) / sd) * sg).sum(1)
Sf, Sr = S[:len(FR)], S[len(FR):]
print(f"famous={len(FR)} ordinary={len(RR)}  domains={dict(Counter(DOM))}")
print(f"\npooled 14-factor AUC per domain (domain-famous held-out vs all {len(RR)} ordinary):")
rows = []
for dnm in sorted(set(DOM)):
    mask = DOM == dnm
    if mask.sum() < 8: continue
    a = auc(Sf[mask], Sr); rows.append((a, dnm, mask.sum()))
for a, dnm, n in sorted(rows, reverse=True):
    print(f"  {dnm:12} n={n:3d}   AUC={a:.3f}")
print(f"  {'ALL famous':12} n={len(FR):3d}   AUC={auc(Sf, Sr):.3f}")
