"""Seed catalogue + back-compat helpers for service pricing.

`DEFAULT_SERVICES` is the canonical baseline — it's used to seed the
`services` Mongo collection on first boot and exists so that pricing
tests have a single source of truth that isn't tied to network state.

`SERVICE_PRICES` / `SERVICE_PRICES_EUR` / `get_price` are kept as
back-compat helpers so existing tests that import these names from
`app.routers.bookings` (which re-exports them) continue to work after
the Phase 4 cut-over to a DB-backed pricing flow.

At runtime, `CreateBooking` no longer calls `get_price` — it goes through
`GetServicePrice` (which hits the repository). This module is the seed +
test-baseline only.
"""

from __future__ import annotations

from app.domain.exceptions import BookingValidationError
from app.models.service import Service, ServiceDuration
from app.utils.exceptions import BadRequestError


# Single source of truth for the default catalogue.
DEFAULT_SERVICES: list[Service] = [
    Service(
        slug="call-consultation",
        durations=[
            ServiceDuration(duration_minutes=30, price_inr=1999, price_eur=29),
            ServiceDuration(duration_minutes=45, price_inr=2499, price_eur=35),
            ServiceDuration(duration_minutes=60, price_inr=2999, price_eur=39),
        ],
    ),
    Service(
        slug="video-consultation",
        durations=[
            ServiceDuration(duration_minutes=30, price_inr=2499, price_eur=35),
            ServiceDuration(duration_minutes=45, price_inr=2999, price_eur=39),
            ServiceDuration(duration_minutes=60, price_inr=3999, price_eur=49),
        ],
    ),
    Service(
        slug="premium-kundli",
        durations=[
            ServiceDuration(duration_minutes=0, price_inr=4999, price_eur=59),
        ],
    ),
    Service(
        slug="numerology-report",
        durations=[
            ServiceDuration(duration_minutes=0, price_inr=1499, price_eur=19),
        ],
    ),
    Service(
        slug="vastu-consultation",
        durations=[
            ServiceDuration(duration_minutes=30, price_inr=2499, price_eur=35),
            ServiceDuration(duration_minutes=45, price_inr=2999, price_eur=39),
            ServiceDuration(duration_minutes=60, price_inr=3499, price_eur=45),
        ],
    ),
    Service(
        slug="matchmaking",
        durations=[
            ServiceDuration(duration_minutes=0, price_inr=2499, price_eur=35),
        ],
    ),
    Service(
        slug="astrological-consulting",
        durations=[
            ServiceDuration(duration_minutes=30, price_inr=2499, price_eur=35),
            ServiceDuration(duration_minutes=45, price_inr=2999, price_eur=39),
            ServiceDuration(duration_minutes=60, price_inr=3499, price_eur=45),
        ],
    ),
    Service(
        slug="personal-growth-coaching",
        durations=[
            ServiceDuration(duration_minutes=30, price_inr=3499, price_eur=45),
            ServiceDuration(duration_minutes=45, price_inr=3999, price_eur=52),
            ServiceDuration(duration_minutes=60, price_inr=4999, price_eur=59),
        ],
    ),
    Service(
        slug="therapeutic-healing",
        durations=[
            ServiceDuration(duration_minutes=45, price_inr=4499, price_eur=52),
            ServiceDuration(duration_minutes=60, price_inr=4999, price_eur=59),
            ServiceDuration(duration_minutes=75, price_inr=5999, price_eur=69),
        ],
    ),
    Service(
        slug="test-payment",
        durations=[
            ServiceDuration(duration_minutes=30, price_inr=100, price_eur=1),
        ],
    ),
]


# Convenience views derived from DEFAULT_SERVICES.
SERVICE_PRICES: dict[str, dict[str, int]] = {
    s.slug: {str(d.duration_minutes): d.price_inr for d in s.durations}
    for s in DEFAULT_SERVICES
}

SERVICE_PRICES_EUR: dict[str, dict[str, int]] = {
    s.slug: {str(d.duration_minutes): d.price_eur for d in s.durations}
    for s in DEFAULT_SERVICES
}


def resolve_price(service: Service, duration_minutes: int) -> tuple[int, int]:
    """Return (inr, eur) for a duration; falls back to the report `0` slot
    if the exact duration isn't sold.

    Pure — no DB, no HTTP. Raises the domain `BookingValidationError` on no
    match so use cases can call it without catching an HTTP exception. The
    router's DomainError handler maps that to a 400.
    """
    by_duration = {d.duration_minutes: d for d in service.durations}
    if duration_minutes in by_duration:
        d = by_duration[duration_minutes]
        return d.price_inr, d.price_eur
    if 0 in by_duration:
        d = by_duration[0]
        return d.price_inr, d.price_eur
    available = ", ".join(
        f"{d.duration_minutes} min" for d in service.durations if d.duration_minutes != 0
    )
    raise BookingValidationError(
        f"Duration {duration_minutes} min not available for this service. "
        f"Options: {available}"
    )


def price_from_service(
    service: Service, duration_minutes: int
) -> tuple[int, int]:
    """Sync/HTTP-facing wrapper around `resolve_price`.

    Kept for the back-compat `get_price` path (and its tests), which expect a
    400-mapped `BadRequestError`. Production use cases call `resolve_price`
    directly and let the domain exception propagate.
    """
    try:
        return resolve_price(service, duration_minutes)
    except BookingValidationError as e:
        raise BadRequestError(str(e))


def get_price(service_slug: str, duration_minutes: int) -> tuple[int, int]:
    """Sync price lookup against the in-code defaults.

    Used by tests + as a back-compat shim. Production goes through
    `GetServicePrice` (DB-backed) instead.
    """
    by_slug = {s.slug: s for s in DEFAULT_SERVICES}
    service = by_slug.get(service_slug)
    if not service:
        raise BadRequestError(f"Unknown service: {service_slug}")
    return price_from_service(service, duration_minutes)
