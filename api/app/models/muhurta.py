"""Request model for the Auspicious Birth-Time (Muhurta) calculator."""
from __future__ import annotations

from pydantic import BaseModel, Field


class BirthMuhurtaRequest(BaseModel):
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    place_name: str = Field(..., min_length=1, max_length=200)
    # Optional aspect keys (e.g. ["health", "wealth"]) to re-rank windows toward
    # what the family values most. Empty/omitted -> rank by overall Lagna strength.
    priorities: list[str] | None = Field(default=None, max_length=12)
