"""Unit tests for the repository-boundary extractions (architecture leak fixes).

Both pieces were previously raw `db.*` access inside a router/use case; now they
are pure and testable without HTTP or a real Mongo:
  - SendBookingReminders  (was raw db in routers/internal.py)
  - MongoAvailabilityRepository.mark_slot_booked  (was raw db in use_cases/payments.py)
"""

from unittest.mock import AsyncMock, MagicMock

from bson import ObjectId

from app.repositories.availability_repository import MongoAvailabilityRepository
from app.use_cases.bookings import SendBookingReminders


def _booking(email: str = "a@b.com") -> dict:
    return {
        "_id": ObjectId(),
        "user_name": "Test",
        "user_email": email,
        "service_title": "Call Consultation",
        "date": "2026-01-02",
        "time_slot": "10:00",
        "duration_minutes": 30,
    }


class _FakeBookingRepo:
    """Minimal fake satisfying the two methods SendBookingReminders calls."""

    def __init__(self, pending: list[dict]) -> None:
        self._pending = pending
        self.marked: list = []

    async def list_pending_reminders(self, booking_date: str) -> list[dict]:
        return self._pending

    async def mark_reminder_sent(self, booking_id) -> int:
        self.marked.append(booking_id)
        return 1


async def test_send_reminders_sends_and_marks_each():
    repo = _FakeBookingRepo([_booking("a@b.com"), _booking("c@d.com")])
    send = AsyncMock()
    sent = await SendBookingReminders(repo, send).execute("2026-01-02")
    assert sent == 2
    assert send.await_count == 2
    assert len(repo.marked) == 2


async def test_send_reminders_skips_failures_without_marking():
    b_ok = _booking("ok@b.com")
    b_bad = _booking("bad@b.com")
    repo = _FakeBookingRepo([b_bad, b_ok])  # first send raises, second succeeds
    send = AsyncMock(side_effect=[Exception("smtp"), None])
    sent = await SendBookingReminders(repo, send).execute("2026-01-02")
    assert sent == 1
    assert repo.marked == [b_ok["_id"]]  # only the successful booking marked


async def test_send_reminders_empty_is_zero():
    repo = _FakeBookingRepo([])
    send = AsyncMock()
    assert await SendBookingReminders(repo, send).execute("2026-01-02") == 0
    send.assert_not_awaited()


async def test_mark_slot_booked_targets_the_day_and_slot():
    coll = MagicMock()
    coll.update_one = AsyncMock(return_value=MagicMock(modified_count=1))
    db = MagicMock()
    db.availability = coll
    n = await MongoAvailabilityRepository(db).mark_slot_booked("2026-01-02", "10:00")
    assert n == 1
    coll.update_one.assert_awaited_once_with(
        {"date": "2026-01-02", "slots.start": "10:00"},
        {"$set": {"slots.$.booked": True}},
    )
