"""Public endpoint for the Auspicious Birth-Time (Muhurta) calculator.

Synchronous request/response (unlike the Kundli flow): the analysis is CPU-bound
but bounded (~12 charts) and returns JSON directly. Thin router — the engine
lives in `app/services/muhurta.py` and the use case in `app/use_cases/muhurta.py`.
"""
from __future__ import annotations

import os

from fastapi import APIRouter, Depends, HTTPException

from app.infrastructure.logging import get_logger
from app.models.muhurta import BirthMuhurtaRequest
# Module-scope so tests can patch `app.routers.muhurta.build_muhurta_chart` / `analyze_birth_muhurta`.
from app.services.muhurta import analyze_birth_muhurta, build_muhurta_chart
from app.use_cases.muhurta import AnalyzeBirthMuhurta

logger = get_logger(__name__)

router = APIRouter(prefix="/api/muhurta", tags=["Muhurta"])


def _analyze_use_case() -> AnalyzeBirthMuhurta:
    # Fresh each call so test patches on the module globals are honoured.
    return AnalyzeBirthMuhurta(chart_fn=build_muhurta_chart, analyze=analyze_birth_muhurta)


@router.post("/birth")
async def birth_muhurta(
    req: BirthMuhurtaRequest,
    use_case: AnalyzeBirthMuhurta = Depends(_analyze_use_case),
) -> dict:
    """Rank the day's rising Lagnas with a per-life-aspect verdict for each."""
    try:
        return await use_case.execute(
            date=req.date,
            lat=req.lat,
            lon=req.lon,
            place_name=req.place_name,
            priorities=req.priorities,
        )
    except Exception as e:  # noqa: BLE001
        logger.exception("Birth muhurta analysis failed")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)[:200]}")


@router.get("/birth/preview")
async def birth_muhurta_preview(
    date: str,
    lat: float = 21.7333,
    lon: float = 70.6167,
    place_name: str = "Jetpur, Gujarat, India",
    use_case: AnalyzeBirthMuhurta = Depends(_analyze_use_case),
) -> dict:
    """Dev preview (GET) — disabled in production, mirrors the kundli preview."""
    if os.environ.get("APP_ENV", "").lower() == "production":
        raise HTTPException(status_code=404, detail="Not found")
    return await use_case.execute(date=date, lat=lat, lon=lon, place_name=place_name)
