"""Verified 16-factor fame composite — reproduction script.

Run inside the API container (the Swiss-Ephemeris engine won't import on the host):
    docker cp ReadMe/scripts/fame_composite.py vedicjivan-api:/app/fame_composite.py
    docker exec -w /app vedicjivan-api python fame_composite.py

Reads two chart sets already staged in the container:
    /app/src_celebrities.json   — the 225 famous charts (== src/data/celebrities.json)
    /app/normal_people.json     — the 96 ordinary/control charts

The 16 factors (see ReadMe/methodology.html for the full write-up):
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
# Factor 2 (Vimśopaka bala) — the 16 Shodashavarga vargas with classical weights (sum 20).
_VARGA_W = {"D1": 3.5, "D2": 1.0, "D3": 1.0, "D4": 0.5, "D7": 0.5, "D9": 3.0, "D10": 0.5,
            "D12": 0.5, "D16": 2.0, "D20": 0.5, "D24": 0.5, "D27": 0.5, "D30": 1.0,
            "D40": 0.5, "D45": 0.5, "D60": 4.0}
FEAT = ["rahu_prime", "vimsopaka", "av_10th", "av_1st", "upa_occ", "raja_late", "dhana_late", "av_11th",
        "bright_moon", "moon_disp", "moon_sav", "sun_disp", "argala_pos", "purna_tithi", "dig_lords",
        "top_vim_seat"]

# Factor 13 — positive Shadbala-weighted argala on the 2/10/12 houses (from Lagna)
_ARG_PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
_ARG_PAIRS = ((2, 12), (4, 10), (5, 9), (11, 3))   # (argala Nth-from-R, virodha Nth-from-R)
_ARG_HOUSES = (2, 10, 12)


def _positive_argala(P, shadbala, bright_moon):
    """Śubha (benefic) argala on 2/10/12, Shadbala-weighted, effective only when
    it outweighs the virodha counter (12/10/9/3)."""
    if not shadbala:
        return 0.0
    benefic = {"Jupiter": 1, "Venus": 1, "Mercury": 1, "Moon": (1 if bright_moon else -1),
               "Sun": -1, "Mars": -1, "Saturn": -1, "Rahu": -1, "Ketu": -1}
    svals = [shadbala[q]["total_shadbala"] for q in _C if q in shadbala]
    avg = sum(svals) / len(svals) if svals else 1.0
    wt = {q: (shadbala[q]["total_shadbala"] if q in shadbala else avg) for q in _ARG_PLANETS}
    by_house = {h: [] for h in range(1, 13)}
    for p in _ARG_PLANETS:
        by_house[P[p]["house"]].append(p)
    total = 0.0
    for R in _ARG_HOUSES:
        for na, nv in _ARG_PAIRS:
            A = ((R - 1 + na - 1) % 12) + 1
            V = ((R - 1 + nv - 1) % 12) + 1
            if sum(wt[p] for p in by_house[A]) > sum(wt[p] for p in by_house[V]):
                s = sum(wt[p] * benefic[p] for p in by_house[A])
                if s > 0:
                    total += s
    return total


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
    c = build_muhurta_chart(dob=dob, tob=tob, lat=lat, lon=lon, with_shadbala=True)
    P, lag = c["planets"], c["lagna"]
    ls = lag["sign"]
    by = int(dob[:4])
    dl = calc_vimshottari_dasha(P["Moon"]["longitude"], dob, tob)["dashas"]

    # 1 — Rahu prime-dasha (20-50) x clean dispositor
    ra = next(((int(d["start_date"][:4]) - by, int(d["end_date"][:4]) - by) for d in dl if d["planet"] == "Rahu"), None)
    rahu_years = max(0, min(ra[1], 50) - max(ra[0], 20)) if ra else 0
    dispf = 1.0 if P[SIGN_LORDS[P["Rahu"]["sign"]]]["house"] not in _BAD else 0.4
    rahu_prime = rahu_years * dispf

    # 2 — Vimśopaka bala: mean cross-divisional strength of the 7 planets over 16 vargas
    varga = calc_divisional_charts(P, lag)
    vim_pp = {}
    for p in _C:
        tot_p = 0.0
        for vname, vw in _VARGA_W.items():
            vsign = P[p]["sign"] if vname == "D1" else varga[vname][p]
            tot_p += vw * (_DP.get(_get_dignity(p, vsign), 45) / 100.0)
        vim_pp[p] = tot_p
    vimsopaka = sum(vim_pp.values()) / len(_C)

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

    # 9, 10, 11 — the Moon bundle (lunar dimension, independent of the houses above)
    ms = P["Moon"]["sign"]
    elong = (P["Moon"]["longitude"] - P["Sun"]["longitude"]) % 360
    bright_moon = 1.0 if 72 <= elong <= 264 else 0.0
    moon_disp = 1.0 if P[SIGN_LORDS[ms]]["house"] in (1, 2, 11, 12) else 0.0
    moon_sav = tv[ms]
    sun_disp = 1.0 if P[SIGN_LORDS[P["Sun"]["sign"]]]["house"] in (1, 2, 3, 4) else 0.0

    # 13 — positive Shadbala-weighted argala on the 2nd/10th/12th houses
    argala_pos = _positive_argala(P, c.get("shadbala", {}), bright_moon)

    # 14 — born in a Pūrṇa tithi (5th/10th/15th of either paksha)
    tithi = int(((P["Moon"]["longitude"] - P["Sun"]["longitude"]) % 360) / 12) + 1
    purna_tithi = 1.0 if (tithi - 1) % 5 == 4 else 0.0

    # 15 — mean Dig Bala of the lagna-lord and 10th-lord (rulers of self & career)
    sb = c.get("shadbala", {})
    lords = (SIGN_LORDS[ls], SIGN_LORDS[(ls + 9) % 12])
    dvals = [sb[q]["dig_bala"] for q in lords if q in sb and "dig_bala" in sb[q]]
    dig_lords = float(np.mean(dvals)) if dvals else 30.0

    # 16 — strongest-Vimśopaka planet (any graha) seated in a prominence house {1,2,4,5,11}
    top_graha = max(_C, key=lambda q: vim_pp[q])
    top_vim_seat = 1.0 if P[top_graha]["house"] in (1, 2, 4, 5, 11) else 0.0

    india = (68 <= lon <= 98 and 6 <= lat <= 37)
    return [rahu_prime, vimsopaka, av_10th, av_1st, upa_occ, raja_late, dhana_late, av_11th,
            bright_moon, moon_disp, moon_sav, sun_disp, argala_pos, purna_tithi, dig_lords,
            top_vim_seat], by, india


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
print(f"\n16-factor composite   count-AUC={c:.3f}  sum-AUC={s:.3f}")

print("\nconfound-matched India-born cuts (sum-AUC):")
for yr in (0, 1940, 1955):
    mask = (FY >= yr) & FI
    Fm = F[mask]
    if len(Fm) < 20:
        continue
    _, sm = cv(Fm, R)
    print(f"  India-born >= {yr:4d}   n_fam={len(Fm):3d}  avg_yr={int(FY[mask].mean())}   sum-AUC={sm:.3f}")
