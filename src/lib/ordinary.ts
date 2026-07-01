import data from "@/data/ordinary.json";
import type { ChartData } from "./celebrities";

export interface OrdinaryPerson {
  slug: string;
  name: string;
  sex: string;
  birth: { date: string; time: string; place: string; lat: number; lon: number };
  lagna: string;
  lagna_lord: string;
  nakshatra: string;
  charts: ChartData;
  dasha: { planet: string; start: string; end: string; age_start: number; age_end: number }[];
}

export const ordinary = data as unknown as OrdinaryPerson[];

export function getOrdinary(slug: string): OrdinaryPerson | undefined {
  return ordinary.find((p) => p.slug === slug);
}
