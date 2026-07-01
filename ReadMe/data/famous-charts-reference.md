# Famous Charts — Calibration Reference (gold-set)

High-reliability birth data for validating/calibrating chart-strength metrics
(esp. the Superstar-grade finder). **AA** = birth certificate / official record.
**A** = autobiography / family records (very reliable). Coordinates added for
direct use with `build_muhurta_chart(dob, tob, lat, lon)` (timezone is derived
from lat/lon by `get_julian_day` via timezonefinder + ZoneInfo).

> ⚠️ **LMT caveat:** pre-~1910 births recorded in *Local Mean Time* (LMT) — e.g.
> Einstein, Tesla, Gandhi, Nehru, Vivekananda, Ramanujan, Hitler, Churchill —
> may be off by the LMT↔standard-zone gap (lon/15h vs the zone offset, up to
> ~30 min), which can shift the Lagna. Treat those as ~±0.5h until LMT handling
> is added. Modern charts with standard-zone times are exact.

## AA-Rated (birth certificate / official record)

### Political leaders
| Person | Date | Place | lat, lon | Time (local) |
|---|---|---|---|---|
| Barack Obama | 1961-08-04 | Honolulu, HI | 21.3069, -157.8583 | 19:24 HST |
| Donald Trump | 1946-06-14 | Jamaica, NY | 40.7020, -73.8060 | 10:54 EDT |
| John F. Kennedy | 1917-05-29 | Brookline, MA | 42.3318, -71.1212 | 15:00 EST |
| Adolf Hitler | 1889-04-20 | Braunau am Inn, AT | 48.2585, 13.0333 | 18:30 LMT |
| Winston Churchill | 1874-11-30 | Woodstock, England | 51.8517, -1.3520 | 01:30 GMT |

### British royals
| Person | Date | Place | lat, lon | Time (local) |
|---|---|---|---|---|
| Queen Elizabeth II | 1926-04-21 | London | 51.5074, -0.1278 | 02:40 BST |
| King Charles III | 1948-11-14 | London | 51.5074, -0.1278 | 21:14 GMT |
| Princess Diana | 1961-07-01 | Sandringham, England | 52.8312, 0.5152 | 19:45 BST |
| Prince William | 1982-06-21 | London | 51.5074, -0.1278 | 21:03 BST |
| Prince Harry | 1984-09-15 | London | 51.5074, -0.1278 | 16:20 BST |

### Entertainment / music
| Person | Date | Place | lat, lon | Time (local) |
|---|---|---|---|---|
| Marilyn Monroe | 1926-06-01 | Los Angeles, CA | 34.0522, -118.2437 | 09:30 PST |
| Elvis Presley | 1935-01-08 | Tupelo, MS | 34.2576, -88.7034 | 04:35 CST |
| Michael Jackson | 1958-08-29 | Gary, IN | 41.5934, -87.3464 | 23:53 CST |
| Oprah Winfrey | 1954-01-29 | Kosciusko, MS | 33.0576, -89.5887 | 04:30 CST |
| Taylor Swift | 1989-12-13 | Reading, PA | 40.3356, -75.9269 | 05:17 EST |
| Madonna | 1958-08-16 | Bay City, MI | 43.5945, -83.8889 | 07:05 EST |

### Sports
| Person | Date | Place | lat, lon | Time (local) |
|---|---|---|---|---|
| Muhammad Ali | 1942-01-17 | Louisville, KY | 38.2527, -85.7585 | 18:35 CST |

### Science / philosophy
| Person | Date | Place | lat, lon | Time (local) |
|---|---|---|---|---|
| Albert Einstein | 1879-03-14 | Ulm, Germany | 48.3984, 9.9916 | 11:30 LMT |
| Nikola Tesla | 1856-07-10 | Smiljan, Croatia | 44.5811, 15.3144 | 00:00 LMT |

## A-Rated (autobiography / family records)
| Person | Date | Place | lat, lon | Time (local) |
|---|---|---|---|---|
| Mahatma Gandhi | 1869-10-02 | Porbandar, GJ | 21.6417, 69.6293 | 07:33 LMT |
| Jawaharlal Nehru | 1889-11-14 | Allahabad, UP | 25.4358, 81.8463 | 23:00 LMT |
| Swami Vivekananda | 1863-01-12 | Calcutta | 22.5726, 88.3639 | 06:33 LMT |
| Srinivasa Ramanujan | 1887-12-22 | Erode, TN | 11.3410, 77.7172 | 05:45 LMT |
| Nelson Mandela | 1918-07-18 | Mvezo, South Africa | -31.9523, 28.5530 | 14:54 SAST |
| John Lennon | 1940-10-09 | Liverpool, England | 53.4084, -2.9916 | 18:30 BST |
| Paul McCartney | 1942-06-18 | Liverpool, England | 53.4084, -2.9916 | 14:00 BST |

## Lower-reliability (B/C/DD — use with caution, noisy times)
| Person | Date | Place | lat, lon | Time (local) | Rating |
|---|---|---|---|---|---|
| Roger Federer | 1981-08-08 | Basel, CH | 47.5596, 7.5886 | 08:40 | B |
| Tiger Woods | 1975-12-30 | Long Beach, CA | 33.7701, -118.1937 | 22:50 PST | A/B |
| Cristiano Ronaldo | 1985-02-05 | Funchal, Madeira | 32.6669, -16.9241 | 10:20 | B/C |
| Lionel Messi | 1987-06-24 | Rosario, AR | -32.9442, -60.6505 | 07:00 | B/C |
| MS Dhoni | 1981-07-07 | Ranchi, JH | 23.3441, 85.3096 | 07:00 | B/C |
| Sachin Tendulkar | 1973-04-24 | Mumbai, MH | 19.0760, 72.8777 | 04:00 | DD/C |
| Virat Kohli | 1988-11-05 | Delhi | 28.6139, 77.2090 | 12:30 | C |
| Narendra Modi | 1950-09-17 | Vadnagar, GJ | 23.7900, 72.6400 | disputed | DD (skip) |

## Calibration findings so far (2026-06-30)
- **Current composite metric does NOT separate superstars from random** — on the
  B/C set, famous mean 62.1 < random mean 64.0; 0/8 beat random max.
- **Spike (peak-layer) also fails** — famous 79.9 ≈ random 80.1; random max 96.3
  beat every superstar (ordinary charts also spike high on *some* layer).
- Untested hypotheses: **D10 (Dasamsa)** and **dasha-timing**. Re-run pending
  with this AA/A gold-set (cleaner times → less noise).
