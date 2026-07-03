# -*- coding: utf-8 -*-
"""Neecha-bhanga on D10 10th-lord — STRICT: kendra from D10 LAGNA ONLY (no Moon)."""
import json
import numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS, SIGN_NAMES, _get_dignity
from app.services.kundli_calculator.divisional import calc_divisional_charts

FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8"))
ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55,
       "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}
EXALT = {"Sun": 0, "Moon": 1, "Mars": 9, "Mercury": 5, "Jupiter": 3, "Venus": 11, "Saturn": 6}
DEBIL = {p: (s + 6) % 12 for p, s in EXALT.items()}
EXALT_OF_SIGN = {s: p for p, s in EXALT.items()}
SPECIAL = {"Mars": {4, 7, 8}, "Jupiter": {5, 7, 9}, "Saturn": {3, 7, 10}}

def _aspects(planet, from_s, to_s):
    return (((to_s - from_s) % 12) + 1) in SPECIAL.get(planet, {7})

def neecha_bhanga(D10, planet):
    if D10[planet] != DEBIL.get(planet):
        return (False, False, "not debilitated")
    dsign = D10[planet]; disp = SIGN_LORDS[dsign]; exlt = EXALT_OF_SIGN.get(dsign)
    lag = D10["Lagna"]
    kend = {(lag + k) % 12 for k in (0, 3, 6, 9)}          # LAGNA ONLY
    if D10[disp] in kend: return (True, True, f"dispositor {disp} in kendra")
    if exlt and D10[exlt] in kend: return (True, True, f"exalted {exlt} in kendra")
    if D10[planet] == D10[disp] or _aspects(disp, D10[disp], D10[planet]): return (True, True, f"conj/aspect by {disp}")
    if exlt and (D10[planet] == D10[exlt] or _aspects(exlt, D10[exlt], D10[planet])): return (True, True, f"aspect by {exlt}")
    if SIGN_LORDS[D10[disp]] == planet: return (True, True, f"parivartana with {disp}")
    return (True, False, "debilitated, NOT cancelled")

def d10_of(p):
    b = p["birth"]
    c = build_muhurta_chart(dob=b["date"], tob=b["time"], lat=b["lat"], lon=b["lon"], with_shadbala=False)
    return calc_divisional_charts(c["planets"], c["lagna"])["D10"]
def tenlord(D10): return SIGN_LORDS[(D10["Lagna"] + 9) % 12]

names1 = ["Muhammad Ali", "Oprah Winfrey", "Napoleon Bonaparte", "Taylor Swift", "Sri Aurobindo",
          "Audrey Hepburn", "Alfred Hitchcock", "Prince Harry", "Aamir Khan"]
by = {p.get("name"): p for p in FAM}
print("=== PART 1 (STRICT, Lagna-only): the 9 icons ===")
for n in names1:
    if n not in by: continue
    D10 = d10_of(by[n]); tl = tenlord(D10); deb, canc, reason = neecha_bhanga(D10, tl)
    tag = "CANCELLED ✓" if canc else "NOT cancelled ✗"
    print(f"  {n:22} {tl:8} deb {SIGN_NAMES[D10[tl]]:11} -> {tag:16} [{reason}]")

def feats(p):
    D10 = d10_of(p); tl = tenlord(D10); deb, canc, _ = neecha_bhanga(D10, tl)
    raw = _DP.get(_get_dignity(tl, D10[tl]), 45)
    corr = (90.0 if canc else 5.0) if deb else raw
    return {"raw": raw, "corr": corr, "nbh": 1.0 if (deb and canc) else 0.0, "deb": deb, "canc": canc}
FF = [feats(p) for p in FAM]; RF = [feats(p) for p in ORDD]
print("\n=== PART 2a (STRICT): cancellation base rates ===")
for lab, rows in [("famous", FF), ("ordinary", RF)]:
    nd = sum(1 for r in rows if r["deb"]); nc = sum(1 for r in rows if r["deb"] and r["canc"])
    print(f"  {lab:9} debilitated={nd} ({nd/len(rows)*100:.0f}%)  cancelled={nc} ({nc/nd*100 if nd else 0:.0f}% of debil)  "
          f"Neecha-bhanga in {nc/len(rows)*100:.0f}% of all")
yv = np.array([1] * len(FF) + [0] * len(RF), float)
def auc(a):
    pos = a[yv == 1]; neg = a[yv == 0]
    return float(np.mean([np.mean(p > neg) + 0.5 * np.mean(p == neg) for p in pos]))
print("\n=== PART 2b (STRICT): solo lift + AUC ===")
for key, lbl in [("raw", "raw D10 10th-lord dignity"), ("corr", "NB-corrected dignity"), ("nbh", "Neecha-bhanga present (0/1)")]:
    fa = np.array([r[key] for r in FF]); ra = np.array([r[key] for r in RF])
    print(f"  {lbl:28} fam={fa.mean():6.2f} ord={ra.mean():6.2f} lift={fa.mean()-ra.mean():+.2f} AUC={auc(np.concatenate([fa,ra])):.3f}")
