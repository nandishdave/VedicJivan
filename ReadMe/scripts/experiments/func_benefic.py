"""Recompute 'benefics in kendra/trikona' using FUNCTIONAL benefics (per lagna),
not natural benefics. AA famous vs random."""
import numpy as np
from app.services.muhurta import build_muhurta_chart

# lagna sign index -> functional benefics
CAMP_A = {9, 10, 6, 1, 2, 5}  # Cap, Aqu, Lib, Tau, Gem, Vir -> Sat/Ven/Mer
FB_A = {"Saturn", "Venus", "Mercury"}
FB_B = {"Sun", "Moon", "Mars", "Jupiter"}  # Ari, Can, Leo, Sco, Sag, Pis
KT = {1, 4, 5, 7, 9, 10}

AA = [
    ("1961-08-04","19:24",21.3069,-157.8583),("1946-06-14","10:54",40.7020,-73.8060),
    ("1917-05-29","15:00",42.3318,-71.1212),("1947-10-26","20:02",41.85,-87.65),
    ("1946-08-19","08:51",33.67,-93.59),("1946-07-06","07:26",41.31,-72.92),
    ("1911-02-06","02:04",41.63,-89.79),("1889-04-20","18:30",48.2585,13.0333),
    ("1874-11-30","01:30",51.8517,-1.3520),("1926-04-21","02:40",51.5074,-0.1278),
    ("1948-11-14","21:14",51.5074,-0.1278),("1961-07-01","19:45",52.8312,0.5152),
    ("1982-06-21","21:03",51.5074,-0.1278),("1984-09-15","16:20",51.5074,-0.1278),
    ("1926-06-01","09:30",34.0522,-118.2437),("1935-01-08","04:35",34.2576,-88.7034),
    ("1958-08-29","23:53",41.5934,-87.3464),("1958-08-16","07:05",43.5945,-83.8889),
    ("1954-01-29","04:30",33.0576,-89.5887),("1989-12-13","05:17",40.3356,-75.9269),
    ("1975-06-04","09:09",34.05,-118.24),("1943-12-08","11:55",28.08,-80.61),
    ("1967-02-20","19:38",46.98,-123.82),("1879-03-14","11:30",48.3984,9.9916),
    ("1875-07-26","19:32",47.60,9.30),("1856-05-06","18:30",49.64,18.15),
    ("1809-02-12","03:00",52.71,-2.75),("1856-07-10","00:00",44.5811,15.3144),
    ("1942-01-17","18:35",38.2527,-85.7585),("1940-10-09","18:30",53.4084,-2.9916),
    ("1942-06-18","14:00",53.4084,-2.9916),("1942-11-27","10:15",47.61,-122.33),
]


def stats(dob, tob, lat, lon):
    c = build_muhurta_chart(dob=dob, tob=tob, lat=lat, lon=lon, with_shadbala=False)
    P, ls = c["planets"], c["lagna"]["sign"]
    fb = FB_A if ls in CAMP_A else FB_B
    n = sum(1 for p in fb if P[p]["house"] in KT)
    return n, n / len(fb)  # count, fraction of func-benefics in kendra/trikona


F = np.array([stats(*r) for r in AA], float)
CITIES = [(19.07,72.87),(28.61,77.20),(51.51,-0.13),(40.71,-74.0),(-33.45,-70.66),(35.68,139.69)]
R = np.array([stats(f"{1930+(i*7919%80):04d}-{1+(i*13%12):02d}-{1+(i*17%28):02d}",
                    f"{(i*7)%24:02d}:{(i*11)%60:02d}", *CITIES[i % 6]) for i in range(150)], float)

print(f"AA famous={len(F)}  random={len(R)}")
print(f"FUNCTIONAL benefics in kendra/trikona:")
print(f"  count:    famous={F[:,0].mean():.2f}  random={R[:,0].mean():.2f}  lift={F[:,0].mean()-R[:,0].mean():+.2f}")
print(f"  fraction: famous={F[:,1].mean():.2f}  random={R[:,1].mean():.2f}  lift={F[:,1].mean()-R[:,1].mean():+.2f}")
