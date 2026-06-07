"""PDF section builders + chart helpers for the Kundli report.

Everything in here is called BY `kundli_pdf.py` (the facade) but NOT
directly patched by tests. The facade keeps `_css`, `_cover`, `_footer`
and `SECTION_BUILDERS` because tests do
`monkeypatch.setattr(kundli_pdf, "<name>", stub)` on those four — and
that pattern only works when the patched name lives in the module that
gets monkeypatched.

Constants (`LOGO_URL`, `BRAND`, `SIGN_ABBR`, `SIGN_NAMES`, `SIGN_LORDS`,
`PLANET_ABBR`, `_HOUSE_TEXT_POS`, `CHART_DESCRIPTIONS`) are imported
back from `kundli_pdf` — they're defined at the top of that module
before the `from .pdf_sections import ...` line fires, so the
back-import resolves cleanly.
"""

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
try:
    from app.services.kundli_data import MUDDA_DASHA_BHAV_DATA
except ImportError:
    MUDDA_DASHA_BHAV_DATA = {}

# LAL_KITAB_DATA is also large and authored separately.
try:
    from app.services.kundli_data import LAL_KITAB_DATA
except ImportError:
    LAL_KITAB_DATA = {}

# Back-import shared constants from the facade. Resolved at call time so the
# circular reference is fine — kundli_pdf.py defines these at the top of the
# module before its `from .pdf_sections import ...` line fires.
from app.services.kundli_pdf import (  # noqa: E402
    BRAND,
    CHART_DESCRIPTIONS,
    LOGO_URL,
    PLANET_ABBR,
    SIGN_ABBR,
    SIGN_LORDS,
    SIGN_NAMES,
    _HOUSE_TEXT_POS,
)


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

def _summary_grid(d: dict) -> str:
    """Astrosage-style page 2 — all 4 info blocks in a compact 2×2 grid."""

    def _mini_table(rows: list[tuple[str, str]]) -> str:
        html = '<table style="font-size: 8pt; width: 100%; margin: 0;">'
        for label, value in rows:
            html += f'<tr><td style="padding: 2px 4px; font-weight: bold; color: #555; width: 45%; font-size: 8pt;">{label}</td><td style="padding: 2px 4px; font-size: 8pt;">{value}</td></tr>'
        html += '</table>'
        return html

    # Basic Details
    pan = d["panchanga"]
    bt = d.get("birth_time", {})
    sr = d.get("sunrise", "N/A")
    ss = d.get("sunset", "N/A")
    # Day duration
    day_duration = "—"
    try:
        def _to_sec(t):
            p = t.split(":")
            return int(p[0]) * 3600 + int(p[1]) * 60 + (int(p[2]) if len(p) > 2 else 0)
        tot = _to_sec(ss) - _to_sec(sr)
        if tot < 0: tot += 86400
        day_duration = f"{tot // 3600:02d}:{(tot % 3600) // 60:02d}:{tot % 60:02d}"
    except Exception:
        pass

    basic_rows = [
        ("Sex", d["gender"].title()),
        ("Date of Birth", "/".join(reversed(d["dob"].split("-")))),
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

    # Avkahada Chakra
    av = d.get("avkahada", {})
    nak = d["nakshatra"]
    moon = d["planets"]["Moon"]
    dasha = d["dasha"]["dashas"][0]
    avk_rows = [
        ("Paya", av.get("paya", "—")),
        ("Varna", av.get("varna", "—")),
        ("Vasya", av.get("vasya", "—")),
        ("Yoni", av.get("yoni", "—")),
        ("Gana", av.get("gana", "—")),
        ("Nadi", av.get("nadi", "—")),
        ("Tatva", av.get("tatva", "—")),
        ("Dasa Balance", _format_dasa_balance(dasha['planet'], dasha['years'])),
        ("Lagna", d["lagna"]["sign_name"]),
        ("Lagna Lord", d["lagna"]["sign_lord"]),
        ("Rasi", moon["sign_name"]),
        ("Rasi Lord", moon["sign_lord"]),
        ("Nakshatra - Pada", f"{nak['name']} - {nak['pada']}"),
        ("Nakshatra Lord", nak["lord"]),
        ("SunSign (Indian)", d["planets"]["Sun"]["sign_name"]),
        ("SunSign (Western)", _SIGN_NAMES_PDF[int(((d["planets"]["Sun"]["longitude"] + d["ayanamsa"]) % 360) / 30)]),
        ("Ayanamsa", f"{d['ayanamsa']:.4f}°"),
        ("Ayanamsa Name", "Lahiri"),
        ("Julian Day", str(d["julian_day"])),
    ]

    sign = d["lagna"]["sign_name"]
    fav = FAVOURABLE.get(sign, {})
    fav_fields = [
        ("lucky_numbers", "Lucky Numbers"), ("good_numbers", "Good Numbers"),
        ("evil_numbers", "Evil Numbers"), ("good_years", "Good Years"),
        ("lucky_days", "Lucky Days"), ("good_planets", "Good Planets"),
        ("friendly_signs", "Friendly Signs"), ("good_lagna", "Good Lagna"),
        ("lucky_metal", "Lucky Metal"), ("lucky_stone", "Lucky Stone"),
    ]
    fav_rows = [(label, fav.get(key, "—")) for key, label in fav_fields]

    ghat = GHATAK.get(sign, {})
    ghat_fields = [
        ("bad_day", "Bad Day"), ("bad_karana", "Bad Karan"),
        ("bad_lagna", "Bad Lagna"), ("bad_masa", "Bad Month"),
        ("bad_nakshatra", "Bad Nakshatra"), ("bad_prahara", "Bad Prahar"),
        ("bad_rashi", "Bad Rasi"), ("bad_tithi", "Bad Tithi"),
        ("bad_yoga", "Bad Yoga"), ("bad_planets", "Bad Planets"),
    ]
    ghat_rows = [(label, ghat.get(key, "—")) for key, label in ghat_fields]

    return f"""
    <div class="page-break"></div>
    <div style="display: flex; flex-wrap: wrap; gap: 10px;">
        <div style="flex: 1; min-width: 45%;">
            <h3 style="font-size: 11pt; margin: 0 0 4px; color: {BRAND};">Basic Details</h3>
            {_mini_table(basic_rows)}
        </div>
        <div style="flex: 1; min-width: 45%;">
            <h3 style="font-size: 11pt; margin: 0 0 4px; color: {BRAND};">Avkahada Chakra</h3>
            {_mini_table(avk_rows)}
        </div>
        <div style="flex: 1; min-width: 45%;">
            <h3 style="font-size: 11pt; margin: 0 0 4px; color: {BRAND};">Favourable Points</h3>
            {_mini_table(fav_rows)}
        </div>
        <div style="flex: 1; min-width: 45%;">
            <h3 style="font-size: 11pt; margin: 0 0 4px; color: {BRAND};">Ghatak (Malefics)</h3>
            {_mini_table(ghat_rows)}
        </div>
    </div>"""


def _basic_details(d: dict) -> str:
    """Astrosage-style Basic Details panel."""
    pan = d["panchanga"]
    bt = d.get("birth_time", {})

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
        ("Date of Birth", "/".join(reversed(d["dob"].split("-")))),
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
    """Astrosage-style Favourable Points panel."""
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
    """Astrosage-style 'Planet Consideration' — per-planet narrative."""
    lagna_sign = d["lagna"]["sign"]
    gd = d.get("graha_drishti", {})
    planet_aspects = gd.get("planet_aspects", {})
    house_aspected_by = gd.get("house_aspected_by", {})

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

    ordered_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]

    for name in ordered_planets:
        if name not in d["planets"]:
            continue
        info = d["planets"][name]
        sign_name = info["sign_name"]
        dignity = info.get("dignity", "")
        house = info["house"]

        lord_houses = _lordship_houses(name)
        if lord_houses:
            lord_str = ", ".join(f"{_ordinal(h)}" for h in lord_houses)
        else:
            lord_str = "—"

        aspects_out = planet_aspects.get(name, [])
        aspects_out_str = ", ".join(f"{_ordinal(h)}" for h in aspects_out) if aspects_out else "—"

        aspected_by = [p for p in house_aspected_by.get(str(house), []) if p != name]
        aspected_by_str = ", ".join(aspected_by) if aspected_by else "None"

        if dignity:
            article = "an" if dignity[0].lower() in "aeiou" else "a"
            dignity_label = f"{article} {dignity}" if "Sign" in dignity else f"{article} {dignity} sign"
        else:
            dignity_label = "—"

        summary = (
            f"Your {name} is in <strong>{sign_name}</strong> sign which is {dignity_label} for {name}. "
            f"{name} is lord of <strong>{lord_str}</strong> house and situated in "
            f"<strong>{_ordinal(house)}</strong> house. "
            f"{name} aspects <strong>{aspects_out_str}</strong> house and "
            f"aspected by <strong>{aspected_by_str}</strong>."
        )

        interp = PLANET_IN_HOUSE.get(name, {}).get(house, {})
        benefic = interp.get("benefic", "")
        malefic = interp.get("malefic", "")
        # Per-planet remedies are consolidated in the Remedies section, not
        # repeated here (and again in Planet Positions).

        interp_html = ""
        if benefic:
            interp_html += f"<p>{benefic}</p>"
        if malefic:
            interp_html += f"<p>{malefic}</p>"

        html += f"""
        <div class="section">
            <h3>{name} Consideration</h3>
            <p style="color:#555;">{summary}</p>
            {interp_html}
        </div>"""

    return html


