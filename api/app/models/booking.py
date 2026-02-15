from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, EmailStr, Field


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
    notes: str = ""


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
