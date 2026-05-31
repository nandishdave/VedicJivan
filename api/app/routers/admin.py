"""Admin HTTP layer — thin Depends-driven router."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.dependencies import (
    get_booking_repository,
    get_payment_repository,
    get_user_repository,
    require_admin,
)
from app.repositories.booking_repository import BookingRepository
from app.repositories.payment_repository import PaymentRepository
from app.repositories.user_repository import UserRepository
from app.use_cases.admin import GetAdminDashboard, GetAdminStats

router = APIRouter(prefix="/api/admin", tags=["Admin"])


def _dashboard_use_case(
    booking_repo: BookingRepository = Depends(get_booking_repository),
    payment_repo: PaymentRepository = Depends(get_payment_repository),
) -> GetAdminDashboard:
    return GetAdminDashboard(booking_repo, payment_repo)


def _stats_use_case(
    user_repo: UserRepository = Depends(get_user_repository),
    booking_repo: BookingRepository = Depends(get_booking_repository),
    payment_repo: PaymentRepository = Depends(get_payment_repository),
) -> GetAdminStats:
    return GetAdminStats(user_repo, booking_repo, payment_repo)


@router.get("/dashboard")
async def dashboard(
    _admin: dict = Depends(require_admin),
    use_case: GetAdminDashboard = Depends(_dashboard_use_case),
):
    return await use_case.execute()


@router.get("/stats")
async def stats(
    _admin: dict = Depends(require_admin),
    use_case: GetAdminStats = Depends(_stats_use_case),
):
    return await use_case.execute()
