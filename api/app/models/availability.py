from pydantic import BaseModel, Field, field_validator


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


# ── Business Hours Settings ──


class DayHours(BaseModel):
    """Business hours for a single day of the week."""

    day: int = Field(..., ge=0, le=6, description="0=Mon, 1=Tue, ..., 6=Sun")
    is_open: bool = True
    open_time: str = Field("10:00", pattern=r"^\d{2}:\d{2}$")
    close_time: str = Field("18:00", pattern=r"^\d{2}:\d{2}$")

    @field_validator("close_time")
    @classmethod
    def close_after_open(cls, v, info):
        open_time = info.data.get("open_time")
        if open_time and info.data.get("is_open"):
            oh, om = map(int, open_time.split(":"))
            ch, cm = map(int, v.split(":"))
            if ch * 60 + cm <= oh * 60 + om:
                raise ValueError("close_time must be after open_time")
        return v


class BusinessHoursSettings(BaseModel):
    """Full business hours configuration stored in db.settings."""

    timezone: str = "Asia/Kolkata"
    weekly_hours: list[DayHours] = Field(
        default_factory=lambda: [
            DayHours(day=0),
            DayHours(day=1),
            DayHours(day=2),
            DayHours(day=3),
            DayHours(day=4),
            DayHours(day=5),
            DayHours(day=6, is_open=False),
        ]
    )

    @field_validator("timezone")
    @classmethod
    def validate_timezone(cls, v):
        from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

        try:
            ZoneInfo(v)
        except (ZoneInfoNotFoundError, KeyError):
            raise ValueError(f"Invalid IANA timezone: {v}")
        return v

    @field_validator("weekly_hours")
    @classmethod
    def validate_weekly_hours(cls, v):
        if len(v) != 7:
            raise ValueError("weekly_hours must contain exactly 7 entries")
        days = sorted([d.day for d in v])
        if days != list(range(7)):
            raise ValueError("weekly_hours must contain days 0-6 exactly once")
        return sorted(v, key=lambda d: d.day)


class BusinessHoursResponse(BaseModel):
    """Response model for business hours settings."""

    timezone: str
    weekly_hours: list[DayHours]
