"""Tests for the Kundli PDF section dispatcher (Commit 0).

The PDF builder (`_build_html`) used to hardcode the section list. It now
reads an optional ordered list of `{id, enabled, ...}` dicts from the admin
report-section toggles in MongoDB. These tests cover:

1. Default behaviour (no toggles passed) is byte-identical to the legacy
   hardcoded order.
2. Disabled sections are excluded.
3. Custom ordering is respected.
4. Unknown section IDs are silently skipped (forward-compat).
5. The MongoDB merge logic in `load_report_sections` returns defaults on a
   missing doc, applies overrides on a present doc, and surfaces new
   defaults that were added after the doc was saved.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from app.models.availability import DEFAULT_REPORT_SECTIONS, ReportSection
from app.services import kundli_pdf
from app.services.kundli_pdf import _build_html, _DEFAULT_SECTION_ORDER
from app.services.report_sections import load_report_sections


# ── Helpers ────────────────────────────────────────────────────────────────


@pytest.fixture
def stub_section_builders(monkeypatch):
    """Replace SECTION_BUILDERS with stubs that emit `<id />` tags.

    This isolates the dispatcher from real chart data and from WeasyPrint.
    """
    stubs = {sid: (lambda d, sid=sid: f"<{sid} />") for sid in _DEFAULT_SECTION_ORDER}
    monkeypatch.setattr(kundli_pdf, "SECTION_BUILDERS", stubs)
    # The cover/footer/css helpers also access chart_data — stub them too.
    # `_css` takes (name, user_timezone) kwargs; absorb anything to avoid
    # signature drift between this stub and the real renderer.
    monkeypatch.setattr(kundli_pdf, "_css", lambda **_kw: "<css />")
    monkeypatch.setattr(kundli_pdf, "_cover", lambda d: "<cover />")
    monkeypatch.setattr(kundli_pdf, "_footer", lambda: "<footer />")
    return stubs


@pytest.fixture
def chart_data():
    return {"name": "Test User"}


# ── Dispatcher tests ───────────────────────────────────────────────────────


def test_default_order_byte_identical(stub_section_builders, chart_data):
    """No `sections` argument → default order, body identical to explicit list."""
    explicit = [
        {"id": sid, "enabled": True} for sid in _DEFAULT_SECTION_ORDER
    ]
    assert _build_html(chart_data) == _build_html(chart_data, explicit)


def test_default_order_includes_all_known_sections(stub_section_builders, chart_data):
    """Default order produces every section from _DEFAULT_SECTION_ORDER."""
    html = _build_html(chart_data)
    body_tags = sum(1 for sid in _DEFAULT_SECTION_ORDER if f"<{sid} />" in html)
    assert body_tags == len(_DEFAULT_SECTION_ORDER)
    assert "<cover />" in html
    assert "<footer />" in html


def test_summary_grid_renders_before_at_a_glance(stub_section_builders, chart_data):
    """Page-2 grid (basic_details + avkahada + favourable + ghatak in one block)
    appears before the dense at-a-glance summary. The standalone avkahada /
    favourable / ghatak / basic_details sections were folded into summary_grid."""
    html = _build_html(chart_data)
    assert "<summary_grid />" in html
    assert "<at_a_glance />" in html
    assert html.index("<summary_grid />") < html.index("<at_a_glance />")
    # Folded sections no longer render as standalone tags
    for folded in ("avkahada", "favourable", "ghatak", "basic_details"):
        assert f"<{folded} />" not in html


def test_friendship_section_present_before_shadbala(stub_section_builders, chart_data):
    """Astrosage page-49 alignment: friendship table sits between divisional and shadbala."""
    html = _build_html(chart_data)
    assert "<friendship />" in html
    assert html.index("<divisional />") < html.index("<friendship />")
    assert html.index("<friendship />") < html.index("<shadbala />")


# ── New sections introduced in commit 721d233 ──────────────────────────────


def test_new_kundli_sections_registered(stub_section_builders, chart_data):
    """All 6 new sections (at_a_glance, jaimini, char_dasha, varshaphal,
    lal_kitab_calc, lal_kitab) must be both in the default order and have
    a SECTION_BUILDERS entry."""
    new_sections = [
        "at_a_glance", "jaimini", "char_dasha",
        "varshaphal", "lal_kitab_calc", "lal_kitab",
    ]
    html = _build_html(chart_data)
    for sid in new_sections:
        assert sid in _DEFAULT_SECTION_ORDER, f"{sid} missing from default order"
        assert f"<{sid} />" in html, f"{sid} not rendered"


def test_jaimini_renders_before_dasha_sections(stub_section_builders, chart_data):
    """User-confirmed ordering: Jaimini (Karakas + Karakamsa + Swamsa) sits
    before the dasha block so dasha context inherits from soul-purpose chart."""
    html = _build_html(chart_data)
    assert html.index("<jaimini />") < html.index("<mahadasha_phal />")
    assert html.index("<jaimini />") < html.index("<antardasha />")


def test_char_dasha_renders_after_yogini_dasha(stub_section_builders, chart_data):
    """Char Dasha (Jaimini sign-based) sits after Yogini in the dasha block."""
    html = _build_html(chart_data)
    assert html.index("<yogini_dasha />") < html.index("<char_dasha />")


def test_lal_kitab_calc_renders_before_lal_kitab_predictions(stub_section_builders, chart_data):
    """Computation page (chart + dasha) appears before the predictions narrative."""
    html = _build_html(chart_data)
    assert html.index("<lal_kitab_calc />") < html.index("<lal_kitab />")


def test_lal_kitab_predictions_render_before_remedies(stub_section_builders, chart_data):
    """Lal Kitab predictions come before the gemstone/remedies section."""
    html = _build_html(chart_data)
    assert html.index("<lal_kitab />") < html.index("<remedies />")


def test_at_a_glance_is_in_top_three_sections(stub_section_builders, chart_data):
    """At-a-glance summary page sits near the top of the report (after the
    summary_grid 2×2 page-2 block). We check it comes before the heavy
    narrative sections rather than asserting a strict slot."""
    html = _build_html(chart_data)
    assert html.index("<at_a_glance />") < html.index("<planet_consideration />")
    assert html.index("<at_a_glance />") < html.index("<yogas />")
    assert html.index("<at_a_glance />") < html.index("<doshas />")


def test_disabled_section_excluded(stub_section_builders, chart_data):
    """A section with enabled=False is dropped from the rendered HTML."""
    sections = [
        {"id": "yogas", "enabled": False},
        {"id": "doshas", "enabled": True},
    ]
    html = _build_html(chart_data, sections)
    assert "<doshas />" in html
    assert "<yogas />" not in html


def test_default_order_always_used_regardless_of_input_order(stub_section_builders, chart_data):
    """Even when sections are passed in a different order, the rendering follows
    _DEFAULT_SECTION_ORDER so stale MongoDB order values can't scramble the layout."""
    sections = [
        {"id": "remedies", "enabled": True},
        {"id": "birth_chart", "enabled": True},
    ]
    html = _build_html(chart_data, sections)
    # birth_chart comes before remedies in _DEFAULT_SECTION_ORDER
    assert html.index("<birth_chart />") < html.index("<remedies />")


