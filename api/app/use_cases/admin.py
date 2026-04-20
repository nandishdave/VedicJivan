"""Admin use cases — dashboard + stats analytics."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.repositories.booking_repository import BookingRepository
from app.repositories.payment_repository import PaymentRepository
from app.repositories.user_repository import UserRepository

# TODO Phase 5: move to settings.ADMIN_DAILY_SERIES_DAYS / RECENT_BOOKINGS_LIMIT.
_DAILY_SERIES_DAYS = 30
_RECENT_BOOKINGS_LIMIT = 10


def _today_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


# ── GetAdminDashboard ─────────────────────────────────────────────────────


class GetAdminDashboard:
    def __init__(
        self,
        booking_repo: BookingRepository,
        payment_repo: PaymentRepository,
    ) -> None:
        self._bookings = booking_repo
        self._payments = payment_repo

    async def execute(self) -> dict:
        today = _today_str()

        today_bookings = await self._bookings.count_for_date(today)
        upcoming = await self._bookings.count_upcoming_confirmed(today)
        total_revenue = await self._payments.total_captured_amount()
        status_counts = await self._bookings.aggregate_status_counts()

        recent_docs = await self._bookings.list_for_user(limit=_RECENT_BOOKINGS_LIMIT)
        recent = [
            {
                "id": str(d["_id"]),
                "user_name": d["user_name"],
                "service_title": d["service_title"],
                "date": d["date"],
                "time_slot": d["time_slot"],
                "status": d["status"],
                "price_inr": d["price_inr"],
            }
            for d in recent_docs
        ]

        return {
            "today_bookings": today_bookings,
            "upcoming_bookings": upcoming,
            "total_revenue": total_revenue,
            "bookings_by_status": status_counts,
            "recent_bookings": recent,
        }


# ── GetAdminStats ─────────────────────────────────────────────────────────


class GetAdminStats:
    def __init__(
        self,
        user_repo: UserRepository,
        booking_repo: BookingRepository,
        payment_repo: PaymentRepository,
    ) -> None:
        self._users = user_repo
        self._bookings = booking_repo
        self._payments = payment_repo

    async def execute(self) -> dict:
        total_users = await self._users.count()
        total_bookings = await self._bookings.count_total()
        total_payments = await self._payments.count_captured()

        revenue_rows = await self._bookings.aggregate_revenue_by_service()
        revenue_by_service = [
            {
                "service": row["_id"],
                "bookings": row["count"],
                "revenue": row["revenue"],
            }
            for row in revenue_rows
        ]

        today = datetime.now(timezone.utc)
        days = _DAILY_SERIES_DAYS
        thirty_days_ago = (today - timedelta(days=days - 1)).strftime("%Y-%m-%d")
        today_str = today.strftime("%Y-%m-%d")

        daily_bookings = await self._bookings.aggregate_daily_counts(
            thirty_days_ago, today_str
        )
        daily_series = [
            {
                "date": (today - timedelta(days=days - 1 - i)).strftime("%Y-%m-%d"),
                "bookings": daily_bookings.get(
                    (today - timedelta(days=days - 1 - i)).strftime("%Y-%m-%d"), 0
                ),
            }
            for i in range(days)
        ]

        daily_revenue = await self._payments.aggregate_daily_captured_amount(
            today - timedelta(days=days - 1)
        )
        revenue_series = [
            {
                "date": (today - timedelta(days=days - 1 - i)).strftime("%Y-%m-%d"),
                "revenue": daily_revenue.get(
                    (today - timedelta(days=days - 1 - i)).strftime("%Y-%m-%d"), 0
                ),
            }
            for i in range(days)
        ]

        return {
            "total_users": total_users,
            "total_bookings": total_bookings,
            "total_payments": total_payments,
            "revenue_by_service": revenue_by_service,
            "daily_bookings": daily_series,
            "daily_revenue": revenue_series,
        }
