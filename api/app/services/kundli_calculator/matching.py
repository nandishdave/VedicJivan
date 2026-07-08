"""Horoscope matching — Ashtakoota (Guna Milap) + Mangal Dosha.

The eight kootas (max 36), each from the two Moon nakṣatras / rāśis:
  Varna 1, Vasya 2, Tara 3, Yoni 4, Graha-Maitri 5, Gana 6, Bhakoot 7, Nadi 8.

Verified against four AstroSage reports (Praveen&Sonali 25.5, Kushal&Sneha 13,
Dhruv&Jigisha 25, Rupal&Rupal 21.5). The scoring *algorithms* (Tara, Nadi,
Bhakoot, Varna, Maitri, Gana) are example-validated; the Yoni 14×14 matrix and
the Vasya group matrix are the standard classical (BV Raman) tables — the four
reports spot-check a handful of their cells.
"""

from __future__ import annotations

_NAK_ARC = 360.0 / 27.0

# ── Nakṣatra classifications (0-indexed, Ashwini=0). All example-confirmed. ──
# Yoni animal index into _YONI_NAMES.
_NAK_YONI = [
    0, 1, 2, 3, 3, 4, 5, 2, 5, 6, 6, 7, 8, 9, 8, 9, 10, 10, 4, 11, 12, 11, 13, 0, 13, 7, 1,
]
_YONI_NAMES = [
    "Ashva", "Gaja", "Mesha", "Sarpa", "Shwan", "Bilav", "Mushak",
    "Gau", "Mahish", "Vyaghra", "Mriga", "Vanar", "Nakul", "Simha",
]
# Gana: 0 Deva, 1 Manushya, 2 Rakshasa.
_NAK_GANA = [
    0, 1, 2, 1, 0, 1, 0, 0, 2, 2, 1, 1, 0, 2, 0, 2, 0, 2, 2, 1, 1, 0, 2, 2, 1, 1, 0,
]
_GANA_NAMES = ["Deva", "Manushya", "Rakshasa"]
# Nadi: 0 Aadi, 1 Madhya, 2 Antya.
_NAK_NADI = [
    0, 1, 2, 2, 1, 0, 0, 1, 2, 2, 1, 0, 0, 1, 2, 2, 1, 0, 0, 1, 2, 2, 1, 0, 0, 1, 2,
]
_NADI_NAMES = ["Aadi", "Madhya", "Antya"]

# ── Sign-based (0-indexed, Aries=0) ─────────────────────────────────────────
# Varna rank: Brahmin 4 > Kshatriya 3 > Vaishya 2 > Shudra 1.
_SIGN_VARNA = [3, 2, 1, 4, 3, 2, 1, 4, 3, 2, 1, 4]
_VARNA_NAMES = {4: "Brahmin", 3: "Kshatriya", 2: "Vaishya", 1: "Shudra"}
# Vasya group: 0 Chatushpad, 1 Manav, 2 Jalachar, 3 Vanachar, 4 Keeta.
# Sagittarius & Capricorn are half-and-half (handled by degree in _vasya_group).
_SIGN_VASYA = [0, 0, 1, 2, 3, 1, 1, 4, None, None, 1, 2]
_VASYA_NAMES = ["Chatushpad", "Manav", "Jalachar", "Vanachar", "Keeta"]
_SIGN_LORD = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
              "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]
_SIGN_NAMES = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
               "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
_NAK_NAMES = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra", "Punarvasu",
    "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta",
    "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha",
    "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
    "Uttara Bhadrapada", "Revati",
]
# Vimśottari nakṣatra lord (repeats every 9, from Ashwini).
_NAK_LORD = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
# Bodies shown in the North-Indian charts (+ their glyphs).
_CHART_BODIES = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn",
                 "Rahu", "Ketu", "Uranus", "Neptune", "Pluto"]
