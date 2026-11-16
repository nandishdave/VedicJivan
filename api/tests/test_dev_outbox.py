"""Local-development mode: in-process job queue + the dev email outbox.

Covers `app.infrastructure.dev_outbox`, `InProcessMessageQueue`, the
`/api/dev/outbox` pages, and the environment gating that keeps all of it
out of deployed environments.
"""

from __future__ import annotations

import asyncio

import pytest

from app import dependencies
from app.config import settings
from app.infrastructure import dev_outbox
from app.infrastructure.queue import InProcessMessageQueue, SqsMessageQueue
from app.services import email_service


@pytest.fixture(autouse=True)
def _clean_outbox():
    dev_outbox.clear()
    yield
    dev_outbox.clear()


async def _drain(queue: InProcessMessageQueue) -> None:
    await asyncio.gather(*list(queue._tasks))


# ── Environment gating ──────────────────────────────────────────────────────


def test_is_dev_only_for_development(monkeypatch):
    for env, expected in [("development", True), ("test", False), ("production", False)]:
        monkeypatch.setattr(settings, "APP_ENV", env)
        assert dev_outbox.is_dev() is expected


def test_message_queue_is_in_process_in_dev_without_queue_url(monkeypatch):
    monkeypatch.setattr(dependencies, "_kundli_queue_singleton", None)
    monkeypatch.setattr(settings, "KUNDLI_QUEUE_URL", "")
    assert isinstance(dependencies.get_message_queue(), InProcessMessageQueue)


def test_message_queue_fails_loud_outside_dev_without_queue_url(monkeypatch):
    monkeypatch.setattr(dependencies, "_kundli_queue_singleton", None)
    monkeypatch.setattr(settings, "KUNDLI_QUEUE_URL", "")
    monkeypatch.setattr(settings, "APP_ENV", "production")
    with pytest.raises(RuntimeError, match="non-empty queue_url"):
        dependencies.get_message_queue()


def test_message_queue_uses_sqs_when_queue_url_set(monkeypatch):
    monkeypatch.setattr(dependencies, "_kundli_queue_singleton", None)
    monkeypatch.setattr(
        settings, "KUNDLI_QUEUE_URL", "https://sqs.ap-south-1.amazonaws.com/1/q"
    )
    assert isinstance(dependencies.get_message_queue(), SqsMessageQueue)


def test_email_is_skipped_not_captured_outside_dev(monkeypatch):
    monkeypatch.setattr(settings, "APP_ENV", "production")
    email_service._send_email("a@example.com", "Subject", "<p>hi</p>")
    assert dev_outbox.list_emails() == []


def test_preview_fields_empty_for_unknown_ids_and_outside_dev(monkeypatch):
    assert dev_outbox.preview_fields("sqs-message-id") == {}
    job_id = dev_outbox.start_job("muhurta")
    assert dev_outbox.preview_fields(job_id) == {
        "preview_url": f"{settings.APP_URL}/api/dev/outbox/jobs/{job_id}"
    }
    monkeypatch.setattr(settings, "APP_ENV", "production")
    assert dev_outbox.preview_fields(job_id) == {}


# ── Capture ─────────────────────────────────────────────────────────────────


def test_send_email_is_captured_in_dev():
    email_service._send_email("a@example.com", "Subject", "<p>hi</p>")
    [captured] = dev_outbox.list_emails()
    assert (captured["to"], captured["subject"], captured["html"]) == (
        "a@example.com", "Subject", "<p>hi</p>",
    )


async def test_kundli_report_is_captured_with_pdf_attachment():
    await email_service.send_kundli_report("a@example.com", "Test User", b"%PDF-fake")
    [captured] = dev_outbox.list_emails()
    assert captured["attachments"] == [
        {
            "filename": "Kundli_Report_Test_User.pdf",
            "content": b"%PDF-fake",
            "media_type": "application/pdf",
        }
    ]


def test_outbox_keeps_only_the_newest_emails():
    for i in range(dev_outbox.MAX_EMAILS + 5):
        dev_outbox.capture_email("a@example.com", f"s{i}", "")
    emails = dev_outbox.list_emails()
    assert len(emails) == dev_outbox.MAX_EMAILS
    assert emails[0]["subject"] == f"s{dev_outbox.MAX_EMAILS + 4}"  # newest first


# ── InProcessMessageQueue ───────────────────────────────────────────────────


