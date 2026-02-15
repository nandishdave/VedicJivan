from pydantic import BaseModel, Field


class TimeSlot(BaseModel):
    start: str = Field(..., pattern=r"^\d{2}:\d{2}$")  # "10:00"
    end: str = Field(..., pattern=r"^\d{2}:\d{2}$")  # "11:00"
    booked: bool = False


class AvailabilityCreate(BaseModel):
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")  # "2026-02-20"
    slots: list[TimeSlot]
    is_holiday: bool = False


class AvailabilityResponse(BaseModel):
    id: str
    date: str
    slots: list[TimeSlot]
    is_holiday: bool


class BulkAvailabilityCreate(BaseModel):
    start_date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    end_date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    working_days: list[int] = Field(
        default=[0, 1, 2, 3, 4],  # Mon-Fri
        description="Day of week (0=Mon, 6=Sun)",
    )
    start_time: str = Field(default="10:00", pattern=r"^\d{2}:\d{2}$")
    end_time: str = Field(default="18:00", pattern=r"^\d{2}:\d{2}$")
    slot_duration_minutes: int = Field(default=60, ge=15, le=120)
