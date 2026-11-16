"""Local-development outbox pages — registered only when APP_ENV is
"development" (see `main.py`), so these routes do not exist on deployed
environments.

Jobs that production hands to SQS + the Lambda worker run in-process locally,
and the emails they would send are captured by `infrastructure/dev_outbox.py`.
These pages show them: the job page waits for the result, then redirects to
the email rendered as HTML.
"""

from __future__ import annotations

from html import escape

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, Response

from app.infrastructure import dev_outbox

router = APIRouter(prefix="/api/dev/outbox", tags=["Dev"], include_in_schema=False)

_BAR = (
    "font-family:sans-serif;background:#1f2937;color:#e5e7eb;padding:10px 16px;"
    "font-size:13px;line-height:1.6;"
)
_LINK = "color:#c4b5fd;"


def _page(title: str, body: str, refresh_seconds: int | None = None) -> HTMLResponse:
    refresh = f'<meta http-equiv="refresh" content="{refresh_seconds}">' if refresh_seconds else ""
    return HTMLResponse(
        f"<!doctype html><html><head><meta charset='utf-8'>{refresh}"
        f"<title>{escape(title)}</title></head>"
        f"<body style='margin:0;background:#f3f4f6;'>{body}</body></html>"
    )


def _message(title: str, text: str, refresh_seconds: int | None = None) -> HTMLResponse:
    body = (
        f"<div style='{_BAR}'>Dev outbox &middot; "
        f"<a style='{_LINK}' href='/api/dev/outbox'>all emails</a></div>"
        f"<div style='font-family:sans-serif;max-width:640px;margin:48px auto;padding:0 16px;'>"
        f"<h2 style='color:#7c3aed;'>{escape(title)}</h2>"
        f"<p style='color:#374151;white-space:pre-wrap;'>{escape(text)}</p></div>"
    )
    return _page(title, body, refresh_seconds)


@router.get("", response_class=HTMLResponse)
async def outbox() -> HTMLResponse:
    """Every captured email, newest first. Auto-refreshes."""
    rows = "".join(
        f"<tr><td style='padding:6px 12px;'>{e['created_at']:%H:%M:%S} UTC</td>"
        f"<td style='padding:6px 12px;'>{escape(e['to'])}</td>"
        f"<td style='padding:6px 12px;'><a href='/api/dev/outbox/emails/{e['id']}'>"
        f"{escape(e['subject'])}</a></td></tr>"
        for e in dev_outbox.list_emails()
    )
    table = (
        f"<table style='border-collapse:collapse;background:#fff;'>{rows}</table>"
        if rows
        else "<p style='color:#6b7280;'>No emails captured yet.</p>"
    )
    body = (
        f"<div style='{_BAR}'>Dev outbox &middot; emails captured instead of sent "
        f"(in memory, cleared when the API restarts)</div>"
        f"<div style='font-family:sans-serif;font-size:14px;padding:24px 16px;'>{table}</div>"
    )
    return _page("Dev outbox", body, refresh_seconds=5)


@router.get("/jobs/{job_id}")
async def job(job_id: str):
    """Wait page for an in-process job: refreshes while it runs, then
    redirects to the email it produced."""
    j = dev_outbox.get_job(job_id)
    if j is None:
        raise HTTPException(status_code=404, detail="Unknown job (the API may have restarted)")
    if j["status"] == "running":
        return _message(
            f"Running {j['kind']} job…",
            "This page refreshes by itself and opens the result when it is ready.",
            refresh_seconds=3,
        )
    if j["status"] == "failed":
        return _message(f"The {j['kind']} job failed", j["error"] or "See the API logs.")
    if j["email_id"] and dev_outbox.get_email(j["email_id"]):
        return RedirectResponse(f"/api/dev/outbox/emails/{j['email_id']}", status_code=303)
    return _message(
        f"The {j['kind']} job finished",
        "No email was captured for it. Either it was sent for real (RESEND_API_KEY "
        "is set) or the job recorded a failure — check the API logs.",
    )


@router.get("/emails/{email_id}", response_class=HTMLResponse)
async def email(email_id: str) -> HTMLResponse:
    """One captured email, rendered as the recipient would see it."""
    e = dev_outbox.get_email(email_id)
    if e is None:
        raise HTTPException(status_code=404, detail="Unknown email (the API may have restarted)")
    attachments = "".join(
        f" &middot; <a style='{_LINK}' target='_blank' "
        f"href='/api/dev/outbox/emails/{email_id}/attachments/{i}'>{escape(a['filename'])}</a>"
        for i, a in enumerate(e["attachments"])
    )
    body = (
        f"<div style='{_BAR}'><a style='{_LINK}' href='/api/dev/outbox'>Dev outbox</a> &middot; "
        f"<b>To:</b> {escape(e['to'])} &middot; <b>Subject:</b> {escape(e['subject'])}"
        f"{' &middot; <b>Attachments:</b>' + attachments if attachments else ''}</div>"
        f"<div style='padding:24px 8px;'>{e['html']}</div>"
    )
    return _page(e["subject"], body)


@router.get("/emails/{email_id}/attachments/{index}")
async def attachment(email_id: str, index: int) -> Response:
    e = dev_outbox.get_email(email_id)
    if e is None or not 0 <= index < len(e["attachments"]):
        raise HTTPException(status_code=404, detail="Unknown attachment")
    a = e["attachments"][index]
    return Response(
        content=a["content"],
        media_type=a["media_type"],
        headers={"Content-Disposition": f"inline; filename={a['filename']}"},
    )
