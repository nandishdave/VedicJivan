# -*- coding: utf-8 -*-
"""Jaimini Chara-Karaka connections (conjunction + RASHI DRISHTI) — which karaka
pairs form the Jaimini raja-yoga link more often in famous vs ordinary? And does
AK-AmK / AK-PK etc. earn factor 15 over the 14-factor model? (225 vs 96)"""
import json, numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS, _get_dignity
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha
from app.services.kundli_calculator.raja_yoga import raja_yoga_score
from app.services.kundli_calculator.dhana_yoga import dhana_yoga_score
from app.services.kundli_calculator.jaimini import calc_jaimini_karakas
FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8")); ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]; _ALL = _C + ["Rahu", "Ketu"]
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55, "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}
_BAD = {3, 6, 8, 12}; _OCC = {3, 6, 10, 11}; _ARG_PAIRS = ((2, 12), (4, 10), (5, 9), (11, 3)); _ARG_HOUSES = (2, 10, 12)
MOV = {0, 3, 6, 9}; FIX = {1, 4, 7, 10}; DUAL = {2, 5, 8, 11}
ROLES = ["Atma", "Amatya", "Bhratru", "Matrua", "Putra", "Gnati", "Dara"]
AB = {"Atma": "AK", "Amatya": "AmK", "Bhratru": "BK", "Matrua": "MK", "Putra": "PK", "Gnati": "GK", "Dara": "DK"}
def rd_aspects(s):
    if s in MOV: return FIX - {(s + 1) % 12}
    if s in FIX: return MOV - {(s - 1) % 12}
    return DUAL - {s}
def connected(sa, sb):
    conj = (sa == sb); asp = (sb in rd_aspects(sa)); return conj, asp, (conj or asp)
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
    kar = calc_jaimini_karakas(P, lag)["chara"]
    ksign = {r: P[kar[r]["planet"]]["sign"] for r in ROLES}
    return f14, ksign, by, (68 <= b["lon"] <= 98 and 6 <= b["lat"] <= 37)
FR = [feats(p) for p in FAM]; RR = [feats(p) for p in ORDD]
F14 = np.array([x[0] for x in FR]); R14 = np.array([x[0] for x in RR])
FY = np.array([x[2] for x in FR]); FI = np.array([x[3] for x in FR])
IDX = {"full": np.ones(len(FR), bool), ">=1940": (FY >= 1940) & FI, ">=1955": (FY >= 1955) & FI}
def auc(fa, ra): return float(np.mean([np.mean(x > ra) + 0.5 * np.mean(x == ra) for x in fa]))
def cv(F, R):
    X = np.vstack([F, R]); y = np.array([1] * len(F) + [0] * len(R), float)
    np.random.seed(7); idx = np.random.permutation(len(y)); folds = np.array_split(idx, 5); s = np.zeros(len(y))
    for i in range(5):
        te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
        sg = np.sign(X[tr][y[tr] == 1].mean(0) - X[tr][y[tr] == 0].mean(0)); m, sd = X[tr].mean(0), X[tr].std(0) + 1e-9
        s[te] = (((X[te] - m) / sd) * sg).sum(1)
    return auc(s[y == 1], s[y == 0])
def pair_conn(rows, a, b, mode):  # mode: 'conj','asp','conn'
    out = []
    for _, ksign, *_ in rows:
        cj, ap, cn = connected(ksign[a], ksign[b]); out.append({"conj": cj, "asp": ap, "conn": cn}[mode])
    return np.array(out, float)
print(f"famous={len(FR)} ordinary={len(RR)}\n=== Karaka-pair CONNECTION rates (conj + rashi drishti) — famous% vs ordinary% ===")
KEY = [("Atma","Amatya"),("Atma","Putra"),("Amatya","Putra"),("Atma","Dara"),("Atma","Bhratru"),("Atma","Matrua"),("Atma","Gnati"),("Amatya","Dara"),("Putra","Dara")]
print(f"  {'pair':10} {'conn F%':>8} {'O%':>6} {'diff':>6} | {'conj F%':>8} {'O%':>6} | {'asp F%':>7} {'O%':>6}")
for a, b in KEY:
    cnF = pair_conn(FR,a,b,'conn'); cnR = pair_conn(RR,a,b,'conn')
    cjF = pair_conn(FR,a,b,'conj'); cjR = pair_conn(RR,a,b,'conj')
    apF = pair_conn(FR,a,b,'asp');  apR = pair_conn(RR,a,b,'asp')
    print(f"  {AB[a]+'-'+AB[b]:10} {cnF.mean()*100:7.1f} {cnR.mean()*100:6.1f} {(cnF.mean()-cnR.mean())*100:+6.1f} | {cjF.mean()*100:7.1f} {cjR.mean()*100:6.1f} | {apF.mean()*100:6.1f} {apR.mean()*100:6.1f}")
print(f"\nbase 14-factor:  " + "  ".join(f"{k}={cv(F14[IDX[k]],R14):.3f}" for k in IDX))
def test(name, a, b):
    Ff = pair_conn(FR,a,b,'conn'); Rf = pair_conn(RR,a,b,'conn')
    F = np.column_stack([F14, Ff]); R = np.column_stack([R14, Rf])
    print(f"+ {name:14} solo-AUC={auc(Ff,Rf):.3f}  |  " + "  ".join(f"{k}={cv(F[IDX[k]],R):.3f}" for k in IDX))
for a, b, nm in [("Atma","Amatya","AK-AmK"),("Atma","Putra","AK-PK"),("Amatya","Putra","AmK-PK"),("Atma","Dara","AK-DK")]:
    test(nm, a, b)
# raja3 = count of {AK-AmK, AK-PK, AmK-PK} connected (0-3)
r3F = sum(pair_conn(FR,a,b,'conn') for a,b in [("Atma","Amatya"),("Atma","Putra"),("Amatya","Putra")])
r3R = sum(pair_conn(RR,a,b,'conn') for a,b in [("Atma","Amatya"),("Atma","Putra"),("Amatya","Putra")])
F = np.column_stack([F14, r3F]); R = np.column_stack([R14, r3R])
print(f"+ {'raja3 (0-3)':14} solo-AUC={auc(r3F,r3R):.3f}  |  " + "  ".join(f"{k}={cv(F[IDX[k]],R):.3f}" for k in IDX) + f"   (fam {r3F.mean():.2f} ord {r3R.mean():.2f})")
