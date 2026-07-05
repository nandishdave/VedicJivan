# Fame-Signal Experiment Scripts (archive)

The **runnable code** behind every experiment in
[`ReadMe/experiment-ledger.md`](../../experiment-ledger.md). These were originally written in
an ephemeral session scratchpad; archived here so the investigation is **reproducible** and,
crucially, **re-runnable against a larger / cleaner chart set in future**.

For *what each idea concluded and why*, read the ledger. This folder is the *how*.

## Why these exist

The whole point: when we add more **AA-rated** (birth-certificate-accurate) charts, we can
re-run the rejected ideas to see whether any of them clears the validation bar on the bigger,
cleaner sample — instead of rebuilding each test from memory. Add charts → re-run → compare.

## How to run

Each script imports the live `app.services...` calculators and reads two JSON datasets from
the container filesystem, so they run **inside the `vedicjivan-api` container**:

```bash
# 1. Make sure the two datasets are present at the paths the scripts expect:
#    /app/src_celebrities.json   <- the famous set   (source: src/data/celebrities.json)
#    /app/normal_people.json     <- the ordinary set (source: ReadMe/data/ordinary_birth_data.json)
docker cp src/data/celebrities.json           vedicjivan-api:/app/src_celebrities.json
docker cp ReadMe/data/ordinary_birth_data.json vedicjivan-api:/app/normal_people.json

# 2. Copy in and run a script (PowerShell on Windows to avoid MSYS path mangling):
docker cp ReadMe/scripts/experiments/d10_byrating.py vedicjivan-api:/app/d10_byrating.py
docker exec -w /app vedicjivan-api python d10_byrating.py
```

Each chart record needs `birth: {date, time, lat, lon, place}`, a `rating` (AA/A/B/C) for the
time-quality cuts, and (for domain slices) a `category`/domain field.

- **Shadbala:** most scripts pass `with_shadbala=False` for speed; the argala factor needs
  `with_shadbala=True` (slower). Each script's docstring says which.
- **Scoring:** 5-fold cross-validated pairwise AUC, sign+scale learned on the train fold only.
  Nested variants re-select the feature *inside* each fold — that's the honest number.

## Map: script → what it tests (verdict in the ledger)

**Accepted factors (re-validate these on new data):**
`final5/12/13/14.py` (composite milestones) · `av_perhouse.py` `winners5.py` (AV + upachaya) ·
`yoga_activation.py` `late_window.py` `winners7.py` (late Raja/Dhana activation) ·
`moon_tests.py` `moon_disp.py` `moon_disp_houses.py` `revalidate.py` `eleven.py` (Moon factors) ·
`sun_validate.py` (Sun dispositor) · `confirm_av11.py` (11th AV) ·
`argala_nested.py` (argala) · `tithi_nested.py` (Pūrṇa tithi) ·
`compare_rahu*.py` `rahu_behavior.py` (Rahu prime) · `multivariate.py` `compare_matched.py` (CV framework).

**Rejected ideas (the re-test candidates):**
D10 — `d10_rich.py` `d10_byrating.py` `dasha_d10houses.py` `neecha.py` `neecha_strict.py` `fame_d10_av11.py` ·
Rich D60 — `d60_rich.py` · static Dhana/Raja — `winners6_dhana.py` `dhana_build.py` `winners6_raja.py` ·
Prosperity — `prosperity8.py` · FB dāśā — `compare_fbdasha.py` `dasha_now.py` ·
3/6/10/11-lord dāśā — `md_lagna.py` `upachaya_cond.py` ·
Numerology — `moolank_test.py` `moolank_house.py` `moolank_rule.py` `moolank_nested.py` `moolank_dasha.py` `numer_recheck.py` ·
Argala variants — `argala.py` `argala_allhouses.py` ·
Nitya-yoga / Tithi — `yogatithi.py` · Jaimini — `jaimini_karaka.py` `jaimini_karakamsa.py` `hyp_jaimini.py` ·
KP — `kp_analysis.py` `kp_probe.py` · Arudha Lagna — `experiment23.py` `al_nested.py` ·
config/lord yogas — `hyp_config.py` `hyp_fb.py` `hyp_lords.py` ·
Chandra/Sūrya kundali — `moon_perfactor.py` `sun_tests.py` · Tatva/nakṣatra — `tatva_nak.py` ·
interactions — `compare_composite.py` · peak-vs-breadth — `compare_peak.py` `compare_activated.py`.

**Structural (birth-time & domain):**
`experiment1.py` `discarded_by_time.py` (time precision is not the ceiling) ·
`experiment2.py` `domain_sig.py` (domain heterogeneity — the key positive result) ·
`superstar_calib.py` `superstar_calib2.py` (early calibration).

