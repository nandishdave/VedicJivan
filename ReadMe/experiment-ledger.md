# Fame-Signal Experiment Ledger

**The complete, authoritative record of every idea tested** in the "can a birth chart tell
famous from ordinary?" investigation — what we kept, what we rejected, and *why*. This is
the **don't-re-test registry**: if an idea is in the "Rejected" table below with a reason,
it has already been tried and failed under honest validation. Add to this file; don't start
a new one.

- **Model as of this writing:** 18-factor `worldly_potential` composite, CV-AUC **≈ 0.775**
  pooled (0.809 on the cleanest India ≥1940 cut; all-India crosses 0.80). Reproduction: `ReadMe/scripts/fame_composite.py`.
- **Data:** 225 famous (rated AA/A/B/C by birth-time reliability) vs 96 ordinary control.
- **Scoring convention:** 5-fold cross-validated pairwise AUC; sign + scale learned on the
  *train* fold only. Solo-AUC = a single factor alone. 0.50 = coin-flip; <0.50 = leans *ordinary*.
- **Validation bars a factor must clear:** (a) correctly signed with an astrological reason,
  (b) survives **nested** CV (feature re-selected inside each train fold — kills selection bias),
  (c) holds on **confound-matched** cuts (India ≥1940 / ≥1955), (d) **seed-stable** across seeds.

> ⚠️ The raw experiment scripts live in a **session temp scratchpad** and are **not** version-
> controlled — they are ephemeral. This ledger is the durable record of what they found.

---

## A. Accepted — the 18 factors

Each survived the validation bars (factor 17 is the marginal exception — acid-neutral; see note). Labels match `worldly_potential.py` / `_WP_LABELS`.
**Model as of 2026-07: 18 factors, CV-AUC 0.775 full / 0.816 clean cut (≥1940), 0.809 all-India.**

