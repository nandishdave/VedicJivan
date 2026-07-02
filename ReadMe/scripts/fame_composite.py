"""Verified 8-factor fame composite — reproduction script.

Run inside the API container (the Swiss-Ephemeris engine won't import on the host):
    docker cp ReadMe/scripts/fame_composite.py vedicjivan-api:/app/fame_composite.py
    docker exec -w /app vedicjivan-api python fame_composite.py

Reads two chart sets already staged in the container:
    /app/src_celebrities.json   — the 207 famous charts (== src/data/celebrities.json)
    /app/normal_people.json     — the 96 ordinary/control charts

The 8 factors (see ReadMe/methodology.html for the full write-up):
  1 Rahu prime-dasha (20-50) x clean-dispositor factor   [meteoric rise]
  2 D60 crude dignity of the 7 planets                    [soul-level strength]
  3 10th-house Ashtakavarga (career) — the anchor
  4 1st-house Ashtakavarga (self)
  5 Upachaya OCCUPANCY dasha in peak (lord sitting in 3/6/10/11)  [striving]
  6 Late Raja-yoga activation (50-80)                     [status matures late]
  7 Late Dhana-yoga activation (50-80)                    [wealth matures late]
  8 11th-house Ashtakavarga (gains) — 2nd-strongest factor [reaping]

Reports per-factor lift, 5-fold cross-validated AUC (count + sum), and the
confound-matched India-born cuts. Verified result: CV-AUC ~0.644 full set,
0.666 on the cleanest cut (India-born, born >= 1940). D10 dignity was tested
alongside 11th-AV and rejected (solo AUC 0.506, hurt the composite).
"""
import json
import numpy as np
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS, _get_dignity
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha
from app.services.kundli_calculator.divisional import calc_divisional_charts
from app.services.kundli_calculator.raja_yoga import raja_yoga_score
from app.services.kundli_calculator.dhana_yoga import dhana_yoga_score

FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8"))
ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55,
       "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}
_BAD = {3, 6, 8, 12}          # dusthana (dispositor / occupancy penalty)
OCC = {3, 6, 10, 11}          # upachaya / growth-effort houses
FEAT = ["rahu_prime", "d60_dignity", "av_10th", "av_1st", "upa_occ", "raja_late", "dhana_late", "av_11th"]


def _yoga_weights(links):
    """planet -> summed link score, for the planets FORMING a yoga."""
    w = {}
    for lk in links:
        for p in lk.get("planets", []):
            w[p] = w.get(p, 0.0) + lk["score"]
    return w


def _activation(dashas, birth_year, weights, a, b):
    """Year-weighted mean of weights[MD-lord] over the [a, b] age window."""
    tot = acc = 0.0
    for d in dashas:
        ov = max(0, min(int(d["end_date"][:4]) - birth_year, b) - max(int(d["start_date"][:4]) - birth_year, a))
        if ov <= 0:
            continue
        tot += ov
        acc += weights.get(d["planet"], 0.0) * ov
    return acc / tot if tot else 0.0


def feats(dob, tob, lat, lon):
    c = build_muhurta_chart(dob=dob, tob=tob, lat=lat, lon=lon)
    P, lag = c["planets"], c["lagna"]
    ls = lag["sign"]
    by = int(dob[:4])
    dl = calc_vimshottari_dasha(P["Moon"]["longitude"], dob, tob)["dashas"]

    # 1 — Rahu prime-dasha (20-50) x clean dispositor
    ra = next(((int(d["start_date"][:4]) - by, int(d["end_date"][:4]) - by) for d in dl if d["planet"] == "Rahu"), None)
    rahu_years = max(0, min(ra[1], 50) - max(ra[0], 20)) if ra else 0
    dispf = 1.0 if P[SIGN_LORDS[P["Rahu"]["sign"]]]["house"] not in _BAD else 0.4
    rahu_prime = rahu_years * dispf

    # 2 — D60 crude dignity
    D60 = calc_divisional_charts(P, lag)["D60"]
    d60_dignity = float(np.mean([_DP.get(_get_dignity(p, D60[p]), 45) for p in _C]))

    # 3, 4, 8 — Ashtakavarga 10th (career) / 1st (self) / 11th (gains)
    tv = c["ashtakavarga"]["totals"]
    av_10th = tv[(ls + 9) % 12]
    av_1st = tv[ls]
    av_11th = tv[(ls + 10) % 12]

    # 5 — upachaya OCCUPANCY dasha in the peak (20-50)
    tot = occ = 0.0
    for d in dl:
        ov = max(0, min(int(d["end_date"][:4]) - by, 50) - max(int(d["start_date"][:4]) - by, 20))
        if ov <= 0:
            continue
        tot += ov
        if P[d["planet"]]["house"] in OCC:
            occ += ov
    upa_occ = occ / tot if tot else 0.0

    # 6, 7 — late (50-80) Raja / Dhana yoga activation by dasha
    raja_late = _activation(dl, by, _yoga_weights(raja_yoga_score(c)[1]), 50, 80)
    dhana_late = _activation(dl, by, _yoga_weights(dhana_yoga_score(c)[1]), 50, 80)

    india = (68 <= lon <= 98 and 6 <= lat <= 37)
    return [rahu_prime, d60_dignity, av_10th, av_1st, upa_occ, raja_late, dhana_late, av_11th], by, india


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
print(f"\n8-factor composite   count-AUC={c:.3f}  sum-AUC={s:.3f}")

print("\nconfound-matched India-born cuts (sum-AUC):")
for yr in (0, 1940, 1955):
    mask = (FY >= yr) & FI
    Fm = F[mask]
    if len(Fm) < 20:
        continue
    _, sm = cv(Fm, R)
    print(f"  India-born >= {yr:4d}   n_fam={len(Fm):3d}  avg_yr={int(FY[mask].mean())}   sum-AUC={sm:.3f}")
