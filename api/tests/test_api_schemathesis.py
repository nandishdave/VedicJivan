"""Schemathesis fuzz tests against the FastAPI OpenAPI schema.

Schemathesis reads the live `/openapi.json` and auto-generates valid +
boundary + malformed requests for every documented endpoint. Two failure
classes that hand-written tests rarely catch:

  1. **5xx crashes** — the server should NEVER 500 on a request that matches
     the documented schema. A 500 means an unhandled exception leaked out
     of FastAPI; this is always a bug.

  2. **Schema drift** — actual response body doesn't match the documented
     `response_model`. Catches forgotten Pydantic field renames, None where
     Optional wasn't declared, etc.

This module hits the running API container at SCHEMATHESIS_BASE_URL
(default `http://localhost:8000`), NOT a mocked ASGI app. Why?

  - ASGI mode + the function-scoped `mock_db` fixture deadlocks under
    Hypothesis iteration. Reproducible but not worth the fight.
  - Real HTTP against the live container exercises the full middleware
    stack including auth deps and CORS — closer to production behaviour.
  - The container already has a real MongoDB connection, so requests don't
    hang on DB timeouts.

The trade-off: this test module is **skipped** unless the API is reachable.
Run via:
    docker compose up -d                 # bring up api + mongo
    pytest tests/test_api_schemathesis.py

Reference: https://schemathesis.readthedocs.io/
"""

from __future__ import annotations

import os

import pytest

# Skip the whole module if schemathesis isn't installed.
schemathesis = pytest.importorskip("schemathesis")

import requests
from hypothesis import HealthCheck, settings


BASE_URL = os.environ.get("SCHEMATHESIS_BASE_URL", "http://localhost:8000")


# Skip entire module if the API isn't reachable — keeps CI happy when only
# unit tests are running and avoids 1080 connection-refused errors.
def _api_reachable() -> bool:
    try:
        r = requests.get(f"{BASE_URL}/api/health", timeout=2)
        return r.status_code == 200
    except Exception:
        return False


pytestmark = pytest.mark.skipif(
    not _api_reachable(),
    reason=f"API not reachable at {BASE_URL} — skipping fuzz tests",
)


# Endpoints we don't want Schemathesis to actually call:
#   - Stripe webhook + create-checkout-session would talk to live Stripe
#   - Kundli generate / preview would render PDFs / send emails
EXCLUDED_PATHS = (
    "/api/payments/webhook",
    "/api/payments/create-checkout-session",
    "/api/kundli/generate",
    "/api/kundli/preview",
)


# Schemathesis 3.x doesn't fully support OpenAPI 3.1; fetch and downgrade.
def _fetch_openapi_30():
    r = requests.get(f"{BASE_URL}/openapi.json", timeout=10)
    spec = r.json()
    spec["openapi"] = "3.0.3"
    return spec


schema = schemathesis.from_dict(_fetch_openapi_30(), base_url=BASE_URL)


def _excluded(case) -> bool:
    return any(case.path.startswith(p) for p in EXCLUDED_PATHS)


@schema.parametrize()
@settings(
    max_examples=5,                     # 5 per endpoint × ~30 = ~150 cases
    deadline=None,                      # tolerate slow first-request startup
    suppress_health_check=[
        HealthCheck.too_slow,
        HealthCheck.filter_too_much,
        HealthCheck.function_scoped_fixture,
    ],
)
def test_no_endpoint_returns_5xx(case):
    """For every documented endpoint × N random inputs: never 500.

    A 5xx means an unhandled exception escaped FastAPI — it's always a bug,
    even if the request itself was nonsense (the framework should turn it
    into a 422 / 400, never crash).
    """
    if _excluded(case):
        pytest.skip(f"{case.path} reaches external systems — excluded from fuzz")
    response = case.call()
    assert response.status_code < 500, (
        f"5xx from {case.method} {case.path} with input "
        f"body={case.body!r} query={case.query!r} path_params={case.path_parameters!r}\n"
        f"Response: {response.text[:500]}"
    )


@schema.parametrize()
@settings(
    max_examples=3,                     # 3 per endpoint × ~30 = ~90 cases
    deadline=None,
    suppress_health_check=[
        HealthCheck.too_slow,
        HealthCheck.filter_too_much,
        HealthCheck.function_scoped_fixture,
    ],
)
def test_response_matches_documented_schema(case):
    """For every endpoint: actual 2xx response body conforms to the schema.

    Catches schema drift — a Pydantic response_model field rename that
    forgot to propagate to the OpenAPI export.
    """
    if _excluded(case):
        pytest.skip(f"{case.path} reaches external systems — excluded from fuzz")
    response = case.call()
    if 200 <= response.status_code < 300:
        case.validate_response(response)
