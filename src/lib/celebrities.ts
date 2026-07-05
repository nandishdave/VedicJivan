// Full celebrity dataset (the heavy ~1 MB import). Only modules that genuinely
// need every field — the detail page (a build-time server component) and
// getCelebrity — should import from here. List pages and client components pull
// helpers/constants from ./chart-people (data-free) and the slim ./list-index
// instead, so they never bundle this file.
import data from "@/data/celebrities.json";
import type { Celebrity } from "./chart-people";

// Re-export the shared, data-free helpers so existing `@/lib/celebrities`
// imports keep working unchanged.
export * from "./chart-people";

export const celebrities = data as unknown as Celebrity[];

export function getCelebrity(slug: string): Celebrity | undefined {
  return celebrities.find((c) => c.slug === slug);
}
