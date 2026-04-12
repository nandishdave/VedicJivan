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
    monkeypatch.setattr(kundli_pdf, "_css", lambda: "<css />")
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


def test_avkahada_and_ghatak_present_in_default_order(stub_section_builders, chart_data):
    """Astrosage page-2 alignment: avkahada and ghatak are now top-level sections."""
    html = _build_html(chart_data)
    assert "<avkahada />" in html
    assert "<ghatak />" in html
    # Page-2 layout: basic_details → avkahada → favourable → ghatak
    assert html.index("<basic_details />") < html.index("<avkahada />")
    assert html.index("<avkahada />") < html.index("<favourable />")
    assert html.index("<favourable />") < html.index("<ghatak />")


def test_friendship_section_present_before_shadbala(stub_section_builders, chart_data):
    """Astrosage page-49 alignment: friendship table sits between divisional and shadbala."""
    html = _build_html(chart_data)
    assert "<friendship />" in html
    assert html.index("<divisional />") < html.index("<friendship />")
    assert html.index("<friendship />") < html.index("<shadbala />")


def test_disabled_section_excluded(stub_section_builders, chart_data):
    """A section with enabled=False is dropped from the rendered HTML."""
    sections = [
        {"id": "yogas", "enabled": False},
        {"id": "doshas", "enabled": True},
    ]
    html = _build_html(chart_data, sections)
    assert "<doshas />" in html
    assert "<yogas />" not in html


def test_custom_order_respected(stub_section_builders, chart_data):
    """The order in the section list determines the order in the HTML."""
    sections = [
        {"id": "remedies", "enabled": True},
        {"id": "birth_chart", "enabled": True},
    ]
    html = _build_html(chart_data, sections)
    assert html.index("<remedies />") < html.index("<birth_chart />")


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
