"""Tests for the SQS-triggered Lambda handler.

The handler itself is thin — its job is to deserialize the SQS event,
reconstruct domain objects, and report partial-batch failures correctly.
We mock the use case (`_get_processor()`) so these tests don't need a
Mongo connection or a real renderer.
"""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, patch

import pytest
from bson import ObjectId


SAMPLE_REQUEST = {
    "name": "Nandish Dave",
    "gender": "male",
    "dob": "1988-11-11",
    "tob": "12:55",
    "lat": 21.7545,
    "lon": 70.6233,
    "place_name": "Jetpur, Gujarat, India",
    "email": "test@example.com",
}


def _make_sqs_event(record_id: str, request: dict, message_id: str = "msg-1") -> dict:
    return {
        "Records": [
            {
                "messageId": message_id,
                "body": json.dumps({"record_id": record_id, **request}),
                "eventSource": "aws:sqs",
            }
        ]
    }


def test_handler_dispatches_to_processor_and_returns_no_failures():
    from app.workers import kundli_lambda

    record_id = ObjectId()
    event = _make_sqs_event(str(record_id), SAMPLE_REQUEST)

    fake_processor = AsyncMock()
    with patch.object(kundli_lambda, "_get_processor", return_value=fake_processor):
        result = kundli_lambda.handler(event, context=None)

    assert result == {"batchItemFailures": []}
    fake_processor.execute.assert_awaited_once()
    call_args = fake_processor.execute.await_args
    assert call_args.args[0] == record_id
    passed_req = call_args.args[1]
    assert passed_req.email == SAMPLE_REQUEST["email"]
    assert passed_req.name == SAMPLE_REQUEST["name"]


def test_handler_marks_failed_message_for_redrive():
    """Bad payload → message id surfaces in batchItemFailures so SQS retries."""
    from app.workers import kundli_lambda

    bad_event = {
        "Records": [
            {
                "messageId": "msg-bad",
                "body": "this-is-not-json",
                "eventSource": "aws:sqs",
            }
        ]
    }

    with patch.object(kundli_lambda, "_get_processor", return_value=AsyncMock()):
        result = kundli_lambda.handler(bad_event, context=None)

    assert result == {"batchItemFailures": [{"itemIdentifier": "msg-bad"}]}


def test_handler_partial_batch_returns_only_failed_ids():
    """One good + one bad message → only the bad one gets redriven."""
    from app.workers import kundli_lambda

    record_id = ObjectId()
    event = {
        "Records": [
            {
                "messageId": "msg-good",
                "body": json.dumps({"record_id": str(record_id), **SAMPLE_REQUEST}),
                "eventSource": "aws:sqs",
            },
            {
                "messageId": "msg-bad",
                "body": "{not json",
                "eventSource": "aws:sqs",
            },
        ]
    }

    with patch.object(kundli_lambda, "_get_processor", return_value=AsyncMock()):
        result = kundli_lambda.handler(event, context=None)

    assert result == {"batchItemFailures": [{"itemIdentifier": "msg-bad"}]}


def test_handler_empty_event_is_a_noop():
    from app.workers import kundli_lambda

    result = kundli_lambda.handler({"Records": []}, context=None)
    assert result == {"batchItemFailures": []}


def test_handler_processor_exception_redrives_message():
    """Use-case raised → message id added to batchItemFailures."""
    from app.workers import kundli_lambda

    record_id = ObjectId()
    event = _make_sqs_event(str(record_id), SAMPLE_REQUEST, message_id="msg-3")

    fake_processor = AsyncMock()
    fake_processor.execute.side_effect = RuntimeError("downstream boom")

    with patch.object(kundli_lambda, "_get_processor", return_value=fake_processor):
        result = kundli_lambda.handler(event, context=None)

    assert result == {"batchItemFailures": [{"itemIdentifier": "msg-3"}]}
