"""Tests for app.services.email_service — email sending."""

from unittest.mock import MagicMock, patch

import pytest

from app.services.email_service import (
    _send_email,
    send_booking_cancellation,
    send_booking_confirmation,
    send_admin_booking_notification,
)


def test_send_email_no_api_key():
    """When RESEND_API_KEY is empty, no email is sent and no error raised."""
    with patch("app.services.email_service.settings") as mock_settings:
        mock_settings.RESEND_API_KEY = ""
        _send_email("to@test.com", "Subject", "<p>Body</p>")
        # Should not raise


def test_send_email_with_api_key():
    """When RESEND_API_KEY is set, resend.Emails.send is called."""
    import resend

    mock_send = MagicMock()
    with patch("app.services.email_service.settings") as mock_settings, \
         patch.object(resend.Emails, "send", mock_send):
        mock_settings.RESEND_API_KEY = "re_test_key"
        mock_settings.EMAIL_FROM = "from@test.com"

        _send_email("to@test.com", "Subject", "<p>Body</p>")

        mock_send.assert_called_once()
        call_args = mock_send.call_args[0][0]
        assert call_args["to"] == "to@test.com"
        assert call_args["subject"] == "Subject"


async def test_send_booking_confirmation():
    with patch("app.services.email_service._send_email") as mock_send:
        await send_booking_confirmation(
            to_email="user@test.com",
            user_name="John",
            service_title="Call Consultation",
            date="2026-03-15",
            time_slot="10:00",
            duration_minutes=30,
            price_inr=1999,
            booking_id="booking123",
        )

        mock_send.assert_called_once()
        call_args = mock_send.call_args
        assert call_args[0][0] == "user@test.com"
        assert "Booking Confirmed" in call_args[0][1]
        assert "Call Consultation" in call_args[0][1]
        # Check HTML contains details
        html = call_args[0][2]
        assert "John" in html
        assert "booking123" in html
        assert "2026-03-15" in html


async def test_send_booking_confirmation_html_contains_price():
    with patch("app.services.email_service._send_email") as mock_send:
        await send_booking_confirmation(
            to_email="user@test.com",
            user_name="John",
            service_title="Call",
            date="2026-03-15",
            time_slot="10:00",
            duration_minutes=30,
            price_inr=1999,
            booking_id="b1",
        )
        html = mock_send.call_args[0][2]
        assert "1999" in html


async def test_send_admin_notification():
    with patch("app.services.email_service._send_email") as mock_send, \
         patch("app.services.email_service.settings") as mock_settings:
        mock_settings.ADMIN_EMAIL = "admin@test.com"

        await send_admin_booking_notification(
            user_name="John",
            user_email="john@test.com",
            user_phone="1234567890",
            service_title="Call Consultation",
            date="2026-03-15",
            time_slot="10:00",
            duration_minutes=30,
            price_inr=1999,
            booking_id="b123",
        )

        mock_send.assert_called_once()
        assert mock_send.call_args[0][0] == "admin@test.com"
        assert "New Booking" in mock_send.call_args[0][1]


async def test_send_admin_notification_no_admin_email():
    with patch("app.services.email_service._send_email") as mock_send, \
         patch("app.services.email_service.settings") as mock_settings:
        mock_settings.ADMIN_EMAIL = ""

        await send_admin_booking_notification(
            user_name="John",
            user_email="john@test.com",
            user_phone="1234567890",
            service_title="Call",
            date="2026-03-15",
            time_slot="10:00",
            duration_minutes=30,
            price_inr=1999,
            booking_id="b1",
        )

        mock_send.assert_not_called()


async def test_send_admin_notification_subject_contains_service():
    with patch("app.services.email_service._send_email") as mock_send, \
         patch("app.services.email_service.settings") as mock_settings:
        mock_settings.ADMIN_EMAIL = "admin@test.com"

        await send_admin_booking_notification(
            user_name="John",
            user_email="john@test.com",
            user_phone="1234567890",
            service_title="Video Consultation",
            date="2026-04-01",
            time_slot="14:00",
            duration_minutes=45,
            price_inr=2999,
            booking_id="b456",
        )

        subject = mock_send.call_args[0][1]
        assert "Video Consultation" in subject
        assert "2026-04-01" in subject


