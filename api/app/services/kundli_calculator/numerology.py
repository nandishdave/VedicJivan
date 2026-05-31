"""Chaldean numerology — name + DOB derived numbers.

Pure module: no swisseph, no DB. Used by `build_chart` and consumed by
the PDF builder. Extracted from the legacy `_core` monolith.
"""

from __future__ import annotations

from datetime import date as _date


_CHALDEAN: dict[str, int] = {
    'A': 1, 'I': 1, 'J': 1, 'Q': 1, 'Y': 1,
    'B': 2, 'K': 2, 'R': 2,
    'C': 3, 'G': 3, 'L': 3, 'S': 3,
    'D': 4, 'M': 4, 'T': 4,
    'E': 5, 'H': 5, 'N': 5, 'X': 5,
    'O': 6, 'U': 6, 'V': 6, 'W': 6,
    'P': 7, 'Z': 7,
    'F': 8,
}

_VOWELS = frozenset("AEIOU")

_NUMBER_INFO: dict[int, dict] = {
    1:  {"planet": "Sun",     "lucky_day": "Sunday",    "lucky_color": "Gold / Orange",    "lucky_gemstone": "Ruby"},
    2:  {"planet": "Moon",    "lucky_day": "Monday",    "lucky_color": "White / Silver",   "lucky_gemstone": "Pearl"},
    3:  {"planet": "Jupiter", "lucky_day": "Thursday",  "lucky_color": "Yellow",           "lucky_gemstone": "Yellow Sapphire"},
    4:  {"planet": "Rahu",    "lucky_day": "Saturday",  "lucky_color": "Dark Blue",        "lucky_gemstone": "Hessonite (Gomed)"},
    5:  {"planet": "Mercury", "lucky_day": "Wednesday", "lucky_color": "Green",            "lucky_gemstone": "Emerald"},
    6:  {"planet": "Venus",   "lucky_day": "Friday",    "lucky_color": "White / Pink",     "lucky_gemstone": "Diamond"},
    7:  {"planet": "Ketu",    "lucky_day": "Tuesday",   "lucky_color": "Brown / Tan",      "lucky_gemstone": "Cat's Eye (Lehsunia)"},
    8:  {"planet": "Saturn",  "lucky_day": "Saturday",  "lucky_color": "Black / Dark Blue","lucky_gemstone": "Blue Sapphire"},
    9:  {"planet": "Mars",    "lucky_day": "Tuesday",   "lucky_color": "Red",              "lucky_gemstone": "Red Coral"},
    11: {"planet": "Sun / Moon (Master)",    "lucky_day": "Sunday",   "lucky_color": "Silver / Gold",  "lucky_gemstone": "Pearl / Ruby"},
    22: {"planet": "Moon / Saturn (Master)", "lucky_day": "Saturday", "lucky_color": "Dark Blue",      "lucky_gemstone": "Blue Sapphire"},
    33: {"planet": "Jupiter / Saturn (Master)", "lucky_day": "Thursday", "lucky_color": "Yellow / Black", "lucky_gemstone": "Yellow Sapphire"},
}

_NUMBER_MEANING: dict[int, str] = {
    1:  "Leadership, individuality, pioneering spirit, and ambition. You are a natural initiator who thrives when forging your own path.",
    2:  "Intuition, sensitivity, and cooperation. You excel in partnerships and have a deep emotional intelligence that draws others to you.",
    3:  "Creativity, self-expression, and optimism. You have a gift for communication and inspiring others with your natural enthusiasm and wisdom.",
    4:  "Discipline, hard work, and building solid foundations. Life asks you to work systematically — patience and persistence are your greatest tools.",
    5:  "Freedom, adaptability, and communication. You thrive on variety, travel, and intellectual stimulation — routine stifles your spirit.",
    6:  "Harmony, responsibility, and nurturing. Home, family, and relationships are your deepest sources of meaning and fulfilment.",
    7:  "Spirituality, introspection, and analytical depth. You are drawn to the mysteries of life and find truth through solitude and contemplation.",
    8:  "Power, material success, and karmic perseverance. You are built for achievement — the universe tests you before rewarding you greatly.",
    9:  "Compassion, completion, and universal service. Your path involves giving back, releasing the past, and serving something larger than yourself.",
    11: "Master Number — Illumination and inspiration. You carry heightened intuition and a calling toward spiritual leadership and visionary work.",
    22: "Master Number — The Master Builder. You have the rare ability to turn grand dreams into tangible reality through disciplined effort.",
    33: "Master Number — The Master Teacher. You are called to selfless service, spiritual guidance, and uplifting humanity through compassion and wisdom.",
}