_BODY_ABBR = {"Sun": "Su", "Moon": "Mo", "Mars": "Ma", "Mercury": "Me", "Jupiter": "Ju",
              "Venus": "Ve", "Saturn": "Sa", "Rahu": "Ra", "Ketu": "Ke",
              "Uranus": "Ur", "Neptune": "Ne", "Pluto": "Pl"}

# ── Scoring matrices ────────────────────────────────────────────────────────
# Yoni 14×14 (standard classical). Diagonal 4; the 7 enemy pairs 0. Anchors
# confirmed vs AstroSage: Mriga×Ashva 3, Marjar×Ashva 3, Vanar×Nakul 2, Mriga×Vyaghra 1.
_YONI_MATRIX = [
    [4, 2, 2, 3, 2, 3, 2, 1, 0, 1, 3, 2, 2, 1],  # Ashva
    [2, 4, 3, 3, 2, 2, 2, 2, 2, 1, 3, 3, 2, 0],  # Gaja
    [2, 3, 4, 2, 1, 2, 1, 3, 3, 1, 2, 0, 3, 2],  # Mesha
    [3, 3, 2, 4, 2, 1, 1, 1, 1, 2, 2, 2, 0, 2],  # Sarpa
    [2, 2, 1, 2, 4, 2, 1, 2, 2, 1, 0, 3, 2, 1],  # Shwan
    [3, 2, 2, 1, 2, 4, 0, 2, 2, 1, 3, 2, 2, 2],  # Marjar
    [2, 2, 1, 1, 1, 0, 4, 2, 2, 2, 2, 3, 2, 2],  # Mushak
    [1, 2, 3, 1, 2, 2, 2, 4, 3, 0, 3, 2, 2, 1],  # Gau
    [0, 2, 3, 1, 2, 2, 2, 3, 4, 1, 2, 2, 2, 2],  # Mahish
    [1, 1, 1, 2, 1, 1, 2, 0, 1, 4, 1, 2, 2, 1],  # Vyaghra
    [3, 3, 2, 2, 0, 3, 2, 3, 2, 1, 4, 2, 2, 2],  # Mriga
    [2, 3, 0, 2, 3, 2, 3, 2, 2, 2, 2, 4, 2, 2],  # Vanar
    [2, 2, 3, 0, 2, 2, 2, 2, 2, 2, 2, 2, 4, 2],  # Nakul
    [1, 0, 2, 2, 1, 2, 2, 1, 2, 1, 2, 2, 2, 4],  # Simha
]
# Gana matrix [boy][girl]; Deva-boy×Rakshasa-girl 0 confirmed.
_GANA_MATRIX = [[6, 6, 0], [6, 6, 0], [1, 0, 6]]
# Vasya group matrix [boy][girl] — same group 2, else 1 (crude standard;
# least-validated koota, only same/Keeta cells example-confirmed).
_VASYA_MATRIX = [[2 if i == j else 1 for j in range(5)] for i in range(5)]

# Natural (Naisargika) friendships for Graha-Maitri.
_FRIENDS = {
    "Sun": {"Moon", "Mars", "Jupiter"}, "Moon": {"Sun", "Mercury"},
    "Mars": {"Sun", "Moon", "Jupiter"}, "Mercury": {"Sun", "Venus"},
    "Jupiter": {"Sun", "Moon", "Mars"}, "Venus": {"Mercury", "Saturn"},
    "Saturn": {"Mercury", "Venus"},
}
_ENEMIES = {
    "Sun": {"Venus", "Saturn"}, "Moon": set(), "Mars": {"Mercury"},
    "Mercury": {"Moon"}, "Jupiter": {"Mercury", "Venus"},
    "Venus": {"Sun", "Moon"}, "Saturn": {"Sun", "Moon", "Mars"},
}
_TARA_NAMES = ["Ati-mitra", "Janma", "Sampat", "Vipat", "Kshema",
               "Pratyak", "Sadhaka", "Vadha", "Mitra"]  # index = t (0..8)

