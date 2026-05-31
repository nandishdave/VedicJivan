"""Nakshatra (lunar mansion) computation from Moon's sidereal longitude.

Pure: no I/O. Extracted from the legacy `_core` monolith.
"""

from __future__ import annotations

from ._core import NAKSHATRA_LORDS, NAKSHATRA_NAMES


def calc_nakshatra(moon_lon: float) -> dict:
    """Calculate birth Nakshatra and Pada from Moon's sidereal longitude."""
    nak_size = 360 / 27  # 13°20' each
    pada_size = nak_size / 4
    nak_num = int(moon_lon / nak_size)  # 0–26
    pada = int((moon_lon % nak_size) / pada_size) + 1  # 1–4
    return {
        "num": nak_num,
        "name": NAKSHATRA_NAMES[nak_num],
        "lord": NAKSHATRA_LORDS[nak_num],
        "pada": pada,
        "degree_in_nak": round(moon_lon % nak_size, 4),
    }
