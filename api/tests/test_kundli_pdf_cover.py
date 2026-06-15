"""Regression guards for the Kundli PDF cover + page header/footer.

These lock in deliberate cosmetic decisions that have been silently overwritten
by past redesigns. If a future change reverts them, these tests fail instead of
the change shipping unnoticed:

  - Page 1 is a clean LOGO-ONLY branding page (no chart, no birth-details table,
    no title text, no header/footer).
  - The "Worth ₹999 — FREE" badge: gradient text, struck price, green FREE.
  - Pages 2+ have a single full-width (edge-to-edge) header rule + footer rule.
"""
from app.services import kundli_pdf
from app.services.kundli_pdf import _cover, _css, _running_header
from app.services.pdf_sections import _app_promo_banner

# The logo-only cover ignores birth fields, but pass a realistic dict so the
# guard still holds if the cover ever starts reading them again.
_D = {"name": "Test User", "dob": "1990-01-01", "place_name": "Test City"}


def test_cover_is_logo_only_branding_page():
    html = _cover(_D)
    # Brand logo must be present and large.
    assert 'alt="VedicJivan"' in html
    assert kundli_pdf.LOGO_URL in html
    # The "FREE" offer badge with gradient + struck price.
    assert 'id="vjbadge"' in html        # purple->gold gradient definition
    assert "FREE" in html
    assert "999" in html
    assert "<line" in html               # explicit strike-through over the price
    # MUST NOT re-introduce the elements that were deliberately removed.
    assert "Lagna Chart" not in html     # no chart label on the cover
    assert "Date of Birth" not in html   # no birth-details rows
    assert "Time of Birth" not in html
    assert "Nakshatra" not in html
    assert "Vedic Birth Chart" not in html  # no title text block
    # Only the small badge SVG belongs on the cover — never a D1 chart SVG.
    assert html.count("<svg") == 1


def test_cover_does_not_embed_page_header():
    # The running header belongs in the page margin, not the cover body.
    assert "run-header" not in _cover(_D)


def test_header_is_single_full_width_running_element():
    css = _css(name="Test User")
    # One running element -> one continuous underline (not segmented margin boxes).
    assert "running(pageheader)" in css
    assert "element(pageheader)" in css
    # Separator rules exist for header (bottom) and footer (top).
    assert "border-bottom: 0.75pt solid" in css
    assert "border-top: 0.75pt solid" in css
    # Both rules bleed past the side margins (edge-to-edge).
    assert "calc(100% + 24mm)" in css    # header bleed
    assert "margin: 0 -12mm" in css      # footer bleed


def test_first_page_has_no_header_or_footer():
    css = _css(name="Test User")
    assert "@page :first" in css
    first_block = css[css.index("@page :first"):css.index("@page :first") + 220]
    # Both the header (@top-center) and footer (@bottom-center) are blanked.
    assert first_block.count("content: none") >= 2


def test_overview_page_has_consultation_promo_banner():
    # The overview page (page 2) carries a clickable VedicJivan consultation
    # promo in the space Astrosage uses for ads — guard against it being dropped.
    banner = _app_promo_banner()
    assert "Book a Consultation" in banner
    assert 'href="https://vedicjivan.nandishdave.world/services"' in banner  # clickable CTA
    assert "Consultations" in banner


def test_running_header_has_name_left_url_right_and_escapes_name():
    h = _running_header("Ravi & <Co>")
    assert 'class="run-header"' in h
    assert "Ravi &amp; &lt;Co&gt;" in h  # user-supplied name is HTML-escaped
    assert "vedicjivan.nandishdave.world" in h
