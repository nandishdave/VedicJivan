"""HTML → PDF renderer abstraction for the Kundli report.

`generate_pdf` in `kundli_pdf.py` builds a single HTML string. This module
turns that HTML into PDF bytes. We support two backends:

  * `WeasyPrintRenderer` — pure-Python CSS engine. Fast, light. Used in
    local dev, in the API container, and in unit tests because no browser
    binary is needed.
  * `PlaywrightRenderer` — headless Chromium. Higher fidelity (real CSS
    grid, modern font rendering, web fonts), heavier (~700 MB - 1.5 GB
    per render). Used by the kundli Lambda worker.

Selected at process start via `settings.PDF_RENDERER`. Override per
container (e.g. `PDF_RENDERER=playwright` on the Lambda task).
"""

from __future__ import annotations

import asyncio
import threading
from typing import Protocol

from app.config import settings
from app.infrastructure.logging import get_logger

logger = get_logger(__name__)


class PdfRenderer(Protocol):
    def render(self, html: str) -> bytes: ...


# ── WeasyPrint (default — local + API container) ─────────────────────────────


class WeasyPrintRenderer:
    """Pure-Python renderer. Byte-identical to the pre-abstraction output."""

    def render(self, html: str) -> bytes:
        # Local import keeps the WeasyPrint native libs out of the import
        # path on Lambda, where Pango/Cairo aren't installed.
        from weasyprint import HTML

        return HTML(string=html).write_pdf()


# ── Playwright (Lambda worker) ───────────────────────────────────────────────


class PlaywrightRenderer:
    """Headless Chromium via Playwright. Reuses one browser per process.

    The first render after import pays the browser-launch cost (~1-3 s on
    Lambda after Chromium is on a warm filesystem cache; ~10-20 s on a
    cold start). Every subsequent render in the same process opens a new
    *page* in the existing browser — sub-second.

    Sync wrapper: Playwright has both async and sync APIs. We use the sync
    API and dispatch from a single dedicated thread because boto-style
    `to_thread` reuse and the nested event-loop semantics in Lambda
    sometimes collide with Playwright's own asyncio loop. The dedicated
    thread keeps the browser instance reachable across invocations.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._playwright = None
        self._browser = None

    def _ensure_browser(self):
        if self._browser is not None:
            return
        # Local import — Playwright is only installed in the Lambda image.
        from playwright.sync_api import sync_playwright

        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--single-process",
            ]
        )
        logger.info("Playwright Chromium browser launched")

    def render(self, html: str) -> bytes:
        with self._lock:
            self._ensure_browser()
            page = self._browser.new_page()
            try:
                page.set_content(html, wait_until="networkidle")
                return page.pdf(
                    format="A4",
                    margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
                    print_background=True,
                )
            finally:
                page.close()


# ── Factory ──────────────────────────────────────────────────────────────────

_renderer_singleton: PdfRenderer | None = None


def get_renderer() -> PdfRenderer:
    """Return the process-wide renderer instance.

    Lazy + cached so importing this module in tests doesn't pull
    Playwright (which would fail without the browser binary). Reading
    `settings.PDF_RENDERER` at first call honours env-var overrides set
    after process start (e.g. by tests via `monkeypatch.setenv`).
    """
    global _renderer_singleton
    if _renderer_singleton is None:
        backend = (settings.PDF_RENDERER or "weasyprint").lower()
        if backend == "playwright":
            _renderer_singleton = PlaywrightRenderer()
        elif backend == "weasyprint":
            _renderer_singleton = WeasyPrintRenderer()
        else:
            raise ValueError(
                f"Unknown PDF_RENDERER {backend!r}; "
                "expected 'weasyprint' or 'playwright'"
            )
    return _renderer_singleton


def reset_renderer_for_tests() -> None:
    """Drop the cached renderer. Tests call this between env-var changes."""
    global _renderer_singleton
    _renderer_singleton = None
