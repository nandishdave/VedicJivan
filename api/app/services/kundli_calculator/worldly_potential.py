"""Worldly-Potential — the validated 18-factor "fame-tilt" composite as a 0-100
readout for a single chart.

This is the productionised form of the fame-signal study (see
``ReadMe/methodology.html`` and ``ReadMe/scripts/fame_composite.py``): across
225 famous vs 96 ordinary charts the 18 factors below reached a cross-validated
AUC ≈ 0.77 (0.82 on the cleanest confound-free cut). It is a *faint* tilt, not
a fame predictor — surface it as worldly-potential, never as destiny.

Distinct from ``fame.py`` (the weaker Yaśa heuristic). The 18 factors:
  1 rahu_prime  — Rahu Mahadasha years in ages 20-50 × clean-dispositor factor
  2 vimsopaka   — mean Vimśopaka bala of the 7 planets across the 16 Shodashavarga
                  divisionals (weights sum 20; D60/D1/D9 dominant). "Does the chart's
                  strength hold across the vargas?" — replaced the old crude single-
                  varga D60 dignity (solo AUC 0.54 → 0.61; lifts the clean cut ~1.6pts)
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
  ── digbala (added 2026-07, a directional-strength dimension) ──
 15 dig_lords   — mean Dig Bala (directional strength) of the lagna-lord and the
                  10th-lord: the rulers of the *self* and the *career* able to act
                  with full force in their power direction. Solo AUC 0.57, ~zero
                  correlation with every existing factor (genuinely orthogonal), so
                  it lifts the composite where strength-of-placement could not. NB:
                  the luminaries' OWN digbala (Sun/Mars) was REVERSED — it is the
                  *lords'* directional strength, not the karakas', that marks fame.
                  Needs ``chart['shadbala']``.
  ── concentration (added 2026-07) ──
 16 top_vim_seat — the chart's single strongest-Vimśopaka planet (any graha) seated
                  in a prominence house {1,2,4,5,11} (self/wealth/home/creativity/gains).
                  A per-house sweep found 1/2/11 the clear winners (2nd +11.7%) with 4/5
                  marginal; the 10th is REVERSED (excluded). It is the *seat* that matters,
                  not whether the strong planet is a benefic (functional-benefic restriction
                  reverses the signal). Solo AUC 0.60; nested floor +0.005.
  ── nakṣatra quality (added 2026-07) ──
 17 nak_mridu_net  — (# of the 9 bodies in a Mṛidu/tender nakṣatra) − (# in a Tikshna/
                  dreadful one). Mṛidu = Mṛigaśira/Chitra/Anurādhā/Revatī (gentle, artistic);
                  Tikshna = Ārdrā/Āśleṣā/Jyeṣṭhā/Mūla (sharp, severing). Famous lean Mṛidu,
                  ordinary lean Tikshna — the signal STRENGTHENS under era-matching (solo
                  0.62 clean cut). The most marginal factor: acid-test-neutral (+0.001), but
                  seed-stable on the confound-matched cuts (+0.013). The two-sided net is
                  more robust than Mṛidu alone (the penalty term backstops the reward term).
  ── poison degrees (added 2026-07) ──
 18 poison_net    — how many of the 9 grahas + the Ascendant fall on a "poison" degree:
                  in the sign's Vish Navāṁśa OR within ±1° of the body's Mṛtyu-Bhāga (fatal)
                  degree (the sign-varying classical table). Famous carry FEWER (1.64 vs 2.01)
                  — a "cleaner" chart, the strive-not-blessed theme again; oriented famous-
                  negative. Solo AUC 0.57, 0.577 clean cut; lifts the composite 0.809 → 0.816
                  (seed-stable, all 5 seeds +). Mṛtyu-Bhāga carries it; Vish adds a little. The
                  auspicious counterparts (Pushkara Navāṁśa/Bhāga) were tested and are noise.

Because the composite is a *relative* (z-scored) model, we bake the 321-chart
reference distribution ``REF = {factor: (famous_mean, ordinary_mean, pooled_std)}``
so a single chart can be scored without a runtime population. Each factor is
z-scored against its midpoint, oriented famous-positive, averaged, and squashed
to 0-100. REF is a calibration snapshot — regenerate it if the study set changes.
"""
from __future__ import annotations

import math

# Shared with vimsopaka / chart_strength / fame_composite — one source of truth
# (see dignity.py) so the fame calibration and the strength scores can't drift apart.
from app.services.kundli_calculator.dignity import (
    DIGNITY_PCT as _DP,
    VARGA_WEIGHTS as _VARGA_W,
)

