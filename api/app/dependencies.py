from fastapi import Depends, Header, HTTPException

from app.config import settings
from app.database import get_db
from app.infrastructure.queue import MessageQueue, SqsMessageQueue
from app.models.user import UserRole
from app.repositories.availability_repository import (
    AvailabilityRepository,
    MongoAvailabilityRepository,
)
from app.repositories.booking_repository import (
    BookingRepository,
    MongoBookingRepository,
)
from app.repositories.kundli_repository import (
    KundliRepository,
    MongoKundliRepository,
)
from app.repositories.rate_limit_repository import (
    MongoRateLimitRepository,
    RateLimitRepository,
)
from app.repositories.payment_repository import (
    MongoPaymentRepository,
    PaymentRepository,
)
from app.repositories.processed_event_repository import (
    MongoProcessedEventRepository,
    ProcessedEventRepository,
)
from app.repositories.settings_repository import (
    MongoSettingsRepository,
    SettingsRepository,
)
from app.repositories.unavailability_repository import (
    MongoUnavailabilityRepository,
    UnavailabilityRepository,
)
from app.repositories.service_repository import (
    MongoServiceRepository,
    ServiceRepository,
)
from app.repositories.user_repository import (
    MongoUserRepository,
    UserRepository,
)
from app.utils.exceptions import ForbiddenError, UnauthorizedError
from app.utils.security import decode_token


async def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise UnauthorizedError("Invalid authorization header")

    token = authorization.split(" ")[1]
    payload = decode_token(token)

    if not payload or payload.get("type") != "access":
        raise UnauthorizedError("Invalid or expired token")

    db = get_db()
    from bson import ObjectId

    user = await db.users.find_one({"_id": ObjectId(payload["sub"])})
    if not user:
        raise UnauthorizedError("User not found")

    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "name": user["name"],
        "role": user["role"],
    }


async def require_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != UserRole.ADMIN:
        raise ForbiddenError("Admin access required")
    return current_user


def block_during_maintenance() -> None:
    """Reject "only-when-live" internal/scheduled work while soft maintenance
    is on. Returns 503 so scheduled callers (e.g. the booking-reminders cron)
    treat it as "skip", not a hard failure.

    Attach to any internal/scheduled endpoint that should pause in maintenance:
        @router.post("/foo", dependencies=[Depends(block_during_maintenance)])

    Complements the infra-level maintenance (ECS scaled to 0 + CloudFront 503),
    which the CI guard `_app-live-guard.yml` catches. This flag covers the case
    where the app stays UP but jobs should still pause.
    """
    if settings.MAINTENANCE_MODE:
        raise HTTPException(status_code=503, detail="Service in maintenance")


# ── Repository factories (clean architecture wiring) ──
# Use cases depend on the Protocol (BookingRepository); production wires the
# concrete MongoBookingRepository here. Tests can override these dependencies
# via FastAPI's `app.dependency_overrides` to substitute in-memory fakes.


def get_booking_repository() -> BookingRepository:
    return MongoBookingRepository(get_db())


def get_payment_repository() -> PaymentRepository:
    return MongoPaymentRepository(get_db())


def get_availability_repository() -> AvailabilityRepository:
    return MongoAvailabilityRepository(get_db())


def get_processed_event_repository() -> ProcessedEventRepository:
    return MongoProcessedEventRepository(get_db())


def get_kundli_repository() -> KundliRepository:
    return MongoKundliRepository(get_db())


def get_rate_limit_repository() -> RateLimitRepository:
    return MongoRateLimitRepository(get_db())


def get_unavailability_repository() -> UnavailabilityRepository:
    return MongoUnavailabilityRepository(get_db())


def get_settings_repository() -> SettingsRepository:
    return MongoSettingsRepository(get_db())


def get_user_repository() -> UserRepository:
    return MongoUserRepository(get_db())


def get_service_repository() -> ServiceRepository:
    return MongoServiceRepository(get_db())


# ── Message queue factory ──
# Singleton — boto3 client construction is non-trivial (config loading,
# credential resolution) and the client itself is thread-safe. Tests
# substitute a FakeMessageQueue via `app.dependency_overrides`.

_kundli_queue_singleton: MessageQueue | None = None


def get_message_queue() -> MessageQueue:
    global _kundli_queue_singleton
    if _kundli_queue_singleton is None:
        _kundli_queue_singleton = SqsMessageQueue(
            queue_url=settings.KUNDLI_QUEUE_URL,
            region=settings.AWS_REGION,
        )
    return _kundli_queue_singleton
