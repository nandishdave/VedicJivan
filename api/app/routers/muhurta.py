"""Public endpoint for the Auspicious Birth-Time (Muhurta) calculator.

The full analysis (12 charts incl. Shadbala) is too heavy for the API's gateway
timeout, so POST /api/muhurta/birth enqueues the job onto the SAME SQS queue the
Kundli flow uses (distinguished by `type: "muhurta"`); the Kundli Lambda worker
runs the full analysis on demand and emails the result. Returns 202 immediately —
the calculation is never simplified, and there's no fixed-cost server scaling.

A dev GET preview runs synchronously for local inspection.
"""
from __future__ import annotations

import os

from fastapi import APIRouter, Depends, HTTPException

from app.config import settings
from app.dependencies import get_message_queue, get_rate_limit_repository
from app.infrastructure.logging import get_logger
from app.infrastructure.queue import MessageQueue
from app.models.muhurta import BirthMuhurtaRequest
from app.repositories.rate_limit_repository import RateLimitRepository
# Module-scope so tests can patch these on `app.routers.muhurta`.
from app.services.muhurta import analyze_birth_muhurta, build_muhurta_chart
from app.use_cases.muhurta import AnalyzeBirthMuhurta
from app.use_cases.rate_limit import EnforceEmailRateLimit

logger = get_logger(__name__)

router = APIRouter(prefix="/api/muhurta", tags=["Muhurta"])


def _rate_limit(
    repo: RateLimitRepository = Depends(get_rate_limit_repository),
) -> EnforceEmailRateLimit:
    return EnforceEmailRateLimit(
        repo, action="muhurta", max_per_window=settings.MAX_MUHURTA_PER_EMAIL_PER_DAY
    )


@router.post("/birth", status_code=202)
async def birth_muhurta(
    req: BirthMuhurtaRequest,
    queue: MessageQueue = Depends(get_message_queue),
    rate_limit: EnforceEmailRateLimit = Depends(_rate_limit),
) -> dict:
    """Queue the full birth-muhurta analysis; the worker emails the result."""
    await rate_limit.execute(req.email)  # per-email daily cap → 429 over limit
    await queue.send({"type": "muhurta", **req.model_dump()})
    return {
        "message": (
            "Your auspicious birth-time analysis is being prepared and will arrive "
            "in your email within a few minutes."
        )
    }


def _analyze_use_case() -> AnalyzeBirthMuhurta:
    return AnalyzeBirthMuhurta(chart_fn=build_muhurta_chart, analyze=analyze_birth_muhurta)


@router.get("/birth/preview")
async def birth_muhurta_preview(
    date: str,
    lat: float = 21.7333,
    lon: float = 70.6167,
    place_name: str = "Jetpur, Gujarat, India",
    time: str | None = None,
    use_case: AnalyzeBirthMuhurta = Depends(_analyze_use_case),
) -> dict:
    """Dev preview (GET, synchronous) — disabled in production. Returns the full
    analysis JSON directly for local inspection."""
    if os.environ.get("APP_ENV", "").lower() == "production":
        raise HTTPException(status_code=404, detail="Not found")
    return await use_case.execute(date=date, lat=lat, lon=lon, place_name=place_name, time=time)