async def test_send_booking_cancellation():
    with patch("app.services.email_service._send_email") as mock_send:
        await send_booking_cancellation(
            to_email="user@test.com",
            user_name="John",
            service_title="Call Consultation",
            date="2026-03-15",
            time_slot="10:00",
            booking_id="b789",
        )

        mock_send.assert_called_once()
        subject = mock_send.call_args[0][1]
        assert "Cancelled" in subject
        html = mock_send.call_args[0][2]
        assert "b789" in html
        assert "John" in html


# ── Reschedule / reminder / Kundli-report email coverage ──


async def test_send_booking_rescheduled_includes_old_and_new_slots():
    from app.services.email_service import send_booking_rescheduled
    with patch("app.services.email_service._send_email") as mock_send:
        await send_booking_rescheduled(
            to_email="user@test.com",
            user_name="John",
            service_title="Call Consultation",
            old_date="2026-04-01",
            old_time="10:00",
            new_date="2026-04-08",
            new_time="14:30",
            booking_id="b900",
        )
        mock_send.assert_called_once()
        subject = mock_send.call_args[0][1]
        assert "Rescheduled" in subject
        html = mock_send.call_args[0][2]
        assert "2026-04-01" in html and "10:00" in html
        assert "2026-04-08" in html and "14:30" in html
        assert "b900" in html


async def test_send_booking_reminder_marks_session_as_tomorrow():
    from app.services.email_service import send_booking_reminder
    with patch("app.services.email_service._send_email") as mock_send:
        await send_booking_reminder(
            to_email="user@test.com",
            user_name="John",
            service_title="Video Consultation",
            date="2026-04-22",
            time_slot="11:00",
            duration_minutes=45,
            booking_id="b777",
        )
        mock_send.assert_called_once()
        subject = mock_send.call_args[0][1]
        assert "Reminder" in subject
        assert "Video Consultation" in subject
        html = mock_send.call_args[0][2]
        assert "Tomorrow" in html
        assert "45 minutes" in html
        assert "b777" in html


async def test_send_kundli_report_skips_when_no_resend_key():
    """Without RESEND_API_KEY, no resend.Emails.send call is made."""
    from app.services.email_service import send_kundli_report
    with patch("app.services.email_service.settings") as mock_settings:
        mock_settings.RESEND_API_KEY = ""
        await send_kundli_report("u@test.com", "User", b"%PDF-fake")
        # No exception, no resend call needed (returns silently)


async def test_send_kundli_report_attaches_pdf_when_key_set():
    """With RESEND_API_KEY set, resend.Emails.send is invoked with a base64 PDF
    attachment named after the user."""
    import resend
    import base64
    mock_send = MagicMock()
    with patch("app.services.email_service.settings") as mock_settings, \
         patch.object(resend.Emails, "send", mock_send):
        mock_settings.RESEND_API_KEY = "re_test"
        mock_settings.EMAIL_FROM = "from@test.com"
        mock_settings.FRONTEND_URL = "https://example.test"

        from app.services.email_service import send_kundli_report
        await send_kundli_report("u@test.com", "Jane Doe", b"%PDF-content")

        mock_send.assert_called_once()
        payload = mock_send.call_args[0][0]
        assert payload["to"] == "u@test.com"
        assert "Kundli Report" in payload["subject"]
        attachments = payload["attachments"]
        assert len(attachments) == 1
        # Filename uses underscores, not spaces
        assert attachments[0]["filename"] == "Kundli_Report_Jane_Doe.pdf"
        # Attachment content is base64-encoded PDF bytes
        assert base64.b64decode(attachments[0]["content"]) == b"%PDF-content"
