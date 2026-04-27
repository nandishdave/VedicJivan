"""Unit tests for `app.infrastructure.queue`.

`botocore.stub.Stubber` ships with botocore — it lets us replay scripted
responses against a real boto3 client without ever hitting AWS. That keeps
the test fast (no network, no credentials) and faithful (the real client
serializes our payload + parses the stubbed XML reply).
"""

from __future__ import annotations

import json

import pytest
from botocore.stub import Stubber

from app.infrastructure.queue import SqsMessageQueue


QUEUE_URL = "https://sqs.ap-south-1.amazonaws.com/123456789012/test-queue"


def test_constructor_raises_on_empty_queue_url():
    """Fail loud: empty url means a misconfigured environment, not a no-op."""
    with pytest.raises(RuntimeError, match="non-empty queue_url"):
        SqsMessageQueue(queue_url="", region="ap-south-1")


@pytest.mark.asyncio
async def test_send_serialises_payload_and_returns_message_id():
    queue = SqsMessageQueue(queue_url=QUEUE_URL, region="ap-south-1")
    payload = {"record_id": "507f1f77bcf86cd799439011", "name": "Nandish"}

    with Stubber(queue._client) as stubber:
        stubber.add_response(
            "send_message",
            {"MessageId": "msg-abc-123", "MD5OfMessageBody": "x" * 32},
            expected_params={
                "QueueUrl": QUEUE_URL,
                "MessageBody": json.dumps(payload, default=str),
            },
        )

        message_id = await queue.send(payload)

        assert message_id == "msg-abc-123"
        stubber.assert_no_pending_responses()


@pytest.mark.asyncio
async def test_send_serialises_non_json_native_values():
    """ObjectId and datetime hit the queue via `default=str`, never crash."""
    from datetime import datetime, timezone

    from bson import ObjectId

    queue = SqsMessageQueue(queue_url=QUEUE_URL, region="ap-south-1")
    oid = ObjectId("507f1f77bcf86cd799439011")
    payload = {
        "record_id": oid,
        "queued_at": datetime(2026, 4, 21, 12, 0, tzinfo=timezone.utc),
    }

    expected_body = json.dumps(payload, default=str)
    with Stubber(queue._client) as stubber:
        stubber.add_response(
            "send_message",
            {"MessageId": "msg-2", "MD5OfMessageBody": "y" * 32},
            expected_params={"QueueUrl": QUEUE_URL, "MessageBody": expected_body},
        )

        await queue.send(payload)
        stubber.assert_no_pending_responses()
