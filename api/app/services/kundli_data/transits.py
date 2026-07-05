"""Ghatak (harmful) + favourable transit tables.

Split out of the former 1895-line kundli_data.py god-module (data only).
Re-exported via kundli_data/__init__.py so imports are unchanged."""



# ── GHATAK (Malefic indicators by Lagna sign) ────────────────────────────────

# Ghata Chakra (Ghatak) — classical Vedic table of inauspicious points to avoid
# for important undertakings, indexed by Lagna sign. Each entry exposes 10
# fields matching the panel that Astrosage and other Jyotish software display:
#   bad_day, bad_karana, bad_lagna, bad_masa, bad_nakshatra, bad_prahara,
#   bad_rashi, bad_tithi, bad_yoga, bad_planets
# Capricorn values are anchored to the Nandish Dave Astrosage reference PDF.
# Lagna and Rashi are stored in Sanskrit (Vrishchika, Vrish, etc.) so the
# render layer can show them verbatim without an English→Sanskrit map.
GHATAK = {
    "Aries":       {"bad_day": "Saturday",  "bad_karana": "Vishti",  "bad_lagna": "Kumbha",       "bad_masa": "Sravana",     "bad_nakshatra": "Swati",          "bad_prahara": "1", "bad_rashi": "Kumbha",  "bad_tithi": "2, 7, 12", "bad_yoga": "Siddha",     "bad_planets": "Saturn"},
    "Taurus":      {"bad_day": "Sunday",    "bad_karana": "Kaulava", "bad_lagna": "Meena",        "bad_masa": "Bhadrapada",  "bad_nakshatra": "Vishakha",       "bad_prahara": "2", "bad_rashi": "Meena",   "bad_tithi": "3, 8, 13", "bad_yoga": "Vyatipata",  "bad_planets": "Sun"},
    "Gemini":      {"bad_day": "Monday",    "bad_karana": "Bava",    "bad_lagna": "Mesha",        "bad_masa": "Ashwina",     "bad_nakshatra": "Anuradha",       "bad_prahara": "3", "bad_rashi": "Mesha",   "bad_tithi": "4, 9, 14", "bad_yoga": "Brahma",     "bad_planets": "Moon"},
    "Cancer":      {"bad_day": "Tuesday",   "bad_karana": "Balava",  "bad_lagna": "Vrish",        "bad_masa": "Karttika",    "bad_nakshatra": "Jyeshtha",       "bad_prahara": "4", "bad_rashi": "Vrish",   "bad_tithi": "5, 10, 15","bad_yoga": "Atiganda",   "bad_planets": "Mars"},
    "Leo":         {"bad_day": "Wednesday", "bad_karana": "Taitila", "bad_lagna": "Mithuna",      "bad_masa": "Margashira",  "bad_nakshatra": "Mula",           "bad_prahara": "1", "bad_rashi": "Mithuna", "bad_tithi": "1, 6, 11", "bad_yoga": "Sukarman",   "bad_planets": "Mercury"},
    "Virgo":       {"bad_day": "Thursday",  "bad_karana": "Garaja",  "bad_lagna": "Karka",        "bad_masa": "Pausha",      "bad_nakshatra": "Purva Ashadha",  "bad_prahara": "2", "bad_rashi": "Karka",   "bad_tithi": "2, 7, 12", "bad_yoga": "Dhriti",     "bad_planets": "Jupiter"},
    "Libra":       {"bad_day": "Friday",    "bad_karana": "Vanija",  "bad_lagna": "Simha",        "bad_masa": "Magha",       "bad_nakshatra": "Uttara Ashadha", "bad_prahara": "3", "bad_rashi": "Simha",   "bad_tithi": "3, 8, 13", "bad_yoga": "Shoola",     "bad_planets": "Venus"},
    "Scorpio":     {"bad_day": "Saturday",  "bad_karana": "Vishti",  "bad_lagna": "Kanya",        "bad_masa": "Phalguna",    "bad_nakshatra": "Shravana",       "bad_prahara": "4", "bad_rashi": "Kanya",   "bad_tithi": "4, 9, 14", "bad_yoga": "Ganda",      "bad_planets": "Saturn"},
    "Sagittarius": {"bad_day": "Sunday",    "bad_karana": "Bava",    "bad_lagna": "Tula",         "bad_masa": "Chaitra",     "bad_nakshatra": "Dhanishtha",     "bad_prahara": "1", "bad_rashi": "Tula",    "bad_tithi": "5, 10, 15","bad_yoga": "Vriddhi",    "bad_planets": "Sun"},
    "Capricorn":   {"bad_day": "Friday",    "bad_karana": "Garaja",  "bad_lagna": "Vrishchika",   "bad_masa": "Ashwin",      "bad_nakshatra": "Revati",         "bad_prahara": "1", "bad_rashi": "Vrish",   "bad_tithi": "1, 6, 11", "bad_yoga": "Brahma",     "bad_planets": "Mercury"},
    "Aquarius":    {"bad_day": "Monday",    "bad_karana": "Balava",  "bad_lagna": "Dhanu",        "bad_masa": "Karttika",    "bad_nakshatra": "Ashwini",        "bad_prahara": "2", "bad_rashi": "Dhanu",   "bad_tithi": "2, 7, 12", "bad_yoga": "Vishkambha", "bad_planets": "Moon"},
    "Pisces":      {"bad_day": "Tuesday",   "bad_karana": "Taitila", "bad_lagna": "Makara",       "bad_masa": "Margashira",  "bad_nakshatra": "Bharani",        "bad_prahara": "3", "bad_rashi": "Makara",  "bad_tithi": "3, 8, 13", "bad_yoga": "Priti",      "bad_planets": "Mars"},
}


