# -*- coding: utf-8 -*-
"""Per-factor solo lift + AUC, computed from the LAGNA vs the MOON reference.
Which of the 8 factors are 'applicable' from the Chandra Kundali? Famous(225) vs ordinary(96).
(raja/dhana use the simplified yoga-lord activation, applied identically to both refs.)"""
import json
import numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS, _get_dignity
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha
from app.services.kundli_calculator.divisional import calc_divisional_charts

FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8"))
ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55,
       "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}
_BAD = {3, 6, 8, 12}; _OCC = {3, 6, 10, 11}
FEAT = ["rahu_prime", "d60", "av_10th", "av_1st", "upa_occ", "raja_late", "dhana_late", "av_11th"]

def eight(P, dl, tv, D60, R, by):
    ra = next(((int(d["start_date"][:4]) - by, int(d["end_date"][:4]) - by) for d in dl if d["planet"] == "Rahu"), None)
    ry = max(0, min(ra[1], 50) - max(ra[0], 20)) if ra else 0
    disp = SIGN_LORDS[P["Rahu"]["sign"]]
    rahu = ry * (1.0 if ((P[disp]["sign"] - R) % 12) + 1 not in _BAD else 0.4)
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

def both(p):
    b = p["birth"]
    c = build_muhurta_chart(dob=b["date"], tob=b["time"], lat=b["lat"], lon=b["lon"], with_shadbala=False)
    P, lag = c["planets"], c["lagna"]; by = int(b["date"][:4])
    dl = calc_vimshottari_dasha(P["Moon"]["longitude"], b["date"], b["time"])["dashas"]
    tv = c["ashtakavarga"]["totals"]; D60 = calc_divisional_charts(P, lag)["D60"]
    return eight(P, dl, tv, D60, lag["sign"], by), eight(P, dl, tv, D60, P["Moon"]["sign"], by)

FR = [both(p) for p in FAM]; RR = [both(p) for p in ORDD]
Flag = np.array([x[0] for x in FR]); Rlag = np.array([x[0] for x in RR])
Fmoon = np.array([x[1] for x in FR]); Rmoon = np.array([x[1] for x in RR])
yv = np.array([1] * len(FR) + [0] * len(RR), float)
def auc(fa, ra):
    return float(np.mean([np.mean(x > ra) + 0.5 * np.mean(x == ra) for x in fa]))

print(f"famous={len(FR)} ordinary={len(RR)}\n")
print(f"  {'factor':11} | {'LAGNA  lift    AUC':22} | {'MOON   lift    AUC':22}")
print("  " + "-" * 60)
for i, n in enumerate(FEAT):
    ll = Flag[:, i].mean() - Rlag[:, i].mean(); la = auc(Flag[:, i], Rlag[:, i])
    ml = Fmoon[:, i].mean() - Rmoon[:, i].mean(); ma = auc(Fmoon[:, i], Rmoon[:, i])
    flag = "  <-- applicable" if ma >= 0.53 else ("  (weak)" if ma >= 0.50 else "  (null/rev)")
    print(f"  {n:11} | {ll:+7.2f}   {la:.3f}       | {ml:+7.2f}   {ma:.3f}{flag}")
