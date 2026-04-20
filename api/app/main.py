from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import close_db, connect_db
from app.domain.exceptions import (
    AccessDeniedError,
    DomainError,
    EntityNotFoundError,
    RateLimitExceededError,
)
from app.infrastructure.logging import configure_root_logging
from app.routers import admin, auth, availability, bookings, internal, kundli, payments

configure_root_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()


app = FastAPI(
    title="VedicJivan API",
    description="Backend API for VedicJivan booking, payments, and admin",
    version="1.3.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL,
        "http://localhost:3000",
        "http://localhost:3001",
        "https://vedicjivan.nandishdave.world",
        "https://vedicjivan-test.nandishdave.world",
    ],
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


@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "VedicJivan API"}


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


@app.exception_handler(RateLimitExceededError)
async def _rate_limit_handler(_req: Request, exc: RateLimitExceededError):
    return JSONResponse(status_code=429, content={"detail": str(exc)})


@app.exception_handler(DomainError)
async def _domain_error_handler(_req: Request, exc: DomainError):
    """Catch-all for any DomainError subclass not handled above. Maps to 400."""
    return JSONResponse(status_code=400, content={"detail": str(exc)})
