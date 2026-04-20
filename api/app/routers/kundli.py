"""Public endpoint for free Kundli report generation.

The endpoint returns 202 Accepted as soon as the request is rate-limited
and a pending record is inserted. The chart calculation, PDF rendering,
email delivery and final DB write all run in a FastAPI BackgroundTask
after the response is sent. This keeps every request well under the
30-second API Gateway HTTP API integration timeout, which was being hit
because PDF generation alone exceeds 30s on a 0.25 vCPU Fargate task.

This module is intentionally thin — every business rule (rate limit,
"what counts as enabled and free", error persistence) lives in
`app/use_cases/kundli.py`.
"""

from __future__ import annotations

import os
import traceback

from bson import ObjectId
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from fastapi.responses import Response

from app.database import get_db
from app.dependencies import get_kundli_repository
from app.models.kundli import KundliRequest
# These imports are kept at module scope on purpose: tests patch them as
# `app.routers.kundli.build_chart` / `generate_pdf` / `load_report_sections`,
# and use cases below resolve them lazily through this module's globals.
from app.repositories.kundli_repository import (
    KundliRepository,
    MongoKundliRepository,
)
from app.services.kundli_calculator import build_chart
from app.services.kundli_pdf import generate_pdf
from app.services.report_sections import load_report_sections
from app.use_cases.kundli import (
    ProcessKundliReport,
    QueueKundliGeneration,
    RenderKundliReport,
)

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


# ── Background worker ────────────────────────────────────────────────────


async def _generate_and_email(record_id: ObjectId, req: KundliRequest) -> None:
    """Background work: chart -> PDF -> email -> mark record done.

    Kept as a router-level coroutine because FastAPI BackgroundTasks need a
    callable here, and tests import this name to exercise the success and
    failure paths directly. The actual business logic lives in
    `ProcessKundliReport`.
    """
    # Deferred import so test patches on `app.services.email_service.send_kundli_report`
    # (the source location) are applied each call.
    from app.services.email_service import send_kundli_report

    repo = MongoKundliRepository(get_db())
    processor = ProcessKundliReport(
        kundli_repo=repo,
        render_use_case=_render_use_case(),
        send_email=send_kundli_report,
    )
    await processor.execute(record_id, req)


# ── Endpoints ────────────────────────────────────────────────────────────


@router.post("/generate", status_code=202)
async def generate_kundli(
    req: KundliRequest,
    background_tasks: BackgroundTasks,
    use_case: QueueKundliGeneration = Depends(_queue_kundli_use_case),
):
    """Queue a Kundli report for generation.

    Returns 202 Accepted immediately. The actual chart calculation, PDF
    rendering and email delivery run as a background task. The user
    receives the report by email when it's ready (typically under a minute).
    """
    record_id = await use_case.execute(req)
    background_tasks.add_task(_generate_and_email, record_id, req)
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
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Preview failed: {str(e)[:200]}")
