"""Request model for the Unshakable Chart Finder (week-scale)."""
from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class UnshakableRequest(BaseModel):
    start_date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    # Week-scale for the Lambda path (a week funnel fits the 300s timeout).
    # Month/year will move to an on-demand ECS/Batch box later.
    days: int = Field(default=7, ge=1, le=7)
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    place_name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    # Absolute quality bar on the 0-100 composite. Default 90 = "magical only"
    # (a fallback "best available" is returned when nothing clears it).
    bar: float = Field(default=90.0, ge=0, le=100)
