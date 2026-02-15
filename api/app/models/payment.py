from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


class PaymentStatus(str, Enum):
    CREATED = "created"
    CAPTURED = "captured"
    FAILED = "failed"
    REFUNDED = "refunded"


class PaymentCreateOrder(BaseModel):
    booking_id: str
    amount_inr: int = Field(..., gt=0)


class PaymentVerify(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
    booking_id: str


class PaymentResponse(BaseModel):
    id: str
    booking_id: str
    razorpay_order_id: str
    razorpay_payment_id: str | None = None
    amount_inr: int
    currency: str = "INR"
    status: PaymentStatus
    created_at: datetime


class PaymentInDB(BaseModel):
    booking_id: str
    razorpay_order_id: str
    razorpay_payment_id: str | None = None
    razorpay_signature: str | None = None
    amount_inr: int
    currency: str = "INR"
    status: PaymentStatus = PaymentStatus.CREATED
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
