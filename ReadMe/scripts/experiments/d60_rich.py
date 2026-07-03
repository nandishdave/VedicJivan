"""Rich D60 (Shashtiamsa) study — all 5 classical elevation rules, run on the
207-celebrity vs 96-ordinary set. Reports per-rule lift, a rich-D60 composite
AUC, OLD-winners vs NEW-winners (crude D60 -> rich D60), and matched-India cuts.

Rules:
 1  Shashtiamsa DEITY (BPHS 60-name list, odd fwd / even reversed) of KEY planets
 2  KEY-lord dignity in D60 (weighted set, not flat 7)
 3  VARGOTTAMA of key lords (same sign D1 & D60)
 4  D60 LAGNA lord condition (dignity + kendra/trikona of D60)
 5  Yoga REPEATS in D60 (9L-10L / kendra-trikona lords co-located)
Key planets = D1 functional benefics + lagna lord + 9th lord + 10th lord + yogakaraka.
"""
import json
import numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS, _get_dignity
from app.services.kundli_calculator.divisional import calc_divisional_charts
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha

FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8"))
ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
KEN = {1, 4, 7, 10}; TRI = {1, 5, 9}
CAMP_A = {9, 10, 6, 1, 2, 5}; FB_A = {"Saturn", "Venus", "Mercury"}; FB_B = {"Sun", "Moon", "Mars", "Jupiter"}
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55,
       "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}
_BAD = {3, 6, 8, 12}

# BPHS / Parashari 60 Shashtiamsa deities  (name, benefic=1 / malefic=0)  index0 = deity #1
DEITIES = [
 ("Ghora",0),("Rakshasa",0),("Deva",1),("Kubera",1),("Yaksha",1),("Kinnara",1),
 ("Bhrashta",0),("Kulaghna",0),("Garala",0),("Vahni",0),("Maya",0),("Purishaka",0),
 ("Apampathi",1),("Marut",1),("Kaala",0),("Sarpa",0),("Amrita",1),("Indu",1),
 ("Mridu",1),("Komala",1),("Heramba",1),("Brahma",1),("Vishnu",1),("Maheshwara",1),
 ("Deva",1),("Ardra",0),("Kalinasa",0),("Kshiteesha",1),("Kamalakara",1),("Gulika",0),
 ("Mrityu",0),("Kaala",0),("Davagni",0),("Ghora",0),("Yama",0),("Kantaka",0),
 ("Sudha",1),("Amrita",1),("Poornachandra",1),("Vishadagdha",0),("Kulanasa",0),("Vamsakshaya",0),
 ("Utpata",0),("Kaala",0),("Saumya",1),("Komala",1),("Sheetala",1),("Karaladamshtra",0),
 ("Chandramukhi",1),("Praveena",1),("Kaalapavaka",0),("Dandayudha",0),("Nirmala",1),("Saumya",1),
 ("Kroora",0),("Atisheetala",1),("Amrita",1),("Payodhi",1),("Bhramana",0),("Indurekha",1),
]

def deity_benefic(sign, deg_in_sign):
    part = min(int(deg_in_sign / 0.5), 59)          # 0..59  (same index as D60 sign calc)
    idx = part if sign % 2 == 0 else 59 - part      # odd sign fwd / even sign reversed
    return DEITIES[idx][1]

def yogakarakas(ls):
    res = []
    for pl in _C:
        owned = [h for h in range(1, 13) if SIGN_LORDS[(ls + h - 1) % 12] == pl]
        ken = [h for h in owned if h in KEN]; tri = [h for h in owned if h in TRI]
        if any(k != t for k in ken for t in tri):
            res.append(pl)
    return res

FEAT = ["r1_deity", "r2_keydig", "r3_vargottama", "r4_d60lagna", "r5_yoga",
        "d60_crude", "rahu_natal", "av_1st", "av_10th"]

