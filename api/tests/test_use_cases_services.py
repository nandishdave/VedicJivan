"""Use-case-level tests for the services catalogue.

Cover the pure logic without a FastAPI client by using an in-memory
ServiceRepository fake.
"""

from __future__ import annotations

import pytest

from app.domain.exceptions import (
    BookingValidationError,
    EntityNotFoundError,
)
from app.models.service import Service, ServiceDuration
from app.services.default_services import DEFAULT_SERVICES
from app.use_cases.services import (
    DeleteService,
    GetService,
    GetServicePrice,
    ListServices,
    UpsertService,
)


class FakeServiceRepo:
    def __init__(self, initial: list[Service] | None = None) -> None:
        self._by_slug = {s.slug: s for s in (initial or [])}

    async def list_all(self) -> list[Service]:
        return list(self._by_slug.values())

    async def find_by_slug(self, slug: str) -> Service | None:
        return self._by_slug.get(slug)

    async def upsert(self, service: Service) -> None:
        self._by_slug[service.slug] = service

    async def delete_by_slug(self, slug: str) -> int:
        if slug in self._by_slug:
            del self._by_slug[slug]
            return 1
        return 0

    async def seed_if_empty(self, defaults):
        if self._by_slug:
            return 0
        for s in defaults:
            self._by_slug[s.slug] = s
        return len(defaults)


# ── GetServicePrice ──


@pytest.mark.asyncio
async def test_get_price_known_service_and_duration():
    repo = FakeServiceRepo(initial=DEFAULT_SERVICES)
    use_case = GetServicePrice(repo)
    inr, eur = await use_case.execute(service_slug="call-consultation", duration_minutes=30)
    assert (inr, eur) == (1999, 29)


@pytest.mark.asyncio
async def test_get_price_unknown_service_raises_validation():
    repo = FakeServiceRepo()
    use_case = GetServicePrice(repo)
    with pytest.raises(BookingValidationError, match="Unknown service"):
        await use_case.execute(service_slug="nope", duration_minutes=30)


@pytest.mark.asyncio
async def test_get_price_report_service_uses_zero_duration_slot():
    repo = FakeServiceRepo(initial=DEFAULT_SERVICES)
    use_case = GetServicePrice(repo)
    # premium-kundli only sells "0" — any duration should map to that price.
    inr, eur = await use_case.execute(service_slug="premium-kundli", duration_minutes=15)
    assert (inr, eur) == (4999, 59)


@pytest.mark.asyncio
async def test_get_price_invalid_duration_for_session_service():
    repo = FakeServiceRepo(initial=DEFAULT_SERVICES)
    use_case = GetServicePrice(repo)
    # call-consultation sells 30/45/60 only — 90 should fail.
    with pytest.raises(BookingValidationError, match="not available"):
        await use_case.execute(service_slug="call-consultation", duration_minutes=90)


# ── List / Get / Upsert / Delete ──


@pytest.mark.asyncio
async def test_list_services_returns_all():
    repo = FakeServiceRepo(initial=DEFAULT_SERVICES)
    services = await ListServices(repo).execute()
    assert len(services) == len(DEFAULT_SERVICES)


@pytest.mark.asyncio
async def test_get_service_unknown_raises_not_found():
    repo = FakeServiceRepo()
    with pytest.raises(EntityNotFoundError):
        await GetService(repo).execute("nope")


@pytest.mark.asyncio
async def test_upsert_service_creates_or_updates():
    repo = FakeServiceRepo()
    payload = Service(
        slug="my-service",
        title="Brand New",
        durations=[ServiceDuration(duration_minutes=30, price_inr=100, price_eur=1)],
    )
    saved = await UpsertService(repo).execute(slug="my-service", payload=payload)
    assert saved.slug == "my-service"
    # Idempotent — second call updates in place.
    payload2 = Service(
        slug="my-service",
        title="Renamed",
        durations=[ServiceDuration(duration_minutes=30, price_inr=200, price_eur=2)],
    )
    saved2 = await UpsertService(repo).execute(slug="my-service", payload=payload2)
    assert saved2.title == "Renamed"
    assert saved2.durations[0].price_inr == 200


@pytest.mark.asyncio
async def test_upsert_service_slug_mismatch_raises_validation():
    repo = FakeServiceRepo()
    payload = Service(
        slug="from-body",
        durations=[ServiceDuration(duration_minutes=30, price_inr=10, price_eur=1)],
    )
    with pytest.raises(BookingValidationError, match="mismatch"):
        await UpsertService(repo).execute(slug="from-url", payload=payload)


@pytest.mark.asyncio
async def test_delete_service_unknown_raises_not_found():
    repo = FakeServiceRepo()
    with pytest.raises(EntityNotFoundError):
        await DeleteService(repo).execute("nope")


@pytest.mark.asyncio
async def test_delete_service_success_removes_entry():
    repo = FakeServiceRepo(
        initial=[
            Service(
                slug="x",
                durations=[ServiceDuration(duration_minutes=30, price_inr=10, price_eur=1)],
            )
        ]
    )
    await DeleteService(repo).execute("x")
    assert await repo.find_by_slug("x") is None


# ── seed_if_empty ──


@pytest.mark.asyncio
async def test_seed_if_empty_inserts_defaults_when_empty():
    repo = FakeServiceRepo()
    inserted = await repo.seed_if_empty(DEFAULT_SERVICES)
    assert inserted == len(DEFAULT_SERVICES)


@pytest.mark.asyncio
async def test_seed_if_empty_is_noop_when_populated():
    repo = FakeServiceRepo(
        initial=[
            Service(
                slug="x",
                durations=[ServiceDuration(duration_minutes=30, price_inr=10, price_eur=1)],
            )
        ]
    )
    inserted = await repo.seed_if_empty(DEFAULT_SERVICES)
    assert inserted == 0
