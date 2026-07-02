"""Request model for the Auspicious Birth-Time (Muhurta) calculator."""
from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class BirthMuhurtaRequest(BaseModel):
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    place_name: str = Field(..., min_length=1, max_length=200)
    # The full analysis is slow; we run it in the background and email the result.
    email: EmailStr
    # Optional HH:MM. If given (e.g. an already-born person), the report flags the
    # Lagna rising at that instant + takes planetary positions at that time;
    # omitted -> nothing highlighted, positions at local noon.
    time: str | None = Field(default=None, pattern=r"^\d{2}:\d{2}$")
    # Optional aspect keys (e.g. ["health", "wealth"]) to re-rank windows toward
    # what the family values most. Empty/omitted -> rank by overall Lagna strength.
    priorities: list[str] | None = Field(default=None, max_length=12)
    # Optionally blend the validated worldly-potential score (~0.63 fame tilt) into
    # the ranking: rank = 0.6*base + 0.4*worldly. Off by default. Worldly is always
    # displayed regardless; this only affects the ordering.
    optimize_prominence: bool = Field(default=False)
