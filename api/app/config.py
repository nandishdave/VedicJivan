"""Pydantic Settings — every tunable lives here.

Magic numbers and runtime configuration are read from the environment so
operators can change behaviour without touching the code (and so each
deploy environment — dev / staging / prod — can pick its own values).
Each Settings field documents what it controls and what its sensible
default is.
"""

from __future__ import annotations

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ── Environment / URLs ──
    APP_ENV: str = "development"
    APP_URL: str = "http://localhost:8000"
    FRONTEND_URL: str = "http://localhost:3000"

    # Comma-separated list of additional allowed origins beyond FRONTEND_URL.
    # The default keeps the production + staging hostnames trusted across
    # environments (mirrors the previous hard-coded list). Override per env
    # to lock down further.
    EXTRA_CORS_ORIGINS: str = (
        "https://vedicjivan.nandishdave.world,"
        "https://vedicjivan-test.nandishdave.world"
    )

    # ── Database ──
    MONGODB_URI: str = "mongodb://mongo:27017/vedicjivan"

    # ── Auth ──
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ── Stripe ──
    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""

    # ── Email ──
    RESEND_API_KEY: str = ""
    EMAIL_FROM: str = "VedicJivan <noreply@nandishdave.world>"
    ADMIN_EMAIL: str = "vedic.jivan33@gmail.com"

    # ── Internal endpoints (booking reminders, etc.) ──
    INTERNAL_SECRET: str = ""

    # ── Google Calendar (admin only) ──
    GOOGLE_CALENDAR_CREDENTIALS: str = ""  # base64-encoded service account JSON
    GOOGLE_CALENDAR_ID: str = ""

    # ── Booking domain rules ──
    # How long a pending booking stays "alive" before slot lookup ignores it.
    PENDING_EXPIRY_MINUTES: int = Field(default=15, ge=1, le=1440)
    # Reschedule cutoff — bookings closer than this can't be moved.
    RESCHEDULE_CUTOFF_HOURS: int = Field(default=24, ge=0, le=720)
    # Default IANA timezone for slot bookings (Asia/Kolkata in production).
    BOOKING_TIMEZONE: str = "Asia/Kolkata"
    # Slot length used by the public availability lookup.
    SLOT_DURATION_MINUTES: int = Field(default=30, ge=5, le=240)

    # ── Kundli rate limits ──
    MAX_KUNDLI_PER_EMAIL_PER_DAY: int = Field(default=10, ge=1, le=1000)
    KUNDLI_RATE_LIMIT_WINDOW_HOURS: int = Field(default=24, ge=1, le=720)

    # ── Admin analytics ──
    # Days of trailing data to surface in /api/admin/stats.
    ADMIN_DAILY_SERIES_DAYS: int = Field(default=30, ge=1, le=365)
    # Limit of recent bookings on /api/admin/dashboard.
    ADMIN_RECENT_BOOKINGS_LIMIT: int = Field(default=10, ge=1, le=100)

    @field_validator("EXTRA_CORS_ORIGINS")
    @classmethod
    def _strip_origins(cls, v: str) -> str:
        return (v or "").strip()

    def cors_origins(self) -> list[str]:
        """Build the final CORS allow-list.

        Always includes FRONTEND_URL. In non-production, also includes the
        common localhost dev ports. EXTRA_CORS_ORIGINS (comma-separated)
        is appended for any environment-specific entries (e.g. staging
        domain). Returns a deduplicated list, preserving insertion order.
        """
        origins: list[str] = [self.FRONTEND_URL]
        if self.APP_ENV.lower() != "production":
            origins.extend(["http://localhost:3000", "http://localhost:3001"])
        for raw in self.EXTRA_CORS_ORIGINS.split(","):
            entry = raw.strip()
            if entry:
                origins.append(entry)
        # Deduplicate while preserving order.
        seen: set[str] = set()
        result: list[str] = []
        for o in origins:
            if o not in seen:
                seen.add(o)
                result.append(o)
        return result

    class Config:
        env_file = ".env"


settings = Settings()
