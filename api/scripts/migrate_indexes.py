"""Idempotent index migration for VedicJivan's MongoDB.

Run order in CI:
  1. Build + push the new API Docker image to ECR.
  2. Run this script (`ecs run-task` with the freshly-built image).
  3. Force ECS service redeploy to pick up the new image.

Doing it in that order means: indexes are in place before the new task
version starts answering requests, and a migration failure aborts the
deploy without ever swapping the live image.

Each repository owns its own `ensure_indexes()`; this script is a thin
orchestrator that calls them all. Add a new repo's indexes by giving the
repo an `ensure_indexes()` method and adding the factory below.

Mongo `create_index` is idempotent — re-running the script is safe.
Changing an existing index spec (e.g. adding a field to a compound) does
NOT drop the old one; you must drop it manually in Atlas.
"""

from __future__ import annotations

import asyncio
import logging
import sys
from typing import Awaitable, Callable

from app.database import close_db, connect_db, get_db
from app.repositories.booking_repository import MongoBookingRepository
from app.repositories.kundli_repository import MongoKundliRepository
from app.repositories.payment_repository import MongoPaymentRepository
from app.repositories.processed_event_repository import (
    MongoProcessedEventRepository,
)
from app.repositories.rate_limit_repository import MongoRateLimitRepository
from app.repositories.service_repository import MongoServiceRepository
from app.repositories.unavailability_repository import (
    MongoUnavailabilityRepository,
)
from app.repositories.user_repository import MongoUserRepository

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("migrate_indexes")


def _repo_targets(db) -> list[tuple[str, Callable[[], Awaitable[None]]]]:
    """Each entry: (collection_name, awaitable that creates its indexes)."""
    return [
        ("bookings", MongoBookingRepository(db).ensure_indexes),
        ("payments", MongoPaymentRepository(db).ensure_indexes),
        ("kundlis", MongoKundliRepository(db).ensure_indexes),
        ("rate_limits", MongoRateLimitRepository(db).ensure_indexes),
        ("unavailability", MongoUnavailabilityRepository(db).ensure_indexes),
        ("services", MongoServiceRepository(db).ensure_indexes),
        ("users", MongoUserRepository(db).ensure_indexes),
        ("stripe_events", MongoProcessedEventRepository(db).ensure_indexes),
    ]


async def main() -> int:
    await connect_db()
    db = get_db()

    failures: list[str] = []
    for name, ensure in _repo_targets(db):
        try:
            await ensure()
            logger.info("indexes ensured for %s", name)
        except Exception as e:  # noqa: BLE001 — capture, continue, fail at end.
            logger.exception("index creation failed for %s: %s", name, e)
            failures.append(name)

    await close_db()

    if failures:
        logger.error("migration failed for: %s", ", ".join(failures))
        return 1
    logger.info("all indexes ensured")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
