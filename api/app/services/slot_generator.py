"""Pure slot-generation helper.

Used by the availability use case. No DB, no I/O — just date math.
"""

from __future__ import annotations

from datetime import datetime, timedelta

# TODO Phase 5: move to settings.SLOT_DURATION_MINUTES.
SLOT_DURATION_MINUTES = 30


def generate_30min_slots(
    open_time: str = "00:00",
    close_time: str = "24:00",
) -> list[dict]:
    """Generate 30-minute slot windows between open_time and close_time."""
    slots: list[dict] = []
    oh, om = map(int, open_time.split(":"))
    current = datetime(2000, 1, 1, oh, om)

    ch, cm = map(int, close_time.split(":"))
    end = (
        datetime(2000, 1, 2, 0, 0)
        if (ch == 24 and cm == 0)
        else datetime(2000, 1, 1, ch, cm)
    )

    delta = timedelta(minutes=SLOT_DURATION_MINUTES)
    while current + delta <= end:
        slot_end = current + delta
        slots.append(
            {
                "start": current.strftime("%H:%M"),
                "end": slot_end.strftime("%H:%M"),
            }
        )
        current = slot_end
    return slots
