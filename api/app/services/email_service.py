from app.config import settings


def _send_email(to: str, subject: str, html: str):
    """Send an email via Resend. Returns silently if no API key configured."""
    if not settings.RESEND_API_KEY:
        print(f"[EMAIL SKIP] No RESEND_API_KEY. Would send to {to}: {subject}")
        return

    import resend

    resend.api_key = settings.RESEND_API_KEY
    resend.Emails.send(
        {"from": settings.EMAIL_FROM, "to": to, "subject": subject, "html": html}
    )


async def send_booking_confirmation(
    to_email: str,
    user_name: str,
    service_title: str,
    date: str,
    time_slot: str,
    duration_minutes: int,
    price_inr: int,
    booking_id: str,
):
    subject = f"Booking Confirmed - {service_title} | VedicJivan"
    html = f"""
    <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto;">
        <h2 style="color: #7c3aed;">Booking Confirmed!</h2>
        <p>Dear {user_name},</p>
        <p>Your booking has been confirmed. Here are the details:</p>
        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee; font-weight: bold;">Booking ID</td><td style="padding: 8px; border-bottom: 1px solid #eee; font-family: monospace; font-size: 13px;">{booking_id}</td></tr>
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee; font-weight: bold;">Service</td><td style="padding: 8px; border-bottom: 1px solid #eee;">{service_title}</td></tr>
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee; font-weight: bold;">Date</td><td style="padding: 8px; border-bottom: 1px solid #eee;">{date}</td></tr>
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee; font-weight: bold;">Time</td><td style="padding: 8px; border-bottom: 1px solid #eee;">{time_slot}</td></tr>
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee; font-weight: bold;">Duration</td><td style="padding: 8px; border-bottom: 1px solid #eee;">{duration_minutes} minutes</td></tr>
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee; font-weight: bold;">Amount Paid</td><td style="padding: 8px; border-bottom: 1px solid #eee;">\u20B9{price_inr}</td></tr>
        </table>
        <div style="background: #f3f0ff; border-left: 4px solid #7c3aed; padding: 16px; margin: 20px 0; border-radius: 4px;">
            <p style="margin: 0 0 8px; font-weight: bold; color: #7c3aed;">Meeting Details</p>
            <p style="margin: 0; font-size: 14px;">A Zoom meeting link will be shared with you before your scheduled session. Please check your email closer to the appointment date.</p>
        </div>
        <p>If you have any questions, please reach out via WhatsApp or email.</p>
        <p style="color: #666; font-size: 14px;">Thank you for choosing VedicJivan!</p>
    </div>
    """
    _send_email(to_email, subject, html)


async def send_admin_booking_notification(
    user_name: str,
    user_email: str,
    user_phone: str,
    service_title: str,
    date: str,
    time_slot: str,
    duration_minutes: int,
    price_inr: int,
    booking_id: str,
):
    """Notify admin about a new confirmed booking."""
    admin_email = settings.ADMIN_EMAIL
    if not admin_email:
        print("[EMAIL SKIP] No ADMIN_EMAIL configured.")
        return

    subject = f"New Booking: {service_title} on {date} at {time_slot}"
    html = f"""
    <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto;">
        <h2 style="color: #7c3aed;">New Booking Received</h2>
        <p>A new booking has been confirmed and paid.</p>
        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee; font-weight: bold;">Booking ID</td><td style="padding: 8px; border-bottom: 1px solid #eee; font-family: monospace; font-size: 13px;">{booking_id}</td></tr>
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee; font-weight: bold;">Service</td><td style="padding: 8px; border-bottom: 1px solid #eee;">{service_title}</td></tr>
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee; font-weight: bold;">Date</td><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>{date}</strong></td></tr>
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee; font-weight: bold;">Time</td><td style="padding: 8px; border-bottom: 1px solid #eee;"><strong>{time_slot}</strong></td></tr>
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee; font-weight: bold;">Duration</td><td style="padding: 8px; border-bottom: 1px solid #eee;">{duration_minutes} minutes</td></tr>
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee; font-weight: bold;">Amount</td><td style="padding: 8px; border-bottom: 1px solid #eee;">\u20B9{price_inr}</td></tr>
        </table>
        <h3 style="color: #333;">Customer Details</h3>
        <table style="width: 100%; border-collapse: collapse; margin: 10px 0;">
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee; font-weight: bold;">Name</td><td style="padding: 8px; border-bottom: 1px solid #eee;">{user_name}</td></tr>
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee; font-weight: bold;">Email</td><td style="padding: 8px; border-bottom: 1px solid #eee;"><a href="mailto:{user_email}">{user_email}</a></td></tr>
            <tr><td style="padding: 8px; border-bottom: 1px solid #eee; font-weight: bold;">Phone</td><td style="padding: 8px; border-bottom: 1px solid #eee;"><a href="tel:{user_phone}">{user_phone}</a></td></tr>
        </table>
        <div style="background: #fef3c7; border-left: 4px solid #f59e0b; padding: 16px; margin: 20px 0; border-radius: 4px;">
            <p style="margin: 0; font-weight: bold; color: #92400e;">Action Required</p>
            <p style="margin: 8px 0 0; font-size: 14px;">Please create a Zoom meeting and share the link with the customer before the session.</p>
        </div>
    </div>
    """
    _send_email(admin_email, subject, html)


async def send_booking_cancellation(
    to_email: str,
    user_name: str,
    service_title: str,
    date: str,
    time_slot: str,
    booking_id: str,
):
    subject = f"Booking Cancelled - {service_title} | VedicJivan"
    html = f"""
    <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto;">
        <h2 style="color: #7c3aed;">Booking Cancelled</h2>
        <p>Dear {user_name},</p>
        <p>Your booking (ID: <code>{booking_id}</code>) for <strong>{service_title}</strong> on <strong>{date}</strong> at <strong>{time_slot}</strong> has been cancelled.</p>
        <p>If this was a mistake or you'd like to rebook, please visit our website.</p>
        <p style="color: #666; font-size: 14px;">VedicJivan Team</p>
    </div>
    """
    _send_email(to_email, subject, html)
