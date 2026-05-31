"""Bookings HTTP layer.

The router is intentionally thin — it parses requests, picks the right use
case via dependency injection, and shapes the response. ALL business rules
(slot validation, conflict detection, reschedule cutoff, ownership checks)
live in `app/use_cases/bookings.py`.

Domain exceptions raised by use cases are translated to HTTP responses by
the app-level exception handlers in `app/main.py`.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.database import get_db
from app.dependencies import (
    get_booking_repository,
    get_current_user,
    get_service_repository,
    require_admin,
)
from app.models.booking import (
    BookingCreate,
    BookingResponse,
    BookingReschedule,
    BookingStatus,
    BookingStatusUpdate,
)
from app.repositories.booking_repository import BookingRepository
from app.repositories.service_repository import ServiceRepository
from app.services.email_service import send_booking_rescheduled
from app.use_cases.bookings import (
    CancelBooking,
    CreateBooking,
    GetBooking,
    GetBookingPublic,
    ListBookings,
    RescheduleBooking,
    ResumeBooking,
    SetBookingStatus,
)
from app.use_cases.services import GetServicePrice

router = APIRouter(prefix="/api/bookings", tags=["Bookings"])


# Back-compat shims — tests import these names from this module.
# Pricing now lives in `app.services.default_services` (defaults / seed) and
# `app.use_cases.services.GetServicePrice` (DB-backed runtime path). The
# names below are re-exported so the existing pricing unit tests keep
# working unchanged.
from app.services.default_services import (  # noqa: E402,F401
    SERVICE_PRICES,
    SERVICE_PRICES_EUR,
    get_price,
)
from app.utils.time_helpers import ranges_overlap as _overlaps  # noqa: E402,F401
from app.utils.time_helpers import time_to_minutes as _time_to_minutes  # noqa: E402,F401


# ── Use-case factories (Depends-friendly) ──
# Each factory wires the use case with its dependencies so routes can do
# `Depends(_create_booking_use_case)`. Tests can override via
# `app.dependency_overrides[_create_booking_use_case] = lambda: FakeUseCase()`.


def _create_booking_use_case(
    repo: BookingRepository = Depends(get_booking_repository),
    service_repo: ServiceRepository = Depends(get_service_repository),
) -> CreateBooking:
    pricing = GetServicePrice(service_repo)
    return CreateBooking(repo, get_db(), pricing.execute)


def _list_bookings_use_case(
    repo: BookingRepository = Depends(get_booking_repository),
) -> ListBookings:
    return ListBookings(repo)


def _get_booking_use_case(
    repo: BookingRepository = Depends(get_booking_repository),
) -> GetBooking:
    return GetBooking(repo)


def _get_booking_public_use_case(
    repo: BookingRepository = Depends(get_booking_repository),
) -> GetBookingPublic:
    return GetBookingPublic(repo)


def _resume_booking_use_case(
    repo: BookingRepository = Depends(get_booking_repository),
) -> ResumeBooking:
    return ResumeBooking(repo)


def _cancel_booking_use_case(
    repo: BookingRepository = Depends(get_booking_repository),
) -> CancelBooking:
    return CancelBooking(repo)


def _set_booking_status_use_case(
    repo: BookingRepository = Depends(get_booking_repository),
) -> SetBookingStatus:
    return SetBookingStatus(repo)


def _reschedule_booking_use_case(
    repo: BookingRepository = Depends(get_booking_repository),
) -> RescheduleBooking:
    return RescheduleBooking(repo, get_db(), send_booking_rescheduled)


# ── Endpoints ──────────────────────────────────────────────────────────────


@router.post("", response_model=BookingResponse)
async def create_booking(
    data: BookingCreate,
    use_case: CreateBooking = Depends(_create_booking_use_case),
):
    doc = await use_case.execute(data)
    return _to_response(doc)


@router.get("", response_model=list[BookingResponse])
async def list_bookings(
    status: BookingStatus | None = None,
    date: str | None = Query(None, pattern=r"^\d{4}-\d{2}-\d{2}$"),
    current_user: dict = Depends(get_current_user),
    use_case: ListBookings = Depends(_list_bookings_use_case),
):
    docs = await use_case.execute(
        current_user=current_user,
        status=status,
        booking_date=date,
    )
    return [_to_response(d) for d in docs]


@router.get("/{booking_id}/resume", response_model=BookingResponse)
async def resume_booking(
    booking_id: str,
    use_case: ResumeBooking = Depends(_resume_booking_use_case),
):
    doc = await use_case.execute(booking_id)
    return _to_response(doc)


@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(
    booking_id: str,
    current_user: dict = Depends(get_current_user),
    use_case: GetBooking = Depends(_get_booking_use_case),
):
    doc = await use_case.execute(booking_id, current_user)
    return _to_response(doc)


@router.patch("/{booking_id}/cancel", response_model=BookingResponse)
async def cancel_booking(
    booking_id: str,
    current_user: dict = Depends(get_current_user),
    use_case: CancelBooking = Depends(_cancel_booking_use_case),
):
    doc = await use_case.execute(booking_id, current_user)
    return _to_response(doc)


@router.patch("/{booking_id}/status", response_model=BookingResponse)
async def update_booking_status(
    booking_id: str,
    data: BookingStatusUpdate,
    _admin: dict = Depends(require_admin),
    use_case: SetBookingStatus = Depends(_set_booking_status_use_case),
):
    doc = await use_case.execute(booking_id, data.status)
    return _to_response(doc)


@router.get("/{booking_id}/view", response_model=BookingResponse)
async def get_booking_public(
    booking_id: str,
    use_case: GetBookingPublic = Depends(_get_booking_public_use_case),
):
    """Public endpoint: returns a confirmed booking by ID (for reschedule page)."""
    doc = await use_case.execute(booking_id)
    return _to_response(doc)


@router.patch("/{booking_id}/reschedule", response_model=BookingResponse)
async def reschedule_booking(
    booking_id: str,
    data: BookingReschedule,
    use_case: RescheduleBooking = Depends(_reschedule_booking_use_case),
):
    """Reschedule a confirmed booking (public — booking ID is the auth token)."""
    doc = await use_case.execute(booking_id, data)
    return _to_response(doc)


# ── Response shaping ───────────────────────────────────────────────────────


def _to_response(doc: dict) -> BookingResponse:
    return BookingResponse(
        id=str(doc["_id"]),
        user_name=doc["user_name"],
        user_email=doc["user_email"],
        user_phone=doc["user_phone"],
        service_slug=doc["service_slug"],
        service_title=doc["service_title"],
        date=doc["date"],
        time_slot=doc["time_slot"],
        duration_minutes=doc["duration_minutes"],
        price_inr=doc["price_inr"],
        price_eur=doc.get("price_eur", 0),
        status=doc["status"],
        payment_id=doc.get("payment_id"),
        notes=doc.get("notes", ""),
        created_at=doc["created_at"],
        date_of_birth=doc.get("date_of_birth", ""),
        time_of_birth=doc.get("time_of_birth"),
        birth_time_unknown=doc.get("birth_time_unknown", False),
        place_of_birth=doc.get("place_of_birth", ""),
        birth_latitude=doc.get("birth_latitude", 0.0),
        birth_longitude=doc.get("birth_longitude", 0.0),
    )