def test_unknown_section_id_skipped(stub_section_builders, chart_data):
    """An ID with no registered builder is silently skipped (forward-compat)."""
    sections = [
        {"id": "future_v2_section", "enabled": True},
        {"id": "yogas", "enabled": True},
    ]
    html = _build_html(chart_data, sections)
    assert "<yogas />" in html
    assert "future_v2_section" not in html


def test_empty_section_list_renders_only_chrome(stub_section_builders, chart_data):
    """An empty enabled list still produces a valid document with cover + footer."""
    html = _build_html(chart_data, [])
    assert "<cover />" in html
    assert "<footer />" in html
    for sid in _DEFAULT_SECTION_ORDER:
        assert f"<{sid} />" not in html


# ── load_report_sections (MongoDB merge) tests ─────────────────────────────


@pytest.mark.asyncio
async def test_load_report_sections_returns_defaults_when_no_doc(mock_db):
    """No saved doc → return DEFAULT_REPORT_SECTIONS verbatim."""
    mock_db.settings.find_one = AsyncMock(return_value=None)
    result = await load_report_sections()
    assert result == list(DEFAULT_REPORT_SECTIONS)


@pytest.mark.asyncio
async def test_load_report_sections_applies_overrides(mock_db):
    """A saved doc overrides defaults for matching IDs only."""
    saved = {
        "_id": "report_sections",
        "sections": [
            {
                "id": "yogas",
                "label": "Custom Yogas Label",
                "description": "overridden",
                "is_paid": True,
                "enabled": False,
                "order": 7,
            }
        ],
    }
    mock_db.settings.find_one = AsyncMock(return_value=saved)
    result = await load_report_sections()
    yogas = next(s for s in result if s.id == "yogas")
    assert yogas.label == "Custom Yogas Label"
    assert yogas.is_paid is True
    assert yogas.enabled is False
    # Other sections still come from defaults
    birth_chart = next(s for s in result if s.id == "birth_chart")
    assert birth_chart.label == "Birth Chart"


@pytest.mark.asyncio
async def test_load_report_sections_surfaces_new_defaults(mock_db):
    """A section added to defaults after the doc was saved still appears."""
    saved = {
        "_id": "report_sections",
        "sections": [
            {
                "id": "yogas",
                "label": "Yogas",
                "description": "x",
                "is_paid": False,
                "enabled": True,
                "order": 7,
            }
        ],
    }
    mock_db.settings.find_one = AsyncMock(return_value=saved)
    result = await load_report_sections()
    result_ids = {s.id for s in result}
    default_ids = {s.id for s in DEFAULT_REPORT_SECTIONS}
    assert default_ids.issubset(result_ids)


@pytest.mark.asyncio
async def test_load_report_sections_sorted_by_order(mock_db):
    """Result is always sorted ascending by `order`."""
    mock_db.settings.find_one = AsyncMock(return_value=None)
    result = await load_report_sections()
    orders = [s.order for s in result]
    assert orders == sorted(orders)
