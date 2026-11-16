// What the public site shows. Everything switched off here is only hidden:
// its pages, data and backend stay in the repo for future expansion. Each item
// comes back when it works end to end — see TODO.md, "Parked".
export const features = {
  // Course catalogue + detail pages. No enrolment, payment or delivery yet.
  courses: false,
  // Client testimonials. Bring back with real ones, used with permission.
  testimonials: false,
  // Headline figures (consultations, countries, students) and the history /
  // credentials built on them. Bring back with real, defensible numbers.
  stats: false,
};

// Services listed on the site and offered for booking. The full catalogue
// stays defined in src/data/services.ts.
export const PUBLIC_SERVICE_SLUGS = [
  "call-consultation",
  "video-consultation",
  "premium-kundli",
  "matchmaking",
];

// Reachable by direct URL but never listed or indexed — used to exercise the
// payment flow end to end.
export const UNLISTED_SERVICE_SLUGS = ["test-payment"];

export function isPublicService(slug: string): boolean {
  return PUBLIC_SERVICE_SLUGS.includes(slug);
}
