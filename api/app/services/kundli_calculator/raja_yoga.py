"""Graded Raja-yoga strength for a chart.

A Raja yoga = association of a **Kendra lord** (1,4,7,10) with a **Trikona lord**
(1,5,9). The 6/8/12 (dusthana) lords are NOT raja-yoga partners. Each link is
graded so quality scales strength:

    link score = connection x lord-grade x dignity x house-of-formation x combustion

* connection — parivartana > raja-karaka(one planet owns a kendra+trikona) >
  conjunction > mutual aspect > one-way aspect
* lord-grade — 9th+10th (Dharma-Karmadhipati) is supreme; any pair with the 1st
  (Lagnesh) next; all four kendras otherwise weighted equally
* house-of-formation (the decisive lever) — Kendra best > Trikona > 2/11 >
  3rd > dusthana 6/8/12
* dignity — Exalted...Debilitated (a debilitated/enemy planet nearly kills it)
* combustion — a yoga-planet too close to the Sun is burnt: heavy penalty even
  when its sign-dignity looks fine (dignity alone cannot catch this)

Empirical note: like Dhana/Prosperity, this does not separate famous from
ordinary charts — it is a power/status readout, not a fame predictor.
"""
from __future__ import annotations

from app.services.kundli_calculator._core import SIGN_LORDS
from app.services.kundli_calculator.avasthas import _is_combust

_CONN = {
    "parivartana": 10,
    "raja_karaka": 9,     # a single planet owning a kendra AND a trikona
    "conjunction": 8,
    "mutual_aspect": 6,
    "aspect": 3,
}
_DIGF = {
    "Exalted": 1.0, "Moolatrikona": 0.9, "Own Sign": 0.8, "Friendly Sign": 0.6,
    "Neutral Sign": 0.45, "Enemy Sign": 0.25, "Debilitated": 0.1,
}
_KENDRA = frozenset({1, 4, 7, 10})
_TRIKONA = frozenset({1, 5, 9})
_COMBUST_PENALTY = 0.5     # per participating planet that is combust
_NORM = 4.5               # raw -> 0..100 scale


def _house_factor(h: int) -> float:
    """Where the yoga forms — placement is the decisive lever (user's ordering)."""
    if h in _KENDRA:            # 1,4,7,10
        return 1.0
    if h in (5, 9):             # trikona
        return 0.85
    if h in (2, 11):
        return 0.65
    if h == 3:
        return 0.5
    return 0.4                  # dusthana 6/8/12


def raja_yoga_score(chart: dict) -> tuple[float, list[dict]]:
    """Graded Raja-yoga strength. Returns ``(score, links)``."""
    planets = chart["planets"]
    lagna_sign = chart["lagna"]["sign"]
    aspects = chart.get("graha_drishti", {}).get("planet_aspects", {})

    owns: dict[str, set[int]] = {}
    for h in range(1, 13):
        owns.setdefault(SIGN_LORDS[(lagna_sign + h - 1) % 12], set()).add(h)

    def dig(p: str) -> float:
        return _DIGF.get(planets[p].get("dignity"), 0.45)

    def house(p: str) -> int:
        return planets[p]["house"]

    def combust_factor(*ps: str) -> float:
        f = 1.0
        for p in ps:
            if _is_combust(p, planets):
                f *= _COMBUST_PENALTY
        return f

    def grade(hs_a: set[int], hs_b: set[int]) -> float:
        # Dharma-Karmadhipati (9th + 10th lords) is supreme; Lagnesh next.
        if (9 in hs_a and 10 in hs_b) or (10 in hs_a and 9 in hs_b):
            return 1.30
        if 1 in hs_a or 1 in hs_b:
            return 1.15
        return 1.0

    total = 0.0
    links: list[dict] = []

    # 1) raja-yoga karaka: one planet owning a kendra AND a trikona (not just the 1st)
    for p, hs in owns.items():
        k, t = hs & _KENDRA, hs & _TRIKONA
        if k and t and (k | t) != {1}:
            sc = _CONN["raja_karaka"] * grade(hs, hs) * dig(p) * _house_factor(house(p)) * combust_factor(p)
            total += sc
            links.append({
                "link": f"{p} owns {'&'.join(map(str, sorted(hs & (_KENDRA | _TRIKONA))))}",
                "type": "raja_karaka", "dignity": round(dig(p), 2), "house": house(p),
                "combust": _is_combust(p, planets), "score": round(sc, 2),
            })

    # 2) a kendra-lord planet associating with a (distinct) trikona-lord planet
    pls = list(owns.keys())
    for i in range(len(pls)):
        for j in range(i + 1, len(pls)):
            a, b = pls[i], pls[j]
            ka, ta = owns[a] & _KENDRA, owns[a] & _TRIKONA
            kb, tb = owns[b] & _KENDRA, owns[b] & _TRIKONA
            # one must fill the kendra role, the other the trikona role
            if not ((ka and tb) or (ta and kb)):
                continue
            ha, hb = house(a), house(b)
            if SIGN_LORDS[planets[a]["sign"]] == b and SIGN_LORDS[planets[b]["sign"]] == a:
                ty = "parivartana"
            elif ha == hb:
                ty = "conjunction"
            elif hb in aspects.get(a, []) and ha in aspects.get(b, []):
                ty = "mutual_aspect"
            elif hb in aspects.get(a, []) or ha in aspects.get(b, []):
                ty = "aspect"
            else:
                continue
            d = (dig(a) + dig(b)) / 2
            hf = _house_factor(ha) if ty == "conjunction" else (_house_factor(ha) + _house_factor(hb)) / 2
            sc = _CONN[ty] * grade(owns[a], owns[b]) * d * hf * combust_factor(a, b)
            total += sc
            links.append({
                "link": f"{a}({'&'.join(map(str, sorted(owns[a] & (_KENDRA | _TRIKONA))))})"
                        f"-{b}({'&'.join(map(str, sorted(owns[b] & (_KENDRA | _TRIKONA))))})",
                "type": ty, "dignity": round(d, 2), "house": f"{ha}/{hb}",
                "combust": _is_combust(a, planets) or _is_combust(b, planets), "score": round(sc, 2),
            })

    return round(total, 2), links


def raja_yoga_normalized(chart: dict) -> float:
    """0–100 view of the Raja-yoga score, for blending into the Muhurta
    career/status verdict."""
    score, _ = raja_yoga_score(chart)
    return max(0.0, min(100.0, score * _NORM))
