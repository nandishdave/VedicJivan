"""
Template text data for Kundli report generation.
Pre-written interpretive text for each Lagna, Nakshatra, planet-in-house, etc.
Based on classical Vedic astrology texts (Brihat Parashara Hora Shastra, Phaladeepika).

Formerly a single 1895-line module; split into per-domain submodules.
Every name is re-exported here so `from app.services.kundli_data import X`
is unchanged.
"""

from .lagna import LAGNA_DATA
from .nakshatra import NAKSHATRA_DATA, NAKSHATRA_PADA_DATA
from .varshaphal import MUNTHA_HOUSE_DATA, MUDDA_DASHA_BHAV_DATA
from .houses import PLANET_IN_HOUSE, BHAVA_DATA
from .dasha import DASHA_PREDICTIONS, SADESATI_PHASES
from .transits import GHATAK, FAVOURABLE
from .lal_kitab import LAL_KITAB_DATA

__all__ = [
    "LAGNA_DATA",
    "NAKSHATRA_DATA",
    "NAKSHATRA_PADA_DATA",
    "MUNTHA_HOUSE_DATA",
    "MUDDA_DASHA_BHAV_DATA",
    "PLANET_IN_HOUSE",
    "BHAVA_DATA",
    "DASHA_PREDICTIONS",
    "SADESATI_PHASES",
    "GHATAK",
    "FAVOURABLE",
    "LAL_KITAB_DATA",
]
