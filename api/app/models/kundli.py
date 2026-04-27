"""Kundli request and storage models."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class KundliRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    gender: Literal["male", "female", "other"]
    dob: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    tob: str = Field(..., pattern=r"^\d{2}:\d{2}$")
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    place_name: str = Field(..., min_length=1, max_length=200)
    email: EmailStr
    timezone: str | None = Field(None, description="User's browser timezone e.g. 'Europe/Amsterdam', 'America/New_York'.")


class KundliInDB(BaseModel):
    name: str
    gender: str
    dob: str
    tob: str
    lat: float
    lon: float
    place_name: str
    email: str
    chart_data: dict = {}
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: Literal["pending", "generated", "failed"] = "pending"
    error: str | None = None
    # Mongo TTL field. Set on `pending` insert (expires_at = now + 24h) so
    # records that never finish processing (SQS dropped, Lambda crashed,
    # whole worker offline for a day) auto-clean. Unset by mark_generated /
    # mark_failed so completed records persist forever.
    expires_at: datetime | None = None
