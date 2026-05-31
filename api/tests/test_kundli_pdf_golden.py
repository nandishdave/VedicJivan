"""Golden / snapshot tests for the generated Kundli PDF.

Two complementary techniques:

1. **Snapshot tests (syrupy)** — pin down stable structure of the PDF: section
   header titles found on each page, page count. Run `pytest --snapshot-update`
   to regenerate when intentional. Stops silent regressions where a refactor
   accidentally drops a section or scrambles page order.

2. **Golden-value assertions** — pin down known calculation outputs that the
   renderer must show (Nandish Dave's lagna = Capricorn, Moon = Scorpio,
   nakshatra = Anuradha-pada-3). These would break if the calculator drifts
   — a far stronger signal than "output changed."

Anything that depends on `date.today()` (current dasha, Varshaphal year,
print-date footer, Sade Sati windowing) is excluded from the snapshot. Tests
focus on the natal-chart facts that never change for a fixed DOB.
"""

from __future__ import annotations

from io import BytesIO

import pytest


# ── Reference chart: Nandish Dave (1988-11-11 12:55 IST, Jetpur) ──
# Same chart used across the repo's other tests so failures map to a known fact.
NANDISH = {
    "name": "Nandish Dave",
    "gender": "male",
    "dob": "1988-11-11",
    "tob": "12:55",
    "lat": 21.7333,
    "lon": 70.6167,
    "place_name": "Jetpur, Gujarat, India",
}


@pytest.fixture(scope="module")
def chart_data():
    """Build the chart once per module — calculation is expensive (~1-2s)."""
    from app.services.kundli_calculator import build_chart
    return build_chart(**NANDISH)


@pytest.fixture(scope="module")
def free_sections():
    """The default set of free (is_paid=False, enabled=True) sections."""
    from app.models.availability import DEFAULT_REPORT_SECTIONS
    return [
        s.model_dump() for s in DEFAULT_REPORT_SECTIONS
        if s.enabled and not s.is_paid
    ]


@pytest.fixture(scope="module")
def pdf_bytes(chart_data, free_sections):
    """Render the full PDF once per module."""
    from app.services.kundli_pdf import generate_pdf
    return generate_pdf(chart_data, sections=free_sections)


@pytest.fixture(scope="module")
def pdf_pages(pdf_bytes):
    """Extracted text per page — used by every text-content assertion."""
    import pdfplumber
    pages = []
    with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text() or "")
    return pages


# ── Smoke / structural tests ───────────────────────────────────────────────


def test_pdf_starts_with_pdf_magic_bytes(pdf_bytes):
    """A valid PDF must start with '%PDF-' (RFC 8551)."""
    assert pdf_bytes.startswith(b"%PDF-")


def test_pdf_has_at_least_ten_pages(pdf_pages):
    """The free report must produce a substantial document (sanity floor)."""
    assert len(pdf_pages) >= 10


def test_pdf_full_text_is_non_empty(pdf_pages):
    """Every page should contain at least some readable text."""
    empty_pages = [i for i, t in enumerate(pdf_pages) if not t.strip()]
    # Allow a couple of mostly-graphical pages (charts), but not many
    assert len(empty_pages) <= 3, f"Too many empty pages: {empty_pages}"


# ── Golden values: facts that never change for Nandish's DOB ───────────────


def test_pdf_shows_nandish_name(pdf_pages):
    """The user's name appears prominently (cover + header band)."""
    full = "\n".join(pdf_pages)
    assert "Nandish Dave" in full


def test_pdf_shows_capricorn_lagna_and_scorpio_moon(pdf_pages):
    """Computed at fixed DOB: Lagna=Capricorn, Moon=Scorpio (Anuradha)."""
    full = "\n".join(pdf_pages)
    assert "Capricorn" in full
    assert "Scorpio" in full
    assert "Anuradha" in full


def test_pdf_shows_birth_place_and_date(pdf_pages):
    full = "\n".join(pdf_pages)
    assert "Jetpur" in full
    # Date may render as 11-11-1988 or 11/11/1988 depending on the section
    assert any(fmt in full for fmt in ["1988", "11-11-1988", "11/11/1988"])


def test_pdf_includes_all_major_section_headers(pdf_pages):
    """Every free section must contribute its section header to the document."""
    full = "\n".join(pdf_pages)
    expected_headings = [
        "Birth Chart",
        "Nakshatra",
        "Yogas",
        "Doshas",
        "Mahadasha",
        "Antardasha",
        "Yogini",
        "Char Dasha",
        "Jaimini",
        "Lal Kitab",
        "Numerology",
        "Varshaphal",
        "Friendship",
        "Shadbala",
        "Remedies",
    ]
    missing = [h for h in expected_headings if h not in full]
    assert not missing, f"Missing section headings: {missing}"


# ── Snapshot: stable structural fingerprint ────────────────────────────────


def test_pdf_section_fingerprint(pdf_pages, snapshot):
    """Snapshot the SET of major section headings present (order-independent).

    This snapshot is intentionally narrow — we don't snapshot every word in
    the PDF (that would break on every dasha date refresh). We only pin the
    *structure*: which sections rendered. To intentionally accept a structure
    change run: `pytest --snapshot-update`.
    """
    candidate_headings = [
        "Cover",
        "Basic Details",
        "Avkahada Chakra",
        "Favourable Points",
        "Ghatak",
        "At-a-Glance",
        "Birth Chart",
        "Planet Considerations",
        "Ascendant",
        "Nakshatra",
        "Character",
        "Yogas",
        "Doshas",
        "Bhava",
        "Mangal Dosha",
        "Sade Sati",
        "Gochar",
        "Mahadasha",
        "Antardasha",
        "Pratyantar",
        "Yogini",
        "Char Dasha",
        "Jaimini",
        "Divisional",
        "Shodashvarga",
        "Friendship",
        "Shadbala",
        "Aspects",
        "Graha Drishti",
        "Planet Positions",
        "Numerology",
        "Varshaphal",
        "Lal Kitab",
        "Remedies",
    ]
    full = "\n".join(pdf_pages)
    found = sorted(h for h in candidate_headings if h in full)
    assert found == snapshot
