# -*- coding: utf-8 -*-
"""Do DISCARDED rules revive on accurate-time (AA/A) charts? Each discarded rule's
solo-AUC across ALL/AA/AA+A/B+C/C. Look for a MONOTONIC lift with time quality
(the signature of a real-but-time-smeared rule). Numerology = zero-time-sensitivity
control (should stay flat). CAVEAT: AA~Western vs C~Indian (geography confound),
n_AA=48 (noisy)."""
import json, numpy as np, swisseph as swe
from collections import Counter
from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import get_julian_day, SIGN_LORDS, _get_dignity
from app.services.kundli_calculator.jaimini import calc_jaimini_karakas
FAM = json.load(open("/app/src_celebrities.json", encoding="utf-8")); ORDD = json.load(open("/app/normal_people.json", encoding="utf-8"))
_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]; _ALL = _C + ["Rahu", "Ketu"]
_DIGN = {"Exalted", "Moolatrikona", "Own Sign"}
MOV = {0, 3, 6, 9}; FIX = {1, 4, 7, 10}; DUAL = {2, 5, 8, 11}
VIM = [("Ketu", 7), ("Venus", 20), ("Sun", 6), ("Moon", 10), ("Mars", 7), ("Rahu", 18), ("Jupiter", 16), ("Saturn", 19), ("Mercury", 17)]
NAK = 360.0 / 27.0; PLC = [("Sun", swe.SUN), ("Moon", swe.MOON), ("Mars", swe.MARS), ("Mercury", swe.MERCURY), ("Jupiter", swe.JUPITER), ("Venus", swe.VENUS), ("Saturn", swe.SATURN), ("Rahu", swe.MEAN_NODE)]
NUMP = {1: "Sun", 2: "Moon", 3: "Jupiter", 4: "Rahu", 5: "Mercury", 6: "Venus", 7: "Ketu", 8: "Saturn", 9: "Mars"}
MALEFIC_YOGA = {0, 5, 8, 9, 12, 14, 16, 18, 26}; SUCCESS = {2, 6, 10, 11}; NAME = {1, 10, 11}; PLSET = {1, 2, 3, 5, 10}
def rd_aspects(s):
    if s in MOV: return FIX - {(s + 1) % 12}
    if s in FIX: return MOV - {(s - 1) % 12}
    return DUAL - {s}
def connected(sa, sb): return (sa == sb) or (sb in rd_aspects(sa))
def star_lord(L): return VIM[int(L / NAK) % 9][0]
def sub_lord(L):
    nak = int(L / NAK); off = L - nak * NAK; start = nak % 9; acc = 0.0
    for i in range(9):
        idx = (start + i) % 9; span = VIM[idx][1] / 120.0 * NAK
        if off < acc + span: return VIM[idx][0]
        acc += span
    return VIM[(start + 8) % 9][0]
def dsum(n):
    n = int(n)
    while n > 9: n = sum(int(c) for c in str(n))
    return n
def kp_sig(dob, tob, lat, lon):
    jd = get_julian_day(dob, tob, lat, lon); swe.set_sid_mode(swe.SIDM_KRISHNAMURTI); flags = swe.FLG_SIDEREAL | swe.FLG_SPEED
    cusps, _ = swe.houses_ex(jd, lat, lon, b"P", swe.FLG_SIDEREAL); cusps = list(cusps)
    plon = {}
    for nm, code in PLC:
        res, _ = swe.calc_ut(jd, code, flags); plon[nm] = res[0] % 360
    plon["Ketu"] = (plon["Rahu"] + 180) % 360
    def house_of(L):
        for h in range(12):
            if (L - cusps[h]) % 360 < (cusps[(h + 1) % 12] - cusps[h]) % 360: return h + 1
        return 12
    occ = {p: house_of(plon[p]) for p in _ALL}; owned = {p: set() for p in _ALL}
    for h in range(12):
        lord = SIGN_LORDS[int(cusps[h] / 30)]
        if lord in owned: owned[lord].add(h + 1)
    def sig(planet):
        sl = star_lord(plon[planet]); hs = {occ[sl]} | owned[sl] | {occ[planet]} | owned[planet]
        if planet in ("Rahu", "Ketu"):
            sd = SIGN_LORDS[int(plon[planet] / 30)]; hs |= {occ[sd]} | owned[sd]
        return hs
    return cusps, sig