# Factor inputs. Were function-local (cycle avoidance) until the dignity de-dup
# removed the real cycles — none of these import back into worldly_potential.
from app.services.kundli_calculator._core import SIGN_LORDS, _get_dignity
from app.services.kundli_calculator.dhana_yoga import dhana_yoga_score
from app.services.kundli_calculator.divisional import calc_divisional_charts
from app.services.kundli_calculator.poison_degrees import poison_degree_count
from app.services.kundli_calculator.raja_yoga import raja_yoga_score
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha

_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_BAD = {3, 6, 8, 12}        # dusthana — dispositor / occupancy penalty
_OCC = {3, 6, 10, 11}       # upachaya / growth-effort houses
# Factor 2 (Vimśopaka bala) uses the 16 Shodashavarga divisionals + their classical
# weights (_VARGA_W, sum 20; D60/D1/D9 dominant) and the 0-100 dignity scale (_DP).
# Argala (factor 13): all 9 grahas participate; benefics (J/V/Me, bright Moon)
# intervene positively. ARG_PAIRS = (argala house Nth-from-R, its virodha Nth-from-R);
# an argala is "effective" only if it outweighs its virodha counter. ARG_HOUSES
# are the reference houses (from Lagna) the study isolated as fame-bearing.
_ARG_PLANETS = _C + ["Rahu", "Ketu"]
_ARG_PAIRS = ((2, 12), (4, 10), (5, 9), (11, 3))
_ARG_HOUSES = (2, 10, 12)
# Factor 17 (nakṣatra quality): net Mṛidu (tender) − Tikshna (dreadful) nakṣatra count
# over the 9 bodies. Mṛidu = Mṛigaśira/Chitra/Anurādhā/Revatī; Tikshna = Ārdrā/Āśleṣā/
# Jyeṣṭhā/Mūla (0-indexed among the 27). Nakṣatra = longitude ÷ (360/27).
_NAK_ARC = 360.0 / 27.0
_MRIDU_NAK = {4, 13, 16, 26}
_TIKSHNA_NAK = {5, 8, 17, 18}

# Calibration snapshot from the 321-chart study (fame_composite.py), regenerated
# 2026-07 on the corrected math (D4 kendra formula + Rahu/Ketu mean node) over the
# current 225 famous + 96 ordinary set.
# factor -> (famous_mean, ordinary_mean, pooled_std (ddof=0) over all 321 charts).
REF = {
    "rahu_prime": (5.1929, 4.1688, 6.4582),
    "vimsopaka":  (10.0484, 9.8191, 0.6763),
    "av_10th":    (31.8311, 29.8229, 4.6541),
    "av_1st":     (28.8267, 29.1875, 4.2278),
    "upa_occ":    (0.3593, 0.3024, 0.3172),
    "raja_late":  (1.6893, 1.4760, 1.6943),
    "dhana_late": (0.5941, 0.3574, 1.1011),
    "av_11th":    (32.3022, 30.8854, 4.4281),
    "bright_moon":  (0.5467, 0.4271, 0.4999),
    "moon_disp":    (0.4844, 0.3021, 0.4951),
    "moon_sav":     (27.5911, 27.1562, 4.7602),
    "sun_disp":     (0.4311, 0.2188, 0.4822),
    "argala_pos":   (785.8690, 592.6378, 492.9063),
    "purna_tithi":  (0.2267, 0.1146, 0.3948),
    "dig_lords":    (32.0009, 28.2630, 12.2771),
    "top_vim_seat": (0.5467, 0.3125, 0.4995),
    "nak_mridu_net": (0.0267, -0.2812, 1.6364),
    "poison_net": (1.6267, 1.9583, 1.2201),
}
_ARGALA_MID = (REF["argala_pos"][0] + REF["argala_pos"][1]) / 2.0  # neutral fallback
_DIG_MID = (REF["dig_lords"][0] + REF["dig_lords"][1]) / 2.0       # neutral fallback
_SQUASH_K = 2.2  # logistic steepness: mean-z 0 -> 50, +0.5 -> ~75, -0.5 -> ~25. Tunable.

NOTE = ("A faint statistical tilt (cross-validated AUC ~0.76, ~0.81 on the cleanest "
        "cut) toward markers seen in prominent charts — most of worldly success lives "
        "outside the chart. Treat as potential, not destiny.")


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


def _dig_lords(chart: dict, ls: int, sign_lords: list) -> float:
    """Factor 15 — mean Dig Bala (directional strength) of the lagna-lord and the
    10th-lord, read from ``chart['shadbala'][planet]['dig_bala']``. The rulers of the
    self and the career able to act in their power direction. Returns the neutral REF
    midpoint if Shadbala (or the dig_bala component) is absent."""
    sb = chart.get("shadbala") or {}
    lords = (sign_lords[ls], sign_lords[(ls + 9) % 12])  # 1st-lord, 10th-lord
    vals = [sb[p]["dig_bala"] for p in lords if p in sb and "dig_bala" in sb[p]]
    return sum(vals) / len(vals) if vals else _DIG_MID


