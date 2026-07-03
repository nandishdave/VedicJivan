# -*- coding: utf-8 -*-
"""Probe: KP Placidus cusps + Krishnamurti ayanamsa + sub-lord math. Confirm
cusp indexing and sub-lord assignment before the full run."""
import swisseph as swe
from app.services.kundli_calculator._core import get_julian_day, SIGN_LORDS, SIGN_NAMES
VIM = [("Ketu", 7), ("Venus", 20), ("Sun", 6), ("Moon", 10), ("Mars", 7), ("Rahu", 18), ("Jupiter", 16), ("Saturn", 19), ("Mercury", 17)]
NAK = 360.0 / 27.0
def star_lord(L): return VIM[int(L / NAK) % 9][0]
def sub_lord(L):
    nak = int(L / NAK); off = L - nak * NAK; start = nak % 9; acc = 0.0
    for i in range(9):
        idx = (start + i) % 9; span = VIM[idx][1] / 120.0 * NAK
        if off < acc + span: return VIM[idx][0]
        acc += span
    return VIM[(start + 8) % 9][0]
PL = [("Sun", swe.SUN), ("Moon", swe.MOON), ("Mars", swe.MARS), ("Mercury", swe.MERCURY),
      ("Jupiter", swe.JUPITER), ("Venus", swe.VENUS), ("Saturn", swe.SATURN), ("Rahu", swe.MEAN_NODE)]
def kp_chart(dob, tob, lat, lon):
    jd = get_julian_day(dob, tob, lat, lon)
    swe.set_sid_mode(swe.SIDM_KRISHNAMURTI)
    flags = swe.FLG_SIDEREAL | swe.FLG_SPEED
    cusps, ascmc = swe.houses_ex(jd, lat, lon, b"P", swe.FLG_SIDEREAL)
    planets = {}
    for nm, code in PL:
        res, _ = swe.calc_ut(jd, code, flags); planets[nm] = res[0] % 360
    planets["Ketu"] = (planets["Rahu"] + 180) % 360
    return list(cusps), ascmc, planets
cusps, ascmc, planets = kp_chart("1981-07-23", "10:30", 19.07, 72.87)
print("len(cusps)=", len(cusps), " ascmc[0]=Asc=", round(ascmc[0], 3))
print("cusps:", [round(c, 2) for c in cusps])
# figure out cusp indexing: the 1st cusp should ~= ascendant
for lbl, arr in (("cusps[0..]", cusps),):
    print(f"  {lbl}: c[0]={round(arr[0],2)}  (Asc={round(ascmc[0],2)})")
# 10th cusp: if cusps[0]=1st then 10th = cusps[9]; if cusps[1]=1st then cusps[10]
for tenth in (cusps[9], cusps[10] if len(cusps) > 10 else None):
    if tenth is None: continue
    print(f"  candidate 10th cusp={round(tenth,2)} sign={SIGN_NAMES[int(tenth/30)]} star={star_lord(tenth)} SUB={sub_lord(tenth)}")
# sanity: sub-lord boundaries within a nakshatra sum to full span
print("sub of 0.0:", sub_lord(0.0), "| sub of 13.0:", sub_lord(13.0), "| sub of 359.9:", sub_lord(359.9))
