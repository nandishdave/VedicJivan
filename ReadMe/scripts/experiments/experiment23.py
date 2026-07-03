# -*- coding: utf-8 -*-
"""#2 domain-specific model (Science+Business+Politics = worldly achievers) +
#3 Arudha Lagna (AL) fame rules. One 14-factor pass for both."""
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
_DIGN = {"Exalted", "Moolatrikona", "Own Sign"}
_BAD = {3, 6, 8, 12}; _OCC = {3, 6, 10, 11}; _ARG_PAIRS = ((2, 12), (4, 10), (5, 9), (11, 3)); _ARG_HOUSES = (2, 10, 12)
KT = {1, 4, 5, 7, 9, 10}; KEND = {1, 4, 7, 10}
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
def arudha_lagna(lagna_sign, P):
    lord = SIGN_LORDS[lagna_sign]; lsgn = P[lord]["sign"]; d = (lsgn - lagna_sign) % 12
    al = (lsgn + d) % 12
    if al == lagna_sign or al == (lagna_sign + 6) % 12: al = (al + 9) % 12
    return al
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
    # ---- Arudha Lagna metrics ----
    al = arudha_lagna(ls, P); ben = {"Jupiter", "Venus", "Mercury"} | ({"Moon"} if bright else set())
    hal = lambda sgn: ((sgn - al) % 12) + 1     # house from AL
    al_2_11_ben = sum(1 for q in _C if q in ben and hal(P[q]["sign"]) in {2, 11})
    al_kt_ben = sum(1 for q in _C if q in ben and hal(P[q]["sign"]) in KT)
    al_occ = sum(1 for q in _ALL if hal(P[q]["sign"]) == 1)
    al_2_10_11 = sum(1 for q in _ALL if hal(P[q]["sign"]) in {2, 10, 11})
    al_lagna_kt = 1.0 if (((al - ls) % 12) + 1) in KT else 0.0
    allord = SIGN_LORDS[al]; al_lord_strong = 1.0 if (_get_dignity(allord, P[allord]["sign"]) in _DIGN or P[allord]["house"] in KEND) else 0.0
    almet = {"al_2_11_ben": al_2_11_ben, "al_kt_ben": al_kt_ben, "al_occ": al_occ, "al_2_10_11": al_2_10_11, "al_lagna_kt": al_lagna_kt, "al_lord_strong": al_lord_strong}
    return f14, domain(p.get("category")) if "category" in p else "ord", almet, (68 <= b["lon"] <= 98 and 6 <= b["lat"] <= 37)
FR = [feats(p) for p in FAM]; RR = [feats(p) for p in ORDD]
F = np.array([x[0] for x in FR]); DOM = np.array([x[1] for x in FR]); R = np.array([x[0] for x in RR])
X = np.vstack([F, R]); Y = np.array([1] * len(FR) + [0] * len(RR), float)
def auc(fa, ra): return float(np.mean([np.mean(x > ra) + 0.5 * np.mean(x == ra) for x in fa]))
def cv_scores(Xin, Yin, seed=7):
    np.random.seed(seed); idx = np.random.permutation(len(Yin)); folds = np.array_split(idx, 5); s = np.zeros(len(Yin))
    for i in range(5):
        te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
        sg = np.sign(Xin[tr][Yin[tr] == 1].mean(0) - Xin[tr][Yin[tr] == 0].mean(0)); m, sd = Xin[tr].mean(0), Xin[tr].std(0) + 1e-9
        s[te] = (((Xin[te] - m) / sd) * sg).sum(1)
    return s
# ===== #2 domain-specific model =====
print(f"famous={len(FR)} ordinary={len(RR)}  domains={dict(Counter(DOM))}")
WORLDLY = np.isin(DOM, ["Science/Lit", "Business", "Politics"])
Sall = cv_scores(X, Y); Sf = Sall[:len(FR)]
print("\n=== #2 Worldly-achiever cluster (Science/Lit+Business+Politics) ===")
print(f"  pooled model, evaluated on cluster:   n={WORLDLY.sum()}  AUC={auc(Sf[WORLDLY], Sall[len(FR):]):.3f}")
Xc = np.vstack([F[WORLDLY], R]); Yc = np.array([1] * WORLDLY.sum() + [0] * len(RR), float)
Sc = cv_scores(Xc, Yc); print(f"  DOMAIN-SPECIFIC model (fit on cluster): n={WORLDLY.sum()}  AUC={auc(Sc[Yc==1], Sc[Yc==0]):.3f}")
# performance/devotion cluster for contrast
PERF = np.isin(DOM, ["Film", "Sports", "Music", "Spiritual"])
print(f"  (contrast) Performance/devotion cluster pooled: n={PERF.sum()}  AUC={auc(Sf[PERF], Sall[len(FR):]):.3f}")
# ===== #3 Arudha Lagna =====
print("\n=== #3 Arudha Lagna fame rules (full 225 vs 96) ===")
IDX = {"full": np.ones(len(FR), bool), ">=1940": np.array([x[3] for x in FR])}
def colal(rows, k): return np.array([r[2][k] for r in rows], float)
def cv14(Fm, Rm):
    Xx = np.vstack([Fm, Rm]); Yy = np.array([1] * len(Fm) + [0] * len(Rm), float); s = cv_scores(Xx, Yy)
    return auc(s[Yy == 1], s[Yy == 0])
FI = np.array([x[3] for x in FR]); mask40 = FI
print(f"base 14-factor: full={cv14(F,R):.3f}  India={cv14(F[mask40],R):.3f}")
for k in ["al_2_11_ben", "al_kt_ben", "al_occ", "al_2_10_11", "al_lagna_kt", "al_lord_strong"]:
    Ff = colal(FR, k); Rf = colal(RR, k); Fn = np.column_stack([F, Ff]); Rn = np.column_stack([R, Rf])
    print(f"  {k:16} fam {Ff.mean():5.2f} ord {Rf.mean():5.2f}  solo={auc(Ff,Rf):.3f}  | +comp full={cv14(Fn,Rn):.3f} India={cv14(Fn[mask40],Rn):.3f}")
