# -*- coding: utf-8 -*-
"""Do the mahadashas a person lives through rule the CAREER houses of their D10?
For each dasha-lord (nodes via their D10 dispositor), which D10 houses does it
rule? Year-weighted over life windows. Famous(207) vs ordinary(96). Fast."""
import json
import numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha
from app.services.kundli_calculator.divisional import calc_divisional_charts

FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8"))
ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
_C = {"Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"}
KENDRA = {1, 4, 7, 10}; TRIKONA = {1, 5, 9}; DUST = {6, 8, 12}
QUAL = {1: 90, 10: 100, 4: 70, 7: 70, 5: 80, 9: 80, 2: 60, 11: 60, 3: 40, 6: 20, 8: 20, 12: 20}

def metrics(p, a, b):
    bb = p["birth"]
    c = build_muhurta_chart(dob=bb["date"], tob=bb["time"], lat=bb["lat"], lon=bb["lon"], with_shadbala=False)
    P, lag = c["planets"], c["lagna"]; by = int(bb["date"][:4])
    D10 = calc_divisional_charts(P, lag)["D10"]; d10lag = D10["Lagna"]
    def houses_ruled(planet):
        return [h for h in range(1, 13) if SIGN_LORDS[(d10lag + h - 1) % 12] == planet]
    dl = calc_vimshottari_dasha(P["Moon"]["longitude"], bb["date"], bb["time"])["dashas"]
    tot = 0.0; f10 = fk = ft = fd = 0.0; qacc = 0.0
    for d in dl:
        ov = max(0, min(int(d["end_date"][:4]) - by, b) - max(int(d["start_date"][:4]) - by, a))
        if ov <= 0: continue
        lord = d["planet"]
        eff = lord if lord in _C else SIGN_LORDS[D10[lord]]   # node acts through D10 dispositor
        hs = houses_ruled(eff)
        if not hs: continue
        tot += ov
        if 10 in hs: f10 += ov
        if any(h in KENDRA for h in hs): fk += ov
        if any(h in TRIKONA for h in hs): ft += ov
        if any(h in DUST for h in hs): fd += ov
        qacc += max(QUAL[h] for h in hs) * ov
    if not tot: return None
    return (f10 / tot, fk / tot, ft / tot, fd / tot, qacc / tot)

def collect(rows, a, b):
    return np.array([m for p in rows if (m := metrics(p, a, b))])

def auc(fa, ra):
    return float(np.mean([np.mean(x > ra) + 0.5 * np.mean(x == ra) for x in fa]))

LABELS = ["rules D10 10th", "rules D10 kendra", "rules D10 trikona", "rules D10 dusthana", "D10 career-quality"]
for (a, b) in [(20, 50), (0, 60)]:
    F = collect(FAM, a, b); R = collect(ORDD, a, b)
    print(f"\n=== window {a}-{b}  (famous n={len(F)}, ordinary n={len(R)}) — year-weighted ===")
    print(f"  {'metric':22} {'famous':>8} {'ordinary':>9} {'diff':>7} {'AUC':>6}")
    for i, lab in enumerate(LABELS):
        fa, ra = F[:, i], R[:, i]
        unit = "" if i == 4 else "%"
        sc = 1 if i == 4 else 100
        print(f"  {lab:22} {fa.mean()*sc:7.2f}{unit} {ra.mean()*sc:7.2f}{unit} {(fa.mean()-ra.mean())*sc:+6.2f} {auc(fa, ra):.3f}")
