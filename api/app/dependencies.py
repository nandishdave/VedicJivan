from fastapi import Depends, Header

from app.database import get_db
from app.models.user import UserRole
from app.repositories.booking_repository import (
    BookingRepository,
    MongoBookingRepository,
)
from app.repositories.kundli_repository import (
    KundliRepository,
    MongoKundliRepository,
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


# ── Repository factories (clean architecture wiring) ──
# Use cases depend on the Protocol (BookingRepository); production wires the
# concrete MongoBookingRepository here. Tests can override these dependencies
# via FastAPI's `app.dependency_overrides` to substitute in-memory fakes.


def get_booking_repository() -> BookingRepository:
    return MongoBookingRepository(get_db())


def get_payment_repository() -> PaymentRepository:
    return MongoPaymentRepository(get_db())


def get_processed_event_repository() -> ProcessedEventRepository:
    return MongoProcessedEventRepository(get_db())


def get_kundli_repository() -> KundliRepository:
    return MongoKundliRepository(get_db())


def get_unavailability_repository() -> UnavailabilityRepository:
    return MongoUnavailabilityRepository(get_db())


def get_settings_repository() -> SettingsRepository:
    return MongoSettingsRepository(get_db())


def get_user_repository() -> UserRepository:
    return MongoUserRepository(get_db())


def get_service_repository() -> ServiceRepository:
    return MongoServiceRepository(get_db())
