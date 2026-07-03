"""Worldly-Potential — the validated 12-factor "fame-tilt" composite as a 0-100
readout for a single chart.

This is the productionised form of the fame-signal study (see
``ReadMe/methodology.html`` and ``ReadMe/scripts/fame_composite.py``): across
225 famous vs 96 ordinary charts the 14 factors below reached a cross-validated
AUC ≈ 0.73 (0.76 on the cleanest confound-free cut). It is a *faint* tilt, not
a fame predictor — surface it as worldly-potential, never as destiny.

Distinct from ``fame.py`` (the weaker Yaśa heuristic). The 14 factors:
  1 rahu_prime  — Rahu Mahadasha years in ages 20-50 × clean-dispositor factor
  2 d60         — average dignity of the 7 classical planets in the D60
  3 av_10th     — Sarvashtakavarga bindus on the 10th (career) — the anchor
  4 av_1st      — SAV bindus on the 1st (self) — near-noise, leans slightly
                  ordinary; kept for fidelity to the validated model
  5 upa_occ     — peak-years (20-50) under a dasha lord SITTING in 3/6/10/11
  6 raja_late   — years 50-80 under the Mahadasha of a Raja-yoga-forming planet
  7 dhana_late  — years 50-80 under the Mahadasha of a Dhana-yoga-forming planet
  8 av_11th     — Sarvashtakavarga bindus on the 11th (gains) — 2nd-strongest
  ── the Moon bundle (added 2026-07, a lunar dimension independent of the above) ──
  9 bright_moon — Moon in the bright half (Shukla-7..Krishna-7 = elongation 72-264°)
 10 moon_disp   — the Moon-sign's dispositor sits in the 1st/2nd/11th/12th (public-presence)
 11 moon_sav    — the Moon-sign's own Sarvashtakavarga bindus (weakest of the three)
 12 sun_disp    — the Sun-sign's dispositor sits in the 1st quadrant (houses 1-4);
                  the 1st house alone is ~6× more common in famous (17.8% vs 3.1%)
  ── argala (added 2026-07, a Jaimini intervention dimension) ──
 13 argala_pos  — positive (śubha) Shadbala-weighted argala on the 2nd/10th/12th
                  houses from Lagna: benefics intervening (from the 2/4/5/11)
                  on wealth/career/foreign houses, unobstructed by their virodha
                  (12/10/9/3) counter. Solo AUC 0.60; lifts the composite
                  0.70 -> 0.72 (nested-validated). Needs ``chart['shadbala']``.
  ── pañchāṅga (added 2026-07) ──
 14 purna_tithi — born in a Pūrṇa tithi (5th/10th/15th of either paksha — the
                  "full/complete" pañcha-tithi group). Famous 22.7% vs ordinary
                  11.5% (~2×); nested-validated (Pūrṇa picked in all 5 folds,
                  honest = in-sample 0.732) and independent of bright_moon
                  (corr −0.07 — separates in both bright and dark subsets).

Because the composite is a *relative* (z-scored) model, we bake the 303-chart
reference distribution ``REF = {factor: (famous_mean, ordinary_mean, pooled_std)}``
so a single chart can be scored without a runtime population. Each factor is
z-scored against its midpoint, oriented famous-positive, averaged, and squashed
to 0-100. REF is a calibration snapshot — regenerate it if the study set changes.
"""
from __future__ import annotations

import math

_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55,
       "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}
_BAD = {3, 6, 8, 12}        # dusthana — dispositor / occupancy penalty
_OCC = {3, 6, 10, 11}       # upachaya / growth-effort houses
# Argala (factor 13): all 9 grahas participate; benefics (J/V/Me, bright Moon)
# intervene positively. ARG_PAIRS = (argala house Nth-from-R, its virodha Nth-from-R);
# an argala is "effective" only if it outweighs its virodha counter. ARG_HOUSES
# are the reference houses (from Lagna) the study isolated as fame-bearing.
_ARG_PLANETS = _C + ["Rahu", "Ketu"]
_ARG_PAIRS = ((2, 12), (4, 10), (5, 9), (11, 3))
_ARG_HOUSES = (2, 10, 12)

