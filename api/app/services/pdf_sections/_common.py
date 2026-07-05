"""Shared foundation for the Kundli PDF sections: module imports, constant
tables, tiny formatting helpers, and the SVG/chart geometry. The section
builders (sections.py) depend on these; nothing here calls back into them.

Split out of the former 2676-line pdf_sections.py god-module."""


from __future__ import annotations


from app.services.kundli_calculator import (
    JAIMINI_CHARA_ROLES,
    SIGN_NAMES as _SIGN_NAMES_PDF,
    calc_nakshatra,
)
from app.services.kundli_data import (
    BHAVA_DATA,
    DASHA_PREDICTIONS,
    FAVOURABLE,
    GHATAK,
    LAGNA_DATA,
    MUNTHA_HOUSE_DATA,
    NAKSHATRA_DATA,
    NAKSHATRA_PADA_DATA,
    PLANET_IN_HOUSE,
    SADESATI_PHASES,
)

# MUDDA_DASHA_BHAV_DATA is large and authored separately; import lazily so the
# module still loads if the data file hasn't been regenerated.

# MUDDA_DASHA_BHAV_DATA is large and authored separately; import lazily so the
# module still loads if the data file hasn't been regenerated.
try:
    from app.services.kundli_data import MUDDA_DASHA_BHAV_DATA
except ImportError:
    MUDDA_DASHA_BHAV_DATA = {}

# LAL_KITAB_DATA is also large and authored separately.

# LAL_KITAB_DATA is also large and authored separately.
try:
    from app.services.kundli_data import LAL_KITAB_DATA
except ImportError:
    LAL_KITAB_DATA = {}

# Shared constants come from the dependency-free leaf module — no back-import
# from the facade, so there is no circular reference to reason about.

# Shared constants come from the dependency-free leaf module — no back-import
# from the facade, so there is no circular reference to reason about.
from app.services.pdf_constants import (
    BRAND,
    CHART_DESCRIPTIONS,
    LOGO_URL,
    PLANET_ABBR,
    PLANET_ORDER,
    SIGN_ABBR,
    SIGN_LORDS,
    SIGN_NAMES,
    _HOUSE_TEXT_POS,
)


# ── Local data tables ────────────────────────────────────────────────────────



# ── Local data tables ────────────────────────────────────────────────────────

_DIGNITY_COLOR = {
    "Exalted":       "#15803d",
    "Moolatrikona":  "#1d4ed8",
    "Own Sign":      "#1d4ed8",
    "Friendly Sign": "#0369a1",
    "Neutral Sign":  "#666",
    "Enemy Sign":    "#b45309",
    "Debilitated":   "#dc2626",
}
_BENEFIC_DIGNITIES = {"Exalted", "Moolatrikona", "Own Sign", "Friendly Sign"}
_MALEFIC_DIGNITIES = {"Enemy Sign", "Debilitated"}