# Graha-Maitri points by (boy-lord→girl-lord, girl-lord→boy-lord) natural
# relationship (+1 friend / 0 neutral / −1 enemy). Validated on 5 AstroSage
# reports (same lord → 5, handled separately).
_MAITRI_TABLE = {
    (1, 1): 5, (1, 0): 4, (1, -1): 1,
    (0, 1): 4, (0, 0): 3, (0, -1): 0.5,
    (-1, 1): 1, (-1, 0): 0.5, (-1, -1): 0,
}


def _rel(a: str, b: str) -> int:
    """+1 if a sees b as friend, -1 enemy, 0 neutral."""
    if b in _FRIENDS[a]:
        return 1
    if b in _ENEMIES[a]:
        return -1
    return 0


def _vasya_group(sign: int, moon_lon: float) -> int:
    if sign == 8:  # Sagittarius: 1st half Manav, 2nd half Chatushpad
        return 1 if (moon_lon % 30) < 15 else 0
    if sign == 9:  # Capricorn: 1st half Chatushpad, 2nd half Jalachar
        return 0 if (moon_lon % 30) < 15 else 2
    return _SIGN_VASYA[sign]


def _tara(b_nak: int, g_nak: int):
    def t(src, dst):
        return (((dst - src) % 27) + 1) % 9
    tb = t(g_nak, b_nak)   # boy's tara (counted from girl)
    tg = t(b_nak, g_nak)   # girl's tara (counted from boy)
    pts = (1.5 if tb % 2 == 0 else 0) + (1.5 if tg % 2 == 0 else 0)
    return pts, _TARA_NAMES[tb], _TARA_NAMES[tg]


def _bhakoot(b_sign: int, g_sign: int) -> int:
    a = ((g_sign - b_sign) % 12) + 1
    b = ((b_sign - g_sign) % 12) + 1
    pair = {a, b}
    if pair in ({2, 12}, {5, 9}, {6, 8}):
        return 0
    return 7


def _maitri(b_sign: int, g_sign: int):
    lb, lg = _SIGN_LORD[b_sign], _SIGN_LORD[g_sign]
    if lb == lg:
        return 5, lb, lg
    pts = _MAITRI_TABLE[(_rel(lb, lg), _rel(lg, lb))]
    return pts, lb, lg


# ── Mangal Dosha ────────────────────────────────────────────────────────────
_MANGAL_HOUSES = {1, 2, 4, 7, 8, 12}


def _house_from(ref_sign: int, planet_sign: int) -> int:
    return ((planet_sign - ref_sign) % 12) + 1


def mangal_dosha(chart: dict) -> dict:
    """Mangal (Kuja) Dosha from Mars in houses 1/2/4/7/8/12 relative to the
    Lagna, the Moon and Venus. Returns a No/Low/High grade + the hits."""
    lagna = chart["lagna"]["sign"]
    mars = chart["planets"]["Mars"]["sign"]
    moon = chart["planets"]["Moon"]["sign"]
    venus = chart["planets"]["Venus"]["sign"]
    hits = {}
    for name, ref in (("Lagna", lagna), ("Moon", moon), ("Venus", venus)):
        h = _house_from(ref, mars)
        if h in _MANGAL_HOUSES:
            hits[name] = h
    # Calibrated on 8 AstroSage charts: a Venus-only hit doesn't make one Manglik
    # ("No"); a Lagna or Moon hit → "Low"; hits from all three refs → "High".
    if "Lagna" not in hits and "Moon" not in hits:
        grade = "No"
    elif {"Lagna", "Moon", "Venus"} <= set(hits):
        grade = "High"
    else:
        grade = "Low"
    return {"grade": grade, "hits": hits}


