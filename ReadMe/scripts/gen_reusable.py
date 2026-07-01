"""Emit copy-paste-friendly reusable birth data (JSON + MD) for all ordinary charts."""
import json
with open("/app/normal_people.json", encoding="utf-8") as fh:
    data = json.load(fh)
rows = []
for p in data:
    b = p["birth"]
    rows.append({
        "name": p["name"], "sex": p["sex"], "date": b["date"], "time": b["time"],
        "place": b["place"], "lat": b["lat"], "lon": b["lon"],
        "lagna": p["lagna"], "lagna_lord": p["lagna_lord"], "nakshatra": p["nakshatra"],
    })
with open("/app/ordinary_birth_data.json", "w", encoding="utf-8") as fh:
    json.dump(rows, fh, indent=2, ensure_ascii=False)
lines = ["| # | Name | Sex | Date | Time | Place | Lat | Lon | Lagna | Lord | Nakshatra |",
         "|--:|------|-----|------|------|-------|----:|----:|-------|------|-----------|"]
for i, r in enumerate(rows, 1):
    lines.append(f"| {i} | {r['name']} | {r['sex']} | {r['date']} | {r['time']} | "
                 f"{r['place']} | {r['lat']} | {r['lon']} | {r['lagna']} | {r['lagna_lord']} | {r['nakshatra']} |")
with open("/app/ordinary_birth_data.md", "w", encoding="utf-8") as fh:
    fh.write(f"# Ordinary Charts — Birth Data ({len(rows)} people)\n\n"
             "Raw birth inputs + computed Lagna/Nakshatra. Full D1–D60 charts + dasha are in "
             "`src/data/ordinary.json`.\n\n" + "\n".join(lines) + "\n")
print(f"wrote {len(rows)} rows -> ordinary_birth_data.json / .md")