# Calibration snapshot from the 303-chart study (fame_composite.py):
# factor -> (famous_mean, ordinary_mean, pooled_std over all 303 charts).
REF = {
    "rahu_prime": (5.2406, 4.0625, 6.4857),
    "d60":        (50.8903, 49.4494, 9.5252),
    "av_10th":    (31.9324, 29.8229, 4.6999),
    "av_1st":     (28.8502, 29.1875, 4.2607),
    "upa_occ":    (0.3649, 0.3056, 0.3157),
    "raja_late":  (1.7283, 1.4760, 1.7269),
    "dhana_late": (0.6001, 0.3574, 1.0889),
    "av_11th":    (32.4010, 30.8854, 4.4462),
    "bright_moon":  (0.5467, 0.4271, 0.5007),
    "moon_disp":    (0.4844, 0.3021, 0.4958),
    "moon_sav":     (27.5911, 27.1562, 4.7677),
    "sun_disp":     (0.4311, 0.2188, 0.4829),
    "argala_pos":   (781.0587, 604.2046, 495.3215),
    "purna_tithi":  (0.2267, 0.1146, 0.3954),
}
_ARGALA_MID = (REF["argala_pos"][0] + REF["argala_pos"][1]) / 2.0  # neutral fallback
_SQUASH_K = 2.2  # logistic steepness: mean-z 0 -> 50, +0.5 -> ~75, -0.5 -> ~25. Tunable.

NOTE = ("A faint statistical tilt (AUC ~0.63) toward markers seen in prominent "
        "charts — most of worldly success lives outside the chart. Treat as "
        "potential, not destiny.")


def _pw(links: list[dict]) -> dict:
    """planet -> summed link score, over the planets FORMING a yoga."""
    w: dict[str, float] = {}
    for lk in links:
        for p in lk.get("planets", []):
            w[p] = w.get(p, 0.0) + lk["score"]
    return w


def _activation(dashas: list[dict], birth_year: int, weights: dict, a: int, b: int) -> float:
    """Year-weighted mean of weights[MD-lord] over the [a, b] age window."""
    tot = acc = 0.0
    for d in dashas:
        ov = max(0, min(int(d["end_date"][:4]) - birth_year, b) - max(int(d["start_date"][:4]) - birth_year, a))
        if ov <= 0:
            continue
        tot += ov
        acc += weights.get(d["planet"], 0.0) * ov
    return acc / tot if tot else 0.0


def _positive_argala(chart: dict, bright_moon: float) -> float:
    """Factor 13 — positive (śubha) Shadbala-weighted argala on the 2/10/12
    houses from Lagna. Benefics (J/V/Me + bright Moon) in a house's 2/4/5/11
    intervene on it; the intervention counts only if it outweighs the virodha
    (12/10/9/3) counter. Returns the neutral REF midpoint if Shadbala is absent
    (the weighting is what carries the signal — the count-only version is flat)."""
    sb = chart.get("shadbala") or {}
    if not sb:
        return _ARGALA_MID
    P = chart["planets"]
    benefic = {"Jupiter": 1, "Venus": 1, "Mercury": 1, "Moon": (1 if bright_moon else -1),
               "Sun": -1, "Mars": -1, "Saturn": -1, "Rahu": -1, "Ketu": -1}
    svals = [sb[q]["total_shadbala"] for q in _C if q in sb]
    avg = sum(svals) / len(svals) if svals else 1.0
    wt = {q: (sb[q]["total_shadbala"] if q in sb else avg) for q in _ARG_PLANETS}
    by_house: dict[int, list[str]] = {h: [] for h in range(1, 13)}
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


