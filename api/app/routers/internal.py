from datetime import date, timedelta

from fastapi import APIRouter, Header, HTTPException
from app.config import settings
from app.database import get_db
from app.services.email_service import send_booking_reminder

router = APIRouter(prefix="/api/internal", tags=["internal"])


@router.post("/send-reminders")
async def send_reminders(x_internal_secret: str = Header(default="")):
    """Send 24h reminder emails for tomorrow's confirmed bookings."""
    if not settings.INTERNAL_SECRET or x_internal_secret != settings.INTERNAL_SECRET:
        raise HTTPException(status_code=403, detail="Forbidden")

    db = get_db()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    cursor = db.bookings.find(
        {"status": "confirmed", "date": tomorrow, "reminder_sent": {"$ne": True}}
    )
    bookings = await cursor.to_list(length=None)

    sent = 0
    for booking in bookings:
        try:
            await send_booking_reminder(
                to_email=booking["user_email"],
                user_name=booking["user_name"],
                service_title=booking["service_title"],
                date=booking["date"],
                time_slot=booking["time_slot"],
                duration_minutes=booking["duration_minutes"],
                booking_id=str(booking["_id"]),
            )
            await db.bookings.update_one(
                {"_id": booking["_id"]}, {"$set": {"reminder_sent": True}}
            )
            sent += 1
        except Exception as e:
            print(f"[REMINDER] Failed for booking {booking['_id']}: {e}")

    return {"sent": sent, "date": tomorrow}
