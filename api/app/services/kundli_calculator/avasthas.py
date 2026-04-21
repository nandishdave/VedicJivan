"""Avasthas — per-planet state classification (Baladi + Jagradadi + Deeptadi).

Three distinct classical schemes:
  - Baladi  (5 states) — by degree within sign, directional by sign parity.
  - Jagradadi (3 states) — by sign-lord friendship with friendship-precedence.
  - Deeptadi (9 states) — full priority-ordered classification combining
    dignity, combustion, planetary war, malefic affliction and Shadbala.

`_calc_baladi` and `_calc_jagradadi` are re-exported via `_core` and
the package `__init__.py` because tests import them directly.
"""

from __future__ import annotations

from ._core import _MIN_SHADBALA, _PLANET_ENEMIES, _PLANET_FRIENDS, SIGN_LORDS


_BALADI_NAMES = ["Bala", "Kumar", "Yuva", "Vradha", "Mrat"]

# Deeptadi Avastha — proper 9-state classification. Multiple criteria are
# checked in priority order; first match wins. See _calc_deeptadi.
_DEEPTADI_MALEFICS = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}
# Combustion thresholds (degrees from Sun) per classical convention.
_DEEPTADI_COMBUST = {
    "Moon": 12, "Mars": 17, "Mercury": 14,
    "Jupiter": 11, "Venus": 10, "Saturn": 15,
}


# Jagradadi Avastha — 3-state classification by sign-lord relationship.
# Only an *enemy* lord drives the planet to Susupta. A friend or neutral lord
# overrides debilitation (so e.g. Moon in Scorpio — Mars's sign, neutral to
# Moon — is Swapna rather than Susupta even though Moon is debilitated there).
#   Own sign / Exalted / Moolatrikona  → Jagrat (awake)
#   Sign lord is friend or neutral     → Swapna (dreaming)
#   Sign lord is enemy                 → Susupta (sleeping)
def _calc_jagradadi(planet: str, sign_zero_indexed: int, dignity: str) -> str:
    if dignity in ("Exalted", "Moolatrikona", "Own Sign"):
        return "Jagrat"
    sign_lord = SIGN_LORDS[sign_zero_indexed]
    if sign_lord in _PLANET_ENEMIES.get(planet, set()):
        return "Susupta"
    return "Swapna"


def _angular_distance(a: float, b: float) -> float:
    """Smallest angular distance between two longitudes (0–180°)."""
    return abs(((a - b + 180) % 360) - 180)


def _is_combust(planet: str, planets: dict) -> bool:
    if planet == "Sun" or planet not in _DEEPTADI_COMBUST:
        return False
    sun = planets.get("Sun")
    p = planets.get(planet)
    if not sun or not p:
        return False
    return _angular_distance(p["longitude"], sun["longitude"]) < _DEEPTADI_COMBUST[planet]


def _is_in_planetary_war(planet: str, planets: dict) -> bool:
    """Two non-luminary planets within 1° in the same sign — both at war."""
    if planet in ("Sun", "Moon", "Rahu", "Ketu", "Uranus", "Neptune", "Pluto"):
        return False
    p = planets.get(planet)
    if not p:
        return False
    for other_name, other in planets.items():
        if other_name == planet:
            continue
        if other_name in ("Sun", "Moon", "Rahu", "Ketu", "Uranus", "Neptune", "Pluto"):
            continue
        if other["sign"] != p["sign"]:
            continue
        if abs(other["longitude"] - p["longitude"]) < 1.0:
            return True
    return False


def _is_pidita(planet: str, planets: dict, graha_drishti: dict | None) -> bool:
    """Planet afflicted by malefic conjunction or aspect."""
    if not graha_drishti:
        return False
    p = planets.get(planet)
    if not p:
        return False
    # Conjunction with malefic in same sign
    for malefic in _DEEPTADI_MALEFICS:
        if malefic == planet or malefic not in planets:
            continue
        if planets[malefic]["sign"] == p["sign"]:
            return True
    # Aspect from malefic (lookup which planets aspect the planet's house)
    house_aspected_by = graha_drishti.get("house_aspected_by", {})
    aspectors = house_aspected_by.get(str(p["house"]), [])
    return any(a in _DEEPTADI_MALEFICS and a != planet for a in aspectors)


