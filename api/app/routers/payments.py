import hmac
import hashlib

from bson import ObjectId
from fastapi import APIRouter, Depends, Request

from app.config import settings
from app.database import get_db
from app.dependencies import require_admin
from app.models.booking import BookingStatus
from app.models.payment import (
    PaymentCreateOrder,
    PaymentInDB,
    PaymentResponse,
    PaymentStatus,
    PaymentVerify,
)
from app.utils.exceptions import BadRequestError, NotFoundError

router = APIRouter(prefix="/api/payments", tags=["Payments"])


def get_razorpay_client():
    import razorpay

    return razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )


@router.post("/create-order", response_model=dict)
async def create_order(data: PaymentCreateOrder):
    db = get_db()

    booking = await db.bookings.find_one({"_id": ObjectId(data.booking_id)})
    if not booking:
        raise NotFoundError("Booking not found")

    if booking["status"] == BookingStatus.CONFIRMED:
        raise BadRequestError("Booking already paid")

    client = get_razorpay_client()
    order = client.order.create(
        {
            "amount": data.amount_inr * 100,  # Razorpay expects paise
            "currency": "INR",
            "receipt": f"booking_{data.booking_id}",
            "notes": {
                "booking_id": data.booking_id,
                "service": booking["service_title"],
            },
        }
    )

    payment = PaymentInDB(
        booking_id=data.booking_id,
        razorpay_order_id=order["id"],
        amount_inr=data.amount_inr,
    )
    await db.payments.insert_one(payment.model_dump())

    return {
        "order_id": order["id"],
        "amount": order["amount"],
        "currency": order["currency"],
        "key_id": settings.RAZORPAY_KEY_ID,
    }


@router.post("/verify", response_model=dict)
async def verify_payment(data: PaymentVerify):
    db = get_db()

    # Verify signature using HMAC SHA256
    message = f"{data.razorpay_order_id}|{data.razorpay_payment_id}"
    expected_signature = hmac.new(
        settings.RAZORPAY_KEY_SECRET.encode(),
        message.encode(),
        hashlib.sha256,
    ).hexdigest()

    if expected_signature != data.razorpay_signature:
        raise BadRequestError("Invalid payment signature")

    # Update payment record
    await db.payments.update_one(
        {"razorpay_order_id": data.razorpay_order_id},
        {
            "$set": {
                "razorpay_payment_id": data.razorpay_payment_id,
                "razorpay_signature": data.razorpay_signature,
                "status": PaymentStatus.CAPTURED,
            }
        },
    )

    # Confirm the booking
    await db.bookings.update_one(
        {"_id": ObjectId(data.booking_id)},
        {"$set": {"status": BookingStatus.CONFIRMED}},
    )

    # Mark the time slot as booked
    booking = await db.bookings.find_one({"_id": ObjectId(data.booking_id)})
    if booking:
        await db.availability.update_one(
            {"date": booking["date"], "slots.start": booking["time_slot"]},
            {"$set": {"slots.$.booked": True}},
        )

    return {"status": "success", "message": "Payment verified and booking confirmed"}


@router.post("/webhook")
async def razorpay_webhook(request: Request):
    body = await request.body()

    if settings.RAZORPAY_WEBHOOK_SECRET:
        signature = request.headers.get("x-razorpay-signature", "")
        expected = hmac.new(
            settings.RAZORPAY_WEBHOOK_SECRET.encode(),
            body,
            hashlib.sha256,
        ).hexdigest()

        if expected != signature:
            raise BadRequestError("Invalid webhook signature")

    import json

    payload = json.loads(body)
    event = payload.get("event")

    db = get_db()

    if event == "payment.captured":
        payment_entity = payload["payload"]["payment"]["entity"]
        order_id = payment_entity.get("order_id")

        await db.payments.update_one(
            {"razorpay_order_id": order_id},
            {
                "$set": {
                    "razorpay_payment_id": payment_entity["id"],
                    "status": PaymentStatus.CAPTURED,
                }
            },
        )

    elif event == "refund.created":
        payment_entity = payload["payload"]["refund"]["entity"]
        payment_id = payment_entity.get("payment_id")

        await db.payments.update_one(
            {"razorpay_payment_id": payment_id},
            {"$set": {"status": PaymentStatus.REFUNDED}},
        )

    return {"status": "ok"}


@router.get("", response_model=list[PaymentResponse])
async def list_payments(_admin: dict = Depends(require_admin)):
    db = get_db()
    cursor = db.payments.find().sort("created_at", -1).limit(100)
    results = []
    async for doc in cursor:
        results.append(
            PaymentResponse(
                id=str(doc["_id"]),
                booking_id=doc["booking_id"],
                razorpay_order_id=doc["razorpay_order_id"],
                razorpay_payment_id=doc.get("razorpay_payment_id"),
                amount_inr=doc["amount_inr"],
                currency=doc.get("currency", "INR"),
                status=doc["status"],
                created_at=doc["created_at"],
            )
        )
    return results