def _graha_drishti_section(d: dict) -> str:
    """Vedic Graha Drishti (planetary aspects) — two-way view."""
    gd = d.get("graha_drishti")
    if not gd:
        return ""

    lagna_sign = d["lagna"]["sign"]

    rows1 = ""
    for name, houses in gd["planet_aspects"].items():
        house_str = ", ".join(
            f"{h} ({SIGN_NAMES[(lagna_sign + h - 1) % 12]})"
            for h in houses
        )
        rows1 += f"<tr><td><strong>{name}</strong> (H{d['planets'][name]['house']})</td><td>{house_str}</td></tr>"

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
    """Astrosage-style Western Planetary Aspects matrix."""
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


def _jaimini_section(d: dict) -> str:
    """Jaimini System — Chara Karakas, Karakamsa Chart, Swamsa Chart, Karak table."""
    j = d.get("jaimini")
    if not j:
        return ""

    kk_signs, kk_planets = _build_jaimini_d1_chart(d, j["karakamsa_sign"])
    sw_signs, sw_planets = _build_jaimini_d9_chart(d, j["swamsa_sign"])
    kk_svg = _chart_svg(kk_signs, kk_planets, "Karakamsa Chart", size=240)
    sw_svg = _chart_svg(sw_signs, sw_planets, "Swamsa Chart", size=240)

    karak_rows = ""
    for role in JAIMINI_CHARA_ROLES:
        sthira = j["sthira"].get(role, "—")
        chara_entry = j["chara"].get(role, {})
        chara_planet = chara_entry.get("planet", "—")
        chara_deg = chara_entry.get("degree", "")
        karak_rows += (
            f'<tr>'
            f'<td style="font-weight:bold; padding:4px 8px;">{role}</td>'
            f'<td style="padding:4px 8px;">{sthira}</td>'
            f'<td style="padding:4px 8px;">{chara_planet}'
            f'{f" <span style=\"color:#888; font-size:8pt;\">({chara_deg}°)</span>" if chara_deg != "" else ""}'
            f'</td>'
            f'</tr>'
        )

    return f"""
    <div class="page-break"></div>
    <h2>Jaimini System — Karakamsa &amp; Swamsa</h2>
    <p>The Jaimini system overlays the standard Parashari chart with a parallel
    set of significators (the <em>Chara Karakas</em>) and two derived charts
    used for soul-purpose and dharma readings. Both charts use the same lagna
    — your <strong>Atmakaraka</strong>'s navamsa sign — but show different
    placements: the <strong>Karakamsa Chart</strong> rotates your <em>Rasi
    (D1) chart</em> so this sign sits as the 1st house, while the
    <strong>Swamsa Chart</strong> rotates your <em>Navamsa (D9) chart</em>
    the same way. Your AK is <strong>{j["atmakaraka"]}</strong> and its
    navamsa sign is <strong>{j["karakamsa_sign_name"]}</strong>.</p>

    <div style="display:flex; gap:8px; margin-bottom:6px; page-break-inside: avoid;">
        <div style="flex:1; text-align:center; border:1px solid #e5e0ff; border-radius:6px; padding:4px;">{kk_svg}</div>
        <div style="flex:1; text-align:center; border:1px solid #e5e0ff; border-radius:6px; padding:4px;">{sw_svg}</div>
    </div>

    <h3 style="margin-top:14px;">Karak Table — Sthira (Fixed) and Chara (Movable)</h3>
    <p>Sthira Karakas are the classical fixed assignments used as a baseline.
    Chara Karakas are computed from your chart by ranking the seven classical
    planets by their degree-within-sign in descending order — the highest-degree
    planet is the Atmakaraka (soul indicator), the lowest is the Darakaraka
    (spouse indicator).</p>
    <table style="width:100%; border-collapse:collapse;">
        <tr>
            <th style="background:{BRAND}; color:white; padding:6px 8px; text-align:left;">Karak</th>
            <th style="background:{BRAND}; color:white; padding:6px 8px; text-align:left;">Sthira (Fixed)</th>
            <th style="background:{BRAND}; color:white; padding:6px 8px; text-align:left;">Chara (Your Chart)</th>
        </tr>
        {karak_rows}
    </table>

    {_avastha_table(j.get("avasthas", []))}
    """


def _avastha_table(avasthas: list[dict]) -> str:
    """Render the Avastha (planetary state) table — Jagradadi + Baladi + Deeptadi."""
    if not avasthas:
        return ""
    rows = ""
    for a in avasthas:
        rows += (
            f'<tr>'
            f'<td style="padding:4px 8px; font-weight:bold;">{a["planet"]}</td>'
            f'<td style="padding:4px 8px;">{a["jagradadi"]}</td>'
            f'<td style="padding:4px 8px;">{a["baladi"]}</td>'
            f'<td style="padding:4px 8px;">{a["deeptadi"]}</td>'
            f'</tr>'
        )
    return f"""
    <h3 style="margin-top:18px;">Avastha — Planetary States</h3>
    <p>The Avasthas describe the condition of each planet in your chart across
    three classical scales: <strong>Jagradadi</strong> (waking / dreaming /
    sleeping — based on the sign-lord relationship), <strong>Baladi</strong>
    (5-stage life progression based on degree in sign — infant to dead), and
    <strong>Deeptadi</strong> (9-stage condition combining sign dignity,
    combustion, planetary war, Shadbala strength and malefic affliction).
    Stronger Avasthas amplify the planet's positive results; weaker ones
    diminish them.</p>
    <table style="width:100%; border-collapse:collapse;">
        <tr>
            <th style="background:{BRAND}; color:white; padding:6px 8px; text-align:left;">Planet</th>
            <th style="background:{BRAND}; color:white; padding:6px 8px; text-align:left;">Jagradadi</th>
            <th style="background:{BRAND}; color:white; padding:6px 8px; text-align:left;">Baladi</th>
            <th style="background:{BRAND}; color:white; padding:6px 8px; text-align:left;">Deeptadi</th>
        </tr>
        {rows}
    </table>
    <p style="font-size:9pt; color:#888; margin-top:6px;"><em>Baladi values
    match Astrosage exactly. Jagradadi follows the classical sign-lord
    relationship (only an enemy lord drives Susupta). Deeptadi combines sign
    dignity, combustion (proximity to Sun), planetary war (≤1° proximity to
    another planet), Shadbala strength and malefic affliction — first match
    in priority order: Vikala → Khala → Deena → Deepta → Swastha → Mudita
    → Shakta → Pidita → Shanta. Friendship takes precedence over
    debilitation; positive sign-dignity states take precedence over Shakta.</em></p>
    """


def _char_dasha_section(d: dict) -> str:
    """Jaimini Chara Dasha — sign-based MDs from natal lagna + sub-periods."""
    cd = d.get("char_dasha")
    if not cd or not cd.get("dashas"):
        return ""

    summary_rows = ""
    for entry in cd["dashas"]:
        summary_rows += (
            f"<tr><td><strong>{entry['sign_name']}</strong></td>"
            f"<td>{entry['years']} years</td>"
            f"<td>{entry['start_date']}</td>"
            f"<td>{entry['end_date']}</td></tr>"
        )

    html = f"""
    <div class="page-break"></div>
    <h2>Char Dasha (Jaimini Chara Dasha)</h2>
    <p>Char Dasha is a sign-based (Rashi) dasha system from the Jaimini Sutras,
    distinct from the Nakshatra-based Vimshottari Dasha. Each Mahadasha's
    duration is computed by counting from the sign to its lord (forward for
    odd signs, backward for even signs) and subtracting one. The cycle starts
    from your Lagna sign and progresses zodiacally if the Lagna is odd, or
    anti-zodiacally if even. Antardashas within each MD cycle through all
    twelve signs in the same direction, each lasting MD/12.</p>
    <table style="page-break-inside: auto;">
        <tr><th>Sign</th><th>Duration</th><th>Start</th><th>End</th></tr>
        {summary_rows}
    </table>"""

    for entry in cd["dashas"]:
        ad_rows = ""
        for ad in entry.get("antardashas", []):
            ad_rows += (
                f"<tr><td>{ad['sign_name']}</td>"
                f"<td>{ad['start_date']}</td><td>{ad['end_date']}</td></tr>"
            )
        html += f"""
        <div class="section">
            <h4 style="color:#555; margin: 12px 0 4px;">{entry['sign_name']} Mahadasha — {entry['years']} years ({entry['start_date']} to {entry['end_date']})</h4>
            <table style="font-size: 9pt;">
                <tr><th>Sub-Period (Sign)</th><th>Start</th><th>End</th></tr>
                {ad_rows}
            </table>
        </div>"""

    return html


