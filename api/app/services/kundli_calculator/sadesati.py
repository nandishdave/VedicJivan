"""Sade Sati — Saturn's 7.5-year transit through 12th/1st/2nd from Moon.

Walks Saturn's sidereal ingress dates with Swiss Ephemeris and
collapses retrograde back-and-forth into a single final ingress per
sign. The output lists every Sade Sati period the native experiences
in their lifetime (search window: 100 years from birth).
"""

from __future__ import annotations

from datetime import date, timedelta

from ._core import SIGN_NAMES
from .vimshottari import _add_years


def _compute_saturn_transits(start_year: int, end_year: int) -> list[tuple[int, date]]:
    """Sidereal Saturn ingress dates between two years using Swiss Ephemeris.

    Walks 14-day steps detecting sign changes, then binary-refines each
    candidate to the exact ingress day. Includes retrograde re-entries —
    callers can collapse those with `_collapse_retrograde_transits`.
    """
    import swisseph as swe

    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags = swe.FLG_SIDEREAL

    def saturn_sign(d: date) -> int:
        jd = swe.julday(d.year, d.month, d.day, 12.0)
        pos, _ = swe.calc_ut(jd, swe.SATURN, flags)
        return int(pos[0] % 360 / 30)

    cursor = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    current_sign = saturn_sign(cursor)
    transits: list[tuple[int, date]] = [(current_sign, cursor)]

    while cursor < end:
        nxt = min(cursor + timedelta(days=14), end)
        nxt_sign = saturn_sign(nxt)
        if nxt_sign != current_sign:
            lo, hi = cursor, nxt
            while (hi - lo).days > 1:
                mid = lo + timedelta(days=(hi - lo).days // 2)
                if saturn_sign(mid) == current_sign:
                    lo = mid
                else:
                    hi = mid
            transits.append((nxt_sign, hi))
            current_sign = nxt_sign
        cursor = nxt

    return transits


def _collapse_retrograde_transits(transits: list[tuple[int, date]]) -> list[tuple[int, date]]:
    """Collapse retrograde back-and-forth into a single final ingress per sign.

    A typical retrograde pattern is A → previous_sign → A again within a few
    months. Keep only the LAST ingress into A — that's the "permanent" entry.
    """
    if not transits:
        return []
    result: list[tuple[int, date]] = [transits[0]]
    for sign, d in transits[1:]:
        if len(result) >= 2 and result[-2][0] == sign and (d - result[-1][1]).days < 365:
            result.pop()
            result[-1] = (sign, d)
        else:
            result.append((sign, d))
    return result


def calc_sadesati(moon_sign: int, dob: str | None = None) -> list[dict]:
    """
    Calculate Saturn's Sade Sati periods.

    Sade Sati = Saturn transiting the 12th, 1st, and 2nd houses from the
    Moon sign (~7.5 years total per cycle, recurring every ~30 years).
    When `dob` is supplied, periods that ended before birth are dropped and
    the search window covers ~100 years from the birth year, so all three
    Sade Satis a person can experience in a normal lifespan are returned.
    """
    birth_date = date.fromisoformat(dob) if dob else None
    if birth_date:
        start_year = birth_date.year
        end_year = birth_date.year + 100
    else:
        start_year = date.today().year - 30
        end_year = date.today().year + 70

    transits = _collapse_retrograde_transits(
        _compute_saturn_transits(start_year, end_year)
    )

    sadesati_signs = {
        (moon_sign - 1) % 12: "Rising",
        moon_sign: "Peak",
        (moon_sign + 1) % 12: "Setting",
    }

    periods = []
    for i, (sign, entry) in enumerate(transits):
        if sign not in sadesati_signs:
            continue
        if i + 1 < len(transits):
            exit_date = transits[i + 1][1]
        else:
            exit_date = _add_years(entry, 2.46)
        if birth_date and exit_date < birth_date:
            continue
        periods.append({
            "phase": sadesati_signs[sign],
            "rashi": SIGN_NAMES[sign],
            "start_date": entry.isoformat(),
            "end_date": exit_date.isoformat(),
        })

    return sorted(periods, key=lambda p: p["start_date"])
