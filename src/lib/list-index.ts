// Slim gallery indexes for the LIST pages. These import the small, generated
// *-index.json files (see scripts/build-list-index.mjs) — NOT the full
// celebrities.json / ordinary.json — so the list route bundles stay tiny.
import celebIndex from "@/data/celebrities-index.json";
import ordIndex from "@/data/ordinary-index.json";

export interface CelebrityListItem {
  slug: string;
  name: string;
  category: string;
  lagna: string;
}

export interface OrdinaryListItem {
  slug: string;
  name: string;
  sex: string;
  lagna: string;
  date: string;
}

export const celebritiesIndex = celebIndex as CelebrityListItem[];
export const ordinaryIndex = ordIndex as OrdinaryListItem[];
