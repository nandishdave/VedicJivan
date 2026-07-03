"""Recompute ONLY the Dasha-timing factor (ReadMe's exact functional-benefic 2x2
node definition) on the current 207 famous vs 96 ordinary set."""
import json
import numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha

FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8"))
ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
CAMP_A = {9, 10, 6, 1, 2, 5}; FB_A = {"Saturn", "Venus", "Mercury"}; FB_B = {"Sun", "Moon", "Mars", "Jupiter"}
_BAD = {3, 6, 8, 12}

def dasha(dob, tob, lat, lon):
    c = build_muhurta_chart(dob=dob, tob=tob, lat=lat, lon=lon)
    P, lag, sb = c["planets"], c["lagna"], c["shadbala"]; ls = lag["sign"]
    def L(h): return SIGN_LORDS[(ls + h - 1) % 12]
    fb = FB_A if ls in CAMP_A else FB_B
    def st(pl):
        if pl in ("Rahu", "Ketu"):
            disp = SIGN_LORDS[P[pl]["sign"]]
            base = min(sb.get(disp, {}).get("ratio", 1.0) / 1.5, 1.0) * 100
            ben = disp in fb or disp == L(1); good = P[disp]["house"] not in _BAD
            tier = 1.20 if (ben and good) else 0.90 if ben else 0.75 if good else 0.45
            return min(base * tier, 100)
        s = min(sb.get(pl, {}).get("ratio", 1.0) / 1.5, 1.0) * 100
        if pl in fb or pl == L(1): s = min(s * 1.15, 100)
        return s
    by = int(dob[:4]); acc = tot = 0.0
    for d in calc_vimshottari_dasha(P["Moon"]["longitude"], dob, tob)["dashas"]:
        ov = max(0, min(int(d["end_date"][:4]) - by, 50) - max(int(d["start_date"][:4]) - by, 20))
        if ov <= 0: continue
        acc += st(d["planet"]) * ov; tot += ov
    return acc / tot if tot else 50

def bd(p): return (p["birth"]["date"], p["birth"]["time"], p["birth"]["lat"], p["birth"]["lon"])
F = np.array([dasha(*bd(p)) for p in FAM])
R = np.array([dasha(*bd(p)) for p in ORDD])
def auc(pos, neg): return float(np.mean([np.mean(p > neg) + 0.5 * np.mean(p == neg) for p in pos]))
print(f"Dasha timing (ages 20-50), current set  famous={len(F)}  ordinary={len(R)}")
print(f"  famous mean   = {F.mean():.2f}")
print(f"  ordinary mean = {R.mean():.2f}")
print(f"  LIFT (fam-ord)= {F.mean()-R.mean():+.2f}")
print(f"  factor AUC    = {auc(F, R):.3f}")
