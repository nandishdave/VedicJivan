from app.config import settings

LOGO_URL = f"{settings.FRONTEND_URL}/images/logo/logo-email.jpg"


def _email_header() -> str:
    return f"""
    <div style="text-align: center; padding: 24px 0 16px;">
        <img src="{LOGO_URL}" alt="VedicJivan" style="height: 60px; width: auto;" />
    </div>
    <hr style="border: none; border-top: 2px solid #7c3aed; margin: 0 0 24px;" />
    """


def _email_footer() -> str:
    return f"""
    <hr style="border: none; border-top: 1px solid #eee; margin: 24px 0 16px;" />
    <div style="text-align: center; padding: 0 0 16px;">
        <p style="color: #999; font-size: 12px; margin: 0;">VedicJivan &middot; Connect the Divine Within</p>
        <p style="color: #999; font-size: 12px; margin: 4px 0 0;">
            <a href="{settings.FRONTEND_URL}" style="color: #7c3aed; text-decoration: none;">vedicjivan.nandishdave.world</a>
        </p>
    </div>
    """


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
    <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto; background: #ffffff;">
        {_email_header()}
        <h2 style="color: #7c3aed; text-align: center; margin: 0 0 8px;">Booking Confirmed!</h2>
        <p style="text-align: center; color: #666; margin: 0 0 24px;">Your session is all set</p>
        <p>Dear {user_name},</p>
        <p>Your booking has been confirmed. Here are the details:</p>
        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
            <tr><td style="padding: 10px 8px; border-bottom: 1px solid #eee; font-weight: bold; color: #555;">Service</td><td style="padding: 10px 8px; border-bottom: 1px solid #eee;">{service_title}</td></tr>
            <tr><td style="padding: 10px 8px; border-bottom: 1px solid #eee; font-weight: bold; color: #555;">Date</td><td style="padding: 10px 8px; border-bottom: 1px solid #eee;">{date}</td></tr>
            <tr><td style="padding: 10px 8px; border-bottom: 1px solid #eee; font-weight: bold; color: #555;">Time</td><td style="padding: 10px 8px; border-bottom: 1px solid #eee;">{time_slot}</td></tr>
            <tr><td style="padding: 10px 8px; border-bottom: 1px solid #eee; font-weight: bold; color: #555;">Duration</td><td style="padding: 10px 8px; border-bottom: 1px solid #eee;">{duration_minutes} minutes</td></tr>
            <tr><td style="padding: 10px 8px; border-bottom: 1px solid #eee; font-weight: bold; color: #555;">Amount Paid</td><td style="padding: 10px 8px; border-bottom: 1px solid #eee; font-weight: bold; color: #16a34a;">\u20B9{price_inr}</td></tr>
            <tr><td style="padding: 10px 8px; border-bottom: 1px solid #eee; font-weight: bold; color: #555;">Booking ID</td><td style="padding: 10px 8px; border-bottom: 1px solid #eee; font-family: monospace; font-size: 12px; color: #888;">{booking_id}</td></tr>
        </table>
        <div style="background: #f3f0ff; border-left: 4px solid #7c3aed; padding: 16px; margin: 20px 0; border-radius: 4px;">
            <p style="margin: 0 0 8px; font-weight: bold; color: #7c3aed;">Meeting Details</p>
            <p style="margin: 0; font-size: 14px;">A Zoom meeting link will be shared with you before your scheduled session. Please check your email closer to the appointment date.</p>
        </div>
        <p>If you have any questions, please reach out via WhatsApp or email.</p>
        <p style="color: #666; font-size: 14px;">Thank you for choosing VedicJivan!</p>
        {_email_footer()}
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
    <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto; background: #ffffff;">
        {_email_header()}
        <h2 style="color: #7c3aed;">New Booking Received</h2>
        <p>A new booking has been confirmed and paid.</p>
        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
            <tr><td style="padding: 10px 8px; border-bottom: 1px solid #eee; font-weight: bold; color: #555;">Service</td><td style="padding: 10px 8px; border-bottom: 1px solid #eee;">{service_title}</td></tr>
            <tr><td style="padding: 10px 8px; border-bottom: 1px solid #eee; font-weight: bold; color: #555;">Date</td><td style="padding: 10px 8px; border-bottom: 1px solid #eee;"><strong>{date}</strong></td></tr>
            <tr><td style="padding: 10px 8px; border-bottom: 1px solid #eee; font-weight: bold; color: #555;">Time</td><td style="padding: 10px 8px; border-bottom: 1px solid #eee;"><strong>{time_slot}</strong></td></tr>
            <tr><td style="padding: 10px 8px; border-bottom: 1px solid #eee; font-weight: bold; color: #555;">Duration</td><td style="padding: 10px 8px; border-bottom: 1px solid #eee;">{duration_minutes} minutes</td></tr>
            <tr><td style="padding: 10px 8px; border-bottom: 1px solid #eee; font-weight: bold; color: #555;">Amount</td><td style="padding: 10px 8px; border-bottom: 1px solid #eee; font-weight: bold; color: #16a34a;">\u20B9{price_inr}</td></tr>
            <tr><td style="padding: 10px 8px; border-bottom: 1px solid #eee; font-weight: bold; color: #555;">Booking ID</td><td style="padding: 10px 8px; border-bottom: 1px solid #eee; font-family: monospace; font-size: 12px; color: #888;">{booking_id}</td></tr>
        </table>
        <h3 style="color: #333;">Customer Details</h3>
        <table style="width: 100%; border-collapse: collapse; margin: 10px 0;">
            <tr><td style="padding: 10px 8px; border-bottom: 1px solid #eee; font-weight: bold; color: #555;">Name</td><td style="padding: 10px 8px; border-bottom: 1px solid #eee;">{user_name}</td></tr>
            <tr><td style="padding: 10px 8px; border-bottom: 1px solid #eee; font-weight: bold; color: #555;">Email</td><td style="padding: 10px 8px; border-bottom: 1px solid #eee;"><a href="mailto:{user_email}">{user_email}</a></td></tr>
            <tr><td style="padding: 10px 8px; border-bottom: 1px solid #eee; font-weight: bold; color: #555;">Phone</td><td style="padding: 10px 8px; border-bottom: 1px solid #eee;"><a href="tel:{user_phone}">{user_phone}</a></td></tr>
        </table>
        <div style="background: #fef3c7; border-left: 4px solid #f59e0b; padding: 16px; margin: 20px 0; border-radius: 4px;">
            <p style="margin: 0; font-weight: bold; color: #92400e;">Action Required</p>
            <p style="margin: 8px 0 0; font-size: 14px;">Please create a Zoom meeting and share the link with the customer before the session.</p>
        </div>
        {_email_footer()}
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
    <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto; background: #ffffff;">
        {_email_header()}
        <h2 style="color: #dc2626; text-align: center;">Booking Cancelled</h2>
        <p>Dear {user_name},</p>
        <p>Your booking (ID: <code style="background: #f3f4f6; padding: 2px 6px; border-radius: 3px; font-size: 12px;">{booking_id}</code>) for <strong>{service_title}</strong> on <strong>{date}</strong> at <strong>{time_slot}</strong> has been cancelled.</p>
        <p>If this was a mistake or you'd like to rebook, please visit our website.</p>
        <div style="text-align: center; margin: 24px 0;">
            <a href="{settings.FRONTEND_URL}/services" style="background: #7c3aed; color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: bold;">Browse Services</a>
        </div>
        {_email_footer()}
    </div>
    """
    _send_email(to_email, subject, html)
