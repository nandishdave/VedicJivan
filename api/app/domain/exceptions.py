"""Domain-level exceptions — raised by use cases, NOT by routers.

Routers translate these into HTTP responses. Use cases stay HTTP-agnostic so
they can be reused from background tasks, CLI scripts, or future gRPC.

Mapping (handled at the router edge):
  DomainError                 → 400 BadRequest
  EntityNotFoundError         → 404 NotFound
  AccessDeniedError           → 403 Forbidden
  RateLimitExceededError      → 429 TooManyRequests
"""

from __future__ import annotations


class DomainError(Exception):
    """Base for all domain errors. Routers map subclasses to HTTP responses."""


class EntityNotFoundError(DomainError):
    """The requested resource does not exist."""


class AccessDeniedError(DomainError):
    """The actor is not authorised to perform the action on this resource."""


class RateLimitExceededError(DomainError):
    """The actor has exceeded a rate limit."""


# ── Booking-specific ──


class BookingValidationError(DomainError):
    """A booking request fails business rules (slot, hours, conflict, etc.)."""


class BookingExpiredError(DomainError):
    """A pending booking has timed out and can no longer be resumed."""


class BookingNotConfirmedError(DomainError):
    """Operation requires a confirmed booking but the booking is in another state."""


class BookingTooSoonToRescheduleError(DomainError):
    """Reschedule attempted within the cutoff window before the session."""


# ── Payment-specific ──


class PaymentAlreadyCompletedError(DomainError):
    """Booking is already paid; cannot start a new checkout."""


class InvalidWebhookSignatureError(DomainError):
    """Stripe webhook signature failed verification."""
