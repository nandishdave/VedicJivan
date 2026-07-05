"""13-domain life analysis + the Balanced-Life score.

Each life domain is judged by the classical **four-fold** method — the way an
astrologer reads any bhāva:

  ① **Bhāveśa** (house-lord, 30%)  — its dignity (sign) + placement (house) +
     a Shadbala nudge, minus Pāpa-Kartari if it is hemmed by malefics.
  ② **Bhāva**   (the house, 28%)   — its Ashtakavarga bindus, benefic/malefic
     occupants, aspects (dṛṣṭi), and Pāpa/Śubha-Kartari on the house.
  ③ **Varga**   (divisional, 30%)  — the area's own divisional chart judged as a
     chart: its lagna-lord, its relevant house (e.g. the 5th-of-D7 for children,
     with occupants + kartari), and the kāraka's dignity — all inside the varga.
  ④ **Kāraka**  (significator, 12%) — the natural significator's Shadbala.

Domains with no clean varga (Longevity uses D8/Aṣṭāṁśa; Foreign has none) fall
back — the score is renormalised across the remaining factors so no factor is
"missing points".

``balanced_life(chart)`` rolls the 13 domains into ONE "how complete is this
life" percentage using a **weakest-links** aggregation (mean + weakest-three +
minimum), so one empty domain visibly drags the score: a chart strong in career/
wealth but empty in marriage/children does NOT read as a great life. It also
names the 2-3 weakest domains as ``concerns``.

This is a CLASSICAL bhāva-strength reading — NOT statistically validated against
real-life outcomes (unlike ``worldly_potential``'s fame model). Interpret it as a
considered classical judgment. All weights below are tunable and documented in
``.local/uncertainty_log.md``. Shared by the Muhurta engine and the Unshakable
finder so both read life-completeness identically.
"""
from __future__ import annotations

from app.services.kundli_calculator._core import SIGN_LORDS, _get_dignity
# Shared 0-100 dignity scale + average-SAV — one source of truth (dignity.py).
from app.services.kundli_calculator.dignity import (
    AVG_SAV as _AVG_SAV,
    DIGNITY_PCT as _DIG100,
)

# ── Functional-benefic scheme (lagna-specific two-group) ─────────────────────
# The Moon is judged by paksha (waxing = benefic); the 6 other classical planets
# by their FUNCTIONAL nature for this lagna (a natural benefic like Jupiter is a
# functional malefic for Libra); Rahu/Ketu inherit their dispositor's nature.
_FB_A = {"Saturn", "Venus", "Mercury"}       # for Ta, Ge, Vi, Li, Cp, Aq lagnas
_FB_B = {"Sun", "Moon", "Mars", "Jupiter"}   # for Ar, Cn, Le, Sc, Sg, Pi lagnas
_FB_A_SIGNS = {1, 2, 5, 6, 9, 10}
_KENDRA = {1, 4, 7, 10}
_TRIKONA = {1, 5, 9}
_DUSTHANA = {6, 8, 12}
# The 9 bodies that count as occupants / hemmers (7 classical + the nodes).
_CLASSICAL = ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu")
# ±20 dignity scale used by the legacy combined _house_strength (kept for compat).
_DIGNITY_PTS = {
    "Exalted": 20, "Moolatrikona": 16, "Own Sign": 14, "Friendly Sign": 7,
    "Neutral Sign": 0, "Enemy Sign": -8, "Debilitated": -18,
}
# _DIG100 (0-100 dignity ladder) and _AVG_SAV are imported from dignity.py above.

# Four-fold weights (must sum to 1.0). Bhāveśa & Varga lead; Kāraka is the light
# day-level modifier (it is the SAME across all 12 muhurta Lagnas).
_W_BHAVESH, _W_BHAVA, _W_VARGA, _W_KARAKA = 0.30, 0.28, 0.30, 0.12
_KARTARI_PAPA, _KARTARI_SHUBHA = -12.0, 8.0

