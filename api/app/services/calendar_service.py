"""Google Calendar integration — creates events for confirmed bookings."""

import base64
import json

from app.config import settings


def create_booking_event(booking: dict) -> str | None:
    """
    Create a Google Calendar event for a confirmed booking.
    Returns the event ID on success, or None if calendar is not configured / on error.
    """
    if not settings.GOOGLE_CALENDAR_CREDENTIALS or not settings.GOOGLE_CALENDAR_ID:
        return None

    try:
        # Lazy imports — google packages may not be installed in dev env
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

        # Decode base64 service account JSON
        creds_json = base64.b64decode(settings.GOOGLE_CALENDAR_CREDENTIALS).decode()
        creds_info = json.loads(creds_json)

        credentials = service_account.Credentials.from_service_account_info(
            creds_info,
            scopes=["https://www.googleapis.com/auth/calendar"],
        )

        service = build("calendar", "v3", credentials=credentials)

        # Build event datetime strings (assume IST / local date + time_slot)
        date = booking["date"]          # "YYYY-MM-DD"
        time_slot = booking["time_slot"]  # "HH:MM"
        duration = booking.get("duration_minutes", 30)

        start_dt = f"{date}T{time_slot}:00"
        h, m = map(int, time_slot.split(":"))
        end_total_minutes = h * 60 + m + duration
        end_h, end_m = divmod(end_total_minutes, 60)
        end_dt = f"{date}T{end_h:02d}:{end_m:02d}:00"

        description = (
            f"Service: {booking.get('service_title', '')}\n"
            f"Customer: {booking.get('user_name', '')} <{booking.get('user_email', '')}>\n"
            f"Phone: {booking.get('user_phone', '')}\n"
            f"Duration: {duration} minutes\n"
            f"Booking ID: {booking.get('booking_id', '')}\n"
            f"Notes: {booking.get('notes', '')}"
        )

        event = {
            "summary": f"{booking.get('service_title', 'Session')} — {booking.get('user_name', '')}",
            "description": description,
            "start": {"dateTime": start_dt, "timeZone": "Asia/Kolkata"},
            "end": {"dateTime": end_dt, "timeZone": "Asia/Kolkata"},
        }

        created = (
            service.events()
            .insert(calendarId=settings.GOOGLE_CALENDAR_ID, body=event)
            .execute()
        )
        return created.get("id")

    except Exception as e:
        print(f"[CALENDAR] Failed to create event: {e}")
        return None
