"""
Kundli PDF generator using WeasyPrint.

This module is now a thin orchestration facade. The 60+ section
builders + chart helpers live in `pdf_sections.py`. The four names
that tests directly monkeypatch (`SECTION_BUILDERS`, `_css`, `_cover`,
`_footer`) MUST stay here — `monkeypatch.setattr(kundli_pdf, "<name>",
stub)` only affects subsequent lookups in `kundli_pdf`'s namespace.
`_build_html` is also kept here so its `_css(...)` and
`SECTION_BUILDERS[...]` lookups resolve through the patched names.
"""

from __future__ import annotations

from datetime import datetime

# ── Public constants ────────────────────────────────────────────────────────
# Hoisted to the dependency-free leaf `pdf_constants` and re-exported here so
# existing `from app.services.kundli_pdf import BRAND` / `kundli_pdf.LOGO_URL`
# access keeps working. pdf_sections imports them from the leaf too, so there's
# no longer a circular reference between this facade and pdf_sections.
from .pdf_constants import (  # noqa: F401
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

# ── Section builders pulled from the sister module ──────────────────────────

from .pdf_sections import (  # noqa: E402,F401
    _antardasha_section,
    _ascendant_section,
    _at_a_glance,
    _avkahada_chakra,
    _basic_details,
    _birth_chart_page,
    _bhava_analysis,
    _char_dasha_section,
    _character_life,
    _dasha_section,
    _divisional_charts_section,
    _doshas_section,
    _favourable_section,
    _friendship_section,
    _ghatak_section,
    _gochar_section,
    _graha_drishti_section,
    _jaimini_section,
    _lal_kitab_calculation_section,
    _lal_kitab_section,
    _mahadasha_phal_section,
    _manglik_section,
    _nakshatra_section,
    _numerology_section,
    _kp_section,
    _planet_consideration_section,
    _planet_positions,
    _pratyantar_section,
    _remedies_section,
    _sadesati_section,
    _shadbala_section,
    _shodashvarga_table_section,
    _summary_grid,
    _varshaphal_section,
    _western_aspects_section,
    _yogas_section,
    _yogini_dasha_section,
)


# ── Public entry point ──────────────────────────────────────────────────────

def generate_pdf(chart_data: dict, sections: list[dict] | None = None) -> bytes:
    """Generate a Kundli report PDF from chart_data dict. Returns raw PDF bytes.

    sections: optional ordered list of `{id, enabled, ...}` dicts (from the
    admin report-section toggles in MongoDB). If None, the default order
    matching DEFAULT_REPORT_SECTIONS is used and the output is byte-identical
    to the pre-toggle behaviour.
    """
    html = _build_html(chart_data, sections)
    from app.services.kundli_pdf_renderer import get_renderer
    return get_renderer().render(html)


# ── HTML builder ─────────────────────────────────────────────────────────────

# Section ID → builder. Each builder takes the chart_data dict and returns an
# HTML string. Cover, footer, and CSS are not toggleable — they always render.
SECTION_BUILDERS = {
    "birth_chart":      lambda d: _birth_chart_page(d),
    "summary_grid":     lambda d: _summary_grid(d),
    "basic_details":    lambda d: _basic_details(d),
    "avkahada":         lambda d: _avkahada_chakra(d),
    "at_a_glance":      lambda d: _at_a_glance(d),
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
    "jaimini":          lambda d: _jaimini_section(d),
    "yogini_dasha":     lambda d: _yogini_dasha_section(d),
    "char_dasha":       lambda d: _char_dasha_section(d),
    "divisional":       lambda d: _divisional_charts_section(d),
    "shodashvarga":     lambda d: _shodashvarga_table_section(d),
    "kp_system":        lambda d: _kp_section(d),
    "friendship":       lambda d: _friendship_section(d),
    "shadbala":         lambda d: _shadbala_section(d),
    "western_aspects":  lambda d: _western_aspects_section(d),
    "graha_drishti":    lambda d: _graha_drishti_section(d),
    "planet_positions": lambda d: _planet_positions(d),
    "numerology":       lambda d: _numerology_section(d),
    "varshaphal":       lambda d: _varshaphal_section(d),
    "lal_kitab_calc":   lambda d: _lal_kitab_calculation_section(d),
    "lal_kitab":        lambda d: _lal_kitab_section(d),
    "remedies":         lambda d: _remedies_section(d),
}

# Default order — Astrosage page-2 layout (basic details → avkahada →
# favourable → ghatak) followed by the rest of the report.
_DEFAULT_SECTION_ORDER = [
    "summary_grid",
    "at_a_glance",
    "birth_chart",
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
    "jaimini",
    "mahadasha_phal",
    "antardasha",
    "pratyantar",
    "yogini_dasha",
    "char_dasha",
    "divisional",
    "shodashvarga",
    "kp_system",
    "friendship",
    "shadbala",
    "western_aspects",
    "graha_drishti",
    "planet_positions",
    "numerology",
    "varshaphal",
    "lal_kitab_calc",
    "lal_kitab",
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

    _name = d.get("name", "")
    parts = [
        _css(name=_name, user_timezone=d.get("user_timezone", "Asia/Kolkata")),
        _running_header(_name),
        _cover(d),
    ]
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


def _css(name: str = "", user_timezone: str = "Asia/Kolkata") -> str:
    from zoneinfo import ZoneInfo
    try:
        local_tz = ZoneInfo(user_timezone)
    except Exception:
        local_tz = ZoneInfo("Asia/Kolkata")
    generated = datetime.now(local_tz).strftime("%d/%m/%Y %I:%M:%S %p")
    return f"""<style>
    @page {{ size: A4; margin: 13mm 12mm 16mm 12mm;
        @top-center {{ content: element(pageheader); width: 100%; }}
        @bottom-center {{ content: "https://vedicjivan.nandishdave.world, E-mail: vedic.jivan33@gmail.com, Phone: +91 98242 92212, Printing Date: {generated}" "\\A" "Page No. " counter(page); white-space: pre-wrap; text-align: center; font-size: 8pt; color: {BRAND}; font-weight: bold; border-top: 0.75pt solid #c9c9c9; box-sizing: border-box; padding: 4pt 12mm 0; margin: 0 -12mm; }}
    }}
    @page :first {{ @top-center {{ content: none; }} @bottom-center {{ content: none; border-top: none; }} }}
    /* Running header element (pulled from flow into @top-center on every page
       except :first) — a single full-width row so the underline is continuous. */
    .run-header {{ position: running(pageheader); display: flex; justify-content: space-between;
        align-items: flex-end; box-sizing: border-box; width: calc(100% + 24mm); margin-left: -12mm;
        padding: 0 12mm 3pt; font-size: 8pt; font-weight: bold;
        border-bottom: 0.75pt solid #c9c9c9; }}
    .run-header .rh-name {{ color: #555; }}
    .run-header .rh-url {{ color: {BRAND}; }}
    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333; line-height: 1.35; font-size: 10pt; }}
    h1 {{ color: {BRAND}; text-align: center; font-size: 20pt; margin: 0 0 4px; }}
    h2 {{ color: {BRAND}; font-size: 14pt; border-bottom: 2px solid {BRAND}; padding-bottom: 3px; margin: 16px 0 8px; page-break-after: avoid; }}
    h3 {{ color: #555; font-size: 12pt; margin: 10px 0 4px; page-break-after: avoid; }}
    table {{ width: 100%; border-collapse: collapse; margin: 6px 0 10px; }}
    th {{ background: {BRAND}; color: white; padding: 4px 8px; text-align: left; font-size: 9.5pt; }}
    td {{ padding: 4px 8px; border-bottom: 1px solid #e5e5e5; font-size: 9.5pt; }}
    tr:nth-child(even) {{ background: #f9f7ff; }}
    .cover {{ text-align: center; padding: 30px 0 40px; page-break-after: always; }}
    /* Density: let sections flow across pages to fill whitespace; keep only
       small atomic blocks (charts) and individual table rows unbroken. */
    .chart-block {{ page-break-inside: avoid; }}
    tr {{ page-break-inside: avoid; }}
    .two-col {{ display: flex; gap: 16px; }}
    .two-col > div {{ flex: 1; }}
    .remedy {{ background: #f3f0ff; border-left: 3px solid {BRAND}; padding: 6px 10px; margin: 4px 0; font-size: 9.5pt; }}
    .manglik-yes {{ background: #fef2f2; border: 1px solid #f87171; padding: 9px; border-radius: 6px; }}
    .manglik-no {{ background: #f0fdf4; border: 1px solid #4ade80; padding: 9px; border-radius: 6px; }}
    .phase-card {{ background: #f9f7ff; border-left: 4px solid {BRAND}; padding: 8px 12px; margin: 6px 0; }}
    .footer {{ text-align: center; color: #999; font-size: 9pt; margin-top: 24px; border-top: 1px solid #eee; padding-top: 8px; }}
    /* Density: section separators flow continuously to fill each page instead
       of forcing a fresh page per section. `.page-break` is now a SOFT spacer
       (the report has ~43 of these). To make a specific section start on a new
       page, change that one div's class to `force-break`. Headings still carry
       `page-break-after: avoid` so a heading never orphans at a page bottom. */
    .page-break {{ height: 6px; }}
    .force-break {{ page-break-before: always; }}
    p {{ margin: 4px 0; }}
    </style>"""


def _running_header(name: str) -> str:
    """Full-width running header (name left, URL right) pulled into @top-center
    on pages 2+. Kept as a SINGLE element so its underline is one continuous,
    full-bleed line (margin-box borders left a gap in the middle)."""
    import html as _html
    return (
        '<div class="run-header">'
        f'<span class="rh-name">{_html.escape(name)}</span>'
        '<span class="rh-url">Get free chart (kundli) at https://vedicjivan.nandishdave.world</span>'
        '</div>'
    )


def _cover(d: dict) -> str:
    """Logo-only title page: just the brand logo, as large as possible and
    centred on the page. All birth data and charts live inside the report
    (the D1/D9 charts on the at-a-glance page, full birth details in the
    overview section), so page 1 is a clean brand cover."""
    # Flex-centre vertically within the A4 content box (~268mm ≈ 1013px tall);
    # min-height kept just under that so it never spills onto a 2nd page.
    return f"""
    <div class="cover" style="padding:0; display:flex; flex-direction:column;
         align-items:center; justify-content:center; min-height:990px;">
        <img src="{LOGO_URL}" alt="VedicJivan" style="width:92%; max-width:660px;" />
        <div style="margin-top:46px;">
            <span style="display:inline-block; background:#f0fdf4; border:1px solid #86efac;
                border-radius:24px; padding:11px 30px;">
                <svg width="544" height="30" viewBox="0 0 362 20" xmlns="http://www.w3.org/2000/svg" style="vertical-align:middle;">
                    <defs>
                        <linearGradient id="vjbadge" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="262" y2="0">
                            <stop offset="0" stop-color="{BRAND}"/>
                            <stop offset="1" stop-color="#d4a017"/>
                        </linearGradient>
                    </defs>
                    <text x="0" y="15" font-family="'Segoe UI', Tahoma, sans-serif" font-size="13" font-weight="bold"><tspan fill="url(#vjbadge)">Comprehensive Report &#160;·&#160; Worth </tspan><tspan fill="url(#vjbadge)">&#8377;999</tspan><tspan fill="url(#vjbadge)"> &#8212; </tspan><tspan fill="#15803d">FREE</tspan></text>
                    <line x1="240" y1="10.5" x2="275" y2="10.5" stroke="#6b7280" stroke-width="1.6" stroke-linecap="round"/>
                </svg>
            </span>
        </div>
    </div>"""


def _footer() -> str:
    return f"""
    <div class="footer">
        <p>This report has been generated based on Vedic astrology calculations using Lahiri Ayanamsa.</p>
        <p>For personalised guidance, book a consultation at <strong style="color:{BRAND};">vedicjivan.nandishdave.world</strong></p>
        <p>&copy; {datetime.now().year} VedicJivan. All rights reserved.</p>
    </div>"""
