# -*- coding: utf-8 -*-
"""Tatva of functional benefics + nakshatra types (janma + prime-dasha), famous vs ordinary."""
import json
import numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha

FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8"))
ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
CAMP_A = {9, 10, 6, 1, 2, 5}; FB_A = {"Saturn", "Venus", "Mercury"}; FB_B = {"Sun", "Moon", "Mars", "Jupiter"}
TATVA = ["Agni(fire)", "Prithvi(earth)", "Vayu(air)", "Jal(water)"]  # sign % 4
VIMLORD = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
GANA = ["D", "M", "R", "M", "D", "M", "D", "D", "R", "R", "M", "M", "D", "R", "D", "R", "D", "R",
        "R", "M", "M", "D", "R", "R", "M", "M", "D"]  # 27 nakshatras: Deva/Manushya/Rakshasa

def nak_of(lon): return int((lon % 360) / (360 / 27)) % 27

def profile(p):
    b = p["birth"]
    c = build_muhurta_chart(dob=b["date"], tob=b["time"], lat=b["lat"], lon=b["lon"], with_shadbala=False)
    P, ls = c["planets"], c["lagna"]["sign"]; by = int(b["date"][:4])
    fb = FB_A if ls in CAMP_A else FB_B
    # A: FB tatva fractions
    tv = np.zeros(4)
    for pl in fb: tv[P[pl]["sign"] % 4] += 1
    tv = tv / len(fb)
    # B: janma nakshatra
    jn = nak_of(P["Moon"]["longitude"]); jgana = GANA[jn]; jlord = VIMLORD[jn % 9]
    # C: prime-dasha (20-50) lord's nakshatra — year-weighted gana + lord
    dl = calc_vimshottari_dasha(P["Moon"]["longitude"], b["date"], b["time"])["dashas"]
    gw = {"D": 0.0, "M": 0.0, "R": 0.0}; lw = {}; tot = 0.0
    for d in dl:
        ov = max(0, min(int(d["end_date"][:4]) - by, 50) - max(int(d["start_date"][:4]) - by, 20))
        if ov <= 0: continue
        md = d["planet"]; nk = nak_of(P[md]["longitude"])
        gw[GANA[nk]] += ov; lw[VIMLORD[nk % 9]] = lw.get(VIMLORD[nk % 9], 0) + ov; tot += ov
    gw = {k: v / tot for k, v in gw.items()} if tot else gw
    return {"tv": tv, "jgana": jgana, "jlord": jlord, "prime_gana": gw, "prime_lord": lw, "tot": tot}

FP = [profile(p) for p in FAM]; RP = [profile(p) for p in ORDD]

print("=== A: Functional benefics by Tatva (avg fraction of FBs in each) ===")
print(f"  {'tatva':14} {'famous':>8} {'ordinary':>9} {'diff':>7}")
for i, t in enumerate(TATVA):
    fa = np.mean([r["tv"][i] for r in FP]); ra = np.mean([r["tv"][i] for r in RP])
    print(f"  {t:14} {fa*100:7.1f}% {ra*100:8.1f}% {(fa-ra)*100:+6.1f}%")

print("\n=== B: Janma (Moon) nakshatra GANA ===")
for g, nm in [("D", "Deva"), ("M", "Manushya"), ("R", "Rakshasa")]:
    fa = np.mean([r["jgana"] == g for r in FP]); ra = np.mean([r["jgana"] == g for r in RP])
    print(f"  {nm:10} famous {fa*100:5.1f}%  ordinary {ra*100:5.1f}%  diff {(fa-ra)*100:+5.1f}%")
print("  Janma nakshatra ruling-planet (famous% | ordinary% | diff):")
for lord in VIMLORD:
    fa = np.mean([r["jlord"] == lord for r in FP]); ra = np.mean([r["jlord"] == lord for r in RP])
    print(f"    {lord:8} {fa*100:5.1f}% | {ra*100:5.1f}% | {(fa-ra)*100:+5.1f}%")

print("\n=== C: PRIME-dasha (20-50) MD-lord's nakshatra — year-weighted ===")
print("  GANA (famous | ordinary | diff):")
for g, nm in [("D", "Deva"), ("M", "Manushya"), ("R", "Rakshasa")]:
    fa = np.mean([r["prime_gana"].get(g, 0) for r in FP]); ra = np.mean([r["prime_gana"].get(g, 0) for r in RP])
    print(f"    {nm:10} {fa*100:5.1f}% | {ra*100:5.1f}% | {(fa-ra)*100:+5.1f}%")
print("  ruling-planet of MD-lord's nakshatra (famous | ordinary | diff):")
for lord in VIMLORD:
    fa = np.mean([r["prime_lord"].get(lord, 0) / (r["tot"] if r["tot"] else 1) for r in FP])
    ra = np.mean([r["prime_lord"].get(lord, 0) / (r["tot"] if r["tot"] else 1) for r in RP])
    print(f"    {lord:8} {fa*100:5.1f}% | {ra*100:5.1f}% | {(fa-ra)*100:+5.1f}%")