# ── The 13 life domains → (key, label, group, houses[primary first], karakas, vargas) ─
# `vargas` = the divisional chart(s) that confirm this area (empty = 3-factor).
LIFE_ASPECTS: list[tuple[str, str, str, list[int], list[str], list[str]]] = [
    ("health",    "Health & Vitality",     "Self & Body",    [1, 6, 8],  ["Sun"],                ["D30"]),
    ("longevity", "Longevity",             "Self & Body",    [8, 1, 3],  ["Saturn"],             ["D8"]),
    ("wealth",    "Wealth & Finances",     "Material",       [2, 11],    ["Jupiter"],            ["D2"]),
    ("career",    "Career & Status",       "Material",       [10, 6],    ["Sun", "Saturn"],      ["D10"]),
    ("property",  "Property & Comforts",   "Material",       [4],        ["Mars", "Venus"],      ["D4", "D16"]),
    ("marriage",  "Marriage & Spouse",     "Relationships",  [7],        ["Venus"],              ["D9"]),
    ("children",  "Children & Progeny",    "Relationships",  [5],        ["Jupiter"],            ["D7"]),
    ("siblings",  "Siblings & Support",    "Relationships",  [3],        ["Mars"],               ["D3"]),
    ("family",    "Family Harmony",        "Relationships",  [4, 2],     ["Moon", "Venus"],      ["D12"]),
    ("education", "Education & Intellect",  "Mind & Growth",  [4, 5, 9],  ["Mercury", "Jupiter"], ["D24"]),
    ("fortune",   "Fortune & Dharma",      "Mind & Growth",  [9],        ["Jupiter", "Sun"],     ["D9"]),
    ("foreign",   "Foreign & Travel",      "Beyond",         [12, 9, 3], ["Rahu"],               []),
    ("spiritual", "Spirituality",          "Beyond",         [12, 9, 5], ["Ketu", "Jupiter"],    ["D20"]),
]


# ── Functional benefic / malefic ─────────────────────────────────────────────
def _moon_waxing(chart: dict) -> bool:
    phase = (chart["planets"]["Moon"]["longitude"] - chart["planets"]["Sun"]["longitude"]) % 360
    return phase < 180


def _functional_benefics(chart: dict) -> set:
    """Functional benefics for this chart's ascendant (lagna-specific)."""
    return _FB_A if chart["lagna"]["sign"] in _FB_A_SIGNS else _FB_B


def _node_dispositor(chart: dict, node: str) -> str:
    """Sign-lord of the node's sign — Rahu/Ketu rule no sign, so they take the
    functional nature of their dispositor (the classical rule for the nodes)."""
    return SIGN_LORDS[chart["planets"][node]["sign"]]


def _is_benefic(chart: dict, p: str) -> bool:
    if p == "Moon":
        return _moon_waxing(chart)
    if p in ("Rahu", "Ketu"):
        return _is_benefic(chart, _node_dispositor(chart, p))
    return p in _functional_benefics(chart)


def _is_malefic(chart: dict, p: str) -> bool:
    if p == "Moon":
        return not _moon_waxing(chart)
    if p in ("Rahu", "Ketu"):
        return _is_malefic(chart, _node_dispositor(chart, p))
    return p not in _functional_benefics(chart)


# ── Small helpers ────────────────────────────────────────────────────────────
def _ratio100(ratio: float) -> float:
    """Shadbala ratio (rūpas / min requirement) → 0-100 (1.0 → ~67, ≥1.5 → 100)."""
    return max(0.0, min(ratio / 1.5, 1.0)) * 100.0


def _dig100(planet: str, sign: int) -> float:
    """0-100 dignity of ``planet`` in ``sign`` (any sign, incl. a varga sign)."""
    return _DIG100.get(_get_dignity(planet, sign), 45.0)


def _d1_house_map(chart: dict) -> dict:
    return {p: chart["planets"][p]["house"]
            for p in _CLASSICAL
            if p in chart["planets"] and "house" in chart["planets"][p]}


def _kartari(chart: dict, house_map: dict, house: int) -> float:
    """Pāpa/Śubha Kartari: what hems a house (or a planet's house). Both flanking
    houses malefic → −12; both benefic → +8; one-sided/mixed → 0. ``house_map`` is
    {body: house} in whichever chart (D1 or a varga)."""
    prev_h = ((house - 2) % 12) + 1
    next_h = (house % 12) + 1
    prev_occ = [p for p, h in house_map.items() if h == prev_h]
    next_occ = [p for p, h in house_map.items() if h == next_h]
    if not prev_occ or not next_occ:
        return 0.0
    if all(_is_malefic(chart, p) for p in prev_occ) and all(_is_malefic(chart, p) for p in next_occ):
        return _KARTARI_PAPA
    if all(_is_benefic(chart, p) for p in prev_occ) and all(_is_benefic(chart, p) for p in next_occ):
        return _KARTARI_SHUBHA
    return 0.0


