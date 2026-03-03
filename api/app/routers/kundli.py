"""Public endpoint for free Kundli report generation."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException

from app.database import get_db
from app.models.kundli import KundliInDB, KundliRequest
from app.services.kundli_calculator import build_chart
from app.services.kundli_pdf import generate_pdf

router = APIRouter(prefix="/api/kundli", tags=["Kundli"])

MAX_PER_EMAIL_PER_DAY = 3


@router.post("/generate")
async def generate_kundli(req: KundliRequest):
    db = get_db()

    # Rate limit: max 3 per email per 24h
    since = datetime.now(timezone.utc) - timedelta(hours=24)
    count = await db.kundlis.count_documents(
        {"email": req.email, "created_at": {"$gte": since}}
    )
    if count >= MAX_PER_EMAIL_PER_DAY:
        raise HTTPException(
            status_code=429,
            detail="You have reached the maximum number of free reports per day. Please try again tomorrow.",
        )

    # Calculate chart
    try:
        chart_data = build_chart(
            name=req.name,
            gender=req.gender,
            dob=req.dob,
            tob=req.tob,
            lat=req.lat,
            lon=req.lon,
            place_name=req.place_name,
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to calculate chart: {e}")

    # Generate PDF
    try:
        pdf_bytes = generate_pdf(chart_data)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {e}")

    # Send email with PDF attachment
    try:
        from app.services.email_service import send_kundli_report
        await send_kundli_report(req.email, req.name, pdf_bytes)
    except Exception as e:
        print(f"[KUNDLI EMAIL ERROR] {e}")
        # Don't fail the whole request if email fails — save the record anyway

    # Save to MongoDB
    record = KundliInDB(
        name=req.name,
        gender=req.gender,
        dob=req.dob,
        tob=req.tob,
        lat=req.lat,
        lon=req.lon,
        place_name=req.place_name,
        email=req.email,
        chart_data=chart_data,
        status="generated",
    )
    await db.kundlis.insert_one(record.model_dump())

    return {"message": "Your Kundli report has been sent to your email!"}
