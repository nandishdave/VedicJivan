"""Peak-period (ages 20-50) dasha PLACEMENT study — not strength.
For each chart, year-weighted over 20-50, which HOUSE does the running
mahadasha lord occupy? Compare famous(207) vs ordinary(96): per-house
fraction of peak time, house-group fractions, and a house-quality AUC.
House = the house the dasha lord OCCUPIES (works for Rahu/Ketu too)."""
import json
import numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha

FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8"))
ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
KENDRA = {1, 4, 7, 10}; TRIKONA = {1, 5, 9}; DUSTHANA = {6, 8, 12}; UPACHAYA = {3, 6, 10, 11}

def profile(dob, tob, lat, lon):
    c = build_muhurta_chart(dob=dob, tob=tob, lat=lat, lon=lon); P = c["planets"]
    by = int(dob[:4]); house_yrs = np.zeros(13); tot = 0.0
    for d in calc_vimshottari_dasha(P["Moon"]["longitude"], dob, tob)["dashas"]:
        ov = max(0, min(int(d["end_date"][:4]) - by, 50) - max(int(d["start_date"][:4]) - by, 20))
        if ov <= 0: continue
        h = P[d["planet"]]["house"]; house_yrs[h] += ov; tot += ov
    return house_yrs[1:] / tot if tot else np.zeros(12)  # fraction per house 1..12

def bd(p): return (p["birth"]["date"], p["birth"]["time"], p["birth"]["lat"], p["birth"]["lon"])
F = np.array([profile(*bd(p)) for p in FAM])   # (207,12)
R = np.array([profile(*bd(p)) for p in ORDD])  # (96,12)

print(f"famous={len(F)}  ordinary={len(R)}\n")
print("Fraction of peak (20-50) years under a dasha lord in each HOUSE:")
print("  house   famous  ordinary   diff")
for h in range(12):
    fm, rm = F[:, h].mean(), R[:, h].mean()
    star = "  <--" if abs(fm - rm) > 0.02 else ""
    print(f"  {h+1:2d}      {fm:6.3f}   {rm:6.3f}   {fm-rm:+6.3f}{star}")

def grp(idxs, arr): return arr[:, [i - 1 for i in idxs]].sum(1)
print("\nHouse-GROUP fraction of peak years (famous | ordinary | diff):")
for name, g in [("Kendra 1/4/7/10", KENDRA), ("Trikona 1/5/9", TRIKONA),
                ("10th only", {10}), ("11th only", {11}),
                ("Dusthana 6/8/12", DUSTHANA), ("Upachaya 3/6/10/11", UPACHAYA)]:
    fm, rm = grp(g, F).mean(), grp(g, R).mean()
    print(f"  {name:20s} {fm:6.3f}   {rm:6.3f}   {fm-rm:+6.3f}")

# house-quality score: fame-weighted, then AUC
W = {10: 3.0, 11: 2.5, 1: 2.0, 9: 2.0, 5: 1.5, 4: 1.0, 7: 1.0, 2: 1.0, 3: 0.5, 6: -1.0, 8: -1.5, 12: -1.0}
w = np.array([W[h] for h in range(1, 13)])
def auc(pos, neg): return float(np.mean([np.mean(p > neg) + 0.5 * np.mean(p == neg) for p in pos]))
Fs, Rs = F @ w, R @ w
print(f"\nHouse-quality score (fame-weighted placement):")
print(f"  famous mean = {Fs.mean():.3f}   ordinary mean = {Rs.mean():.3f}   lift = {Fs.mean()-Rs.mean():+.3f}")
print(f"  factor AUC  = {auc(Fs, Rs):.3f}")

# also a plain (kendra+trikona+11) minus dusthana score
simple = (grp(KENDRA | TRIKONA | {11}, F) - grp(DUSTHANA, F)), (grp(KENDRA | TRIKONA | {11}, R) - grp(DUSTHANA, R))
print(f"\nSimple (kendra+trikona+11 − dusthana) fraction:")
print(f"  famous mean = {simple[0].mean():.3f}   ordinary mean = {simple[1].mean():.3f}   lift = {simple[0].mean()-simple[1].mean():+.3f}")
print(f"  factor AUC  = {auc(simple[0], simple[1]):.3f}")
