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
    "D3": ("Drekkana Chart", "The Drekkana chart divides each sign into three equal parts and is used for analyzing siblings, courage, and communication. It also has significance in predicting the nature of one's death in traditional texts."),
    "D9": ("Navamsa Chart", "The Navamsa is the most important divisional chart after the Rasi chart. It divides each sign into nine parts and is primarily used for marriage analysis, spouse characteristics, and the overall strength of planets. A strong Navamsa can elevate weak Rasi placements."),
    "D10": ("Dasamsa Chart", "The Dasamsa chart divides each sign into ten parts and is specifically used for career and professional analysis. It reveals the nature of one's profession, career achievements, and public reputation."),
    "D12": ("Dwadasamsa Chart", "The Dwadasamsa divides each sign into twelve parts and is used for analyzing parents, lineage, and ancestral karma. It provides insights into the relationship with parents and inherited traits."),
    "D60": ("Shastiamsa Chart", "The Shastiamsa is the most subtle divisional chart, dividing each sign into sixty parts. It is used for confirming the results indicated by other charts and for fine-tuning predictions. Classical texts consider it the final arbiter of planetary strength."),
}


def generate_pdf(chart_data: dict) -> bytes:
    """Generate a Kundli report PDF from chart_data dict. Returns raw PDF bytes."""
    html = _build_html(chart_data)
    from weasyprint import HTML
    return HTML(string=html).write_pdf()


# ── HTML builder ─────────────────────────────────────────────────────────────

def _build_html(d: dict) -> str:
    """Build the full HTML document for the Kundli report."""
    sections = [
        _css(),
        _cover(d),
        _birth_chart_page(d),
        _basic_details(d),
        _favourable_ghatak(d),
        _ascendant_section(d),
        _nakshatra_section(d),
        _character_life(d),
        _bhava_analysis(d),
        _divisional_charts_section(d),
        _shadbala_section(d),
        _manglik_section(d),
        _sadesati_section(d),
        _dasha_section(d),
        _antardasha_section(d),
        _planet_positions(d),
        _footer(),
    ]
    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Kundli Report - {d['name']}</title></head>
<body>{''.join(sections)}</body>
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
    lagna = d["lagna"]
    nak = d["nakshatra"]
    pan = d["panchanga"]
    dasha = d["dasha"]["dashas"][0]
    moon = d["planets"]["Moon"]

    rows = [
        ("Name", d["name"]),
        ("Gender", d["gender"].title()),
        ("Date of Birth", d["dob"]),
        ("Time of Birth", d["tob"]),
        ("Place of Birth", d["place_name"]),
        ("Latitude / Longitude", f"{abs(d['lat']):.2f}{'N' if d['lat'] >= 0 else 'S'} / {abs(d['lon']):.2f}{'E' if d['lon'] >= 0 else 'W'}"),
        ("", ""),
        ("Lagna (Ascendant)", f"{lagna['sign_name']}"),
        ("Lagna Lord", lagna["sign_lord"]),
        ("Rasi (Moon Sign)", moon["sign_name"]),
        ("Rasi Lord", moon["sign_lord"]),
        ("Nakshatra - Pada", f"{nak['name']} - {nak['pada']}"),
        ("Nakshatra Lord", nak["lord"]),
        ("Tithi", pan["tithi_name"]),
        ("Paksha", pan["paksha"]),
        ("Yoga", pan["yoga_name"]),
        ("Karan", pan["karan_name"]),
        ("Sunrise / Sunset", f"{d.get('sunrise', 'N/A')} / {d.get('sunset', 'N/A')}"),
        ("Dasha Balance at Birth", f"{dasha['planet']}  {dasha['years']:.1f} years"),
        ("Ayanamsa (Lahiri)", f"{d['ayanamsa']:.4f}°"),
        ("Julian Day", str(d["julian_day"])),
    ]

    rows_html = ""
    for label, value in rows:
        if label == "":
            rows_html += '<tr><td colspan="2" style="height: 6px; border: none;"></td></tr>'
        else:
            rows_html += f"<tr><td style='font-weight:bold; color:#555; width:45%;'>{label}</td><td>{value}</td></tr>"

    return f"""
    <h2>Basic Details</h2>
    <table>{rows_html}</table>

    <h3>Planetary Positions</h3>
    <table>
        <tr><th>Planet</th><th>Sign</th><th>Degree</th><th>House</th><th>Lord</th><th>Retro</th></tr>
        {''.join(_planet_row(name, info) for name, info in d['planets'].items())}
    </table>"""


