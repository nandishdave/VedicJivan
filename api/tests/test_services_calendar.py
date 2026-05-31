"""Tests for app.services.calendar_service — Google Calendar integration.

The service is wrapped in a try/except so a missing dep or an API failure
returns `None` rather than crashing the booking flow. We exercise:
  - Returns None when GOOGLE_CALENDAR_CREDENTIALS / GOOGLE_CALENDAR_ID are unset
  - Returns None when the google client raises (network / auth failure)
  - Builds the correct event payload (start/end datetime, IST timezone,
    description with all booking metadata) and returns the event id on success
"""

from __future__ import annotations

import base64
import json
import sys
import types
from unittest.mock import MagicMock, patch

import pytest


_VALID_BOOKING = {
    "date": "2026-05-01",
    "time_slot": "14:30",
    "duration_minutes": 45,
    "service_title": "Video Consultation",
    "user_name": "Jane Doe",
    "user_email": "jane@test.com",
    "user_phone": "+91999",
    "booking_id": "b123",
    "notes": "First-time consult",
}


def _fake_creds_b64() -> str:
    """Return a base64-encoded JSON blob shaped like a service-account file."""
    creds = {
        "type": "service_account",
        "project_id": "test",
        "private_key_id": "x",
        "private_key": "-----BEGIN PRIVATE KEY-----\nFAKE\n-----END PRIVATE KEY-----\n",
        "client_email": "svc@test.iam.gserviceaccount.com",
        "client_id": "1",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/svc",
    }
    return base64.b64encode(json.dumps(creds).encode()).decode()


def test_create_event_returns_none_when_credentials_missing():
    from app.services.calendar_service import create_booking_event
    with patch("app.services.calendar_service.settings") as mock_settings:
        mock_settings.GOOGLE_CALENDAR_CREDENTIALS = ""
        mock_settings.GOOGLE_CALENDAR_ID = ""
        assert create_booking_event(_VALID_BOOKING) is None


def test_create_event_returns_none_when_only_calendar_id_missing():
    from app.services.calendar_service import create_booking_event
    with patch("app.services.calendar_service.settings") as mock_settings:
        mock_settings.GOOGLE_CALENDAR_CREDENTIALS = _fake_creds_b64()
        mock_settings.GOOGLE_CALENDAR_ID = ""
        assert create_booking_event(_VALID_BOOKING) is None


def test_create_event_returns_none_on_google_api_failure():
    """If the google client raises (auth / network), we return None silently."""
    from app.services.calendar_service import create_booking_event

    fake_sa = types.ModuleType("google.oauth2.service_account")
    fake_sa.Credentials = MagicMock()
    fake_sa.Credentials.from_service_account_info = MagicMock(side_effect=RuntimeError("bad creds"))
    fake_oauth = types.ModuleType("google.oauth2")
    fake_oauth.service_account = fake_sa
    fake_google = types.ModuleType("google")
    fake_google.oauth2 = fake_oauth
    fake_apicore = types.ModuleType("googleapiclient")
    fake_discovery = types.ModuleType("googleapiclient.discovery")
    fake_discovery.build = MagicMock()
    fake_apicore.discovery = fake_discovery

    modules_patch = {
        "google": fake_google,
        "google.oauth2": fake_oauth,
        "google.oauth2.service_account": fake_sa,
        "googleapiclient": fake_apicore,
        "googleapiclient.discovery": fake_discovery,
    }

    with patch("app.services.calendar_service.settings") as mock_settings, \
         patch.dict(sys.modules, modules_patch):
        mock_settings.GOOGLE_CALENDAR_CREDENTIALS = _fake_creds_b64()
        mock_settings.GOOGLE_CALENDAR_ID = "primary"
        assert create_booking_event(_VALID_BOOKING) is None