def feats(p):
    b = p["birth"]; c = build_muhurta_chart(dob=b["date"], tob=b["time"], lat=b["lat"], lon=b["lon"], with_shadbala=False)
    P, lag = c["planets"], c["lagna"]; ls = lag["sign"]
    slon, mlon = P["Sun"]["longitude"], P["Moon"]["longitude"]; elong = (mlon - slon) % 360
    bright = 72 <= elong <= 264
    # Panchanga
    yoga = int(((slon + mlon) % 360) / (360 / 27)); nitya_benefic = 0.0 if yoga in MALEFIC_YOGA else 1.0
    tithi = int(elong / 12) + 1; tg = (tithi - 1) % 5
    # Jaimini karaka
    kar = calc_jaimini_karakas(P, lag); chara = kar["chara"]; kk = kar["karakamsa_sign"]; ak = kar["atmakaraka"]
    ks = {r: P[chara[r]["planet"]]["sign"] for r in chara}
    ak_amk = 1.0 if connected(ks["Atma"], ks["Amatya"]) else 0.0
    raja3 = float(connected(ks["Atma"], ks["Amatya"]) + connected(ks["Atma"], ks["Putra"]) + connected(ks["Amatya"], ks["Putra"]))
    ben = {"Jupiter", "Venus", "Mercury"} | ({"Moon"} if bright else set())
    hfrom = lambda s: ((s - kk) % 12) + 1
    kk_trik_ben = float(sum(1 for q in _C if q in ben and hfrom(P[q]["sign"]) in {1, 5, 9}))
    ak_dig = 1.0 if _get_dignity(ak, P[ak]["sign"]) in _DIGN else 0.0
    # Numerology (date-based -> time-invariant control)
    date = b["date"]; mool = dsum(int(date[8:10])); bhag = dsum(sum(int(ch) for ch in date if ch.isdigit()))
    numer_place = float((P[NUMP[mool]]["house"] in PLSET) + (P[NUMP[bhag]]["house"] in PLSET))
    # KP
    cusps, sig = kp_sig(b["date"], b["time"], b["lat"], b["lon"])
    kp_1st = 1.0 if sig(sub_lord(cusps[0])) & NAME else 0.0
    kp_10th = 1.0 if sig(sub_lord(cusps[9])) & SUCCESS else 0.0
    kp_cnt = float(sum(1 for ci in (0, 1, 9, 10) if sig(sub_lord(cusps[ci])) & (NAME if ci == 0 else SUCCESS)))
    return {"kp_1st_name": kp_1st, "kp_10th": kp_10th, "kp_count": kp_cnt, "ak_amk": ak_amk, "raja3": raja3,
            "kk_trik_ben": kk_trik_ben, "ak_dig": ak_dig, "nitya_benefic": nitya_benefic,
            "tithi_nanda": float(tg == 0), "numer_place": numer_place}
def rating(p):
    r = str(p.get("rating", "")).strip().upper(); return r if r in ("AA", "A", "B", "C") else "?"
FR = [(feats(p), rating(p)) for p in FAM]; RR = [feats(p) for p in ORDD]
RT = np.array([x[1] for x in FR])
print(f"famous={len(FR)} ordinary={len(RR)}  ratings={dict(Counter(RT))}")
KEYS = ["kp_1st_name", "kp_10th", "kp_count", "ak_amk", "raja3", "kk_trik_ben", "ak_dig", "nitya_benefic", "tithi_nanda", "numer_place"]
def auc(fa, ra): return float(np.mean([np.mean(x > ra) + 0.5 * np.mean(x == ra) for x in fa]))
def rr(k): return np.array([r[k] for r in RR], float)
SUBS = [("ALL", np.ones(len(FR), bool)), ("AA", RT == "AA"), ("AA+A", np.isin(RT, ["AA", "A"])), ("B+C", np.isin(RT, ["B", "C"])), ("C", RT == "C")]
print("\nsolo-AUC per subset (raw; <0.5 = ordinary-leaning). Look for MONOTONIC lift C->AA:")
print(f"  {'rule':14} " + "  ".join(f"{nm:>6}" for nm, _ in SUBS))
for k in KEYS:
    Rf = rr(k); row = []
    for nm, m in SUBS:
        Ff = np.array([r[0][k] for r, keep in zip(FR, m) if keep], float)
        row.append(f"{auc(Ff, Rf):.3f}" if m.sum() >= 15 else "  -  ")
    print(f"  {k:14} " + "  ".join(f"{v:>6}" for v in row))
