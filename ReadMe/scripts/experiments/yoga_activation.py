"""Yoga ACTIVATION by dasha across wider adult windows.
Principle: a Raja/Dhana yoga delivers only when the MD of a planet FORMING it
runs. Fame can come after 50 (politicians, businessmen) -> test 20-50 vs 20-70
vs 20-80. For each chart, weight each MD by how strongly its lord participates
in the Raja / Dhana yoga (summed link scores), year-weighted over the window.
Famous(207) vs ordinary(96)."""
import json
import numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha
from app.services.kundli_calculator.raja_yoga import raja_yoga_score
from app.services.kundli_calculator.dhana_yoga import dhana_yoga_score

FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8"))
ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
WINDOWS = [(20, 50), (20, 70), (20, 80), (35, 75)]

def planet_weights(links):
    w = {}
    for lk in links:
        for p in lk.get("planets", []):
            w[p] = w.get(p, 0.0) + lk["score"]
    return w

def feats(dob, tob, lat, lon):
    c = build_muhurta_chart(dob=dob, tob=tob, lat=lat, lon=lon)
    P = c["planets"]; by = int(dob[:4])
    raja_w = planet_weights(raja_yoga_score(c)[1])
    dhana_w = planet_weights(dhana_yoga_score(c)[1])
    dl = calc_vimshottari_dasha(P["Moon"]["longitude"], dob, tob)["dashas"]
    out = []
    for a, b in WINDOWS:
        tot = racc = dacc = 0.0
        for d in dl:
            ov = max(0, min(int(d["end_date"][:4]) - by, b) - max(int(d["start_date"][:4]) - by, a))
            if ov <= 0: continue
            tot += ov; L = d["planet"]
            racc += raja_w.get(L, 0.0) * ov
            dacc += dhana_w.get(L, 0.0) * ov
        out.append(racc / tot if tot else 0.0)   # raja activation in window
        out.append(dacc / tot if tot else 0.0)   # dhana activation in window
    return out

def bd(p): return (p["birth"]["date"], p["birth"]["time"], p["birth"]["lat"], p["birth"]["lon"])
F = np.array([feats(*bd(p)) for p in FAM])
R = np.array([feats(*bd(p)) for p in ORDD])
def auc(pos, neg): return float(np.mean([np.mean(p > neg) + 0.5 * np.mean(p == neg) for p in pos]))

print(f"famous={len(F)}  ordinary={len(R)}\n")
print("Yoga activation by dasha (year-weighted, forming-planet MD) — fam | ord | lift | AUC")
i = 0
for (a, b) in WINDOWS:
    print(f"\n  window {a}-{b}:")
    for name in ("RAJA activation", "DHANA activation"):
        fm, rm = F[:, i].mean(), R[:, i].mean()
        print(f"    {name:18s} {fm:6.3f} {rm:6.3f}  {fm-rm:+6.3f}  AUC={auc(F[:, i], R[:, i]):.3f}")
        i += 1

# combined raja+dhana activation, best window (20-80), + AUC
print("\ncombined RAJA+DHANA activation AUC per window:")
i = 0
for (a, b) in WINDOWS:
    comb_f = F[:, i] + F[:, i + 1]; comb_r = R[:, i] + R[:, i + 1]
    print(f"  window {a}-{b}:  AUC={auc(comb_f, comb_r):.3f}")
    i += 2
