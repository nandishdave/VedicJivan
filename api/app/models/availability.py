from pydantic import BaseModel, Field


class UnavailabilityCreate(BaseModel):
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    start_time: str | None = Field(None, pattern=r"^\d{2}:\d{2}$")
    end_time: str | None = Field(None, pattern=r"^\d{2}:\d{2}$")
    is_holiday: bool = False
    reason: str = ""


class UnavailabilityResponse(BaseModel):
    id: str
    date: str
    start_time: str | None = None
    end_time: str | None = None
    is_holiday: bool
    reason: str = ""


class AvailableSlot(BaseModel):
    start: str
    end: str
