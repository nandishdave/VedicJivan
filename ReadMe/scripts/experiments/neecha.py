# -*- coding: utf-8 -*-
"""Neecha-bhanga (cancellation of debilitation) on the D10 10th-lord.
Part 1: do the debilitated-D10 famous charts actually cancel?
Part 2: forward factor across 303 — does CANCELLED debilitation separate fame?"""
import json
import numpy as np
from app.services.muhurta import (build_muhurta_chart, _overall_score, _aspect_score, _verdict, LIFE_ASPECTS)
from app.services.kundli_calculator._core import SIGN_LORDS, SIGN_NAMES, _get_dignity
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha
from app.services.kundli_calculator.divisional import calc_divisional_charts
from app.services.kundli_calculator.raja_yoga import raja_yoga_score
from app.services.kundli_calculator.dhana_yoga import dhana_yoga_score

FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8"))
ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55,
       "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}
_BAD = {3, 6, 8, 12}; _OCC = {3, 6, 10, 11}
EXALT = {"Sun": 0, "Moon": 1, "Mars": 9, "Mercury": 5, "Jupiter": 3, "Venus": 11, "Saturn": 6}
DEBIL = {p: (s + 6) % 12 for p, s in EXALT.items()}
EXALT_OF_SIGN = {s: p for p, s in EXALT.items()}
SPECIAL = {"Mars": {4, 7, 8}, "Jupiter": {5, 7, 9}, "Saturn": {3, 7, 10}}

def _aspects(planet, from_s, to_s):
    dist = ((to_s - from_s) % 12) + 1
    return dist in SPECIAL.get(planet, {7})

def neecha_bhanga(D10, planet):
    """(is_debil, cancelled, reason) for a planet in D10."""
    if D10[planet] != DEBIL.get(planet):
        return (False, False, "not debilitated")
    dsign = D10[planet]; disp = SIGN_LORDS[dsign]; exlt = EXALT_OF_SIGN.get(dsign)
    lag, moon = D10["Lagna"], D10["Moon"]
    kend = {(lag + k) % 12 for k in (0, 3, 6, 9)} | {(moon + k) % 12 for k in (0, 3, 6, 9)}
    if D10[disp] in kend: return (True, True, f"dispositor {disp} in kendra")
    if exlt and D10[exlt] in kend: return (True, True, f"exalted {exlt} in kendra")
    if D10[planet] == D10[disp] or _aspects(disp, D10[disp], D10[planet]): return (True, True, f"conj/aspect by {disp}")
    if exlt and (D10[planet] == D10[exlt] or _aspects(exlt, D10[exlt], D10[planet])): return (True, True, f"aspect by {exlt}")
    if SIGN_LORDS[D10[disp]] == planet: return (True, True, f"parivartana with {disp}")
    return (True, False, "debilitated, NOT cancelled")

def d10_of(p):
    b = p["birth"]
    c = build_muhurta_chart(dob=b["date"], tob=b["time"], lat=b["lat"], lon=b["lon"], with_shadbala=False)
    return c, calc_divisional_charts(c["planets"], c["lagna"])["D10"]

# ---------- PART 1: specific charts ----------
def tenlord(D10): return SIGN_LORDS[(D10["Lagna"] + 9) % 12]
names1 = ["Muhammad Ali", "Oprah Winfrey", "Napoleon Bonaparte", "Taylor Swift", "Sri Aurobindo",
          "Audrey Hepburn", "Alfred Hitchcock", "Prince Harry", "Aamir Khan"]
by = {p.get("name"): p for p in FAM}
print("=== PART 1: debilitated-D10-10th-lord FAMOUS — does it cancel? ===")
for n in names1:
    if n not in by: continue
    _, D10 = d10_of(by[n]); tl = tenlord(D10)
    deb, canc, reason = neecha_bhanga(D10, tl)
    tag = "CANCELLED ✓ (Raja Yoga)" if canc else "not cancelled ✗" if deb else "not debilitated"
    print(f"  {n:22} 10th-lord {tl:8} in {SIGN_NAMES[D10[tl]]:11} -> {tag:26} [{reason}]")

# ---------- PART 2: forward factor across 303 ----------
def corrected_dig(D10):
    tl = tenlord(D10); raw = _DP.get(_get_dignity(tl, D10[tl]), 45)
    deb, canc, _ = neecha_bhanga(D10, tl)
    if deb: return 90.0 if canc else 5.0   # cancelled debilitation acts strong
    return raw

def features(p):
    c, D10 = d10_of(p)
    tl = tenlord(D10); deb, canc, _ = neecha_bhanga(D10, tl)
    return {
        "raw": _DP.get(_get_dignity(tl, D10[tl]), 45),
        "corr": corrected_dig(D10),
        "nbh": 1.0 if (deb and canc) else 0.0,
        "deb": deb, "canc": canc,
    }

FF = [features(p) for p in FAM]; RF = [features(p) for p in ORDD]
def frac(rows, key): return np.mean([r[key] for r in rows])
print("\n=== PART 2a: cancellation base rates ===")
for lab, rows in [("famous", FF), ("ordinary", RF)]:
    ndeb = sum(1 for r in rows if r["deb"]); ncanc = sum(1 for r in rows if r["deb"] and r["canc"])
    print(f"  {lab:9} n={len(rows)}  debilitated-10th-lord={ndeb} ({ndeb/len(rows)*100:.0f}%)  "
          f"of those CANCELLED={ncanc} ({ncanc/ndeb*100 if ndeb else 0:.0f}%)  "
          f"Neecha-bhanga present in {ncanc/len(rows)*100:.0f}% of all")

def auc(a, yv):
    pos = a[yv == 1]; neg = a[yv == 0]
    return float(np.mean([np.mean(p > neg) + 0.5 * np.mean(p == neg) for p in pos]))
yv = np.array([1] * len(FF) + [0] * len(RF), float)
print("\n=== PART 2b: solo lift + AUC ===")
for key, lbl in [("raw", "raw D10 10th-lord dignity"), ("corr", "NB-corrected dignity"), ("nbh", "Neecha-bhanga present (0/1)")]:
    fa = np.array([r[key] for r in FF]); ra = np.array([r[key] for r in RF])
    print(f"  {lbl:28} famous={fa.mean():6.2f} ord={ra.mean():6.2f} lift={fa.mean()-ra.mean():+.2f} AUC={auc(np.concatenate([fa,ra]),yv):.3f}")