| # | Factor | What it measures | Established in |
|---|--------|------------------|----------------|
| 1 | `rahu` | Rahu mahadāśā lived in prime (20–50) × dispositor not in 3/6/8/12 | compare_rahu, compare_rahu_natal, compare_rahu_composite |
| 2 | `vimsopaka` | **Vimśopaka bala** — mean dignity of the 7 planets across all 16 Shodashavarga vargas (wt sum 20; D60/D1/D9 dominant). **Upgraded from crude D60 (0.54→0.61) on 2026-07** | strength_A, strength_final |
| 3 | `av10` | 10th-house Sarvāṣṭakavarga bindus | av_perhouse, winners5 |
| 4 | `av1` | 1st-house SAV bindus | av_perhouse, winners5 |
| 5 | `upa` | Peak (20–50) years under a dāśā lord *occupying* 3/6/10/11 | winners5, dasha_house |
| 6 | `raja` | Late (50–80) Rāja-yoga dāśā activation (yoga-lord participation) | yoga_activation, late_window, winners7 |
| 7 | `dhana` | Late (50–80) Dhana-yoga dāśā activation | yoga_activation, late_window, winners7 |
| 8 | `av11` | 11th-house SAV bindus (added as the 8th factor) | fame_d10_av11, confirm_av11 |
| 9 | `bright` | Bright (Śukla) Moon — Sun–Moon elongation 72–264° | moon_tests, eleven |
| 10 | `moon_disp` | Moon-sign dispositor placed in {1,2,11,12} | moon_disp, moon_disp_houses, revalidate |
| 11 | `moon_sav` | Moon-sign SAV bindus | moon_tests, eleven |
| 12 | `sun_disp` | Sun-sign dispositor placed in {1,2,3,4} | sun_tests, sun_validate |
| 13 | `argala_pos` | Positive (śubha) Shadbala-weighted Jaimini argala on 2/10/12 | argala_nested, final13 |
| 14 | `purna_tithi` | Born in a Pūrṇa tithi (5th/10th/15th of either pakṣa) | tithi_nested, final14 |
| 15 | `dig_lords` | **Mean Dig Bala (directional strength) of the lagna-lord & 10th-lord.** Solo 0.57, ~zero corr with all others (orthogonal). **Added 2026-07** | strength_C, strength_final |
| 16 | `top_vim_seat` | **Chart's strongest-Vimśopaka planet (any graha) seated in {1,2,4,5,11}.** Per-house sweep: 1/2/11 clear winners, 4/5 marginal (edged composite higher), 10th reversed; functional-benefic restriction reverses. Solo 0.60. **Added 2026-07** | vimsopaka_pattern, per_house |
| 17 | `nak_mridu_net` | **(# of 9 bodies in a Mṛidu nakṣatra) − (# in a Tikshna one).** Mṛidu {Mṛigaśira, Chitra, Anurādhā, Revatī} favors famous; Tikshna {Ārdrā, Āśleṣā, Jyeṣṭhā, Mūla} favors ordinary. Solo 0.62 (clean cut), STRENGTHENS under era-matching. **Most marginal factor** — acid-neutral (+0.001), seed-stable clean-cut +0.013. **Added 2026-07** | nakquality, strength_nakfactor, nak_acid_B |
| 18 | `poison_net` | **(# of the 9 grahas + Ascendant on a "poison" degree)** — in the sign's **Vish Navāṁśa** (poison navamsa: {Ar,Ta,Vi,Sg}→nav1, {Ge,Le,Li,Aq}→nav5, {Cn,Sc,Cp,Pi}→nav9) OR within **±1° of their Mṛtyu Bhāga** (sign-varying fatal-degree table, user-supplied+verified). Famous carry FEWER (1.64 vs 2.01) → oriented famous-negative. Solo 0.57, **0.577 clean cut**; lifts composite **0.809→0.816 (seed-stable, all 5 seeds +)**. Mṛtyu Bhāga carries it; Vish adds a little. The auspicious mirrors (**Pushkara Navāṁśa** 0.53, **Pushkara Bhāga** 0.50) are NOISE — tested + dropped (adding them dilutes: net 0.564 < poison-only 0.579). **Added 2026-07-05** | vish_navamsa, pushkara_net, full_net, nested_net |

Milestone composite runs: final5 → final12 → final13 → final14 → **strength_final** (the 15-factor
verification); matched-cut checks in compare_matched, confirm_av11. Multivariate CV framework:
multivariate, score_ranking, breakdown. Reproduction: `ReadMe/scripts/fame_composite.py` (15-factor).

### The 2026-07 strength sweep (5 candidates, 2 survived)
Nandish's intuition that *strength* was under-read. Tested one-by-one, each nested + seed-validated:
- **A · Cross-divisional strength** → **WIN (swap)**. Vimśopaka bala replaced crude D60 (factor 2).
  The +factor form was redundant; **vargottama count was reversed** (ordinary 0.81 vs famous 0.67). `strength_A`
- **B · Yogakāraka** → rejected (see below). `strength_B`
- **C · Digbala of the lords** → **WIN (+factor 15)** `dig_lords`. `strength_C`
- **D · House-lord total Shadbala** → rejected — it is *directional* strength specifically, not total. `strength_D`
- **E · Indu / Sree Lagna** → rejected. `strength_E`
- Combined A+C verification: full 0.732→0.751, ≥1940 0.759→**0.789**, ≥1955 0.708→0.753 (seed-stable). `strength_final`

**Round 2 (F–I, tested vs the 15-factor base) — ALL NULL, model stays 15:**
- **F · Bhāva Dṛṣṭi Bala** (aspects onto fame houses) → null 0.742. `strength_F`
- **H · Combustion** → null 0.740. `strength_H`
- **G · Iṣṭa Phala** (√Uccha×Cheṣṭa) → null 0.736. `strength_G`
- **I · Atmakāraka strength** → null 0.723. `strength_I`
- **Interpretation:** the *strength axis is saturated* — `vimsopaka` + `dig_lords` already captured what planetary strength offers for fame; every further strength *magnitude* is redundant or null.

**Factor 16 (2026-07-04) — a different axis: WHERE the strongest planet sits.** `top_vim_seat` = the chart's single strongest-Vimśopaka planet (any graha) seated in **{1,2,4,5,11}**. Per-house sweep (`per_house`): 2nd +11.7%, 11th +4.9%, 1st +4.3% (clear winners), 4th +2.3%, 5th +1.3% (marginal), **10th REVERSED −4.6%**. Functional-benefic restriction *reverses* it (0.49) — it is the *seat*, not the planet's nature. **Combine-vs-separate tested** (`strength_combine`): merging Vimśopaka-magnitude + seat into ONE factor is WORSE (0.734 < 0.751 vim-mean-alone) — they're near-uncorrelated (r≈0.03–0.13), so keep SEPARATE. Seat house-set {1,2,4,5,11} edged {1,2,11} by +0.005 (within noise) — user chose {1,2,4,5,11}. Solo 0.60; nested +0.005 floor; seed-stable +0.010. REF `top_vim_seat=(0.5467, 0.3021, 0.5001)`. Lifted 0.751→0.766 full, 0.789→0.795 clean cut. Scripts `vimsopaka_pattern`, `per_house`, `refine_vimsopaka`, `strength_combine`, `seat_ref`.
- **Rāhu/Ketu in Vimśopaka — tested, does NOT help the model** (`strength_nodes`): a node is the strongest planet *more* often in ordinary (12% fam vs 16% ord, AUC 0.484 reversed); including nodes in the *mean* drops it 0.610→0.586; composite 5-seed full ~identical/worse (nodes-in-strongest 0.759 vs 0.758 = noise; nodes-in-mean 0.755–0.756). **Model stays 7-graha.** Nodes shown in the *calculator* as display-only rows (Parāśara dignities), excluded from the average + strongest pick.

---

## B. Rejected — do NOT re-test

Every row was tested and **failed** to earn a place under honest validation. Numbers are
solo-AUC unless stated; "nested +x" = honest lift over the then-current composite.

| Tested idea | Result | Why it failed | Script(s) |
|-------------|--------|---------------|-----------|
| **D10 (Dasāṁśa) — crude dignity** | 0.506 | coin-flip; hurt the composite | fame_d10_av11, superstar_calib2 |
| **D10 — rich significators** (Lagna-lord & 10th-lord dignity + placement + **connection**, 10th occupants, career composite) | solo 0.44–0.52 | every reading coin-flip; the career-varga is silent on fame even though D60 (karma) works | d10_rich, d10_charts, neecha, neecha_strict |
| **D10 — dāśā rules the D10 career houses** | no separation | year-weighted "MD rules D10 10th/kendra/trikoṇa" flat | dasha_d10houses |
| **D10 — revival on accurate (AA/AA+A) times** | solo 0.45–0.52, **no C→AA gradient** | not birth-time-smeared; genuinely null even on clean charts | d10_byrating |
| **Rich D60** — deity names, vargottama, D60-lagna condition, yoga-repeats | composite 0.452 | wrong-way; the deity rule is ~50/50 by construction | d60_rich |
| **Static Dhana yoga** (classical, un-activated) | 0.515 | earned-wealth combos are everywhere | winners6_dhana, dhana_build |
| **Static Rāja yoga** (classical, un-activated) | 0.529 | power combos don't mark fame | winners6_raja |
| **Prosperity yoga (5th/9th)** | 0.478 (<0.5) | leans *ordinary* — grace ≠ fame | prosperity8 |
| **Functional-benefic dāśā strength** (20–50) | lift −1.95 | negative once computed *functionally* (not natural benefics) | compare_fbdasha, dasha_now |
| **3/6/10/11-*lord* dāśā** (by lordship) | 0.409 | reversed — bundles in the 6th-lord dusthāna | md_lagna, upachaya_cond |
| **Lagna-link / strong-lagna-lord gating** on the above | softens, never predicts | the lagna filter can't flip a negative rule positive | md_lagna |
| **Numerology** — Mūlāṅk/Bhāgyāṅk planet = a functional benefic | 0.40 (reversed) | famous sit at the random base rate; original gap was a control artifact | moolank_test |
| **Numerology — house placement** {1,2,3,5,10} | nested +0.004 | real but tiny & redundant; AV factors already capture it (re-confirmed vs 14-factor) | moolank_house, moolank_rule, moolank_nested, numer_recheck |
| **Numerology — Mahādaśā in prime** (20–50) | 0.48 | dāśā order is set by birth *nakṣatra*, independent of the calendar date | moolank_dasha |
| **Net / negative / count-based argala** | flat / hurt | only *positive, Shadbala-weighted* argala survives; count-only is noise | argala, argala_allhouses |
| **Pañchāṅga Nitya-Yoga (27)** — benefic-vs-malefic split | 0.51 | incoherent — malefic yogas (Vyatipāta, Vajra) lean famous too; sparse over 27 buckets | yogatithi |
| **Tithi groups other than Pūrṇa** (Nanda/Jaya/Rikta as +factors) | flat / reversed | only Pūrṇa separates; the rest lean ordinary or wash out | yogatithi, tithi_nested |
| **Jaimini karaka connections** (AK–AmK, AK–PK, AmK–PK by conjunction / rāśi dṛṣṭi) | 0.46–0.49 (reversed) | the premier "rāja sambandha" is *more* common in ordinary; famous have *un*-entangled karakas | jaimini_karaka, hyp_jaimini |
| **Jaimini Kārakāṁśa rāja yogas** (benefics/dignified in kendras & trikoṇas from Kārakāṁśa, AK dignity) | 0.47–0.52 across 7 variants | near-chance; none lift the matched cuts | jaimini_karakamsa, hyp_jaimini |
| **KP cuspal sub-lords** (10th/11th/2nd CSL signifying 2/6/10/11; Placidus + KP ayanāṁśa) | ≈90% both (near-ceiling) | the "any of 4 houses" net is too broad to discriminate; 1st-CSL→1/10/11 hint (0.54) too weak & needs KP-grade times | kp_analysis, kp_probe |
| **Arudha Lagna fame rules** (AL angular to Lagna; benefics in 2/10/11 from AL) | seed-avg +0.004; nested +0.000 | correctly signed but the in-sample +0.014 was seed luck — a hint, not a factor | experiment23, al_nested |
| **Neecha-bhaṅga** on the D10 10th-lord (cancelled debilitation) | no separation | cancellation doesn't mark fame | neecha, neecha_strict |
| **Config yogas** — wealth (stellium, 2–11 exchange, 2nd-lord+Rahu…) & sports (6th-lord in lagna, debilitated in 6/8) | no separation vs base rate | classical "signatures" appear at the random rate | hyp_config |
| **Trikoṇa-lord (1/5/9) sambandha** raja yoga | no lift | over-represented claim didn't hold | hyp_fb |
| **1/2/10/11 house-lord sambandha** + Rahu/Ketu involvement | no usable lift | interconnection common in both groups | hyp_lords |
| **Chandra Kundali** — the 8 factors recomputed from the Moon as lagna | no net gain | Moon-as-lagna doesn't out-read the Lagna; kept only the specific Moon factors (9–11) | moon_tests, moon_perfactor |
| **Sun-as-lagna** — 8 factors from the Sun sign | no net gain | kept only `sun_disp` (factor 12) | sun_tests |
| **Pairwise interaction terms / multiplicative synergy** | no gain over additive | a linear additive composite captures it; interactions overfit | compare_composite |
| **Peak single-strongest combination** (breadth vs one activated yoga) | ~0.58, no better than breadth | the count/breadth composite already wins | compare_peak, compare_activated |
| **Tatva of functional benefics + nakṣatra types** | no separation | element/nakṣatra typing doesn't discriminate | tatva_nak |
| **Upachaya-*lord condition*** (dignity of 3/6/10/11 lords + dispositors) | no lift beyond occupancy | only the *occupancy* dāśā (factor 5) survived | upachaya_cond |
| **Yogakāraka** condition (strength/dignity/placement/dasha of the kendra-and-trikoṇa lord) | nested-honest 0.724 (<0.732) | dignified/activated yogakāraka leans faintly famous (0.54–0.56) but redundant with raja/dhana + dasha-activation | strength_B |
| **House-lord *total* Shadbala** (1st/10th/11th lords, occupant strength) | solo 0.46–0.52; adds nothing beyond digbala | the sharp counter to factor 15 — it is the *directional* (dik) strength, not total strength, that marks fame | strength_D |
| **Vargottama count** (planets in same D1 & D9 sign) | solo 0.449 (reversed) | ordinary have *more* vargottama (0.81 vs 0.67) — "fixed/repetitive" ≠ dynamic | strength_A |
| **Indu Lagna & Sree Lagna** (Moon-based wealth/prosperity points) | nested-honest 0.718; several metrics reversed | one right-signed metric (benefics in K/T from Indu Lagna, 0.57) too weak; ordinary carry *more* support at the wealth point — a base-rate mirage | strength_E |
| **Bhāva Dṛṣṭi Bala** (benefic-vs-malefic *aspects* onto the 1st/10th/11th, count + Shadbala-wt) | nested-honest 0.742 (<0.751) | the aspectual "weather" on the fame houses is net-malefic for everyone and barely differs; only the *lords'* strength marks fame, not who aspects the house | strength_F |
| **Combustion (Astaṅgata)** — key benefics/lords free of the Sun's burning | nested-honest 0.740; direction mixed/reversed | combust = conjunct the Sun = also "close to power"; the two cancel, so combustion is silent on fame | strength_H |
| **Iṣṭa Phala** — √(Uccha × Cheṣṭa bala) of the key lords / planets | nested-honest 0.736 | lagna-lord Iṣṭa leans right (0.53) but redundant with `dig_lords`+`vimsopaka`; mean/benefic Iṣṭa reversed | strength_G |
| **Atmakāraka strength** (soul-planet's dignity / Vimśopaka / digbala / SAV / Shadbala) | nested-honest 0.723; all metrics 0.49–0.52 | a strong AK does not mark fame; already inside `vimsopaka` (mean over 7). We tested Kārakāṁśa *yogas* earlier (also null) | strength_I |
| **D9 (Navamsa) — functional-benefic specific**: trikoṇa lords strong in D9, parivartana among them in D9, D9-lagna in a good house {1,2,4,5,9,10,11} of D1 | nested-honest 0.732; all metrics 0.50–0.53 | D9 dignity is already inside `vimsopaka` (D9 = weight 3, third-heaviest varga); the FB-specific read re-counts it. **D9-lagna-in-good-house is a clean null (65% famous vs 66% ordinary)**; FB parivartana in D9 too rare (~6%) | strength_J |
| **Navatāra Chakra** — planets in benefic tāras {2,4,6,8,9} vs malefic {3,5,7} from the Janma nakṣatra | solo 0.51–0.53; nested 0.764 (<0.767) | *direction correct* (famous lean benefic, fewer Vipat/Pratyari/Vadha) but far too weak — the Janma-relative tāra is ≈uniform for both groups (~3.3 benefic/2.0 malefic of 6 each); a muhurta/compatibility tool, not a natal-prominence one | strength_navatara |
| **2nd-house Ashtakavarga** (SAV bindus on the 2nd/dhana, as an 18th factor) | lift **−1.57** (reversed); composite +0.001 full, **−0.002 mean on the ≥1940 clean cut** (5 seeds) | famous carry *fewer* 2nd-house bindus (25.9 vs 27.5) — like `av_1st` it leans ordinary. Fame lives on the **career/gains axis (10th +2.01, 11th +1.42)**, not accumulated wealth (2nd). **Fame ≠ wealth.** The two AV fame houses (10/11) were already accepted; the 2nd adds nothing. (2026-07-05, verifies the choice to exclude it) | av2_test |

### Structural findings (not single rules)
- **Birth-time precision is NOT the ceiling.** AA/A charts score *lower* (0.68–0.70) than the
  pooled model because Rodden rating is confounded with Western-vs-Indian geography. (experiment1, discarded_by_time)
- **Discarded rules do not revive on accurate times.** No rejected rule shows a monotonic
  C→AA lift — the signature of a real-but-time-smeared effect is absent everywhere. (discarded_by_time, d10_byrating)
- **Domain heterogeneity — the key positive result.** The pooled 0.73 hides large variation:
  worldly-achievement fame (Science 0.82, Business 0.80, Politics 0.76) reads far better than
  performance/devotion (Music 0.72, Film 0.71, Sports 0.69, Spiritual 0.65). 0.80+ *is* reached
  for the right domain. **Domain-specific weight-refitting HURTS** (small n overfits) — the lever
  is more charts in legible domains, not more rules. (experiment2, experiment23, domain_sig)

---

## C. Framework, calibration & data-generation scripts (not hypotheses)

Kept for reference; these build data or infrastructure rather than test a fame rule.

- **CV / scoring framework:** multivariate, score_ranking, breakdown, rank_all, pattern_scan, calib, scan_scores
- **Composite milestone runs:** final5, final12, final13, final14, confirm_av11, revalidate, compare_matched, compare_real, compare_all140, compare_celebs, compare_composite, compare_winners, compare_moved, late_window, winners5/6/7
- **Per-chart diagnostics:** celeb_table, ordinary_table, shikha_diag, nandish_dhana, nandish_raja, d10_charts, av11_list, dasha_controls, rahu_behavior, dasha_now
- **Data / HTML generation:** gen_celebrities, gen_normal, gen_reusable, gen_celeb_html, gen_ordinary_html, gen_charts_html, gen_charts_north, dump_charts, domain_sig, find_charts, find_new, append_* (batch/dhoni/kohli/famous/indian/indian2), dhoni, kohli
- **Smoke tests:** smoke, smoke_u, smoke_pct, smoke_stack, smoke_mu, smoke_bd, smoke_recal, wp_smoke, num_smoke, kp_probe, ref_sun, superstar_calib, ali_d10, func_benefic, hyp_jaimini, prosperity8

---

*Last updated: 2026-07-05. Model = 18 factors, CV-AUC ≈ 0.775 pooled / 0.816 cleanest cut.*
