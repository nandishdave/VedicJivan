"""Shared constants for the Kundli PDF (leaf module — imports nothing local).

Previously these lived at the top of `kundli_pdf.py` and `pdf_sections.py`
back-imported them from there, creating a circular import that only held
together because of statement ordering (kundli_pdf defined the constants
*before* its `from .pdf_sections import ...` line fired). Hoisting them into a
dependency-free leaf that BOTH modules import removes the cycle entirely.

`kundli_pdf` re-exports every name from here, so existing
`from app.services.kundli_pdf import BRAND` / `kundli_pdf.LOGO_URL` access
keeps working unchanged.
"""

from __future__ import annotations

LOGO_URL = "https://vedicjivan-website.s3.ap-south-1.amazonaws.com/images/logo/logo-final.png"
BRAND = "#7c3aed"

SIGN_ABBR = ["Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]
SIGN_NAMES = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]
SIGN_LORDS = [
    "Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
    "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter",
]
PLANET_ABBR = {
    "Sun": "Su", "Moon": "Mo", "Mars": "Ma", "Mercury": "Me",
    "Jupiter": "Ju", "Venus": "Ve", "Saturn": "Sa", "Rahu": "Ra", "Ketu": "Ke",
    "Uranus": "Ur", "Neptune": "Ne", "Pluto": "Pl",
}
# Canonical display order for the nine classical bodies (Sun→Ketu).
PLANET_ORDER = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]

# North Indian chart house text positions (x, y) in a 300×300 SVG
# Houses go COUNTER-CLOCKWISE from top center (standard North Indian layout)
_HOUSE_TEXT_POS = {
    1:  (150, 68),    # top center
    2:  (75, 25),     # top left
    3:  (30, 68),     # left upper
    4:  (75, 150),    # left center
    5:  (30, 232),    # left lower
    6:  (75, 275),    # bottom left
    7:  (150, 232),   # bottom center
    8:  (225, 275),   # bottom right
    9:  (270, 232),   # right lower
    10: (225, 150),   # right center
    11: (270, 68),    # right upper
    12: (225, 25),    # top right
}

CHART_DESCRIPTIONS = {
    "D1": ("Rasi Chart (Lagna)", "The Rasi or Lagna chart is the main birth chart showing the positions of all planets in the zodiac signs at the time of birth. This is the foundation of all Vedic astrology analysis."),
    "D2": ("Hora Chart", "The Hora chart divides each sign into two halves and is primarily used for analyzing wealth and financial matters. Planets in Sun's Hora (Leo) indicate wealth through effort, while Moon's Hora (Cancer) indicates wealth through inheritance or luck."),
    "D3": ("Drekkana Chart", "The Drekkana chart divides each sign into three equal parts and is used for analyzing siblings, courage, and communication."),
    "D4": ("Chaturthamsha Chart", "The Chaturthamsha divides each sign into four parts and is used for analyzing property, home, fixed assets, and luck."),
    "D6": ("Shashtiamsha (Health)", "The six-fold division is used for analyzing health, disease, enemies, and obstacles."),
    "D7": ("Saptamsha Chart", "The Saptamsha divides each sign into seven parts and is used for analyzing children, progeny, and creative potential."),
    "D8": ("Ashtamsha Chart", "The Ashtamsha divides each sign into eight parts and relates to longevity, sudden events, and hidden matters."),
    "D9": ("Navamsa Chart", "The Navamsa is the most important divisional chart after the Rasi chart. It divides each sign into nine parts and is primarily used for marriage analysis, spouse characteristics, and the overall strength of planets."),
    "D10": ("Dasamsa Chart", "The Dasamsa chart divides each sign into ten parts and is specifically used for career and professional analysis. It reveals the nature of one's profession, career achievements, and public reputation."),
    "D11": ("Ekadamsha (Rudramsa)", "The Ekadamsha divides each sign into eleven parts and is used for analyzing gains from networks, friends, and large groups."),
    "D12": ("Dwadasamsa Chart", "The Dwadasamsa divides each sign into twelve parts and is used for analyzing parents, lineage, and ancestral karma."),
    "D16": ("Shodashamsha Chart", "The Shodashamsha divides each sign into sixteen parts and relates to vehicles, travel, conveyances, and comforts."),
    "D20": ("Vimsamsha Chart", "The Vimsamsha divides each sign into twenty parts and is used for analyzing spiritual practices, religious inclinations, and deity alignment."),
    "D24": ("Chaturvimsamsha Chart", "The Chaturvimsamsha divides each sign into twenty-four parts and relates to education, learning, and academic achievements."),
    "D27": ("Saptavimsamsha (Bhamsa)", "The Saptavimsamsha divides each sign into twenty-seven parts and is used for assessing overall strength and weaknesses."),
    "D30": ("Trimsamsha Chart", "The Trimsamsha uses unequal divisions and relates to misfortune, karmic burdens, and moral character."),
    "D40": ("Khavedamsha Chart", "The Khavedamsha divides each sign into forty parts and relates to auspicious/inauspicious results and overall well-being."),
    "D45": ("Akshvedamsha Chart", "The Akshvedamsha divides each sign into forty-five parts and is used for assessing general well-being and paternal legacy."),
    "D60": ("Shastiamsa Chart", "The Shastiamsa is the most subtle divisional chart, dividing each sign into sixty parts. Classical texts consider it the final arbiter of planetary strength."),
}