async def test_in_process_queue_runs_job_and_links_its_email(mocker):
    """The email sent from the worker's thread is tied back to the job."""

    async def fake_process(record):
        await asyncio.to_thread(email_service._send_email, "a@example.com", "Done", "<p>r</p>")

    mocker.patch("app.workers.kundli_lambda._process_record", side_effect=fake_process)
    queue = InProcessMessageQueue()

    job_id = await queue.send({"type": "unshakable", "email": "a@example.com"})
    assert dev_outbox.get_job(job_id)["status"] == "running"
    await _drain(queue)

    job = dev_outbox.get_job(job_id)
    assert job["status"] == "done" and job["kind"] == "unshakable"
    assert dev_outbox.get_email(job["email_id"])["subject"] == "Done"


async def test_in_process_queue_records_failure(mocker):
    mocker.patch(
        "app.workers.kundli_lambda._process_record", side_effect=ValueError("bad date")
    )
    queue = InProcessMessageQueue()

    job_id = await queue.send({"type": "muhurta"})
    await _drain(queue)

    job = dev_outbox.get_job(job_id)
    assert job["status"] == "failed"
    assert job["error"] == "ValueError: bad date"


# ── Pages ───────────────────────────────────────────────────────────────────


async def test_job_page_waits_then_redirects_to_the_email(client):
    job_id = dev_outbox.start_job("unshakable")

    running = await client.get(f"/api/dev/outbox/jobs/{job_id}")
    assert running.status_code == 200
    assert 'http-equiv="refresh"' in running.text

    token = dev_outbox.current_job.set(job_id)
    try:
        email_id = dev_outbox.capture_email("a@example.com", "Charts", "<p>ranked</p>")
    finally:
        dev_outbox.current_job.reset(token)
    dev_outbox.finish_job(job_id)

    done = await client.get(f"/api/dev/outbox/jobs/{job_id}")
    assert done.status_code == 303
    assert done.headers["location"] == f"/api/dev/outbox/emails/{email_id}"

    page = await client.get(done.headers["location"])
    assert page.status_code == 200
    assert "<p>ranked</p>" in page.text and "a@example.com" in page.text


async def test_job_page_shows_failure(client):
    job_id = dev_outbox.start_job("muhurta")
    dev_outbox.finish_job(job_id, error="ValueError: bad <date>")
    resp = await client.get(f"/api/dev/outbox/jobs/{job_id}")
    assert resp.status_code == 200
    assert "failed" in resp.text and "bad &lt;date&gt;" in resp.text


async def test_job_page_when_done_without_captured_email(client):
    job_id = dev_outbox.start_job("kundli")
    dev_outbox.finish_job(job_id)
    resp = await client.get(f"/api/dev/outbox/jobs/{job_id}")
    assert resp.status_code == 200 and "No email was captured" in resp.text


async def test_outbox_list_and_attachment(client):
    empty = await client.get("/api/dev/outbox")
    assert "No emails captured yet" in empty.text

    email_id = dev_outbox.capture_email(
        "a@example.com", "Report <1>", "<p>x</p>",
        attachments=[{"filename": "r.pdf", "content": b"%PDF", "media_type": "application/pdf"}],
    )
    listing = await client.get("/api/dev/outbox")
    assert "Report &lt;1&gt;" in listing.text and email_id in listing.text

    pdf = await client.get(f"/api/dev/outbox/emails/{email_id}/attachments/0")
    assert pdf.content == b"%PDF" and pdf.headers["content-type"] == "application/pdf"
    assert (await client.get(f"/api/dev/outbox/emails/{email_id}/attachments/1")).status_code == 404


async def test_unknown_job_and_email_are_404(client):
    assert (await client.get("/api/dev/outbox/jobs/nope")).status_code == 404
    assert (await client.get("/api/dev/outbox/emails/nope")).status_code == 404


async def test_submit_endpoint_returns_preview_url_for_in_process_job(client, mocker):
    """End to end through the router: 202 carries the dev preview link."""
    mocker.patch("app.workers.kundli_lambda._process_record", return_value=None)
    queue = InProcessMessageQueue()
    from app.main import app

    app.dependency_overrides[dependencies.get_message_queue] = lambda: queue
    try:
        resp = await client.post(
            "/api/unshakable/find",
            json={
                "start_date": "2026-12-01", "days": 1, "lat": 21.7333, "lon": 70.6167,
                "place_name": "Jetpur", "email": "test@example.com",
            },
        )
    finally:
        app.dependency_overrides.pop(dependencies.get_message_queue, None)
    await _drain(queue)

    assert resp.status_code == 202
    assert "/api/dev/outbox/jobs/" in resp.json()["preview_url"]
