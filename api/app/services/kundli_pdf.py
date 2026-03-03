"""
Kundli PDF generator using WeasyPrint.
Builds a styled HTML document from chart_data, then converts to PDF bytes.
"""

from __future__ import annotations

from datetime import datetime

from app.services.kundli_data import (
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
        _basic_details(d),
        _favourable_ghatak(d),
        _ascendant_section(d),
        _nakshatra_section(d),
        _character_life(d),
        _manglik_section(d),
        _sadesati_section(d),
        _dasha_section(d),
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
    @page {{ size: A4; margin: 20mm 15mm; }}
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
        ("Latitude / Longitude", f"{d['lat']:.2f}N / {d['lon']:.2f}E"),
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
    retro = "R" if info["retrograde"] else ""
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
