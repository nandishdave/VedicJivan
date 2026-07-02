"""AWS Lambda handler — processes one or more kundli generation jobs from SQS.

Triggered by an EventSourceMapping on the kundli SQS queue. Each invocation
receives an `event` shaped like:

    {
      "Records": [
        {
          "messageId": "...",
          "body": "{\"record_id\": \"...\", \"name\": \"...\", ...}",
          ...
        }
      ]
    }

We deserialize each record body, reconstruct (`ObjectId`, `KundliRequest`),
and run `ProcessKundliReport.execute()` — the same use case the in-process
BackgroundTask used to call. Failures per-message are reported via
`batchItemFailures` so SQS only redrives the bad ones.

Cold-start optimization:
  Module-level singletons (Mongo client, ProcessKundliReport, browser via
  the renderer factory) are reused across warm invocations. The first
  invocation pays the launch cost; subsequent ones reuse everything.
"""

from __future__ import annotations

import asyncio
import json
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings
from app.infrastructure.logging import configure_root_logging, get_logger
from app.models.kundli import KundliRequest
from app.repositories.kundli_repository import MongoKundliRepository
from app.services.email_service import send_kundli_report
from app.services.kundli_calculator import build_chart
from app.services.kundli_pdf import generate_pdf
from app.services.report_sections import load_report_sections
from app.use_cases.kundli import ProcessKundliReport, RenderKundliReport

configure_root_logging()
logger = get_logger(__name__)


# ── Cold-start singletons ────────────────────────────────────────────────────

_mongo_client: AsyncIOMotorClient | None = None
_processor: ProcessKundliReport | None = None


def _get_processor() -> ProcessKundliReport:
    """Build the use case once per Lambda execution environment."""
    global _mongo_client, _processor
    if _processor is None:
        _mongo_client = AsyncIOMotorClient(settings.MONGODB_URI)
        db = _mongo_client.get_default_database()
        repo = MongoKundliRepository(db)
        render = RenderKundliReport(
            build_chart=build_chart,
            generate_pdf=generate_pdf,
            load_report_sections=load_report_sections,
        )
        _processor = ProcessKundliReport(
            kundli_repo=repo,
            render_use_case=render,
            send_email=send_kundli_report,
        )
    return _processor


# ── Lambda entry point ───────────────────────────────────────────────────────


def _run_muhurta_sync(body: dict[str, Any]) -> None:
    """Run the full birth-muhurta analysis (incl. Shadbala) and email it. Imported
    lazily so kundli invocations don't pay for it. Synchronous CPU work, so the
    caller offloads it to a worker thread."""
    from app.services.email_service import send_muhurta_analysis
    from app.services.muhurta import analyze_birth_muhurta, build_muhurta_chart

    result = analyze_birth_muhurta(
        dob=body["date"],
        lat=body["lat"],
        lon=body["lon"],
        place_name=body["place_name"],
        chart_fn=build_muhurta_chart,
        priorities=body.get("priorities"),
        time=body.get("time"),
        optimize_prominence=body.get("optimize_prominence", False),
    )
    send_muhurta_analysis(body["email"], result)


def _run_unshakable_sync(body: dict[str, Any]) -> None:
    """Run a week-scale unshakable search (funnel) and email the ranked results.
    Imported lazily; synchronous CPU work offloaded to a worker thread."""
    from app.services.email_service import send_unshakable_analysis
    from app.services.unshakable_finder import find_unshakable

    result = find_unshakable(
        start_date=body["start_date"],
        days=body.get("days", 7),
        lat=body["lat"],
        lon=body["lon"],
        place_name=body["place_name"],
        bar=body.get("bar", 90.0),
        mode="bruteforce",  # complete per-day ranked menu (week-scale fits 300s)
    )
    send_unshakable_analysis(body["email"], result)


async def _process_record(record: dict[str, Any]) -> None:
    body = json.loads(record["body"])
    # Extra job types on the same queue, distinguished by `type` (kundli messages
    # have no `type`, so they keep working unchanged).
    if body.get("type") == "muhurta":
        await asyncio.to_thread(_run_muhurta_sync, body)
        return
    if body.get("type") == "unshakable":
        await asyncio.to_thread(_run_unshakable_sync, body)
        return
    record_id = ObjectId(body.pop("record_id"))
    req = KundliRequest(**body)
    await _get_processor().execute(record_id, req)


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """SQS-triggered Lambda entry point.

    Returns `{"batchItemFailures": [{"itemIdentifier": "..."}, ...]}` so
    AWS only redrives the failed messages from a partial-success batch.
    Lambda auto-deletes successfully-processed messages from the queue.
    """
    failures: list[dict[str, str]] = []
    records = event.get("Records", [])
    logger.info("Received %d SQS record(s)", len(records))

    for record in records:
        message_id = record.get("messageId", "<unknown>")
        try:
            asyncio.run(_process_record(record))
            logger.info("Processed message %s", message_id)
        except Exception:
            logger.exception("Failed to process message %s", message_id)
            failures.append({"itemIdentifier": message_id})

    return {"batchItemFailures": failures}
