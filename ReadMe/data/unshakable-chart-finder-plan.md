# Unshakable Chart Finder — Build Plan

> Goal: for a date **range + place**, find birth (date, time) moments whose chart is
> classically *exceptional* — strong Shadbala across planets, high Ashtakavarga in
> key houses, real Raja/Dhana/Mahapurusha yogas, good longevity. Return **every**
> chart that clears a quality bar, not just the single best.

## Locked decisions (2026-06-30)
- **v1 range:** WEEK (exercises the funnel across days).
- **Build order:** rigorous core first, then greatness layer, then productionize.
- **Longevity:** surface all three Ayurdaya methods as a **BAND** + Balarishta flags (honest about their disagreement).
- **Quality bar:** ABSOLUTE 90/100 with fallback (see note). *(pending final confirm)*

## Reuse vs build (from the calculator inventory)
**Reuse (exist in `api/app/services/kundli_calculator/`):**
- `calc_shadbala(planets, lagna, jd, dob, tob, divisional, sun_sunset)` → per-planet 6-fold + `ratio` + `rank`. **HIGH cost (the bottleneck).**
- `calc_ashtakavarga(planets, lagna_sign)` → `totals[12]` (SAV/sign) + per-planet BAV. LOW.
- `calc_divisional_charts(planets, lagna)` → D2–D60 (18 vargas). LOW.
- `calc_yogas(planets, lagna)` → list of `{name,type,planets}` (~11 yogas). MED. **Binary present/absent.**
- dignity, `calc_graha_drishti`, `calc_panchanga`, `calc_nakshatra`, `calc_sunrise_sunset`, friendships, avasthas, doshas — LOW–MED.

**Build new:**
- `longevity.py` — Pinda/Amsa/Nisarga ayu band + Balarishta + Maraka. (none exists)
- `fame.py` — 10th-house + Sun/Atmakaraka + raja-combo → indicative Yaśa score. (none)
- `yoga_strength.py` — weight `calc_yogas` output by forming-planets' Shadbala, minus bhanga.
- `chart_strength.py` — the composite 0–100 aggregator (Layer 1 + Layer 2).
- `unshakable_finder.py` — the funnel orchestrator (T1–T4, stream-and-discard, threshold, audit).

## The 0–100 metric — two labelled layers
**Layer 1 — Structural Strength (rigorous, ~70%, all reuse):** Shadbala (planets ≥ min-req; weight lagna-lord + benefics), Ashtakavarga (SAV in kendras 1/4/7/10 + trikonas 1/5/9 + lagna), dignity, lagna-lord strength, benefic placement, D9 strength.

**Layer 2 — Greatness markers (heuristic, ~30%, labelled indicative, new):** yoga strength (Mahapurusha/Raja/Dhana minus bhanga), longevity band + Balarishta, fame markers.

A chart clears 90 only if **both** the structural core is excellent **and** real greatness markers are present.

## The funnel (Shadbala runs ONLY in T4)
| Tier | Computes | Uses (cheap until T4) | Conservative cutoff |
|---|---|---|---|
| **T1 Day filter** | Panchanga + nakshatra + Moon/paksha + dosha flags @ sunrise | `calc_panchanga`, `calc_nakshatra` | Drop only hard-dosha days (Amavasya/eclipse/Rikta+bad-yoga). Keep ~30–50% |
| **T2 Coarse Lagna** | 12 Lagnas/day: SAV (kendra/trikona) + dignity + lagna-lord placement. NO Shadbala | `calc_ashtakavarga`, `calc_divisional_charts`, `calc_graha_drishti` | Keep windows that can't be ruled out of 90% |
| **T3 Fine time** | Sample every few min in survivors; re-proxy + yoga detect | + `calc_yogas` | Keep strong-proxy/notable-yoga moments |
| **T4 Deep eval** | Finalists only: full Shadbala + divisional strength + yoga strength + longevity + fame → 0–100 | `calc_shadbala` (HIGH) + new modules | Compute 0–100; keep all ≥ 90 |

## Quality bar — ABSOLUTE vs RELATIVE (note)
- **Absolute 90/100:** fixed quality bar. A barren week → *zero* results → fallback shows best-available with a clear "below the magical bar" note. A rich week → many results. Quality guaranteed; count varies.
- **Relative top-10%:** always returns the top 10% of the range regardless of absolute quality — can *include* mediocre charts in a weak week AND *drop* genuinely magical charts in a rich week (if they fall outside the top 10%).
- **Choice: ABSOLUTE + fallback** — for "person of the century" we want genuine excellence, not "least-bad this week."

## Safety & trust
- Return the whole ≥90 band, ranked, each with a breakdown. Cap (e.g. 100) + **warn if capped** (no silent truncation).
- **Calibration/audit:** periodically run full T4 on a sample of T1–T3 *rejected* charts; confirm none would score ≥90. If any would → loosen the cheap filter. Proves "no magical chart dropped."
- **Stream-and-discard:** hold only finalists + running ≥90 set → flat RAM at any range.

## Compute placement + charging
- Day/week → existing Lambda (fits 300s with funnel) + async-email.
- Month/year full → on-demand **ECS RunTask / AWS Batch**, sized per job (2→16 vCPU), spin up → run → email → shut down. No idle cost.
- Charging: record vCPU-hours/job → price = cost × margin (cents → ~$0.30).
- Fan-out: not built; escape hatch only if year-scale + frequent.

## Phasing
1. **Phase 1 — rigorous core + funnel + local harness.** `chart_strength.py` (Layer 1), 4-tier funnel, stream-and-discard CLI, calibration test. Validate on day/week locally.
2. **Phase 2 — greatness layer.** `yoga_strength.py`, `longevity.py`, `fame.py` → fold into Layer 2.
3. **Phase 3 — productionize.** API + email + on-demand box + charging + frontend.
4. **Phase 4 (only if needed)** — fan-out for year-scale.

## Local testing guidance
- Validate day & week **brute-force** (seconds–2 min) → eyeball metrics + calibrate funnel.
- Then funnel for month/year (~minutes, flat RAM). Don't fine-sample brute-force beyond a week locally.