def _is_shakta(planet: str, planets: dict, shadbala: dict | None) -> bool:
    """Planet has 'capable' strength: retrograde OR Shadbala above min threshold."""
    p = planets.get(planet)
    if p and p.get("retrograde"):
        return True
    if shadbala and planet in shadbala:
        rupas = shadbala[planet].get("shadbala_rupas", 0)
        min_req = _MIN_SHADBALA.get(planet, 0)
        if rupas >= min_req:
            return True
    return False


def _calc_deeptadi(
    planet: str,
    planets: dict,
    dignity: str,
    graha_drishti: dict | None,
    shadbala: dict | None,
) -> str:
    """Compute Deeptadi avastha — first match wins in priority order:
    Vikala → Khala → Deena → Deepta → Swastha → Mudita → Shakta → Pidita → Shanta.

    Sign-dignity states (Deepta/Swastha/Mudita) take precedence over Shakta:
    a friend-sign or own-sign placement is the more meaningful description
    even if the planet also happens to be retrograde or have high Shadbala.
    Shakta becomes a fallback for "strong but not specially dignified".

    Friendship takes precedence over debilitation: if the sign lord is a
    friend, the planet is Mudita even when technically debilitated, rather
    than being demoted to Deena.
    """
    if _is_combust(planet, planets):
        return "Vikala"
    if _is_in_planetary_war(planet, planets):
        return "Khala"

    sign_zero_indexed = planets[planet]["sign"]
    sign_lord = SIGN_LORDS[sign_zero_indexed]
    is_friend_sign = sign_lord in _PLANET_FRIENDS.get(planet, set())

    if dignity == "Enemy Sign" or (dignity == "Debilitated" and not is_friend_sign):
        return "Deena"
    if dignity == "Exalted":
        return "Deepta"
    if dignity in ("Own Sign", "Moolatrikona"):
        return "Swastha"
    if dignity == "Friendly Sign" or is_friend_sign:
        return "Mudita"
    if _is_shakta(planet, planets, shadbala):
        return "Shakta"
    if _is_pidita(planet, planets, graha_drishti):
        return "Pidita"
    return "Shanta"


def _calc_baladi(sign_zero_indexed: int, degree_in_sign: float) -> str:
    """Baladi (5-state) Avastha by degree-within-sign.

    Odd 1-indexed signs (Aries, Gemini, Leo, Libra, Sag, Aqu): Bala→Mrat
    ascending. Even 1-indexed signs: reversed (Mrat→Bala). Each zone is 6°.
    """
    is_odd = (sign_zero_indexed + 1) % 2 == 1
    zone = min(int(degree_in_sign / 6), 4)
    return _BALADI_NAMES[zone] if is_odd else _BALADI_NAMES[4 - zone]


def calc_avasthas(
    planets: dict,
    graha_drishti: dict | None = None,
    shadbala: dict | None = None,
) -> list[dict]:
    """Per-planet Avastha states for the 7 classical planets.

    Returns a list of {planet, jagradadi, baladi, deeptadi}.
      - Baladi: exact 5-state degree-zone calculation (matches Astrosage).
      - Jagradadi: 3-state classification with friendship-precedence rule
        (only enemy lord drives Susupta).
      - Deeptadi: full 9-state classification combining sign dignity,
        combustion, planetary war, malefic affliction and Shadbala strength.
        Pass `graha_drishti` (for malefic-aspect Pidita check) and `shadbala`
        (for Shakta strength check) to enable the full state set; without them
        the function falls back to dignity-only and skips Pidita/Shakta.
    """
    classical = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    out = []
    for name in classical:
        info = planets.get(name)
        if not info:
            continue
        dignity = info.get("dignity", "")
        out.append({
            "planet": name,
            "jagradadi": _calc_jagradadi(name, info["sign"], dignity),
            "baladi":    _calc_baladi(info["sign"], info["degree_in_sign"]),
            "deeptadi":  _calc_deeptadi(name, planets, dignity, graha_drishti, shadbala),
        })
    return out