# ── Legacy combined house strength — kept for the muhurta re-export + tests ───
def _house_strength(chart: dict, house: int) -> float:
    """0–100 combined strength of one Whole-Sign house (bhāva + bhāveśa merged).
    Retained for backward-compatible callers/tests; the four-fold scorer below
    splits these into explicit factors."""
    lagna_sign = chart["lagna"]["sign"]
    sign = (lagna_sign + house - 1) % 12
    score = 50.0
    score += (chart["ashtakavarga"]["totals"][sign] - _AVG_SAV) * 1.6
    lord = SIGN_LORDS[sign]
    lp = chart["planets"].get(lord)
    if lp:
        score += _DIGNITY_PTS.get(lp["dignity"], 0) * 0.9
        lh = lp["house"]
        if lh in _TRIKONA:
            score += 10
        elif lh in _KENDRA:
            score += 7
        elif lh in _DUSTHANA:
            score -= 12
    for pname, pdata in chart["planets"].items():
        if pname not in _CLASSICAL:
            continue
        if pdata["house"] == house:
            if _is_benefic(chart, pname):
                score += 8
            elif _is_malefic(chart, pname):
                score -= 8
    for asp in chart.get("graha_drishti", {}).get("house_aspected_by", {}).get(str(house), []):
        if _is_benefic(chart, asp):
            score += 4
        elif _is_malefic(chart, asp):
            score -= 4
    return max(0.0, min(100.0, score))


# ── ① Bhāveśa (house-lord) 0–100 ─────────────────────────────────────────────
def _bhavesh_score(chart: dict, house: int) -> float:
    sign = (chart["lagna"]["sign"] + house - 1) % 12
    lord = SIGN_LORDS[sign]
    lp = chart["planets"].get(lord)
    if not lp:
        return 45.0
    val = _DIG100.get(lp.get("dignity"), 45.0)          # dignity (sign) of the lord
    lh = lp.get("house", 0)                              # placement (house) of the lord
    val += (12.0 if lh in _TRIKONA else 8.0 if lh in _KENDRA
            else 3.0 if lh in (2, 3, 11) else -22.0 if lh in _DUSTHANA else 0.0)
    sb = chart.get("shadbala", {}).get(lord, {})         # real six-fold strength nudge
    if "ratio" in sb:
        val = 0.75 * val + 0.25 * _ratio100(sb["ratio"])
    val += _kartari(chart, _d1_house_map(chart), lh)     # is the lord hemmed?
    return max(0.0, min(100.0, val))


# ── ② Bhāva (the house itself) 0–100 ─────────────────────────────────────────
def _bhava_score(chart: dict, house: int) -> float:
    sign = (chart["lagna"]["sign"] + house - 1) % 12
    val = 50.0 + (chart["ashtakavarga"]["totals"][sign] - _AVG_SAV) * 1.6
    for p in _CLASSICAL:                                  # occupants
        if chart["planets"].get(p, {}).get("house") == house:
            val += 8.0 if _is_benefic(chart, p) else (-8.0 if _is_malefic(chart, p) else 0.0)
    for asp in chart.get("graha_drishti", {}).get("house_aspected_by", {}).get(str(house), []):
        val += 4.0 if _is_benefic(chart, asp) else (-4.0 if _is_malefic(chart, asp) else 0.0)
    val += _kartari(chart, _d1_house_map(chart), house)  # is the house hemmed?
    return max(0.0, min(100.0, val))


# ── ③ Varga (divisional chart, judged as a chart) 0–100 ──────────────────────
def _varga_score(chart: dict, house: int, karakas: list[str], vargas: list[str] | None) -> float | None:
    if not vargas:
        return None
    div = chart.get("divisional") or {}
    parts: list[float] = []
    for V in vargas:
        vc = div.get(V)
        if not vc or "Lagna" not in vc:
            continue
        vlag = vc["Lagna"]
        # house of each body within this varga (whole-sign from the varga lagna)
        hmap = {p: ((vc[p] - vlag) % 12) + 1 for p in _CLASSICAL if p in vc}
        # (a) varga lagna-lord dignity in the varga (the native in this chart)
        vlord = SIGN_LORDS[vlag]
        s_lagna = _dig100(vlord, vc[vlord]) if vlord in vc else 45.0
        # (b) the relevant varga house (Hth from the varga lagna): its lord's
        #     dignity + benefic/malefic occupants + kartari on it
        vh_sign = (vlag + house - 1) % 12
        vh_lord = SIGN_LORDS[vh_sign]
        s_hlord = _dig100(vh_lord, vc[vh_lord]) if vh_lord in vc else 45.0
        occ = 50.0
        for p in _CLASSICAL:
            if hmap.get(p) == house:
                occ += 8.0 if _is_benefic(chart, p) else (-8.0 if _is_malefic(chart, p) else 0.0)
        occ += _kartari(chart, hmap, house)
        s_house = 0.6 * s_hlord + 0.4 * max(0.0, min(100.0, occ))
        # (c) kāraka dignity in the varga
        kv = [_dig100(k, vc[k]) for k in karakas if k in vc]
        s_karaka = sum(kv) / len(kv) if kv else 45.0
        parts.append(0.45 * s_house + 0.30 * s_lagna + 0.25 * s_karaka)
    return sum(parts) / len(parts) if parts else None


