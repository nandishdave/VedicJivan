"""Verified 17-factor fame composite — reproduction script.

Run inside the API container (the Swiss-Ephemeris engine won't import on the host):
    docker cp ReadMe/scripts/fame_composite.py vedicjivan-api:/app/fame_composite.py
    docker exec -w /app vedicjivan-api python fame_composite.py

Reads two chart sets already staged in the container:
    /app/src_celebrities.json   — the 225 famous charts (== src/data/celebrities.json)
    /app/normal_people.json     — the 96 ordinary/control charts

SINGLE SOURCE OF TRUTH (M1, 2026-07-05): the 17-factor math lives ONLY in
``worldly_potential.factor_values`` — this script imports and calls it rather than
reimplementing the factors (the two copies used to be hand-kept in lockstep and
could silently drift, invalidating the baked REF calibration). This file is now
just the CV harness (per-factor lift, 5-fold cross-validated AUC, confound-matched
cuts) running on top of the production factor values.

The 17 factors (see ReadMe/methodology.html for the full write-up):
  1 Rahu prime-dasha (20-50) x clean-dispositor factor   [meteoric rise]
  2 Vimśopaka bala — mean dignity of the 7 planets across the 16 Shodashavarga
     divisionals (weights sum 20; D60/D1/D9 dominant)     [cross-varga strength]
  3 10th-house Ashtakavarga (career) — the anchor
  4 1st-house Ashtakavarga (self)
  5 Upachaya OCCUPANCY dasha in peak (lord sitting in 3/6/10/11)  [striving]
  6 Late Raja-yoga activation (50-80)                     [status matures late]
  7 Late Dhana-yoga activation (50-80)                    [wealth matures late]
  8 11th-house Ashtakavarga (gains)                        [reaping]
  9 Bright Moon (Shukla-7..Krishna-7, elongation 72-264°) [lunar strength]
 10 Moon-sign dispositor in the 1st/2nd/11th/12th house   [public persona]
 11 Moon-sign's own Sarvashtakavarga bindus               [weakest of the Moon 3]
 12 Sun-sign dispositor in the 1st quadrant (houses 1-4)  [self/status]
 13 Positive Shadbala-weighted argala on the 2/10/12 houses [Jaimini intervention]
 14 Born in a Pūrṇa tithi (5th/10th/15th — the "full/complete" group) [pañchāṅga]
 15 Mean Dig Bala of the lagna-lord and 10th-lord         [directional strength]
 16 Strongest-Vimsopaka planet (any graha) seated in {1,2,4,5,11} [concentration]
 17 (# of 9 bodies in a Mridu nakshatra) - (# in a Tikshna nakshatra) [nakshatra quality]

Reports per-factor lift, 5-fold cross-validated AUC (count + sum), and the
confound-matched India-born cuts. Verified result: CV-AUC ~0.74 full set,
0.78 on the cleanest cut (India-born, born >= 1940). The Moon bundle (9-11)
lifted the 8-factor 0.644 -> 0.680; the Sun dispositor (12) 0.686 -> 0.703;
the positive argala (13) 0.703 -> 0.724; the Pūrṇa tithi (14) 0.724 -> 0.732;
then two *strength* upgrades (2026-07): swapping crude D60 for the full
Shodashavarga Vimśopaka bala (factor 2) and adding the lagna/10th-lord Dig Bala
(factor 15) lifted 0.732 -> 0.751 full and 0.759 -> 0.789 on the clean cut
(all seed-stable). Yogakāraka strength, house-lord total Shadbala, and the
Indu/Sree Lagna special points were tested and rejected; D10, date numerology,
dasha-timing, and the Pañchāṅga Nitya-yoga were rejected earlier.
"""
import json
import numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha
# The 17-factor math — the ONE source of truth (see module docstring). This script
# no longer reimplements the factors; it sources them from production.
from app.services.kundli_calculator.worldly_potential import factor_values

FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8"))
ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
FEAT = ["rahu_prime", "vimsopaka", "av_10th", "av_1st", "upa_occ", "raja_late", "dhana_late", "av_11th",
        "bright_moon", "moon_disp", "moon_sav", "sun_disp", "argala_pos", "purna_tithi", "dig_lords",
        "top_vim_seat", "nak_mridu_net"]


def feats(dob, tob, lat, lon):
    """The 17 factor values for one chart, sourced from worldly_potential (the
    single source of truth), plus the birth year and the India-born flag."""
    c = build_muhurta_chart(dob=dob, tob=tob, lat=lat, lon=lon, with_shadbala=True)
    by = int(dob[:4])
    dl = calc_vimshottari_dasha(c["planets"]["Moon"]["longitude"], dob, tob)["dashas"]
    fv = factor_values(c, dl, by)
    india = (68 <= lon <= 98 and 6 <= lat <= 37)
    return [fv[k] for k in FEAT], by, india


def _bd(p):
    return (p["birth"]["date"], p["birth"]["time"], p["birth"]["lat"], p["birth"]["lon"])


FR = [feats(*_bd(p)) for p in FAM]
RR = [feats(*_bd(p)) for p in ORDD]
F = np.array([x[0] for x in FR])
R = np.array([x[0] for x in RR])
FY = np.array([x[1] for x in FR])
FI = np.array([x[2] for x in FR])


def auc(scores, labels):
    pos = scores[labels == 1]
    neg = scores[labels == 0]
    return float(np.mean([np.mean(p > neg) + 0.5 * np.mean(p == neg) for p in pos]))


def cv(Xf, Xr):
    """5-fold CV; sign + z-scaling learned on train, scored on held-out. Returns (count-AUC, sum-AUC)."""
    X = np.vstack([Xf, Xr])
    y = np.array([1] * len(Xf) + [0] * len(Xr), float)
    np.random.seed(7)
    idx = np.random.permutation(len(y))
    folds = np.array_split(idx, 5)
    cvc = np.zeros(len(y))
    cvs = np.zeros(len(y))
    for i in range(5):
        te = folds[i]
        tr = np.concatenate([folds[j] for j in range(5) if j != i])
        sg = np.sign(X[tr][y[tr] == 1].mean(0) - X[tr][y[tr] == 0].mean(0))
        m, s = X[tr].mean(0), X[tr].std(0) + 1e-9
        Z = ((X[te] - m) / s) * sg
        cvc[te] = (Z > 0).sum(1)
        cvs[te] = Z.sum(1)
    return auc(cvc, y), auc(cvs, y)


print(f"famous={len(F)}  ordinary={len(R)}\nper-factor lift (famous | ordinary | diff):")
for i, n in enumerate(FEAT):
    print(f"  {n:12} {F[:, i].mean():7.2f} {R[:, i].mean():7.2f}  {F[:, i].mean() - R[:, i].mean():+6.2f}")

c, s = cv(F, R)
print(f"\n17-factor composite   count-AUC={c:.3f}  sum-AUC={s:.3f}")

print("\nconfound-matched India-born cuts (sum-AUC):")
for yr in (0, 1940, 1955):
    mask = (FY >= yr) & FI
    Fm = F[mask]
    if len(Fm) < 20:
        continue
    _, sm = cv(Fm, R)
    print(f"  India-born >= {yr:4d}   n_fam={len(Fm):3d}  avg_yr={int(FY[mask].mean())}   sum-AUC={sm:.3f}")