def feats(dob, tob, lat, lon):
    c = build_muhurta_chart(dob=dob, tob=tob, lat=lat, lon=lon)
    P, lag, sb = c["planets"], c["lagna"], c["shadbala"]; ls = lag["sign"]
    def L(h): return SIGN_LORDS[(ls + h - 1) % 12]
    fb = FB_A if ls in CAMP_A else FB_B; by = int(dob[:4])
    key = set(fb) | {L(1), L(9), L(10)} | set(yogakarakas(ls))
    D60 = calc_divisional_charts(P, lag)["D60"]

    # rule 1 — benefic-deity fraction among key planets
    r1 = float(np.mean([deity_benefic(P[pl]["sign"], P[pl]["degree_in_sign"]) for pl in key]))
    # rule 2 — mean D60 dignity of key planets (weighted set, not flat 7)
    r2 = float(np.mean([_DP.get(_get_dignity(pl, D60[pl]), 45) for pl in key]))
    # rule 3 — vargottama count among key planets
    r3 = float(sum(1 for pl in key if P[pl]["sign"] == D60[pl]))
    # rule 4 — D60 lagna lord condition
    dls = D60["Lagna"]; dlord = SIGN_LORDS[dls]
    r4 = _DP.get(_get_dignity(dlord, D60[dlord]), 45) + (20 if ((D60[dlord] - dls) % 12) + 1 in (KEN | TRI) else 0)
    # rule 5 — yoga repeats in D60 (co-location)
    ken_l = {L(h) for h in (1, 4, 7, 10)}; tri_l = {L(h) for h in (1, 5, 9)}
    r5 = (1 if D60[L(9)] == D60[L(10)] else 0) + sum(1 for kl in ken_l for tl in tri_l if kl != tl and D60[kl] == D60[tl])

    # crude d60 (old flat mean of all 7) for comparison
    d60c = float(np.mean([_DP.get(_get_dignity(p, D60[p]), 45) for p in _C]))
    # rahu_natal (age-free) + ashtakavarga 1st/10th — the surviving winners
    dl = calc_vimshottari_dasha(P["Moon"]["longitude"], dob, tob)["dashas"]
    ra = next(((int(d["start_date"][:4]) - by, int(d["end_date"][:4]) - by) for d in dl if d["planet"] == "Rahu"), None)
    natal = max(0, min(ra[1], 50) - max(ra[0], 20)) if ra else 0
    dispf = 1.0 if P[SIGN_LORDS[P["Rahu"]["sign"]]]["house"] not in _BAD else 0.4
    tv = c["ashtakavarga"]["totals"]
    return [r1, r2, r3, r4, float(r5), d60c, natal * dispf, tv[ls], tv[(ls + 9) % 12]], by, (68 <= lon <= 98 and 6 <= lat <= 37)

def bd(p): return (p["birth"]["date"], p["birth"]["time"], p["birth"]["lat"], p["birth"]["lon"])
FR = [feats(*bd(p)) for p in FAM]; RR = [feats(*bd(p)) for p in ORDD]
F = np.array([x[0] for x in FR]); R = np.array([x[0] for x in RR])
FY = np.array([x[1] for x in FR]); FI = np.array([x[2] for x in FR])

print(f"famous={len(F)}  ordinary={len(R)}\nlift (famous | ordinary | diff):")
for i, n in enumerate(FEAT):
    print(f"  {n:13} {F[:, i].mean():7.2f} {R[:, i].mean():7.2f}  {F[:, i].mean() - R[:, i].mean():+6.2f}")

def auc(sc, yy):
    pos = sc[yy == 1]; neg = sc[yy == 0]
    return float(np.mean([np.mean(p > neg) + 0.5 * np.mean(p == neg) for p in pos]))

def cv(Xf, Xr):
    X = np.vstack([Xf, Xr]); y = np.array([1] * len(Xf) + [0] * len(Xr), float)
    np.random.seed(7); idx = np.random.permutation(len(y)); folds = np.array_split(idx, 5)
    cvc = np.zeros(len(y)); cvs = np.zeros(len(y))
    for i in range(5):
        te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
        sg = np.sign(X[tr][y[tr] == 1].mean(0) - X[tr][y[tr] == 0].mean(0))
        m, s = X[tr].mean(0), X[tr].std(0) + 1e-9
        Z = ((X[te] - m) / s) * sg
        cvc[te] = (Z > 0).sum(1) if Xf.shape[1] > 1 else Z[:, 0]; cvs[te] = Z.sum(1)
    return auc(cvc, y), auc(cvs, y)

N = {n: i for i, n in enumerate(FEAT)}
def cols(*names): return [N[n] for n in names]
def report(cs, label, Fm=F, Rm=R):
    c, s = cv(Fm[:, cs], Rm[:, cs])
    print(f"  {label:38s} count-AUC={c:.3f}  sum-AUC={s:.3f}")

print()
report(cols("r1_deity", "r2_keydig", "r3_vargottama", "r4_d60lagna", "r5_yoga"), "RICH-D60 alone (r1-r5)")
report(cols("rahu_natal", "d60_crude", "av_10th", "av_1st"), "OLD winners (crude D60)")
report(cols("rahu_natal", "r1_deity", "r2_keydig", "r3_vargottama", "r4_d60lagna", "r5_yoga", "av_10th", "av_1st"),
       "NEW winners (rich D60 expanded)")

print("\nmatched-India cuts — NEW winners (sum-AUC):")
NW = cols("rahu_natal", "r1_deity", "r2_keydig", "r3_vargottama", "r4_d60lagna", "r5_yoga", "av_10th", "av_1st")
for yr in (0, 1940, 1955):
    mask = (FY >= yr) & FI
    Fm = F[mask]
    if len(Fm) < 20:
        print(f"  India-born >= {yr}: n={len(Fm)} (too small)"); continue
    _, s = cv(Fm[:, NW], R[:, NW])
    print(f"  India-born >= {yr:4d}   n_fam={len(Fm):3d}  avg_yr={int(FY[mask].mean())}   sum-AUC={s:.3f}")
