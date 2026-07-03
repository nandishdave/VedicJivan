"""Superstar calibration exp.2 — do D10 (Dasamsa) + dasha-timing separate the
AA/A gold-set from random charts? Clean birth-cert times."""
import statistics as st

from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import _get_dignity
from app.services.kundli_calculator.chart_strength import unshakable_score
from app.services.kundli_calculator.divisional import calc_divisional_charts
from app.services.kundli_calculator.vimshottari import calc_vimshottari_dasha

_C = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
_BEN = {"Jupiter", "Venus", "Mercury"}
_DP = {"Exalted": 100, "Moolatrikona": 85, "Own Sign": 75, "Friendly Sign": 55,
       "Neutral Sign": 45, "Enemy Sign": 25, "Debilitated": 5}

# AA + A gold-set (name, date, local time, lat, lon)
GOLD = [
    ("Obama", "1961-08-04", "19:24", 21.3069, -157.8583), ("Trump", "1946-06-14", "10:54", 40.7020, -73.8060),
    ("JFK", "1917-05-29", "15:00", 42.3318, -71.1212), ("Hitler", "1889-04-20", "18:30", 48.2585, 13.0333),
    ("Churchill", "1874-11-30", "01:30", 51.8517, -1.3520), ("QE2", "1926-04-21", "02:40", 51.5074, -0.1278),
    ("Charles", "1948-11-14", "21:14", 51.5074, -0.1278), ("Diana", "1961-07-01", "19:45", 52.8312, 0.5152),
    ("William", "1982-06-21", "21:03", 51.5074, -0.1278), ("Harry", "1984-09-15", "16:20", 51.5074, -0.1278),
    ("Monroe", "1926-06-01", "09:30", 34.0522, -118.2437), ("Elvis", "1935-01-08", "04:35", 34.2576, -88.7034),
    ("MJackson", "1958-08-29", "23:53", 41.5934, -87.3464), ("Oprah", "1954-01-29", "04:30", 33.0576, -89.5887),
    ("TSwift", "1989-12-13", "05:17", 40.3356, -75.9269), ("Madonna", "1958-08-16", "07:05", 43.5945, -83.8889),
    ("Ali", "1942-01-17", "18:35", 38.2527, -85.7585), ("Einstein", "1879-03-14", "11:30", 48.3984, 9.9916),
    ("Tesla", "1856-07-10", "00:00", 44.5811, 15.3144), ("Gandhi", "1869-10-02", "07:33", 21.6417, 69.6293),
    ("Nehru", "1889-11-14", "23:00", 25.4358, 81.8463), ("Vivekananda", "1863-01-12", "06:33", 22.5726, 88.3639),
    ("Ramanujan", "1887-12-22", "05:45", 11.3410, 77.7172), ("Mandela", "1918-07-18", "14:54", -31.9523, 28.5530),
    ("Lennon", "1940-10-09", "18:30", 53.4084, -2.9916), ("McCartney", "1942-06-18", "14:00", 53.4084, -2.9916),
]
CITIES = [(19.07, 72.87), (28.61, 77.20), (13.08, 80.27), (22.57, 88.36), (12.97, 77.59), (51.51, -0.13), (40.71, -74.0)]


def spike(L):
    v = sorted(L.values(), reverse=True)
    return 0.8 * v[0] + 0.2 * v[1]


def d10_score(chart):
    d10 = calc_divisional_charts(chart["planets"], chart["lagna"])["D10"]
    lag = d10["Lagna"]
    num = den = 0.0
    for p in _C:
        sign = d10[p]
        house = ((sign - lag) % 12) + 1
        dig = _DP.get(_get_dignity(p, sign), 45)
        place = 100 if house in {1, 5, 9} else 80 if house in {4, 7, 10} else 30 if house in {6, 8, 12} else 55
        w = 1.6 if house == 10 else 1.0
        num += (0.5 * dig + 0.5 * place) * w
        den += w
    return num / den


def dasha_score(chart, dob, tob):
    dashas = calc_vimshottari_dasha(chart["planets"]["Moon"]["longitude"], dob, tob)["dashas"]
    by = int(dob[:4])
    sb, lord = chart["shadbala"], chart["lagna"]["sign_lord"]
    acc = tot = 0.0
    for d in dashas:
        a0, a1 = int(d["start_date"][:4]) - by, int(d["end_date"][:4]) - by
        ov = max(0, min(a1, 50) - max(a0, 18))
        if ov <= 0:
            continue
        p = d["planet"]
        s = min(sb.get(p, {}).get("ratio", 1.0) / 1.5, 1.0) * 100
        if p in _BEN:
            s = min(s * 1.15, 100)
        if p == lord:
            s = min(s * 1.15, 100)
        acc += s * ov
        tot += ov
    return acc / tot if tot else 50.0


def signals(dob, tob, lat, lon):
    c = build_muhurta_chart(dob=dob, tob=tob, lat=lat, lon=lon)
    L = unshakable_score(c)["layers"]
    return {"cur": sum(L.values()) / 4, "spike": spike(L), "d10": d10_score(c), "dasha": dasha_score(c, dob, tob)}


fam = [signals(d, t, la, lo) for _, d, t, la, lo in GOLD]
rnd = []
for i in range(60):
    y = 1940 + (i * 7919 % 60); mo = 1 + (i * 13 % 12); d = 1 + (i * 17 % 28)
    la, lo = CITIES[i % len(CITIES)]
    rnd.append(signals(f"{y:04d}-{mo:02d}-{d:02d}", f"{(i*7)%24:02d}:{(i*11)%60:02d}", la, lo))

for key in ("cur", "spike", "d10", "dasha"):
    f = [s[key] for s in fam]
    r = sorted(s[key] for s in rnd)
    rmean, rmax, rp90 = st.mean(r), max(r), r[int(len(r) * 0.9)]
    print(f"{key:6}: famous mean={st.mean(f):5.1f} | random mean={rmean:5.1f} p90={rp90:5.1f} max={rmax:5.1f} "
          f"| fam>rmean {sum(1 for x in f if x>rmean)}/{len(f)}  fam>p90 {sum(1 for x in f if x>rp90)}/{len(f)}")