# ── Interpretation text (original, Astrosage-style; tiered by score) ────────
# Each koota: what it governs + a favourable / moderate / weak outlook paragraph.
_KOOTA_INFO = {
    "Varna": {
        "governs": "the spiritual and mental grade of the two people and the balance of ego, "
                   "duty and their approach to work and domestic life",
        "good": "their temperaments blend easily here; each respects the other's way of thinking "
                "and handling everyday responsibilities, which brings quiet cooperation and mutual "
                "regard into the home.",
        "mod": "there is workable understanding, though the two occasionally approach duty and "
               "domestic matters from different angles; a little give-and-take keeps this in balance.",
        "weak": "their outlooks on duty and household matters can differ, and one may not readily "
                "value the other's approach — a source of small friction that patience and respect "
                "can smooth over.",
    },
    "Vasya": {
        "governs": "mutual magnetism and control — how naturally each partner is drawn to and able "
                   "to influence the other",
        "good": "a strong, natural pull draws them together; they influence and win over one another "
                "with ease, and their bond feels magnetic and mutually devoted.",
        "mod": "the attraction is present but not effortless; each retains a degree of independence, "
               "and steady affection is what keeps the pull alive.",
        "weak": "the natural give of influence is uneven here, so one may feel the other is hard to "
                "sway or too assertive; conscious effort is needed to keep the dynamic comfortable.",
    },
    "Tara": {
        "governs": "destiny, fortune, health and the auspiciousness each partner brings to the other",
        "good": "the birth-star energies support one another, favouring health, fortune and a sense "
                "of shared good luck through the ups and downs of life.",
        "mod": "the star energies are partly supportive; fortune flows well in some seasons and asks "
               "for patience in others, but the overall current is workable.",
        "weak": "the flow of destiny between the stars is not smooth, and the two may struggle to "
                "fully understand each other's needs — best offset by strength in the other gunas.",
    },
    "Yoni": {
        "governs": "physical and instinctive compatibility — the animal nature, intimacy and bodily "
                   "rapport of the couple",
        "good": "they are instinctively in tune, sharing warmth, attraction and a satisfying physical "
                "understanding that deepens the marital bond.",
        "mod": "physical rapport is reasonable; with openness and affection the two find a comfortable "
               "intimate rhythm together.",
        "weak": "their instinctive natures differ, which can make physical understanding and everyday "
                "closeness harder to reach; honest communication helps most here.",
    },
    "Maitri": {
        "governs": "mental friendship and psychological rapport, read from the friendship of the two "
                   "Moon-sign lords",
        "good": "their minds meet as natural friends — supportive, caring and easy in each other's "
                "company, which makes the relationship warm and genuinely companionable.",
        "mod": "there is fair mental rapport; the two think somewhat differently but can meet in the "
               "middle and enjoy each other's company with a little effort.",
        "weak": "the ruling planets are not friendly, so the two may need real lifestyle and attitude "
                "adjustments to find a common wavelength and avoid talking past one another.",
    },
    "Gana": {
        "governs": "temperament and character — the divine, human or demonic disposition that shapes "
                   "everyday conduct",
        "good": "they share a compatible temperament, tending to be peace-loving, understanding and "
                "forbearing with one another, which keeps daily life harmonious.",
        "mod": "their temperaments are broadly workable, with only occasional differences in conduct "
               "that mutual tolerance easily absorbs.",
        "weak": "the temperaments pull in different directions — one gentler, one more forceful — so "
                "clashes over conduct and small matters are possible unless both stay patient.",
    },
    "Bhakoot": {
        "governs": "emotional bonding, love, prosperity and the welfare of the family, from the "
                   "relative placement of the two Moon signs",
        "good": "the Moon signs sit in a supportive relationship, favouring emotional closeness, love "
                "and the growth and prosperity of the family.",
        "mod": "emotional bonding is serviceable, though the couple should nurture communication so "
               "small distances don't widen over time.",
        "weak": "the Moon signs fall in an inauspicious axis (2-12, 5-9 or 6-8), which can strain "
                "emotional harmony, finances or family welfare — an area to handle with care, though "
                "a strong overall match and a good Nadi/Gana can offset it.",
    },
    "Nadi": {
        "governs": "health, vitality, genetic constitution and healthy progeny — considered the most "
                   "important koota",
        "good": "the two belong to different nadis, which is excellent for health, vitality and "
                "healthy children, and strengthens the overall compatibility of the match.",
        "mod": "the nadi factor is workable here.",
        "weak": "both partners share the same nadi (Nadi Dosha), which classical texts caution against "
                "for health and progeny; some schools relax this when the pada or nakshatra differ, "
                "but it should be reviewed carefully with an astrologer.",
    },
}


