"""Tests for app.database — connection lifecycle and get_db."""

from unittest.mock import patch, MagicMock, AsyncMock

import pytest

from app import database


@pytest.fixture(autouse=True)
def reset_globals():
    """Reset module-level globals before each test."""
    original_client = database.client
    original_db = database.db
    database.client = None
    database.db = None
    yield
    database.client = original_client
    database.db = original_db


@pytest.mark.asyncio
async def test_connect_db_creates_client_and_db():
    mock_client_instance = MagicMock()
    mock_client_instance.get_default_database.return_value = MagicMock(name="test-db")

    with patch("app.database.AsyncIOMotorClient", return_value=mock_client_instance):
        await database.connect_db()

    assert database.client is mock_client_instance
    assert database.db is not None
    mock_client_instance.get_default_database.assert_called_once()


@pytest.mark.asyncio
async def test_close_db_closes_client():
    mock_client = MagicMock()
    database.client = mock_client

    await database.close_db()

    mock_client.close.assert_called_once()


@pytest.mark.asyncio
async def test_close_db_noop_when_no_client():
    database.client = None
    # Should not raise
    await database.close_db()


def test_get_db_returns_current_db():
    mock_db = MagicMock()
    database.db = mock_db

    result = database.get_db()

    assert result is mock_db


def test_get_db_returns_none_before_connect():
    database.db = None
    result = database.get_db()
    assert result is None