_GEMSTONE: dict[str, str] = {
    "Sun":     "Ruby (Manik)",
    "Moon":    "Pearl (Moti)",
    "Mars":    "Red Coral (Moonga)",
    "Mercury": "Emerald (Panna)",
    "Jupiter": "Yellow Sapphire (Pukhraj)",
    "Venus":   "Diamond (Heera) / White Sapphire",
    "Saturn":  "Blue Sapphire (Neelam)",
    "Rahu":    "Hessonite (Gomed)",
    "Ketu":    "Cat's Eye (Lahsuniya)",
}
_MANTRA: dict[str, str] = {
    "Sun":     "Om Suryaya Namah — 108x, chanted at sunrise on Sundays",
    "Moon":    "Om Chandraya Namah — 108x, chanted on Mondays",
    "Mars":    "Om Angarakaya Namah — 108x, chanted on Tuesdays",
    "Mercury": "Om Budhaya Namah — 108x, chanted on Wednesdays",
    "Jupiter": "Om Guruve Namah — 108x, chanted on Thursdays",
    "Venus":   "Om Shukraya Namah — 108x, chanted on Fridays",
    "Saturn":  "Om Shanaischaraya Namah — 108x, chanted on Saturdays",
    "Rahu":    "Om Rahave Namah — 108x, chanted on Saturdays",
    "Ketu":    "Om Ketave Namah — 108x, chanted on Saturdays",
}
_DEITY: dict[str, str] = {
    "Sun":     "Lord Surya / Lord Vishnu",
    "Moon":    "Lord Shiva / Chandra Deva",
    "Mars":    "Lord Hanuman / Lord Kartikeya",
    "Mercury": "Lord Ganesha / Lord Vishnu",
    "Jupiter": "Lord Brahma / Lord Vishnu (Guru puja)",
    "Venus":   "Goddess Lakshmi / Goddess Parvati",
    "Saturn":  "Lord Shani / Lord Yama",
    "Rahu":    "Goddess Durga / Lord Bhairav",
    "Ketu":    "Lord Ganesha / Lord Bhairav",
}
_LUCKY_DAY: dict[str, str] = {
    "Sun": "Sunday", "Moon": "Monday", "Mars": "Tuesday",
    "Mercury": "Wednesday", "Jupiter": "Thursday",
    "Venus": "Friday", "Saturn": "Saturday",
    "Rahu": "Saturday", "Ketu": "Saturday",
}
_DONATION: dict[str, str] = {
    "Sun":     "Wheat, jaggery, copper items — on Sundays",
    "Moon":    "Rice, milk, white cloth — on Mondays",
    "Mars":    "Red lentils (masoor dal), red cloth — on Tuesdays",
    "Mercury": "Green moong dal, green cloth — on Wednesdays",
    "Jupiter": "Yellow gram, turmeric, yellow cloth — on Thursdays",
    "Venus":   "White rice, sugar, white cloth — on Fridays",
    "Saturn":  "Black sesame, mustard oil, black cloth — on Saturdays",
    "Rahu":    "Coconut, blue flowers, black items — on Saturdays",
    "Ketu":    "Blanket, black sesame, multi-coloured cloth — on Saturdays",
}


# ── Tiny utilities ──────────────────────────────────────────────────────────




# ── Tiny utilities ──────────────────────────────────────────────────────────

def _ordinal(n: int) -> str:
    """1 → '1st', 2 → '2nd', etc."""
    if 11 <= (n % 100) <= 13:
        return f"{n}th"
    return f"{n}{['th','st','nd','rd','th','th','th','th','th','th'][n % 10]}"




def _format_dasa_balance(planet: str, years: float) -> str:
    """Convert dasha balance from decimal years to 'Sat 1 Y 6 M 3 D' format."""
    total_days = int(round(years * 365.25))
    y = total_days // 365
    remaining = total_days - y * 365
    m = remaining // 30
    d = remaining - m * 30
    abbr = planet[:3]
    return f"{abbr} {y} Y {m} M {d} D"




