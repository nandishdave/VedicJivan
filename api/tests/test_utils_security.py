"""Tests for app.utils.security — password hashing and JWT tokens."""

from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from jose import jwt

from app.config import settings
from app.utils.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)


# ── Password hashing ──


def test_hash_password_returns_bcrypt_hash():
    h = hash_password("mypassword")
    assert h.startswith("$2b$")


def test_hash_password_different_salts():
    h1 = hash_password("same")
    h2 = hash_password("same")
    assert h1 != h2


def test_verify_password_correct():
    h = hash_password("mypassword")
    assert verify_password("mypassword", h) is True


def test_verify_password_incorrect():
    h = hash_password("mypassword")
    assert verify_password("wrong", h) is False


def test_verify_password_empty_string():
    h = hash_password("mypassword")
    assert verify_password("", h) is False


# ── Access tokens ──


def test_create_access_token_returns_string():
    token = create_access_token({"sub": "123"})
    assert isinstance(token, str)


def test_create_access_token_contains_sub_claim():
    token = create_access_token({"sub": "user-42"})
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    assert payload["sub"] == "user-42"


def test_create_access_token_contains_type_access():
    token = create_access_token({"sub": "123"})
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    assert payload["type"] == "access"


def test_create_access_token_has_exp_claim():
    token = create_access_token({"sub": "123"})
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    assert "exp" in payload
    exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    now = datetime.now(timezone.utc)
    # Should expire roughly ACCESS_TOKEN_EXPIRE_MINUTES from now
    assert timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES - 1) < (exp - now) < timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES + 1)


# ── Refresh tokens ──


def test_create_refresh_token_contains_type_refresh():
    token = create_refresh_token({"sub": "123"})
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    assert payload["type"] == "refresh"


def test_create_refresh_token_has_longer_expiry():
    access = create_access_token({"sub": "123"})
    refresh = create_refresh_token({"sub": "123"})
    a_payload = jwt.decode(access, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    r_payload = jwt.decode(refresh, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    assert r_payload["exp"] > a_payload["exp"]


# ── Token decoding ──


def test_decode_token_valid():
    token = create_access_token({"sub": "123"})
    payload = decode_token(token)
    assert payload is not None
    assert payload["sub"] == "123"


def test_decode_token_expired():
    # Create a token already expired
    data = {"sub": "123", "exp": datetime.now(timezone.utc) - timedelta(hours=1), "type": "access"}
    token = jwt.encode(data, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    assert decode_token(token) is None


def test_decode_token_invalid_string():
    assert decode_token("not.a.valid.jwt") is None


def test_decode_token_wrong_secret():
    data = {"sub": "123", "exp": datetime.now(timezone.utc) + timedelta(hours=1), "type": "access"}
    token = jwt.encode(data, "wrong-secret", algorithm=settings.JWT_ALGORITHM)
    assert decode_token(token) is None
