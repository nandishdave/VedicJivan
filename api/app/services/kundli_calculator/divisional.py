"""Divisional charts (Vargas) — Shodashvarga + D40, D45, D60.

Implements all 16 Shodashvarga charts plus three special ones (D40
Khavedamsha, D45 Akshvedamsha, D60 Shastiamsa). Pure: no DB, no
swisseph. Sign + degree → resulting sign in the divisional chart.

`_calc_varga_sign` is also used by the Jaimini Karakamsa calculation
(D9 lookup) elsewhere in the package — re-exported via _core.
"""

from __future__ import annotations


def calc_divisional_charts(planets: dict, lagna: dict) -> dict:
    """Calculate divisional chart positions: all Shodashvarga (16) + D40, D45, D60."""
    charts = {}
    for chart_type in (
        "D2", "D3", "D4", "D6", "D7", "D8", "D9", "D10",
        "D11", "D12", "D16", "D20", "D24", "D27", "D30",
        "D40", "D45", "D60",
    ):
        chart = {}
        for name, info in planets.items():
            chart[name] = _calc_varga_sign(info["sign"], info["degree_in_sign"], chart_type)
        # Also calculate Lagna position in each varga
        chart["Lagna"] = _calc_varga_sign(lagna["sign"], lagna["degree"], chart_type)
        charts[chart_type] = chart
    return charts


def _calc_varga_sign(sign: int, degree: float, chart_type: str) -> int:
    """Calculate the resulting sign (0–11) for a planet in a divisional chart."""
    is_odd = sign % 2 == 0  # 0-indexed: Aries(0)=odd, Taurus(1)=even

    if chart_type == "D2":
        # Hora: 2 parts per sign (15° each)
        # Odd sign: 0-15° → Leo(4), 15-30° → Cancer(3)
        # Even sign: 0-15° → Cancer(3), 15-30° → Leo(4)
        half = 0 if degree < 15 else 1
        if is_odd:
            return 4 if half == 0 else 3
        else:
            return 3 if half == 0 else 4

    elif chart_type == "D3":
        # Drekkana: 3 parts (10° each)
        # 1st (0-10°): same sign, 2nd (10-20°): 5th from sign, 3rd (20-30°): 9th from sign
        part = min(int(degree / 10), 2)
        offsets = [0, 4, 8]
        return (sign + offsets[part]) % 12

    elif chart_type == "D9":
        # Navamsa: 9 parts (3°20' each)
        # Fire signs (0,4,8): start from Aries(0)
        # Earth signs (1,5,9): start from Capricorn(9)
        # Air signs (2,6,10): start from Libra(6)
        # Water signs (3,7,11): start from Cancer(3)
        element = sign % 4
        starts = {0: 0, 1: 9, 2: 6, 3: 3}
        part = min(int(degree / (30 / 9)), 8)
        return (starts[element] + part) % 12

    elif chart_type == "D10":
        # Dasamsa: 10 parts (3° each)
        # Odd sign: start from same sign
        # Even sign: start from 9th sign (sign + 8)
        part = min(int(degree / 3), 9)
        start = sign if is_odd else (sign + 8) % 12
        return (start + part) % 12

    elif chart_type == "D12":
        # Dwadasamsa: 12 parts (2°30' each), start from same sign
        part = min(int(degree / 2.5), 11)
        return (sign + part) % 12

    elif chart_type == "D7":
        # Saptamsa: 7 equal parts of 4°17' each
        # Odd signs: start from same sign; Even signs: start from 7th sign
        part = min(int(degree / (30 / 7)), 6)
        start = sign if is_odd else (sign + 6) % 12
        return (start + part) % 12

    elif chart_type == "D30":
        # Trimshamsa: unequal parts (no portion for 0° boundary planet)
        # Odd signs: Mars(0-5)→Aries, Saturn(5-10)→Aquarius,
        #   Jupiter(10-18)→Sagittarius, Mercury(18-25)→Gemini, Venus(25-30)→Libra
        # Even signs: Venus(0-5)→Taurus, Mercury(5-12)→Virgo,
        #   Jupiter(12-20)→Pisces, Saturn(20-25)→Capricorn, Mars(25-30)→Scorpio
        if is_odd:
            if degree < 5:    return 0   # Aries
            elif degree < 10: return 10  # Aquarius
            elif degree < 18: return 8   # Sagittarius
            elif degree < 25: return 2   # Gemini
            else:             return 6   # Libra
        else:
            if degree < 5:    return 1   # Taurus
            elif degree < 12: return 5   # Virgo
            elif degree < 20: return 11  # Pisces
            elif degree < 25: return 9   # Capricorn
            else:             return 7   # Scorpio

    elif chart_type == "D60":
        # Shastiamsa: 60 parts (0°30' each), start from same sign
        part = min(int(degree / 0.5), 59)
        return (sign + part) % 12

    # ── Additional Shodashvarga charts ──────────────────────────────────────

    elif chart_type == "D4":
        # Chaturthamsha: 4 parts (7°30' each). The parts go to the four KENDRAS
        # from the sign — 1st/4th/7th/10th (Parashara), i.e. sign + 3·part.
        # Verified against Astrosage (13/13 bodies).
        part = min(int(degree / 7.5), 3)
        return (sign + 3 * part) % 12

    elif chart_type == "D6":
        # Shashtiamsha (health variant, 6 parts): 5° each
        # Start from same sign for all
        part = min(int(degree / 5), 5)
        return (sign + part) % 12

    elif chart_type == "D8":
        # Ashtamsha: 8 parts (3°45' each)
        # Movable signs start from Aries(0); Fixed from Sagittarius(8); Dual from Leo(4)
        sign_type = sign % 3  # 0=movable(Ari,Can,Lib,Cap), 1=fixed(Tau,Leo,Sco,Aqu), 2=dual(Gem,Vir,Sag,Pis)
        starts_d8 = {0: 0, 1: 8, 2: 4}
        part = min(int(degree / 3.75), 7)
        return (starts_d8.get(sign_type, 0) + part) % 12

    elif chart_type == "D11":
        # Ekadamsha (Rudramsa): 11 parts (~2°43.6' each)
        # Start from same sign for all
        part = min(int(degree / (30 / 11)), 10)
        return (sign + part) % 12

    elif chart_type == "D16":
        # Shodashamsha: 16 parts (1°52.5' each)
        # Movable signs start from Aries(0); Fixed from Leo(4); Dual from Sagittarius(8)
        sign_type = sign % 3
        starts_d16 = {0: 0, 1: 4, 2: 8}
        part = min(int(degree / (30 / 16)), 15)
        return (starts_d16.get(sign_type, 0) + part) % 12

    elif chart_type == "D20":
        # Vimsamsha: 20 parts (1°30' each)
        # Movable signs start from Aries(0); Fixed from Sagittarius(8); Dual from Leo(4)
        sign_type = sign % 3
        starts_d20 = {0: 0, 1: 8, 2: 4}
        part = min(int(degree / 1.5), 19)
        return (starts_d20.get(sign_type, 0) + part) % 12

    elif chart_type == "D24":
        # Chaturvimsamsha: 24 parts (1°15' each)
        # Odd signs start from Leo(4); Even signs start from Cancer(3)
        part = min(int(degree / 1.25), 23)
        start = 4 if is_odd else 3
        return (start + part) % 12

    elif chart_type == "D27":
        # Saptavimsamsha (Bhamsa): 27 parts (~1°6.67' each)
        # Fire signs start from Aries(0); Earth from Cancer(3); Air from Libra(6); Water from Capricorn(9)
        element = sign % 4
        starts_d27 = {0: 0, 1: 3, 2: 6, 3: 9}
        part = min(int(degree / (30 / 27)), 26)
        return (starts_d27.get(element, 0) + part) % 12

    elif chart_type == "D40":
        # Khavedamsha: 40 parts (0°45' each)
        # Odd signs start from Aries(0); Even signs start from Libra(6)
        part = min(int(degree / 0.75), 39)
        start = 0 if is_odd else 6
        return (start + part) % 12

    elif chart_type == "D45":
        # Akshvedamsha: 45 parts (0°40' each)
        # Movable signs start from Aries(0); Fixed from Leo(4); Dual from Sagittarius(8)
        sign_type = sign % 3
        starts_d45 = {0: 0, 1: 4, 2: 8}
        part = min(int(degree / (30 / 45)), 44)
        return (starts_d45.get(sign_type, 0) + part) % 12

    return sign


