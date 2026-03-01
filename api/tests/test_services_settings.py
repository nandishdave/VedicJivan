"""Tests for app.services.settings — business hours loading."""

from unittest.mock import AsyncMock, patch, MagicMock

import pytest

from app.models.availability import BusinessHoursSettings
from app.services.settings import get_business_hours, DEFAULT_SETTINGS


def _full_week_hours(overrides=None):
    """Build a valid 7-day weekly_hours list (days 0-6).

    Override specific days via dict keyed by day number.
    """
    overrides = overrides or {}
    result = []
    for day in range(7):
        if day in overrides:
            result.append({"day": day, **overrides[day]})
        else:
            result.append({"day": day, "is_open": True, "open_time": "10:00", "close_time": "18:00"})
    return result


@pytest.fixture
def mock_db():
    db = MagicMock()
    db.settings = MagicMock()
    db.settings.find_one = AsyncMock()
    return db


@pytest.mark.asyncio
async def test_returns_defaults_when_no_db_document(mock_db):
    mock_db.settings.find_one.return_value = None

    with patch("app.services.settings.get_db", return_value=mock_db):
        result = await get_business_hours()

    assert result == DEFAULT_SETTINGS
    assert result.timezone == "Asia/Kolkata"
    mock_db.settings.find_one.assert_awaited_once_with({"_id": "business_hours"})


@pytest.mark.asyncio
async def test_returns_settings_from_db(mock_db):
    hours = _full_week_hours({
        0: {"is_open": True, "open_time": "09:00", "close_time": "17:00"},
        1: {"is_open": True, "open_time": "10:00", "close_time": "19:00"},
    })
    mock_db.settings.find_one.return_value = {
        "_id": "business_hours",
        "timezone": "America/New_York",
        "weekly_hours": hours,
    }

    with patch("app.services.settings.get_db", return_value=mock_db):
        result = await get_business_hours()

    assert isinstance(result, BusinessHoursSettings)
    assert result.timezone == "America/New_York"
    assert len(result.weekly_hours) == 7
    # Days are sorted by day number
    assert result.weekly_hours[0].day == 0
    assert result.weekly_hours[0].open_time == "09:00"
    assert result.weekly_hours[0].close_time == "17:00"
    assert result.weekly_hours[1].open_time == "10:00"
    assert result.weekly_hours[1].close_time == "19:00"


@pytest.mark.asyncio
async def test_uses_default_timezone_when_missing_in_doc(mock_db):
    mock_db.settings.find_one.return_value = {
        "_id": "business_hours",
        "weekly_hours": _full_week_hours(),
    }

    with patch("app.services.settings.get_db", return_value=mock_db):
        result = await get_business_hours()

    assert result.timezone == "Asia/Kolkata"
    assert len(result.weekly_hours) == 7


@pytest.mark.asyncio
async def test_weekend_closed(mock_db):
    hours = _full_week_hours({
        5: {"is_open": False, "open_time": "00:00", "close_time": "00:00"},
        6: {"is_open": False, "open_time": "00:00", "close_time": "00:00"},
    })
    mock_db.settings.find_one.return_value = {
        "_id": "business_hours",
        "timezone": "Europe/London",
        "weekly_hours": hours,
    }

    with patch("app.services.settings.get_db", return_value=mock_db):
        result = await get_business_hours()

    assert result.timezone == "Europe/London"
    assert result.weekly_hours[5].is_open is False
    assert result.weekly_hours[6].is_open is False
    assert result.weekly_hours[0].is_open is True


def test_default_settings_is_valid_model():
    assert isinstance(DEFAULT_SETTINGS, BusinessHoursSettings)
    assert DEFAULT_SETTINGS.timezone == "Asia/Kolkata"
    assert len(DEFAULT_SETTINGS.weekly_hours) == 7
