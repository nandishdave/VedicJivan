"""Per-email rate-limit use case for the public async-analysis endpoints.

Mirrors the Kundli per-email daily cap (``QueueKundliGeneration``) but for the
muhurta / unshakable endpoints, which persist no domain record of their own.
Counts recent requests for (email, action) and raises ``RateLimitExceededError``
(→ 429) over the cap; otherwise records the request.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from app.config import settings
from app.domain.exceptions import RateLimitExceededError
from app.repositories.rate_limit_repository import RateLimitRepository


class EnforceEmailRateLimit:
    def __init__(
        self,
        repo: RateLimitRepository,
        *,
        action: str,
        max_per_window: int,
        window_hours: int | None = None,
    ) -> None:
        self._repo = repo
        self._action = action
        self._max = max_per_window
        self._window_hours = (
            window_hours
            if window_hours is not None
            else settings.KUNDLI_RATE_LIMIT_WINDOW_HOURS
        )

    async def execute(self, email: str) -> None:
        since = datetime.now(timezone.utc) - timedelta(hours=self._window_hours)
        count = await self._repo.count_since(email, self._action, since)
        if count >= self._max:
            raise RateLimitExceededError(
                "You have reached today's limit for this tool. "
                "Please try again tomorrow."
            )
        await self._repo.record(email, self._action, ttl_hours=self._window_hours)