# ── Display transform for the calculator ────────────────────────────────────
# Local sign names so this stays a leaf module (_core imports this module).
_DIV_SIGN_ABBR = ["Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]
_VARGA_ORDER = [
    "D1", "D2", "D3", "D4", "D6", "D7", "D8", "D9", "D10",
    "D11", "D12", "D16", "D20", "D24", "D27", "D30", "D40", "D45", "D60",
]
_VARGA_NAME = {
    "D1": "Rāśi (body/life)", "D2": "Horā (wealth)", "D3": "Drekkāṇa (siblings)",
    "D4": "Chaturthāṁśa (fortune)", "D6": "Ṣaṣṭhāṁśa (health)", "D7": "Saptāṁśa (children)",
    "D8": "Aṣṭāṁśa (longevity)", "D9": "Navāṁśa (spouse/dharma)", "D10": "Daśāṁśa (career)",
    "D11": "Rudrāṁśa (gains)", "D12": "Dvādaśāṁśa (parents)", "D16": "Ṣoḍaśāṁśa (vehicles)",
    "D20": "Viṁśāṁśa (spiritual)", "D24": "Chaturviṁśāṁśa (learning)", "D27": "Bhāṁśa (strengths)",
    "D30": "Triṁśāṁśa (misfortune)", "D40": "Khavedāṁśa (maternal)", "D45": "Akṣavedāṁśa (paternal)",
    "D60": "Ṣaṣṭyāṁśa (past karma)",
}
_DIV_BODY_ORDER = [
    "Ascendant", "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn",
    "Rahu", "Ketu", "Uranus", "Neptune", "Pluto",
]


def divisional_table(planets: dict, lagna: dict, divisional: dict | None = None) -> dict:
    """Each body's sign across the 16 Ṣoḍaśavarga divisionals (+ D6/D8/D11) for the
    calculator: D1 is the natal sign; the rest come from ``calc_divisional_charts``.
    Returns ``{vargas: [{key, name}], bodies: [{body, signs: [sign-abbr per varga]}]}``.
    """
    div = divisional or calc_divisional_charts(planets, lagna)

    def sign_of(body: str, varga: str) -> int | None:
        if varga == "D1":
            return lagna["sign"] if body == "Ascendant" else planets[body]["sign"]
        key = "Lagna" if body == "Ascendant" else body
        return div.get(varga, {}).get(key)

    bodies = []
    for body in _DIV_BODY_ORDER:
        if body != "Ascendant" and body not in planets:
            continue
        signs = []
        for v in _VARGA_ORDER:
            s = sign_of(body, v)
            signs.append(_DIV_SIGN_ABBR[s] if s is not None else "")
        bodies.append({"body": body, "signs": signs})
    return {
        "vargas": [{"key": v, "name": _VARGA_NAME[v]} for v in _VARGA_ORDER],
        "bodies": bodies,
    }
