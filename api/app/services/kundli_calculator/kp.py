"""KP (Krishnamurti Paddhati) sub-lord system.

KP refines classical Vedic placement with the *sub-lord*: each nakshatra
(13°20' = 800') is divided into nine unequal "subs" whose sizes are
proportional to each planet's Vimshottari dasha years (120-year total),
starting from the nakshatra's own lord and proceeding in the fixed
Vimshottari order. The sub-lord of any longitude is the planet whose sub
that longitude falls in. Going one level deeper inside the sub (same
proportional split) gives the sub-sub-lord (SS).

We compute, for a given sidereal longitude:
  - the sign (RASH), nakshatra + its lord (NAK), the sub-lord (SUB),
    and the sub-sub-lord (SS).

Reuses the project's existing DASHA_SEQUENCE / DASHA_YEARS / NAKSHATRA_*
tables so the KP order always matches the Vimshottari dasha used elsewhere.

NOTE on ayanamsa: classical Astrosage prints "Ayan Type: K.P. New" for this
page (a slightly different ayanamsa than Lahiri). We compute KP sub-lords on
the SAME Lahiri longitudes used by the rest of the report rather than
re-deriving a KP-Newcomb ayanamsa — this keeps the report internally
consistent (the KP table matches our charts). A future refinement could add
the KP ayanamsa offset; logged in the uncertainty notes.
"""

from __future__ import annotations

from ._core import (
    DASHA_SEQUENCE,
    DASHA_YEARS,
    NAKSHATRA_LORDS,
    NAKSHATRA_NAMES,
    SIGN_NAMES,
)

_NAK_SPAN = 360.0 / 27.0      # 13°20' per nakshatra
_TOTAL_DASHA_YEARS = 120.0


def _sub_divisions(start_lord: str) -> list[tuple[str, float]]:
    """Nine (planet, span_in_degrees) subs within one nakshatra, starting at
    `start_lord` and following the Vimshottari order, each sized by the
    planet's dasha-year fraction of the 13°20' nakshatra span."""
    start = DASHA_SEQUENCE.index(start_lord)
    order = [DASHA_SEQUENCE[(start + i) % 9] for i in range(9)]
    return [(p, _NAK_SPAN * DASHA_YEARS[p] / _TOTAL_DASHA_YEARS) for p in order]


def _lord_at(offset_in_nak: float, start_lord: str) -> tuple[str, float, float]:
    """Given an offset into a nakshatra (0.._NAK_SPAN) and the nakshatra lord,
    return (sub_lord, sub_start_offset, sub_span) for the sub it lands in."""
    cursor = 0.0
    for planet, span in _sub_divisions(start_lord):
        if offset_in_nak < cursor + span or planet == DASHA_SEQUENCE[(DASHA_SEQUENCE.index(start_lord) + 8) % 9]:
            return planet, cursor, span
        cursor += span
    # Fallback (floating-point edge at the very end): last sub.
    planet, span = _sub_divisions(start_lord)[-1]
    return planet, _NAK_SPAN - span, span


def kp_sublords(longitude: float) -> dict:
    """Return KP breakdown for a sidereal longitude (degrees, 0..360).

    {
      "sign": str, "sign_index": int,
      "nakshatra": str, "nak_index": int, "nak_lord": str,
      "sub_lord": str, "sub_sub_lord": str,
    }
    """
    lon = longitude % 360.0
    sign_index = int(lon // 30)
    nak_index = int(lon // _NAK_SPAN)
    nak_lord = NAKSHATRA_LORDS[nak_index]
    offset = lon - nak_index * _NAK_SPAN  # 0.._NAK_SPAN within the nakshatra

    sub_lord, sub_start, sub_span = _lord_at(offset, nak_lord)

    # Sub-sub: subdivide the sub itself in the same proportional order,
    # starting from the sub-lord.
    offset_in_sub = offset - sub_start
    frac_in_sub = offset_in_sub / sub_span if sub_span else 0.0
    ss_start = DASHA_SEQUENCE.index(sub_lord)
    ss_order = [DASHA_SEQUENCE[(ss_start + i) % 9] for i in range(9)]
    cursor = 0.0
    sub_sub_lord = ss_order[-1]
    for planet in ss_order:
        frac = DASHA_YEARS[planet] / _TOTAL_DASHA_YEARS
        if frac_in_sub < cursor + frac:
            sub_sub_lord = planet
            break
        cursor += frac

    return {
        "sign": SIGN_NAMES[sign_index],
        "sign_index": sign_index,
        "nakshatra": NAKSHATRA_NAMES[nak_index],
        "nak_index": nak_index,
        "nak_lord": nak_lord,
        "sub_lord": sub_lord,
        "sub_sub_lord": sub_sub_lord,
    }


def placidus_cusps(jd: float, lat: float, lon: float) -> list[float]:
    """Sidereal Placidus house cusps (12 longitudes, cusp 1 = Ascendant), in
    the KP (Krishnamurti) ayanamsa.

    KP differs from our main report in two ways, both honoured here for parity
    with standard KP software (verified 12/12 sub-lords vs Astrosage for the
    reference chart):
      - houses: Placidus (b"P"), not whole-sign;
      - ayanamsa: Krishnamurti (SIDM_KRISHNAMURTI), which sits ~5-6 arcmin from
        Lahiri and shifts cusp degrees / boundary sub-lords accordingly.

    Restores Lahiri afterwards so the rest of the report is unaffected.
    """
    import swisseph as swe

    try:
        swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)
        cusps, _ascmc = swe.houses_ex(jd, lat, lon, b"P", swe.FLG_SIDEREAL)
        return [c % 360.0 for c in cusps[:12]]
    finally:
        # Every other calc in the report assumes Lahiri — never leak KP mode.
        swe.set_sid_mode(swe.SIDM_LAHIRI)


def calc_kp(planets: dict, house_cusps: list[float] | None, lagna_longitude: float,
            moon_longitude: float) -> dict:
    """Build the KP section data.

    - ruling: KP sub-lord breakdown for Lagna and Moon (the "Ruling Planet" box)
    - cusps: per-house-cusp KP breakdown (Cuspal Position table)
    - planets: per-planet KP breakdown (Planetary Positions w/ sub-lords)

    `house_cusps` should be the 12 Placidus cusp longitudes (see
    `placidus_cusps`). If None, falls back to whole-sign cusps (cusp = sign
    start from the lagna) — sub-lords stay classically correct but cusp degrees
    won't match a Placidus KP reference.
    """
    if not house_cusps:
        lagna_sign_start = (int(lagna_longitude // 30)) * 30.0
        house_cusps = [(lagna_sign_start + 30.0 * h) % 360.0 for h in range(12)]

    cusps = []
    for h, cusp_lon in enumerate(house_cusps, start=1):
        kp = kp_sublords(cusp_lon)
        cusps.append({"house": h, "degree": round(cusp_lon % 30, 2), **kp})

    planet_kp = {}
    for name, info in planets.items():
        lon = info.get("longitude")
        if lon is None:
            continue
        planet_kp[name] = {"degree": round(lon % 30, 2), **kp_sublords(lon)}

    return {
        "ruling": {
            "Lagna": kp_sublords(lagna_longitude),
            "Moon": kp_sublords(moon_longitude),
        },
        "cusps": cusps,
        "planets": planet_kp,
    }
