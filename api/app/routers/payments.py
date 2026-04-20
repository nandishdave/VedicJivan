"""Payments HTTP layer.

The router is thin: parses requests, picks the right use case via DI,
shapes responses. Stripe interaction, signature verification, payment
state transitions and email/calendar side effects live in
`app/use_cases/payments.py`.
"""

from __future__ import annotations

import stripe
from fastapi import APIRouter, Depends, Request

from app.config import settings
from app.database import get_db
from app.dependencies import (
    get_booking_repository,
    get_payment_repository,
    require_admin,
)
from app.models.payment import (
    PaymentCreateCheckout,
    PaymentResponse,
)
from app.repositories.booking_repository import BookingRepository
from app.repositories.payment_repository import PaymentRepository
from app.services.calendar_service import create_booking_event
from app.services.email_service import (
    send_admin_booking_notification,
    send_booking_confirmation,
)
from app.use_cases.payments import (
    CreateCheckoutSession,
    GetSessionStatus,
    ListPayments,
    ProcessStripeWebhook,
)

router = APIRouter(prefix="/api/payments", tags=["Payments"])

stripe.api_key = settings.STRIPE_SECRET_KEY


# ── Use-case factories (Depends-friendly) ──


def _create_checkout_session_use_case(
    payment_repo: PaymentRepository = Depends(get_payment_repository),
    booking_repo: BookingRepository = Depends(get_booking_repository),
) -> CreateCheckoutSession:
    return CreateCheckoutSession(payment_repo, booking_repo)


def _process_stripe_webhook_use_case(
    payment_repo: PaymentRepository = Depends(get_payment_repository),
    booking_repo: BookingRepository = Depends(get_booking_repository),
) -> ProcessStripeWebhook:
    return ProcessStripeWebhook(
        payment_repo=payment_repo,
        booking_repo=booking_repo,
        db=get_db(),
        webhook_secret=settings.STRIPE_WEBHOOK_SECRET,
        send_confirmation=send_booking_confirmation,
        send_admin_notification=send_admin_booking_notification,
        create_calendar_event=create_booking_event,
    )


def _get_session_status_use_case(
    payment_repo: PaymentRepository = Depends(get_payment_repository),
    booking_repo: BookingRepository = Depends(get_booking_repository),
) -> GetSessionStatus:
    return GetSessionStatus(payment_repo, booking_repo)


def _list_payments_use_case(
    payment_repo: PaymentRepository = Depends(get_payment_repository),
) -> ListPayments:
    return ListPayments(payment_repo)


# ── Endpoints ──────────────────────────────────────────────────────────────


@router.post("/create-checkout-session", response_model=dict)
async def create_checkout_session(
    data: PaymentCreateCheckout,
    use_case: CreateCheckoutSession = Depends(_create_checkout_session_use_case),
):
    checkout_url = await use_case.execute(
        booking_id=data.booking_id, currency=data.currency
    )
    return {"checkout_url": checkout_url}


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    use_case: ProcessStripeWebhook = Depends(_process_stripe_webhook_use_case),
):
    body = await request.body()
    signature = request.headers.get("stripe-signature", "")
    await use_case.execute(payload=body, signature=signature)
    return {"status": "ok"}


@router.get("/session-status")
async def get_session_status(
    session_id: str,
    booking_id: str,
    use_case: GetSessionStatus = Depends(_get_session_status_use_case),
):
    return await use_case.execute(session_id=session_id, booking_id=booking_id)


@router.get("", response_model=list[PaymentResponse])
async def list_payments(
    _admin: dict = Depends(require_admin),
    use_case: ListPayments = Depends(_list_payments_use_case),
):
    docs = await use_case.execute()
    return [_to_response(d) for d in docs]


# ── Response shaping ───────────────────────────────────────────────────────


def _to_response(doc: dict) -> PaymentResponse:
    return PaymentResponse(
        id=str(doc["_id"]),
        booking_id=doc["booking_id"],
        stripe_session_id=doc.get("stripe_session_id", ""),
        stripe_payment_intent_id=doc.get("stripe_payment_intent_id"),
        amount=doc.get("amount", doc.get("amount_inr", 0)),
        currency=doc.get("currency", "INR"),
        status=doc["status"],
        created_at=doc["created_at"],
    )
