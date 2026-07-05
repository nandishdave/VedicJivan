// Build-time generator for the slim list-page indexes.
//
// The gallery LIST pages (/celebrities, /ordinary) render only ~4 fields per
// row, but importing the full celebrities.json (~1 MB) / ordinary.json (~435 KB)
// shipped every field — charts, dashas, bios — to the browser just to draw a
// list. This script projects each record down to the handful of fields the list
// actually uses and writes a physically separate JSON, so the list route bundle
// references the slim file instead of the heavy one.
//
// Wired as an npm `prebuild` hook (see package.json) → runs automatically before
// every `next build`, so the slim indexes can never drift from the source data.
// Committed to the repo as well so local dev / vitest work without a build.
//
// Run manually:  node scripts/build-list-index.mjs
import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const dataDir = join(root, "src", "data");

const read = (name) => JSON.parse(readFileSync(join(dataDir, name), "utf8"));
const write = (name, rows) => {
  writeFileSync(join(dataDir, name), JSON.stringify(rows) + "\n");
  return rows.length;
};

// Celebrity list row: name + category + lagna (+ slug for the link).
const celebs = read("celebrities.json").map((c) => ({
  slug: c.slug,
  name: c.name,
  category: c.category,
  lagna: c.lagna,
}));

// Ordinary list row: name + sex + lagna + birth date (+ slug for the link).
const ordinary = read("ordinary.json").map((p) => ({
  slug: p.slug,
  name: p.name,
  sex: p.sex,
  lagna: p.lagna,
  date: p.birth?.date ?? "",
}));

const nc = write("celebrities-index.json", celebs);
const no = write("ordinary-index.json", ordinary);
console.log(`Wrote slim indexes: celebrities-index.json (${nc}), ordinary-index.json (${no}).`);
