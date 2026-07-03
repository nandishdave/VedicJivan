from app.config import settings
from app.infrastructure.logging import get_logger

logger = get_logger(__name__)

# Direct S3 URL — no CloudFront/GitHub restrictive headers, works in all email clients
LOGO_URL = "https://vedicjivan-website.s3.ap-south-1.amazonaws.com/images/logo/logo-email.jpg"


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
        logger.info("Email skip — no RESEND_API_KEY. Would send to=%s subject=%s", to, subject)
        return

    import resend

    resend.api_key = settings.RESEND_API_KEY
    resend.Emails.send(
        {
            "from": settings.EMAIL_FROM,
            "to": to,
            "subject": subject,
            "html": html,
            # Deliverability signal (Gmail bulk-sender guidance) — a valid
            # List-Unsubscribe pointing at a real, monitored inbox. We use a
            # mailto: (not One-Click, which would need an HTTPS POST endpoint).
            "headers": {
                "List-Unsubscribe": f"<mailto:{settings.ADMIN_EMAIL}?subject=unsubscribe>",
            },
        }
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
        <div style="text-align: center; margin: 24px 0;">
            <a href="{settings.FRONTEND_URL}/reschedule/?id={booking_id}" style="color: #7c3aed; font-size: 13px; text-decoration: underline;">Need to reschedule?</a>
        </div>
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
        logger.info("Email skip — no ADMIN_EMAIL configured")
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


async def send_booking_rescheduled(
    to_email: str,
    user_name: str,
    service_title: str,
    old_date: str,
    old_time: str,
    new_date: str,
    new_time: str,
    booking_id: str,
):
    subject = f"Booking Rescheduled - {service_title} | VedicJivan"
    html = f"""
    <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto; background: #ffffff;">
        {_email_header()}
        <h2 style="color: #7c3aed; text-align: center; margin: 0 0 8px;">Booking Rescheduled</h2>
        <p style="text-align: center; color: #666; margin: 0 0 24px;">Your session has been moved to a new time</p>
        <p>Dear {user_name},</p>
        <p>Your <strong>{service_title}</strong> session has been successfully rescheduled.</p>
        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
            <tr><td colspan="2" style="padding: 8px; background: #f9fafb; font-weight: bold; color: #555; font-size: 13px; text-transform: uppercase; letter-spacing: 0.05em;">Previous</td></tr>
            <tr><td style="padding: 10px 8px; border-bottom: 1px solid #eee; font-weight: bold; color: #999; width: 40%;">Date</td><td style="padding: 10px 8px; border-bottom: 1px solid #eee; color: #999; text-decoration: line-through;">{old_date}</td></tr>
            <tr><td style="padding: 10px 8px; border-bottom: 1px solid #eee; font-weight: bold; color: #999;">Time</td><td style="padding: 10px 8px; border-bottom: 1px solid #eee; color: #999; text-decoration: line-through;">{old_time}</td></tr>
            <tr><td colspan="2" style="padding: 8px; background: #f3f0ff; font-weight: bold; color: #7c3aed; font-size: 13px; text-transform: uppercase; letter-spacing: 0.05em;">New</td></tr>
            <tr><td style="padding: 10px 8px; border-bottom: 1px solid #eee; font-weight: bold; color: #555;">Date</td><td style="padding: 10px 8px; border-bottom: 1px solid #eee; font-weight: bold;">{new_date}</td></tr>
            <tr><td style="padding: 10px 8px; border-bottom: 1px solid #eee; font-weight: bold; color: #555;">Time</td><td style="padding: 10px 8px; border-bottom: 1px solid #eee; font-weight: bold;">{new_time}</td></tr>
            <tr><td style="padding: 10px 8px; border-bottom: 1px solid #eee; font-weight: bold; color: #555;">Booking ID</td><td style="padding: 10px 8px; border-bottom: 1px solid #eee; font-family: monospace; font-size: 12px; color: #888;">{booking_id}</td></tr>
        </table>
        <p style="color: #666; font-size: 14px;">A Zoom meeting link will be shared with you before your new session time.</p>
        <p style="text-align: center; margin: 16px 0; font-size: 13px; color: #888;">
            <a href="{settings.FRONTEND_URL}/reschedule/?id={booking_id}" style="color: #7c3aed; font-size: 13px; text-decoration: underline;">Need to reschedule again?</a>
        </p>
        {_email_footer()}
    </div>
    """
    _send_email(to_email, subject, html)


async def send_booking_reminder(
    to_email: str,
    user_name: str,
    service_title: str,
    date: str,
    time_slot: str,
    duration_minutes: int,
    booking_id: str,
):
    subject = f"Reminder: Your {service_title} session is tomorrow | VedicJivan"
    html = f"""
    <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto; background: #ffffff;">
        {_email_header()}
        <h2 style="color: #7c3aed; text-align: center; margin: 0 0 8px;">Your Session is Tomorrow!</h2>
        <p style="text-align: center; color: #666; margin: 0 0 24px;">Just a friendly reminder about your upcoming session</p>
        <p>Dear {user_name},</p>
        <p>This is a reminder that your session is scheduled for <strong>tomorrow</strong>. Here are the details:</p>
        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
            <tr><td style="padding: 10px 8px; border-bottom: 1px solid #eee; font-weight: bold; color: #555;">Service</td><td style="padding: 10px 8px; border-bottom: 1px solid #eee;">{service_title}</td></tr>
            <tr><td style="padding: 10px 8px; border-bottom: 1px solid #eee; font-weight: bold; color: #555;">Date</td><td style="padding: 10px 8px; border-bottom: 1px solid #eee;"><strong>{date}</strong></td></tr>
            <tr><td style="padding: 10px 8px; border-bottom: 1px solid #eee; font-weight: bold; color: #555;">Time</td><td style="padding: 10px 8px; border-bottom: 1px solid #eee;"><strong>{time_slot}</strong></td></tr>
            <tr><td style="padding: 10px 8px; border-bottom: 1px solid #eee; font-weight: bold; color: #555;">Duration</td><td style="padding: 10px 8px; border-bottom: 1px solid #eee;">{duration_minutes} minutes</td></tr>
            <tr><td style="padding: 10px 8px; border-bottom: 1px solid #eee; font-weight: bold; color: #555;">Booking ID</td><td style="padding: 10px 8px; border-bottom: 1px solid #eee; font-family: monospace; font-size: 12px; color: #888;">{booking_id}</td></tr>
        </table>
        <div style="background: #f3f0ff; border-left: 4px solid #7c3aed; padding: 16px; margin: 20px 0; border-radius: 4px;">
            <p style="margin: 0 0 8px; font-weight: bold; color: #7c3aed;">Prepare for Your Session</p>
            <p style="margin: 0; font-size: 14px;">A Zoom meeting link will be shared with you shortly. Please ensure you are in a quiet space and have a stable internet connection.</p>
        </div>
        <p style="color: #666; font-size: 14px;">If you need to cancel or have questions, please contact us as soon as possible.</p>
        {_email_footer()}
    </div>
    """
    _send_email(to_email, subject, html)


async def send_kundli_report(to_email: str, user_name: str, pdf_bytes: bytes):
    """Send Kundli PDF report as email attachment via Resend."""
    if not settings.RESEND_API_KEY:
        logger.info("Kundli email skip — no RESEND_API_KEY. Would send to=%s", to_email)
        return

    import base64

    import resend

    resend.api_key = settings.RESEND_API_KEY

    subject = "Your Free Kundli Report | VedicJivan"
    html = f"""
    <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto; background: #ffffff;">
        {_email_header()}
        <h2 style="color: #7c3aed; text-align: center; margin: 0 0 8px;">Your Kundli Report is Ready!</h2>
        <p style="text-align: center; color: #666; margin: 0 0 24px;">Your personalised Vedic birth chart</p>
        <p>Dear {user_name},</p>
        <p>Thank you for using VedicJivan's free Kundli generator. Your personalised Vedic birth chart report is attached to this email as a PDF.</p>
        <p>Your report includes:</p>
        <ul style="color: #555; line-height: 1.8;">
            <li>Birth chart details &amp; planetary positions</li>
            <li>Ascendant &amp; Nakshatra analysis</li>
            <li>Character, career &amp; life predictions</li>
            <li>Manglik Dosha analysis</li>
            <li>Sade Sati report</li>
            <li>Vimshottari Dasha periods</li>
            <li>Planetary effects &amp; remedies</li>
        </ul>
        <div style="background: #f3f0ff; border-left: 4px solid #7c3aed; padding: 16px; margin: 20px 0; border-radius: 4px;">
            <p style="margin: 0 0 8px; font-weight: bold; color: #7c3aed;">Want deeper insights?</p>
            <p style="margin: 0; font-size: 14px;">Book a personalised consultation with our Vedic astrology expert for detailed guidance tailored to your life questions.</p>
        </div>
        <div style="text-align: center; margin: 24px 0;">
            <a href="{settings.FRONTEND_URL}/services/" style="background: #7c3aed; color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: bold;">Book a Consultation</a>
        </div>
        {_email_footer()}
    </div>
    """

    import asyncio

    await asyncio.to_thread(
        resend.Emails.send,
        {
            "from": settings.EMAIL_FROM,
            "to": to_email,
            "subject": subject,
            "html": html,
            "attachments": [
                {
                    "filename": f"Kundli_Report_{user_name.replace(' ', '_')}.pdf",
                    "content": base64.b64encode(pdf_bytes).decode("utf-8"),
                }
            ],
        },
    )


# ── Muhurta (Auspicious Birth-Time) analysis email ──────────────────────────
# (key, 3-letter header) — full names spelled out in the legend. The 12 aspects
# made the email table too wide, so headers are abbreviated and cells stay G/M/W.
_MUHURTA_ASPECTS = [
    ("health", "Hth"), ("longevity", "Lng"), ("wealth", "Wth"),
    ("career", "Car"), ("property", "Prp"), ("marriage", "Mrg"),
    ("children", "Chd"), ("family", "Fam"), ("education", "Edu"),
    ("fortune", "Ftn"), ("foreign", "Frn"), ("spiritual", "Spr"),
]
_MUHURTA_ASPECT_LEGEND = ("Hth Health &middot; Lng Longevity &middot; Wth Wealth &middot; Car Career &middot; "
                          "Prp Property &middot; Mrg Marriage &middot; Chd Children &middot; Fam Family &middot; "
                          "Edu Education &middot; Ftn Fortune &middot; Frn Foreign &middot; Spr Spiritual")
_MUHURTA_CELL = {
    "good": ("#dcfce7", "#166534", "G"),
    "moderate": ("#fef9c3", "#854d0e", "M"),
    "challenging": ("#fee2e2", "#991b1b", "W"),
}


# ── Numerology (Moolank / Bhagyank) — display only ──────────────────────────
# Classical number -> planet. Moolank = root number of the birth day; Bhagyank
# = destiny number of the full date, each reduced to 1-9. Rahu(4)/Ketu(7) are
# the shadow planets. NOTE: this is a display readout only. Tested against the
# fame gold-set (Moolank/Bhagyank planet overlapping the functional benefics)
# and found NOT predictive — famous charts sit at the random base rate — so it
# is shown for interest and never enters any score.
_NUM_PLANET = {1: "Sun", 2: "Moon", 3: "Jupiter", 4: "Rahu", 5: "Mercury",
               6: "Venus", 7: "Ketu", 8: "Saturn", 9: "Mars"}


def _digit_sum(n: int) -> int:
    n = abs(int(n))
    while n > 9:
        n = sum(int(c) for c in str(n))
    return n


def _numerology(date_str: str) -> dict:
    """Moolank (root, from the day) + Bhagyank (destiny, from the whole date),
    each 1-9, with its ruling planet. ``date_str`` is ISO YYYY-MM-DD."""
    day = int(date_str[8:10])
    moolank = _digit_sum(day)
    bhagyank = _digit_sum(sum(int(c) for c in date_str if c.isdigit()))
    return {"moolank": moolank, "moolank_planet": _NUM_PLANET[moolank],
            "bhagyank": bhagyank, "bhagyank_planet": _NUM_PLANET[bhagyank]}


def _numerology_line(date_str: str) -> str:
    """Compact inline text: Moolank N (Planet) · Bhagyank N (Planet)."""
    nm = _numerology(date_str)
    return (f'Moolank <strong>{nm["moolank"]}</strong> ({nm["moolank_planet"]}) '
            f'&middot; Bhagyank <strong>{nm["bhagyank"]}</strong> ({nm["bhagyank_planet"]})')


def _numerology_badge(date_str: str) -> str:
    """A centred pill for a single-date email (muhurta / 1-day unshakable)."""
    return (
        '<div style="text-align:center;margin:0 0 18px;">'
        '<span style="display:inline-block;background:#f7f5fb;border:1px solid #e7e2f0;'
        'border-radius:20px;padding:6px 16px;font-size:12px;color:#4c1d95;">'
        f'&#128302; {_numerology_line(date_str)}</span>'
        '<div style="font-size:10px;color:#aaa;margin-top:4px;">Moolank = root number of the day '
        '&middot; Bhagyank = destiny number of the full date</div></div>'
    )


_WP_LABELS = [
    ("rahu_prime", "Rahu prime-dasha"), ("d60", "D60 dignity"),
    ("av_10th", "10th-house AV"), ("av_11th", "11th-house AV"), ("av_1st", "1st-house AV"),
    ("upa_occ", "Upachaya dasha"), ("raja_late", "Late Raja"), ("dhana_late", "Late Dhana"),
    ("bright_moon", "Bright Moon"), ("moon_disp", "Moon-lord in 1/2/11/12"), ("moon_sav", "Moon-sign AV"),
    ("sun_disp", "Sun-lord in 1st quadrant"),
]


def _worldly_breakdown(wp: dict) -> str:
    """The 7 worldly-potential factors with an up/down marker vs the average chart."""
    f = wp.get("factors", {})
    parts = []
    for k, lbl in _WP_LABELS:
        z = f.get(k, {}).get("z", 0)
        if z > 0.05:
            arrow, col = "&#9650;", "#166534"   # above average
        elif z < -0.05:
            arrow, col = "&#9660;", "#991b1b"   # below average
        else:
            arrow, col = "&ndash;", "#999"
        parts.append(f'<span style="white-space:nowrap;margin-right:14px;display:inline-block;">'
                     f'{lbl} <span style="color:{col};font-weight:bold;">{arrow}</span></span>')
    return "".join(parts)


def _render_muhurta_html(result: dict) -> str:
    th = "background:#7c3aed;color:#fff;padding:5px 4px;font-size:11px;text-align:center;"
    # Narrower header for the 12 aspect columns so the table fits email width.
    ath = "background:#7c3aed;color:#fff;padding:5px 2px;font-size:10px;text-align:center;"
    head_cells = "".join(f'<th style="{ath}">{short}</th>' for _k, short in _MUHURTA_ASPECTS)
    rows = ""
    for w in result["windows"]:
        cells = ""
        for key, _short in _MUHURTA_ASPECTS:
            v = w["aspects"].get(key, {}).get("verdict", "moderate")
            bg, fg, ltr = _MUHURTA_CELL[v]
            cells += f'<td style="background:{bg};color:{fg};text-align:center;font-weight:bold;padding:5px 0;border:1px solid #fff;font-size:11px;">{ltr}</td>'
        lord = w["lagna_lord"] + (" (R)" if w.get("lord_retrograde") else "")
        hl = w.get("highlighted")
        tr_style = "background:#ede9fe;" if hl else ""
        star = ' <span style="color:#7c3aed;">&#9733;</span>' if hl else ""
        wp = w.get("worldly_potential")
        wp_cell = (
            f'<td style="padding:4px 3px;text-align:center;color:#7c3aed;font-weight:bold;">{round(wp["score"])}</td>'
            if wp else '<td style="padding:4px 3px;text-align:center;color:#bbb;">&ndash;</td>'
        )
        rows += (
            f'<tr style="{tr_style}"><td style="padding:4px 3px;font-weight:bold;color:#7c3aed;">{w["rank"]}</td>'
            f'<td style="padding:4px 4px;font-weight:bold;white-space:nowrap;">{w["lagna_name"]}{star}</td>'
            f'<td style="padding:4px 4px;white-space:nowrap;">{lord}</td>'
            f'<td style="padding:4px 4px;white-space:nowrap;font-size:11px;">{w["window"]["start"]}&ndash;{w["window"]["end"]}</td>'
            f'<td style="padding:4px 3px;text-align:center;font-weight:bold;">{round(w["overall"])}</td>{wp_cell}{cells}</tr>'
        )
    grid = (
        '<div style="overflow-x:auto;-webkit-overflow-scrolling:touch;">'
        '<table style="width:100%;border-collapse:collapse;font-family:sans-serif;font-size:12px;min-width:560px;">'
        f'<tr><th style="{th}">#</th><th style="{th}">Lagna</th><th style="{th}">Lord</th>'
        f'<th style="{th}">Window</th><th style="{th}">Str</th><th style="{th}">Pot</th>{head_cells}</tr>{rows}</table>'
        '</div>'
    )
    pos_rows = ""
    for i, p in enumerate(result.get("planet_positions", [])):
        bg = "#faf9ff" if i % 2 else "#ffffff"
        mc = "#b91c1c" if p.get("retrograde") else "#15803d"
        pos_rows += (
            f'<tr style="background:{bg};"><td style="padding:5px 8px;font-weight:bold;">{p["planet"]}</td>'
            f'<td style="padding:5px 8px;">{p["sign"]}</td>'
            f'<td style="padding:5px 8px;">{p["degree_dms"]}</td>'
            f'<td style="padding:5px 8px;color:{mc};font-weight:bold;">{p["motion"]}</td></tr>'
        )
    positions = (
        '<table style="width:100%;border-collapse:collapse;font-family:sans-serif;font-size:13px;">'
        f'<tr><th style="{th};text-align:left;">Planet</th><th style="{th};text-align:left;">Rashi</th>'
        f'<th style="{th};text-align:left;">Degree</th><th style="{th};text-align:left;">Motion</th></tr>{pos_rows}</table>'
    )
    pr = result.get("priorities") or []
    prioritised = f' &middot; prioritised for: <strong>{", ".join(pr)}</strong>' if pr else ""
    # "Already born?" banner — point to the Lagna rising at the given time.
    banner = ""
    hl_lagna, qt = result.get("highlight_lagna"), result.get("query_time")
    if hl_lagna and qt:
        hlw = next((w for w in result["windows"] if w.get("highlighted")), None)
        rank = hlw["rank"] if hlw else "?"
        banner = (
            f'<p style="background:#ede9fe;border-left:4px solid #7c3aed;padding:10px 14px;'
            f'border-radius:4px;color:#4c1d95;margin:0 0 16px;">At your chosen time '
            f'<strong>{qt}</strong>, the rising Lagna is <strong>{hl_lagna}</strong> '
            f'(highlighted &#9733; below, ranked <strong>#{rank}</strong> of 12 for the day).</p>'
        )
    pos_label = result.get("positions_time", "12:00")
    prom_on = result.get("optimize_prominence")
    wp_note = (
        '<p style="font-size:11px;color:#999;margin:6px 0 0;line-height:1.5;">'
        '<strong>Pot</strong> = Worldly Prominence Potential (0&ndash;100): a faint statistical tilt '
        '(~0.63 AUC) toward markers seen in prominent charts. Most of worldly success lies outside the '
        'chart &mdash; treat this as potential, not destiny.'
        + (' &nbsp;These windows are ranked with potential blended in (0.6 auspiciousness + 0.4 potential).'
           if prom_on else '')
        + '</p>'
    )
    # Per-factor worldly breakdown for the recommended pick (highlighted, else #1).
    bw = next((w for w in result["windows"] if w.get("highlighted")), None)
    if bw is None and result["windows"]:
        bw = result["windows"][0]
    bwp = bw.get("worldly_potential") if bw else None
    breakdown_block = ""
    if bwp:
        breakdown_block = (
            '<div style="margin:12px 0 0;padding:10px 14px;background:#f7f5fb;border:1px solid #e7e2f0;border-radius:8px;">'
            f'<p style="font-size:12px;color:#555;margin:0 0 5px;"><strong>Worldly-potential factors</strong> &mdash; '
            f'{bw["lagna_name"]} (Pot {round(bwp["score"])}) &nbsp;<span style="color:#166534;">&#9650;</span> above average'
            f' &nbsp;<span style="color:#991b1b;">&#9660;</span> below</p>'
            f'<p style="font-size:12px;color:#444;margin:0;line-height:1.8;">{_worldly_breakdown(bwp)}</p></div>'
        )
    return f"""
    <div style="font-family: sans-serif; max-width: 760px; margin: 0 auto; background:#ffffff;">
        {_email_header()}
        <h2 style="color:#7c3aed;text-align:center;margin:0 0 4px;">Auspicious Birth-Time Analysis</h2>
        <p style="text-align:center;color:#666;margin:0 0 12px;">
            {result["date"]} &middot; {result["place_name"]}{prioritised}
        </p>
        {_numerology_badge(result["date"])}
        <p style="color:#555;">Each row below is one rising ascendant (Lagna) for the day, ranked by overall
        strength. The coloured cells show how that Lagna favours each area of life. No Lagna is perfect —
        choose the window that best matches what your family values.</p>
        {banner}
        <h3 style="color:#7c3aed;margin:20px 0 8px;">Rising Lagna Windows</h3>
        {grid}
        <p style="font-size:12px;color:#777;margin:8px 0 0;">
            <span style="background:#dcfce7;color:#166534;font-weight:bold;padding:1px 6px;border-radius:8px;">G</span> Good
            &nbsp; <span style="background:#fef9c3;color:#854d0e;font-weight:bold;padding:1px 6px;border-radius:8px;">M</span> Moderate
            &nbsp; <span style="background:#fee2e2;color:#991b1b;font-weight:bold;padding:1px 6px;border-radius:8px;">W</span> Weak
            &nbsp; &middot; (R) = Lagna-lord retrograde &middot; Str = overall strength 0&ndash;100 &middot; Pot = worldly-potential
        </p>
        <p style="font-size:11px;color:#888;margin:6px 0 0;">Aspect columns: {_MUHURTA_ASPECT_LEGEND}</p>
        {wp_note}
        {breakdown_block}
        <h3 style="color:#7c3aed;margin:28px 0 8px;">Planetary Positions ({result["date"]}, {pos_label})</h3>
        {positions}
        <p style="font-size:12px;color:#999;margin:16px 0 0;">Computed with Lahiri ayanamsha (Swiss Ephemeris),
        Whole-Sign houses, Ashtakavarga &amp; Shadbala. Guidance only &mdash; consult an astrologer for a final decision.</p>
        <div style="text-align:center;margin:24px 0;">
            <a href="{settings.FRONTEND_URL}/services/" style="background:#7c3aed;color:white;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:bold;">Book a Consultation</a>
        </div>
        {_email_footer()}
    </div>
    """


def send_muhurta_analysis(to_email: str, result: dict) -> None:
    """Render + send the birth-muhurta analysis email (synchronous; safe to call
    from a background worker thread). No-ops with a log if RESEND_API_KEY unset."""
    subject = f"Your Auspicious Birth-Time Analysis — {result.get('date', '')}"
    _send_email(to_email, subject, _render_muhurta_html(result))


# ── Unshakable Chart Finder email ────────────────────────────────────────────
_U_TH = "background:#7c3aed;color:#fff;padding:5px 6px;font-size:11px;text-align:center;"

# Calibrated from the composite's real distribution over 303 diverse charts
# (min ~46, median ~61, p90 ~67, p99 ~71.5, max ~72.6). A two-point map
# [floor, ceiling] -> [0, 100]% so a typical chart reads ~59%, a top-decile chart
# ~81%, and a top-1% chart ~100%; a rare over-achiever legitimately exceeds 100%.
_POTENTIAL_FLOOR = 45.0
_POTENTIAL_CEILING = 72.0


def _potential_pct(score: float) -> int:
    return max(0, round((score - _POTENTIAL_FLOOR) / (_POTENTIAL_CEILING - _POTENTIAL_FLOOR) * 100))


# Short labels for the 8 strength-stack factors, shown under the count.
_STACK_ABBR = {"Shadbala": "Shad", "Ashtakavarga": "AV", "Dignity": "Dig",
               "Lagna-lord": "LagL", "Placement": "Place", "Dhana": "Dhana",
               "Prosperity": "Prosp", "Raja": "Raja"}


def _u_chart_row(rank, c, bg, dated=False):
    """One ranked chart row (rank, [date], time, lagna, score, S·Y·L·F, longevity
    band). Exceptional (>= bar) charts are starred + tinted."""
    L = c["layers"]
    ayu = c["ayurdaya"]
    if c.get("exceptional"):
        bg = "#ede9fe"
    star = ' <span style="color:#7c3aed;">&#9733;</span>' if c.get("exceptional") else ""
    date_cell = f'<td style="padding:5px 6px;white-space:nowrap;">{c["date"]}</td>' if dated else ""
    num_cell = ""
    if dated:
        nm = _numerology(c["date"])
        num_cell = (f'<td style="padding:5px 6px;text-align:center;font-size:11px;color:#7c3aed;'
                    f'white-space:nowrap;">{nm["moolank"]}&middot;{nm["bhagyank"]}</td>')
    stack = c.get("strength_stack") or {}
    if "count" in stack:
        names = "&middot;".join(_STACK_ABBR.get(s, s[:4]) for s in stack.get("strong", []))
        name_line = f'<br><span style="font-size:9px;color:#999;font-weight:normal;">{names}</span>' if names else ""
        stack_txt = f'{stack["count"]}/{stack.get("of", 8)}{name_line}'
    else:
        stack_txt = "&ndash;"
    w = L.get("worldly")
    w_txt = round(w) if w is not None else "&ndash;"
    return (
        f'<tr style="background:{bg};">'
        f'<td style="padding:5px 6px;font-weight:bold;color:#7c3aed;">{rank}</td>'
        f'{date_cell}{num_cell}'
        f'<td style="padding:5px 6px;">{c["time"]}</td>'
        f'<td style="padding:5px 6px;white-space:nowrap;">{c["lagna"]}{star}</td>'
        f'<td style="padding:5px 6px;text-align:center;font-weight:bold;font-size:14px;">{_potential_pct(c["score"])}%</td>'
        f'<td style="padding:5px 6px;text-align:center;font-weight:bold;color:#7c3aed;">{stack_txt}</td>'
        f'<td style="padding:5px 6px;text-align:center;color:#666;font-size:11px;">'
        f'{round(L["structural"])}&middot;{round(L["yoga"])}&middot;{round(L["longevity"])}&middot;{round(L["fame"])}&middot;{w_txt}</td>'
        f'<td style="padding:5px 6px;white-space:nowrap;font-size:11px;">{ayu["band"][0]}&ndash;{ayu["band"][1]} {ayu["label"].split()[0]}</td>'
        f'</tr>'
    )


def _u_table(charts, start_rank=1, dated=False):
    date_h = f'<th style="{_U_TH}">Date</th><th style="{_U_TH}">Num</th>' if dated else ""
    head = (f'<tr><th style="{_U_TH}">#</th>{date_h}<th style="{_U_TH}">Time</th><th style="{_U_TH}">Lagna</th>'
            f'<th style="{_U_TH}">Potential</th><th style="{_U_TH}">Stack</th>'
            f'<th style="{_U_TH}">S&middot;Y&middot;L&middot;F&middot;W</th><th style="{_U_TH}">Longevity</th></tr>')
    rows = "".join(_u_chart_row(start_rank + i, c, "#faf9ff" if i % 2 else "#ffffff", dated)
                   for i, c in enumerate(charts))
    return ('<table style="width:100%;border-collapse:collapse;font-family:sans-serif;font-size:12px;">'
            f'{head}{rows}</table>')


def _u_positions(result):
    if not result.get("planet_positions"):
        return ""
    rows = ""
    for i, p in enumerate(result["planet_positions"]):
        bg = "#faf9ff" if i % 2 else "#ffffff"
        mc = "#b91c1c" if p.get("retrograde") else "#15803d"
        rows += (f'<tr style="background:{bg};"><td style="padding:5px 8px;font-weight:bold;">{p["planet"]}</td>'
                 f'<td style="padding:5px 8px;">{p["sign"]}</td><td style="padding:5px 8px;">{p["degree_dms"]}</td>'
                 f'<td style="padding:5px 8px;color:{mc};font-weight:bold;">{p["motion"]}</td></tr>')
    return (f'<h3 style="color:#7c3aed;margin:28px 0 8px;">Planetary Positions '
            f'({result["start_date"]}, {result.get("positions_time", "12:00")})</h3>'
            '<table style="width:100%;border-collapse:collapse;font-family:sans-serif;font-size:13px;">'
            f'<tr><th style="{_U_TH};text-align:left;">Planet</th><th style="{_U_TH};text-align:left;">Rashi</th>'
            f'<th style="{_U_TH};text-align:left;">Degree</th><th style="{_U_TH};text-align:left;">Motion</th></tr>{rows}</table>')


def _render_unshakable_html(result: dict) -> str:
    n = result.get("exceptional_count", 0)
    bar_pct = _potential_pct(result.get("bar", 72))
    top_list = result.get("top_overall") or []
    strongest_pct = _potential_pct(top_list[0]["score"]) if top_list else None
    if n:
        summary = (
            f'<p style="background:#ede9fe;border-left:4px solid #7c3aed;padding:10px 14px;border-radius:4px;color:#4c1d95;">'
            f'<strong>{n}</strong> genuinely strong chart(s) here (&ge; {bar_pct}% of potential, marked &#9733;). '
            'Every moment below is ranked by its potential score.</p>'
        )
    else:
        strong_txt = f' The strongest reaches <strong>{strongest_pct}%</strong>.' if strongest_pct is not None else ''
        summary = (
            f'<p style="color:#555;">No standout chart (&ge; {bar_pct}% of potential) in this window &mdash; '
            f'{bar_pct}%+ is rare and genuinely strong.{strong_txt} Every moment is still ranked below by its '
            'potential score; widen the date range for more options.</p>'
        )

    if result["days"] == 1:
        charts = result["per_day"][0]["charts"] if result["per_day"] else []
        body = (
            f'{summary}'
            f'{_numerology_badge(result["start_date"])}'
            '<h3 style="color:#7c3aed;margin:20px 0 8px;">Every Rising Lagna, Ranked</h3>'
            f'{_u_table(charts)}'
            f'{_u_positions(result)}'
        )
    elif result["days"] <= 7:
        sections = ""
        for day in result["per_day"]:
            sections += (f'<h3 style="color:#7c3aed;margin:22px 0 6px;">{day["date"]} &mdash; top {len(day["charts"])} '
                         f'<span style="font-size:12px;font-weight:normal;color:#7c3aed;">'
                         f'&#128302; {_numerology_line(day["date"])}</span></h3>'
                         f'{_u_table(day["charts"])}')
        body = f'{summary}{sections}'
    else:
        top = result.get("top_overall", [])
        body = (
            f'{summary}'
            f'<h3 style="color:#7c3aed;margin:20px 0 8px;">Strongest {len(top)} Moments '
            f'({result["days"]} days)</h3>'
            f'{_u_table(top, dated=True)}'
        )

    body += ('<p style="font-size:11px;color:#888;margin:8px 0 0;">'
             'Potential = strength as a % of the practical ceiling (calibrated from 300+ charts): ~59% is a '
             'typical chart, ~80% top-decile, 100% the top ~1%; a rare chart exceeds 100%. '
             'Stack = how many of 8 strength factors are notably strong (Shadbala, Ashtakavarga, dignity, '
             'Lagna-lord, placement, Dhana, Prosperity, Raja) &mdash; the strong ones are named beneath the count. '
             'S&middot;Y&middot;L&middot;F&middot;W = Structural &middot; Yoga &middot; Longevity &middot; Fame &middot; Worldly-potential layer scores (0&ndash;100). '
             'Num = Moolank&middot;Bhagyank (the date&rsquo;s root &amp; destiny numbers, 1&ndash;9). '
             f'Longevity = indicative Ayurdaya band (estimates only). &#9733; = genuinely strong (&ge; {bar_pct}% of potential).</p>')

    return f"""
    <div style="font-family: sans-serif; max-width: 760px; margin: 0 auto; background:#ffffff;">
        {_email_header()}
        <h2 style="color:#7c3aed;text-align:center;margin:0 0 4px;">Unshakable Birth-Time Search</h2>
        <p style="text-align:center;color:#666;margin:0 0 20px;">
            {result["start_date"]} &middot; {result["days"]} day(s) &middot; {result["place_name"]}
        </p>
        {body}
        <p style="font-size:12px;color:#999;margin:18px 0 0;">Composite of Shadbala, Ashtakavarga, dignity, yogas,
        longevity &amp; fame (Lahiri ayanamsha, Whole-Sign houses). The yoga/longevity/fame layers are classical
        heuristics &mdash; indicative, not absolute. Guidance only; consult an astrologer for a final decision.</p>
        <div style="text-align:center;margin:24px 0;">
            <a href="{settings.FRONTEND_URL}/services/" style="background:#7c3aed;color:white;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:bold;">Book a Consultation</a>
        </div>
        {_email_footer()}
    </div>
    """


def send_unshakable_analysis(to_email: str, result: dict) -> None:
    """Render + send the unshakable search results (synchronous; safe from a
    background worker thread). No-ops with a log if RESEND_API_KEY unset."""
    subject = f"Your Auspicious Birth Charts — {result.get('start_date', '')} (+{result.get('days', '')}d)"
    _send_email(to_email, subject, _render_unshakable_html(result))
