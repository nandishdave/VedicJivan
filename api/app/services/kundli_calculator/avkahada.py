"""Avkahada Chakra — traditional Vedic chart attributes.

Varna, Vasya and Tatva are derived from the Moon sign (rashi).
Yoni, Gana, Nadi and Paya are derived from the Moon's nakshatra.
Matches what Astrosage and other classical Jyotish software display
on the basic-details page.
"""

from __future__ import annotations


# Yoni (animal yoni) by nakshatra index 0..26 — Sanskrit names per BPHS,
# matching the Astrosage PDF convention.
NAKSHATRA_YONI = [
    "Ashwa", "Gaja", "Mesha", "Sarpa", "Sarpa", "Shwan",
    "Marjara", "Mesha", "Marjara", "Mushak", "Mushak", "Gau",
    "Mahisha", "Vyaghra", "Mahisha", "Vyaghra", "Mriga", "Mriga",
    "Shwan", "Vanara", "Nakula", "Vanara", "Simha",
    "Ashwa", "Simha", "Gau", "Gaja",
]

# Gana by nakshatra index 0..26 — using Astrosage's "Devta" spelling.
NAKSHATRA_GANA = [
    "Devta", "Manushya", "Rakshasa", "Manushya", "Devta", "Manushya",
    "Devta", "Devta", "Rakshasa", "Rakshasa", "Manushya", "Manushya",
    "Devta", "Rakshasa", "Devta", "Rakshasa", "Devta", "Rakshasa",
    "Rakshasa", "Manushya", "Manushya", "Devta", "Rakshasa",
    "Rakshasa", "Manushya", "Manushya", "Devta",
]

# Nadi by nakshatra index 0..26 — Vata=Aadi, Pitta=Madhya, Kapha=Antya.
NAKSHATRA_NADI = [
    "Aadi", "Madhya", "Antya", "Antya", "Madhya", "Aadi",
    "Aadi", "Madhya", "Antya", "Antya", "Madhya", "Aadi",
    "Aadi", "Madhya", "Antya", "Antya", "Madhya", "Aadi",
    "Aadi", "Madhya", "Antya", "Antya", "Madhya", "Aadi",
    "Aadi", "Madhya", "Antya",
]

# Paya (metal) by nakshatra index 0..26 — one common classical assignment.
# Astrosage shows Anuradha = Silver, which this table matches.
NAKSHATRA_PAYA = [
    "Iron", "Iron", "Silver", "Silver", "Silver", "Silver",
    "Silver", "Silver", "Silver", "Copper", "Copper", "Copper",
    "Silver", "Silver", "Iron", "Iron", "Silver", "Silver",
    "Iron", "Copper", "Copper", "Silver", "Iron",
    "Iron", "Gold", "Gold", "Gold",
]

# Varna by Moon sign (rashi) index 0..11. Per BPHS — water signs Brahmin,
# fire Kshatriya, earth Vaishya, air Shudra.
RASHI_VARNA = [
    "Kshatriya",  # Aries (fire)
    "Vaishya",    # Taurus (earth)
    "Shudra",     # Gemini (air)
    "Brahmin",    # Cancer (water)
    "Kshatriya",  # Leo (fire)
    "Vaishya",    # Virgo (earth)
    "Shudra",     # Libra (air)
    "Brahmin",    # Scorpio (water)
    "Kshatriya",  # Sagittarius (fire)
    "Vaishya",    # Capricorn (earth)
    "Shudra",     # Aquarius (air)
    "Brahmin",    # Pisces (water)
]

# Vasya (controllability) by Moon sign index 0..11.
RASHI_VASYA = [
    "Chatuspada",  # Aries (quadruped)
    "Chatuspada",  # Taurus
    "Manava",      # Gemini (human)
    "Jalachara",   # Cancer (aquatic)
    "Vanachara",   # Leo (wild)
    "Manava",      # Virgo
    "Manava",      # Libra
    "Keeta",       # Scorpio (insect)
    "Chatuspada",  # Sagittarius (1st half — simplification)
    "Jalachara",   # Capricorn (2nd half) — simplification
    "Manava",      # Aquarius
    "Jalachara",   # Pisces
]

# Tatva (element) by Moon sign index 0..11.
RASHI_TATVA = [
    "Fire", "Earth", "Air", "Water",
    "Fire", "Earth", "Air", "Water",
    "Fire", "Earth", "Air", "Water",
]

SIGN_NAMES_EN = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]


def calc_avkahada(nakshatra_num: int, moon_sign: int) -> dict:
    """Return the traditional Avkahada Chakra attributes for the chart.

    Varna and Vasya are derived from the Moon sign (rashi); yoni, gana, nadi
    and paya are derived from the Moon's nakshatra. These match what Astrosage
    and other classical Jyotish software display on the basic-details page.
    """
    return {
        "varna": RASHI_VARNA[moon_sign],
        "vasya": RASHI_VASYA[moon_sign],
        "yoni": NAKSHATRA_YONI[nakshatra_num],
        "gana": NAKSHATRA_GANA[nakshatra_num],
        "nadi": NAKSHATRA_NADI[nakshatra_num],
        "paya": NAKSHATRA_PAYA[nakshatra_num],
        "tatva": RASHI_TATVA[moon_sign],
    }
