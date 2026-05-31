"""Vedic astrology chart calculator — package facade.

The implementation lives in `_core` (legacy monolith) and is being
incrementally extracted into thematic submodules. The public surface
is preserved here so every existing
`from app.services.kundli_calculator import X` keeps working.

Once a function/constant is moved out of `_core` to a dedicated module,
this `__init__.py` re-exports it from the new home; downstream callers
don't need to know.
"""

from __future__ import annotations

# Wildcard re-export of public names from the legacy core.
from ._core import *  # noqa: F401, F403

# Re-export underscore-prefixed names that tests / other modules import
# directly. Wildcard imports skip names starting with `_`, so these have
# to be listed explicitly.
from ._core import (  # noqa: F401
    _VIMSHOTTARI_DAYS_PER_YEAR,
    _birth_datetime,
    _calc_baladi,
    _calc_jagradadi,
    _MOVABLE_KARANAS,
)
