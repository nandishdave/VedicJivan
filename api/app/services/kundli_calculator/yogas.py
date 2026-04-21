"""Yoga detection — classical Vedic yoga patterns in the birth chart.

Detects 11+ classical yogas: Pancha Mahapurusha (Ruchaka, Bhadra, Hamsa,
Malavya, Sasa), Gaja Kesari, Budhaditya, Chandra Mangala, the four Moon
yogas (Sunapha/Anapha/Durudhara/Kemdrum), Dharma Karmadhipati, Viparita
Raja (Harsha/Sarala/Vimala), Neecha Bhanga Raja, Amala, Lakshmi, Adhi.

References: BPHS Ch.36, Phaladeepika Ch.6-7, B.V. Raman "300 Important
Combinations."
"""

from __future__ import annotations

from ._core import _EXALTATION, _MOOLATRIKONA, _OWN_SIGNS, SIGN_LORDS


def calc_yogas(planets: dict, lagna: dict) -> list[dict]:
    """Detect classical Vedic yogas present in the birth chart.

    Returns a list of present yogas. Each entry has:
      name, type, description, planets (list), house (int|None)

    Types: mahapurusha | raj | dhan | chandra | challenging
    Reference: BPHS Ch.36, Phaladeepika Ch.6-7, B.V. Raman "300 Important Combinations"
    """
    CLASSICAL = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    BENEFICS = {"Jupiter", "Venus", "Mercury"}
    yogas: list[dict] = []
    lagna_sign = lagna["sign"]

    # ── Helpers ──────────────────────────────────────────────────────────────

    def psign(p: str) -> int:
        return planets[p]["sign"] if p in planets else -1

    def phouse(p: str) -> int | None:
        return planets[p]["house"] if p in planets else None

    def sign_lord(sign_idx: int) -> str:
        return SIGN_LORDS[sign_idx % 12]

    def house_lord(n: int) -> str:
        return sign_lord(lagna_sign + n - 1)

    def in_kendra(p: str) -> bool:
        return phouse(p) in (1, 4, 7, 10)

    def in_trikona(p: str) -> bool:
        return phouse(p) in (1, 5, 9)

    def in_kendra_or_trikona(p: str) -> bool:
        return phouse(p) in (1, 4, 5, 7, 9, 10)

    def in_dusthana(p: str) -> bool:
        return phouse(p) in (6, 8, 12)

    def in_own_sign(p: str) -> bool:
        s = psign(p)
        return s in _OWN_SIGNS.get(p, []) or s == _MOOLATRIKONA.get(p, -1)

    def in_exaltation(p: str) -> bool:
        return psign(p) == int(_EXALTATION[p] / 30) if p in _EXALTATION else False

    def in_debilitation(p: str) -> bool:
        if p not in _EXALTATION:
            return False
        return psign(p) == (int(_EXALTATION[p] / 30) + 6) % 12

    def in_dignity(p: str) -> bool:
        return in_own_sign(p) or in_exaltation(p)

    def same_sign(p1: str, p2: str) -> bool:
        return p1 in planets and p2 in planets and psign(p1) == psign(p2)

    def aspects(aspector: str, target: str) -> bool:
        """Graha Drishti — sign-based aspect (house count forward from aspector)."""
        if aspector not in planets or target not in planets:
            return False
        diff = round(((planets[target]["longitude"] - planets[aspector]["longitude"]) % 360) / 30)
        if diff == 7:
            return True
        if aspector == "Mars" and diff in (4, 8):
            return True
        if aspector == "Jupiter" and diff in (5, 9):
            return True
        if aspector == "Saturn" and diff in (3, 10):
            return True
        return False

    # ── 1. Pancha Mahapurusha Yogas ──────────────────────────────────────────
    for yoga_name, planet, desc in [
        ("Ruchaka", "Mars",    "Mars strong in Kendra → courage, leadership, physical strength, warrior spirit."),
        ("Bhadra",  "Mercury", "Mercury strong in Kendra → sharp intellect, eloquence, business acumen, scholarship."),
        ("Hamsa",   "Jupiter", "Jupiter strong in Kendra → wisdom, spirituality, dharmic authority, teaching ability."),
        ("Malavya", "Venus",   "Venus strong in Kendra → luxury, arts, beauty, refined pleasures, marital happiness."),
        ("Sasa",    "Saturn",  "Saturn strong in Kendra → discipline, mass following, endurance, administrative power."),
    ]:
        if planet in planets and in_dignity(planet) and in_kendra(planet):
            yogas.append({
                "name": f"{yoga_name} Yoga",
                "type": "mahapurusha",
                "description": desc,
                "planets": [planet],
                "house": phouse(planet),
            })

    # ── 2. Gaja Kesari Yoga ───────────────────────────────────────────────────
    if "Jupiter" in planets and "Moon" in planets:
        diff = (psign("Jupiter") - psign("Moon")) % 12
        if diff in (0, 3, 6, 9) and not in_debilitation("Jupiter"):
            yogas.append({
                "name": "Gaja Kesari Yoga",
                "type": "raj",
                "description": "Jupiter in Kendra from Moon → wisdom, fame, prosperity, noble character, leadership.",
                "planets": ["Jupiter", "Moon"],
                "house": phouse("Jupiter"),
            })

    # ── 3. Budhaditya Yoga ────────────────────────────────────────────────────
    if same_sign("Sun", "Mercury") and not in_debilitation("Mercury"):
        yogas.append({
            "name": "Budhaditya Yoga",
            "type": "raj",
            "description": "Sun and Mercury conjunct → sharp analytical mind, articulate communication, success in intellectual or government roles.",
            "planets": ["Sun", "Mercury"],
            "house": phouse("Sun"),
        })

    # ── 4. Chandra Mangala Yoga ───────────────────────────────────────────────
    if same_sign("Moon", "Mars"):
        yogas.append({
            "name": "Chandra Mangala Yoga",
            "type": "dhan",
            "description": "Moon and Mars conjunct → financial gains through bold action, entrepreneurial drive, strong willpower.",
            "planets": ["Moon", "Mars"],
            "house": phouse("Moon"),
        })

    # ── 5. Moon Yogas: Sunapha / Anapha / Durudhara / Kemdrum ────────────────
    moon_sign = psign("Moon")
    second_from_moon  = (moon_sign + 1) % 12
    twelfth_from_moon = (moon_sign - 1) % 12
    p2  = [p for p in CLASSICAL if p not in ("Sun", "Moon") and psign(p) == second_from_moon]
    p12 = [p for p in CLASSICAL if p not in ("Sun", "Moon") and psign(p) == twelfth_from_moon]

    if p2 and not p12:
        yogas.append({
            "name": "Sunapha Yoga",
            "type": "chandra",
            "description": "Planet(s) in 2nd from Moon (none in 12th) → self-made wealth, intelligence, confident nature.",
            "planets": ["Moon"] + p2,
            "house": None,
        })
    elif p12 and not p2:
        yogas.append({
            "name": "Anapha Yoga",
            "type": "chandra",
            "description": "Planet(s) in 12th from Moon (none in 2nd) → charisma, comfortable life, spiritual inclination.",
            "planets": ["Moon"] + p12,
            "house": None,
        })
    elif p2 and p12:
        yogas.append({
            "name": "Durudhara Yoga",
            "type": "chandra",
            "description": "Planets in both 2nd and 12th from Moon → abundant wealth, recognition, well-rounded prosperous life.",
            "planets": ["Moon"] + p2 + p12,
            "house": None,
        })
    else:
        yogas.append({
            "name": "Kemdrum Yoga",
            "type": "challenging",
            "description": "No planets in 2nd or 12th from Moon → emotional instability, need for self-reliance. Effect reduced if Moon or benefics are in Kendra.",
            "planets": ["Moon"],
            "house": None,
        })

    # ── 6. Dharma Karmadhipati Yoga ───────────────────────────────────────────
    lord_9  = house_lord(9)
    lord_10 = house_lord(10)
    if lord_9 != lord_10 and lord_9 in planets and lord_10 in planets:
        if same_sign(lord_9, lord_10) or aspects(lord_9, lord_10) or aspects(lord_10, lord_9):
            yogas.append({
                "name": "Dharma Karmadhipati Yoga",
                "type": "raj",
                "description": (
                    f"Lords of 9th ({lord_9}) and 10th ({lord_10}) are conjunct or in mutual aspect "
                    f"→ highly successful career, dharmic profession, authority, government recognition."
                ),
                "planets": [lord_9, lord_10],
                "house": None,
            })

    # ── 7. Viparita Raja Yoga (Harsha / Sarala / Vimala) ─────────────────────
    lord_6  = house_lord(6)
    lord_8  = house_lord(8)
    lord_12 = house_lord(12)
    for label, variant, lord in [
        ("6th",  "Harsha",  lord_6),
        ("8th",  "Sarala",  lord_8),
        ("12th", "Vimala",  lord_12),
    ]:
        if lord in planets and phouse(lord) in (6, 8, 12):
            yogas.append({
                "name": f"Viparita Raja Yoga — {variant}",
                "type": "raj",
                "description": (
                    f"Lord of {label} house ({lord}) placed in a dusthana (6/8/12) "
                    f"→ rise after adversity, hidden strength, victory over enemies."
                ),
                "planets": [lord],
                "house": phouse(lord),
            })

    # ── 8. Neecha Bhanga Raja Yoga ────────────────────────────────────────────
    for p in CLASSICAL:
        if p not in planets or not in_debilitation(p):
            continue
        debit_sign = psign(p)
        debit_lord = sign_lord(debit_sign)
        exalt_lord = sign_lord(int(_EXALTATION[p] / 30))
        reasons: list[str] = []

        if debit_lord in planets and in_kendra(debit_lord):
            reasons.append(f"{debit_lord} (lord of debilitation sign) in Kendra")
        if exalt_lord in planets and in_kendra(exalt_lord):
            reasons.append(f"{exalt_lord} (lord of exaltation sign) in Kendra")
        if same_sign(p, debit_lord):
            reasons.append(f"conjunct its sign lord {debit_lord}")

        if reasons:
            yogas.append({
                "name": f"Neecha Bhanga Raja Yoga ({p})",
                "type": "raj",
                "description": (
                    f"{p} is debilitated but cancellation occurs ({'; '.join(reasons)}) "
                    f"→ weakness converts to strength, rise from adversity."
                ),
                "planets": [p],
                "house": phouse(p),
            })

    # ── 9. Amala Yoga ─────────────────────────────────────────────────────────
    tenth_planets = [p for p in CLASSICAL if phouse(p) == 10]
    if tenth_planets and all(p in BENEFICS for p in tenth_planets):
        yogas.append({
            "name": "Amala Yoga",
            "type": "raj",
            "description": "Only benefics in 10th house → spotless reputation, fame through ethical means, respected career.",
            "planets": tenth_planets,
            "house": 10,
        })

    # ── 10. Lakshmi Yoga ──────────────────────────────────────────────────────
    if lord_9 in planets and in_dignity(lord_9) and "Venus" in planets and in_kendra_or_trikona("Venus"):
        yogas.append({
            "name": "Lakshmi Yoga",
            "type": "dhan",
            "description": (
                f"9th lord ({lord_9}) in own/exaltation sign + Venus in Kendra/Trikona "
                f"→ great wealth, luxury, blessings of Lakshmi, material abundance."
            ),
            "planets": [lord_9, "Venus"],
            "house": None,
        })

    # ── 11. Adhi Yoga ─────────────────────────────────────────────────────────
    adhi_planets = [
        p for p in ("Jupiter", "Venus", "Mercury")
        if p in planets and (psign(p) - moon_sign) % 12 in (5, 6, 7)
    ]
    if len(adhi_planets) >= 2:
        yogas.append({
            "name": "Adhi Yoga",
            "type": "raj",
            "description": (
                f"Benefics ({', '.join(adhi_planets)}) in 6th/7th/8th from Moon "
                f"→ leadership, authority, noble environment, victory over enemies."
            ),
            "planets": adhi_planets,
            "house": None,
        })

    return yogas