def _yogini_dasha_section(d: dict) -> str:
    """Yogini Dasha — 36-year cycle with 8 yoginis."""
    yd = d.get("yogini_dasha")
    if not yd:
        return ""

    summary_rows = ""
    for entry in yd["dashas"]:
        summary_rows += (
            f"<tr><td><strong>{entry['abbr']}</strong> ({entry['yogini']})</td>"
            f"<td>{entry['years']} years</td><td>{entry['start_date']}</td>"
            f"<td>{entry['end_date']}</td></tr>"
        )

    html = f"""
    <div class="page-break"></div>
    <h2>Yogini Dasha</h2>
    <p>The Yogini Dasha is a 36-year cycle based on 8 yoginis. It is particularly useful for
    timing events within 1-2 year windows. Your starting yogini is <strong>{yd['starting_yogini']}</strong>
    with <strong>{yd['balance_years']}</strong> years remaining at birth.</p>
    <table style="page-break-inside: auto;">
        <tr><th>Yogini</th><th>Duration</th><th>Start</th><th>End</th></tr>
        {summary_rows}
    </table>"""

    # Sub-period tables are narrow (3 cols); lay them two-per-row to halve the
    # page span. Each cell is atomic; rows break between pairs.
    cells = []
    for entry in yd["dashas"]:
        ad_rows = ""
        for ad in entry.get("antardashas", []):
            ad_rows += (
                f"<tr><td>{ad['abbr']} ({ad['yogini']})</td>"
                f"<td>{ad['start_date']}</td><td>{ad['end_date']}</td></tr>"
            )
        cells.append(
            f'<div style="width:48%; box-sizing:border-box;">'
            f'<h4 style="color:#555; margin:8px 0 3px; font-size:10pt;">{entry["abbr"]} — {entry["yogini"]}</h4>'
            f'<div style="font-size:8pt; color:#888; margin-bottom:2px;">{entry["start_date"]} to {entry["end_date"]}</div>'
            f'<table style="font-size:8pt;"><tr><th>Sub-Period</th><th>Start</th><th>End</th></tr>{ad_rows}</table>'
            f'</div>'
        )
    for k in range(0, len(cells), 2):
        pair = "".join(cells[k:k + 2])
        html += f'<div style="display:flex; flex-wrap:nowrap; justify-content:space-between; page-break-inside:avoid;">{pair}</div>'

    return html


def _shodashvarga_table_section(d: dict) -> str:
    """Astrosage-style Shodashvarga Bhav Table."""
    charts = d.get("divisional_charts", {})
    if not charts:
        return ""

    varga_order = [
        "D2", "D3", "D4", "D7", "D9", "D10",
        "D12", "D16", "D20", "D24", "D27", "D30",
        "D40", "D45", "D60",
    ]
    present_vargas = [v for v in varga_order if v in charts]

    header = "<th>Planet</th>" + "".join(
        f"<th style='text-align:center; font-size:8pt; padding:3px;'>{v}</th>"
        for v in present_vargas
    )

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


def _kp_section(d: dict) -> str:
    """KP System / Nakshatra Nadi — Ruling Planet box, Cuspal Position table,
    and per-planet sub-lord table. Uses Krishnamurti ayanamsa + Placidus cusps
    (verified 12/12 sub-lords vs Astrosage for the reference chart)."""
    kp = d.get("kp")
    if not kp:
        return ""

    abbr = {"Sun": "Su", "Moon": "Mo", "Mars": "Ma", "Mercury": "Me",
            "Jupiter": "Ju", "Venus": "Ve", "Saturn": "Sa", "Rahu": "Ra", "Ketu": "Ke"}

    def _deg(v):
        d_ = int(v); m = int((v - d_) * 60); s = int(round(((v - d_) * 60 - m) * 60))
        if s == 60:
            s = 0; m += 1
        return f"{d_:02d}°{m:02d}'{s:02d}\""

    # Ruling planets (Lagna + Moon)
    ruling_rows = ""
    for who in ("Lagna", "Moon"):
        r = kp["ruling"][who]
        ruling_rows += (
            f"<tr><td style='font-weight:bold;'>{who}</td><td>{r['sign']}</td>"
            f"<td>{r['nak_lord']}</td><td>{r['sub_lord']}</td></tr>"
        )

    # Cuspal positions
    cusp_rows = ""
    for c in kp["cusps"]:
        cusp_rows += (
            f"<tr><td style='text-align:center;'>{c['house']}</td>"
            f"<td>{_deg(c['degree'])}</td><td>{c['sign']}</td>"
            f"<td>{c['nakshatra']}</td><td>{c['nak_lord']}</td>"
            f"<td>{c['sub_lord']}</td><td>{c['sub_sub_lord']}</td></tr>"
        )

    # Planetary sub-lords
    planet_order = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus",
                    "Saturn", "Rahu", "Ketu"]
    planet_rows = ""
    for name in planet_order:
        p = kp["planets"].get(name)
        if not p:
            continue
        planet_rows += (
            f"<tr><td style='font-weight:bold;'>{name}</td>"
            f"<td>{_deg(p['degree'])}</td><td>{p['sign']}</td>"
            f"<td>{p['nakshatra']}</td><td>{p['nak_lord']}</td>"
            f"<td>{p['sub_lord']}</td><td>{p['sub_sub_lord']}</td></tr>"
        )

    return f"""
    <div class="page-break"></div>
    <h2>KP System / Nakshatra Nadi</h2>
    <p style='font-size:10pt; color:#666;'>Krishnamurti Paddhati refines each placement with a
    <strong>sub-lord</strong>: each nakshatra is split into nine unequal parts in Vimshottari-dasha
    proportion. Computed with the KP (Krishnamurti) ayanamsa and Placidus house cusps, per KP tradition.</p>
    <h3>Ruling Planets</h3>
    <table style='font-size:9.5pt;'>
        <tr><th>Body</th><th>Sign (Rasi)</th><th>Nakshatra Lord</th><th>Sub Lord</th></tr>
        {ruling_rows}
    </table>
    <h3>Cuspal Positions</h3>
    <table style='font-size:9pt;'>
        <tr><th>Cusp</th><th>Degree</th><th>Sign</th><th>Nakshatra</th><th>Nak Lord</th><th>Sub Lord</th><th>Sub-Sub</th></tr>
        {cusp_rows}
    </table>
    <h3>Planetary Sub-Lords</h3>
    <table style='font-size:9pt;'>
        <tr><th>Planet</th><th>Degree</th><th>Sign</th><th>Nakshatra</th><th>Nak Lord</th><th>Sub Lord</th><th>Sub-Sub</th></tr>
        {planet_rows}
    </table>
    {_kp_cusp_aspects_table(kp)}"""


def _kp_cusp_aspects_table(kp: dict) -> str:
    """Aspects On KP Cusp (Astrosage p53): planet × 12-cusp matrix of
    Western-style angular aspects (abbr + orb), '—' where none within orb."""
    ca = kp.get("cusp_aspects")
    if not ca or not ca.get("planets"):
        return ""
    abbr = {"Sun": "Su", "Moon": "Mo", "Mars": "Ma", "Mercury": "Me",
            "Jupiter": "Ju", "Venus": "Ve", "Saturn": "Sa", "Rahu": "Ra", "Ketu": "Ke"}
    th = "padding:3px 4px; background:#f3f0ff; text-align:center; font-size:8pt;"
    headers = "".join(f'<th style="{th}">{i}</th>' for i in range(1, 13))
    rows = ""
    for p in ca["planets"]:
        cells = ""
        for cell in ca["matrix"][p]:
            if cell:
                cells += (f'<td style="text-align:center; font-size:7.5pt; padding:2px;">'
                          f'{cell["abbr"]}<br><span style="color:#999;">{cell["orb"]}</span></td>')
            else:
                cells += '<td style="text-align:center; color:#ccc; padding:2px;">—</td>'
        rows += (f'<tr><td style="font-weight:bold; padding:2px 4px;">{abbr.get(p, p)}</td>{cells}</tr>')
    return f"""
    <h3>Aspects on KP Cusp</h3>
    <p style='font-size:9pt; color:#666;'>Western-style angular aspects (Conjunction, Sextile, Square, Trine,
    Opposition + minor) each planet casts onto the 12 house cusps, with orb in degrees.</p>
    <table style='font-size:8pt;'>
        <tr><th style="{th}">Planet</th>{headers}</tr>
        {rows}
    </table>"""


