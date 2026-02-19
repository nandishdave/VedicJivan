"""Tests for app.config — Settings loading and defaults."""

import os

from app.config import Settings


def test_settings_default_values():
    s = Settings(JWT_SECRET="test")
    assert s.APP_ENV == "development"
    assert s.JWT_ALGORITHM == "HS256"
    assert s.ACCESS_TOKEN_EXPIRE_MINUTES == 15
    assert s.REFRESH_TOKEN_EXPIRE_DAYS == 7


def test_settings_razorpay_defaults_empty(monkeypatch):
    monkeypatch.delenv("RAZORPAY_KEY_ID", raising=False)
    monkeypatch.delenv("RAZORPAY_KEY_SECRET", raising=False)
    s = Settings(JWT_SECRET="test", _env_file=None)
    assert s.RAZORPAY_KEY_ID == ""
    assert s.RAZORPAY_KEY_SECRET == ""


def test_settings_email_defaults(monkeypatch):
    monkeypatch.delenv("ADMIN_EMAIL", raising=False)
    s = Settings(JWT_SECRET="test", _env_file=None)
    assert s.EMAIL_FROM == "noreply@vedicjivan.com"
    assert s.ADMIN_EMAIL == "vedic.jivan33@gmail.com"


def test_settings_frontend_url_default():
    s = Settings(JWT_SECRET="test")
    assert s.FRONTEND_URL == "http://localhost:3000"


def test_settings_overridden_by_constructor():
    s = Settings(JWT_SECRET="custom", APP_ENV="production", ACCESS_TOKEN_EXPIRE_MINUTES=60)
    assert s.APP_ENV == "production"
    assert s.ACCESS_TOKEN_EXPIRE_MINUTES == 60
