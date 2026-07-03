"""Test the user's configuration hypotheses vs random base-rate.
Wealth: stellium, 2-11 exchange, 2nd lord + Rahu, 2nd lord in 11, 2/11 conj.
Sports: 6th-lord in Lagna, Lagna-lord (retro) in 6th, debilitated in 6/8."""
import json
from collections import Counter

from app.services.muhurta import build_muhurta_chart
from app.services.kundli_calculator._core import SIGN_LORDS

with open("/app/famous_charts_computed.json", encoding="utf-8") as fh:
    BASE = [(x["name"], x["birth"]["date"], x["birth"]["time"], x["birth"]["lat"], x["birth"]["lon"])
            for x in json.load(fh)]
NEW = [
    ("Hillary Clinton", "1947-10-26", "20:02", 41.85, -87.65), ("Bill Clinton", "1946-08-19", "08:51", 33.67, -93.59),
    ("George W Bush", "1946-07-06", "07:26", 41.31, -72.92), ("Ronald Reagan", "1911-02-06", "02:04", 41.63, -89.79),
    ("Angelina Jolie", "1975-06-04", "09:09", 34.05, -118.24), ("Jim Morrison", "1943-12-08", "11:55", 28.08, -80.61),
    ("Kurt Cobain", "1967-02-20", "19:38", 46.98, -123.82), ("Carl Jung", "1875-07-26", "19:32", 47.60, 9.30),
    ("Sigmund Freud", "1856-05-06", "18:30", 49.64, 18.15), ("Charles Darwin", "1809-02-12", "03:00", 52.71, -2.75),
    ("Jimi Hendrix", "1942-11-27", "10:15", 47.61, -122.33),
]
FAMOUS = BASE + NEW
ATHLETES = {"Roger Federer", "Tiger Woods", "Cristiano Ronaldo", "Lionel Messi", "MS Dhoni",
            "Sachin Tendulkar", "Virat Kohli", "Muhammad Ali"}
BEN = {"Jupiter", "Venus", "Mercury"}


def patterns(dob, tob, lat, lon):
    c = build_muhurta_chart(dob=dob, tob=tob, lat=lat, lon=lon)
    P, lag = c["planets"], c["lagna"]
    ls = lag["sign"]
    def lord(h): return SIGN_LORDS[(ls + h - 1) % 12]
    l1, l2, l6, l11 = lord(1), lord(2), lord(6), lord(11)
    hc = Counter(P[p]["house"] for p in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"))
    maxhouse = max(hc.values())
    # stellium: 3+ planets in one house, and 3+ with >=2 benefics
    stellium = maxhouse >= 3
    stellium_ben = any(sum(1 for b in BEN if P[b]["house"] == h) >= 2 and hc[h] >= 3 for h in hc)
    ex_2_11 = l2 != l11 and SIGN_LORDS[P[l2]["sign"]] == l11 and SIGN_LORDS[P[l11]["sign"]] == l2
    l2_rahu = P[l2]["house"] == P["Rahu"]["house"]
    l2_in_11 = P[l2]["house"] == 11
    l2_l11_conj = l2 != l11 and P[l2]["house"] == P[l11]["house"]
    l2_exalt = P[l2]["dignity"] == "Exalted"
    wealth_2_11 = ex_2_11 or l2_l11_conj or (l2_in_11) or l2_rahu
    # sports / 6th
    l6_in_1 = P[l6]["house"] == 1
    ll_in_6 = P[l1]["house"] == 6
    ll_retro_6 = ll_in_6 and P[l1]["retrograde"]
    debil_6_8 = any(P[p]["dignity"] == "Debilitated" and P[p]["house"] in (6, 8) for p in P)
    sixth_focus = l6_in_1 or ll_in_6 or (hc.get(6, 0) >= 1 and any(P[p]["house"] == 6 for p in ("Mars", "Saturn", "Sun")))
    return {
        "stellium3": stellium, "stellium_2ben": stellium_ben, "ex_2_11": ex_2_11,
        "l2_with_rahu": l2_rahu, "l2_in_11": l2_in_11, "l2_l11_conj": l2_l11_conj,
        "l2_exalted": l2_exalt, "wealth_2_11_any": wealth_2_11,
        "l6_in_lagna": l6_in_1, "lagnalord_in_6": ll_in_6, "lagnalord_retro_6": ll_retro_6,
        "debil_in_6_8": debil_6_8, "sixth_focus": sixth_focus,
    }


fam = {n: patterns(d, t, la, lo) for n, d, t, la, lo in FAMOUS}
CITIES = [(19.07, 72.87), (28.61, 77.20), (51.51, -0.13), (40.71, -74.0), (-33.45, -70.66), (35.68, 139.69)]
rnd = []
for i in range(150):
    yr = 1930 + (i * 7919 % 80); mo = 1 + (i * 13 % 12); d = 1 + (i * 17 % 28)
    la, lo = CITIES[i % len(CITIES)]
    rnd.append(patterns(f"{yr:04d}-{mo:02d}-{d:02d}", f"{(i*7)%24:02d}:{(i*11)%60:02d}", la, lo))

KEYS = list(next(iter(fam.values())).keys())
athl = [v for n, v in fam.items() if n in ATHLETES]
famv = list(fam.values())


def rate(rows, k): return 100 * sum(1 for r in rows if r[k]) / len(rows)


print(f"famous={len(famv)}  random={len(rnd)}  athletes={len(athl)}\n")
print(f"{'pattern':18} {'FAM%':>5} {'RND%':>5} {'lift':>5} {'ATHL%':>6}")
for k in KEYS:
    print(f"{k:18} {rate(famv,k):5.0f} {rate(rnd,k):5.0f} {rate(famv,k)-rate(rnd,k):+5.0f} {rate(athl,k):6.0f}")
# who has the strong wealth 2-11 config
print("\nfamous with 2/11 wealth link:", [n for n, v in fam.items() if v["wealth_2_11_any"]][:15])
print("athletes with 6th focus:", [n for n in ATHLETES if fam.get(n, {}).get("sixth_focus")])