def _friendship_section(d: dict) -> str:
    """Astrosage-style Friendship Tables — Permanent, Temporary, Compound."""
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
    """Astrosage-style Ghatak (Malefics) panel — points to avoid."""
    sign = d["lagna"]["sign_name"]
    ghat = GHATAK.get(sign, {})

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
    pada_text = NAKSHATRA_PADA_DATA.get(nak["num"], {}).get(nak["pada"], "")
    pada_block = (
        f'<h3 style="margin-top:14px;">Your Pada: {nak["pada"]}</h3><p>{pada_text}</p>'
        if pada_text else f'<p><strong>Pada:</strong> {nak["pada"]}</p>'
    )
    return f"""
    <h2>Your Nakshatra: {nak['name']}</h2>
    <p><strong>Pada:</strong> {nak['pada']} &nbsp;|&nbsp; <strong>Lord:</strong> {nak['lord']}</p>
    <p>{data.get('prediction', '')}</p>
    {pada_block}"""


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
    """Current Vimshottari Mahadasha narrative."""
    current = d["dasha"]["current_dasha"]
    pred = DASHA_PREDICTIONS.get(current["planet"], "")

    return f"""
    <div class="page-break"></div>
    <h2>Current Mahadasha: {current['planet']}</h2>
    <p>The Vimshottari Dasha system covers a 120-year cycle of planetary periods based on your
    birth Nakshatra. The full sequence is shown on the at-a-glance summary page; this section
    introduces your <strong>current</strong> Mahadasha lord.</p>
    <div style="background:#f3f0ff; border-left:4px solid {BRAND}; padding:10px 14px; margin:8px 0;">
        <strong>Current Period:</strong> {current['planet']} Mahadasha
        &nbsp;|&nbsp; <strong>Runs:</strong> {current['start_date']} → {current['end_date']}
    </div>
    <p>{pred}</p>"""


def _mahadasha_phal_section(d: dict) -> str:
    """Astrosage-style Mahadasha Phal — house-specific interpretation per period."""
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

        house_data = PLANET_IN_HOUSE.get(planet, {}).get(house, {}) if house else {}
        benefic = house_data.get("benefic", "")
        malefic = house_data.get("malefic", "")

        interp_html = ""
        if benefic:
            interp_html += f"<p>{benefic}</p>"
        if malefic:
            interp_html += f"<p>{malefic}</p>"
        if not interp_html:
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
        # Remedies consolidated in the Remedies section (not repeated here).

        if dignity in _BENEFIC_DIGNITIES:
            interp_html = f"<p>{benefic}</p>"
        elif dignity in _MALEFIC_DIGNITIES:
            interp_html = f"<p>{malefic}</p>"
        else:
            interp_html = f"<p><strong>If well-placed:</strong> {benefic}</p><p><strong>If ill-placed:</strong> {malefic}</p>"

        html += f"""
        <div class="section">
            <h3>{name} in {info['sign_name']}{dignity_badge} — {_ordinal(house)} House{retro_str}</h3>
            {interp_html}
        </div>"""

    return html


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

def _at_a_glance(d: dict) -> str:
    """Dense single-page summary — the Astrosage page-3 equivalent."""
    nak = d["nakshatra"]
    moon = d["planets"]["Moon"]
    current = d["dasha"]["current_dasha"]

    d1_signs, d1_planets = _build_d1_chart_data(d)
    d9_signs, d9_planets = _build_divisional_chart_data(d, "D9")
    d1_svg = _chart_svg(d1_signs, d1_planets, "D1 — Lagna", size=270)
    d9_svg = _chart_svg(d9_signs, d9_planets, "D9 — Navamsa", size=270)

    def _fmt_deg(deg: float) -> str:
        d_int = int(deg)
        rem = (deg - d_int) * 60
        m_int = int(rem)
        s_int = int(round((rem - m_int) * 60))
        if s_int == 60:
            m_int += 1
            s_int = 0
        if m_int == 60:
            d_int += 1
            m_int = 0
        return f"{d_int}°{m_int:02d}'{s_int:02d}\""

    def _planet_row_local(label: str, sign_name: str, lord: str, deg: float, nak_name: str, pada: int, dignity: str, retro: bool) -> str:
        dignity_color = _DIGNITY_COLOR.get(dignity, "#888")
        retro_cell = "R" if retro else ""
        return (
            f'<tr>'
            f'<td style="padding:2px 4px; font-weight:bold; border-bottom:1px solid #eee;">{label}</td>'
            f'<td style="padding:2px 4px; border-bottom:1px solid #eee;">{sign_name}</td>'
            f'<td style="padding:2px 4px; border-bottom:1px solid #eee;">{lord}</td>'
            f'<td style="padding:2px 4px; border-bottom:1px solid #eee;">{_fmt_deg(deg)}</td>'
            f'<td style="padding:2px 4px; border-bottom:1px solid #eee;">{nak_name}</td>'
            f'<td style="padding:2px 4px; border-bottom:1px solid #eee; text-align:center;">{pada}</td>'
            f'<td style="padding:2px 4px; border-bottom:1px solid #eee; color:{dignity_color}; font-size:7pt;">{dignity}</td>'
            f'<td style="padding:2px 4px; border-bottom:1px solid #eee; text-align:center; color:#dc2626; font-weight:bold;">{retro_cell}</td>'
            f'</tr>'
        )

    lagna = d["lagna"]
    lagna_nak = calc_nakshatra(lagna["longitude"])
    planet_rows_html = _planet_row_local(
        "ASC", lagna["sign_name"], lagna["sign_lord"], lagna["degree"],
        lagna_nak["name"], lagna_nak["pada"], "", False,
    )
    for name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu", "Uranus", "Neptune", "Pluto"]:
        info = d["planets"].get(name)
        if not info:
            continue
        pnak = calc_nakshatra(info["longitude"])
        planet_rows_html += _planet_row_local(
            name, info["sign_name"], info["sign_lord"], info["degree_in_sign"],
            pnak["name"], pnak["pada"], info.get("dignity", ""), info.get("retrograde", False),
        )

    dasha_rows_html = ""
    for ds in d["dasha"]["dashas"]:
        is_cur = ds["planet"] == current["planet"] and ds["start_date"] == current["start_date"]
        row_style = ' style="background:#f3f0ff; font-weight:bold;"' if is_cur else ""
        label = " (Current)" if is_cur else ""
        dasha_rows_html += (
            f'<tr{row_style}>'
            f'<td style="padding:2px 4px; border-bottom:1px solid #eee;">{ds["planet"]}{label}</td>'
            f'<td style="padding:2px 4px; border-bottom:1px solid #eee;">{ds["start_date"]}</td>'
            f'<td style="padding:2px 4px; border-bottom:1px solid #eee;">{ds["end_date"]}</td>'
            f'</tr>'
        )

    dob_fmt = "/".join(reversed(d["dob"].split("-")))
    section_title = (
        f'font-size:8.5pt; font-weight:bold; color:{BRAND}; '
        f'border-bottom:1px solid {BRAND}; margin:4px 0 2px; padding-bottom:1px;'
    )
    col_th = f'background:{BRAND}; color:white; padding:3px 4px; text-align:left; font-size:7.5pt;'

    return f"""
    <div class="page-break"></div>
    <div>
        <div style="background:#f9f7ff; border:1px solid #e5e0ff; border-radius:6px; padding:6px 10px; margin-bottom:6px;">
            <div style="font-size:13pt; color:{BRAND}; font-weight:bold;">{d['name']} — Birth Chart at a Glance</div>
            <div style="font-size:8pt; color:#555; margin-top:2px; line-height:1.35;">
                <strong>DOB:</strong> {dob_fmt}
                &nbsp;|&nbsp; <strong>Time:</strong> {d['tob']}
                &nbsp;|&nbsp; <strong>Place:</strong> {d['place_name']}
                &nbsp;|&nbsp; <strong>Gender:</strong> {d['gender'].title()}
                <br/>
                <strong>Lagna:</strong> {d['lagna']['sign_name']} ({d['lagna']['sign_lord']})
                &nbsp;|&nbsp; <strong>Rasi:</strong> {moon['sign_name']} ({moon['sign_lord']})
                &nbsp;|&nbsp; <strong>Nakshatra:</strong> {nak['name']} — Pada {nak['pada']} ({nak['lord']})
            </div>
        </div>

        <div style="display:flex; gap:6px; margin-bottom:6px; page-break-inside: avoid;">
            <div style="flex:1; text-align:center; border:1px solid #e5e0ff; border-radius:6px; padding:2px;">{d1_svg}</div>
            <div style="flex:1; text-align:center; border:1px solid #e5e0ff; border-radius:6px; padding:2px;">{d9_svg}</div>
        </div>

        <div style="page-break-inside: avoid;">
            <div style="{section_title}">Planetary Positions</div>
            <table style="width:100%; font-size:8pt; border-collapse:collapse; margin:0;">
                <tr><th style="{col_th}">Planet</th><th style="{col_th}">Sign</th><th style="{col_th}">Lord</th><th style="{col_th}">Degree</th><th style="{col_th}">Nakshatra</th><th style="{col_th} text-align:center;">Pada</th><th style="{col_th}">Dignity</th><th style="{col_th} text-align:center;">R</th></tr>
                {planet_rows_html}
            </table>
        </div>
        <div style="page-break-inside: avoid;">
            <div style="{section_title}">Vimshottari Dasha (120-year cycle)</div>
            <table style="width:100%; font-size:8pt; border-collapse:collapse; margin:0;">
                <tr><th style="{col_th}">Planet</th><th style="{col_th}">Start Date</th><th style="{col_th}">End Date</th></tr>
                {dasha_rows_html}
            </table>
        </div>
        {_ashtakavarga_table(d, section_title, col_th)}
    </div>
    """


