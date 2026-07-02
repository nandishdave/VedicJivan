"""Graded Dhana-yoga (wealth) + Prosperity (fortune) strength for a chart.

Two SEPARATE graded scores, deliberately not mixed:

* **Dhana yoga** — the tight wealth yoga: association of the lords of the *core
  money houses* 1 (self / Lagnesh), 2 (accumulated wealth / Dhanesh) and 11
  (gains / Labhesh). This is "am I wealthy".

* **Prosperity yoga** — the wider fortune extension: any association that also
  touches the 5th (purva-punya) or 9th (bhagya) lords. Classical texts fold these
  into Dhana yogas, but they are dharma/fortune links, not pure Dhanesh–Labhesh
  wealth — so they are scored on their own, at the naturally lower weight their
  non-core lords carry, and never added into the Dhana number.

Each link is graded ``connection-type x which-lords x dignity x house-of-formation``
so a strong, well-placed yoga outscores a "technically present but diluted" one
(a fallen lord in a dusthana scores low but non-zero).

Empirical note: neither score separates famous from ordinary charts (both yogas
are ~equally common in both) — these are wealth/fortune readouts, not fame
predictors. See ReadMe/ (famous-vs-ordinary study).
"""
from __future__ import annotations

from app.services.kundli_calculator._core import SIGN_LORDS

# connection type → base points (strongest → weakest)
_CONN = {
    "parivartana": 10,    # mutual exchange of signs
    "conjunction": 8,     # same house
    "inherent": 7,        # a single planet owning two money-houses
    "mutual_aspect": 6,   # both aspect each other
    "aspect": 3,          # one-way aspect
}
# dignity of a participating planet → factor (Exalted → Debilitated)
_DIGF = {
    "Exalted": 1.0, "Moolatrikona": 0.9, "Own Sign": 0.8, "Friendly Sign": 0.6,
    "Neutral Sign": 0.45, "Enemy Sign": 0.25, "Debilitated": 0.1,
}
_MONEY = (1, 2, 5, 9, 11)          # money + fortune axis
_CORE = frozenset({1, 2, 11})      # Dhana: self + wealth + gains
_EXT = frozenset({5, 9})           # Prosperity: purva-punya + fortune
_GOOD_HOUSES = frozenset({1, 2, 4, 5, 9, 10, 11})
_NORM = 4.5                        # raw→0..100 scale (strong yogas reach ~15-25 raw)


def _house_factor(h: int) -> float:
    """Where the yoga forms — good houses full strength, dusthanas diluted."""
    if h in _GOOD_HOUSES:
        return 1.0
    if h == 7:
        return 0.75
    if h == 3:
        return 0.5
    return 0.35  # dusthana 6 / 8 / 12


def _all_links(chart: dict) -> tuple[list[dict], list[dict]]:
    """All graded money-lord links, split into ``(dhana_links, prosperity_links)``.

    A link is *Dhana* only when every money-house it touches is core {1,2,11};
    any link touching the 5th or 9th is bucketed as *Prosperity*. Deduplicated so
    one physical connection is never counted twice.
    """
    planets = chart["planets"]
    lagna_sign = chart["lagna"]["sign"]
    aspects = chart.get("graha_drishti", {}).get("planet_aspects", {})

    lord = {h: SIGN_LORDS[(lagna_sign + h - 1) % 12] for h in _MONEY}
    owns: dict[str, set[int]] = {}
    for h in _MONEY:
        owns.setdefault(lord[h], set()).add(h)

    def dig(p: str) -> float:
        return _DIGF.get(planets[p].get("dignity"), 0.45)

    def house(p: str) -> int:
        return planets[p]["house"]

    dhana: list[dict] = []
    prosperity: list[dict] = []

    def bucket(houses_touched: set[int]) -> list[dict]:
        return dhana if houses_touched <= _CORE else prosperity

    # 1) a single planet owning two or more money-houses = an inherent link
    for p, hs in owns.items():
        if len(hs) >= 2:
            core_ct = len(hs & _CORE)
            mult = 1.0 if core_ct >= 2 else (0.7 if core_ct == 1 else 0.5)
            sc = _CONN["inherent"] * mult * dig(p) * _house_factor(house(p))
            bucket(hs).append({
                "link": f"{p} owns {'&'.join(map(str, sorted(hs)))}",
                "type": "inherent", "dignity": round(dig(p), 2),
                "house": house(p), "score": round(sc, 2), "planets": [p],
            })

    # 2) mutual association between two distinct money-lords
    pls = list(owns.keys())
    for i in range(len(pls)):
        for j in range(i + 1, len(pls)):
            a, b = pls[i], pls[j]
            ha, hb = house(a), house(b)
            if SIGN_LORDS[planets[a]["sign"]] == b and SIGN_LORDS[planets[b]["sign"]] == a:
                t = "parivartana"
            elif ha == hb:
                t = "conjunction"
            elif hb in aspects.get(a, []) and ha in aspects.get(b, []):
                t = "mutual_aspect"
            elif hb in aspects.get(a, []) or ha in aspects.get(b, []):
                t = "aspect"
            else:
                continue
            ca, cb = owns[a] & _CORE, owns[b] & _CORE
            mult = 1.0 if (ca and cb) else (0.7 if (ca or cb) else 0.5)
            d = (dig(a) + dig(b)) / 2
            hf = _house_factor(ha) if t == "conjunction" else (_house_factor(ha) + _house_factor(hb)) / 2
            sc = _CONN[t] * mult * d * hf
            bucket(owns[a] | owns[b]).append({
                "link": f"{a}({'&'.join(map(str, sorted(owns[a])))})-{b}({'&'.join(map(str, sorted(owns[b])))})",
                "type": t, "dignity": round(d, 2), "house": f"{ha}/{hb}", "score": round(sc, 2), "planets": [a, b],
            })

    return dhana, prosperity


def dhana_yoga_score(chart: dict) -> tuple[float, list[dict]]:
    """Option A — strict Dhana yoga: lords of 1, 2, 11 only. ``(score, links)``."""
    dhana, _ = _all_links(chart)
    return round(sum(link["score"] for link in dhana), 2), dhana


def prosperity_yoga_score(chart: dict) -> tuple[float, list[dict]]:
    """Option B — Prosperity/fortune extension: links touching the 5th/9th lord,
    scored separately (never mixed into Dhana). ``(score, links)``."""
    _, prosperity = _all_links(chart)
    return round(sum(link["score"] for link in prosperity), 2), prosperity


def dhana_yoga_normalized(chart: dict) -> float:
    """0–100 view of the Dhana score, for blending with the 0–100 house/karaka
    strengths in the Muhurta wealth verdict."""
    score, _ = dhana_yoga_score(chart)
    return max(0.0, min(100.0, score * _NORM))


def prosperity_yoga_normalized(chart: dict) -> float:
    """0–100 view of the Prosperity score, for blending into the Muhurta fortune
    verdict."""
    score, _ = prosperity_yoga_score(chart)
    return max(0.0, min(100.0, score * _NORM))
