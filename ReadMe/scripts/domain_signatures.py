# -*- coding: utf-8 -*-
"""Domain chart-signatures — which planets/houses distinguish each field.

Leave-one-out baseline: each domain is compared to *the other domains*, not the
whole set, so a large field (Cinema) no longer washes out its own signature.
Planet "prominence" = 0.6*dignity + 0.4*angularity; houses = Sarvashtakavarga
bindus (incl. the artistry houses 2/3/5). Run in the API container:

    docker cp ReadMe/scripts/domain_tags.py       vedicjivan-api:/app/domain_tags.py
    docker cp ReadMe/scripts/domain_signatures.py  vedicjivan-api:/app/domain_signatures.py
    docker exec -w /app vedicjivan-api python domain_signatures.py
"""
import json
import numpy as np
from collections import defaultdict
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import _get_dignity
from domain_tags import domain_of

FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8"))
_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55,
       "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}
_ANG = {1, 4, 5, 7, 9, 10}; _DUS = {6, 8, 12}
HOUSES = (1, 2, 3, 5, 9, 10, 11)

def features(p):
    b = p["birth"]
    c = build_muhurta_chart(dob=b["date"], tob=b["time"], lat=b["lat"], lon=b["lon"], with_shadbala=False)
    P, ls = c["planets"], c["lagna"]["sign"]
    prom = {}
    for pl in _C:
        dig = _DP.get(_get_dignity(pl, P[pl]["sign"]), 45)
        h = P[pl]["house"]
        prom[pl] = 0.6 * dig + 0.4 * (100 if h in _ANG else 35 if h in _DUS else 60)
    tv = c["ashtakavarga"]["totals"]
    sav = {h: tv[(ls + h - 1) % 12] for h in HOUSES}
    return prom, sav

by_dom = defaultdict(list); names = defaultdict(list)
for p in FAM:
    d = domain_of(p.get("category"))
    by_dom[d].append(features(p)); names[d].append(p.get("name"))

def mean_planet(rows, pl): return np.mean([r[0][pl] for r in rows])
def mean_house(rows, h): return np.mean([r[1][h] for r in rows])

print("=== DOMAIN SIGNATURES — leave-one-out (domain vs the OTHER fields) ===")
for d in sorted(by_dom, key=lambda k: -len(by_dom[k])):
    if len(by_dom[d]) < 8 or d == "Other":
        continue
    rest = [r for k, rows in by_dom.items() if k != d for r in rows]
    pdiff = {pl: mean_planet(by_dom[d], pl) - mean_planet(rest, pl) for pl in _C}
    hdiff = {h: mean_house(by_dom[d], h) - mean_house(rest, h) for h in HOUSES}
    topp = sorted(pdiff.items(), key=lambda kv: -kv[1])[:3]
    toph = sorted(hdiff.items(), key=lambda kv: -kv[1])[:3]
    print(f"\n  {d} (n={len(by_dom[d])})  e.g. {', '.join(names[d][:4])}")
    print("    planets ↑ " + " · ".join(f"{pl} {v:+.1f}" for pl, v in topp))
    print("    houses  ↑ " + " · ".join(f"{h}th {v:+.1f}" for h, v in toph))
