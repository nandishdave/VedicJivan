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

from app.dependencies import get_message_queue
from app.infrastructure.logging import get_logger
from app.infrastructure.queue import MessageQueue
from app.models.unshakable import UnshakableRequest
from app.services.unshakable_finder import find_unshakable

logger = get_logger(__name__)

router = APIRouter(prefix="/api/unshakable", tags=["Unshakable"])


@router.post("/find", status_code=202)
async def find_endpoint(
    req: UnshakableRequest,
    queue: MessageQueue = Depends(get_message_queue),
) -> dict:
    """Queue a week-scale unshakable search; the worker emails the ranked results."""
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
