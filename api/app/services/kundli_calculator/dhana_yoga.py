"""Graded Dhana-Yoga (wealth-yoga) strength for a chart.

Classical Dhana yogas form from the mutual association of the lords of the
"money axis" — houses 1 (self), 2 (accumulated wealth), 5 (purva-punya), 9
(fortune) and 11 (gains). Instead of a yes/no flag, this scores the yoga as a
single graded number so the *quality* of the yoga scales its strength:

    link score = connection-type  x  which-lords  x  dignity  x  house-of-formation

so an exalted Dhanesh+Labhesh conjunct in the 11th scores near the top, while a
"technically present but diluted" yoga (a fallen lord in a dusthana) scores low
but non-zero. This is deliberately faithful to the classical grading — a strong
yoga and a weak one are not treated alike.

Empirical note: this does NOT separate famous from ordinary charts (Dhana yogas
are roughly as common in both) — it is a *wealth-strength* readout, not a fame
predictor. See ReadMe/ (famous-vs-ordinary study).
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
_MONEY = (1, 2, 5, 9, 11)          # the money axis
_CORE = frozenset({1, 2, 11})      # self + wealth + gains carry full weight
_GOOD_HOUSES = frozenset({1, 2, 4, 5, 9, 10, 11})
_NORM = 4.5                        # raw→0..100 scale (strong yogas reach ~20-26 raw)


def _house_factor(h: int) -> float:
    """Where the yoga forms — good houses full strength, dusthanas diluted."""
    if h in _GOOD_HOUSES:
        return 1.0
    if h == 7:
        return 0.75
    if h == 3:
        return 0.5
    return 0.35  # dusthana 6 / 8 / 12


def dhana_yoga_score(chart: dict) -> tuple[float, list[dict]]:
    """Graded Dhana-yoga strength for a chart.

    Returns ``(score, links)`` where ``score >= 0`` and ``links`` describes each
    contributing connection (link name, type, avg dignity, house(s), sub-score).
    Deduplicated so a single physical conjunction is never counted twice.
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

    total = 0.0
    links: list[dict] = []

    # 1) a single planet owning two or more money-houses = an inherent link
    for p, hs in owns.items():
        if len(hs) >= 2:
            core_ct = len(hs & _CORE)
            mult = 1.0 if core_ct >= 2 else (0.7 if core_ct == 1 else 0.5)
            sc = _CONN["inherent"] * mult * dig(p) * _house_factor(house(p))
            total += sc
            links.append({
                "link": f"{p} owns {'&'.join(map(str, sorted(hs)))}",
                "type": "inherent", "dignity": round(dig(p), 2),
                "house": house(p), "score": round(sc, 2),
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
            total += sc
            links.append({
                "link": f"{a}({'&'.join(map(str, sorted(owns[a])))})-{b}({'&'.join(map(str, sorted(owns[b])))})",
                "type": t, "dignity": round(d, 2), "house": f"{ha}/{hb}", "score": round(sc, 2),
            })

    return round(total, 2), links


def dhana_yoga_normalized(chart: dict) -> float:
    """0–100 view of the Dhana-yoga score, for blending with the other 0–100
    house/karaka strengths in the Muhurta scorer."""
    score, _ = dhana_yoga_score(chart)
    return max(0.0, min(100.0, score * _NORM))