def _planet_row(name: str, info: dict) -> str:
    retro = "*" if info["retrograde"] else ""
    return f"<tr><td><strong>{name}</strong></td><td>{info['sign_name']}</td><td>{info['degree_in_sign']:.1f}°</td><td>{info['house']}</td><td>{info['sign_lord']}</td><td>{retro}</td></tr>"


def _favourable_ghatak(d: dict) -> str:
    sign = d["lagna"]["sign_name"]
    fav = FAVOURABLE.get(sign, {})
    ghat = GHATAK.get(sign, {})

    fav_rows = "".join(
        f"<tr><td style='font-weight:bold; color:#555;'>{k.replace('_', ' ').title()}</td><td>{v}</td></tr>"
        for k, v in fav.items()
    )
    ghat_rows = "".join(
        f"<tr><td style='font-weight:bold; color:#555;'>{k.replace('bad_', '').replace('_', ' ').title()}</td><td>{v}</td></tr>"
        for k, v in ghat.items()
    )

    return f"""
    <div class="page-break"></div>
    <h2>Avakahada Chakra &amp; Favourable Points</h2>
    <div class="two-col">
        <div>
            <h3>Favourable Points</h3>
            <table>{fav_rows}</table>
        </div>
        <div>
            <h3>Ghatak (Malefics)</h3>
            <table>{ghat_rows}</table>
        </div>
    </div>"""


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


def _planet_positions(d: dict) -> str:
    html = '<div class="page-break"></div><h2>Planetary Positions &amp; Effects</h2>'
    html += "<p>Below is the analysis of each planet's position in your birth chart with effects and remedies.</p>"

    for name, info in d["planets"].items():
        house = info["house"]
        house_data = PLANET_IN_HOUSE.get(name, {}).get(house, {})
        if not house_data:
            continue

        retro_str = " (Retrograde)" if info["retrograde"] else ""
        benefic = house_data.get("benefic", "")
        malefic = house_data.get("malefic", "")
        remedies = house_data.get("remedies", [])

        remedies_html = ""
        if remedies:
            remedies_html = '<h4 style="margin: 8px 0 4px;">Remedies</h4>'
            for r in remedies:
                remedies_html += f'<div class="remedy">{r}</div>'

        html += f"""
        <div class="section">
            <h3>{name} in {info['sign_name']} — {_ordinal(house)} House{retro_str}</h3>
            <p><strong>If benefic:</strong> {benefic}</p>
            <p><strong>If malefic:</strong> {malefic}</p>
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
        planets = planets_in_house[house_num]
        planet_str = ", ".join(planets) if planets else "No planets"

        html += f"""
        <div class="section">
            <h3>{bhava['name']}</h3>
            <p><strong>Sign:</strong> {sign_name} &nbsp;|&nbsp; <strong>Planets:</strong> {planet_str}</p>
            <p><strong>Significations:</strong> {bhava['signification']}</p>
            <p>{bhava['description']}</p>
        </div>"""

    return html


def _divisional_charts_section(d: dict) -> str:
    """Render all divisional chart pages with SVG diagrams."""
    charts = d.get("divisional_charts", {})
    if not charts:
        return ""

    html = ""
    for chart_type in ("D9", "D10", "D2", "D3", "D12", "D60"):
        if chart_type not in charts:
            continue
        title, description = CHART_DESCRIPTIONS.get(chart_type, (chart_type, ""))
        house_signs, house_planets = _build_divisional_chart_data(d, chart_type)
        chart_svg = _chart_svg(house_signs, house_planets, chart_type)

        # Build a table of planet positions for this chart
        chart_data = charts[chart_type]
        planet_rows = ""
        for name in PLANET_ABBR:
            if name in chart_data:
                sign_num = chart_data[name]
                planet_rows += f"<tr><td><strong>{name}</strong></td><td>{SIGN_NAMES[sign_num]}</td></tr>"

        html += f"""
        <div class="page-break"></div>
        <h2>{title} ({chart_type})</h2>
        <p>{description}</p>
        {chart_svg}
        <h3>Planetary Positions in {chart_type}</h3>
        <table>
            <tr><th>Planet</th><th>Sign</th></tr>
            {planet_rows}
        </table>"""

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
