from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import close_db, connect_db
from app.domain.exceptions import (
    AccessDeniedError,
    AuthenticationFailedError,
    DomainError,
    EntityNotFoundError,
    RateLimitExceededError,
)
from app.infrastructure.logging import configure_root_logging
from app.repositories.service_repository import MongoServiceRepository
from app.routers import (
    admin,
    auth,
    availability,
    bookings,
    internal,
    kundli,
    payments,
    services,
)
from app.services.default_services import DEFAULT_SERVICES

configure_root_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    # Seed the services catalogue from in-code defaults if empty.
    # Idempotent — boots are cheap once seeded.
    try:
        from app.database import get_db

        repo = MongoServiceRepository(get_db())
        await repo.seed_if_empty(DEFAULT_SERVICES)
    except Exception:  # noqa: BLE001 — never block startup on seed failure.
        pass
    # Index creation lives in `scripts/migrate_indexes.py` (run by CI as
    # an `ecs run-task` step before each deploy). The API process must not
    # be the one to create indexes — building one against a large collection
    # blocks reads on a foreground build.
    yield
    await close_db()


app = FastAPI(
    title="VedicJivan API",
    description="Backend API for VedicJivan booking, payments, and admin",
    version="1.3.0",
    lifespan=lifespan,
)

# CORS — see `Settings.cors_origins()` for the build rule (FRONTEND_URL +
# localhost dev ports outside production + EXTRA_CORS_ORIGINS env entries).
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(availability.router)
app.include_router(bookings.router)
app.include_router(payments.router)
app.include_router(admin.router)
app.include_router(internal.router)
app.include_router(kundli.router)
app.include_router(services.router)


@app.get("/api/health")
async def health():
    """Back-compat alias for /api/health/live. Kept stable for any
    external callers (uptime monitors, manual curl). New infra (ECS
    task health check) should target /api/health/ready instead."""
    return {"status": "ok", "service": "VedicJivan API"}


@app.get("/api/health/live")
async def liveness():
    """Liveness: process is running. No DB or external-dependency
    check — failing this means the container should be restarted."""
    return {"status": "ok"}


@app.get("/api/health/ready")
async def readiness():
    """Readiness: process is up AND can talk to its hard dependencies
    (Mongo). Returning 503 tells the load balancer / ECS to stop
    routing new traffic to this task without restarting it. The task
    auto-rejoins once the next ping succeeds.

    We DON'T gate readiness on Stripe / Resend / Google Calendar —
    those are downstream best-effort dependencies, not hot-path
    requirements. Mongo is the one thing every API call needs."""
    from fastapi import HTTPException

    from app.database import get_db

    try:
        # `command("ping")` is the cheapest possible round-trip to Mongo —
        # no auth check, no collection scan, just "are you there".
        await get_db().command("ping")
    except Exception as e:  # noqa: BLE001 — any failure means not-ready.
        raise HTTPException(status_code=503, detail=f"DB unreachable: {e}")
    return {"status": "ready"}


# ── Domain-exception → HTTP translation ─────────────────────────────────────
# Use cases raise pure domain exceptions (no FastAPI imports). The framework
# boundary translates them to HTTP responses here so business code stays
# transport-agnostic.

@app.exception_handler(EntityNotFoundError)
async def _entity_not_found_handler(_req: Request, exc: EntityNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(AccessDeniedError)
async def _access_denied_handler(_req: Request, exc: AccessDeniedError):
    return JSONResponse(status_code=403, content={"detail": str(exc)})


@app.exception_handler(AuthenticationFailedError)
async def _authentication_failed_handler(_req: Request, exc: AuthenticationFailedError):
    return JSONResponse(
        status_code=401,
        content={"detail": str(exc)},
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.exception_handler(RateLimitExceededError)
async def _rate_limit_handler(_req: Request, exc: RateLimitExceededError):
    return JSONResponse(status_code=429, content={"detail": str(exc)})


@app.exception_handler(DomainError)
async def _domain_error_handler(_req: Request, exc: DomainError):
    """Catch-all for any DomainError subclass not handled above. Maps to 400."""
    return JSONResponse(status_code=400, content={"detail": str(exc)})