_PERSONAL_YEAR_MEANING: dict[int, str] = {
    1: "A year of fresh starts and new beginnings. Plant seeds now — initiatives launched this year carry long-term momentum.",
    2: "A year of patience, cooperation, and relationships. Focus on partnerships rather than solo ambition.",
    3: "A year of creative expression, socialising, and joy. Opportunities come through self-expression and networking.",
    4: "A year of hard work and building foundations. Discipline and persistence are rewarded — focus on structure.",
    5: "A year of change, freedom, and unexpected opportunities. Stay adaptable — rigid plans will be disrupted.",
    6: "A year of home, family, and responsibility. Nurturing relationships and fulfilling obligations brings deep satisfaction.",
    7: "A year of reflection, spirituality, and inner growth. Step back from the external world — answers come from within.",
    8: "A year of achievement, ambition, and abundance. Material efforts are rewarded — step into your power.",
    9: "A year of completion, release, and humanitarianism. Let go of what no longer serves you — endings open new cycles.",
}


def _reduce_chaldean(n: int) -> int:
    """Reduce to single digit, preserving master numbers 11, 22, 33."""
    while n > 9:
        if n in (11, 22, 33):
            break
        n = sum(int(d) for d in str(n))
    return n


def _sum_digits(n: int) -> int:
    return sum(int(d) for d in str(n))


def _numerology_entry(value: int, label: str, extra: dict | None = None) -> dict:
    info = _NUMBER_INFO.get(value, _NUMBER_INFO.get(((value - 1) % 9) + 1, _NUMBER_INFO[1]))
    entry = {
        "value": value,
        "planet": info["planet"],
        "label": label,
        "meaning": _NUMBER_MEANING.get(value, ""),
        "lucky_day": info["lucky_day"],
        "lucky_color": info["lucky_color"],
        "lucky_gemstone": info["lucky_gemstone"],
    }
    if extra:
        entry.update(extra)
    return entry


def calc_numerology(name: str, dob_str: str, current_year: int) -> dict:
    """Calculate Chaldean numerology numbers from name and date of birth.

    Args:
        name: Full name (spaces/punctuation ignored; only alpha characters used).
        dob_str: Date of birth as 'YYYY-MM-DD'.
        current_year: Year to use for Personal Year calculation.
    """
    dob = _date.fromisoformat(dob_str)

    moolank_raw = _sum_digits(dob.day)
    moolank = _reduce_chaldean(moolank_raw)

    bhagyank_raw = _sum_digits(dob.day) + _sum_digits(dob.month) + _sum_digits(dob.year)
    bhagyank = _reduce_chaldean(bhagyank_raw)

    py_raw = _sum_digits(dob.day) + _sum_digits(dob.month) + _sum_digits(current_year)
    personal_year_val = _reduce_chaldean(py_raw)

    result: dict = {
        "moolank":     _numerology_entry(moolank, "Birth Number (Moolank)"),
        "bhagyank":    _numerology_entry(bhagyank, "Destiny Number (Bhagyank)"),
        "personal_year": {
            **_numerology_entry(personal_year_val, f"Personal Year {current_year}"),
            "year": current_year,
            "meaning": _PERSONAL_YEAR_MEANING.get(personal_year_val, ""),
        },
    }

    alpha = [c.upper() for c in name if c.isalpha()] if name else []

    if alpha:
        namank_raw = sum(_CHALDEAN.get(c, 0) for c in alpha)
        namank = _reduce_chaldean(namank_raw)

        soul_raw = sum(_CHALDEAN.get(c, 0) for c in alpha if c in _VOWELS)
        soul = _reduce_chaldean(soul_raw) if soul_raw else None

        pers_raw = sum(_CHALDEAN.get(c, 0) for c in alpha if c not in _VOWELS)
        personality = _reduce_chaldean(pers_raw) if pers_raw else None

        result["namank"] = _numerology_entry(namank, "Name Number (Namank)")
        if soul is not None:
            result["soul_number"] = _numerology_entry(soul, "Soul Number")
        if personality is not None:
            result["personality_number"] = _numerology_entry(personality, "Personality Number")
    else:
        result["namank"] = None
        result["soul_number"] = None
        result["personality_number"] = None

    return result
