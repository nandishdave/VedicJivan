"""Superstar calibration — experiment 1: does the CURRENT metric separate real
superstars from random charts? (timezone handled by get_julian_day)."""
import statistics as st

from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator.chart_strength import unshakable_score

# name, date, local-time, lat, lon, reliability  (Modi excluded: DD/disputed)
FAMOUS = [
    ("Tendulkar", "1973-04-24", "04:00", 19.0760, 72.8777, "DD/C"),
    ("Obama", "1961-08-04", "19:24", 21.3069, -157.8583, "AA"),
    ("Ronaldo", "1985-02-05", "10:20", 32.6669, -16.9241, "B/C"),
    ("Messi", "1987-06-24", "07:00", -32.9442, -60.6505, "B/C"),
    ("Federer", "1981-08-08", "08:40", 47.5596, 7.5886, "B"),
    ("Woods", "1975-12-30", "22:50", 33.7701, -118.1937, "A/B"),
    ("Kohli", "1988-11-05", "12:30", 28.6139, 77.2090, "C"),
    ("Dhoni", "1981-07-07", "07:00", 23.3441, 85.3096, "B/C"),
]

CITIES = [(19.07, 72.87), (28.61, 77.20), (13.08, 80.27), (22.57, 88.36), (12.97, 77.59)]

def spike(L):
    """Peak hypothesis: strongest layer + a nudge from the 2nd-strongest, instead
    of averaging everything down."""
    vals = sorted(L.values(), reverse=True)
    return round(0.8 * vals[0] + 0.2 * vals[1], 1)


print("=== Famous (current unshakable metric, actual birth time) ===")
fam = []
fam_spike = []
for name, dob, tob, lat, lon, rel in FAMOUS:
    s = unshakable_score(build_muhurta_chart(dob=dob, tob=tob, lat=lat, lon=lon))
    L = s["layers"]
    fam.append((name, s["score"]))
    fam_spike.append(spike(L))
    print(f"{name:10} {rel:5} score={s['score']:5} spike={spike(L):5}  "
          f"struct={L['structural']:.0f} yoga={L['yoga']:.0f} long={L['longevity']:.0f} fame={L['fame']:.0f}")

# Deterministic 'random' baseline of ordinary charts.
rnd = []
rnd_spike = []
for i in range(60):
    y = 1950 + (i * 7919 % 50)
    mo = 1 + (i * 13 % 12)
    d = 1 + (i * 17 % 28)
    hh = (i * 7) % 24
    mm = (i * 11) % 60
    lat, lon = CITIES[i % len(CITIES)]
    sc = unshakable_score(build_muhurta_chart(
        dob=f"{y:04d}-{mo:02d}-{d:02d}", tob=f"{hh:02d}:{mm:02d}", lat=lat, lon=lon))
    rnd.append(sc["score"])
    rnd_spike.append(spike(sc["layers"]))


def report(label, fam_vals, rnd_vals):
    r = sorted(rnd_vals)
    rmean, rmax, rp90 = st.mean(r), max(r), r[int(len(r) * 0.9)]
    print(f"\n=== {label}: separation ===")
    print(f"famous mean={st.mean(fam_vals):.1f}  |  random mean={rmean:.1f} p90={rp90:.1f} max={rmax:.1f}")
    print(f"famous > random MEAN: {sum(1 for s in fam_vals if s > rmean)}/{len(fam_vals)}  "
          f"> P90: {sum(1 for s in fam_vals if s > rp90)}/{len(fam_vals)}  "
          f"> MAX: {sum(1 for s in fam_vals if s > rmax)}/{len(fam_vals)}")


report("CURRENT (averaged)", [s for _, s in fam], rnd)
report("SPIKE (peak layer)", fam_spike, rnd_spike)
