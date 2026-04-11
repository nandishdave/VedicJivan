"""Service for loading report-section toggles from MongoDB.

The admin can enable/disable individual report sections and toggle them
between free and paid via `/admin/settings`. This module is the single source
of truth for reading that configuration so both the admin endpoint
(routers/availability.py) and the Kundli generator (routers/kundli.py) stay
in sync.
"""

from __future__ import annotations

from app.database import get_db
from app.models.availability import DEFAULT_REPORT_SECTIONS, ReportSection


async def load_report_sections() -> list[ReportSection]:
    """Return the merged, ordered list of report sections.

    Merge strategy: defaults provide the source of truth for which sections
    exist; any section saved in the DB overrides the default for that ID;
    new sections added to DEFAULT_REPORT_SECTIONS automatically appear even
    if the saved doc predates them.
    """
    db = get_db()
    doc = await db.settings.find_one({"_id": "report_sections"})
    if not doc or not doc.get("sections"):
        return list(DEFAULT_REPORT_SECTIONS)

    saved = {s["id"]: s for s in doc["sections"]}
    merged: list[ReportSection] = []
    for default in DEFAULT_REPORT_SECTIONS:
        if default.id in saved:
            merged.append(ReportSection(**saved[default.id]))
        else:
            merged.append(default)
    return sorted(merged, key=lambda s: s.order)
