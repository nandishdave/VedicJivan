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
