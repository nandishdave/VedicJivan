"""Functional benefics = the 3 trikona lords (1st/5th/9th). Test whether their
sambandha (conjunction | aspect | exchange) is over-represented in famous charts.
This is the classical trikona-lord raja yoga (e.g. Einstein: Ve+Me+Sa in 10th)."""
import json

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


def sambandha(a, b, P, asp):
    if a == b:
        return True
    ha, hb = P[a]["house"], P[b]["house"]
    if ha == hb:
        return True
    if hb in asp.get(a, []) or ha in asp.get(b, []):
        return True
    if SIGN_LORDS[P[a]["sign"]] == b and SIGN_LORDS[P[b]["sign"]] == a:
        return True
    return False


def metrics(dob, tob, lat, lon):
    c = build_muhurta_chart(dob=dob, tob=tob, lat=lat, lon=lon)
    P, lag = c["planets"], c["lagna"]
    asp = c["graha_drishti"]["planet_aspects"]
    ls = lag["sign"]
    fb = list({SIGN_LORDS[(ls + h - 1) % 12] for h in (1, 5, 9)})  # trikona lords
    pairs = [(fb[i], fb[j]) for i in range(len(fb)) for j in range(i + 1, len(fb))]
    conn = [(a, b) for a, b in pairs if sambandha(a, b, P, asp)]
    # union-find cluster
    par = {p: p for p in fb}

    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    for a, b in conn:
        par[f(a)] = f(b)
    sizes = {}
    for p in fb:
        sizes[f(p)] = sizes.get(f(p), 0) + 1
    cluster = max(sizes.values())
    all_conj = len({P[p]["house"] for p in fb}) == 1  # Einstein-style: all in one house
    all_conn = cluster == len(fb)  # all trikona lords in one connected web
    any_two = len(conn) >= 1
    exch = any(SIGN_LORDS[P[a]["sign"]] == b and SIGN_LORDS[P[b]["sign"]] == a for a, b in pairs)
    return {"n_unique": len(fb), "all_conjunct": all_conj, "all_connected": all_conn,
            "two_plus_connected": any_two, "exchange": exch, "cluster": cluster}


fam = {n: metrics(d, t, la, lo) for n, d, t, la, lo in FAMOUS}
CITIES = [(19.07, 72.87), (28.61, 77.20), (51.51, -0.13), (40.71, -74.0), (-33.45, -70.66), (35.68, 139.69)]
rnd = []
for i in range(160):
    yr = 1930 + (i * 7919 % 80); mo = 1 + (i * 13 % 12); d = 1 + (i * 17 % 28)
    la, lo = CITIES[i % len(CITIES)]
    rnd.append(metrics(f"{yr:04d}-{mo:02d}-{d:02d}", f"{(i*7)%24:02d}:{(i*11)%60:02d}", la, lo))

famv = list(fam.values())
BOOL = ["all_conjunct", "all_connected", "two_plus_connected", "exchange"]


def rate(rows, k): return 100 * sum(1 for r in rows if r[k]) / len(rows)


print(f"famous={len(famv)}  random={len(rnd)}")
print(f"avg cluster: fam={sum(r['cluster'] for r in famv)/len(famv):.2f} rnd={sum(r['cluster'] for r in rnd)/len(rnd):.2f}")
print(f"\n{'pattern':20} {'FAM%':>5} {'RND%':>5} {'lift':>5}")
for k in BOOL:
    print(f"{k:20} {rate(famv,k):5.0f} {rate(rnd,k):5.0f} {rate(famv,k)-rate(rnd,k):+5.0f}")
print("\nfamous with ALL 3 trikona lords CONNECTED:", [n for n, v in fam.items() if v["all_connected"]])
print("\nfamous with ALL 3 CONJUNCT (Einstein-style):", [n for n, v in fam.items() if v["all_conjunct"]])
