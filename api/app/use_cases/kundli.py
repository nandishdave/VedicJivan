"""Kundli use cases — application workflows for free Kundli reports.

Use cases:
  - QueueKundliGeneration  — rate-limit + insert pending record
  - RenderKundliReport     — load sections, build chart, render PDF
  - ProcessKundliReport    — orchestrates the background work
                             (render + email + persist)

The router stays thin; it owns scheduling the background task and the
preview-only HTTP semantics. Domain rules (rate limit, what counts as
"pending") live here.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from bson import ObjectId

from app.config import settings
from app.domain.exceptions import RateLimitExceededError
from app.infrastructure.logging import get_logger
from app.models.kundli import KundliInDB, KundliRequest
from app.repositories.kundli_repository import KundliRepository

logger = get_logger(__name__)


# ── QueueKundliGeneration ──────────────────────────────────────────────────


class QueueKundliGeneration:
    """Validate the per-email rate limit and persist a `pending` record.

    The router schedules `ProcessKundliReport.execute(record_id, req)` as a
    BackgroundTask after this returns, so the HTTP response can come back
    well within the 30-second API Gateway timeout.
    """

    def __init__(
        self,
        kundli_repo: KundliRepository,
        max_per_email_per_day: int | None = None,
    ) -> None:
        self._repo = kundli_repo
        self._max_per_email_per_day = (
            max_per_email_per_day
            if max_per_email_per_day is not None
            else settings.MAX_KUNDLI_PER_EMAIL_PER_DAY
        )

    async def execute(self, req: KundliRequest) -> ObjectId:
        since = datetime.now(timezone.utc) - timedelta(
            hours=settings.KUNDLI_RATE_LIMIT_WINDOW_HOURS
        )
        count = await self._repo.count_for_email_since(req.email, since)
        if count >= self._max_per_email_per_day:
            raise RateLimitExceededError(
                "You have reached the maximum number of free reports per day. "
                "Please try again tomorrow."
            )

        # 24h TTL window. Mongo's TTL background runs every ~60s; if SQS
        # never delivered the message or the worker crashed, this orphan
        # gets reaped automatically — no admin cleanup ritual.
        expires_at = datetime.now(timezone.utc) + timedelta(hours=24)
        record = KundliInDB(
            name=req.name,
            gender=req.gender,
            dob=req.dob,
            tob=req.tob,
            lat=req.lat,
            lon=req.lon,
            place_name=req.place_name,
            email=req.email,
            chart_data={},
            status="pending",
            expires_at=expires_at,
        )
        return await self._repo.insert_pending(record)


# ── RenderKundliReport ─────────────────────────────────────────────────────


class RenderKundliReport:
    """Pure render: load enabled free sections, build the chart, render PDF.

    No DB writes, no email. Used both by the background processor and the
    dev preview endpoint. Collaborators are injected so tests can substitute.
    """

    def __init__(
        self,
        build_chart,
        generate_pdf,
        load_report_sections,
    ) -> None:
        self._build_chart = build_chart
        self._generate_pdf = generate_pdf
        self._load_report_sections = load_report_sections

    async def execute(
        self,
        *,
        name: str,
        gender: str,
        dob: str,
        tob: str,
        lat: float,
        lon: float,
        place_name: str,
        timezone: str | None = None,
    ) -> tuple[dict, bytes]:
        sections_models = await self._load_report_sections()
        free_sections = [
            s.model_dump() for s in sections_models if s.enabled and not s.is_paid
        ]

        chart_data = self._build_chart(
            name=name,
            gender=gender,
            dob=dob,
            tob=tob,
            lat=lat,
            lon=lon,
            place_name=place_name,
        )
        chart_data["user_timezone"] = timezone or "Asia/Kolkata"

        pdf_bytes = self._generate_pdf(chart_data, sections=free_sections)
        return chart_data, pdf_bytes


# ── ProcessKundliReport (background work) ─────────────────────────────────


class ProcessKundliReport:
    """Background workflow: render the report, email it, mark the record.

    Failure path persists `status='failed'` with the truncated error so the
    admin dashboard can surface it. The function never re-raises — Starlette
    BackgroundTasks would otherwise swallow exceptions silently anyway.
    """

    def __init__(
        self,
        kundli_repo: KundliRepository,
        render_use_case: RenderKundliReport,
        send_email,  # async callable: (to_email, name, pdf_bytes) -> None
    ) -> None:
        self._repo = kundli_repo
        self._render = render_use_case
        self._send_email = send_email

    async def execute(self, record_id: ObjectId, req: KundliRequest) -> None:
        try:
            chart_data, pdf_bytes = await self._render.execute(
                name=req.name,
                gender=req.gender,
                dob=req.dob,
                tob=req.tob,
                lat=req.lat,
                lon=req.lon,
                place_name=req.place_name,
                timezone=req.timezone,
            )
            await self._send_email(req.email, req.name, pdf_bytes)
            await self._repo.mark_generated(record_id, chart_data=chart_data)
        except Exception as e:
            logger.exception("Kundli generation failed for record_id=%s", record_id)
            await self._repo.mark_failed(record_id, error=str(e))
