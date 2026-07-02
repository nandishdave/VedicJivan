"""Request model for the Unshakable Chart Finder (week-scale)."""
from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class UnshakableRequest(BaseModel):
    start_date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    # Up to a month on the Lambda (with the 900s timeout). Year -> on-demand
    # ECS box later.
    days: int = Field(default=7, ge=1, le=31)
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    place_name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    # No user-facing quality bar: every moment is ranked by its honest 0-100
    # score, and a fixed internal threshold flags the genuinely strong ones. The
    # score itself is the quality signal, so a slider only confused (the metric
    # tops out ~78, making a 0-100 bar misleading).
