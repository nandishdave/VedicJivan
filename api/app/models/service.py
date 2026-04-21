"""Service catalogue models — what we sell and how it's priced.

The booking flow looks up `(price_inr, price_eur)` for a `(slug, duration_minutes)`
pair. A "report" service has a single duration entry with `duration_minutes=0`
and is charged the same regardless of how the booking was constructed.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


class ServiceDuration(BaseModel):
    duration_minutes: int = Field(
        ...,
        ge=0,
        le=600,
        description="0 = report (single price, any duration).",
    )
    price_inr: int = Field(..., ge=0)
    price_eur: int = Field(..., ge=0)


class Service(BaseModel):
    """Public service definition — admin-editable."""

    slug: str = Field(..., min_length=1, max_length=100)
    title: Optional[str] = Field(
        None,
        description=(
            "Optional human title. Bookings still pass a `service_title` "
            "string at create time so legacy display stays unchanged."
        ),
    )
    durations: list[ServiceDuration] = Field(..., min_length=1)


class ServiceInDB(Service):
    """Persisted form — adds bookkeeping fields."""

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class ServiceResponse(Service):
    """API-shaped response — same fields as Service for now."""
