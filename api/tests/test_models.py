"""Tests for all Pydantic models — validation, defaults, and enums."""

import pytest
from pydantic import ValidationError

from app.models.availability import AvailableSlot, UnavailabilityCreate
from app.models.booking import (
    BookingCreate,
    BookingInDB,
    BookingStatus,
    BookingStatusUpdate,
)
from app.models.payment import (
    PaymentCreateOrder,
    PaymentInDB,
    PaymentStatus,
    PaymentVerify,
)
from app.models.user import (
    TokenRefresh,
    TokenResponse,
    UserCreate,
    UserInDB,
    UserLogin,
    UserRole,
)


# ═══════════════════════════════════════
# User models
# ═══════════════════════════════════════


def test_user_create_valid():
    u = UserCreate(name="John", email="john@test.com", password="12345678")
    assert u.name == "John"


def test_user_create_name_min_length():
    with pytest.raises(ValidationError):
        UserCreate(name="J", email="a@b.com", password="12345678")


def test_user_create_name_max_length():
    with pytest.raises(ValidationError):
        UserCreate(name="x" * 101, email="a@b.com", password="12345678")


def test_user_create_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(name="John", email="not-an-email", password="12345678")


def test_user_create_password_too_short():
    with pytest.raises(ValidationError):
        UserCreate(name="John", email="a@b.com", password="1234567")


def test_user_create_password_max_length():
    with pytest.raises(ValidationError):
        UserCreate(name="John", email="a@b.com", password="x" * 129)


def test_user_create_phone_default_empty():
    u = UserCreate(name="John", email="a@b.com", password="12345678")
    assert u.phone == ""


def test_user_create_phone_max_length():
    with pytest.raises(ValidationError):
        UserCreate(name="John", email="a@b.com", password="12345678", phone="x" * 21)


def test_user_login_valid():
    u = UserLogin(email="test@test.com", password="pass")
    assert u.email == "test@test.com"


def test_user_login_invalid_email():
    with pytest.raises(ValidationError):
        UserLogin(email="invalid", password="pass")


def test_user_role_enum_values():
    assert UserRole.USER == "user"
    assert UserRole.ADMIN == "admin"


def test_user_in_db_defaults():
    u = UserInDB(name="A", email="a@b.com", password_hash="hash")
    assert u.role == UserRole.USER
    assert u.phone == ""
    assert u.created_at is not None


def test_token_response_default_type():
    t = TokenResponse(access_token="a", refresh_token="b")
    assert t.token_type == "bearer"


def test_token_refresh_valid():
    t = TokenRefresh(refresh_token="tok")
    assert t.refresh_token == "tok"


# ═══════════════════════════════════════
# Booking models
# ═══════════════════════════════════════

_VALID_BOOKING = dict(
    service_slug="call-consultation",
    service_title="Call Consultation",
    date="2026-03-15",
    time_slot="10:00",
    duration_minutes=30,
    user_name="John Doe",
    user_email="john@test.com",
    user_phone="1234567890",
    notes="I need help with my birth chart",
    date_of_birth="1990-05-15",
    time_of_birth="08:30 AM",
    birth_time_unknown=False,
    place_of_birth="Mumbai, India",
    birth_latitude=19.076,
    birth_longitude=72.8777,
)


def test_booking_create_valid():
    b = BookingCreate(**_VALID_BOOKING)
    assert b.service_slug == "call-consultation"


def test_booking_create_date_invalid_format():
    with pytest.raises(ValidationError):
        BookingCreate(**{**_VALID_BOOKING, "date": "2024/01/01"})


def test_booking_create_date_valid_format():
    b = BookingCreate(**{**_VALID_BOOKING, "date": "2024-01-01"})
    assert b.date == "2024-01-01"


def test_booking_create_time_slot_invalid():
    with pytest.raises(ValidationError):
        BookingCreate(**{**_VALID_BOOKING, "time_slot": "9:00"})


def test_booking_create_time_slot_valid():
    b = BookingCreate(**{**_VALID_BOOKING, "time_slot": "09:00"})
    assert b.time_slot == "09:00"


def test_booking_create_duration_too_short():
    with pytest.raises(ValidationError):
        BookingCreate(**{**_VALID_BOOKING, "duration_minutes": 14})


def test_booking_create_duration_too_long():
    with pytest.raises(ValidationError):
        BookingCreate(**{**_VALID_BOOKING, "duration_minutes": 121})


def test_booking_create_duration_boundary_min():
    b = BookingCreate(**{**_VALID_BOOKING, "duration_minutes": 15})
    assert b.duration_minutes == 15


def test_booking_create_duration_boundary_max():
    b = BookingCreate(**{**_VALID_BOOKING, "duration_minutes": 120})
    assert b.duration_minutes == 120


def test_booking_create_user_name_min_length():
    with pytest.raises(ValidationError):
        BookingCreate(**{**_VALID_BOOKING, "user_name": "A"})


def test_booking_create_user_phone_min_length():
    with pytest.raises(ValidationError):
        BookingCreate(**{**_VALID_BOOKING, "user_phone": "123456789"})


def test_booking_create_user_email_invalid():
    with pytest.raises(ValidationError):
        BookingCreate(**{**_VALID_BOOKING, "user_email": "bad"})


def test_booking_create_notes_required():
    data = {**_VALID_BOOKING}
    del data["notes"]
    with pytest.raises(ValidationError):
        BookingCreate(**data)


def test_booking_create_notes_empty_rejected():
    with pytest.raises(ValidationError):
        BookingCreate(**{**_VALID_BOOKING, "notes": ""})


