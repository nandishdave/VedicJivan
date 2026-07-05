"""PDF section builders + chart helpers for the Kundli report.

Everything in here is called BY `kundli_pdf.py` (the facade) but NOT
directly patched by tests. The facade keeps `_css`, `_cover`, `_footer`
and `SECTION_BUILDERS` because tests do
`monkeypatch.setattr(kundli_pdf, "<name>", stub)` on those four — and
that pattern only works when the patched name lives in the module that
gets monkeypatched.

Shared constants (`LOGO_URL`, `BRAND`, `SIGN_ABBR`, `SIGN_NAMES`,
`SIGN_LORDS`, `PLANET_ABBR`, `_HOUSE_TEXT_POS`, `CHART_DESCRIPTIONS`) live in
the dependency-free leaf `pdf_constants`; both this module and `kundli_pdf`
import them from there, so there is no circular import between the two.

Formerly a single 2676-line module; split into ._common (imports, constants,
helpers, chart geometry) + .sections (the builders). Every name is re-exported
here so `from app.services.pdf_sections import _x` is unchanged.
"""

from app.services.pdf_sections._common import *  # noqa: F401,F403
from app.services.pdf_sections.sections import *  # noqa: F401,F403