def factor_values(chart: dict, dashas: list[dict], birth_year: int) -> dict:
    """The 17 raw factor values for a chart. Pure, and the SINGLE source of truth
    for the factor math — ``ReadMe/scripts/fame_composite.py`` imports and calls
    this (rather than reimplementing it) so the study and production can't drift."""
    P, lag = chart["planets"], chart["lagna"]
    ls = lag["sign"]

    # 1 — Rahu prime-dasha (20-50) × clean dispositor
    ra = next(((int(d["start_date"][:4]) - birth_year, int(d["end_date"][:4]) - birth_year)
               for d in dashas if d["planet"] == "Rahu"), None)
    rahu_years = max(0, min(ra[1], 50) - max(ra[0], 20)) if ra else 0
    dispf = 1.0 if P[SIGN_LORDS[P["Rahu"]["sign"]]]["house"] not in _BAD else 0.4
    rahu_prime = rahu_years * dispf

    # 2 — Vimśopaka bala: mean cross-divisional strength of the 7 planets over the 16
    # Shodashavarga vargas (weights sum 20). "D1" = the natal rasi sign. Replaces the
    # old crude single-varga D60 dignity — D60 remains the heaviest weight (4) within it.
    varga = chart.get("divisional") or calc_divisional_charts(P, lag)
    vim_pp = {}  # per-planet Vimśopaka (0-20), reused for factor 16
    for p in _C:
        tot_p = 0.0
        for vname, vw in _VARGA_W.items():
            vsign = P[p]["sign"] if vname == "D1" else varga[vname][p]
            tot_p += vw * (_DP.get(_get_dignity(p, vsign), 45) / 100.0)
        vim_pp[p] = tot_p
    vimsopaka = sum(vim_pp.values()) / len(_C)

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

    # 15 — mean digbala of the lagna-lord and 10th-lord (rulers of self & career)
    dig_lords = _dig_lords(chart, ls, SIGN_LORDS)

    # 16 — the chart's single strongest-Vimśopaka planet (any graha) seated in a
    # prominence house {1,2,4,5,11} (self · wealth · home · creativity · gains). The
    # per-house sweep found 1/2/11 the clear winners (2nd +11.7%) with 4/5 marginal;
    # the composite edged slightly higher including 4/5. The 10th is *reversed* and is
    # excluded. It is the *seat* that matters, not whether the planet is a benefic.
    top_graha = max(_C, key=lambda q: vim_pp[q])
    top_vim_seat = 1.0 if P[top_graha]["house"] in (1, 2, 4, 5, 11) else 0.0

    # 17 — nakṣatra quality: (# of the 9 bodies in a Mṛidu/tender nakṣatra) minus (# in a
    # Tikshna/dreadful one). Famous carry more Mṛidu (gentle/artistic) stars, fewer Tikshna
    # (sharp/severing); the signal strengthens under era-matching (solo 0.62 on the clean cut).
    nak_mridu_net = 0.0
    for p in _ARG_PLANETS:
        ni = int((P[p]["longitude"] % 360) / _NAK_ARC)
        if ni in _MRIDU_NAK:
            nak_mridu_net += 1.0
        elif ni in _TIKSHNA_NAK:
            nak_mridu_net -= 1.0

    # 18 — poison-degree count: how many of the 9 grahas + Ascendant sit in a Vish
    # Navāṁśa or within 1° of their Mṛtyu-Bhāga (fatal) degree. Famous carry FEWER
    # (1.64 vs 2.01) — a "cleaner" chart; oriented famous-negative by the REF.
    poison_net = poison_degree_count(chart)

    return {"rahu_prime": rahu_prime, "vimsopaka": vimsopaka, "av_10th": av_10th,
            "av_1st": av_1st, "upa_occ": upa_occ, "raja_late": raja_late,
            "dhana_late": dhana_late, "av_11th": av_11th,
            "bright_moon": bright_moon, "moon_disp": moon_disp, "moon_sav": moon_sav,
            "sun_disp": sun_disp, "argala_pos": argala_pos, "purna_tithi": purna_tithi,
            "dig_lords": dig_lords, "top_vim_seat": top_vim_seat,
            "nak_mridu_net": nak_mridu_net, "poison_net": poison_net}


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
        dashas = calc_vimshottari_dasha(chart["planets"]["Moon"]["longitude"], dob, chart.get("tob", "12:00"))["dashas"]

    return score_from_factors(factor_values(chart, dashas, birth_year))


def score_from_factors(raw: dict) -> dict:
    """Map the 17 raw factor values to a 0-100 worldly-potential readout: z-score
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
