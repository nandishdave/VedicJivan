"""Use case: analyse the auspicious birth-time windows for a date + place.

Thin wrapper around the muhurta engine. The heavy CPU work (12x build_chart +
ephemeris) is pushed to a worker thread so it doesn't block the API event loop.
The engine (`analyze`) is injected so tests can substitute a fake.
"""
from __future__ import annotations

from fastapi.concurrency import run_in_threadpool


class AnalyzeBirthMuhurta:
    def __init__(self, chart_fn, analyze) -> None:
        self._chart_fn = chart_fn
        self._analyze = analyze

    async def execute(
        self,
        *,
        date: str,
        lat: float,
        lon: float,
        place_name: str,
        priorities: list[str] | None = None,
    ) -> dict:
        return await run_in_threadpool(
            self._analyze,
            dob=date,
            lat=lat,
            lon=lon,
            place_name=place_name,
            chart_fn=self._chart_fn,
            priorities=priorities,
        )
