import re
from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator


class BookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class BookingCreate(BaseModel):
    service_slug: str
    service_title: str
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    time_slot: str = Field(..., pattern=r"^\d{2}:\d{2}$")
    duration_minutes: int = Field(..., ge=15, le=120)
    user_name: str = Field(..., min_length=2, max_length=100)
    user_email: EmailStr
    user_phone: str = Field(..., min_length=10, max_length=20)
    notes: str = Field(..., min_length=1, max_length=1000)

    # Birth details for astrology
    date_of_birth: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    time_of_birth: str | None = None
    birth_time_unknown: bool = False
    place_of_birth: str = Field(..., min_length=1, max_length=200)
    birth_latitude: float = Field(..., ge=-90, le=90)
    birth_longitude: float = Field(..., ge=-180, le=180)

    @field_validator("time_of_birth")
    @classmethod
    def validate_time_format(cls, v: str | None) -> str | None:
        if v is not None:
            if not re.match(r"^(0[1-9]|1[0-2]):[0-5][0-9] (AM|PM)$", v):
                raise ValueError("time_of_birth must be in 'HH:MM AM/PM' format")
        return v

    @model_validator(mode="after")
    def validate_birth_time(self) -> "BookingCreate":
        if not self.birth_time_unknown and not self.time_of_birth:
            raise ValueError(
                "Either provide time_of_birth or set birth_time_unknown to true"
            )
        if self.birth_time_unknown:
            self.time_of_birth = None
        return self


class BookingResponse(BaseModel):
    id: str
    user_name: str
    user_email: str
    user_phone: str
    service_slug: str
    service_title: str
    date: str
    time_slot: str
    duration_minutes: int
    price_inr: int
    status: BookingStatus
    payment_id: str | None = None
    notes: str
    created_at: datetime

    # Birth details
    date_of_birth: str = ""
    time_of_birth: str | None = None
    birth_time_unknown: bool = False
    place_of_birth: str = ""
    birth_latitude: float = 0.0
    birth_longitude: float = 0.0


class BookingStatusUpdate(BaseModel):
    status: BookingStatus


class BookingInDB(BaseModel):
    user_id: str | None = None
    user_name: str
    user_email: str
    user_phone: str
    service_slug: str
    service_title: str
    date: str
    time_slot: str
    duration_minutes: int
    price_inr: int
    status: BookingStatus = BookingStatus.PENDING
    payment_id: str | None = None
    notes: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Birth details
    date_of_birth: str = ""
    time_of_birth: str | None = None
    birth_time_unknown: bool = False
    place_of_birth: str = ""
    birth_latitude: float = 0.0
    birth_longitude: float = 0.0
