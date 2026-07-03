# -*- coding: utf-8 -*-
"""Sun exercise (mirror of the Moon): 8 factors from the SUN sign vs the Lagna
(per-factor + composite), Sun-sign own SAV, and Sun-dispositor placement +
connection to Lagna/Lagnesh. Famous(225) vs ordinary(96)."""
import json
import numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS, _get_dignity
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha
from app.services.kundli_calculator.divisional import calc_divisional_charts

FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8"))
ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55, "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}
_BAD = {3, 6, 8, 12}; _OCC = {3, 6, 10, 11}
FEAT = ["rahu_prime", "d60", "av_10th", "av_1st", "upa_occ", "raja_late", "dhana_late", "av_11th"]

def eight(P, dl, tv, D60, R, by):
    ra = next(((int(d["start_date"][:4]) - by, int(d["end_date"][:4]) - by) for d in dl if d["planet"] == "Rahu"), None)
    ry = max(0, min(ra[1], 50) - max(ra[0], 20)) if ra else 0
    rahu = ry * (1.0 if ((P[SIGN_LORDS[P["Rahu"]["sign"]]]["sign"] - R) % 12) + 1 not in _BAD else 0.4)
    d60c = float(np.mean([_DP.get(_get_dignity(p, D60[p]), 45) for p in _C]))
    av10, av1, av11 = tv[(R + 9) % 12], tv[R], tv[(R + 10) % 12]
    def Lr(h): return SIGN_LORDS[(R + h - 1) % 12]
    raja_set = {Lr(h) for h in (1, 4, 7, 10)} | {Lr(h) for h in (1, 5, 9)}; dhana_set = {Lr(h) for h in (1, 2, 11)}
    tot = occ = rl = dl2 = t2 = 0.0
    for d in dl:
        ov = max(0, min(int(d["end_date"][:4]) - by, 50) - max(int(d["start_date"][:4]) - by, 20))
        if ov > 0:
            tot += ov
            if ((P[d["planet"]]["sign"] - R) % 12) + 1 in _OCC: occ += ov
        ovl = max(0, min(int(d["end_date"][:4]) - by, 80) - max(int(d["start_date"][:4]) - by, 50))
        if ovl > 0:
            t2 += ovl
            if d["planet"] in raja_set: rl += ovl
            if d["planet"] in dhana_set: dl2 += ovl
    return [rahu, d60c, av10, av1, occ / tot if tot else 0, rl / t2 if t2 else 0, dl2 / t2 if t2 else 0, av11]

def feats(p):
    b = p["birth"]; c = build_muhurta_chart(dob=b["date"], tob=b["time"], lat=b["lat"], lon=b["lon"], with_shadbala=False)
    P, lag = c["planets"], c["lagna"]; ls = lag["sign"]; by = int(b["date"][:4])
    dl = calc_vimshottari_dasha(P["Moon"]["longitude"], b["date"], b["time"])["dashas"]
    tv = c["ashtakavarga"]["totals"]; D60 = calc_divisional_charts(P, lag)["D60"]
    ss = P["Sun"]["sign"]; asp = c["graha_drishti"]["planet_aspects"]; LL = SIGN_LORDS[ls]
    sun_disp = SIGN_LORDS[ss]; sdh = P[sun_disp]["house"]
    def connects(X):
        if X == LL: return True
        if P[X]["house"] == P[LL]["house"]: return True
        if P[LL]["house"] in asp.get(X, []) or P[X]["house"] in asp.get(LL, []): return True
        if SIGN_LORDS[P[X]["sign"]] == LL and SIGN_LORDS[P[LL]["sign"]] == X: return True
        if P[X]["house"] == 1 or 1 in asp.get(X, []): return True
        return False
    return {"lag8": eight(P, dl, tv, D60, ls, by), "sun8": eight(P, dl, tv, D60, ss, by),
            "sun_sav": tv[ss], "sun_disp_house": sdh, "sun_connects": 1.0 if connects(sun_disp) else 0.0,
            "india": (68 <= b["lon"] <= 98 and 6 <= b["lat"] <= 37)}

FR = [feats(p) for p in FAM]; RR = [feats(p) for p in ORDD]
yv = np.array([1] * len(FR) + [0] * len(RR), float)
Fl = np.array([r["lag8"] for r in FR]); Rl = np.array([r["lag8"] for r in RR])
Fs = np.array([r["sun8"] for r in FR]); Rs = np.array([r["sun8"] for r in RR])
def auc(fa, ra): return float(np.mean([np.mean(x > ra) + 0.5 * np.mean(x == ra) for x in fa]))
def cv(F, R):
    X = np.vstack([F, R]); y = np.array([1] * len(F) + [0] * len(R), float)
    np.random.seed(7); idx = np.random.permutation(len(y)); folds = np.array_split(idx, 5); s = np.zeros(len(y))
    for i in range(5):
        te = folds[i]; tr = np.concatenate([folds[j] for j in range(5) if j != i])
        sg = np.sign(X[tr][y[tr] == 1].mean(0) - X[tr][y[tr] == 0].mean(0)); m, sd = X[tr].mean(0), X[tr].std(0) + 1e-9
        s[te] = (((X[te] - m) / sd) * sg).sum(1)
    return auc(s[y == 1], s[y == 0])

print(f"famous={len(FR)} ordinary={len(RR)}")
print("\n=== 1. 8 factors: LAGNA vs SUN reference (per-factor solo AUC) ===")
print(f"  {'factor':11} | LAGNA | SUN")
for i, n in enumerate(FEAT):
    print(f"  {n:11} | {auc(Fl[:,i], Rl[:,i]):.3f} | {auc(Fs[:,i], Rs[:,i]):.3f}" + ("  <-- Sun applicable" if auc(Fs[:,i], Rs[:,i]) >= 0.53 else ""))
print(f"\n  composite Lagna-8 sum-AUC = {cv(Fl, Rl):.3f}   |   Sun-8 sum-AUC = {cv(Fs, Rs):.3f}")

sav_f = np.array([r["sun_sav"] for r in FR]); sav_r = np.array([r["sun_sav"] for r in RR])
cn_f = np.array([r["sun_connects"] for r in FR]); cn_r = np.array([r["sun_connects"] for r in RR])
print("\n=== 2. Sun-sign own SAV  &  Sun-dispositor connection ===")
print(f"  Sun-sign SAV            famous {sav_f.mean():.1f} ord {sav_r.mean():.1f}  AUC={auc(np.concatenate([sav_f,sav_r]), yv):.3f}")
print(f"  Sun-disp connects L/LL  famous {cn_f.mean()*100:.0f}% ord {cn_r.mean()*100:.0f}%  AUC={auc(np.concatenate([cn_f,cn_r]), yv):.3f}")
print("\n=== 3. Sun-dispositor by house (famous% | ordinary% | diff) ===")
Fh = np.array([r["sun_disp_house"] for r in FR]); Rh = np.array([r["sun_disp_house"] for r in RR])
for h in range(1, 13):
    fa = np.mean(Fh == h) * 100; ra = np.mean(Rh == h) * 100
    print(f"  house {h:2}: {fa:4.1f}% | {ra:4.1f}%  ({fa-ra:+4.1f})" + ("  <-- famous" if fa - ra > 2 else "  <-- ordinary" if fa - ra < -2 else ""))
