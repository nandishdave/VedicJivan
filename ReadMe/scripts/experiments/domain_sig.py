# -*- coding: utf-8 -*-
"""Domain-signature analysis: segment the celebrities by field, and find each
domain's chart signature (planetary prominence + house SAV emphasis) vs the
all-famous baseline. Cheap chart (no Shadbala) -> fast."""
import json
import numpy as np
from collections import defaultdict
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import _get_dignity

FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8"))
_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55,
       "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}
_ANG = {1, 4, 5, 7, 9, 10}; _DUS = {6, 8, 12}

def domain(cat):
    c = (cat or "").lower()
    def has(*ks): return any(k in c for k in ks)
    if has("actor", "actress", "filmmaker", "comedian", "model", "animator", "director", "media mogul"): return "Cinema"
    if has("musician", "singer", "composer", "dancer"): return "Music"
    if has("cricket", "tennis", "badminton", "boxer", "golf", "foot", "sprint", "basketball", "f1", "billiard", "chess", "sportsperson", "racing", "shooter", "driver"): return "Sports"
    if has("scientist", "physicist", "economist", "mathematician", "naturalist", "astronomer", "inventor", "psychoanalyst", "psychiatrist"): return "Science"
    if has("spiritual", "yogi", "yoga", "sage", "religious", "guru", "humanitarian", "philosopher"): return "Spiritual"
    if has("author", "poet"): return "Literature"
    if has("industrial", "entrepreneur", "tech executive", "business", "investor"): return "Business"
    if has("president", "prime minister", "pm of", "politician", "monarch", "chancellor", "secretary", "prince", "princess", "duke", "dictator", "emperor", "independence", "revolution", "freedom", "leader"): return "Politics"
    return "Other"

def features(p):
    b = p["birth"]
    c = build_muhurta_chart(dob=b["date"], tob=b["time"], lat=b["lat"], lon=b["lon"], with_shadbala=False)
    P, ls = c["planets"], c["lagna"]["sign"]
    prom = {}
    for pl in _C:
        dig = _DP.get(_get_dignity(pl, P[pl]["sign"]), 45)
        h = P[pl]["house"]
        hq = 100 if h in _ANG else 35 if h in _DUS else 60
        prom[pl] = 0.6 * dig + 0.4 * hq
    tv = c["ashtakavarga"]["totals"]
    sav = {h: tv[(ls + h - 1) % 12] for h in (1, 3, 5, 9, 10, 11)}
    return prom, sav

dom = defaultdict(list)
allp = {pl: [] for pl in _C}; allh = {h: [] for h in (1, 3, 5, 9, 10, 11)}
rows = []
for p in FAM:
    d = domain(p.get("category"))
    prom, sav = features(p)
    rows.append((d, p.get("name"), prom, sav))
    dom[d].append((prom, sav))
    for pl in _C: allp[pl].append(prom[pl])
    for h in allh: allh[h].append(sav[h])

base_p = {pl: np.mean(allp[pl]) for pl in _C}
base_h = {h: np.mean(allh[h]) for h in allh}

print("=== domain counts + sample ===")
for d in sorted(dom, key=lambda k: -len(dom[k])):
    names = [n for (dd, n, _, _) in rows if dd == d][:6]
    print(f"  {d:12} n={len(dom[d]):3}  e.g. {', '.join(names)}")

print(f"\n=== all-famous baseline ===")
print("  planet prominence:", {pl: round(base_p[pl]) for pl in _C})
print("  house SAV:        ", {h: round(base_h[h], 1) for h in allh})

print("\n=== DOMAIN SIGNATURES (diff vs all-famous baseline; only n>=8) ===")
for d in sorted(dom, key=lambda k: -len(dom[k])):
    if len(dom[d]) < 8 or d == "Other": continue
    pdiff = {pl: np.mean([x[0][pl] for x in dom[d]]) - base_p[pl] for pl in _C}
    hdiff = {h: np.mean([x[1][h] for x in dom[d]]) - base_h[h] for h in allh}
    topp = sorted(pdiff.items(), key=lambda kv: -kv[1])[:3]
    toph = sorted(hdiff.items(), key=lambda kv: -kv[1])[:3]
    print(f"\n  {d} (n={len(dom[d])})")
    print(f"    planets ↑: " + " · ".join(f"{pl} {v:+.1f}" for pl, v in topp))
    print(f"    houses  ↑: " + " · ".join(f"{h}th {v:+.1f}" for h, v in toph))
