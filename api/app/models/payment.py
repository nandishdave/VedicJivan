from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


class PaymentStatus(str, Enum):
    CREATED = "created"
    CAPTURED = "captured"
    FAILED = "failed"
    REFUNDED = "refunded"
    EXPIRED = "expired"


class PaymentCreateCheckout(BaseModel):
    booking_id: str
    currency: str = "INR"


class PaymentResponse(BaseModel):
    id: str
    booking_id: str
    stripe_session_id: str
    stripe_payment_intent_id: str | None = None
    amount: int
    currency: str = "INR"
    status: PaymentStatus
    created_at: datetime


class PaymentInDB(BaseModel):
    booking_id: str
    stripe_session_id: str
    stripe_payment_intent_id: str | None = None
    amount: int
    currency: str = "INR"
    status: PaymentStatus = PaymentStatus.CREATED
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
