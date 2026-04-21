"""Unit tests for each repository's `ensure_indexes()`.

These assert the *spec* we pass to Mongo — not the Mongo behaviour itself.
Mongo handles the actual index build; our job is to make sure the right
spec leaves the application.

Adding a new index should land with a new assertion in here. If CI fails
because a test is missing, your migration script ran something the repo
tests don't know about.
"""

from __future__ import annotations

from app.repositories.booking_repository import MongoBookingRepository
from app.repositories.kundli_repository import MongoKundliRepository
from app.repositories.payment_repository import MongoPaymentRepository
from app.repositories.processed_event_repository import (
    MongoProcessedEventRepository,
)
from app.repositories.service_repository import MongoServiceRepository
from app.repositories.unavailability_repository import (
    MongoUnavailabilityRepository,
)
from app.repositories.user_repository import MongoUserRepository


def _index_specs(create_index_mock) -> list[tuple[list, dict]]:
    """Reduce call_args_list to (keys, kwargs) pairs so assertions read cleanly."""
    return [
        (list(call.args[0]), dict(call.kwargs))
        for call in create_index_mock.call_args_list
    ]


async def test_bookings_ensure_indexes(mock_db):
    await MongoBookingRepository(mock_db).ensure_indexes()
    specs = _index_specs(mock_db.bookings.create_index)
    assert ([("date", 1), ("status", 1)], {}) in specs
    assert ([("user_email", 1), ("created_at", -1)], {}) in specs
    assert ([("status", 1), ("created_at", 1)], {}) in specs


async def test_payments_ensure_indexes(mock_db):
    await MongoPaymentRepository(mock_db).ensure_indexes()
    specs = _index_specs(mock_db.payments.create_index)
    assert ([("stripe_session_id", 1)], {"unique": True}) in specs
    assert ([("stripe_payment_intent_id", 1)], {}) in specs
    assert ([("status", 1), ("created_at", -1)], {}) in specs


async def test_kundlis_ensure_indexes(mock_db):
    await MongoKundliRepository(mock_db).ensure_indexes()
    specs = _index_specs(mock_db.kundlis.create_index)
    assert ([("email", 1), ("created_at", -1)], {}) in specs


async def test_unavailability_ensure_indexes(mock_db):
    await MongoUnavailabilityRepository(mock_db).ensure_indexes()
    specs = _index_specs(mock_db.unavailability.create_index)
    assert ([("date", 1), ("is_holiday", 1)], {}) in specs


async def test_services_ensure_indexes(mock_db):
    await MongoServiceRepository(mock_db).ensure_indexes()
    specs = _index_specs(mock_db.services.create_index)
    assert ([("slug", 1)], {"unique": True}) in specs


async def test_users_ensure_indexes(mock_db):
    await MongoUserRepository(mock_db).ensure_indexes()
    specs = _index_specs(mock_db.users.create_index)
    assert ([("email", 1)], {"unique": True}) in specs


async def test_processed_events_ensure_indexes_has_90d_ttl(mock_db):
    await MongoProcessedEventRepository(mock_db).ensure_indexes()
    specs = _index_specs(mock_db.stripe_events.create_index)
    # 90 days in seconds.
    assert ([("received_at", 1)], {"expireAfterSeconds": 60 * 60 * 24 * 90}) in specs
