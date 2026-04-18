"""Public endpoint for free Kundli report generation.

The endpoint returns 202 Accepted as soon as the request is validated and
rate-limited. Chart calculation, PDF rendering, email delivery and the final
DB write all run in a FastAPI BackgroundTask after the response is sent. This
keeps every request well under the 30-second API Gateway HTTP API integration
timeout, which was being hit because PDF generation alone exceeds 30s on a
0.25 vCPU Fargate task.
"""

from __future__ import annotations

import traceback
from datetime import datetime, timedelta, timezone

from bson import ObjectId
from fastapi import APIRouter, BackgroundTasks, HTTPException, Query
from fastapi.responses import Response

from app.database import get_db
from app.models.kundli import KundliInDB, KundliRequest
from app.services.kundli_calculator import build_chart
from app.services.kundli_pdf import generate_pdf
from app.services.report_sections import load_report_sections

router = APIRouter(prefix="/api/kundli", tags=["Kundli"])

MAX_PER_EMAIL_PER_DAY = 10


async def _generate_and_email(record_id: ObjectId, req: KundliRequest) -> None:
    """Background work: calculate chart, render PDF, email it, mark record done.

    Runs after the HTTP response has already been returned. Any failure is
    logged to CloudWatch and persisted on the kundli record so it surfaces in
    the admin dashboard.
    """
    db = get_db()
    try:
        # Load admin section toggles (free tier = sections where is_paid=False).
        sections_models = await load_report_sections()
        free_sections = [
            s.model_dump() for s in sections_models
            if s.enabled and not s.is_paid
        ]

        chart_data = build_chart(
            name=req.name,
            gender=req.gender,
            dob=req.dob,
            tob=req.tob,
            lat=req.lat,
            lon=req.lon,
            place_name=req.place_name,
        )
        # Attach user's browser timezone for the PDF printing date
        chart_data["user_timezone"] = req.timezone or "Asia/Kolkata"

        pdf_bytes = generate_pdf(chart_data, sections=free_sections)

        from app.services.email_service import send_kundli_report
        await send_kundli_report(req.email, req.name, pdf_bytes)

        await db.kundlis.update_one(
            {"_id": record_id},
            {"$set": {"chart_data": chart_data, "status": "generated"}},
        )
    except Exception as e:
        traceback.print_exc()
        await db.kundlis.update_one(
            {"_id": record_id},
            {"$set": {"status": "failed", "error": str(e)[:500]}},
        )


@router.post("/generate", status_code=202)
async def generate_kundli(req: KundliRequest, background_tasks: BackgroundTasks):
    """Queue a Kundli report for generation.

    Returns 202 Accepted immediately. The actual chart calculation, PDF
    rendering and email delivery run as a background task. The user receives
    the report by email when it's ready (typically under a minute).
    """
    db = get_db()

    # Rate limit: max 10 per email per 24h. Counts both pending and completed
    # records so a user spamming the form can't queue 100 background tasks.
    since = datetime.now(timezone.utc) - timedelta(hours=24)
    count = await db.kundlis.count_documents(
        {"email": req.email, "created_at": {"$gte": since}}
    )
    if count >= MAX_PER_EMAIL_PER_DAY:
        raise HTTPException(
            status_code=429,
            detail="You have reached the maximum number of free reports per day. Please try again tomorrow.",
        )

    # Insert a pending record up-front so the rate-limit query above includes
    # in-flight tasks and so admin can see failed runs in the dashboard.
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
    )
    insert_result = await db.kundlis.insert_one(record.model_dump())

    # Schedule the heavy work to run after the response is sent.
    background_tasks.add_task(_generate_and_email, insert_result.inserted_id, req)

    return {"message": "Your Kundli report is being generated and will arrive in your email within a minute."}


@router.get("/preview")
async def preview_kundli(
    name: str = Query("Preview User"),
    gender: str = Query("male"),
    dob: str = Query("1988-11-11"),
    tob: str = Query("12:55"),
    lat: float = Query(22.3072),
    lon: float = Query(73.1812),
    place_name: str = Query("Vadodara, Gujarat, India"),
    timezone: str = Query("Asia/Kolkata"),
):
    """Instant PDF preview — returns the PDF directly in the browser.

    No email, no background task, no rate limit, no DB write. Designed for
    fast layout iteration during development. Bookmark the URL and refresh
    after each deploy to see changes immediately.

    **Disabled in production.** Only works when APP_ENV is not "production".

    Example:
      /api/kundli/preview?name=Nandish+Dave&dob=1988-11-11&tob=12:55&lat=21.7333&lon=70.6167
    """
    import os
    if os.environ.get("APP_ENV", "").lower() == "production":
        raise HTTPException(status_code=404, detail="Not found")

    try:
        sections_models = await load_report_sections()
        free_sections = [
            s.model_dump() for s in sections_models
            if s.enabled and not s.is_paid
        ]

        chart_data = build_chart(
            name=name, gender=gender, dob=dob, tob=tob,
            lat=lat, lon=lon, place_name=place_name,
        )
        chart_data["user_timezone"] = timezone
        pdf_bytes = generate_pdf(chart_data, sections=free_sections)

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"inline; filename=Kundli_Preview_{name.replace(' ', '_')}.pdf"},
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Preview failed: {str(e)[:200]}")
