"""Payment use cases — application workflows for the payment aggregate.

Use cases:
  - CreateCheckoutSession   — start a Stripe Checkout session for a pending booking
  - ProcessStripeWebhook    — verify + dispatch a Stripe webhook delivery
  - GetSessionStatus        — public lookup by session id
  - ListPayments            — admin recent-payment list

Side effects (DB writes, Stripe API calls, email sends, Calendar inserts) are
expressed as injected collaborators so tests can swap them out.
"""

from __future__ import annotations

from typing import Any

import stripe
from bson import ObjectId
from bson.errors import InvalidId

from app.config import settings
from app.domain.exceptions import (
    BookingValidationError,
    EntityNotFoundError,
    InvalidWebhookSignatureError,
    PaymentAlreadyCompletedError,
)
from app.infrastructure.logging import get_logger
from app.models.booking import BookingStatus
from app.models.payment import PaymentInDB
from app.repositories.availability_repository import AvailabilityRepository
from app.repositories.booking_repository import BookingRepository
from app.repositories.payment_repository import PaymentRepository
from app.repositories.processed_event_repository import ProcessedEventRepository

logger = get_logger(__name__)


def _safe_object_id(value: str) -> ObjectId:
    """Coerce a string to ObjectId; raise EntityNotFoundError on garbage."""
    try:
        return ObjectId(value)
    except (InvalidId, TypeError):
        raise EntityNotFoundError("Booking not found")


# ── CreateCheckoutSession ──────────────────────────────────────────────────


class CreateCheckoutSession:
    """Start a Stripe Checkout Session for a pending booking."""

    def __init__(
        self,
        payment_repo: PaymentRepository,
        booking_repo: BookingRepository,
    ) -> None:
        self._payment_repo = payment_repo
        self._booking_repo = booking_repo

    async def execute(self, *, booking_id: str, currency: str) -> str:
        """Returns the Stripe-hosted checkout URL."""
        oid = _safe_object_id(booking_id)
        booking = await self._booking_repo.find_by_id(oid)
        if not booking:
            raise EntityNotFoundError("Booking not found")

        if booking["status"] == BookingStatus.CONFIRMED:
            raise PaymentAlreadyCompletedError("Booking already paid")

        currency = currency.upper()
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
                f"?session_id={{CHECKOUT_SESSION_ID}}&booking_id={booking_id}"
            ),
            cancel_url=(
                f"{settings.FRONTEND_URL}/booking-cancelled/"
                f"?booking_id={booking_id}"
            ),
            customer_email=booking["user_email"],
            metadata={"booking_id": booking_id},
            payment_intent_data={"metadata": {"booking_id": booking_id}},
        )

        await self._payment_repo.insert(
            PaymentInDB(
                booking_id=booking_id,
                stripe_session_id=session.id,
                amount=amount_cents,
                currency=currency,
            )
        )

        return session.url


# ── ProcessStripeWebhook ──────────────────────────────────────────────────