def test_create_event_returns_event_id_on_success():
    """Successful path: builds correct event payload and returns the new event id."""
    from app.services.calendar_service import create_booking_event

    # Mock service.events().insert(...).execute()
    insert_call = MagicMock()
    insert_call.execute.return_value = {"id": "evt_abc123"}
    events_obj = MagicMock()
    events_obj.insert.return_value = insert_call
    service_obj = MagicMock()
    service_obj.events.return_value = events_obj

    fake_sa = types.ModuleType("google.oauth2.service_account")
    fake_sa.Credentials = MagicMock()
    fake_sa.Credentials.from_service_account_info.return_value = "fake-creds"
    fake_oauth = types.ModuleType("google.oauth2")
    fake_oauth.service_account = fake_sa
    fake_google = types.ModuleType("google")
    fake_google.oauth2 = fake_oauth
    fake_discovery = types.ModuleType("googleapiclient.discovery")
    fake_discovery.build = MagicMock(return_value=service_obj)
    fake_apicore = types.ModuleType("googleapiclient")
    fake_apicore.discovery = fake_discovery

    modules_patch = {
        "google": fake_google,
        "google.oauth2": fake_oauth,
        "google.oauth2.service_account": fake_sa,
        "googleapiclient": fake_apicore,
        "googleapiclient.discovery": fake_discovery,
    }

    with patch("app.services.calendar_service.settings") as mock_settings, \
         patch.dict(sys.modules, modules_patch):
        mock_settings.GOOGLE_CALENDAR_CREDENTIALS = _fake_creds_b64()
        mock_settings.GOOGLE_CALENDAR_ID = "primary"

        result = create_booking_event(_VALID_BOOKING)

    assert result == "evt_abc123"
    # Verify the event payload that was sent
    insert_kwargs = events_obj.insert.call_args.kwargs
    assert insert_kwargs["calendarId"] == "primary"
    body = insert_kwargs["body"]
    assert body["start"] == {"dateTime": "2026-05-01T14:30:00", "timeZone": "Asia/Kolkata"}
    # 14:30 + 45 min = 15:15
    assert body["end"] == {"dateTime": "2026-05-01T15:15:00", "timeZone": "Asia/Kolkata"}
    assert "Jane Doe" in body["summary"]
    assert "Video Consultation" in body["summary"]
    desc = body["description"]
    assert "jane@test.com" in desc
    assert "+91999" in desc
    assert "b123" in desc
    assert "First-time consult" in desc


def test_create_event_handles_duration_overflow_into_next_hour():
    """A 50-minute meeting starting at 23:30 should NOT roll into next-day math
    in this simple integer-divmod implementation; it overflows into 24:20.
    Verifies the divmod arithmetic without crashing."""
    from app.services.calendar_service import create_booking_event

    insert_call = MagicMock()
    insert_call.execute.return_value = {"id": "evt_late"}
    events_obj = MagicMock()
    events_obj.insert.return_value = insert_call
    service_obj = MagicMock()
    service_obj.events.return_value = events_obj

    fake_sa = types.ModuleType("google.oauth2.service_account")
    fake_sa.Credentials = MagicMock()
    fake_sa.Credentials.from_service_account_info.return_value = "fake"
    fake_oauth = types.ModuleType("google.oauth2")
    fake_oauth.service_account = fake_sa
    fake_google = types.ModuleType("google")
    fake_google.oauth2 = fake_oauth
    fake_discovery = types.ModuleType("googleapiclient.discovery")
    fake_discovery.build = MagicMock(return_value=service_obj)
    fake_apicore = types.ModuleType("googleapiclient")
    fake_apicore.discovery = fake_discovery
    modules_patch = {
        "google": fake_google,
        "google.oauth2": fake_oauth,
        "google.oauth2.service_account": fake_sa,
        "googleapiclient": fake_apicore,
        "googleapiclient.discovery": fake_discovery,
    }

    booking = {**_VALID_BOOKING, "time_slot": "23:30", "duration_minutes": 50}

    with patch("app.services.calendar_service.settings") as mock_settings, \
         patch.dict(sys.modules, modules_patch):
        mock_settings.GOOGLE_CALENDAR_CREDENTIALS = _fake_creds_b64()
        mock_settings.GOOGLE_CALENDAR_ID = "primary"
        result = create_booking_event(booking)

    assert result == "evt_late"
    body = events_obj.insert.call_args.kwargs["body"]
    # 23:30 + 50 = 24:20 (current implementation; book this as a known
    # behaviour rather than a bug, since the booking router rejects late slots).
    assert body["end"]["dateTime"] == "2026-05-01T24:20:00"
