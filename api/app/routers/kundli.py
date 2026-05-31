"""Public endpoint for free Kundli report generation.

The endpoint inserts a `pending` record + enqueues an SQS message for the
out-of-process Lambda worker to pick up, then returns 202 Accepted. The
Lambda runs the chart calculation, PDF rendering, and email delivery,
and writes the final state back to the same record.

This pattern replaced the original FastAPI BackgroundTask approach
because PDF generation on Playwright takes ~10-30 s per render and was
starving the API event loop on a 0.25 vCPU Fargate task.

This module is intentionally thin — every business rule (rate limit,
"what counts as enabled and free", error persistence) lives in
`app/use_cases/kundli.py`.
"""

from __future__ import annotations

import os

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response

from app.dependencies import get_kundli_repository, get_message_queue
from app.infrastructure.logging import get_logger
from app.infrastructure.queue import MessageQueue
from app.models.kundli import KundliRequest
# These imports are kept at module scope on purpose: tests patch them as
# `app.routers.kundli.build_chart` / `generate_pdf` / `load_report_sections`,
# and the render use case below resolves them lazily through this module's
# globals.
from app.repositories.kundli_repository import KundliRepository
from app.services.kundli_calculator import build_chart
from app.services.kundli_pdf import generate_pdf
from app.services.report_sections import load_report_sections
from app.use_cases.kundli import (
    QueueKundliGeneration,
    RenderKundliReport,
)

logger = get_logger(__name__)

router = APIRouter(prefix="/api/kundli", tags=["Kundli"])


# ── Use-case factories ────────────────────────────────────────────────────


def _queue_kundli_use_case(
    repo: KundliRepository = Depends(get_kundli_repository),
) -> QueueKundliGeneration:
    return QueueKundliGeneration(repo)


def _render_use_case() -> RenderKundliReport:
    # Construct fresh each call so mock.patch on the module globals here
    # (build_chart / generate_pdf / load_report_sections) is honoured.
    return RenderKundliReport(
        build_chart=build_chart,
        generate_pdf=generate_pdf,
        load_report_sections=load_report_sections,
    )


# ── Endpoints ────────────────────────────────────────────────────────────


@router.post("/generate", status_code=202)
async def generate_kundli(
    req: KundliRequest,
    use_case: QueueKundliGeneration = Depends(_queue_kundli_use_case),
    queue: MessageQueue = Depends(get_message_queue),
):
    """Queue a Kundli report for generation.

    Inserts a `pending` row + enqueues to SQS, then returns 202. The
    Lambda worker picks up the message, renders the PDF, and emails it.
    The user receives the report by email when it's ready (typically
    under a minute).
    """
    record_id = await use_case.execute(req)

    # If SQS enqueue fails, the pending row stays in Mongo — its TTL
    # (set inside QueueKundliGeneration) reaps it within 24 h. We
    # surface a 500 to the caller so they know to retry rather than
    # silently dropping the request.
    try:
        await queue.send({"record_id": str(record_id), **req.model_dump()})
    except Exception:
        logger.exception(
            "Failed to enqueue kundli generation for record_id=%s", record_id
        )
        raise HTTPException(
            status_code=500,
            detail="Could not queue your kundli report. Please try again.",
        )

    return {
        "message": (
            "Your Kundli report is being generated and will arrive in your "
            "email within a minute."
        )
    }


@router.get("/preview")
async def preview_kundli(
    name: str = Query("Nandish Dave"),
    gender: str = Query("male"),
    dob: str = Query("1988-11-11"),
    tob: str = Query("12:55"),
    lat: float = Query(21.7333),
    lon: float = Query(70.6167),
    place_name: str = Query("Jetpur, Gujarat, India"),
    timezone: str = Query("Asia/Kolkata"),
):
    """Instant PDF preview — returns the PDF directly in the browser.

    No email, no background task, no rate limit, no DB write. Designed for
    fast layout iteration during development. Bookmark the URL and refresh
    after each deploy to see changes immediately.

    **Disabled in production.** Only works when APP_ENV is not "production".
    """
    if os.environ.get("APP_ENV", "").lower() == "production":
        raise HTTPException(status_code=404, detail="Not found")

    try:
        _, pdf_bytes = await _render_use_case().execute(
            name=name,
            gender=gender,
            dob=dob,
            tob=tob,
            lat=lat,
            lon=lon,
            place_name=place_name,
            timezone=timezone,
        )
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": (
                    f"inline; filename=Kundli_Preview_{name.replace(' ', '_')}.pdf"
                )
            },
        )
    except Exception as e:
        logger.exception("Kundli preview failed")
        raise HTTPException(status_code=500, detail=f"Preview failed: {str(e)[:200]}")
