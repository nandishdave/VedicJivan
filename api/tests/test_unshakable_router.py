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

def _chart(time, lagna, score, exceptional=False):
    return {
        "date": "2026-06-20", "time": time, "lagna": lagna, "score": score,
        "layers": {"structural": 70.0, "yoga": 100.0, "longevity": 73.5, "fame": 83.5},
        "ayurdaya": {"band": [75.3, 85.7], "label": "Purnayu (full)"},
        "yogas": ["Hamsa Yoga"], "balarishta": [], "atmakaraka": "Mars",
        "exceptional": exceptional,
        "dhana": 6, "prosperity": 3, "raja": 8, "strength_stack": {"count": 5, "of": 8},
    }


_RESULT = {
    "start_date": "2026-06-20", "days": 1, "place_name": "Jetpur", "bar": 90.0,
    "exceptional_count": 0,
    "per_day": [{"date": "2026-06-20", "charts": [_chart("03:01", "Aries", 76.1)]}],
    "planet_positions": [{"planet": "Sun", "sign": "Gemini", "degree_dms": "05° 00'",
                          "motion": "Direct", "retrograde": False}],
    "positions_time": "12:00",
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


async def test_days_capped_at_month(client, fake_queue):
    app.dependency_overrides[get_message_queue] = lambda: fake_queue
    try:
        resp = await client.post("/api/unshakable/find", json={**_REQ, "days": 32})
        assert resp.status_code == 422  # month-scale cap (le=31)
        assert len(fake_queue.sent) == 0
        ok = await client.post("/api/unshakable/find", json={**_REQ, "days": 30})
        assert ok.status_code == 202  # a month is allowed
    finally:
        app.dependency_overrides.pop(get_message_queue, None)


async def test_lambda_routes_unshakable_message(mocker):
    captured = {}
    mocker.patch.object(kundli_lambda, "_run_unshakable_sync", lambda body: captured.update(body))
    await kundli_lambda._process_record({"body": json.dumps({"type": "unshakable", **_REQ})})
    assert captured["type"] == "unshakable" and captured["email"] == "test@example.com"


def test_email_renders_single_day_with_positions():
    html = _render_unshakable_html(_RESULT)
    assert "Unshakable Birth-Time Search" in html
    assert "Every Rising Lagna" in html and "Planetary Positions" in html
    assert "Aries" in html and "76.1" in html and "Gemini" in html  # chart + positions
    assert "No standout chart" in html  # exceptional_count == 0 -> the soft note
    assert "Stack" in html and "5/8" in html  # composite strength-stack column + value
    assert "D&middot;P&middot;R" in html and "6&middot;3&middot;8" in html  # graded yogas column


def test_email_renders_multi_day_top_per_day():
    result = {
        "start_date": "2026-06-20", "days": 2, "place_name": "Jetpur", "bar": 90.0,
        "exceptional_count": 1,
        "per_day": [
            {"date": "2026-06-20", "charts": [_chart("03:01", "Aries", 91.0, exceptional=True)]},
            {"date": "2026-06-21", "charts": [_chart("06:00", "Gemini", 72.0)]},
        ],
    }
    html = _render_unshakable_html(result)
    assert "2026-06-20" in html and "2026-06-21" in html  # per-day sections
    assert "genuinely strong" in html  # exceptional summary
    assert "&#9733;" in html  # the star on the exceptional chart
    assert "Planetary Positions" not in html  # multi-day has no positions table


def test_email_renders_big_range_top_overall():
    result = {
        "start_date": "2026-06-01", "days": 30, "place_name": "Jetpur", "bar": 90.0,
        "exceptional_count": 0, "per_day": [],
        "top_overall": [_chart("03:01", "Aries", 76.1), _chart("06:00", "Gemini", 72.0)],
    }
    html = _render_unshakable_html(result)
    assert "Strongest 2 Moments" in html and "30 days" in html
    assert "Aries" in html and ">Date<" in html  # dated table for the big range
    assert "Planetary Positions" not in html
