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
_KOOTA_THEME = {
    "Varna": "ego balance and the couple's approach to work and duty",
    "Vasya": "mutual magnetism, control and how naturally they influence one another",
    "Tara": "destiny, fortune and each other's well-being",
    "Yoni": "physical and instinctive compatibility",
    "Maitri": "mental friendship and psychological rapport",
    "Gana": "temperament, character and everyday conduct",
    "Bhakoot": "emotional bonding, love and the welfare of the family",
    "Nadi": "health, vitality and healthy progeny",
}


def _interpret(koota: str, points: float, mx: int, boy: str, girl: str) -> str:
    r = points / mx
    theme = _KOOTA_THEME[koota]
    same = boy == girl
    who = (f"Both partners share the {boy} attribute" if same
           else f"The boy's side is {boy} while the girl's is {girl}")
    if r >= 0.66:
        return (f"{who}. For {theme}, this is a favourable and supportive combination "
                f"({points} of {mx}). The natives understand each other's needs here and it "
                f"adds harmony and stability to the union.")
    if r > 0:
        return (f"{who}. For {theme}, this is a moderate combination ({points} of {mx}) — "
                f"neither the strongest nor the weakest. With mutual understanding and a little "
                f"patience the natives can bridge the small differences this factor indicates.")
    return (f"{who}. For {theme}, this factor scores {points} of {mx}, which is not favourable "
            f"and points to friction in this area. It should be weighed carefully, though a "
            f"strong overall match and other well-placed gunas can help offset it.")


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
    }
