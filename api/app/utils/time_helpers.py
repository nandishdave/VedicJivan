"""Time-of-day arithmetic shared by bookings + availability routers.

Two slightly different `_time_to_minutes` + `_overlaps` implementations
existed in `routers/bookings.py` and `routers/availability.py`. This module
is the single source of truth.

Time strings are always 24-hour `HH:MM`. We never deal with calendar dates
here — the caller is responsible for ensuring both inputs refer to the same
day.
"""

from __future__ import annotations


def time_to_minutes(time_hhmm: str) -> int:
    """Convert "HH:MM" to minutes since midnight.

    Raises:
        ValueError: if the string isn't parseable as HH:MM.
    """
    hours_str, minutes_str = time_hhmm.split(":")
    return int(hours_str) * 60 + int(minutes_str)


def ranges_overlap(
    start1: int | str,
    end1: int | str,
    start2: int | str,
    end2: int | str,
) -> bool:
    """True if two [start, end) minute-ranges intersect.

    Accepts either int (already minutes since midnight) or "HH:MM" strings —
    matches both legacy call sites without forcing the caller to convert.

    Touching boundaries (e.g., 10:00-10:30 and 10:30-11:00) do NOT overlap;
    the second slot starts exactly when the first ends.
    """
    s1 = time_to_minutes(start1) if isinstance(start1, str) else start1
    e1 = time_to_minutes(end1) if isinstance(end1, str) else end1
    s2 = time_to_minutes(start2) if isinstance(start2, str) else start2
    e2 = time_to_minutes(end2) if isinstance(end2, str) else end2
    return s1 < e2 and s2 < e1
