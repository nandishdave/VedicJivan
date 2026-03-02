import stripe
from bson import ObjectId
from fastapi import APIRouter, Depends, Request

from app.config import settings
from app.database import get_db
from app.dependencies import require_admin
from app.models.booking import BookingStatus
from app.models.payment import (
    PaymentCreateCheckout,
    PaymentInDB,
    PaymentResponse,
    PaymentStatus,
)
from app.services.email_service import (
    send_admin_booking_notification,
    send_booking_confirmation,
)
from app.services.calendar_service import create_booking_event
from app.utils.exceptions import BadRequestError, NotFoundError

router = APIRouter(prefix="/api/payments", tags=["Payments"])

stripe.api_key = settings.STRIPE_SECRET_KEY


@router.post("/create-checkout-session", response_model=dict)
async def create_checkout_session(data: PaymentCreateCheckout):
    db = get_db()

    booking = await db.bookings.find_one({"_id": ObjectId(data.booking_id)})
    if not booking:
        raise NotFoundError("Booking not found")

    if booking["status"] == BookingStatus.CONFIRMED:
        raise BadRequestError("Booking already paid")

    currency = data.currency.upper()
    if currency == "EUR":
        amount_cents = booking.get("price_eur", 0) * 100
        stripe_currency = "eur"
    else:
        amount_cents = booking["price_inr"] * 100
        stripe_currency = "inr"

    description = (
        f"Booking for {booking['date']} at {booking['time_slot']}"
        if booking.get("duration_minutes", 0) > 0
        else "Report booking"
    )

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": stripe_currency,
                    "product_data": {
                        "name": booking["service_title"],
                        "description": description,
                    },
                    "unit_amount": amount_cents,
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=(
            f"{settings.FRONTEND_URL}/booking-success/"
            f"?session_id={{CHECKOUT_SESSION_ID}}&booking_id={data.booking_id}"
        ),
        cancel_url=(
            f"{settings.FRONTEND_URL}/booking-cancelled/"
            f"?booking_id={data.booking_id}"
        ),
        customer_email=booking["user_email"],
        metadata={"booking_id": data.booking_id},
        payment_intent_data={"metadata": {"booking_id": data.booking_id}},
    )

    payment = PaymentInDB(
        booking_id=data.booking_id,
        stripe_session_id=session.id,
        amount=amount_cents,
        currency=currency,
    )
    await db.payments.insert_one(payment.model_dump())

    return {"checkout_url": session.url}


@router.post("/webhook")
async def stripe_webhook(request: Request):
    body = await request.body()
    signature = request.headers.get("stripe-signature", "")

    try:
        event = stripe.Webhook.construct_event(
            body, signature, settings.STRIPE_WEBHOOK_SECRET
        )
    except stripe.SignatureVerificationError:
        raise BadRequestError("Invalid webhook signature")

    db = get_db()

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        booking_id = session["metadata"]["booking_id"]

        await db.payments.update_one(
            {"stripe_session_id": session["id"]},
            {
                "$set": {
                    "stripe_payment_intent_id": session.get("payment_intent"),
                    "status": PaymentStatus.CAPTURED,
                }
            },
        )

        await db.bookings.update_one(
            {"_id": ObjectId(booking_id)},
            {"$set": {"status": BookingStatus.CONFIRMED}},
        )

        booking = await db.bookings.find_one({"_id": ObjectId(booking_id)})
        if booking:
            await db.availability.update_one(
                {"date": booking["date"], "slots.start": booking["time_slot"]},
                {"$set": {"slots.$.booked": True}},
            )

            try:
                await send_booking_confirmation(
                    to_email=booking["user_email"],
                    user_name=booking["user_name"],
                    service_title=booking["service_title"],
                    date=booking["date"],
                    time_slot=booking["time_slot"],
                    duration_minutes=booking["duration_minutes"],
                    price_inr=booking["price_inr"],
                    booking_id=booking_id,
                )
            except Exception as e:
                print(f"[EMAIL ERROR] Customer confirmation: {e}")

            try:
                await send_admin_booking_notification(
                    user_name=booking["user_name"],
                    user_email=booking["user_email"],
                    user_phone=booking["user_phone"],
                    service_title=booking["service_title"],
                    date=booking["date"],
                    time_slot=booking["time_slot"],
                    duration_minutes=booking["duration_minutes"],
                    price_inr=booking["price_inr"],
                    booking_id=booking_id,
                )
            except Exception as e:
                print(f"[EMAIL ERROR] Admin notification: {e}")

            try:
                event_id = create_booking_event({**booking, "booking_id": booking_id})
                if event_id:
                    await db.bookings.update_one(
                        {"_id": ObjectId(booking_id)},
                        {"$set": {"google_event_id": event_id}},
                    )
            except Exception as e:
                print(f"[CALENDAR ERROR] {e}")

    elif event["type"] == "checkout.session.expired":
        session = event["data"]["object"]
        await db.payments.update_one(
            {"stripe_session_id": session["id"]},
            {"$set": {"status": PaymentStatus.EXPIRED}},
        )

    elif event["type"] == "charge.refunded":
        charge = event["data"]["object"]
        payment_intent_id = charge.get("payment_intent")
        await db.payments.update_one(
            {"stripe_payment_intent_id": payment_intent_id},
            {"$set": {"status": PaymentStatus.REFUNDED}},
        )

    return {"status": "ok"}


@router.get("/session-status")
async def get_session_status(session_id: str, booking_id: str):
    db = get_db()

    payment = await db.payments.find_one({"stripe_session_id": session_id})
    if not payment:
        raise NotFoundError("Payment not found")

    booking = await db.bookings.find_one({"_id": ObjectId(booking_id)})

    result = {
        "payment_status": payment["status"],
        "booking_status": booking["status"] if booking else "unknown",
    }

    if booking:
        result["booking"] = {
            "service_title": booking.get("service_title", ""),
            "date": booking.get("date", ""),
            "time_slot": booking.get("time_slot", ""),
            "duration_minutes": booking.get("duration_minutes", 0),
            "price_inr": booking.get("price_inr", 0),
            "user_name": booking.get("user_name", ""),
            "user_email": booking.get("user_email", ""),
        }

    return result


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
                stripe_session_id=doc.get("stripe_session_id", ""),
                stripe_payment_intent_id=doc.get("stripe_payment_intent_id"),
                amount=doc.get("amount", doc.get("amount_inr", 0)),
                currency=doc.get("currency", "INR"),
                status=doc["status"],
                created_at=doc["created_at"],
            )
        )
    return results