def factor_values(chart: dict, dashas: list[dict], birth_year: int) -> dict:
    """The 14 raw factor values for a chart. Pure; mirrors fame_composite.py."""
    from app.services.kundli_calculator._core import SIGN_LORDS, _get_dignity
    from app.services.kundli_calculator.divisional import calc_divisional_charts
    from app.services.kundli_calculator.raja_yoga import raja_yoga_score
    from app.services.kundli_calculator.dhana_yoga import dhana_yoga_score

    P, lag = chart["planets"], chart["lagna"]
    ls = lag["sign"]

    # 1 — Rahu prime-dasha (20-50) × clean dispositor
    ra = next(((int(d["start_date"][:4]) - birth_year, int(d["end_date"][:4]) - birth_year)
               for d in dashas if d["planet"] == "Rahu"), None)
    rahu_years = max(0, min(ra[1], 50) - max(ra[0], 20)) if ra else 0
    dispf = 1.0 if P[SIGN_LORDS[P["Rahu"]["sign"]]]["house"] not in _BAD else 0.4
    rahu_prime = rahu_years * dispf

    # 2 — D60 crude dignity (reuse cached divisional if present)
    d60 = (chart.get("divisional") or calc_divisional_charts(P, lag))["D60"]
    d60_dignity = sum(_DP.get(_get_dignity(p, d60[p]), 45) for p in _C) / len(_C)

    # 3, 4, 8 — Ashtakavarga 10th (career) / 1st (self) / 11th (gains)
    tv = chart["ashtakavarga"]["totals"]
    av_10th, av_1st, av_11th = tv[(ls + 9) % 12], tv[ls], tv[(ls + 10) % 12]

    # 5 — upachaya OCCUPANCY dasha in the peak (20-50)
    tot = occ = 0.0
    for d in dashas:
        ov = max(0, min(int(d["end_date"][:4]) - birth_year, 50) - max(int(d["start_date"][:4]) - birth_year, 20))
        if ov <= 0:
            continue
        tot += ov
        if P[d["planet"]]["house"] in _OCC:
            occ += ov
    upa_occ = occ / tot if tot else 0.0

    # 6, 7 — late (50-80) Raja / Dhana yoga activation by dasha
    raja_late = _activation(dashas, birth_year, _pw(raja_yoga_score(chart)[1]), 50, 80)
    dhana_late = _activation(dashas, birth_year, _pw(dhana_yoga_score(chart)[1]), 50, 80)

    # 9, 10, 11 — the Moon bundle (a lunar dimension, independent of the houses above)
    ms = P["Moon"]["sign"]
    elong = (P["Moon"]["longitude"] - P["Sun"]["longitude"]) % 360
    bright_moon = 1.0 if 72 <= elong <= 264 else 0.0        # Shukla-7 .. Krishna-7 (bright half)
    moon_disp = 1.0 if P[SIGN_LORDS[ms]]["house"] in (1, 2, 11, 12) else 0.0  # Moon-lord in a public-presence house
    moon_sav = tv[ms]                                        # the Moon-sign's own SAV bindus
    # 12 — Sun-sign dispositor in the first quadrant (self/valor/foundation houses)
    ss = P["Sun"]["sign"]
    sun_disp = 1.0 if P[SIGN_LORDS[ss]]["house"] in (1, 2, 3, 4) else 0.0

    # 13 — positive Shadbala-weighted argala on the 2nd/10th/12th (fame houses)
    argala_pos = _positive_argala(chart, bright_moon)

    # 14 — born in a Pūrṇa tithi (5th/10th/15th of either paksha). Tithi from the
    # Moon-Sun elongation; the pañcha-tithi group is (tithi-1) mod 5 (4 = Pūrṇa).
    tithi = int(elong / 12) + 1                      # 1..30
    purna_tithi = 1.0 if (tithi - 1) % 5 == 4 else 0.0

    return {"rahu_prime": rahu_prime, "d60": d60_dignity, "av_10th": av_10th,
            "av_1st": av_1st, "upa_occ": upa_occ, "raja_late": raja_late,
            "dhana_late": dhana_late, "av_11th": av_11th,
            "bright_moon": bright_moon, "moon_disp": moon_disp, "moon_sav": moon_sav,
            "sun_disp": sun_disp, "argala_pos": argala_pos, "purna_tithi": purna_tithi}


def worldly_potential(chart: dict) -> dict | None:
    """0-100 worldly-potential readout for a chart. Self-sufficient: computes
    Vimshottari dashas from ``chart['dob']``/``['tob']`` (or reuses ``chart['dashas']``)
    and D60 from ``chart['divisional']`` (or recomputes). Returns ``None`` when the
    chart lacks a birth date (the dasha factors can't be timed) so callers can
    gracefully drop the layer.

    Returns ``{"score", "mean_z", "factors": {name: {value, z}}, "note"}``.
    """
    dob = chart.get("dob")
    if not dob:
        return None
    birth_year = int(dob[:4])
    dashas = chart.get("dashas")
    if dashas is None:
        from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha
        dashas = calc_vimshottari_dasha(chart["planets"]["Moon"]["longitude"], dob, chart.get("tob", "12:00"))["dashas"]

    return score_from_factors(factor_values(chart, dashas, birth_year))


def score_from_factors(raw: dict) -> dict:
    """Map the 14 raw factor values to a 0-100 worldly-potential readout: z-score
    each against its REF midpoint, orient famous-positive, average, squash. Pure —
    the deterministic core, split out for testing."""
    zs = {}
    for k, (fam, ordm, std) in REF.items():
        mid = (fam + ordm) / 2.0
        orient = 1.0 if fam >= ordm else -1.0
        zs[k] = orient * (raw[k] - mid) / std if std else 0.0
    mean_z = sum(zs.values()) / len(zs)
    score = 100.0 / (1.0 + math.exp(-_SQUASH_K * mean_z))
    return {
        "score": round(score, 1),
        "mean_z": round(mean_z, 3),
        "factors": {k: {"value": round(raw[k], 2), "z": round(zs[k], 2)} for k in raw},
        "note": NOTE,
    }
