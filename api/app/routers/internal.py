import hmac
from datetime import date, timedelta

from fastapi import APIRouter, Depends, Header, HTTPException

from app.config import settings
from app.dependencies import block_during_maintenance, get_booking_repository
from app.repositories.booking_repository import BookingRepository
from app.services.email_service import send_booking_reminder
from app.use_cases.bookings import SendBookingReminders

router = APIRouter(prefix="/api/internal", tags=["internal"])


def _send_reminders_use_case(
    repo: BookingRepository = Depends(get_booking_repository),
) -> SendBookingReminders:
    # Email sender wired at the boundary, mirroring routers/payments.py — the
    # use case stays free of the email import and is fully unit-testable.
    return SendBookingReminders(repo, send_booking_reminder)


@router.post("/send-reminders", dependencies=[Depends(block_during_maintenance)])
async def send_reminders(
    x_internal_secret: str = Header(default=""),
    use_case: SendBookingReminders = Depends(_send_reminders_use_case),
):
    """Send 24h reminder emails for tomorrow's confirmed bookings."""
    # Constant-time compare so a timing side-channel can't be used to recover
    # the secret byte-by-byte. Short-circuit if the server has no secret set.
    if not settings.INTERNAL_SECRET or not hmac.compare_digest(
        x_internal_secret, settings.INTERNAL_SECRET
    ):
        raise HTTPException(status_code=403, detail="Forbidden")

    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    sent = await use_case.execute(tomorrow)
    return {"sent": sent, "date": tomorrow}
