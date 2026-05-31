"""Admin services CRUD — manage the priced catalogue at runtime.

GET endpoints are public so the frontend can render the pricing page from
the same source of truth that the booking flow uses. Mutations are
admin-only.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.dependencies import get_service_repository, require_admin
from app.models.service import Service, ServiceResponse
from app.repositories.service_repository import ServiceRepository
from app.use_cases.services import (
    DeleteService,
    GetService,
    ListServices,
    UpsertService,
)

router = APIRouter(prefix="/api/services", tags=["Services"])


# ── Use-case factories ────────────────────────────────────────────────────


def _list_use_case(
    repo: ServiceRepository = Depends(get_service_repository),
) -> ListServices:
    return ListServices(repo)


def _get_use_case(
    repo: ServiceRepository = Depends(get_service_repository),
) -> GetService:
    return GetService(repo)


def _upsert_use_case(
    repo: ServiceRepository = Depends(get_service_repository),
) -> UpsertService:
    return UpsertService(repo)


def _delete_use_case(
    repo: ServiceRepository = Depends(get_service_repository),
) -> DeleteService:
    return DeleteService(repo)


# ── Endpoints ────────────────────────────────────────────────────────────


@router.get("", response_model=list[ServiceResponse])
async def list_services(use_case: ListServices = Depends(_list_use_case)):
    services = await use_case.execute()
    return [ServiceResponse(**s.model_dump()) for s in services]


@router.get("/{slug}", response_model=ServiceResponse)
async def get_service(
    slug: str,
    use_case: GetService = Depends(_get_use_case),
):
    service = await use_case.execute(slug)
    return ServiceResponse(**service.model_dump())


@router.put("/{slug}", response_model=ServiceResponse)
async def upsert_service(
    slug: str,
    payload: Service,
    _admin: dict = Depends(require_admin),
    use_case: UpsertService = Depends(_upsert_use_case),
):
    saved = await use_case.execute(slug=slug, payload=payload)
    return ServiceResponse(**saved.model_dump())


@router.delete("/{slug}")
async def delete_service(
    slug: str,
    _admin: dict = Depends(require_admin),
    use_case: DeleteService = Depends(_delete_use_case),
):
    await use_case.execute(slug)
    return {"message": "Removed"}
