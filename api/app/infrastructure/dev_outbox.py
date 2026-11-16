"""Local-development outbox — an in-memory stand-in for SQS delivery + Resend.

Only active when APP_ENV is "development" (deployed environments set
"production" / "test" via Terraform). With no KUNDLI_QUEUE_URL the API runs
queued jobs in-process (`InProcessMessageQueue`); with no RESEND_API_KEY the
emails those jobs would send are captured here instead, and `routers/dev.py`
serves them as HTML pages so the result can be read in a browser.

State is per-process and lost on restart — a viewing aid, not storage.
"""

from __future__ import annotations

import uuid
from collections import OrderedDict
from contextvars import ContextVar
from datetime import UTC, datetime
from typing import Any

from app.config import settings
from app.infrastructure.logging import get_logger

logger = get_logger(__name__)

MAX_EMAILS = 50
MAX_JOBS = 200

# Job the current task/thread is working for — set by InProcessMessageQueue and
# inherited by `asyncio.to_thread`, so a captured email can be tied to its job.
current_job: ContextVar[str | None] = ContextVar("dev_outbox_current_job", default=None)

_emails: OrderedDict[str, dict[str, Any]] = OrderedDict()
_jobs: OrderedDict[str, dict[str, Any]] = OrderedDict()


def is_dev() -> bool:
    return settings.APP_ENV.lower() == "development"


def _trim(store: OrderedDict, limit: int) -> None:
    while len(store) > limit:
        store.popitem(last=False)


# ── Jobs ────────────────────────────────────────────────────────────────────


def start_job(kind: str) -> str:
    job_id = uuid.uuid4().hex
    _jobs[job_id] = {
        "id": job_id,
        "kind": kind,
        "status": "running",
        "error": None,
        "email_id": None,
        "started_at": datetime.now(UTC),
    }
    _trim(_jobs, MAX_JOBS)
    return job_id


def finish_job(job_id: str, error: str | None = None) -> None:
    job = _jobs.get(job_id)
    if job is not None:
        job["status"] = "failed" if error else "done"
        job["error"] = error


def get_job(job_id: str) -> dict[str, Any] | None:
    return _jobs.get(job_id)


def preview_fields(message_id: str) -> dict[str, str]:
    """Extra 202-response fields for an in-process job: where its result will
    appear. Empty for real SQS message ids (and always outside development)."""
    if is_dev() and message_id in _jobs:
        return {"preview_url": f"{settings.APP_URL}/api/dev/outbox/jobs/{message_id}"}
    return {}


# ── Emails ──────────────────────────────────────────────────────────────────


def capture_email(
    to: str,
    subject: str,
    html: str,
    attachments: list[dict[str, Any]] | None = None,
) -> str:
    """Store an email instead of sending it. `attachments` items are
    `{"filename": str, "content": bytes, "media_type": str}`."""
    email_id = uuid.uuid4().hex
    _emails[email_id] = {
        "id": email_id,
        "to": to,
        "subject": subject,
        "html": html,
        "attachments": attachments or [],
        "created_at": datetime.now(UTC),
    }
    _trim(_emails, MAX_EMAILS)
    job = _jobs.get(current_job.get() or "")
    if job is not None:
        job["email_id"] = email_id
    logger.info(
        "Email captured in dev outbox (no RESEND_API_KEY): %s/api/dev/outbox/emails/%s to=%s",
        settings.APP_URL, email_id, to,
    )
    return email_id


def get_email(email_id: str) -> dict[str, Any] | None:
    return _emails.get(email_id)


def list_emails() -> list[dict[str, Any]]:
    """Newest first."""
    return list(reversed(_emails.values()))


def clear() -> None:
    _emails.clear()
    _jobs.clear()