def _interpret(koota: str, points: float, mx: int, boy: str, girl: str) -> str:
    r = points / mx
    info = _KOOTA_INFO[koota]
    tier = "good" if r >= 0.66 else ("mod" if r > 0 else "weak")
    who = (f"Both partners share the {boy} attribute" if boy == girl
           else f"The groom's side is {boy} while the bride's is {girl}")
    return (f"{who}. This koota reflects {info['governs']} ({points} of {mx}). "
            f"Here {info[tier]}")


def _person_summary(chart: dict) -> dict:
    """Birth-summary for one chart: Lagna/Rāśi/Nakṣatra + their lords and the
    koota classifications (Gana, Nadi, Yoni, Varna, Vasya)."""
    lagna = chart["lagna"]["sign"]
    mlon = chart["planets"]["Moon"]["longitude"]
    moon = int(mlon // 30)
    nak = int(mlon // _NAK_ARC)
    pada = int((mlon % _NAK_ARC) // (_NAK_ARC / 4)) + 1
    return {
        "lagna": _SIGN_NAMES[lagna], "lagna_lord": _SIGN_LORD[lagna],
        "rashi": _SIGN_NAMES[moon], "rashi_lord": _SIGN_LORD[moon],
        "nakshatra": _NAK_NAMES[nak], "pada": pada, "nakshatra_lord": _NAK_LORD[nak % 9],
        "gana": _GANA_NAMES[_NAK_GANA[nak]], "nadi": _NADI_NAMES[_NAK_NADI[nak]],
        "yoni": _YONI_NAMES[_NAK_YONI[nak]], "varna": _VARNA_NAMES[_SIGN_VARNA[moon]],
        "vasya": _VASYA_NAMES[_vasya_group(moon, mlon)],
    }


def _by_sign(signs: dict) -> dict:
    out: dict[str, list[str]] = {}
    for body, s in signs.items():
        out.setdefault(str(s), []).append(_BODY_ABBR[body])
    return out


def _person_charts(chart: dict) -> dict:
    """Lagna (D1), Navāṁśa (D9) and Chandra (Moon) charts for one person, each as
    ``{asc_sign, by_sign}`` for the North-Indian renderer."""
    from app.services.kundli_calculator.divisional import _calc_varga_sign

    P, lagna = chart["planets"], chart["lagna"]
    bodies = [b for b in _CHART_BODIES if b in P]
    natal = {b: P[b]["sign"] for b in bodies}
    d9 = {b: _calc_varga_sign(P[b]["sign"], P[b]["degree_in_sign"], "D9") for b in bodies}
    lagna_d9 = _calc_varga_sign(lagna["sign"], lagna["degree"], "D9")
    return {
        "D1": {"asc_sign": lagna["sign"], "by_sign": _by_sign(natal)},
        "D9": {"asc_sign": lagna_d9, "by_sign": _by_sign(d9)},
        "Moon": {"asc_sign": P["Moon"]["sign"], "by_sign": _by_sign(natal)},
    }


def compute_matching(boy: dict, girl: dict) -> dict:
    """Full Ashtakoota + Mangal-Dosha result from two charts (each a
    build_muhurta_chart output). Returns the per-koota table, total, Mangal
    grades and the overall verdict."""
    bm = boy["planets"]["Moon"]["longitude"]
    gm = girl["planets"]["Moon"]["longitude"]
    b_nak, g_nak = int(bm // _NAK_ARC), int(gm // _NAK_ARC)
    b_sign, g_sign = int(bm // 30), int(gm // 30)

    varna = 1 if _SIGN_VARNA[b_sign] >= _SIGN_VARNA[g_sign] else 0
    bvg, gvg = _vasya_group(b_sign, bm), _vasya_group(g_sign, gm)
    vasya = _VASYA_MATRIX[bvg][gvg]
    tara, b_tara, g_tara = _tara(b_nak, g_nak)
    by, gy = _NAK_YONI[b_nak], _NAK_YONI[g_nak]
    yoni = _YONI_MATRIX[by][gy]
    maitri, b_lord, g_lord = _maitri(b_sign, g_sign)
    gana = _GANA_MATRIX[_NAK_GANA[b_nak]][_NAK_GANA[g_nak]]
    bhakoot = _bhakoot(b_sign, g_sign)
    nadi = 0 if _NAK_NADI[b_nak] == _NAK_NADI[g_nak] else 8

    kootas = [
        {"koota": "Varna", "max": 1, "boy": _VARNA_NAMES[_SIGN_VARNA[b_sign]],
         "girl": _VARNA_NAMES[_SIGN_VARNA[g_sign]], "points": varna, "area": "Work"},
        {"koota": "Vasya", "max": 2, "boy": _VASYA_NAMES[bvg],
         "girl": _VASYA_NAMES[gvg], "points": vasya, "area": "Dominance"},
        {"koota": "Tara", "max": 3, "boy": b_tara, "girl": g_tara,
         "points": tara, "area": "Destiny"},
        {"koota": "Yoni", "max": 4, "boy": _YONI_NAMES[by],
         "girl": _YONI_NAMES[gy], "points": yoni, "area": "Mentality"},
        {"koota": "Maitri", "max": 5, "boy": b_lord, "girl": g_lord,
         "points": maitri, "area": "Compatibility"},
        {"koota": "Gana", "max": 6, "boy": _GANA_NAMES[_NAK_GANA[b_nak]],
         "girl": _GANA_NAMES[_NAK_GANA[g_nak]], "points": gana, "area": "Guna Level"},
        {"koota": "Bhakoot", "max": 7, "boy": _SIGN_NAMES[b_sign],
         "girl": _SIGN_NAMES[g_sign], "points": bhakoot, "area": "Love"},
        {"koota": "Nadi", "max": 8, "boy": _NADI_NAMES[_NAK_NADI[b_nak]],
         "girl": _NADI_NAMES[_NAK_NADI[g_nak]], "points": nadi, "area": "Health"},
    ]
    for k in kootas:
        k["interpretation"] = _interpret(k["koota"], k["points"], k["max"], k["boy"], k["girl"])
    total = sum(k["points"] for k in kootas)
    boy_mangal = mangal_dosha(boy)
    girl_mangal = mangal_dosha(girl)

    if total < 18:
        verdict = "This marriage is NOT preferable due to low match points obtained."
    elif boy_mangal["grade"] != girl_mangal["grade"]:
        verdict = ("Ashtakoot Match is successful, however there is a difference in the "
                   "level of Mangal Dosha compatibility. It is advisable to consult a "
                   "learned astrologer before proceeding to marriage.")
    else:
        verdict = "This marriage is preferable."

    return {
        "kootas": kootas,
        "total": round(total, 1),
        "max_total": 36,
        "boy_mangal": boy_mangal["grade"],
        "girl_mangal": girl_mangal["grade"],
        "verdict": verdict,
        "boy_summary": _person_summary(boy),
        "girl_summary": _person_summary(girl),
        "boy_charts": _person_charts(boy),
        "girl_charts": _person_charts(girl),
    }
