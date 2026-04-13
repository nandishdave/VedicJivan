"""
Kundli PDF generator using WeasyPrint.
Builds a styled HTML document from chart_data, then converts to PDF bytes.
"""

from __future__ import annotations

from datetime import datetime

from app.services.kundli_data import (
    BHAVA_DATA,
    DASHA_PREDICTIONS,
    FAVOURABLE,
    GHATAK,
    LAGNA_DATA,
    NAKSHATRA_DATA,
    PLANET_IN_HOUSE,
    SADESATI_PHASES,
)

LOGO_URL = "https://vedicjivan-website.s3.ap-south-1.amazonaws.com/images/logo/logo-email.jpg"
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


def generate_pdf(chart_data: dict, sections: list[dict] | None = None) -> bytes:
    """Generate a Kundli report PDF from chart_data dict. Returns raw PDF bytes.

    sections: optional ordered list of `{id, enabled, ...}` dicts (from the
    admin report-section toggles in MongoDB). If None, the default order
    matching DEFAULT_REPORT_SECTIONS is used and the output is byte-identical
    to the pre-toggle behaviour.
    """
    html = _build_html(chart_data, sections)
    from weasyprint import HTML
    return HTML(string=html).write_pdf()


# ── HTML builder ─────────────────────────────────────────────────────────────

# Section ID → builder. Each builder takes the chart_data dict and returns an
# HTML string. Cover, footer, and CSS are not toggleable — they always render.
SECTION_BUILDERS = {
    "birth_chart":      lambda d: _birth_chart_page(d),
    "basic_details":    lambda d: _basic_details(d),
    "avkahada":         lambda d: _avkahada_chakra(d),
    "favourable":       lambda d: _favourable_section(d),
    "ghatak":           lambda d: _ghatak_section(d),
    "planet_consideration": lambda d: _planet_consideration_section(d),
    "ascendant":        lambda d: _ascendant_section(d),
    "nakshatra":        lambda d: _nakshatra_section(d),
    "character_life":   lambda d: _character_life(d),
    "yogas":            lambda d: _yogas_section(d),
    "doshas":           lambda d: _doshas_section(d),
    "bhava_analysis":   lambda d: _bhava_analysis(d),
    "manglik":          lambda d: _manglik_section(d),
    "sadesati":         lambda d: _sadesati_section(d),
    "gochar":           lambda d: _gochar_section(d),
    "dasha":            lambda d: _dasha_section(d),
    "mahadasha_phal":   lambda d: _mahadasha_phal_section(d),
    "antardasha":       lambda d: _antardasha_section(d),
    "pratyantar":       lambda d: _pratyantar_section(d),
    "yogini_dasha":     lambda d: _yogini_dasha_section(d),
    "divisional":       lambda d: _divisional_charts_section(d),
    "shodashvarga":     lambda d: _shodashvarga_table_section(d),
    "friendship":       lambda d: _friendship_section(d),
    "shadbala":         lambda d: _shadbala_section(d),
    "western_aspects":  lambda d: _western_aspects_section(d),
    "graha_drishti":    lambda d: _graha_drishti_section(d),
    "planet_positions": lambda d: _planet_positions(d),
    "numerology":       lambda d: _numerology_section(d),
    "remedies":         lambda d: _remedies_section(d),
}

# Default order — Astrosage page-2 layout (basic details → avkahada →
# favourable → ghatak) followed by the rest of the report.
_DEFAULT_SECTION_ORDER = [
    "birth_chart",
    "basic_details",
    "avkahada",
    "favourable",
    "ghatak",
    "planet_consideration",
    "ascendant",
    "nakshatra",
    "character_life",
    "yogas",
    "doshas",
    "bhava_analysis",
    "manglik",
    "sadesati",
    "gochar",
    "dasha",
    "mahadasha_phal",
    "antardasha",
    "pratyantar",
    "yogini_dasha",
    "divisional",
    "shodashvarga",
    "friendship",
    "shadbala",
    "western_aspects",
    "graha_drishti",
    "planet_positions",
    "numerology",
    "remedies",
]


def _build_html(d: dict, sections: list[dict] | None = None) -> str:
    """Build the full HTML document for the Kundli report.

    If `sections` is None, render the default ordered list (byte-identical to
    pre-toggle output). Otherwise iterate the provided list, skipping any
    section where `enabled` is falsy or whose id has no registered builder.
    """
    if sections is None:
        body_section_ids = _DEFAULT_SECTION_ORDER
    else:
        # Use _DEFAULT_SECTION_ORDER for ordering (source of truth for layout),
        # and the sections list only for enabled/disabled filtering. This prevents
        # stale MongoDB order values from scrambling the report layout.
        enabled_ids = {
            s["id"] for s in sections
            if s.get("enabled", True) and s.get("id") in SECTION_BUILDERS
        }
        body_section_ids = [sid for sid in _DEFAULT_SECTION_ORDER if sid in enabled_ids]

    parts = [_css(), _cover(d)]
    for sid in body_section_ids:
        builder = SECTION_BUILDERS.get(sid)
        if builder is not None:
            parts.append(builder(d))
    parts.append(_footer())

    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Kundli Report - {d['name']}</title></head>
