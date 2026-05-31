"""Dosha detection — classical Vedic afflictions in the birth chart.

Covers Kaal Sarp (+variants), Pitra, Guru Chandal, Grahan (solar/lunar),
Angarak, Vish, Shakat. Excludes Manglik (in manglik.py) and Sade Sati
(in sadesati.py) — those have their own dedicated modules.

References: BPHS, Phaladeepika, B.V. Raman "300 Important Combinations."
"""

from __future__ import annotations


def calc_doshas(planets: dict, lagna: dict) -> list[dict]:
    """Detect classical Vedic doshas (afflictions) in the birth chart.

    Returns a list of present doshas. Each entry has:
      name, type, description, planets (list), house (int|None)
      + optional severity (for Kaal Sarp only)

    Note: Mangal Dosha and Sade Sati are handled by calc_manglik() and
    calc_sadesati() separately — they are NOT duplicated here.

    Types: kaal_sarp | pitra | guru_chandal | grahan | angarak | vish | shakat
    Reference: BPHS, Phaladeepika, B.V. Raman "300 Important Combinations"
    """
    CLASSICAL = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    _KAAL_SARP_NAMES = [
        "Anant", "Kulik", "Vasuki", "Shankhapal", "Padma", "Mahapadma",
        "Takshak", "Karkotak", "Shankachood", "Ghatak", "Vishdhar", "Sheshnag",
    ]
    doshas: list[dict] = []

    def psign(p: str) -> int:
        return planets[p]["sign"] if p in planets else -1

    def phouse(p: str) -> int | None:
        return planets[p]["house"] if p in planets else None

    def plon(p: str) -> float:
        return planets[p]["longitude"] if p in planets else 0.0

    def same_sign(p1: str, p2: str) -> bool:
        return p1 in planets and p2 in planets and psign(p1) == psign(p2)

    # ── 1. Kaal Sarp Dosha ───────────────────────────────────────────────────
    if "Rahu" in planets and "Ketu" in planets:
        rahu_lon = plon("Rahu")
        present_classical = [p for p in CLASSICAL if p in planets]
        arcs = [(plon(p) - rahu_lon) % 360 for p in present_classical]

        planets_between = sum(1 for a in arcs if a < 180)
        planets_outside = sum(1 for a in arcs if a > 180)
        total = len(present_classical)

        if planets_between == total:
            rahu_house = phouse("Rahu") or 1
            variant = _KAAL_SARP_NAMES[rahu_house - 1]
            doshas.append({
                "name": f"Kaal Sarp Dosha — {variant}",
                "type": "kaal_sarp",
                "description": (
                    f"All planets are hemmed between Rahu ({rahu_house}th house) and Ketu. "
                    f"{variant} variant — challenges related to the {rahu_house}th house significations. "
                    f"Indicates karmic restriction of life force by the serpent axis."
                ),
                "planets": ["Rahu", "Ketu"] + present_classical,
                "house": rahu_house,
                "severity": "full",
            })
        elif planets_outside == total:
            doshas.append({
                "name": "Kaal Amrit Yoga",
                "type": "kaal_sarp",
                "description": (
                    "All planets are on the Ketu-to-Rahu arc (reverse Kaal Sarp). "
                    "Associated with spiritual depth, fame after hardship, and liberation energy."
                ),
                "planets": ["Rahu", "Ketu"] + present_classical,
                "house": phouse("Ketu"),
                "severity": "reverse",
            })
        elif planets_between >= 5:
            rahu_house = phouse("Rahu") or 1
            variant = _KAAL_SARP_NAMES[rahu_house - 1]
            doshas.append({
                "name": f"Partial Kaal Sarp Dosha — {variant}",
                "type": "kaal_sarp",
                "description": (
                    f"{planets_between} of {total} planets hemmed between Rahu and Ketu. "
                    f"Partial {variant} Kaal Sarp — milder effect than full dosha."
                ),
                "planets": ["Rahu", "Ketu"],
                "house": rahu_house,
                "severity": "partial",
            })

    # ── 2. Pitra Dosha ───────────────────────────────────────────────────────
    pitra_reasons: list[str] = []
    pitra_planets: list[str] = ["Sun"]

    if same_sign("Sun", "Rahu"):
        pitra_reasons.append("Sun conjunct Rahu — ancestral confusion")
        pitra_planets.append("Rahu")
    if same_sign("Sun", "Ketu"):
        pitra_reasons.append("Sun conjunct Ketu — detachment from paternal lineage")
        if "Ketu" not in pitra_planets:
            pitra_planets.append("Ketu")
    if "Rahu" in planets and phouse("Rahu") == 9:
        pitra_reasons.append("Rahu in 9th house — affliction to house of father/dharma")
        if "Rahu" not in pitra_planets:
            pitra_planets.append("Rahu")
    if "Ketu" in planets and phouse("Ketu") == 9:
        pitra_reasons.append("Ketu in 9th house — ancestral karmic debt")
        if "Ketu" not in pitra_planets:
            pitra_planets.append("Ketu")
    if "Sun" in planets and "Saturn" in planets and same_sign("Sun", "Saturn") and phouse("Sun") == 9:
        pitra_reasons.append("Sun and Saturn conjunct in 9th — severe father-karma burden")
        if "Saturn" not in pitra_planets:
            pitra_planets.append("Saturn")

    if pitra_reasons:
        doshas.append({
            "name": "Pitra Dosha",
            "type": "pitra",
            "description": (
                "Ancestral debt indicated: " + "; ".join(pitra_reasons) + ". "
                "Challenges with father, paternal lineage, or receiving ancestral blessings. "
                "Remedy: Pitru Tarpan, Shradh rituals, charity on Amavasya."
            ),
            "planets": pitra_planets,
            "house": phouse("Sun"),
        })

    # ── 3. Guru Chandal Dosha ────────────────────────────────────────────────
    if same_sign("Jupiter", "Rahu"):
        doshas.append({
            "name": "Guru Chandal Dosha",
            "type": "guru_chandal",
            "description": (
                "Jupiter conjunct Rahu — Rahu corrupts Jupiter's wisdom and dharma. "
                "May manifest as misguided beliefs, unorthodox spirituality, or guru-related issues. "
                "Can also produce unconventional brilliance and esoteric inclination."
            ),
            "planets": ["Jupiter", "Rahu"],
            "house": phouse("Jupiter"),
        })
    elif same_sign("Jupiter", "Ketu"):
        doshas.append({
            "name": "Guru Chandal Dosha (Ketu)",
            "type": "guru_chandal",
            "description": (
                "Jupiter conjunct Ketu — spiritual detachment from conventional wisdom. "
                "Past-life spiritual karma, inclination toward moksha, or disconnection from dharmic guidance."
            ),
            "planets": ["Jupiter", "Ketu"],
            "house": phouse("Jupiter"),
        })

    # ── 4. Grahan Dosha ──────────────────────────────────────────────────────
    if same_sign("Sun", "Rahu") or same_sign("Sun", "Ketu"):
        afflicting = "Rahu" if same_sign("Sun", "Rahu") else "Ketu"
        doshas.append({
            "name": "Surya Grahan Dosha",
            "type": "grahan",
            "description": (
                f"Sun conjunct {afflicting} — solar eclipse pattern in natal chart. "
                "Identity confusion, authority challenges, difficulties with father. "
                "Soul's expression is partially eclipsed."
            ),
            "planets": ["Sun", afflicting],
            "house": phouse("Sun"),
        })

    if same_sign("Moon", "Rahu") or same_sign("Moon", "Ketu"):
        afflicting = "Rahu" if same_sign("Moon", "Rahu") else "Ketu"
        doshas.append({
            "name": "Chandra Grahan Dosha",
            "type": "grahan",
            "description": (
                f"Moon conjunct {afflicting} — lunar eclipse pattern in natal chart. "
                "Emotional instability, anxiety, difficult relationship with mother. "
                "Mind is susceptible to obsessive patterns."
            ),
            "planets": ["Moon", afflicting],
            "house": phouse("Moon"),
        })

    # ── 5. Angarak Dosha ─────────────────────────────────────────────────────
    if same_sign("Mars", "Rahu"):
        doshas.append({
            "name": "Angarak Dosha",
            "type": "angarak",
            "description": (
                "Mars conjunct Rahu — Rahu amplifies Mars's aggression to explosive levels. "
                "Risk of accidents, legal trouble, or impulsive outbursts. "
                "Can produce extraordinary ambition when channelled constructively."
            ),
            "planets": ["Mars", "Rahu"],
            "house": phouse("Mars"),
        })

    # ── 6. Vish Yoga ─────────────────────────────────────────────────────────
    if same_sign("Saturn", "Moon"):
        doshas.append({
            "name": "Vish Yoga",
            "type": "vish",
            "description": (
                "Saturn and Moon conjunct — Saturn suppresses Moon's emotional warmth. "
                "Tendency toward depression, emotional coldness, or difficult relationship with mother. "
                "Severity depends on Moon's sign strength."
            ),
            "planets": ["Saturn", "Moon"],
            "house": phouse("Moon"),
        })

    # ── 7. Shakat Yoga ───────────────────────────────────────────────────────
    if "Jupiter" in planets and "Moon" in planets:
        diff = (psign("Jupiter") - psign("Moon")) % 12
        if diff in (5, 7):
            doshas.append({
                "name": "Shakat Yoga",
                "type": "shakat",
                "description": (
                    "Jupiter in 6th or 8th from Moon — opposite of Gaja Kesari. "
                    "Fluctuating fortune, instability in career and finances, recurring obstacles. "
                    "Reduced if Jupiter is strong or in Kendra from Lagna."
                ),
                "planets": ["Jupiter", "Moon"],
                "house": phouse("Jupiter"),
            })

    return doshas