def _svg_logo() -> str:
    """Inline SVG logo — vector, scales to any size without blur."""
    gold = "#d4a017"
    purple = "#7c3aed"
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 200" width="280" height="175"
         style="display: block; margin: 0 auto 10px;">
      <!-- Lotus petals -->
      <g transform="translate(160, 75)">
        <!-- Outer petals (gold) -->
        <ellipse cx="0" cy="-35" rx="12" ry="30" fill="{gold}" opacity="0.8"
                 transform="rotate(0)"/>
        <ellipse cx="0" cy="-35" rx="12" ry="30" fill="{gold}" opacity="0.7"
                 transform="rotate(30)"/>
        <ellipse cx="0" cy="-35" rx="12" ry="30" fill="{gold}" opacity="0.7"
                 transform="rotate(-30)"/>
        <ellipse cx="0" cy="-35" rx="12" ry="30" fill="{gold}" opacity="0.6"
                 transform="rotate(60)"/>
        <ellipse cx="0" cy="-35" rx="12" ry="30" fill="{gold}" opacity="0.6"
                 transform="rotate(-60)"/>
        <!-- Inner petals (purple) -->
        <ellipse cx="0" cy="-25" rx="8" ry="22" fill="{purple}" opacity="0.7"
                 transform="rotate(15)"/>
        <ellipse cx="0" cy="-25" rx="8" ry="22" fill="{purple}" opacity="0.7"
                 transform="rotate(-15)"/>
        <ellipse cx="0" cy="-25" rx="8" ry="22" fill="{purple}" opacity="0.8"
                 transform="rotate(0)"/>
        <!-- Center dot -->
        <circle cx="0" cy="0" r="6" fill="{gold}"/>
        <circle cx="0" cy="0" r="3" fill="{purple}"/>
        <!-- Sparkle dots -->
        <circle cx="-40" cy="-45" r="2" fill="{gold}" opacity="0.6"/>
        <circle cx="40" cy="-45" r="2" fill="{gold}" opacity="0.6"/>
        <circle cx="-25" cy="-55" r="1.5" fill="{gold}" opacity="0.4"/>
        <circle cx="25" cy="-55" r="1.5" fill="{gold}" opacity="0.4"/>
        <circle cx="0" cy="-65" r="2" fill="{gold}" opacity="0.5"/>
      </g>
      <!-- Brand text -->
      <text x="100" y="140" font-family="Georgia, 'Times New Roman', serif"
            font-size="28" fill="{gold}" font-weight="bold" letter-spacing="1">Vedic</text>
      <text x="177" y="142" font-family="Georgia, 'Times New Roman', serif"
            font-size="32" fill="{purple}" font-style="italic" letter-spacing="1">Jivan</text>
      <!-- Tagline -->
      <text x="160" y="165" text-anchor="middle" font-family="'Segoe UI', sans-serif"
            font-size="7" fill="#999" letter-spacing="3" text-transform="uppercase">CONNECT THE DIVINE WITHIN</text>
    </svg>"""


# ── Section builders + chart helpers ────────────────────────────────────────



# ── Section builders + chart helpers ────────────────────────────────────────

def _app_promo_banner() -> str:
    """In-report promotion for VedicJivan's paid consultations — fills the
    otherwise-empty lower half of the overview page (Astrosage runs an ad
    banner in the same spot) and converts free-report readers. Clickable link
    to the services/booking page."""
    return f"""
    <a href="https://vedicjivan.nandishdave.world/services" target="_blank" rel="noopener noreferrer" style="display:block; text-decoration:none;">
    <div style="margin-top:12px; border-radius:12px; overflow:hidden; page-break-inside:avoid;
                background:{BRAND}; background-image:linear-gradient(135deg,{BRAND},#9333ea);
                text-align:center; padding:18px 26px;">
        <div style="font-size:10pt; font-weight:bold; letter-spacing:2px; text-transform:uppercase; color:#f5d97a; margin-bottom:5px;">
            VedicJivan Consultations
        </div>
        <div style="font-size:16pt; font-weight:bold; color:#ffffff; line-height:1.2;">
            Want deeper guidance on <span style="color:#f5d97a;">your</span> chart?
        </div>
        <div style="font-size:10.5pt; color:#ece8fb; margin:8px auto 12px; max-width:470px; line-height:1.4;">
            Book a 1-on-1 consultation with our Vedic experts for personalised predictions,
            favourable timings and remedies tailored to your kundli.
        </div>
        <span style="display:inline-block; background:#f5d97a; color:#4c1d95; font-weight:bold;
                     font-size:12.5pt; padding:9px 30px; border-radius:24px;">
            Book a Consultation &nbsp;&#8594;
        </span>
    </div>
    </a>"""




def _planet_row(name: str, info: dict) -> str:
    retro = "*" if info["retrograde"] else ""
    return f"<tr><td><strong>{name}</strong></td><td>{info['sign_name']}</td><td>{info['degree_in_sign']:.1f}°</td><td>{info['house']}</td><td>{info['sign_lord']}</td><td>{retro}</td></tr>"




# ── North Indian Chart SVG + chart-data builders ────────────────────────────

def _chart_svg(house_signs: dict[int, int], house_planets: dict[int, list[str]], title: str = "", size: int = 280) -> str:
    """Render a North Indian style Kundli chart as inline SVG."""
    W = 300
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {W}" width="{size}" height="{size}"
        style="display: block; margin: 2px auto;">
    <rect x="1" y="1" width="{W-2}" height="{W-2}" fill="white" stroke="{BRAND}" stroke-width="2"/>
    <!-- Diamond connecting midpoints -->
    <polygon points="150,0 300,150 150,300 0,150" fill="none" stroke="{BRAND}" stroke-width="1.5"/>
    <!-- Diagonals -->
    <line x1="0" y1="0" x2="300" y2="300" stroke="{BRAND}" stroke-width="1" opacity="0.6"/>
    <line x1="300" y1="0" x2="0" y2="300" stroke="{BRAND}" stroke-width="1" opacity="0.6"/>
    """

    for house_num in range(1, 13):
        x, y = _HOUSE_TEXT_POS[house_num]
        sign = house_signs.get(house_num, 0)
        planets = house_planets.get(house_num, [])
        rashi_num = sign + 1
        svg += f'<text x="{x}" y="{y}" text-anchor="middle" font-size="14" font-weight="bold" fill="{BRAND}">{rashi_num}</text>'
        if planets:
            planet_str = " ".join(planets)
            if len(planets) <= 3:
                svg += f'<text x="{x}" y="{y + 16}" text-anchor="middle" font-size="12" fill="#333">{planet_str}</text>'
            else:
                line1 = " ".join(planets[:3])
                line2 = " ".join(planets[3:])
                svg += f'<text x="{x}" y="{y + 16}" text-anchor="middle" font-size="12" fill="#333">{line1}</text>'
                svg += f'<text x="{x}" y="{y + 30}" text-anchor="middle" font-size="12" fill="#333">{line2}</text>'

    svg += "</svg>"
    if title:
        svg += f'<div style="text-align: center; margin: 8px 0 12px; font-size: 14pt; font-weight: bold; color: {BRAND}; opacity: 0.7;">{title}</div>'
    return svg




def _build_d1_chart_data(d: dict) -> tuple[dict, dict]:
    """Build house_signs and house_planets dicts for D1 (Rasi) chart."""
    lagna_sign = d["lagna"]["sign"]
    house_signs = {}
    for h in range(1, 13):
        house_signs[h] = (lagna_sign + h - 1) % 12

    house_planets: dict[int, list[str]] = {h: [] for h in range(1, 13)}
    for name, info in d["planets"].items():
        house = info["house"]
        abbr = PLANET_ABBR.get(name, name[:2])
        if info.get("retrograde"):
            abbr += "*"
        house_planets[house].append(abbr)

    return house_signs, house_planets




def _build_divisional_chart_data(d: dict, chart_type: str) -> tuple[dict, dict]:
    """Build house_signs and house_planets for a divisional chart."""
    charts = d.get("divisional_charts", {})
    chart = charts.get(chart_type, {})
    if not chart:
        return {h: 0 for h in range(1, 13)}, {}

    lagna_sign = chart.get("Lagna", d["lagna"]["sign"])
    house_signs = {}
    for h in range(1, 13):
        house_signs[h] = (lagna_sign + h - 1) % 12

    house_planets: dict[int, list[str]] = {h: [] for h in range(1, 13)}
    planets_data = d.get("planets", {})
    for name in PLANET_ABBR:
        if name in chart:
            planet_sign = chart[name]
            house = ((planet_sign - lagna_sign) % 12) + 1
            abbr = PLANET_ABBR[name]
            if planets_data.get(name, {}).get("retrograde"):
                abbr += "*"
            house_planets[house].append(abbr)

    return house_signs, house_planets




def _build_jaimini_d1_chart(d: dict, override_lagna_sign: int) -> tuple[dict, dict]:
    """Build D1 (Rasi) chart house data rotated so `override_lagna_sign` is house 1."""
    house_signs = {h: (override_lagna_sign + h - 1) % 12 for h in range(1, 13)}
    house_planets: dict[int, list[str]] = {h: [] for h in range(1, 13)}
    for name, info in d.get("planets", {}).items():
        if name not in PLANET_ABBR:
            continue
        planet_sign = info["sign"]
        house = ((planet_sign - override_lagna_sign) % 12) + 1
        abbr = PLANET_ABBR[name]
        if info.get("retrograde"):
            abbr += "*"
        house_planets[house].append(abbr)
    return house_signs, house_planets




def _build_jaimini_d9_chart(d: dict, override_lagna_sign: int) -> tuple[dict, dict]:
    """Build D9 (Navamsa) chart house data rotated so `override_lagna_sign` is house 1."""
    charts = d.get("divisional_charts", {})
    d9 = charts.get("D9", {})
    if not d9:
        return {h: override_lagna_sign for h in range(1, 13)}, {}

    house_signs = {h: (override_lagna_sign + h - 1) % 12 for h in range(1, 13)}
    house_planets: dict[int, list[str]] = {h: [] for h in range(1, 13)}
    planets_data = d.get("planets", {})
    for name in PLANET_ABBR:
        if name in d9:
            planet_sign = d9[name]
            house = ((planet_sign - override_lagna_sign) % 12) + 1
            abbr = PLANET_ABBR[name]
            if planets_data.get(name, {}).get("retrograde"):
                abbr += "*"
            house_planets[house].append(abbr)
    return house_signs, house_planets


# ── At-a-glance + downstream sections ───────────────────────────────────────



def _sarva_chart(d: dict, av: dict) -> str:
    """Sarvashtakavarga chart — the 12 sign-totals laid out in a North-Indian
    chart oriented to the lagna (Astrosage's 'Ashtakvarga Chart')."""
    lagna_sign = d["lagna"]["sign"]
    house_signs = {h: (lagna_sign + h - 1) % 12 for h in range(1, 13)}
    # Put each house's Sarva total (for the sign occupying that house) as the
    # chart "planet" text. av["totals"] is indexed by absolute sign (0=Aries).
    house_planets = {h: [str(av["totals"][house_signs[h]])] for h in range(1, 13)}
    svg = _chart_svg(house_signs, house_planets, "Sarvashtakavarga Chart", size=260)
    return f'<div class="chart-block" style="text-align:center; margin-top:10px;">{svg}</div>'




def _moon_chart_svg(d: dict) -> str:
    """Render a Moon chart (Chandra Kundli) where Moon sign = House 1."""
    moon_sign = d["planets"]["Moon"]["sign"]
    house_signs = {}
    for h in range(1, 13):
        house_signs[h] = (moon_sign + h - 1) % 12

    house_planets: dict[int, list[str]] = {h: [] for h in range(1, 13)}
    for name, info in d["planets"].items():
        planet_sign = info["sign"]
        house = ((planet_sign - moon_sign) % 12) + 1
        abbr = PLANET_ABBR.get(name, name[:2])
        if info.get("retrograde"):
            abbr += "*"
        house_planets[house].append(abbr)

    return _chart_svg(house_signs, house_planets, "Moon")


# Re-export every public name (including the underscore-prefixed helpers)
# so `from ._common import *` in sections.py picks them all up.
__all__ = [n for n in dir() if not n.startswith("__") and n != "annotations"]
