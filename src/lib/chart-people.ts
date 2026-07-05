// Data-free chart helpers, constants, and types shared by the celebrity and
// ordinary galleries. Deliberately imports NO JSON: anything that pulls in the
// 1 MB `celebrities.json` / `ordinary.json` belongs in celebrities.ts /
// ordinary.ts. Client components (NorthIndianChart) and the list pages import
// from HERE so their bundles never reference the heavy data files.

export interface D1Planet {
  sign: string;
  house: number;
  deg: number;
  dignity: string;
  retro: boolean;
}

export interface Celebrity {
  slug: string;
  name: string;
  category: string;
  rating: string;
  birth: { date: string; time: string; place: string; lat: number; lon: number };
  bio: string;
  lagna: string;
  lagna_lord: string;
  nakshatra: string;
  charts: {
    D1: Record<string, D1Planet>;
    D2: Record<string, string>;
    D4: Record<string, string>;
    D9: Record<string, string>;
    D10: Record<string, string>;
    D11: Record<string, string>;
    D16: Record<string, string>;
    D24: Record<string, string>;
    D60: Record<string, string>;
  };
  dasha: { planet: string; start: string; end: string; age_start: number; age_end: number }[];
}

const SIGNS = [
  "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
  "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
];
const idx = (s: string) => SIGNS.indexOf(s);

const TITLES = new Set(["Queen", "King", "Prince", "Princess", "Sir", "Dr", "Dame", "Lord"]);
const ROMAN = new Set(["II", "III", "IV", "V", "Jr", "Sr"]);

/** The A–Z index letter: surname, ignoring titles + regnal numerals. */
export function indexLetter(name: string): string {
  const words = name.split(" ").filter((w) => !TITLES.has(w));
  while (words.length && ROMAN.has(words[words.length - 1])) words.pop();
  return (words[words.length - 1] || name)[0].toUpperCase();
}

export const PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"];
export const ABBR: Record<string, string> = {
  Sun: "Su", Moon: "Mo", Mars: "Ma", Mercury: "Me", Jupiter: "Ju",
  Venus: "Ve", Saturn: "Sa", Rahu: "Ra", Ketu: "Ke",
};
export const PLANET_COLOR: Record<string, string> = {
  Sun: "#d97706", Moon: "#475569", Mars: "#dc2626", Mercury: "#16a34a", Jupiter: "#ca8a04",
  Venus: "#db2777", Saturn: "#1e3a8a", Rahu: "#6d28d9", Ketu: "#6d28d9",
};

export interface HouseData {
  houses: Record<number, string[]>;
  signByHouse: Record<number, number>;
}

/** Turn a varga chart into house→planets + house→sign-number for rendering. */
export type VargaKey = "D1" | "D2" | "D4" | "D9" | "D10" | "D11" | "D16" | "D24" | "D60";
export type ChartData = Celebrity["charts"];

/** Works for any person with a `charts` + `lagna` (celebrity or ordinary). */
export function chartHouses(person: { charts: ChartData; lagna: string }, type: VargaKey): HouseData {
  const houses: Record<number, string[]> = {};
  const signByHouse: Record<number, number> = {};
  let lagnaIdx: number;

  if (type === "D1") {
    lagnaIdx = idx(person.lagna);
    for (const p of PLANETS) {
      const h = person.charts.D1[p].house;
      (houses[h] ||= []).push(p);
    }
  } else {
    const ch = person.charts[type];
    lagnaIdx = idx(ch.Lagna);
    for (const p of PLANETS) {
      const h = ((idx(ch[p]) - lagnaIdx + 12) % 12) + 1;
      (houses[h] ||= []).push(p);
    }
  }
  for (let h = 1; h <= 12; h++) signByHouse[h] = ((lagnaIdx + h - 1) % 12) + 1;
  return { houses, signByHouse };
}
