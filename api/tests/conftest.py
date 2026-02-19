"""Shared test fixtures for the VedicJivan API test suite."""

import os
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from bson import ObjectId
from httpx import ASGITransport, AsyncClient

# Set test environment variables BEFORE importing app modules
os.environ["JWT_SECRET"] = "test-secret-key-for-unit-tests"
os.environ["RAZORPAY_KEY_ID"] = "rzp_test_key"
os.environ["RAZORPAY_KEY_SECRET"] = "rzp_test_secret"
os.environ["RESEND_API_KEY"] = ""
os.environ["ADMIN_EMAIL"] = "admin@test.com"
os.environ["MONGODB_URI"] = "mongodb://localhost:27017/test"

from app.main import app
from app.utils.security import create_access_token, hash_password


# ── Mock cursor helper ──


class MockCursor:
    """Simulates a Motor async cursor with .sort(), .limit(), and async iteration."""

    def __init__(self, documents: list[dict]):
        self._documents = list(documents)

    def sort(self, *args, **kwargs):
        return self

    def limit(self, *args, **kwargs):
        return self

    def __aiter__(self):
        return self._AsyncIterator(self._documents)

    class _AsyncIterator:
        def __init__(self, docs):
            self._docs = iter(docs)

        async def __anext__(self):
            try:
                return next(self._docs)
            except StopIteration:
                raise StopAsyncIteration


class MockAggregationCursor(MockCursor):
    """Adds .to_list() support for aggregate pipelines."""

    async def to_list(self, length=None):
        return self._documents


# ── Sample documents ──

USER_ID = ObjectId("507f1f77bcf86cd799439011")
ADMIN_ID = ObjectId("507f1f77bcf86cd799439012")
BOOKING_ID = ObjectId("507f1f77bcf86cd799439013")
PAYMENT_ID = ObjectId("507f1f77bcf86cd799439014")


@pytest.fixture
def sample_user_doc():
    return {
        "_id": USER_ID,
        "name": "Test User",
        "email": "test@example.com",
        "password_hash": hash_password("Password123"),
        "phone": "1234567890",
        "role": "user",
        "created_at": datetime.now(timezone.utc),
    }


@pytest.fixture
def sample_admin_doc():
    return {
        "_id": ADMIN_ID,
        "name": "Admin User",
        "email": "admin@example.com",
        "password_hash": hash_password("AdminPass123"),
        "phone": "9876543210",
        "role": "admin",
        "created_at": datetime.now(timezone.utc),
    }


@pytest.fixture
def sample_booking_doc():
    return {
        "_id": BOOKING_ID,
        "user_name": "Test User",
        "user_email": "test@example.com",
        "user_phone": "1234567890",
        "service_slug": "call-consultation",
        "service_title": "Call Consultation",
        "date": "2026-03-16",
        "time_slot": "10:00",
        "duration_minutes": 30,
        "price_inr": 1999,
        "status": "pending",
        "payment_id": None,
        "notes": "",
        "created_at": datetime.now(timezone.utc),
    }


# ── Mock database ──


def _make_mock_collection():
    """Create a mock MongoDB collection with common async methods."""
    col = MagicMock()
    col.find_one = AsyncMock(return_value=None)
    col.insert_one = AsyncMock(return_value=MagicMock(inserted_id=ObjectId()))
    col.update_one = AsyncMock(return_value=MagicMock(modified_count=1))
    col.delete_one = AsyncMock(return_value=MagicMock(deleted_count=1))
    col.replace_one = AsyncMock(return_value=MagicMock(modified_count=1))
    col.count_documents = AsyncMock(return_value=0)
    col.find = MagicMock(return_value=MockCursor([]))
    col.aggregate = MagicMock(return_value=MockAggregationCursor([]))
    return col


@pytest.fixture
def mock_db():
    """Patch the database module to return a mock DB with all collections."""
    db = MagicMock()
    db.users = _make_mock_collection()
    db.bookings = _make_mock_collection()
    db.payments = _make_mock_collection()
    db.unavailability = _make_mock_collection()
    db.availability = _make_mock_collection()
    db.settings = _make_mock_collection()

    with patch("app.database.db", db), patch("app.database.get_db", return_value=db):
        yield db


# ── Auth tokens ──


@pytest.fixture
def user_token():
    return create_access_token({"sub": str(USER_ID)})


@pytest.fixture
def admin_token():
    return create_access_token({"sub": str(ADMIN_ID)})


# ── Async HTTP client ──


@pytest.fixture
async def client(mock_db, sample_user_doc, sample_admin_doc):
    """Async HTTP client for testing FastAPI endpoints.

    Automatically patches the DB so that:
    - user_token resolves to sample_user_doc
    - admin_token resolves to sample_admin_doc
    """

    async def _find_user(query):
        if "_id" in query:
            uid = query["_id"]
            if uid == USER_ID:
                return sample_user_doc
            if uid == ADMIN_ID:
                return sample_admin_doc
        if "email" in query:
            email = query["email"]
            if email == sample_user_doc["email"]:
                return sample_user_doc
            if email == sample_admin_doc["email"]:
                return sample_admin_doc
        return None

    mock_db.users.find_one = AsyncMock(side_effect=_find_user)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
