"""Tests for the renderer dispatch in `kundli_pdf_renderer`.

We don't test that WeasyPrint or Playwright actually render correctly —
that's covered by the snapshot test (`test_kundli_pdf_golden`) and by
real-Chromium runs in the Lambda smoke test. Here we only verify that
`get_renderer()` returns the right backend for each `PDF_RENDERER`
value, and that the cache doesn't leak across tests.
"""

from __future__ import annotations

from importlib import reload

import pytest


@pytest.fixture(autouse=True)
def reset_renderer_singleton():
    """Each test gets a fresh singleton — no cross-test pollution."""
    from app.services import kundli_pdf_renderer

    kundli_pdf_renderer.reset_renderer_for_tests()
    yield
    kundli_pdf_renderer.reset_renderer_for_tests()


def test_default_renderer_is_weasyprint(monkeypatch):
    monkeypatch.setattr("app.services.kundli_pdf_renderer.settings.PDF_RENDERER", "")
    from app.services.kundli_pdf_renderer import WeasyPrintRenderer, get_renderer

    assert isinstance(get_renderer(), WeasyPrintRenderer)


def test_explicit_weasyprint(monkeypatch):
    monkeypatch.setattr(
        "app.services.kundli_pdf_renderer.settings.PDF_RENDERER", "weasyprint"
    )
    from app.services.kundli_pdf_renderer import WeasyPrintRenderer, get_renderer

    assert isinstance(get_renderer(), WeasyPrintRenderer)


def test_playwright_selection(monkeypatch):
    """Playwright renderer is constructed lazily — no browser launched yet."""
    monkeypatch.setattr(
        "app.services.kundli_pdf_renderer.settings.PDF_RENDERER", "playwright"
    )
    from app.services.kundli_pdf_renderer import PlaywrightRenderer, get_renderer

    renderer = get_renderer()
    assert isinstance(renderer, PlaywrightRenderer)
    assert renderer._browser is None  # lazy — not started until first render


def test_unknown_backend_raises(monkeypatch):
    monkeypatch.setattr(
        "app.services.kundli_pdf_renderer.settings.PDF_RENDERER", "foo"
    )
    from app.services.kundli_pdf_renderer import get_renderer

    with pytest.raises(ValueError, match="Unknown PDF_RENDERER"):
        get_renderer()


def test_get_renderer_caches_instance(monkeypatch):
    monkeypatch.setattr(
        "app.services.kundli_pdf_renderer.settings.PDF_RENDERER", "weasyprint"
    )
    from app.services.kundli_pdf_renderer import get_renderer

    assert get_renderer() is get_renderer()


def test_weasyprint_renderer_actually_renders():
    """Smoke test: WeasyPrint accepts our HTML and returns PDF bytes.

    Catches missing native libs in the test image and any signature drift.
    """
    from app.services.kundli_pdf_renderer import WeasyPrintRenderer

    pdf = WeasyPrintRenderer().render("<html><body><h1>hi</h1></body></html>")
    assert isinstance(pdf, bytes)
    assert pdf.startswith(b"%PDF")