# ── ④ Kāraka (natural significator) 0–100 ────────────────────────────────────
def _karaka_score(chart: dict, karakas: list[str]) -> float:
    sb = chart.get("shadbala", {})
    vals: list[float] = []
    for k in karakas:
        if k in sb and "ratio" in sb[k]:
            vals.append(_ratio100(sb[k]["ratio"]))
        elif k in chart["planets"]:
            vals.append(_DIG100.get(chart["planets"][k].get("dignity"), 45.0))
    return sum(vals) / len(vals) if vals else 50.0


def _aspect_score(chart: dict, houses: list[int], karakas: list[str],
                  vargas: list[str] | None = None) -> float:
    """The four-fold domain score 0–100. ``vargas=None`` (or empty, or no
    divisional on the chart) → renormalise across Bhāveśa/Bhāva/Kāraka."""
    primary = houses[0]
    bhava = _bhava_score(chart, primary)
    if len(houses) > 1:  # secondary houses fold lightly into the Bhāva term
        sec = sum(_bhava_score(chart, h) for h in houses[1:]) / len(houses[1:])
        bhava = 0.73 * bhava + 0.27 * sec
    bhavesh = _bhavesh_score(chart, primary)
    karaka = _karaka_score(chart, karakas)
    varga = _varga_score(chart, primary, karakas, vargas)
    if varga is None:
        tot = _W_BHAVESH + _W_BHAVA + _W_KARAKA
        return round((_W_BHAVESH * bhavesh + _W_BHAVA * bhava + _W_KARAKA * karaka) / tot, 1)
    return round(_W_BHAVESH * bhavesh + _W_BHAVA * bhava + _W_VARGA * varga + _W_KARAKA * karaka, 1)


def _verdict(score: float) -> str:
    if score >= 60:
        return "good"
    if score >= 45:
        return "moderate"
    return "challenging"


def domain_scores(chart: dict) -> dict:
    """The 13 life domains scored 0–100 by the four-fold method, keyed by aspect.
    Each value: ``{label, group, score, verdict}``. Single source of truth for the
    per-domain life reading — Muhurta and the Unshakable finder both call it."""
    out: dict = {}
    for key, label, group, houses, karakas, vargas in LIFE_ASPECTS:
        sc = _aspect_score(chart, houses, karakas, vargas)
        out[key] = {"label": label, "group": group, "score": sc, "verdict": _verdict(sc)}
    return out


# ── Balanced-Life aggregation ────────────────────────────────────────────────
# A weakest-links blend (tunable): the mean rewards breadth, but the weakest-3
# mean and the single minimum guarantee one empty domain drags the score — a
# great career cannot hide a null marriage. e.g. twelve strong domains (~85) and
# one null (~5) reads ~60%, "a good life with a serious gap", not ~80%.
_BAL_W_MEAN, _BAL_W_WEAK3, _BAL_W_MIN = 0.45, 0.35, 0.20
_CONCERN_BAR = 50.0   # a domain scoring below this is flagged as an area of concern


def _bal_band(score: float) -> str:
    if score >= 68:
        return "Very complete"
    if score >= 56:
        return "Well-rounded"
    if score >= 46:
        return "Mixed"
    return "Uneven"


def balanced_life(chart: dict, domains: dict | None = None) -> dict:
    """0–100 "how complete is this life" + the 2-3 weakest domains as ``concerns``.

    ``domains`` — an optional pre-computed ``domain_scores()`` dict. The Muhurta
    engine passes its own so the % matches the columns it already displays;
    omitted on the Unshakable path, where it is computed here.
    """
    if domains is None:
        domains = domain_scores(chart)
    items = [(k, d["label"], d["score"]) for k, d in domains.items()]
    scores = sorted(s for _, _, s in items)
    n = len(scores) or 1
    mean = sum(scores) / n
    weak3 = sum(scores[:3]) / min(3, n)
    lo = scores[0] if scores else 0.0
    score = round(_BAL_W_MEAN * mean + _BAL_W_WEAK3 * weak3 + _BAL_W_MIN * lo, 1)
    concerns = [lbl for _, lbl, s in sorted(items, key=lambda x: x[2]) if s < _CONCERN_BAR][:3]
    return {
        "score": score,
        "band": _bal_band(score),
        "concerns": concerns,
        "domains": {k: d["score"] for k, d in domains.items()},
    }