def _ashtakavarga_table(d: dict, section_title: str, col_th: str) -> str:
    """Render Bhinnashtakavarga per planet + Sarvashtakavarga totals per sign."""
    av = d.get("ashtakavarga")
    if not av:
        return ""

    planet_order = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    sign_headers = "".join(f'<th style="{col_th} text-align:center;">{i}</th>' for i in range(1, 13))

    body = ""
    for planet in planet_order:
        cells = "".join(
            f'<td style="padding:2px 4px; border-bottom:1px solid #eee; text-align:center;">{b}</td>'
            for b in av["bindus"][planet]
        )
        body += (
            f'<tr>'
            f'<td style="padding:2px 4px; font-weight:bold; border-bottom:1px solid #eee;">{planet}</td>'
            f'{cells}'
            f'</tr>'
        )

    total_cells = "".join(
        f'<td style="padding:3px 4px; border-top:2px solid {BRAND}; text-align:center; font-weight:bold;">{t}</td>'
        for t in av["totals"]
    )
    body += (
        f'<tr style="background:#f3f0ff;">'
        f'<td style="padding:3px 4px; border-top:2px solid {BRAND}; font-weight:bold; color:{BRAND};">Total</td>'
        f'{total_cells}'
        f'</tr>'
    )

    return f"""
        <div style="page-break-inside: avoid;">
            <div style="{section_title}">Ashtakavarga (Bindus per sign — grand total {av['grand_total']})</div>
            <table style="width:100%; font-size:8pt; border-collapse:collapse; margin:0;">
                <tr><th style="{col_th}">Sign №</th>{sign_headers}</tr>
                {body}
            </table>
        </div>
        {_sarva_chart(d, av)}
        {_prasthar_tables(d, av, section_title, col_th)}
    """


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


def _prasthar_tables(d: dict, av: dict, section_title: str, col_th: str) -> str:
    """Prastharashtakavarga — for each planet, the 8 contributors × 12 signs
    bindu matrix (Astrosage page 55). `prasthar[planet][contributor][sign]`."""
    prasthar = av.get("prasthar")
    if not prasthar:
        return ""

    planet_order = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    contributors = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Lagna"]
    abbr = {"Sun": "Su", "Moon": "Mo", "Mars": "Ma", "Mercury": "Me",
            "Jupiter": "Ju", "Venus": "Ve", "Saturn": "Sa", "Lagna": "La"}
    sign_headers = "".join(f'<th style="{col_th} text-align:center;">{i}</th>' for i in range(1, 13))

    blocks = []
    for planet in planet_order:
        rows = ""
        for contributor in contributors:
            cells = "".join(
                f'<td style="padding:1px 3px; border-bottom:1px solid #eee; text-align:center; '
                f'{"color:#bbb;" if v == 0 else "font-weight:600;"}">{v}</td>'
                for v in prasthar[planet][contributor]
            )
            rows += (
                f'<tr><td style="padding:1px 3px; font-weight:bold; border-bottom:1px solid #eee;">'
                f'{abbr[contributor]}</td>{cells}</tr>'
            )
        # total row for this planet
        col_totals = [sum(prasthar[planet][c][s] for c in contributors) for s in range(12)]
        total_cells = "".join(
            f'<td style="padding:2px 3px; border-top:2px solid {BRAND}; text-align:center; font-weight:bold;">{t}</td>'
            for t in col_totals
        )
        rows += (
            f'<tr style="background:#f3f0ff;"><td style="padding:2px 3px; border-top:2px solid {BRAND}; '
            f'font-weight:bold; color:{BRAND};">Total</td>{total_cells}</tr>'
        )
        blocks.append(
            f'<div style="page-break-inside: avoid; margin-top:8px;">'
            f'<div style="font-weight:bold; color:{BRAND}; font-size:9.5pt; margin:6px 0 2px;">{planet}</div>'
            f'<table style="width:100%; font-size:7.5pt; border-collapse:collapse; margin:0;">'
            f'<tr><th style="{col_th}">Contrib</th>{sign_headers}</tr>{rows}</table></div>'
        )

    return (
        f'<div style="margin-top:12px;">'
        f'<div style="{section_title}">Prastharashtakavarga (contributor detail per sign)</div>'
        f'<div style="font-size:8.5pt; color:#777; margin-bottom:4px;">Each row shows which contributor '
        f'(Su Mo Ma Me Ju Ve Sa, plus La = Lagna) grants a bindu to the planet in each of the 12 signs.</div>'
        f'{"".join(blocks)}</div>'
    )


def _birth_chart_page(d: dict) -> str:
    """Moon Chart (Chandra Kundli) page with personalised interpretation."""
    return f"""
    <div class="page-break"></div>
    <div class="chart-block">
    <h2>Moon Chart (Chandra Kundli)</h2>
    <p>The Chandra Kundli places <strong>{d['planets']['Moon']['sign_name']}</strong> (your Moon sign) in the
    first house, showing all planetary positions relative to the Moon. While the Lagna chart reveals your
    outer personality and physical life, the Moon chart reveals your <strong>emotional landscape, mental
    patterns, and how you experience life internally</strong>. Vedic transit predictions (Gochar) are
    primarily read from this chart.</p>
    {_moon_chart_svg(d)}
    {_moon_chart_interpretation(d)}
    </div>
    """