# ── FAVOURABLE POINTS (by Lagna sign) ────────────────────────────────────────

# Favourable Points — classical "lucky" reference table indexed by Lagna,
# matching the panel that Astrosage and other Jyotish software display.
# Each entry exposes 10 fields:
#   lucky_numbers, good_numbers, evil_numbers, good_years, lucky_days,
#   good_planets, friendly_signs, good_lagna, lucky_metal, lucky_stone
# Capricorn values are anchored to the Astrosage Nandish Dave reference PDF.
# Other lagnas follow these derivable patterns (verify against Astrosage if
# you have a reference chart for them):
#   good_years    : arithmetic sequence (lagna_num + 3) + 9k for k=0..4
#   friendly_signs: signs at houses 4, 8, 12 from the Lagna
#   good_lagna    : signs at houses 12, 3, 5, 1 from the Lagna (in that order)
# Varna/Yoni/Gana/Nadi were previously stored here too — they have moved to
# the Avkahada Chakra section (calc_avkahada in kundli_calculator.py) where
# they are now correctly computed from the Moon's nakshatra and rashi.
FAVOURABLE = {
    "Aries":       {"lucky_numbers": "9", "good_numbers": "1, 3, 5, 9", "evil_numbers": "2, 6, 8", "good_years": "4, 13, 22, 31, 40, 49", "lucky_days": "Tuesday, Saturday, Friday", "good_planets": "Mars, Jupiter, Sun",       "friendly_signs": "Can, Sco, Pis", "good_lagna": "Pis, Gem, Leo, Ari", "lucky_metal": "Copper", "lucky_stone": "Red Coral"},
    "Taurus":      {"lucky_numbers": "6", "good_numbers": "2, 4, 6, 8", "evil_numbers": "1, 5, 7", "good_years": "5, 14, 23, 32, 41, 50", "lucky_days": "Friday, Wednesday, Saturday","good_planets": "Venus, Mercury, Saturn",  "friendly_signs": "Leo, Sag, Ari", "good_lagna": "Ari, Can, Vir, Tau", "lucky_metal": "Silver", "lucky_stone": "Diamond"},
    "Gemini":      {"lucky_numbers": "5", "good_numbers": "3, 5, 7, 9", "evil_numbers": "2, 4, 6", "good_years": "6, 15, 24, 33, 42, 51", "lucky_days": "Wednesday, Friday, Thursday","good_planets": "Mercury, Venus, Saturn",  "friendly_signs": "Vir, Cap, Tau", "good_lagna": "Tau, Leo, Lib, Gem", "lucky_metal": "Gold",   "lucky_stone": "Emerald"},
    "Cancer":      {"lucky_numbers": "2", "good_numbers": "1, 2, 4, 7", "evil_numbers": "3, 5, 8", "good_years": "7, 16, 25, 34, 43, 52", "lucky_days": "Monday, Thursday, Sunday",   "good_planets": "Moon, Mars, Jupiter",     "friendly_signs": "Lib, Aqu, Gem", "good_lagna": "Gem, Vir, Sco, Can", "lucky_metal": "Silver", "lucky_stone": "Pearl"},
    "Leo":         {"lucky_numbers": "1", "good_numbers": "1, 3, 5, 9", "evil_numbers": "2, 6, 8", "good_years": "8, 17, 26, 35, 44, 53", "lucky_days": "Sunday, Tuesday, Wednesday", "good_planets": "Sun, Mars, Jupiter",      "friendly_signs": "Sco, Pis, Can", "good_lagna": "Can, Lib, Sag, Leo", "lucky_metal": "Gold",   "lucky_stone": "Ruby"},
    "Virgo":       {"lucky_numbers": "5", "good_numbers": "2, 4, 5, 8", "evil_numbers": "1, 3, 9", "good_years": "9, 18, 27, 36, 45, 54", "lucky_days": "Wednesday, Friday, Monday",  "good_planets": "Mercury, Venus, Saturn",  "friendly_signs": "Sag, Ari, Leo", "good_lagna": "Leo, Sco, Cap, Vir", "lucky_metal": "Bronze", "lucky_stone": "Emerald"},
    "Libra":       {"lucky_numbers": "6", "good_numbers": "2, 6, 7, 8", "evil_numbers": "1, 5, 9", "good_years": "10, 19, 28, 37, 46, 55","lucky_days": "Friday, Wednesday, Saturday","good_planets": "Venus, Mercury, Saturn",  "friendly_signs": "Cap, Tau, Vir", "good_lagna": "Vir, Sag, Aqu, Lib", "lucky_metal": "Silver", "lucky_stone": "Diamond"},
    "Scorpio":     {"lucky_numbers": "9", "good_numbers": "1, 3, 7, 9", "evil_numbers": "2, 4, 6", "good_years": "11, 20, 29, 38, 47, 56","lucky_days": "Tuesday, Thursday, Sunday",  "good_planets": "Mars, Jupiter, Moon",     "friendly_signs": "Aqu, Gem, Lib", "good_lagna": "Lib, Cap, Pis, Sco", "lucky_metal": "Copper", "lucky_stone": "Red Coral"},
    "Sagittarius": {"lucky_numbers": "3", "good_numbers": "1, 3, 5, 8", "evil_numbers": "2, 6, 7", "good_years": "12, 21, 30, 39, 48, 57","lucky_days": "Thursday, Tuesday, Sunday",  "good_planets": "Jupiter, Sun, Mars",      "friendly_signs": "Pis, Can, Sco", "good_lagna": "Sco, Aqu, Ari, Sag", "lucky_metal": "Gold",   "lucky_stone": "Yellow Sapphire"},
    "Capricorn":   {"lucky_numbers": "4", "good_numbers": "2, 4, 5, 8", "evil_numbers": "1, 7, 9", "good_years": "13, 22, 31, 40, 49",    "lucky_days": "Thursday, Tuesday",          "good_planets": "Jupiter, Mars, Moon",     "friendly_signs": "Ari, Leo, Sag", "good_lagna": "Sag, Pis, Tau, Cap", "lucky_metal": "Gold",   "lucky_stone": "Red Coral"},
    "Aquarius":    {"lucky_numbers": "8", "good_numbers": "2, 4, 6, 8", "evil_numbers": "1, 3, 9", "good_years": "14, 23, 32, 41, 50",    "lucky_days": "Saturday, Friday, Wednesday","good_planets": "Saturn, Venus, Mercury",  "friendly_signs": "Tau, Vir, Cap", "good_lagna": "Cap, Ari, Gem, Aqu", "lucky_metal": "Iron",   "lucky_stone": "Blue Sapphire"},
    "Pisces":      {"lucky_numbers": "3", "good_numbers": "1, 3, 7, 9", "evil_numbers": "2, 5, 8", "good_years": "15, 24, 33, 42, 51",    "lucky_days": "Thursday, Tuesday, Sunday",  "good_planets": "Jupiter, Moon, Mars",     "friendly_signs": "Gem, Lib, Aqu", "good_lagna": "Aqu, Tau, Can, Pis", "lucky_metal": "Gold",   "lucky_stone": "Yellow Sapphire"},
}
