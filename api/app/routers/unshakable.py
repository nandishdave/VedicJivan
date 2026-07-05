"""Public endpoint for the Unshakable Chart Finder (week-scale).

The scan is heavy (real Shadbala over every rising Lagna of the range), so POST
enqueues onto the SAME Kundli SQS queue (``type="unshakable"``) and the Lambda
worker runs the funnel + emails the ranked results. Returns 202 immediately. A
dev GET preview runs a tiny range synchronously for local inspection.
"""
from __future__ import annotations

import os

from fastapi import APIRouter, Depends, HTTPException
from fastapi.concurrency import run_in_threadpool

from app.config import settings
from app.dependencies import get_message_queue, get_rate_limit_repository
from app.infrastructure.logging import get_logger
from app.infrastructure.queue import MessageQueue
from app.models.unshakable import UnshakableRequest
from app.repositories.rate_limit_repository import RateLimitRepository
from app.services.unshakable_finder import find_unshakable
from app.use_cases.rate_limit import EnforceEmailRateLimit

logger = get_logger(__name__)

router = APIRouter(prefix="/api/unshakable", tags=["Unshakable"])


def _rate_limit(
    repo: RateLimitRepository = Depends(get_rate_limit_repository),
) -> EnforceEmailRateLimit:
    return EnforceEmailRateLimit(
        repo, action="unshakable",
        max_per_window=settings.MAX_UNSHAKABLE_PER_EMAIL_PER_DAY,
    )


@router.post("/find", status_code=202)
async def find_endpoint(
    req: UnshakableRequest,
    queue: MessageQueue = Depends(get_message_queue),
    rate_limit: EnforceEmailRateLimit = Depends(_rate_limit),
) -> dict:
    """Queue a week-scale unshakable search; the worker emails the ranked results."""
    await rate_limit.execute(req.email)  # per-email daily cap → 429 over limit
    await queue.send({"type": "unshakable", **req.model_dump()})
    return {
        "message": (
            "Your unshakable birth-time search is running. The ranked results will "
            "arrive in your email within a few minutes."
        )
    }


@router.get("/find/preview")
async def preview(
    start_date: str,
    lat: float = 21.7333,
    lon: float = 70.6167,
    place_name: str = "Jetpur, Gujarat, India",
    days: int = 1,
) -> dict:
    """Dev preview (GET, synchronous, capped at 2 days) — disabled in production."""
    if os.environ.get("APP_ENV", "").lower() == "production":
        raise HTTPException(status_code=404, detail="Not found")
    return await run_in_threadpool(
        find_unshakable, start_date=start_date, days=min(days, 2),
        lat=lat, lon=lon, place_name=place_name, mode="bruteforce",
    )
