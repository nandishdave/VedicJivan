"""Calibration: per-factor famous_mean, ordinary_mean, and POOLED std (over all
303 charts) for the 7-factor worldly-potential REF distribution."""
import json
import numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS, _get_dignity
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha
from app.services.kundli_calculator.divisional import calc_divisional_charts
from app.services.kundli_calculator.raja_yoga import raja_yoga_score
from app.services.kundli_calculator.dhana_yoga import dhana_yoga_score

FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8"))
ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55,
       "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}
_BAD = {3, 6, 8, 12}; OCC = {3, 6, 10, 11}
FEAT = ["rahu_prime", "d60", "av_10th", "av_1st", "upa_occ", "raja_late", "dhana_late"]

def _pw(links):
    w = {}
    for lk in links:
        for p in lk.get("planets", []):
            w[p] = w.get(p, 0.0) + lk["score"]
    return w
def _act(dl, by, wd, a, b):
    tot = acc = 0.0
    for d in dl:
        ov = max(0, min(int(d["end_date"][:4]) - by, b) - max(int(d["start_date"][:4]) - by, a))
        if ov <= 0: continue
        tot += ov; acc += wd.get(d["planet"], 0.0) * ov
    return acc / tot if tot else 0.0

def feats(dob, tob, lat, lon):
    c = build_muhurta_chart(dob=dob, tob=tob, lat=lat, lon=lon)
    P, lag = c["planets"], c["lagna"]; ls = lag["sign"]; by = int(dob[:4])
    dl = calc_vimshottari_dasha(P["Moon"]["longitude"], dob, tob)["dashas"]
    ra = next(((int(d["start_date"][:4]) - by, int(d["end_date"][:4]) - by) for d in dl if d["planet"] == "Rahu"), None)
    dispf = 1.0 if P[SIGN_LORDS[P["Rahu"]["sign"]]]["house"] not in _BAD else 0.4
    rahu = (max(0, min(ra[1], 50) - max(ra[0], 20)) if ra else 0) * dispf
    D60 = calc_divisional_charts(P, lag)["D60"]
    d60c = float(np.mean([_DP.get(_get_dignity(p, D60[p]), 45) for p in _C]))
    tv = c["ashtakavarga"]["totals"]; av10 = tv[(ls + 9) % 12]; av1 = tv[ls]
    tot = occ = 0.0
    for d in dl:
        ov = max(0, min(int(d["end_date"][:4]) - by, 50) - max(int(d["start_date"][:4]) - by, 20))
        if ov <= 0: continue
        tot += ov
        if P[d["planet"]]["house"] in OCC: occ += ov
    upa = occ / tot if tot else 0.0
    return [rahu, d60c, av10, av1, upa, _act(dl, by, _pw(raja_yoga_score(c)[1]), 50, 80), _act(dl, by, _pw(dhana_yoga_score(c)[1]), 50, 80)]

def bd(p): return (p["birth"]["date"], p["birth"]["time"], p["birth"]["lat"], p["birth"]["lon"])
F = np.array([feats(*bd(p)) for p in FAM]); R = np.array([feats(*bd(p)) for p in ORDD])
ALL = np.vstack([F, R])
print("REF = {")
for i, n in enumerate(FEAT):
    fam, ordm, std = F[:, i].mean(), R[:, i].mean(), ALL[:, i].std(ddof=1)
    print(f'    "{n}": ({fam:.4f}, {ordm:.4f}, {std:.4f}),')
print("}")
