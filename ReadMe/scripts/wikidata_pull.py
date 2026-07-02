# -*- coding: utf-8 -*-
"""Discover candidate famous charts from Wikidata (CC0 — no licensing worries).

Pulls the most-notable people (by number of Wikipedia sitelinks) per field, with
birth DATE, birth PLACE + coordinates, and occupation, and tags each with our
study domain. Output: a JSON candidate list you can then source birth TIMES for.

    pip install requests
    python wikidata_pull.py            # -> wikidata_candidates.json

IMPORTANT — what this is and isn't:
  * Wikidata birth dates are DAY-precision: it does NOT contain birth times.
    So this is a *discovery list* (who + date + place + field), not chart-ready
    data. Supplement each with a Rodden-rated birth time before adding to a
    chart study.
  * Data is CC0 (public domain). Be a good citizen: descriptive User-Agent +
    modest rate limiting (this script does both). The public endpoint is shared.
"""
from __future__ import annotations

import json
import re
import time
import urllib.parse
import urllib.request

from domain_tags import domain_of  # sibling module

ENDPOINT = "https://query.wikidata.org/sparql"
UA = "VedicJivan-research/1.0 (fame-signal study; contact: nandish.engg2010@gmail.com)"
PER_OCCUPATION = 150   # top-N most-notable per field

# domain -> Wikidata occupation QID (a representative one per field)
OCCUPATIONS = {
    "Cinema":     "Q33999",    # actor
    "Politics":   "Q82955",    # politician
    "Science":    "Q901",      # scientist
    "Music":      "Q639669",   # musician
    "Business":   "Q43845",    # businessperson
    "Sports":     "Q2066131",  # athlete
    "Literature": "Q36180",    # writer
}

_QUERY = """
SELECT ?person ?personLabel ?dob ?placeLabel ?coord ?occLabel (COUNT(DISTINCT ?sl) AS ?fame) WHERE {{
  ?person wdt:P31 wd:Q5 ;
          wdt:P106 wd:{occ} ;
          wdt:P569 ?dob ;
          wdt:P19 ?place .
  ?place wdt:P625 ?coord .
  ?sl schema:about ?person .
  OPTIONAL {{ ?person wdt:P106 ?occ2 . ?occ2 rdfs:label ?occLabel . FILTER(LANG(?occLabel)="en") }}
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
}}
GROUP BY ?person ?personLabel ?dob ?placeLabel ?coord ?occLabel
ORDER BY DESC(?fame)
LIMIT {n}
"""


def _run(sparql: str) -> list[dict]:
    url = ENDPOINT + "?" + urllib.parse.urlencode({"query": sparql, "format": "json"})
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/sparql-results+json"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read())["results"]["bindings"]


def _parse(b: dict, field: str) -> dict | None:
    m = re.match(r"Point\(([-\d.]+) ([-\d.]+)\)", b.get("coord", {}).get("value", ""))
    if not m:
        return None
    lon, lat = float(m.group(1)), float(m.group(2))
    dob = b.get("dob", {}).get("value", "")[:10]           # YYYY-MM-DD (day precision)
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", dob):
        return None
    occ = b.get("occLabel", {}).get("value", field)
    return {
        "name": b.get("personLabel", {}).get("value"),
        "date": dob,
        "place": b.get("placeLabel", {}).get("value"),
        "lat": round(lat, 4), "lon": round(lon, 4),
        "occupation": occ,
        "domain": domain_of(occ) if domain_of(occ) != "Other" else field,
        "sitelinks": int(b.get("fame", {}).get("value", 0)),
        "time": None,   # <-- Wikidata has no birth time; fill from a rated source
    }


def main() -> None:
    seen, out = set(), []
    for field, occ in OCCUPATIONS.items():
        print(f"querying {field} (occ {occ})…")
        try:
            rows = _run(_QUERY.format(occ=occ, n=PER_OCCUPATION))
        except Exception as e:
            print(f"  ! {field} failed: {e}")
            continue
        for b in rows:
            rec = _parse(b, field)
            if rec and rec["name"] and rec["name"] not in seen:
                seen.add(rec["name"]); out.append(rec)
        print(f"  {field}: {len(rows)} rows")
        time.sleep(2)   # be polite to the shared endpoint
    out.sort(key=lambda r: -r["sitelinks"])
    json.dump(out, open("wikidata_candidates.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    from collections import Counter
    print(f"\nwrote wikidata_candidates.json — {len(out)} unique people")
    print("by domain:", dict(Counter(r["domain"] for r in out)))
    print("NOTE: birth TIMES are null — source Rodden-rated times before charting.")


if __name__ == "__main__":
    main()