def test_booking_create_dob_invalid_format():
    with pytest.raises(ValidationError):
        BookingCreate(**{**_VALID_BOOKING, "date_of_birth": "15-05-1990"})


def test_booking_create_dob_valid():
    b = BookingCreate(**{**_VALID_BOOKING, "date_of_birth": "1990-05-15"})
    assert b.date_of_birth == "1990-05-15"


def test_booking_create_time_of_birth_valid():
    b = BookingCreate(**{**_VALID_BOOKING, "time_of_birth": "08:30 AM"})
    assert b.time_of_birth == "08:30 AM"


def test_booking_create_time_of_birth_invalid_format():
    with pytest.raises(ValidationError):
        BookingCreate(**{**_VALID_BOOKING, "time_of_birth": "8:30 am"})


def test_booking_create_birth_time_unknown_clears_time():
    b = BookingCreate(
        **{**_VALID_BOOKING, "birth_time_unknown": True, "time_of_birth": "08:30 AM"}
    )
    assert b.time_of_birth is None
    assert b.birth_time_unknown is True


def test_booking_create_requires_time_or_unknown():
    with pytest.raises(ValidationError):
        BookingCreate(
            **{**_VALID_BOOKING, "time_of_birth": None, "birth_time_unknown": False}
        )


def test_booking_create_latitude_out_of_range():
    with pytest.raises(ValidationError):
        BookingCreate(**{**_VALID_BOOKING, "birth_latitude": 91.0})


def test_booking_create_longitude_out_of_range():
    with pytest.raises(ValidationError):
        BookingCreate(**{**_VALID_BOOKING, "birth_longitude": 181.0})


def test_booking_create_place_of_birth_min_length():
    with pytest.raises(ValidationError):
        BookingCreate(**{**_VALID_BOOKING, "place_of_birth": ""})


def test_booking_status_enum_values():
    assert BookingStatus.PENDING == "pending"
    assert BookingStatus.CONFIRMED == "confirmed"
    assert BookingStatus.COMPLETED == "completed"
    assert BookingStatus.CANCELLED == "cancelled"


def test_booking_in_db_defaults():
    b = BookingInDB(
        user_name="A",
        user_email="a@b.com",
        user_phone="1234567890",
        service_slug="x",
        service_title="X",
        date="2026-01-01",
        time_slot="10:00",
        duration_minutes=30,
        price_inr=1999,
    )
    assert b.status == BookingStatus.PENDING
    assert b.payment_id is None
    assert b.notes == ""
    assert b.date_of_birth == ""
    assert b.time_of_birth is None
    assert b.birth_time_unknown is False
    assert b.place_of_birth == ""
    assert b.birth_latitude == 0.0
    assert b.birth_longitude == 0.0


def test_booking_status_update_valid():
    u = BookingStatusUpdate(status=BookingStatus.CONFIRMED)
    assert u.status == BookingStatus.CONFIRMED


# ═══════════════════════════════════════
# Payment models
# ═══════════════════════════════════════


def test_payment_create_order_valid():
    p = PaymentCreateOrder(booking_id="abc", amount_inr=100)
    assert p.amount_inr == 100


def test_payment_create_order_zero_amount():
    with pytest.raises(ValidationError):
        PaymentCreateOrder(booking_id="abc", amount_inr=0)


def test_payment_create_order_negative_amount():
    with pytest.raises(ValidationError):
        PaymentCreateOrder(booking_id="abc", amount_inr=-1)


def test_payment_verify_valid():
    p = PaymentVerify(
        razorpay_order_id="o1",
        razorpay_payment_id="p1",
        razorpay_signature="s1",
        booking_id="b1",
    )
    assert p.razorpay_order_id == "o1"


def test_payment_status_enum_values():
    assert PaymentStatus.CREATED == "created"
    assert PaymentStatus.CAPTURED == "captured"
    assert PaymentStatus.FAILED == "failed"
    assert PaymentStatus.REFUNDED == "refunded"


def test_payment_in_db_defaults():
    p = PaymentInDB(
        booking_id="b1",
        razorpay_order_id="o1",
        amount_inr=1000,
    )
    assert p.status == PaymentStatus.CREATED
    assert p.razorpay_payment_id is None
    assert p.currency == "INR"


# ═══════════════════════════════════════
# Availability models
# ═══════════════════════════════════════


def test_unavailability_create_valid_holiday():
    u = UnavailabilityCreate(date="2024-01-01", is_holiday=True)
    assert u.is_holiday is True


def test_unavailability_create_valid_time_block():
    u = UnavailabilityCreate(date="2024-01-01", start_time="09:00", end_time="17:00")
    assert u.start_time == "09:00"


def test_unavailability_create_date_invalid_format():
    with pytest.raises(ValidationError):
        UnavailabilityCreate(date="01-01-2024")


def test_unavailability_create_start_time_invalid():
    with pytest.raises(ValidationError):
        UnavailabilityCreate(date="2024-01-01", start_time="9:00")


def test_unavailability_create_start_time_optional():
    u = UnavailabilityCreate(date="2024-01-01")
    assert u.start_time is None


def test_unavailability_create_end_time_optional():
    u = UnavailabilityCreate(date="2024-01-01")
    assert u.end_time is None


def test_unavailability_create_is_holiday_default_false():
    u = UnavailabilityCreate(date="2024-01-01")
    assert u.is_holiday is False


def test_unavailability_create_reason_default_empty():
    u = UnavailabilityCreate(date="2024-01-01")
    assert u.reason == ""


def test_available_slot_model():
    s = AvailableSlot(start="09:00", end="09:30")
    assert s.start == "09:00"
    assert s.end == "09:30"
