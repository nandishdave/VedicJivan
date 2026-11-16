"""Message queue abstraction — Protocol + AWS SQS implementation.

Used by the API to fan out long-running jobs (kundli PDF generation) to a
separate worker process. Mirrors the repository pattern: the use case /
router depends on the `MessageQueue` Protocol; production wires
`SqsMessageQueue`; tests substitute an in-memory fake.

Why an abstraction (not bare boto3 in the router):
  * Router-level tests don't need AWS credentials or network access.
  * Future swap (e.g. RabbitMQ, Redis Streams, Cloud Tasks) is local.
  * Failure semantics are explicit at the boundary.
"""

from __future__ import annotations

import asyncio
import json
from typing import Any, Protocol

import boto3

from app.infrastructure import dev_outbox
from app.infrastructure.logging import get_logger

logger = get_logger(__name__)


class MessageQueue(Protocol):
    """Send-only queue interface."""

    async def send(self, payload: dict[str, Any]) -> str:
        """Enqueue `payload` and return the broker-assigned message id."""
        ...


# ── AWS SQS implementation ──────────────────────────────────────────────────


class SqsMessageQueue:
    """Production impl — wraps a sync boto3 SQS client via `to_thread`.

    boto3 is synchronous; calling it directly from an async handler would
    block the event loop for the duration of the SQS round-trip (~30-150 ms).
    `asyncio.to_thread` punts the call to the default thread pool so other
    requests on the same Uvicorn worker keep moving.

    Fail-loud constructor: an empty `queue_url` raises immediately rather
    than silently dropping messages or accidentally talking to a default
    queue. Local-dev / test code should inject a fake queue, not a no-op
    SqsMessageQueue.
    """

    def __init__(self, queue_url: str, region: str) -> None:
        if not queue_url:
            raise RuntimeError(
                "SqsMessageQueue requires a non-empty queue_url. "
                "Set KUNDLI_QUEUE_URL or inject a fake MessageQueue in tests."
            )
        self._queue_url = queue_url
        self._client = boto3.client("sqs", region_name=region)

    async def send(self, payload: dict[str, Any]) -> str:
        body = json.dumps(payload, default=str)
        response = await asyncio.to_thread(
            self._client.send_message,
            QueueUrl=self._queue_url,
            MessageBody=body,
        )
        message_id = response["MessageId"]
        logger.info("Enqueued message id=%s to %s", message_id, self._queue_url)
        return message_id


# ── Local-development implementation ────────────────────────────────────────


class InProcessMessageQueue:
    """Local-dev impl — no broker. `send` runs the Lambda worker's record
    handler as a background task inside the API process, so the queued flows
    (kundli / muhurta / unshakable) work end to end without AWS.

    Wired by `get_message_queue` only when APP_ENV is "development" and no
    KUNDLI_QUEUE_URL is set. The returned message id is a dev-outbox job id;
    the job's outcome is viewable at /api/dev/outbox/jobs/<id>.
    """

    def __init__(self) -> None:
        # Hold references so running tasks aren't garbage-collected mid-flight.
        self._tasks: set[asyncio.Task] = set()

    async def send(self, payload: dict[str, Any]) -> str:
        job_id = dev_outbox.start_job(payload.get("type", "kundli"))
        record = {"messageId": job_id, "body": json.dumps(payload, default=str)}
        task = asyncio.create_task(self._run(job_id, record))
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)
        logger.info("Running job id=%s in-process (no KUNDLI_QUEUE_URL)", job_id)
        return job_id

    async def _run(self, job_id: str, record: dict[str, Any]) -> None:
        # Imported lazily: the worker pulls in the whole PDF/chart stack.
        from app.workers.kundli_lambda import _process_record

        dev_outbox.current_job.set(job_id)
        try:
            await _process_record(record)
        except Exception as e:
            logger.exception("In-process job %s failed", job_id)
            dev_outbox.finish_job(job_id, error=f"{type(e).__name__}: {e}")
        else:
            dev_outbox.finish_job(job_id)
