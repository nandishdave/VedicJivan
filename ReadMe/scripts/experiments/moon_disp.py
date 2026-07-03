# -*- coding: utf-8 -*-
"""Moon-sign DISPOSITOR (rashi lord) only — placement + connection to Lagna/Lagnesh.
Verify Indira Gandhi & Trump, then compare famous(225) vs ordinary(96)."""
import json
import numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS, SIGN_NAMES, _get_dignity
from app.services.kundli_calculator.divisional import calc_divisional_charts

FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8"))
ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55,
       "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}
KENDRA = {1, 4, 7, 10}; TRIKONA = {1, 5, 9}

def analyze(p):
    b = p["birth"]
    c = build_muhurta_chart(dob=b["date"], tob=b["time"], lat=b["lat"], lon=b["lon"], with_shadbala=False)
    P, ls = c["planets"], c["lagna"]["sign"]
    asp = c["graha_drishti"]["planet_aspects"]; LL = SIGN_LORDS[ls]
    ms = P["Moon"]["sign"]; disp = SIGN_LORDS[ms]; dh = P[disp]["house"]
    def connects(X):
        if X == LL: return True
        if P[X]["house"] == P[LL]["house"]: return True
        if P[LL]["house"] in asp.get(X, []) or P[X]["house"] in asp.get(LL, []): return True
        if SIGN_LORDS[P[X]["sign"]] == LL and SIGN_LORDS[P[LL]["sign"]] == X: return True
        if P[X]["house"] == 1 or 1 in asp.get(X, []): return True
        return False
    return {
        "lagna": SIGN_NAMES[ls], "lagnesh": LL, "moon_sign": SIGN_NAMES[ms], "disp": disp,
        "disp_house": dh, "in_1st": dh == 1, "in_kendra": dh in KENDRA, "in_trikona": dh in TRIKONA,
        "connects": connects(disp), "is_lagnesh": disp == LL,
        "disp_dig": _DP.get(_get_dignity(disp, P[disp]["sign"]), 45),
    }

print("=== verify examples ===")
by = {p.get("name"): p for p in FAM}
for n in ("Indira Gandhi", "Donald Trump"):
    if n in by:
        a = analyze(by[n])
        print(f"  {n}: Lagna {a['lagna']} (lord {a['lagnesh']}) | Moon {a['moon_sign']} -> dispositor {a['disp']} in house {a['disp_house']}"
              f"  | in 1st: {a['in_1st']} | connects lagna/lagnesh: {a['connects']}")

FA = [analyze(p) for p in FAM]; RA = [analyze(p) for p in ORDD]
yv = np.array([1] * len(FA) + [0] * len(RA), float)
def auc(sc):
    p, n = sc[yv == 1], sc[yv == 0]
    return float(np.mean([np.mean(x > n) + 0.5 * np.mean(x == n) for x in p]))

print("\n=== Moon dispositor — famous vs ordinary ===")
for key, lab in [("in_1st", "in the 1st house (Lagna)"), ("in_kendra", "in a kendra (1/4/7/10)"),
                 ("in_trikona", "in a trikona (1/5/9)"), ("connects", "connects to Lagna/Lagnesh"),
                 ("is_lagnesh", "IS the Lagnesh")]:
    fa = np.array([1.0 if a[key] else 0.0 for a in FA]); ra = np.array([1.0 if a[key] else 0.0 for a in RA])
    print(f"  dispositor {lab:26} famous {fa.mean()*100:4.0f}%  ordinary {ra.mean()*100:4.0f}%  AUC={auc(np.concatenate([fa,ra])):.3f}")
fd = np.array([a["disp_dig"] for a in FA]); rd = np.array([a["disp_dig"] for a in RA])
print(f"  dispositor dignity (avg /100)          famous {fd.mean():4.0f}   ordinary {rd.mean():4.0f}   AUC={auc(np.concatenate([fd,rd])):.3f}")

print("\n=== Moon-dispositor HOUSE distribution (famous% | ordinary%) ===")
for h in range(1, 13):
    fa = np.mean([a["disp_house"] == h for a in FA]) * 100; ra = np.mean([a["disp_house"] == h for a in RA]) * 100
    star = "  <--" if abs(fa - ra) > 3 else ""
    print(f"  house {h:2}: {fa:4.1f}% | {ra:4.1f}%  ({fa-ra:+4.1f}){star}")
