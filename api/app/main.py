from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import close_db, connect_db
from app.routers import admin, auth, availability, bookings, payments


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()


app = FastAPI(
    title="VedicJivan API",
    description="Backend API for VedicJivan booking, payments, and admin",
    version="1.1.0",
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


@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "VedicJivan API"}
