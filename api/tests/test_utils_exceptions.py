"""Tests for app.utils.exceptions — custom HTTP exception classes."""

from fastapi import HTTPException

from app.utils.exceptions import (
    BadRequestError,
    ForbiddenError,
    NotFoundError,
    UnauthorizedError,
)


# ── BadRequestError ──


def test_bad_request_error_status_code():
    assert BadRequestError().status_code == 400


def test_bad_request_error_default_detail():
    assert BadRequestError().detail == "Bad request"


def test_bad_request_error_custom_detail():
    assert BadRequestError("oops").detail == "oops"


# ── UnauthorizedError ──


def test_unauthorized_error_status_code():
    assert UnauthorizedError().status_code == 401


def test_unauthorized_error_default_detail():
    assert UnauthorizedError().detail == "Not authenticated"


def test_unauthorized_error_has_www_authenticate_header():
    err = UnauthorizedError()
    assert err.headers == {"WWW-Authenticate": "Bearer"}


def test_unauthorized_error_custom_detail():
    assert UnauthorizedError("bad token").detail == "bad token"


# ── ForbiddenError ──


def test_forbidden_error_status_code():
    assert ForbiddenError().status_code == 403


def test_forbidden_error_default_detail():
    assert ForbiddenError().detail == "Not authorized"


# ── NotFoundError ──


def test_not_found_error_status_code():
    assert NotFoundError().status_code == 404


def test_not_found_error_default_detail():
    assert NotFoundError().detail == "Not found"


# ── All are HTTPException subclasses ──


def test_all_are_http_exceptions():
    for cls in [BadRequestError, UnauthorizedError, ForbiddenError, NotFoundError]:
        assert issubclass(cls, HTTPException)
