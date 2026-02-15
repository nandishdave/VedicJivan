from app.config import settings


async def send_booking_confirmation(
    to_email: str,
    user_name: str,
    service_title: str,
    date: str,
    time_slot: str,
    duration_minutes: int,
    price_inr: int,
):
    if not settings.RESEND_API_KEY:
        print(f"[EMAIL SKIP] No RESEND_API_KEY. Would send confirmation to {to_email}")
        return

    import resend

    resend.api_key = settings.RESEND_API_KEY

    resend.Emails.send(
        {
            "from": settings.EMAIL_FROM,
            "to": to_email,
            "subject": f"Booking Confirmed - {service_title} | VedicJivan",
            "html": f"""
            <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #7c3aed;">Booking Confirmed!</h2>
                <p>Dear {user_name},</p>
                <p>Your booking has been confirmed. Here are the details:</p>
                <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                    <tr><td style="padding: 8px; border-bottom: 1px solid #eee; font-weight: bold;">Service</td><td style="padding: 8px; border-bottom: 1px solid #eee;">{service_title}</td></tr>
                    <tr><td style="padding: 8px; border-bottom: 1px solid #eee; font-weight: bold;">Date</td><td style="padding: 8px; border-bottom: 1px solid #eee;">{date}</td></tr>
                    <tr><td style="padding: 8px; border-bottom: 1px solid #eee; font-weight: bold;">Time</td><td style="padding: 8px; border-bottom: 1px solid #eee;">{time_slot}</td></tr>
                    <tr><td style="padding: 8px; border-bottom: 1px solid #eee; font-weight: bold;">Duration</td><td style="padding: 8px; border-bottom: 1px solid #eee;">{duration_minutes} minutes</td></tr>
                    <tr><td style="padding: 8px; border-bottom: 1px solid #eee; font-weight: bold;">Amount Paid</td><td style="padding: 8px; border-bottom: 1px solid #eee;">\u20B9{price_inr}</td></tr>
                </table>
                <p>We will contact you at the scheduled time. If you have any questions, please reach out via WhatsApp.</p>
                <p style="color: #666; font-size: 14px;">Thank you for choosing VedicJivan!</p>
            </div>
            """,
        }
    )


async def send_booking_cancellation(
    to_email: str,
    user_name: str,
    service_title: str,
    date: str,
    time_slot: str,
):
    if not settings.RESEND_API_KEY:
        print(f"[EMAIL SKIP] No RESEND_API_KEY. Would send cancellation to {to_email}")
        return

    import resend

    resend.api_key = settings.RESEND_API_KEY

    resend.Emails.send(
        {
            "from": settings.EMAIL_FROM,
            "to": to_email,
            "subject": f"Booking Cancelled - {service_title} | VedicJivan",
            "html": f"""
            <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto;">
                <h2 style="color: #7c3aed;">Booking Cancelled</h2>
                <p>Dear {user_name},</p>
                <p>Your booking for <strong>{service_title}</strong> on <strong>{date}</strong> at <strong>{time_slot}</strong> has been cancelled.</p>
                <p>If this was a mistake or you'd like to rebook, please visit our website.</p>
                <p style="color: #666; font-size: 14px;">VedicJivan Team</p>
            </div>
            """,
        }
    )
