"""Tests for the Unshakable router, Lambda routing, and email rendering.

Fast: the heavy finder is never run here (endpoint only enqueues; Lambda routing
is patched; email render uses a canned result).
"""
import json

from app.dependencies import get_message_queue
from app.main import app
from app.services.email_service import _render_unshakable_html
from app.workers import kundli_lambda

_REQ = {
    "start_date": "2026-06-20", "days": 7, "lat": 21.7333, "lon": 70.6167,
    "place_name": "Jetpur", "email": "test@example.com", "bar": 90.0,
}

_RESULT = {
    "start_date": "2026-06-20", "days": 7, "place_name": "Jetpur", "bar": 90.0,
    "candidates": [{
        "date": "2026-06-26", "time": "01:02", "lagna": "Pisces", "score": 76.1,
        "layers": {"structural": 70.0, "yoga": 100.0, "longevity": 73.5, "fame": 83.5},
        "ayurdaya": {"band": [75.3, 85.7], "label": "Purnayu (full)"},
        "yogas": ["Hamsa Yoga"], "balarishta": [], "atmakaraka": "Mars",
    }],
}


async def test_find_endpoint_enqueues_job(client, fake_queue):
    app.dependency_overrides[get_message_queue] = lambda: fake_queue
    try:
        resp = await client.post("/api/unshakable/find", json=_REQ)
        assert resp.status_code == 202
        assert len(fake_queue.sent) == 1
        payload = fake_queue.sent[0]
        assert payload["type"] == "unshakable"
        assert payload["email"] == "test@example.com"
        assert payload["days"] == 7
    finally:
        app.dependency_overrides.pop(get_message_queue, None)


async def test_requires_email(client, fake_queue):
    app.dependency_overrides[get_message_queue] = lambda: fake_queue
    try:
        body = {k: v for k, v in _REQ.items() if k != "email"}
        resp = await client.post("/api/unshakable/find", json=body)
        assert resp.status_code == 422
        assert len(fake_queue.sent) == 0
    finally:
        app.dependency_overrides.pop(get_message_queue, None)


async def test_days_capped_at_week(client, fake_queue):
    app.dependency_overrides[get_message_queue] = lambda: fake_queue
    try:
        resp = await client.post("/api/unshakable/find", json={**_REQ, "days": 31})
        assert resp.status_code == 422  # week-scale cap (le=7)
        assert len(fake_queue.sent) == 0
    finally:
        app.dependency_overrides.pop(get_message_queue, None)


async def test_lambda_routes_unshakable_message(mocker):
    captured = {}
    mocker.patch.object(kundli_lambda, "_run_unshakable_sync", lambda body: captured.update(body))
    await kundli_lambda._process_record({"body": json.dumps({"type": "unshakable", **_REQ})})
    assert captured["type"] == "unshakable" and captured["email"] == "test@example.com"


def test_email_renders_candidates():
    html = _render_unshakable_html(_RESULT)
    assert "Unshakable Birth-Time Search" in html
    assert "Pisces" in html and "76.1" in html and "Purnayu" in html


def test_email_renders_fallback():
    result = {**_RESULT, "candidates": [],
              "fallback": {"date": "2026-06-26", "time": "01:02", "lagna": "Pisces", "score": 68.4}}
    html = _render_unshakable_html(result)
    assert "No chart cleared" in html and "Pisces" in html