class ProcessStripeWebhook:
    """Verify a Stripe webhook delivery and dispatch by event type.

    Email sends and Calendar event creation are best-effort: a failure logs
    but never causes the webhook to return non-2xx (Stripe would otherwise
    retry indefinitely).
    """

    def __init__(
        self,
        payment_repo: PaymentRepository,
        booking_repo: BookingRepository,
        processed_event_repo: ProcessedEventRepository,
        availability_repo: AvailabilityRepository,
        webhook_secret: str,
        send_confirmation,
        send_admin_notification,
        create_calendar_event,
    ) -> None:
        self._payment_repo = payment_repo
        self._booking_repo = booking_repo
        self._processed_event_repo = processed_event_repo
        self._availability_repo = availability_repo
        self._webhook_secret = webhook_secret
        self._send_confirmation = send_confirmation
        self._send_admin_notification = send_admin_notification
        self._create_calendar_event = create_calendar_event

    async def execute(self, *, payload: bytes, signature: str) -> None:
        try:
            event = stripe.Webhook.construct_event(
                payload, signature, self._webhook_secret
            )
        except stripe.SignatureVerificationError:
            raise InvalidWebhookSignatureError("Invalid webhook signature")

        event_id = event["id"]
        event_type = event["type"]

        # Record-before dedupe: any redelivery of the same event id is a
        # silent no-op. The repo's atomic insert + DuplicateKeyError catch
        # is race-safe across two concurrent retries hitting this task.
        if not await self._processed_event_repo.mark_processed(event_id, event_type):
            logger.info(
                "Stripe event %s (%s) already processed — skipping",
                event_id,
                event_type,
            )
            return

        obj = event["data"]["object"]

        if event_type == "checkout.session.completed":
            await self._handle_checkout_completed(obj)
        elif event_type == "checkout.session.expired":
            await self._payment_repo.mark_expired(obj["id"])
        elif event_type == "charge.refunded":
            # Stripe SDK v15+ returns StripeObject (not dict). `.get()` raises
            # AttributeError. Bracket access + try/except is the safe form —
            # a refund webhook without payment_intent is a no-op.
            try:
                payment_intent_id = obj["payment_intent"]
            except (KeyError, AttributeError):
                payment_intent_id = None
            if payment_intent_id:
                await self._payment_repo.mark_refunded(payment_intent_id)

    async def _handle_checkout_completed(self, session: Any) -> None:
        booking_id = session["metadata"]["booking_id"]

        # See note above on StripeObject vs dict.
        try:
            pi_id = session["payment_intent"]
        except (KeyError, AttributeError):
            pi_id = None

        await self._payment_repo.mark_captured(session["id"], payment_intent_id=pi_id)
        await self._booking_repo.update_status(booking_id, BookingStatus.CONFIRMED)

        booking = await self._booking_repo.find_by_id(booking_id)
        if not booking:
            return

        # Slot-booked flag on the legacy `availability` collection (a different
        # collection from `unavailability`, kept for back-compat with the
        # frontend slot lookup). Routed through its repository so the use case
        # holds no Mongo handle.
        await self._availability_repo.mark_slot_booked(
            booking["date"], booking["time_slot"]
        )

        try:
            await self._send_confirmation(
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
            logger.error("Customer confirmation email failed: %s", e)

        try:
            await self._send_admin_notification(
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
            logger.error("Admin notification email failed: %s", e)

        try:
            event_id = self._create_calendar_event({**booking, "booking_id": booking_id})
            if event_id:
                await self._booking_repo.set_google_event_id(booking_id, event_id)
        except Exception as e:
            logger.error("Calendar event sync failed: %s", e)


# ── GetSessionStatus ──────────────────────────────────────────────────────


class GetSessionStatus:
    """Public lookup of payment + booking state by Stripe session id."""

    def __init__(
        self,
        payment_repo: PaymentRepository,
        booking_repo: BookingRepository,
    ) -> None:
        self._payment_repo = payment_repo
        self._booking_repo = booking_repo

    async def execute(self, *, session_id: str, booking_id: str) -> dict:
        payment = await self._payment_repo.find_by_session_id(session_id)
        if not payment:
            raise EntityNotFoundError("Payment not found")

        try:
            oid = ObjectId(booking_id)
        except (InvalidId, TypeError):
            raise BookingValidationError(f"Invalid booking id: {booking_id}")

        booking = await self._booking_repo.find_by_id(oid)

        result: dict[str, Any] = {
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


# ── ListPayments ──────────────────────────────────────────────────────────


class ListPayments:
    """Admin list of recent payments (most recent first)."""

    def __init__(self, payment_repo: PaymentRepository) -> None:
        self._payment_repo = payment_repo

    async def execute(self, *, limit: int = 100) -> list[dict]:
        return await self._payment_repo.list_recent(limit=limit)