def _moon_chart_interpretation(d: dict) -> str:
    """Generate personalized interpretation of the Moon chart placements."""
    moon_sign = d["planets"]["Moon"]["sign"]

    kendra_planets = []
    trikona_planets = []
    for name, info in d["planets"].items():
        if name == "Moon":
            continue
        house_from_moon = ((info["sign"] - moon_sign) % 12) + 1
        if house_from_moon in (1, 4, 7, 10):
            kendra_planets.append(f"{name} ({_ordinal(house_from_moon)})")
        if house_from_moon in (1, 5, 9):
            trikona_planets.append(f"{name} ({_ordinal(house_from_moon)})")

    interpretation = ""
    if kendra_planets:
        interpretation += f"<p><strong>Planets in Kendra from Moon</strong> (1st, 4th, 7th, 10th — pillars of emotional stability): {', '.join(kendra_planets)}. These planets strongly influence your mental peace, domestic happiness, and emotional responses.</p>"
    if trikona_planets:
        interpretation += f"<p><strong>Planets in Trikona from Moon</strong> (1st, 5th, 9th — fortune and creativity): {', '.join(trikona_planets)}. These planets support emotional fulfilment, creative expression, and inner faith.</p>"

    if not interpretation:
        interpretation = "<p>No classical planets occupy Kendra or Trikona positions from the Moon in this chart.</p>"

    return interpretation


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
    # Two-column grid: each cell is a compact chart + short caption, so ~4
    # charts fit per page (was ~2). Each cell stays atomic (no mid-chart break).
    cells = ""
    for chart_type in (
        "D9", "D10", "D2", "D3", "D4", "D6", "D7", "D8",
        "D11", "D12", "D16", "D20", "D24", "D27", "D30",
        "D40", "D45", "D60",
    ):
        if chart_type not in charts:
            continue
        title, description = CHART_DESCRIPTIONS.get(chart_type, (chart_type, ""))
        house_signs, house_planets = _build_divisional_chart_data(d, chart_type)
        chart_svg = _chart_svg(house_signs, house_planets, "", size=210)

        lagna_sign = charts[chart_type].get("Lagna", 0)
        lagna_name = SIGN_NAMES[lagna_sign]

        cells += f"""
        <div class="dvg-cell chart-block" style="width:48%; box-sizing:border-box; padding:2px 4px 8px;">
            <div style="font-weight:bold; color:{BRAND}; font-size:10.5pt;">{title} ({chart_type})</div>
            <div style="font-size:8.5pt; color:#888; margin-bottom:2px;">{lagna_name} Ascendant</div>
            {chart_svg}
            <p style="font-size:8pt; color:#777; margin:2px 0 0;">{description}</p>
        </div>"""

    # NOTE: a flex container can't page-break internally in WeasyPrint, so a
    # single flex wrapper would jump wholesale to the next page and orphan the
    # heading. Group cells into rows of 2 — each row is an atomic flex block
    # that flows and breaks between rows, filling pages from the heading down.
    cell_list = [c for c in cells.split('<div class="dvg-cell') if c.strip()]
    rows_html = ""
    for k in range(0, len(cell_list), 2):
        pair = "".join('<div class="dvg-cell' + c for c in cell_list[k:k + 2])
        rows_html += f'<div style="display:flex; flex-wrap:nowrap; justify-content:space-between; page-break-inside:avoid;">{pair}</div>'
    html += rows_html
    return html


def _antardasha_section(d: dict) -> str:
    """Render Antardasha (sub-period) tables for each Mahadasha."""
    antardasha_list = d.get("antardasha", [])
    if not antardasha_list:
        return ""

    html = '<div class="page-break"></div><h2>Antardasha (Sub-Periods)</h2>'
    html += "<p>Each Mahadasha is divided into nine Antardashas (sub-periods). The Antardasha planet modifies the results of the Mahadasha, creating specific effects during each sub-period. Below is the complete breakdown of all sub-periods within each Mahadasha.</p>"

    current_dasha = d["dasha"]["current_dasha"]

    # Build a compact 2-up cell per Mahadasha (the AD tables are narrow), then
    # flow them two-per-row. The current-MD interpretation card is appended
    # full-width after the grid so it stays readable.
    cells = []
    current_pred_html = ""
    for md in antardasha_list:
        is_current_md = (md["mahadasha"] == current_dasha["planet"] and md["start_date"] == current_dasha["start_date"])
        md_label = " (Current)" if is_current_md else ""
        head_bg = "background:#f3f0ff;" if is_current_md else ""

        rows = ""
        for ad in md["antardashas"]:
            rows += f"<tr><td>{ad['planet']}</td><td>{ad['years']}</td><td>{ad['start_date']}</td><td>{ad['end_date']}</td></tr>"

        cells.append(
            f'<div style="width:48%; box-sizing:border-box;">'
            f'<h4 style="{head_bg} color:#555; margin:8px 0 2px; font-size:10pt; padding:2px 4px;">'
            f'{md["mahadasha"]} — {md["mahadasha_years"]}y{md_label}</h4>'
            f'<div style="font-size:8pt; color:#888; margin-bottom:2px;">{md["start_date"]} to {md["end_date"]}</div>'
            f'<table style="font-size:8pt;"><tr><th>Planet</th><th>Yrs</th><th>Start</th><th>End</th></tr>{rows}</table>'
            f'</div>'
        )

        if is_current_md:
            pred = DASHA_PREDICTIONS.get(md["mahadasha"], "")
            if pred:
                current_pred_html = f'<div class="phase-card"><h3>Current {md["mahadasha"]} Mahadasha Interpretation</h3><p>{pred}</p></div>'

    for k in range(0, len(cells), 2):
        pair = "".join(cells[k:k + 2])
        html += f'<div style="display:flex; flex-wrap:nowrap; justify-content:space-between; page-break-inside:avoid;">{pair}</div>'

    html += current_pred_html
    return html


def _pratyantar_section(d: dict) -> str:
    """Render Pratyantar Dasha (3rd-level sub-sub-periods) tables."""
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

        if md != current_md:
            if current_md is not None:
                html += '</div>'
            html += f'<div class="page-break"></div><h3>{md} Mahadasha</h3>'
            current_md = md

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
    """Shadbala and Bhavabala – Planetary Strength Calculations."""
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


def _kalsarpa_block(doshas: list[dict]) -> str:
    """Always-on Kalsarpa Dosh subsection."""
    kaal = next((x for x in doshas if x.get("type") == "kaal_sarp"), None)
    if kaal:
        sev = kaal.get("severity", "full")
        result_color, result_bg, result_border = (
            ("#15803d", "#f0fdf4", "#4ade80") if sev == "reverse"
            else ("#dc2626", "#fff7f7", "#f87171")
        )
        result_label = (
            f"<strong>{kaal['name']}</strong> is present in your horoscope. "
            f"{kaal['description']}"
        )
    else:
        result_color, result_bg, result_border = "#15803d", "#f0fdf4", "#4ade80"
        result_label = "Your Horoscope is free from Kalsarpa Yoga."

    return f"""
    <div style="page-break-inside: avoid;">
        <h3 style="margin-top:14px;">Kalsarpa Dosh / Yog</h3>
        <p>As per the current definition, when all planets are situated between Rahu and Ketu in the
        birth-chart, astrologers call it Kalsarp Dosh. Discussions about this dosh are common among
        Hindu astrologers in India, and many problems in life are often attributed to it. However, if
        all other planets are well-placed, Kalsarp Dosh need not be harmful — and may even support
        the beneficial results of those well-placed planets. Kalsarp is genuinely inauspicious only
        when the supporting planetary positions are weak. It is therefore not wise to be alarmed by
        the mere mention of Kalsarp Dosh; the actual influence varies for each person depending on
        which sign is in which house, what other planets occupy that house, and their dignities.</p>
        <p style="background:{result_bg}; border:1px solid {result_border}; color:{result_color}; padding:10px 12px; border-radius:6px;">
            <strong>Result:</strong> {result_label}
        </p>
    </div>"""