<body>{''.join(parts)}</body>
</html>"""


def _css() -> str:
    return f"""<style>
    @page {{ size: A4; margin: 20mm 15mm 25mm 15mm;
        @bottom-center {{ content: "Page " counter(page) " of " counter(pages); font-size: 8pt; color: #999; }}
        @bottom-right {{ content: "VedicJivan"; font-size: 8pt; color: {BRAND}; }}
    }}
    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333; line-height: 1.6; font-size: 11pt; }}
    h1 {{ color: {BRAND}; text-align: center; font-size: 22pt; margin: 0 0 5px; }}
    h2 {{ color: {BRAND}; font-size: 16pt; border-bottom: 2px solid {BRAND}; padding-bottom: 4px; margin-top: 30px; page-break-after: avoid; }}
    h3 {{ color: #555; font-size: 13pt; margin-top: 18px; page-break-after: avoid; }}
    table {{ width: 100%; border-collapse: collapse; margin: 10px 0 15px; }}
    th {{ background: {BRAND}; color: white; padding: 8px 10px; text-align: left; font-size: 10pt; }}
    td {{ padding: 7px 10px; border-bottom: 1px solid #e5e5e5; font-size: 10pt; }}
    tr:nth-child(even) {{ background: #f9f7ff; }}
    .cover {{ text-align: center; padding: 80px 0 60px; page-break-after: always; }}
    .cover img {{ height: 80px; margin-bottom: 30px; }}
    .cover .name {{ font-size: 28pt; color: {BRAND}; font-weight: bold; margin: 10px 0; }}
    .cover .sub {{ font-size: 12pt; color: #666; margin: 5px 0; }}
    .section {{ page-break-inside: avoid; }}
    .chart-block {{ page-break-inside: avoid; }}
    table {{ page-break-inside: avoid; }}
    .two-col {{ display: flex; gap: 20px; }}
    .two-col > div {{ flex: 1; }}
    .remedy {{ background: #f3f0ff; border-left: 3px solid {BRAND}; padding: 8px 12px; margin: 5px 0; font-size: 10pt; }}
    .manglik-yes {{ background: #fef2f2; border: 1px solid #f87171; padding: 12px; border-radius: 6px; }}
    .manglik-no {{ background: #f0fdf4; border: 1px solid #4ade80; padding: 12px; border-radius: 6px; }}
    .phase-card {{ background: #f9f7ff; border-left: 4px solid {BRAND}; padding: 10px 14px; margin: 8px 0; }}
    .footer {{ text-align: center; color: #999; font-size: 9pt; margin-top: 40px; border-top: 1px solid #eee; padding-top: 10px; }}
    .page-break {{ page-break-before: always; }}
    p {{ margin: 6px 0; }}
    </style>"""


def _cover(d: dict) -> str:
    generated = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    return f"""
    <div class="cover">
        <img src="{LOGO_URL}" alt="VedicJivan" />
        <div style="font-size: 12pt; color: #666; letter-spacing: 2px; text-transform: uppercase;">Vedic Birth Chart</div>
        <div class="name">{d['name']}</div>
        <div class="sub"><strong>Date of Birth:</strong> {d['dob']} &nbsp;|&nbsp; <strong>Time:</strong> {d['tob']}</div>
        <div class="sub"><strong>Place:</strong> {d['place_name']}</div>
        <div class="sub"><strong>Gender:</strong> {d['gender'].title()}</div>
        <hr style="border: none; border-top: 2px solid {BRAND}; width: 60%; margin: 30px auto;" />
        <div class="sub" style="margin-top: 20px;">Generated on {generated}</div>
        <div class="sub" style="color: {BRAND};">vedicjivan.nandishdave.world</div>
    </div>"""


def _basic_details(d: dict) -> str:
    """Astrosage-style Basic Details panel.

    Mirrors the leftmost panel on Astrosage page 2 — birth particulars,
    coordinates, time conversions, panchanga summary and luminary timings.
    """
    pan = d["panchanga"]
    bt = d.get("birth_time", {})

    # Day duration: sunset - sunrise. Accepts either HH:MM or HH:MM:SS.
    sr = d.get("sunrise", "N/A")
    ss = d.get("sunset", "N/A")
    day_duration = "—"
    try:
        def _to_seconds(t: str) -> int:
            parts = t.split(":")
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + (int(parts[2]) if len(parts) > 2 else 0)
        total = _to_seconds(ss) - _to_seconds(sr)
        if total < 0:
            total += 86400
        day_duration = f"{total // 3600:02d}:{(total % 3600) // 60:02d}:{total % 60:02d}"
    except (ValueError, AttributeError, IndexError):
        pass

    rows = [
        ("Sex", d["gender"].title()),
        ("Date of Birth", d["dob"].replace("-", " : ")),
        ("Time of Birth", d["tob"] + ":00"),
        ("Day of Birth", bt.get("day_of_birth", "—")),
        ("Ishtkaal", bt.get("ishtkaal", "—")),
        ("Place of Birth", d["place_name"]),
        ("Time Zone", str(bt.get("tz_offset_hours", "—"))),
        ("Latitude", bt.get("latitude_dms", "—")),
        ("Longitude", bt.get("longitude_dms", "—")),
        ("Local Time Correction", bt.get("local_time_correction", "—")),
        ("LMT at Birth", bt.get("lmt_at_birth", "—")),
        ("GMT at Birth", bt.get("gmt_at_birth", "—")),
        ("Sidereal Time", bt.get("sidereal_time", "—")),
        ("Tithi", pan["tithi_name"]),
        ("Paksha", pan["paksha"]),
        ("Yoga", pan["yoga_name"]),
        ("Karan", pan["karan_name"]),
        ("Sunrise", sr),
        ("Sunset", ss),
        ("Day Duration", day_duration),
    ]

    rows_html = "".join(
        f"<tr><td style='font-weight:bold; color:#555; width:45%;'>{label}</td><td>{value}</td></tr>"
        for label, value in rows
    )
    return f"""
    <h2>Basic Details</h2>
    <table>{rows_html}</table>"""


def _avkahada_chakra(d: dict) -> str:
    """Astrosage-style Avkahada Chakra — traditional Vedic chart attributes."""
    av = d.get("avkahada", {})
    lagna = d["lagna"]
    nak = d["nakshatra"]
    moon = d["planets"]["Moon"]
    dasha = d["dasha"]["dashas"][0]

    # Sun sign — sidereal Indian and tropical Western (rough approximation:
    # Western = Indian + 1 sign for the equinox precession of ~24°).
    sun = d["planets"]["Sun"]
    sun_sign_indian = sun["sign_name"]

    rows = [
        ("Paya (Nakshatra Based)", av.get("paya", "—")),
        ("Varna", av.get("varna", "—")),
        ("Vasya", av.get("vasya", "—")),
        ("Yoni", av.get("yoni", "—")),
        ("Gana", av.get("gana", "—")),
        ("Nadi", av.get("nadi", "—")),
        ("Tatva", av.get("tatva", "—")),
        ("Dasa Balance", f"{dasha['planet']}  {dasha['years']:.1f} years"),
        ("Lagna", lagna["sign_name"]),
        ("Lagna Lord", lagna["sign_lord"]),
        ("Rasi", moon["sign_name"]),
        ("Rasi Lord", moon["sign_lord"]),
        ("Nakshatra - Pada", f"{nak['name']} - {nak['pada']}"),
        ("Nakshatra Lord", nak["lord"]),
        ("SunSign (Indian)", sun_sign_indian),
        ("Ayanamsa", f"{d['ayanamsa']:.4f}°"),
        ("Ayanamsa Name", "Lahiri"),
        ("Julian Day", str(d["julian_day"])),
    ]

    rows_html = "".join(
        f"<tr><td style='font-weight:bold; color:#555; width:45%;'>{label}</td><td>{value}</td></tr>"
        for label, value in rows
    )
    return f"""
    <h2>Avkahada Chakra</h2>
    <table>{rows_html}</table>"""


def _planet_row(name: str, info: dict) -> str:
    retro = "*" if info["retrograde"] else ""
    return f"<tr><td><strong>{name}</strong></td><td>{info['sign_name']}</td><td>{info['degree_in_sign']:.1f}°</td><td>{info['house']}</td><td>{info['sign_lord']}</td><td>{retro}</td></tr>"


def _favourable_section(d: dict) -> str:
    """Astrosage-style Favourable Points panel.

    Renders the 10 Favourable Points fields in Astrosage's display order:
    Lucky Numbers → Good Numbers → Evil Numbers → Good Years → Lucky Days →
    Good Planets → Friendly Signs → Good Lagna → Lucky Metal → Lucky Stone.
    """
    sign = d["lagna"]["sign_name"]
    fav = FAVOURABLE.get(sign, {})
    ordered_fields = [
        ("lucky_numbers",  "Lucky Numbers"),
        ("good_numbers",   "Good Numbers"),
        ("evil_numbers",   "Evil Numbers"),
        ("good_years",     "Good Years"),
        ("lucky_days",     "Lucky Days"),
        ("good_planets",   "Good Planets"),
        ("friendly_signs", "Friendly Signs"),
        ("good_lagna",     "Good Lagna"),
        ("lucky_metal",    "Lucky Metal"),
        ("lucky_stone",    "Lucky Stone"),
    ]
    rows = "".join(
        f"<tr><td style='font-weight:bold; color:#555; width:45%;'>{label}</td><td>{fav.get(key, '—')}</td></tr>"
        for key, label in ordered_fields
    )
    return f"""
    <h2>Favourable Points</h2>
    <table>{rows}</table>"""


def _planet_consideration_section(d: dict) -> str:
    """Astrosage-style 'Planet Consideration' — per-planet narrative with
    sign, house, lordship, aspects given/received, and interpretation.

    Matches Astrosage pages 35-39: one block per planet with a summary header
    line (sign, dignity, lordship, aspects) followed by interpretation text.
    """
    lagna_sign = d["lagna"]["sign"]
    gd = d.get("graha_drishti", {})
    planet_aspects = gd.get("planet_aspects", {})
    house_aspected_by = gd.get("house_aspected_by", {})

    # Lordship: for each planet, which houses (1-12) does it lord for this lagna?
    _SIGN_LORD_MAP = {
        "Sun": [4], "Moon": [3], "Mars": [0, 7], "Mercury": [2, 5],
        "Jupiter": [8, 11], "Venus": [1, 6], "Saturn": [9, 10],
    }

    def _lordship_houses(planet_name: str) -> list[int]:
        signs = _SIGN_LORD_MAP.get(planet_name, [])
        houses = []
        for s in signs:
            h = ((s - lagna_sign) % 12) + 1
            houses.append(h)
        return sorted(houses)

    html = '<div class="page-break"></div><h2>Planet Considerations</h2>'
    html += "<p>Each planet's placement by sign, house, lordship, and aspects — with interpretation based on classical Vedic texts.</p>"

    # Classical 7 + Rahu/Ketu
    ordered_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]

    for name in ordered_planets:
        if name not in d["planets"]:
            continue
        info = d["planets"][name]
        sign_name = info["sign_name"]
        dignity = info.get("dignity", "")
        house = info["house"]

        # Lordship
        lord_houses = _lordship_houses(name)
        if lord_houses:
            lord_str = ", ".join(f"{_ordinal(h)}" for h in lord_houses)
        else:
            lord_str = "—"

        # Houses this planet aspects
        aspects_out = planet_aspects.get(name, [])
        aspects_out_str = ", ".join(f"{_ordinal(h)}" for h in aspects_out) if aspects_out else "—"

        # Planets aspecting this planet's house
        aspected_by = [p for p in house_aspected_by.get(str(house), []) if p != name]
        aspected_by_str = ", ".join(aspected_by) if aspected_by else "None"

        # Dignity label for Astrosage-style summary.
        # Dignity values like "Friendly Sign" already include "Sign", so avoid
        # double-"sign" ("a Friendly Sign sign"). Just prepend "a/an".
        if dignity:
            article = "an" if dignity[0].lower() in "aeiou" else "a"
            # If dignity already ends with "Sign", use as-is; otherwise append "sign"
            dignity_label = f"{article} {dignity}" if "Sign" in dignity else f"{article} {dignity} sign"
        else:
            dignity_label = "—"

        # Summary header
        summary = (
            f"Your {name} is in <strong>{sign_name}</strong> sign which is {dignity_label} for {name}. "
            f"{name} is lord of <strong>{lord_str}</strong> house and situated in "
            f"<strong>{_ordinal(house)}</strong> house. "
            f"{name} aspects <strong>{aspects_out_str}</strong> house and "
            f"aspected by <strong>{aspected_by_str}</strong>."
        )

        # Interpretation text from PLANET_IN_HOUSE
        interp = PLANET_IN_HOUSE.get(name, {}).get(house, {})
        benefic = interp.get("benefic", "")
        malefic = interp.get("malefic", "")
        remedies = interp.get("remedies", [])

        interp_html = ""
        if benefic:
            interp_html += f"<p>{benefic}</p>"
        if malefic:
            interp_html += f"<p>{malefic}</p>"

        remedies_html = ""
        if remedies:
            remedies_html = '<h4 style="margin: 8px 0 4px;">Remedies</h4>'
            for r in remedies:
                remedies_html += f'<div class="remedy">{r}</div>'

        html += f"""
        <div class="section">
            <h3>{name} Consideration</h3>
            <p style="color:#555;">{summary}</p>
            {interp_html}
            {remedies_html}
        </div>"""

    return html


def _graha_drishti_section(d: dict) -> str:
    """Vedic Graha Drishti (planetary aspects) — two-way view.

    Table 1: Each planet → which houses it aspects.
    Table 2: Each house → which planets aspect it.
    Uses the classical rules: all planets aspect 7th; Mars 4th/8th;
    Jupiter 5th/9th; Saturn 3rd/10th; Rahu/Ketu 5th/9th.
    """
    gd = d.get("graha_drishti")
    if not gd:
        return ""

    lagna_sign = d["lagna"]["sign"]

    # Table 1: Planet → aspected houses
    rows1 = ""
    for name, houses in gd["planet_aspects"].items():
        house_str = ", ".join(
            f"{h} ({SIGN_NAMES[(lagna_sign + h - 1) % 12]})"
            for h in houses
        )
        rows1 += f"<tr><td><strong>{name}</strong> (H{d['planets'][name]['house']})</td><td>{house_str}</td></tr>"

    # Table 2: House → aspecting planets
    rows2 = ""
    for h in range(1, 13):
        sign_name = SIGN_NAMES[(lagna_sign + h - 1) % 12]
        aspecting = gd["house_aspected_by"].get(str(h), [])
        planets_str = ", ".join(aspecting) if aspecting else "—"
        rows2 += f"<tr><td><strong>H{h} ({sign_name})</strong></td><td>{planets_str}</td></tr>"

    return f"""
    <div class="page-break"></div>
    <h2>Graha Drishti (Vedic Planetary Aspects)</h2>
    <p style='font-size:10pt; color:#666;'>Classical Vedic aspects: all planets aspect the 7th house from themselves.
    Mars also aspects 4th &amp; 8th; Jupiter 5th &amp; 9th; Saturn 3rd &amp; 10th; Rahu/Ketu 5th &amp; 9th.</p>

    <h3>Planet → Houses Aspected</h3>
    <table>
        <tr><th>Planet (House)</th><th>Aspects Houses</th></tr>
        {rows1}
    </table>

    <h3>House → Aspected By</h3>
    <table>
        <tr><th>House (Sign)</th><th>Aspected By</th></tr>
        {rows2}
    </table>"""


def _western_aspects_section(d: dict) -> str:
    """Astrosage-style Western Planetary Aspects matrix.

    Renders all planet-pair aspects (Conjunction, Opposition, Trine, Square,
    Sextile and minor aspects) with their orbs. Cells with no aspect show "—".
    """
    wa = d.get("western_aspects")
    if not wa:
        return ""

    planets = wa["planets"]
    matrix = wa["matrix"]

    header = "<th></th>" + "".join(
        f"<th style='text-align:center; font-size:8pt; padding:4px;'>{PLANET_ABBR.get(p, p[:2])}</th>"
        for p in planets
    )

    rows = ""
    for from_p in planets:
        cells = ""
        for to_p in planets:
            if from_p == to_p:
                cells += "<td style='text-align:center; background:#f3f0ff;'>—</td>"
            else:
                asp = matrix[from_p].get(to_p)
                if asp:
                    cells += (
                        f"<td style='text-align:center; font-size:8pt; padding:3px;'>"
                        f"<strong>{asp['abbr']}</strong><br/>{asp['orb']:.2f}°</td>"
                    )
                else:
                    cells += "<td style='text-align:center; color:#ccc;'>—</td>"
        rows += f"<tr><th style='text-align:left; font-size:9pt;'>{PLANET_ABBR.get(from_p, from_p[:2])}</th>{cells}</tr>"

    return f"""
    <div class="page-break"></div>
    <h2>Planetary Aspects (Western)</h2>
    <p style='font-size:10pt; color:#666;'>Angular relationships between planets using Western (Ptolemaic + minor) aspects.
    Each cell shows the aspect type and orb. CONJ=Conjunction(0°), OPPN=Opposition(180°), TRIN=Trine(120°),
    SQUR=Square(90°), SEXT=Sextile(60°), NONL=Nonile(40°), QUIN=Quintile(72°).</p>
    <table style='font-size:9pt;'>
        <tr>{header}</tr>
        {rows}
    </table>"""


def _yogini_dasha_section(d: dict) -> str:
    """Yogini Dasha — 36-year cycle with 8 yoginis (Astrosage pages 21-22).

    Shows the full Yogini Dasha sequence + sub-periods for each major period.
    """
    yd = d.get("yogini_dasha")
    if not yd:
        return ""

    html = '<div class="page-break"></div><h2>Yogini Dasha</h2>'
    html += f"""<p>The Yogini Dasha is a 36-year cycle based on 8 yoginis. It is particularly useful for
    timing events within 1-2 year windows. Your starting yogini is <strong>{yd['starting_yogini']}</strong>
    with <strong>{yd['balance_years']}</strong> years remaining at birth.</p>"""

    # Summary table of major periods
    summary_rows = ""
    for entry in yd["dashas"]:
        summary_rows += f"<tr><td><strong>{entry['abbr']}</strong> ({entry['yogini']})</td><td>{entry['years']} years</td><td>{entry['start_date']}</td><td>{entry['end_date']}</td></tr>"

    html += f"""
    <h3>Yogini Mahadasha Sequence</h3>
    <table>
        <tr><th>Yogini</th><th>Duration</th><th>Start</th><th>End</th></tr>
        {summary_rows}
    </table>"""

    # Sub-periods for each major period
    for entry in yd["dashas"]:
        ad_rows = ""
        for ad in entry.get("antardashas", []):
            ad_rows += f"<tr><td>{ad['abbr']} ({ad['yogini']})</td><td>{ad['start_date']}</td><td>{ad['end_date']}</td></tr>"

        html += f"""
        <div class="section">
            <h4 style="color:#555; margin: 12px 0 4px;">{entry['abbr']} — {entry['yogini']} ({entry['start_date']} to {entry['end_date']})</h4>
            <table style="font-size: 9pt;">
                <tr><th>Sub-Period</th><th>Start</th><th>End</th></tr>
                {ad_rows}
            </table>
        </div>"""

    return html


def _shodashvarga_table_section(d: dict) -> str:
    """Astrosage-style Shodashvarga Bhav Table — a compact grid showing each
    planet's sign across all divisional charts at a glance.

    Columns = varga charts (D1 through D60); Rows = planets.
    Each cell shows the sign abbreviation.
    """
    charts = d.get("divisional_charts", {})
    if not charts:
        return ""

    varga_order = [
        "D2", "D3", "D4", "D7", "D9", "D10",
        "D12", "D16", "D20", "D24", "D27", "D30",
        "D40", "D45", "D60",
    ]
    present_vargas = [v for v in varga_order if v in charts]

    # Column headers
    header = "<th>Planet</th>" + "".join(
        f"<th style='text-align:center; font-size:8pt; padding:3px;'>{v}</th>"
        for v in present_vargas
    )

    # Include D1 (Rasi) as the first column from planet positions
    planet_names = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]

    rows = ""
    for name in planet_names:
        if name not in d["planets"]:
            continue
        d1_sign = d["planets"][name]["sign"]
        cells = f"<td style='text-align:center; font-size:8pt;'>{SIGN_ABBR[d1_sign]}</td>"
        for v in present_vargas:
            sign = charts.get(v, {}).get(name)
            cell = SIGN_ABBR[sign] if sign is not None else "—"
            cells += f"<td style='text-align:center; font-size:8pt;'>{cell}</td>"
        rows += f"<tr><td style='font-weight:bold; font-size:9pt;'>{PLANET_ABBR.get(name, name[:2])}</td>{cells}</tr>"

    # Lagna row
    d1_lagna = d["lagna"]["sign"]
    lagna_cells = f"<td style='text-align:center; font-size:8pt;'>{SIGN_ABBR[d1_lagna]}</td>"
    for v in present_vargas:
        lagna_sign = charts.get(v, {}).get("Lagna")
        cell = SIGN_ABBR[lagna_sign] if lagna_sign is not None else "—"
        lagna_cells += f"<td style='text-align:center; font-size:8pt;'>{cell}</td>"
    rows = f"<tr style='background:#f3f0ff;'><td style='font-weight:bold; font-size:9pt;'>Asc</td>{lagna_cells}</tr>" + rows

    return f"""
    <div class="page-break"></div>
    <h2>Shodashvarga Table</h2>
    <p style='font-size:10pt; color:#666;'>Each planet's sign across all divisional charts at a glance.
    D1 = Rasi (birth chart); higher vargas refine specific life areas.</p>
    <table style='font-size:8pt;'>
        <tr><th></th><th style='text-align:center;'>D1</th>{header.replace('<th>Planet</th>', '')}</tr>
        {rows}
    </table>
    <p style='font-size:8pt; color:#999;'>{', '.join(f'{k}={v}' for k, v in zip(SIGN_ABBR, SIGN_NAMES))}</p>"""


def _friendship_section(d: dict) -> str:
    """Astrosage-style Friendship Tables — Permanent, Temporary, Compound.

    Renders three 7×7 matrices between the seven traditional planets:

      Permanent (Naisargika): static classical table per BPHS — same for everyone.
      Temporary (Tatkalika)  : derived from each planet's current sign placement.
      Compound (Panchadha)   : combination of the above; the strongest practical
                               friendship measure used in dignity calculations.
    """
    fr = d.get("friendships")
    if not fr:
        return ""

    planets = fr["planets"]

    def _build_table(matrix: dict, caption: str) -> str:
        header = "<th></th>" + "".join(
            f"<th style='text-align:center;'>{PLANET_ABBR.get(p, p[:2])}</th>"
            for p in planets
        )
        rows = ""
        for from_p in planets:
            row_cells = "".join(
                f"<td style='text-align:center; font-size:9pt;'>{matrix[from_p][to_p]}</td>"
                for to_p in planets
            )
            rows += (
                f"<tr><th style='text-align:left;'>{from_p}</th>{row_cells}</tr>"
            )
        return f"""
        <h3>{caption}</h3>
        <table>
            <tr>{header}</tr>
            {rows}
        </table>"""

    return f"""
    <div class="page-break"></div>
    <h2>Friendship Table</h2>
    <p>The classical Vedic friendship matrix between the seven traditional
    planets. Permanent friendship is fixed by classical doctrine; Temporary
    friendship depends on each planet's current sign placement; Compound
    friendship (Panchadha Maitri) combines the two and is used to judge a
    planet's effective dignity in any sign.</p>
    {_build_table(fr['permanent'], 'Permanent Friendship (Naisargika)')}
    {_build_table(fr['temporary'], 'Temporary Friendship (Tatkalika)')}
    {_build_table(fr['compound'], 'Compound Friendship (Panchadha Maitri)')}"""


def _ghatak_section(d: dict) -> str:
    """Astrosage-style Ghatak (Malefics) panel — points to avoid.

    Renders the 10 classical Ghata Chakra fields in Astrosage's display order:
    Day, Karan, Lagna, Month, Nakshatra, Prahar, Rasi, Tithi, Yoga, Planets.
    """
    sign = d["lagna"]["sign_name"]
    ghat = GHATAK.get(sign, {})

    # Astrosage's exact field order and labels (Bad <Field>).
    ordered_fields = [
        ("bad_day",       "Bad Day"),
        ("bad_karana",    "Bad Karan"),
        ("bad_lagna",     "Bad Lagna"),
        ("bad_masa",      "Bad Month"),
        ("bad_nakshatra", "Bad Nakshatra"),
        ("bad_prahara",   "Bad Prahar"),
        ("bad_rashi",     "Bad Rasi"),
        ("bad_tithi",     "Bad Tithi"),
        ("bad_yoga",      "Bad Yoga"),
        ("bad_planets",   "Bad Planets"),
    ]
    rows = "".join(
        f"<tr><td style='font-weight:bold; color:#555; width:45%;'>{label}</td><td>{ghat.get(key, '—')}</td></tr>"
        for key, label in ordered_fields
    )
    return f"""
    <h2>Ghatak (Malefics)</h2>
    <p style='font-size:10pt; color:#666; margin-bottom:8px;'>Points and timings to avoid for important undertakings.</p>
    <table>{rows}</table>"""


def _ascendant_section(d: dict) -> str:
    sign = d["lagna"]["sign_name"]
    data = LAGNA_DATA.get(sign, {})
    return f"""
    <div class="page-break"></div>
    <h2>Your Ascendant: {sign}</h2>
    <h3>Health for {sign} Ascendant</h3>
    <p>{data.get('health', '')}</p>
    <h3>Temperament &amp; Personality</h3>
    <p>{data.get('temperament', '')}</p>"""


def _nakshatra_section(d: dict) -> str:
    nak = d["nakshatra"]
    data = NAKSHATRA_DATA.get(nak["num"], {})
    return f"""
    <h2>Your Nakshatra: {nak['name']}</h2>
    <p><strong>Pada:</strong> {nak['pada']} &nbsp;|&nbsp; <strong>Lord:</strong> {nak['lord']}</p>
    <p>{data.get('prediction', '')}</p>"""


def _character_life(d: dict) -> str:
    sign = d["lagna"]["sign_name"]
    data = LAGNA_DATA.get(sign, {})
    sections = [
        ("Character", "character"),
        ("Career", "career"),
        ("Occupation", "occupation"),
        ("Hobbies", "hobbies"),
        ("Education", "education"),
        ("Love Matters", "love"),
        ("Finance", "finance"),
    ]
    html = '<div class="page-break"></div><h2>Life Predictions</h2>'
    for title, key in sections:
        text = data.get(key, "")
        if text:
            html += f"<h3>{title}</h3><p>{text}</p>"
    return html


def _manglik_section(d: dict) -> str:
    m = d["manglik"]
    if m["is_manglik"]:
        detail = []
        if m["from_lagna"]:
            detail.append(f"Mars is in the {_ordinal(m['mars_house_lagna'])} house from Lagna")
        if m["from_moon"]:
            detail.append(f"Mars is in the {_ordinal(m['mars_house_moon'])} house from Moon")
        detail_str = " and ".join(detail)
        status_html = f"""
        <div class="manglik-yes">
            <strong>Mangal Dosha is present.</strong><br/>
            {detail_str}.<br/>
            Mangal Dosha is considered to create hurdles in married life. It is considered that if a Manglik person marries another Manglik person, the dosha gets cancelled.
        </div>
        <h3>Remedies</h3>
        <div class="remedy">Kumbha Vivah, Vishnu Vivah, and Ashwatha Vivah are popular remedies.</div>
        <div class="remedy">Keep Kesariya Ganapati in your worship room and worship daily.</div>
        <div class="remedy">Worship Lord Hanuman by reciting Hanuman Chalisa daily.</div>
        <div class="remedy">Mahamrityunjaya Paath (recitation of Mahamrityunjaya mantra).</div>
        """
    else:
        status_html = """
        <div class="manglik-no">
            <strong>Mangal Dosha is not present</strong> in your Lagna Chart or Moon Chart. No special remedies are needed.
        </div>
        """
    return f"""
    <div class="page-break"></div>
    <h2>Manglik Dosha (Mangal Dosha)</h2>
    <p>Manglik Dosha is analyzed from the position of Mars (Mangal) relative to Lagna and Moon in the birth chart.</p>
    {status_html}
    <p style="color:#888; font-size:9pt; margin-top:12px;"><em>Note: We strongly recommend consulting an astrologer before performing remedies.</em></p>"""


def _sadesati_section(d: dict) -> str:
    periods = d.get("sadesati", [])
    if not periods:
        return '<div class="page-break"></div><h2>Sade Sati Report</h2><p>No Sade Sati periods found in the calculated range.</p>'

    rows = ""
    for i, p in enumerate(periods, 1):
        rows += f"<tr><td>{i}</td><td>Sade Sati</td><td>{p['phase']}</td><td>{p['rashi']}</td><td>{p['start_date']}</td><td>{p['end_date']}</td></tr>"

    phase_descriptions = ""
    for phase_name, desc in SADESATI_PHASES.items():
        phase_descriptions += f'<div class="phase-card"><h3>Sade Sati: {phase_name} Phase</h3><p>{desc}</p></div>'

    return f"""
    <div class="page-break"></div>
    <h2>Sade Sati Report</h2>
    <p>Rasi (Moon Sign): <strong>{d['planets']['Moon']['sign_name']}</strong></p>
    <table>
        <tr><th>#</th><th>Type</th><th>Phase</th><th>Saturn Rashi</th><th>Start</th><th>End</th></tr>
        {rows}
    </table>
    {phase_descriptions}"""


def _dasha_section(d: dict) -> str:
    dashas = d["dasha"]["dashas"]
    current = d["dasha"]["current_dasha"]

    rows = ""
    for dasha in dashas:
        is_current = dasha["planet"] == current["planet"] and dasha["start_date"] == current["start_date"]
        style = f' style="background: #f3f0ff; font-weight: bold;"' if is_current else ""
        label = " (Current)" if is_current else ""
        rows += f'<tr{style}><td>{dasha["planet"]}{label}</td><td>{dasha["years"]}</td><td>{dasha["start_date"]}</td><td>{dasha["end_date"]}</td></tr>'

    # Current dasha prediction
    pred = DASHA_PREDICTIONS.get(current["planet"], "")

    return f"""
    <div class="page-break"></div>
    <h2>Vimshottari Dasha</h2>
    <p>The Vimshottari Dasha system covers a 120-year cycle of planetary periods based on your birth Nakshatra.</p>
    <table>
        <tr><th>Planet</th><th>Years</th><th>Start Date</th><th>End Date</th></tr>
        {rows}
    </table>
    <h3>Current Period: {current['planet']} Mahadasha</h3>
    <p>{pred}</p>"""


def _mahadasha_phal_section(d: dict) -> str:
    """Astrosage-style Mahadasha Phal — house-specific interpretation per period.

    For each Mahadasha, identifies which house the lord occupies and renders
    the PLANET_IN_HOUSE interpretation text alongside the period dates.
    This is far more specific than the generic DASHA_PREDICTIONS paragraph
    because it factors in the planet's actual house placement.
    """
    dashas = d["dasha"]["dashas"]
    planets = d["planets"]
    current = d["dasha"]["current_dasha"]

    html = '<div class="page-break"></div><h2>Mahadasha Phal (Period Predictions)</h2>'
    html += "<p>Detailed predictions for each Mahadasha period based on the lord's actual house placement in your birth chart. The active period is highlighted.</p>"

    for dasha in dashas:
        planet = dasha["planet"]
        info = planets.get(planet, {})
        sign_name = info.get("sign_name", "—")
        house = info.get("house")

        is_current = (planet == current["planet"] and dasha["start_date"] == current["start_date"])
        highlight = ' style="background: #f3f0ff; border-left: 4px solid ' + BRAND + ';"' if is_current else ""
        current_badge = ' <span style="color: ' + BRAND + '; font-weight: bold;">(Active)</span>' if is_current else ""

        # House-specific interpretation from PLANET_IN_HOUSE
        house_data = PLANET_IN_HOUSE.get(planet, {}).get(house, {}) if house else {}
        benefic = house_data.get("benefic", "")
        malefic = house_data.get("malefic", "")

        interp_html = ""
        if benefic:
            interp_html += f"<p>{benefic}</p>"
        if malefic:
            interp_html += f"<p>{malefic}</p>"
        if not interp_html:
            # Fallback to generic DASHA_PREDICTIONS
            generic = DASHA_PREDICTIONS.get(planet, "")
            if generic:
                interp_html = f"<p>{generic}</p>"

        html += f"""
        <div class="section" {highlight}>
            <h3>{planet} Mahadasha ({dasha['start_date']} — {dasha['end_date']}){current_badge}</h3>
            <p style="color:#555;"><strong>{planet}</strong> is in <strong>{sign_name}</strong> in your
            <strong>{_ordinal(house) if house else '—'}</strong> house.</p>
            {interp_html}
        </div>"""

    return html


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


def _planet_positions(d: dict) -> str:
    html = '<div class="page-break"></div><h2>Planetary Positions &amp; Effects</h2>'
    html += "<p>Each planet's interpretation is personalised to its actual dignity in your chart.</p>"

    for name, info in d["planets"].items():
        house = info["house"]
        house_data = PLANET_IN_HOUSE.get(name, {}).get(house, {})
        if not house_data:
            continue

        dignity = info.get("dignity", "")
        dignity_color = _DIGNITY_COLOR.get(dignity, "#666")
        dignity_badge = (
            f'&nbsp;<span style="background:{dignity_color}; color:white; font-size:8pt;'
            f' padding:2px 8px; border-radius:10px;">{dignity}</span>'
        ) if dignity else ""

        retro_str = " (Retrograde)" if info["retrograde"] else ""
        benefic = house_data.get("benefic", "")
        malefic = house_data.get("malefic", "")
        remedies = house_data.get("remedies", [])

        # Show the interpretation most relevant to the planet's actual condition
        if dignity in _BENEFIC_DIGNITIES:
            interp_html = f"<p>{benefic}</p>"
        elif dignity in _MALEFIC_DIGNITIES:
            interp_html = f"<p>{malefic}</p>"
            if remedies:
                interp_html += '<h4 style="margin: 8px 0 4px;">Recommended Remedies</h4>'
                for r in remedies:
                    interp_html += f'<div class="remedy">{r}</div>'
            remedies = []  # already rendered
        else:
            interp_html = f"<p><strong>If well-placed:</strong> {benefic}</p><p><strong>If ill-placed:</strong> {malefic}</p>"

        remedies_html = ""
        if remedies:
            remedies_html = '<h4 style="margin: 8px 0 4px;">Remedies</h4>'
            for r in remedies:
                remedies_html += f'<div class="remedy">{r}</div>'

        html += f"""
        <div class="section">
            <h3>{name} in {info['sign_name']}{dignity_badge} — {_ordinal(house)} House{retro_str}</h3>
            {interp_html}
            {remedies_html}
        </div>"""

    return html


# ── North Indian Chart SVG ────────────────────────────────────────────────────

def _chart_svg(house_signs: dict[int, int], house_planets: dict[int, list[str]], title: str = "") -> str:
    """Render a North Indian style Kundli chart as inline SVG.
    house_signs: {1: sign_num, 2: sign_num, ...} (0-indexed sign numbers)
    house_planets: {1: ["Su", "Mo"], 2: ["Ma"], ...} (planet abbreviations per house)
    """
    W = 300
    # SVG lines: outer square + diamond (midpoints) + two diagonals
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {W}" width="280" height="280"
        style="display: block; margin: 10px auto;">
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
        # Rashi number (1-12) — bold, in brand color
        rashi_num = sign + 1  # 0-indexed sign → 1-indexed Rashi number
        svg += f'<text x="{x}" y="{y}" text-anchor="middle" font-size="11" font-weight="bold" fill="{BRAND}">{rashi_num}</text>'
        # Planet abbreviations (smaller, below number)
        if planets:
            planet_str = " ".join(planets)
            # Split into multiple lines if too many planets
            if len(planets) <= 3:
                svg += f'<text x="{x}" y="{y + 14}" text-anchor="middle" font-size="9" fill="#333">{planet_str}</text>'
            else:
                line1 = " ".join(planets[:3])
                line2 = " ".join(planets[3:])
                svg += f'<text x="{x}" y="{y + 14}" text-anchor="middle" font-size="9" fill="#333">{line1}</text>'
                svg += f'<text x="{x}" y="{y + 24}" text-anchor="middle" font-size="9" fill="#333">{line2}</text>'

    if title:
        svg += f'<text x="150" y="155" text-anchor="middle" font-size="10" fill="#666">{title}</text>'

    svg += "</svg>"
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


# ── New PDF sections ──────────────────────────────────────────────────────────

def _birth_chart_page(d: dict) -> str:
    """D1 Rasi/Lagna chart with visual diagram."""
    house_signs, house_planets = _build_d1_chart_data(d)
    chart_svg = _chart_svg(house_signs, house_planets, "D1")
    return f"""
    <div class="page-break"></div>
    <h2>Lagna Chart (D1 — Rasi Chart)</h2>
    <p>The Lagna chart shows the positions of all nine planets in the twelve houses at the time of your birth.
    The ascendant sign <strong>{d['lagna']['sign_name']}</strong> is placed in the first house (top center).
    Signs progress clockwise through the twelve houses.</p>
    {chart_svg}
    <p style="text-align: center; font-size: 9pt; color: #888;">
    1=Aries(Mesh), 2=Taurus(Vrushabh), 3=Gemini(Mithun), 4=Cancer(Karka), 5=Leo(Simha), 6=Virgo(Kanya),
    7=Libra(Tula), 8=Scorpio(Vruschik), 9=Sagittarius(Dhanu), 10=Capricorn(Makar), 11=Aquarius(Kumbh), 12=Pisces(Meen)<br/>
    Su=Sun, Mo=Moon, Ma=Mars, Me=Mercury, Ju=Jupiter, Ve=Venus, Sa=Saturn, Ra=Rahu, Ke=Ketu,
    Ur=Uranus, Ne=Neptune, Pl=Pluto &nbsp;|&nbsp; *=Retrograde
    </p>
    <h3>Moon Chart (Chandra Kundli)</h3>
    <p>The Moon chart places the Moon's sign in the first house, showing planetary positions relative to the Moon.</p>
    {_moon_chart_svg(d)}
    """


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


def _bhava_analysis(d: dict) -> str:
    """House-by-house Bhava analysis section."""
    lagna_sign = d["lagna"]["sign"]
    html = '<div class="page-break"></div><h2>Bhava (House) Analysis</h2>'
    html += "<p>Each house (Bhava) in the birth chart governs specific areas of life. Below is the analysis of each house based on the sign placed in it and any planets occupying it.</p>"

    # Collect which planets are in each house
    planets_in_house: dict[int, list[str]] = {h: [] for h in range(1, 13)}
    for name, info in d["planets"].items():
        planets_in_house[info["house"]].append(name)

    for house_num in range(1, 13):
        bhava = BHAVA_DATA.get(house_num, {})
        if not bhava:
            continue
        house_sign = (lagna_sign + house_num - 1) % 12
        sign_name = SIGN_NAMES[house_sign]
        house_lord = SIGN_LORDS[house_sign]
        planets = planets_in_house[house_num]
        planet_str = ", ".join(planets) if planets else "No planets"

        # House lord placement
        lord_info = d["planets"].get(house_lord, {})
        lord_house = lord_info.get("house", "?")
        lord_sign = lord_info.get("sign_name", "?")
        lord_dignity = lord_info.get("dignity", "")
        lord_dignity_str = f", <strong>{lord_dignity}</strong>" if lord_dignity else ""
        lord_detail = (
            f"<strong>{house_lord}</strong> is placed in {lord_sign} "
            f"({_ordinal(lord_house)} House{lord_dignity_str})"
        )

        html += f"""
        <div class="section">
            <h3>{bhava['name']}</h3>
            <p><strong>Sign:</strong> {sign_name} &nbsp;|&nbsp;
               <strong>Lord:</strong> {lord_detail} &nbsp;|&nbsp;
               <strong>Occupants:</strong> {planet_str}</p>
            <p><strong>Significations:</strong> {bhava['signification']}</p>
            <p>{bhava['description']}</p>
        </div>"""

    return html


def _divisional_charts_section(d: dict) -> str:
    """Render all divisional chart pages with SVG diagrams."""
    charts = d.get("divisional_charts", {})
    if not charts:
        return ""

    html = '<div class="page-break"></div><h2>Divisional Charts</h2>'
    for chart_type in (
        "D9", "D10", "D2", "D3", "D4", "D6", "D7", "D8",
        "D11", "D12", "D16", "D20", "D24", "D27", "D30",
        "D40", "D45", "D60",
    ):
        if chart_type not in charts:
            continue
        title, description = CHART_DESCRIPTIONS.get(chart_type, (chart_type, ""))
        house_signs, house_planets = _build_divisional_chart_data(d, chart_type)
        chart_svg = _chart_svg(house_signs, house_planets, chart_type)

        # Build a table of planet positions — classical 9 only (no outer planets)
        # to keep the table compact and avoid the Pluto-orphan page-break problem.
        chart_data = charts[chart_type]
        planet_rows = ""
        for name in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"):
            if name in chart_data:
                sign_num = chart_data[name]
                planet_rows += f"<tr><td><strong>{name}</strong></td><td>{SIGN_NAMES[sign_num]}</td></tr>"

        html += f"""
        <div class="chart-block">
            <h3>{title} ({chart_type})</h3>
            <p style="font-size:10pt; color:#666;">{description}</p>
            {chart_svg}
            <table style="font-size:9pt;">
                <tr><th>Planet</th><th>Sign</th></tr>
                {planet_rows}
            </table>
        </div>"""

    return html


def _antardasha_section(d: dict) -> str:
    """Render Antardasha (sub-period) tables for each Mahadasha."""
    antardasha_list = d.get("antardasha", [])
    if not antardasha_list:
        return ""

    html = '<div class="page-break"></div><h2>Antardasha (Sub-Periods)</h2>'
    html += "<p>Each Mahadasha is divided into nine Antardashas (sub-periods). The Antardasha planet modifies the results of the Mahadasha, creating specific effects during each sub-period. Below is the complete breakdown of all sub-periods within each Mahadasha.</p>"

    current_dasha = d["dasha"]["current_dasha"]

    for md in antardasha_list:
        is_current_md = (md["mahadasha"] == current_dasha["planet"] and md["start_date"] == current_dasha["start_date"])
        md_label = " (Current Mahadasha)" if is_current_md else ""
        highlight_style = f' style="background: #f3f0ff;"' if is_current_md else ""

        rows = ""
        for ad in md["antardashas"]:
            rows += f"<tr><td>{ad['planet']}</td><td>{ad['years']}</td><td>{ad['start_date']}</td><td>{ad['end_date']}</td></tr>"

        html += f"""
        <div class="section">
            <h3{highlight_style}>{md['mahadasha']} Mahadasha — {md['mahadasha_years']} years{md_label}</h3>
            <p><strong>Period:</strong> {md['start_date']} to {md['end_date']}</p>
            <table>
                <tr><th>Antardasha Planet</th><th>Years</th><th>Start Date</th><th>End Date</th></tr>
                {rows}
            </table>
        </div>"""

        # Add prediction text for current mahadasha
        if is_current_md:
            pred = DASHA_PREDICTIONS.get(md["mahadasha"], "")
            if pred:
                html += f'<div class="phase-card"><h3>Current {md["mahadasha"]} Mahadasha Interpretation</h3><p>{pred}</p></div>'

    return html


def _pratyantar_section(d: dict) -> str:
    """Render Pratyantar Dasha (3rd-level sub-sub-periods) tables.

    Astrosage shows Pratyantar for every Mahadasha/Antardasha combination
    (pages 45-48). We show the same — grouped by MD → AD with a compact
    table of 9 Pratyantar entries per AD.
    """
    pratyantar_list = d.get("pratyantar", [])
    if not pratyantar_list:
        return ""

    current_md = d.get("dasha", {}).get("current_dasha", {}).get("planet", "")
    html = '<div class="page-break"></div><h2>Pratyantar Dasha (Sub-Sub-Periods)</h2>'
    html += f"<p>Each Antardasha is further divided into nine Pratyantars. These sub-sub-periods refine the timing of events. Showing Pratyantar breakdown for the <strong>current {current_md} Mahadasha</strong>.</p>"

    current_md = None
    for entry in pratyantar_list:
        md = entry["mahadasha"]
        ad = entry["antardasha"]

        # MD header (only print once per Mahadasha)
        if md != current_md:
            if current_md is not None:
                html += '</div>'  # close previous MD wrapper
            html += f'<div class="page-break"></div><h3>{md} Mahadasha</h3>'
            current_md = md

        # AD sub-header + Pratyantar table
        rows = ""
        for pd in entry["pratyantars"]:
            rows += f"<tr><td>{pd['planet']}</td><td>{pd['start_date']}</td><td>{pd['end_date']}</td><td>{pd['days']}d</td></tr>"

        html += f"""
        <div class="section">
            <h4 style="color:#555; margin: 12px 0 4px;">{md} — {ad} Antardasha ({entry['start_date']} to {entry['end_date']})</h4>
            <table style="font-size: 9pt;">
                <tr><th>Pratyantar</th><th>Start</th><th>End</th><th>Duration</th></tr>
                {rows}
            </table>
        </div>"""

    if current_md is not None:
        html += '</div>'

    return html


def _shadbala_table(shadbala: dict, planet_list: list, label_note: str) -> str:
    """Render a Shadbala strength table for a given list of planets."""
    present = [p for p in planet_list if p in shadbala]
    if not present:
        return ""

    def row(label: str, key: str) -> str:
        cells = "".join(f"<td>{shadbala[p][key]}</td>" for p in present)
        return f"<tr><td style='font-weight:bold;color:#555;'>{label}</td>{cells}</tr>"

    headers = "".join(f"<th>{p[:3].upper()}</th>" for p in present)
    rank_cells = "".join(
        f"<td style='font-weight:bold;color:{BRAND};'>{shadbala[p].get('rank', '-')}</td>"
        for p in present
    )
    status_cells = "".join(
        f"<td style='color:{'#16a34a' if shadbala[p]['ratio'] >= 1 else '#dc2626'};font-weight:bold;'>"
        f"{'Strong' if shadbala[p]['ratio'] >= 1 else 'Weak'}</td>"
        for p in present
    )

    return f"""
    <table style="font-size:9pt;">
        <tr><th>Strength Component</th>{headers}</tr>
        {row("Ochcha Bala", "ochcha_bala")}
        {row("Saptavargaja Bala", "saptavargaja_bala")}
        {row("Ojayugmarasyamsa Bala", "ojayugma_bala")}
        {row("Kendra Bala", "kendra_bala")}
        {row("Drekkana Bala", "drekkana_bala")}
        <tr style="background:#f3f0ff;font-weight:bold;">
            <td>Total Sthana Bala</td>
            {"".join(f"<td>{shadbala[p]['sthan_bala']}</td>" for p in present)}
        </tr>
        <tr style="background:#f3f0ff;font-weight:bold;">
            <td>Total Dig Bala</td>
            {"".join(f"<td>{shadbala[p]['dig_bala']}</td>" for p in present)}
        </tr>
        {row("Nathonnatha Bala", "nathonnatha_bala")}
        {row("Paksha Bala", "paksha_bala")}
        {row("Thribhaga Bala", "thribhaga_bala")}
        {row("Abda Bala", "abda_bala")}
        {row("Masa Bala", "masa_bala")}
        {row("Vara Bala", "vara_bala")}
        {row("Hora Bala", "hora_bala")}
        {row("Ayana Bala", "ayana_bala")}
        {row("Yuddha Bala", "yuddha_bala")}
        <tr style="background:#f3f0ff;font-weight:bold;">
            <td>Total Kala Bala</td>
            {"".join(f"<td>{shadbala[p]['kala_bala']}</td>" for p in present)}
        </tr>
        {row("Chesta Bala", "chesta_bala")}
        {row("Naisargeka Bala", "naisargeka_bala")}
        {row("Drik Bala", "drik_bala")}
        <tr style="background:{BRAND};color:white;font-weight:bold;">
            <td>Total Shadbala (Virupas)</td>
            {"".join(f"<td>{shadbala[p]['total_shadbala']}</td>" for p in present)}
        </tr>
        <tr style="font-weight:bold;">
            <td>Shadbala in Rupas</td>
            {"".join(f"<td>{shadbala[p]['shadbala_rupas']}</td>" for p in present)}
        </tr>
        <tr>
            <td style="font-weight:bold;color:#555;">Minimum Requirement</td>
            {"".join(f"<td>{shadbala[p]['min_requirement']}</td>" for p in present)}
        </tr>
        <tr style="font-weight:bold;">
            <td>Ratio</td>
            {"".join(f"<td style='color:{'#16a34a' if shadbala[p]['ratio'] >= 1 else '#dc2626'};'>{shadbala[p]['ratio']}</td>" for p in present)}
        </tr>
        <tr>
            <td style="font-weight:bold;color:#555;">Relative Rank</td>
            {rank_cells}
        </tr>
        <tr>
            <td style="font-weight:bold;color:#555;">Strength Status</td>
            {status_cells}
        </tr>
    </table>
    <p style="font-size:9pt;color:#888;margin-top:4px;"><em>{label_note}</em></p>"""


def _shadbala_section(d: dict) -> str:
    """Shadbala and Bhavabala – Planetary Strength Calculations (classical + extended)."""
    shadbala = d.get("shadbala", {})
    if not shadbala:
        return ""

    classical = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    extended  = ["Rahu", "Ketu", "Uranus", "Neptune", "Pluto"]

    classical_table = _shadbala_table(
        shadbala, classical,
        "Classical Shadbala — Virupas (1 Rupa = 60 Virupas). Uses Lahiri Ayanamsa, "
        "Whole Sign houses. Saptavargaja weighted across D1, D9, D3."
    )
    extended_table = _shadbala_table(
        shadbala, extended,
        "Extended Strength — adapted Shadbala framework applied to Rahu, Ketu, and outer planets. "
        "Exaltations and dignities follow contemporary Jyotish research (not classical texts). "
        "Temporal lord components (Thribhaga, Hora, Vara, Abda, Masa) are not applicable and shown as 0."
    )

    return f"""
    <div class="page-break"></div>
    <h2>Shadbala &amp; Bhavabala – Strength Calculations</h2>
    <p>Shadbala (six-fold strength) measures planetary strength across positional, directional,
    temporal, natural, and aspectual dimensions. Ratio &ge; 1.0 indicates sufficient strength.</p>

    <h3>Classical Shadbala — Seven Traditional Planets</h3>
    {classical_table}

    <h3 style="margin-top:24px;">Extended Strength Analysis — Rahu, Ketu &amp; Outer Planets</h3>
    <p style="font-size:10pt;color:#555;">This section applies an adapted Shadbala framework to the
    lunar nodes and outer planets — a modern extension unique to this report. It provides comparative
    strength analysis across all planetary bodies in your chart.</p>
    {extended_table}"""


def _yogas_section(d: dict) -> str:
    """Render detected Vedic yogas."""
    yogas = d.get("yogas", [])
    if not yogas:
        return ""

    _TYPE_LABEL = {
        "mahapurusha": "Pancha Mahapurusha",
        "raj":         "Raja Yoga",
        "dhan":        "Dhan Yoga",
        "chandra":     "Chandra Yoga",
        "challenging": "Challenging Yoga",
    }
    _TYPE_COLOR = {
        "mahapurusha": "#7c3aed",
        "raj":         "#1d4ed8",
        "dhan":        "#15803d",
        "chandra":     "#0369a1",
        "challenging": "#b45309",
    }

    cards = ""
    for yoga in yogas:
        label = _TYPE_LABEL.get(yoga.get("type", ""), yoga.get("type", "").replace("_", " ").title())
        color = _TYPE_COLOR.get(yoga.get("type", ""), "#555")
        planets_str = ", ".join(yoga.get("planets", []))
        house_str = f" &nbsp;|&nbsp; House {yoga['house']}" if yoga.get("house") else ""
        cards += f"""
        <div style="border-left: 4px solid {color}; background: #faf9ff; padding: 10px 14px; margin: 8px 0; page-break-inside: avoid;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                <strong style="color:{color}; font-size:11pt;">{yoga['name']}</strong>
                <span style="background:{color}; color:white; font-size:8pt; padding:2px 8px; border-radius:10px;">{label}</span>
            </div>
            <p style="margin:4px 0 2px;">{yoga['description']}</p>
            <p style="font-size:9pt; color:#888; margin:0;">Planets: <em>{planets_str}</em>{house_str}</p>
        </div>"""

    return f"""
    <div class="page-break"></div>
    <h2>Yogas — Planetary Combinations</h2>
    <p>Yogas are specific planetary combinations in the birth chart that produce defined results.
    Your chart contains <strong>{len(yogas)}</strong> active yoga{"s" if len(yogas) != 1 else ""}.</p>
    {cards}
    <p style="font-size:9pt; color:#888; margin-top:10px;"><em>Yoga strength depends on the dignity and overall chart strength of the participating planets. Consult an astrologer for detailed timing of yoga results through Dasha periods.</em></p>"""


def _doshas_section(d: dict) -> str:
    """Render detected Vedic doshas (excluding Manglik and Sade Sati — those have their own sections)."""
    doshas = d.get("doshas", [])
    if not doshas:
        return f"""
    <div class="page-break"></div>
    <h2>Doshas — Planetary Afflictions</h2>
    <p style="background:#f0fdf4; border:1px solid #4ade80; padding:12px; border-radius:6px;">
        <strong>No major doshas detected</strong> in your birth chart. Your chart is free from the primary classical afflictions.
    </p>"""

    _SEVERITY_COLOR = {"full": "#dc2626", "partial": "#b45309", "reverse": "#15803d"}
    _TYPE_ICON = {
        "kaal_sarp":   "Kaal Sarp",
        "pitra":       "Pitra Dosha",
        "guru_chandal":"Guru Chandal",
        "grahan":      "Grahan Dosha",
        "angarak":     "Angarak Dosha",
        "vish":        "Vish Yoga",
        "shakat":      "Shakat Yoga",
    }

    cards = ""
    for dosha in doshas:
        severity = dosha.get("severity", "")
        sev_label = severity.title() if severity else ""
        sev_color = _SEVERITY_COLOR.get(severity, "#b45309")
        badge = f'<span style="background:{sev_color}; color:white; font-size:8pt; padding:2px 8px; border-radius:10px;">{sev_label}</span>' if sev_label else ""
        planets_str = ", ".join(dosha.get("planets", []))
        house_str = f" &nbsp;|&nbsp; House {dosha['house']}" if dosha.get("house") else ""
        cards += f"""
        <div style="border-left: 4px solid #dc2626; background: #fff7f7; padding: 10px 14px; margin: 8px 0; page-break-inside: avoid;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                <strong style="color:#dc2626; font-size:11pt;">{dosha['name']}</strong>
                {badge}
            </div>
            <p style="margin:4px 0 2px;">{dosha['description']}</p>
            <p style="font-size:9pt; color:#888; margin:0;">Planets: <em>{planets_str}</em>{house_str}</p>
        </div>"""

    return f"""
    <div class="page-break"></div>
    <h2>Doshas — Planetary Afflictions</h2>
    <p>Doshas are challenging planetary configurations. A dosha is not a life sentence — its severity
    depends on the overall chart strength, cancellation conditions, and free will. Remedies are available.</p>
    {cards}
    <p style="font-size:9pt; color:#888; margin-top:10px;"><em>Note: Mangal Dosha and Sade Sati are covered in their dedicated sections below.
    Always consult a qualified astrologer before undertaking remedial measures.</em></p>"""


def _gochar_section(d: dict) -> str:
    """Render current planetary transits (Gochar) over the natal chart."""
    gochar = d.get("gochar", {})
    if not gochar:
        return ""

    transits = gochar.get("transits", {})
    special_periods = gochar.get("special_periods", [])
    dasha_note = gochar.get("dasha_gochar_note", "")
    computed_date = gochar.get("computed_for_date", "")

    # Transit table
    transit_rows = ""
    planet_order = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
    for planet in planet_order:
        if planet not in transits:
            continue
        t = transits[planet]
        fav = t.get("moon_transit_favorable", False)
        fav_color = "#15803d" if fav else "#dc2626"
        fav_label = t.get("moon_transit_label", "")
        special = t.get("special") or ""
        transit_rows += f"""<tr>
            <td><strong>{planet}</strong></td>
            <td>{t.get('current_sign_name', '')} ({t.get('current_degree', 0):.1f}°)</td>
            <td>{t.get('house_from_moon', '')}</td>
            <td style="color:{fav_color}; font-weight:bold;">{fav_label}</td>
            <td>{t.get('lagna_transit_label', '')}</td>
            <td style="font-size:9pt; color:#666;">{special}</td>
        </tr>"""

    # Special periods
    special_html = ""
    if special_periods:
        special_html = "<h3>Active Special Transit Periods</h3>"
        for sp in special_periods:
            sp_color = "#7c3aed" if "favorable" in sp.get("name", "").lower() or "guru" in sp.get("name", "").lower() else "#b45309"
            if "Sade Sati" in sp.get("name", "") or "Ashtama" in sp.get("name", ""):
                sp_color = "#dc2626"
            special_html += f"""
            <div style="border-left:4px solid {sp_color}; background:#faf9ff; padding:10px 14px; margin:6px 0;">
                <strong style="color:{sp_color};">{sp['name']}</strong> — {sp.get('planet', '')} in house {sp.get('house_from_moon', '')} from natal Moon
            </div>"""

    # Dasha-Gochar note
    note_html = ""
    if dasha_note:
        note_html = f"""
        <div style="background:#f3f0ff; border:1px solid {BRAND}; border-radius:6px; padding:14px; margin:14px 0;">
            <strong style="color:{BRAND};">Dasha-Gochar Synthesis</strong>
            <p style="margin:6px 0 0;">{dasha_note}</p>
        </div>"""

    return f"""
    <div class="page-break"></div>
    <h2>Gochar — Current Planetary Transits</h2>
    <p>Gochar shows where the planets are positioned <em>today</em> relative to your natal Moon sign
    (primary reference) and Lagna (secondary). This reveals which life areas are currently activated.
    <strong>Computed for: {computed_date}</strong></p>

    <table>
        <tr>
            <th>Planet</th>
            <th>Current Position</th>
            <th>House from Moon</th>
            <th>Moon Transit</th>
            <th>Lagna Transit</th>
            <th>Special</th>
        </tr>
        {transit_rows}
    </table>

    {special_html}
    {note_html}
    <p style="font-size:9pt; color:#888;"><em>Transit results are measured primarily from the natal Moon sign (Chandra Lagna) per BPHS tradition.
    For the most accurate timing of events, combine with active Dasha-Antardasha periods.</em></p>"""


def _numerology_section(d: dict) -> str:
    """Render Chaldean numerology section."""
    num = d.get("numerology", {})
    if not num:
        return ""

    def _num_card(key: str, show_lucky: bool = True) -> str:
        entry = num.get(key)
        if not entry:
            return ""
        value = entry.get("value", "")
        label = entry.get("label", "")
        planet = entry.get("planet", "")
        meaning = entry.get("meaning", "")
        lucky_day = entry.get("lucky_day", "")
        lucky_color = entry.get("lucky_color", "")
        lucky_gem = entry.get("lucky_gemstone", "")
        year = entry.get("year", "")

        lucky_html = ""
        if show_lucky and lucky_day:
            lucky_html = f"""
            <div style="display:flex; gap:20px; flex-wrap:wrap; font-size:9pt; color:#555; margin-top:6px;">
                <span><strong>Lucky Day:</strong> {lucky_day}</span>
                <span><strong>Lucky Color:</strong> {lucky_color}</span>
                <span><strong>Gemstone:</strong> {lucky_gem}</span>
            </div>"""

        year_html = f" <span style='color:#888;font-size:9pt;'>({year})</span>" if year else ""

        return f"""
        <div style="border-left:4px solid {BRAND}; background:#faf9ff; padding:10px 14px; margin:8px 0; page-break-inside:avoid;">
            <div style="display:flex; align-items:baseline; gap:12px;">
                <span style="font-size:22pt; font-weight:bold; color:{BRAND};">{value}</span>
                <div>
                    <strong style="font-size:11pt;">{label}{year_html}</strong><br/>
                    <span style="font-size:9pt; color:#666;">Ruling Planet: {planet}</span>
                </div>
            </div>
            <p style="margin:8px 0 4px;">{meaning}</p>
            {lucky_html}
        </div>"""

    core_cards = (
        _num_card("moolank") +
        _num_card("bhagyank") +
        _num_card("personal_year")
    )

    name_cards = ""
    if num.get("namank"):
        name_cards = f"""
        <h3>Name-Based Numbers</h3>
        {_num_card("namank")}
        {_num_card("soul_number", show_lucky=False)}
        {_num_card("personality_number", show_lucky=False)}"""

    return f"""
    <div class="page-break"></div>
    <h2>Numerology — Chaldean System</h2>
    <p>Chaldean numerology assigns vibrational values to letters and numbers based on ancient Babylonian tradition,
    aligned with Vedic planetary rulerships. Numbers reveal the energetic blueprint of the personality and destiny.</p>

    <h3>Core Numbers</h3>
    {core_cards}
    {name_cards}
    <p style="font-size:9pt; color:#888; margin-top:10px;"><em>Master numbers 11, 22, and 33 are preserved without further reduction as they carry heightened spiritual significance.</em></p>"""


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


def _remedies_section(d: dict) -> str:
    """Gemstone recommendations and personalised remedies section."""
    lagna_sign = d["lagna"]["sign"]
    lagna_lord = d["lagna"]["sign_lord"]
    moon_lord = d["planets"]["Moon"]["sign_lord"]

    # Trinal lords: 1st, 5th (lagna+4), 9th (lagna+8)
    lord_5 = SIGN_LORDS[(lagna_sign + 4) % 12]
    lord_9 = SIGN_LORDS[(lagna_sign + 8) % 12]

    # Build primary gem recommendations (unique planets only)
    seen: set[str] = set()
    gem_rows = ""
    for planet, reason in [
        (lagna_lord, "Lagna Lord — primary, always beneficial"),
        (lord_5,     "5th House Lord — strengthens intelligence &amp; creativity"),
        (lord_9,     "9th House Lord — activates fortune &amp; dharma"),
    ]:
        if planet in _GEMSTONE and planet not in seen:
            gem = _GEMSTONE[planet]
            day = _LUCKY_DAY.get(planet, "")
            gem_rows += f"""
            <tr>
                <td><strong>{planet}</strong></td>
                <td>{gem}</td>
                <td style="color:#555;">{reason}</td>
                <td style="color:#555;">{day}</td>
            </tr>"""
            seen.add(planet)

    # Caution gems — 6th, 8th, 12th lords (Dusthana lords)
    lords_caution = {
        SIGN_LORDS[(lagna_sign + 5) % 12],   # 6th lord
        SIGN_LORDS[(lagna_sign + 7) % 12],   # 8th lord
        SIGN_LORDS[(lagna_sign + 11) % 12],  # 12th lord
    } - seen  # don't warn if already recommended
    caution_text = ", ".join(
        f"{p} ({_GEMSTONE.get(p, '')})" for p in lords_caution if p in _GEMSTONE
    )

    # Weak planets from Shadbala (ratio < 1.0)
    shadbala = d.get("shadbala", {})
    classical = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    weak = sorted(
        [(p, shadbala[p]["ratio"]) for p in classical if p in shadbala and shadbala[p]["ratio"] < 1.0],
        key=lambda x: x[1],
    )

    weak_rows = ""
    for planet, ratio in weak:
        weak_rows += f"""
        <div style="border-left:4px solid #b45309; background:#fffbeb; padding:10px 14px; margin:8px 0;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                <strong style="color:#b45309;">{planet} — Shadbala Ratio {ratio:.2f}</strong>
                <span style="font-size:9pt; color:#666;">Gemstone: {_GEMSTONE.get(planet, 'N/A')}</span>
            </div>
            <p style="margin:4px 0 2px; font-size:10pt;"><strong>Mantra:</strong> {_MANTRA.get(planet, '')}</p>
            <p style="margin:2px 0; font-size:10pt;"><strong>Worship:</strong> {_DEITY.get(planet, '')}</p>
            <p style="margin:2px 0; font-size:10pt;"><strong>Donate:</strong> {_DONATION.get(planet, '')}</p>
        </div>"""

    # Dasha lord remedy
    dasha_lord = d["dasha"]["current_dasha"]["planet"]
    dasha_remedy = ""
    if dasha_lord in _MANTRA:
        dasha_remedy = f"""
        <h3>Current Mahadasha — {dasha_lord}</h3>
        <div style="border-left:4px solid {BRAND}; background:#faf9ff; padding:10px 14px; margin:8px 0;">
            <p style="margin:4px 0;"><strong>Gemstone:</strong> {_GEMSTONE.get(dasha_lord, 'N/A')}</p>
            <p style="margin:4px 0;"><strong>Mantra:</strong> {_MANTRA.get(dasha_lord, '')}</p>
            <p style="margin:4px 0;"><strong>Worship:</strong> {_DEITY.get(dasha_lord, '')}</p>
            <p style="margin:4px 0;"><strong>Donate:</strong> {_DONATION.get(dasha_lord, '')}</p>
        </div>"""

    caution_html = ""
    if caution_text:
        caution_html = f"""
        <p style="background:#fef9ec; border:1px solid #fbbf24; padding:10px; border-radius:6px; font-size:10pt;">
            <strong>Gems to wear with caution (Dusthana lords):</strong> {caution_text}.
            Consult a qualified astrologer before wearing these gemstones.
        </p>"""

    weak_section = ""
    if weak:
        weak_section = f"""
        <h3>Planets Needing Strengthening (Shadbala &lt; 1.0)</h3>
        <p>The following planets are below the required Shadbala threshold in your chart. Strengthening them
        through mantra, worship, and charity can improve their results in your life.</p>
        {weak_rows}"""

    return f"""
    <div class="page-break"></div>
    <h2>Gemstone &amp; Remedy Recommendations</h2>
    <p>Vedic remedies work by strengthening beneficial planets and mitigating the effects of afflicted or weak ones.
    <strong>Always wear gemstones only after consulting a qualified Jyotishi</strong> — an incorrect gemstone can cause harm.</p>

    <h3>Recommended Gemstones</h3>
    <p>Based on your Lagna and trinal house lords, the following gemstones are considered universally beneficial for your chart:</p>
    <table>
        <tr><th>Planet</th><th>Gemstone</th><th>Reason</th><th>Lucky Day</th></tr>
        {gem_rows}
    </table>
    {caution_html}
    {weak_section}
    {dasha_remedy}
    <p style="font-size:9pt; color:#888; margin-top:12px;"><em>Remedies in Vedic astrology are tools for self-improvement, not guarantees of outcome.
    The best remedy is right action (Karma), charity (Dana), and spiritual practice (Sadhana).</em></p>"""


def _footer() -> str:
    return f"""
    <div class="footer">
        <p>This report has been generated based on Vedic astrology calculations using Lahiri Ayanamsa.</p>
        <p>For personalised guidance, book a consultation at <strong style="color:{BRAND};">vedicjivan.nandishdave.world</strong></p>
        <p>&copy; {datetime.now().year} VedicJivan. All rights reserved.</p>
    </div>"""


def _ordinal(n: int) -> str:
    """1 → '1st', 2 → '2nd', etc."""
    if 11 <= (n % 100) <= 13:
        return f"{n}th"
    return f"{n}{['th','st','nd','rd','th','th','th','th','th','th'][n % 10]}"
