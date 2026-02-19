"""Shared business hours settings accessor."""

from app.database import get_db
from app.models.availability import BusinessHoursSettings, DayHours

DEFAULT_SETTINGS = BusinessHoursSettings()


async def get_business_hours() -> BusinessHoursSettings:
    """Load business hours from DB, or return defaults if none exist."""
    db = get_db()
    doc = await db.settings.find_one({"_id": "business_hours"})
    if not doc:
        return DEFAULT_SETTINGS
    return BusinessHoursSettings(
        timezone=doc.get("timezone", "Asia/Kolkata"),
        weekly_hours=[DayHours(**d) for d in doc.get("weekly_hours", [])],
    )