def _doshas_section(d: dict) -> str:
    """Render detected Vedic doshas (excluding Manglik and Sade Sati)."""
    doshas = d.get("doshas", [])
    other_doshas = [x for x in doshas if x.get("type") != "kaal_sarp"]

    _SEVERITY_COLOR = {"full": "#dc2626", "partial": "#b45309", "reverse": "#15803d"}

    if other_doshas:
        cards = ""
        for dosha in other_doshas:
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
        other_block = f"<h3 style='margin-top:14px;'>Other Doshas Detected</h3>{cards}"
    else:
        other_block = (
            "<h3 style='margin-top:14px;'>Other Doshas</h3>"
            "<p style='background:#f0fdf4; border:1px solid #4ade80; padding:12px; border-radius:6px;'>"
            "<strong>No other major doshas detected.</strong> Your chart is free from the remaining classical afflictions."
            "</p>"
        )

    return f"""
    <div class="page-break"></div>
    <h2>Doshas — Planetary Afflictions</h2>
    <p>Doshas are challenging planetary configurations. A dosha is not a life sentence — its severity
    depends on the overall chart strength, cancellation conditions, and free will. Remedies are available.</p>
    {_kalsarpa_block(doshas)}
    {other_block}
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


def _varshaphal_year_block(v: dict) -> str:
    """Render one Varshaphal year (current OR upcoming)."""
    muntha = v["muntha"]
    muntha_text = MUNTHA_HOUSE_DATA.get(muntha["house"], "")
    mudda = v["mudda_dasha"]
    annual_planets = v["annual_planets"]
    current = mudda["current"]
    label = v.get("label", "")
    label_pill = ""
    if label == "current":
        label_pill = (
            f' <span style="background:{BRAND}; color:white; font-size:9pt; padding:2px 10px; '
            f'border-radius:10px;">Current Year</span>'
        )
    elif label == "upcoming":
        label_pill = (
            ' <span style="background:#888; color:white; font-size:9pt; padding:2px 10px; '
            'border-radius:10px;">Upcoming Year</span>'
        )

    rows_html = ""
    cards_html = ""
    for p in mudda["periods"]:
        is_cur = p["planet"] == current["planet"] and p["start_date"] == current["start_date"]
        row_style = ' style="background:#f3f0ff; font-weight:bold;"' if is_cur else ""
        cur_label = " (Current)" if is_cur else ""
        rows_html += (
            f'<tr{row_style}>'
            f'<td>{p["planet"]}{cur_label}</td>'
            f'<td>{p["start_date"]}</td>'
            f'<td>{p["end_date"]}</td>'
            f'<td>{p["days"]}</td>'
            f'</tr>'
        )

        planet_info = annual_planets.get(p["planet"])
        if not planet_info:
            continue
        bhav = planet_info["house"]
        sign_name = planet_info["sign_name"]
        bhav_text = MUDDA_DASHA_BHAV_DATA.get(p["planet"], {}).get(bhav, "")
        if not bhav_text:
            bhav_text = (
                f"{p['planet']} occupies the {bhav}{_ordinal(bhav)[-2:]} bhav of your annual chart "
                f"(in {sign_name}). Effects during this period reflect that placement."
            )
        highlight = f' style="border-left:4px solid {BRAND}; background:#f9f7ff;"' if is_cur else ""
        cur_pill = (
            f' <span style="background:{BRAND}; color:white; font-size:8pt; padding:2px 8px; '
            f'border-radius:10px;">Current</span>'
            if is_cur else ""
        )
        cards_html += f"""
        <div style="border-left:3px solid #ddd; background:#fafafa; padding:8px 12px; margin:6px 0; page-break-inside: avoid;"{highlight}>
            <div style="font-size:10pt; font-weight:bold; color:{BRAND}; margin-bottom:2px;">
                {p["start_date"]} — {p["end_date"]} &nbsp;·&nbsp; Mudda Dasha: {p["planet"]}{cur_pill}
            </div>
            <div style="font-size:9pt; color:#666; margin-bottom:4px;">
                {p["planet"]} is in Bhav {bhav} ({sign_name}) of the annual chart.
            </div>
            <p style="margin:0; font-size:10pt;">{bhav_text}</p>
        </div>"""

    return f"""
    <h3 style="margin-top:18px; border-bottom:1px solid {BRAND}; padding-bottom:4px;">
        Year {v["target_year"]} (Age {v["age_years"]}){label_pill}
    </h3>
    <div style="background:#f9f7ff; border:1px solid #e5e0ff; border-radius:6px; padding:8px 12px; margin:6px 0;">
        <strong>Solar Return:</strong> {v["solar_return_date"]} at {v["solar_return_local_time"]} (local time)
        &nbsp;|&nbsp; <strong>Annual Lagna:</strong> {v["annual_lagna"]["sign_name"]}
    </div>

    <h4 style="margin-top:10px;">Muntha — {muntha["sign_name"]} (Bhav {muntha["house"]})</h4>
    <p>{muntha_text}</p>

    <h4 style="margin-top:14px;">Annual Vimshottari (Mudda Dasha) — Period Sequence</h4>
    <table style="width:100%; font-size:9pt; border-collapse:collapse; margin:6px 0;">
        <tr>
            <th style="background:{BRAND}; color:white; padding:4px 8px; text-align:left;">Lord</th>
            <th style="background:{BRAND}; color:white; padding:4px 8px; text-align:left;">Start</th>
            <th style="background:{BRAND}; color:white; padding:4px 8px; text-align:left;">End</th>
            <th style="background:{BRAND}; color:white; padding:4px 8px; text-align:left;">Days</th>
        </tr>
        {rows_html}
    </table>

    <h4 style="margin-top:12px;">Period-by-Period Predictions</h4>
    {cards_html}
    """


def _varshaphal_section(d: dict) -> str:
    """Varshaphal (Annual Horoscope) — current year + upcoming year."""
    bundle = d.get("varshaphal")
    if not bundle:
        return ""
    if isinstance(bundle, dict):
        bundle = [bundle]
    if not bundle:
        return ""

    blocks = "".join(_varshaphal_year_block(v) for v in bundle)

    return f"""
    <div class="page-break"></div>
    <h2>Varshaphal — Annual Horoscope</h2>
    <p>Varshaphal is the Tajik (annual) chart cast at the moment the Sun returns to its natal
    sidereal longitude each year. It shows the dominant themes for the year ahead and is read
    alongside the natal chart, not in place of it. Both your current Varshaphal year and the
    upcoming one are shown below.</p>
    {blocks}
    <p style="font-size:9pt; color:#888; margin-top:10px;"><em>Varshaphal is a forecast,
    not a fixed verdict. Read each period's notes alongside your overall natal chart strength.</em></p>
    """


def _lal_kitab_calculation_section(d: dict) -> str:
    """Lal Kitab Calculation page."""
    nak = d.get("nakshatra", {})
    pan = d.get("panchanga", {})
    bt = d.get("birth_time", {})
    lagna = d.get("lagna", {})
    moon = d.get("planets", {}).get("Moon", {})
    dasha0 = d.get("dasha", {}).get("dashas", [{}])[0]

    def _row(k, v):
        return (
            f'<td style="padding:2px 6px; font-weight:bold; color:#555; border:none; font-size:8pt;">{k}</td>'
            f'<td style="padding:2px 6px; border:none; font-size:8pt;">{v}</td>'
        )

    dasa_balance = (
        _format_dasa_balance(dasha0.get("planet", "—"), dasha0.get("years", 0))
        if dasha0 else "—"
    )
    sid = bt.get("sidereal_time", "—")
    ayan_value = f"{d.get('ayanamsa', 0):.4f}°"
    details_html = f"""
    <table style="width:100%; border-collapse:collapse; border:1px solid #ddd; margin-bottom:10px;">
        <tr>{_row("Name", d.get("name", "—"))}{_row("Longitude", bt.get("longitude_dms", "—"))}{_row("Sunrise", d.get("sunrise", "—"))}{_row("Dasa Balance", dasa_balance)}</tr>
        <tr>{_row("Sex", d.get("gender", "—").title())}{_row("Latitude", bt.get("latitude_dms", "—"))}{_row("Sunset", d.get("sunset", "—"))}{_row("Tithi", pan.get("tithi_name", "—"))}</tr>
        <tr>{_row("Date", "/".join(reversed(d.get("dob", "").split("-"))))}{_row("Place", d.get("place_name", "—"))}{_row("Yoga", pan.get("yoga_name", "—"))}{_row("Karan", pan.get("karan_name", "—"))}</tr>
        <tr>{_row("Day", bt.get("day_of_birth", "—"))}{_row("Ayan", ayan_value)}{_row("Lagna", lagna.get("sign_name", "—"))}{_row("Lagna Lord", lagna.get("sign_lord", "—"))}</tr>
        <tr>{_row("Time of Birth", d.get("tob", "—"))}{_row("Ayan Type", "Lahiri")}{_row("Rashi", moon.get("sign_name", "—"))}{_row("Rasi Lord", moon.get("sign_lord", "—"))}</tr>
        <tr>{_row("SID", sid)}{_row("", "")}{_row("Nakshatra", f"{nak.get('name', '—')}-{nak.get('pada', '')}")}{_row("Nakshatra Lord", nak.get("lord", "—"))}</tr>
    </table>"""

    planets_dict = d.get("planets", {})

    planet_order = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
    planet_rows = ""
    for name in planet_order:
        info = planets_dict.get(name)
        if not info:
            continue
        house = info.get("house", 0)
        try:
            lk_sign = SIGN_NAMES[(int(house) - 1) % 12]
        except Exception:
            lk_sign = "—"
        retro = " (R)" if info.get("retrograde") else ""
        planet_rows += (
            f'<tr>'
            f'<td style="padding:3px 6px; font-weight:bold; font-size:8pt;">{name}{retro}</td>'
            f'<td style="padding:3px 6px; font-size:8pt;">{lk_sign}</td>'
            f'</tr>'
        )

    th_style = f'background:{BRAND}; color:white; padding:4px 6px; text-align:left; font-size:8pt;'
    planet_table_html = f"""
    <div style="font-size:9pt; font-weight:bold; color:{BRAND}; margin-bottom:2px;">Planetary Positions (Lal Kitab)</div>
    <table style="width:100%; border-collapse:collapse; margin-bottom:10px;">
        <tr>
            <th style="{th_style}">Planets</th>
            <th style="{th_style}">Sign</th>
        </tr>
        {planet_rows}
    </table>
    <p style="font-size:8pt; color:#888; margin:0 0 10px;"><em>Sign follows the
    Lal Kitab convention (1st house = Aries, 2nd = Taurus, ..., 12th = Pisces).
    Soya / Kismat Jagonewala / Benefic-Malefic columns are omitted pending a
    verified rule set from a Lal Kitab commentary.</em></p>"""

    lk_house_labels = {h: h - 1 for h in range(1, 13)}
    lk_house_planets: dict[int, list[str]] = {h: [] for h in range(1, 13)}
    for name, info in d.get("planets", {}).items():
        if name not in PLANET_ABBR:
            continue
        house = info.get("house")
        if not house:
            continue
        abbr = PLANET_ABBR[name]
        if info.get("retrograde"):
            abbr += "*"
        lk_house_planets[house].append(abbr)
    lagna_chart_html = f"""
    <div style="text-align:center; margin-bottom:10px;">
        <div style="font-size:9pt; font-weight:bold; color:{BRAND};">Lagna Chart</div>
        {_chart_svg(lk_house_labels, lk_house_planets, "", size=240)}
    </div>"""

    lk = d.get("lal_kitab_dasha", {}).get("dashas", [])
    cards = ""
    for entry in lk:
        sub_rows = ""
        for sp in entry.get("subperiods", []):
            sub_rows += (
                f'<tr>'
                f'<td style="padding:1px 4px; font-size:7pt;">{sp["planet"][:3]}</td>'
                f'<td style="padding:1px 4px; font-size:7pt;">{sp["end_date"]}</td>'
                f'</tr>'
            )
        cards += f"""
        <div style="border:1px solid #ddd; padding:4px 6px; margin:2px; min-width:140px; flex:0 0 30%;">
            <div style="font-weight:bold; font-size:8pt; color:{BRAND};">{entry["planet"][:3]} {entry["years"]} Year</div>
            <table style="width:100%; border-collapse:collapse; margin:2px 0;">
                <tr><td style="padding:1px 4px; font-size:7pt; color:#555;">From</td><td style="padding:1px 4px; font-size:7pt;">{entry["start_date"]}</td></tr>
                <tr><td style="padding:1px 4px; font-size:7pt; color:#555;">To</td><td style="padding:1px 4px; font-size:7pt;">{entry["end_date"]}</td></tr>
                {sub_rows}
            </table>
        </div>"""

    dasha_html = f"""
    <div style="font-size:9pt; font-weight:bold; color:{BRAND}; margin:6px 0;">Lal Kitab Dasha</div>
    <div style="display:flex; flex-wrap:wrap;">
        {cards}
    </div>"""

    return f"""
    <div class="page-break"></div>
    <h2>Lal Kitab Calculation</h2>
    {details_html}
    <div style="display:flex; gap:10px; margin-bottom:10px;">
        <div style="flex:0 0 60%;">{planet_table_html}</div>
        <div style="flex:1;">{lagna_chart_html}</div>
    </div>
    {dasha_html}
    <p style="font-size:8pt; color:#888; margin-top:10px;"><em>Lal Kitab Dasha runs
    a fixed 35-year cycle starting at birth — Saturn (6) → Rahu (6) → Ketu (3)
    → Jupiter (6) → Sun (2) → Moon (1) → Venus (3) → Mars (6) → Mercury (2) —
    repeating across the lifetime. Each Mahadasha contains three sub-periods
    of equal length per the classical Lal Kitab lookup. Cycles shown cover
    approximately the first 105 years from birth.</em></p>
    """


def _lal_kitab_section(d: dict) -> str:
    """Lal Kitab Predictions — per-planet narrative + remedies."""
    if not LAL_KITAB_DATA:
        return ""

    planet_order = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
    cards = ""
    for name in planet_order:
        info = d.get("planets", {}).get(name)
        if not info:
            continue
        house = info.get("house")
        entry = LAL_KITAB_DATA.get(name, {}).get(house)
        if not entry:
            continue
        prediction = entry.get("prediction", "")
        remedies = entry.get("remedies", [])
        remedies_html = "".join(
            f'<div class="remedy">{r}</div>' for r in remedies
        )
        cards += f"""
        <div class="section">
            <h3>{name} in your {_ordinal(house)} house</h3>
            <p>{prediction}</p>
            <h4 style="margin: 8px 0 4px;">Remedies</h4>
            {remedies_html}
        </div>"""

    return f"""
    <div class="page-break"></div>
    <h2>Lal Kitab Predictions</h2>
    <p>Lal Kitab is a distinct astrological tradition that originated in the
    Punjab region in the early 20th century, attributed to Pandit Roop Chand
    Joshi. It uses simplified rules and offers very specific, physical
    remedies — donating particular items, wearing certain colours, performing
    rituals on specific days. The predictions below are based on the house
    placement of each planet in your natal chart. Read alongside the Vedic
    interpretations in the Planet Considerations section.</p>
    {cards}
    <p style="font-size:9pt; color:#888; margin-top:10px;"><em>Lal Kitab
    remedies are most effective when followed consistently and with sincere
    intent. Always consult a qualified Lal Kitab practitioner before adopting
    any major remedial measure.</em></p>"""


def _remedies_section(d: dict) -> str:
    """Gemstone recommendations and personalised remedies section."""
    lagna_sign = d["lagna"]["sign"]
    lagna_lord = d["lagna"]["sign_lord"]

    lord_5 = SIGN_LORDS[(lagna_sign + 4) % 12]
    lord_9 = SIGN_LORDS[(lagna_sign + 8) % 12]

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

    lords_caution = {
        SIGN_LORDS[(lagna_sign + 5) % 12],
        SIGN_LORDS[(lagna_sign + 7) % 12],
        SIGN_LORDS[(lagna_sign + 11) % 12],
    } - seen
    caution_text = ", ".join(
        f"{p} ({_GEMSTONE.get(p, '')})" for p in lords_caution if p in _GEMSTONE
    )

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

    # Per-planet remedies by house placement (consolidated here from
    # PLANET_IN_HOUSE so they appear ONCE in the report rather than being
    # repeated inline in Planet Considerations / Planet Positions).
    planet_rem_rows = ""
    for name, info in d["planets"].items():
        house = info.get("house")
        rem = PLANET_IN_HOUSE.get(name, {}).get(house, {}).get("remedies", []) if house else []
        if not rem:
            continue
        items = "".join(f'<div class="remedy">{r}</div>' for r in rem)
        planet_rem_rows += (
            f'<div style="page-break-inside:avoid; margin:6px 0;">'
            f'<div style="font-weight:bold; color:{BRAND}; font-size:10pt;">{name} '
            f'<span style="color:#888; font-weight:normal;">— {_ordinal(house)} house</span></div>'
            f'{items}</div>'
        )
    planet_rem_section = ""
    if planet_rem_rows:
        planet_rem_section = f"""
        <h3>Planetary Remedies (by house placement)</h3>
        <p>Targeted remedies for each planet based on the house it occupies in your chart.</p>
        {planet_rem_rows}"""

    # Manglik remedies live in the Manglik section (dosha-specific + only shown
    # when Manglik is present); the dosha calc carries no remedy data, so dosha
    # remedies are not consolidated here. Gemstone + weak-planet + current-dasha
    # + per-planet (by house) remedies are all gathered below.

    return f"""
    <div class="page-break"></div>
    <h2>Remedies — Gemstones &amp; Planetary</h2>
    <p>Vedic remedies work by strengthening beneficial planets and mitigating the effects of afflicted or weak ones.
    All classical remedies for your chart are gathered here in one place. <strong>Always wear gemstones only after
    consulting a qualified Jyotishi</strong> — an incorrect gemstone can cause harm. (Lal Kitab has its own distinct
    remedies, shown in the Lal Kitab section; Manglik remedies appear with the Mangal Dosha analysis.)</p>

    <h3>Recommended Gemstones</h3>
    <p>Based on your Lagna and trinal house lords, the following gemstones are considered universally beneficial for your chart:</p>
    <table>
        <tr><th>Planet</th><th>Gemstone</th><th>Reason</th><th>Lucky Day</th></tr>
        {gem_rows}
    </table>
    {caution_html}
    {weak_section}
    {dasha_remedy}
    {planet_rem_section}
    <p style="font-size:9pt; color:#888; margin-top:12px;"><em>Remedies in Vedic astrology are tools for self-improvement, not guarantees of outcome.
    The best remedy is right action (Karma), charity (Dana), and spiritual practice (Sadhana).</em></p>"""