**2026-07 strength sweep (A–E; two survived → the 15-factor model):**
`strength_A.py` (cross-divisional Vimśopaka — WIN, swapped in as factor 2) ·
`strength_B.py` (yogakāraka — rejected) ·
`strength_C.py` (digbala of lagna/10th lords — WIN, added as factor 15) ·
`strength_D.py` (house-lord total Shadbala — rejected: it's *directional* strength specifically) ·
`strength_E.py` (Indu/Sree Lagna — rejected) ·
`strength_final.py` (combined A+C verification: 0.732→0.751 full, 0.759→**0.789** clean cut).

**2026-07 strength sweep, round 2 (F–I; all NULL → strength axis saturated, model stays 15):**
`strength_F.py` (Bhāva Dṛṣṭi Bala — aspects onto fame houses) ·
`strength_H.py` (combustion) ·
`strength_G.py` (Iṣṭa Phala √Uccha×Cheṣṭa) ·
`strength_I.py` (Atmakāraka strength) ·
`strength_J.py` (D9/Navamsa functional-benefic strength, exchanges, D9-lagna house). Each nested-honest 0.72–0.74 &lt; 0.751 base.

**Factor 16 — `top_vim_seat` (2026-07-04, the prominence-seat rule):**
`vimsopaka_pattern.py` (per-planet Vimśopaka calculator core + which-planet / which-house pattern + nested acid test) ·
`per_house.py` (per-house breakdown of the strongest planet: 2nd +11.7%, 10th reversed) ·
`refine_vimsopaka.py` (house-set narrowing; any-planet vs functional-benefic → any wins) ·
`strength_combine.py` (combine-vs-separate: merging magnitude+seat into ONE factor is WORSE — keep separate) ·
`seat_ref.py` (REF for the {1,2,4,5,11} seat). Result: strongest-Vimśopaka planet in **{1,2,4,5,11}** → **factor 16** (0.751→0.766 full, 0.789→0.795 clean). Kept SEPARATE from Vimśopaka-magnitude (they're near-uncorrelated).

**Factor 17 — `nak_mridu_net` (2026-07-05, nakṣatra quality):**
`nakquality.py` (per-quality famous-vs-ordinary; the Violent signal is an era/node confound that EVAPORATES under matching, while Mṛidu STRENGTHENS) ·
`strength_nakfactor.py` (tests A=Mṛidu, B=Mṛidu−Tikshna, A+B, C=Mṛidu+Swift, D=broad net) ·
`nak_acid.py` (acid test for A: single Mṛidu fails, −0.004) ·
`nak_acid_B.py` (acid test for B: survives at base, +0.001 — the penalty term backstops the reward). Result: **B (Mṛidu − Tikshna) → factor 17** (0.766→0.772 full, 0.795→**0.809** clean). Most marginal factor: acid-neutral, seed-stable clean cuts. `strength_navatara.py` (a *different* nakṣatra idea — Navatāra tāras from Janma — was rejected).

**2nd-house Ashtakavarga test — `av2_test.py` (2026-07-05, REJECTED):** does SAV bindus on the 2nd (dhana) house earn an 18th slot? No — lift **−1.57** (reversed: famous carry *fewer* 2nd-house bindus), composite +0.001 full / **−0.002 mean on the ≥1940 clean cut** across 5 seeds. Fame lives on the career/gains axis (10th/11th, both already accepted), not the accumulated-wealth 2nd. Model stays 17. See the ledger's rejected table.

**Factor 18 — poison degrees (2026-07-05, ACCEPTED):** the auspicious/poison-degree investigation. `navamsa_bhaga_tables.json` holds all four user-supplied tables (Pushkara Navāṁśa, Vish Navāṁśa, Pushkara Bhāga, sign-varying Mṛtyu Bhāga). `vish_navamsa.py` (Vish solo — faint 0.536) · `pushkara_net.py` (Pushkara solo + Pushkara−Vish net) · `full_net.py` (all 4 components + net; **Mṛtyu Bhāga is the engine: solo 0.572/0.570 clean; malefic sum Vish+Mṛtyu 0.579/0.577; the Pushkara/auspicious side is NOISE ~0.50-0.53 and dilutes**) · `nested_net.py` (acid test: full-net +0.003 clean cut, **MALEFIC-only +0.007 seed-stable all 5 seeds → factor 18**). Result: **`poison_net` = count of the 9 grahas + Ascendant in a Vish Navāṁśa OR within ±1° of their Mṛtyu-Bhāga degree; fewer = more famous.** 0.809→**0.816** clean cut. Productionised in `kundli_calculator/poison_degrees.py`.
