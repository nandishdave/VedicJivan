"""Service-catalogue use cases.

  - GetServicePrice    — public lookup used by the booking flow
  - ListServices       — admin
  - GetService         — admin
  - UpsertService      — admin (create + update via slug PUT)
  - DeleteService      — admin

The use cases sit between the booking flow / admin UI and the repository.
Domain rules (slug must exist, can't delete in-use slugs) live here.
"""

from __future__ import annotations

from app.domain.exceptions import (
    BookingValidationError,
    EntityNotFoundError,
)
from app.models.service import Service
from app.repositories.service_repository import ServiceRepository
from app.services.default_services import resolve_price


# ── GetServicePrice ───────────────────────────────────────────────────────


class GetServicePrice:
    """Async pricing lookup that hits the DB.

    Returns `(price_inr, price_eur)`. Raises BookingValidationError on an
    unknown slug or a duration that the service doesn't sell.
    """

    def __init__(self, service_repo: ServiceRepository) -> None:
        self._repo = service_repo

    async def execute(
        self, *, service_slug: str, duration_minutes: int
    ) -> tuple[int, int]:
        service = await self._repo.find_by_slug(service_slug)
        if not service:
            raise BookingValidationError(f"Unknown service: {service_slug}")
        # resolve_price raises BookingValidationError (domain) directly — no
        # HTTP exception ever enters this layer.
        return resolve_price(service, duration_minutes)


# ── ListServices ──────────────────────────────────────────────────────────


class ListServices:
    def __init__(self, service_repo: ServiceRepository) -> None:
        self._repo = service_repo

    async def execute(self) -> list[Service]:
        return await self._repo.list_all()


# ── GetService ────────────────────────────────────────────────────────────


class GetService:
    def __init__(self, service_repo: ServiceRepository) -> None:
        self._repo = service_repo

    async def execute(self, slug: str) -> Service:
        service = await self._repo.find_by_slug(slug)
        if not service:
            raise EntityNotFoundError(f"Service not found: {slug}")
        return service


# ── UpsertService ─────────────────────────────────────────────────────────


class UpsertService:
    def __init__(self, service_repo: ServiceRepository) -> None:
        self._repo = service_repo

    async def execute(self, *, slug: str, payload: Service) -> Service:
        if payload.slug != slug:
            raise BookingValidationError(
                f"Slug mismatch: URL '{slug}' vs body '{payload.slug}'"
            )
        await self._repo.upsert(payload)
        saved = await self._repo.find_by_slug(slug)
        if not saved:
            # Should not happen unless the upsert failed silently.
            raise EntityNotFoundError(f"Service not found after upsert: {slug}")
        return saved


# ── DeleteService ─────────────────────────────────────────────────────────


class DeleteService:
    def __init__(self, service_repo: ServiceRepository) -> None:
        self._repo = service_repo

    async def execute(self, slug: str) -> None:
        deleted = await self._repo.delete_by_slug(slug)
        if deleted == 0:
            raise EntityNotFoundError(f"Service not found: {slug}")
