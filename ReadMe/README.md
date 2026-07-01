# Famous-vs-Ordinary Chart Study

An honest investigation into a single question: **can Vedic birth-chart factors
distinguish famous/successful people from ordinary people?**

Short answer: **a real but weak signal exists (~0.57 AUC)** — genuine, stable,
directionally consistent, but nowhere near a predictor. This folder holds the
full data, the reproducible scripts, and the findings.

---

## The finding

Against **32 AA-rated famous charts** (birth-certificate reliability) and
**96 real, verified ordinary charts**, a cross-validated model separates the two
groups with:

```
CV-AUC by control size: 0.591@30 → 0.597@35 → 0.612@49 → 0.554@58
                      → 0.582@69 → 0.577@88 → 0.554@96      center ≈ 0.57
```

Seven checkpoints all land in one ±0.06 band — the fingerprint of a **genuine but
weak** effect. In the pick-two test: shown one famous + one ordinary chart, the
model picks the famous one ~57% of the time (a coin flip is 50%, "useful" is 65%+).

**Best formulation = a composite CO-OCCURRENCE count.** No single factor and no
weighted linear model beats a simple **count of how many of the 8 strong-chart
factors a chart stacks** (orient each famous-positive, count the elevated ones).
Famous charts stack more (mean ~4.1 vs ~3.4 of 8; ≥5 strong: 34% vs 21%), and this
count gives **CV-AUC 0.565 > the linear model's 0.498**. It is co-occurrence, not
synergy — adding pairwise interactions *overfits* (0.428). Still weak (~0.55, not a
predictor), but the right shape for the signal — so the ranking is now scored by
this strong-factor count. (Dasha factor uses functional benefics — lagna-specific.)

### What stands strong (consistent, famous-positive every run)
| Factor | Strength | Reading |
|---|---|---|
| **Dasha timing (Vimshottari) in productive years** | strongest | *timing beats the static snapshot* |
| **D60 (Shashtiamsa) strength** | solid | the karma/fruits varga carries signal |
| **10th-house Ashtakavarga** | solid | career-house bindu density |
| **2–11 wealth-axis connections** | consistent | classic wealth combinations |
| **1st-house Ashtakavarga**, **trikona (1/5/9) links** | mild | vitality + raja-yoga trines |

### What failed
- **Functional benefics in kendra/trikona** — the *lone consistently negative*
  factor (famous slightly LOWER). The popular "benefics in the kendras" rule did
  **not** predict worldly success here.
- Static raja-yoga / exalted-planet / Shadbala-total snapshots — no separation.

**Takeaway for muhurta / future-date work:** weight *timing* (dasha) + career/
wealth/karma indicators; de-emphasise "benefics in kendra"; always present results
as a soft tilt (~0.57), never a guarantee.

### Graded Dhana + Prosperity yogas
The crude "2–11 flag" was replaced by **two separate graded scores** —
`connection-type × which-lords × dignity × house-of-formation` — in the shared
module **`api/app/services/kundli_calculator/dhana_yoga.py`**:

- **Dhana** (wealth) — the tight yoga among the lords of **1, 2, 11** (Lagnesh /
  Dhanesh / Labhesh).
- **Prosperity** (fortune) — the wider extension that also touches the **5th / 9th**
  lords, scored on its own at a lower weight and **never mixed into Dhana**.

They are wired into the **baby-birth Muhurta** (Dhana → the *wealth* verdict,
Prosperity → the *fortune* verdict; each Lagna window exposes both score + links)
and into this ranking as two separate features. Honest note: astrologically
faithful (a strong, well-placed yoga outscores a fallen one) but neither improves
fame separation (both yogas are ~equally common in famous & ordinary charts) — they
are wealth/fortune readouts, not fame predictors.

### Graded Raja yoga
`api/app/services/kundli_calculator/raja_yoga.py` grades the classical Raja yoga —
association of a **Kendra lord (1/4/7/10)** with a **Trikona lord (1/5/9)** — as
`connection × lord-grade × dignity × house-of-formation × combustion`:

- **lord-grade** — 9th+10th (Dharma-Karmadhipati) supreme, then any pair with the
  1st (Lagnesh), all four kendras otherwise equal;
- **house** — Kendra best > Trikona > 2/11 > 3 > dusthana 6/8/12 (placement is the
  decisive lever);
- **combustion** — a yoga-planet too close to the Sun is burnt (×0.5 each), which
  dignity alone can't catch.

It feeds the Muhurta **career/status** verdict and replaces the crude trikona
feature in this ranking. Example: Nandish's 9L↔10L parivartana (a "supreme"
Dharma-Karmadhipati) scores only ~2.1 — Venus debilitated **and** Mercury combust.

---

## Contents

```
ReadMe/
├── README.md                        ← this file
├── methodology.html                 ← the 8 factors + composite, explained (open in a browser)
├── data/
│   ├── ordinary_birth_data.json     ← clean birth inputs, re-importable  ← canonical input list
│   ├── ordinary_birth_data.md       ← same, human-readable table
│   ├── famous_vs_ordinary_ranking.md← all 128 charts ranked by famous-likeness
│   ├── famous-charts-reference.md   ← famous gold-set reference (ratings, sources)
│   └── unshakable-chart-finder-plan.md
└── scripts/
    ├── gen_normal.py     ← birth inputs → full databank (add charts here)
    ├── compare_real.py   ← famous-vs-ordinary verification (CV-AUC + lifts)
    ├── score_ranking.py  ← full 128-chart ranking
    ├── breakdown.py      ← per-chart weights + line-by-line "why this score"
    └── gen_reusable.py   ← export birth data → JSON/MD
```

### The full chart data lives in the app (single source of truth — not duplicated here)
- **`src/data/celebrities.json`** — 37 famous charts (D1–D60 + dasha + bios), served on `/celebrities`
- **`src/data/ordinary.json`** — 96 ordinary charts (D1–D60 + dasha), served on `/ordinary`

`data/ordinary_birth_data.*` is just the clean birth-**input** slice of `ordinary.json`
(regenerate it with `scripts/gen_reusable.py`).

---

## How to reproduce

The scripts import the backend chart engine, so they run **inside the API Docker
container**:

```bash
# copy a script in and run it
docker cp ReadMe/scripts/compare_real.py vedicjivan-api:/app/compare_real.py
docker exec -w /app vedicjivan-api python compare_real.py
```

To **add ordinary charts**: append `(name, sex, "YYYY-MM-DD", "HH:MM", place, lat, lon)`
tuples to the `NORMAL` list in `scripts/gen_normal.py`, then:

```bash
docker cp ReadMe/scripts/gen_normal.py vedicjivan-api:/app/gen_normal.py
docker exec -w /app vedicjivan-api python gen_normal.py           # regenerate
docker cp vedicjivan-api:/app/normal_people.json src/data/ordinary.json
```

---

## Caveats

- **Birth-time accuracy** is the main risk for ordinary charts (must be from
  records, not guessed).
- The signal is **weak (~0.57)** — treat it as a tendency of the crowd, not a
  verdict on any individual chart.
- Pre-~1910 charts use LMT that may be off ±30 min until LMT handling is added.
