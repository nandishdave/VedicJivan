import { test, expect } from "@playwright/test";

/**
 * Smoke tests — every public page must load and render its key copy.
 *
 * These are the cheapest E2E tests: they catch hard regressions like
 * - 5xx from the static-export pipeline (bad next build)
 * - CloudFront / S3 cache misconfiguration
 * - JS bundle errors that blank the page
 * - CSS bundle missing (page renders but invisible)
 *
 * If a smoke test fails, no other E2E test will succeed — they're the
 * canary in the coal mine.
 */

const PUBLIC_PAGES: Array<{ path: string; expectedHeading: RegExp }> = [
  { path: "/", expectedHeading: /VedicJivan|Vedic|astrolog/i },
  { path: "/services/", expectedHeading: /service/i },
  { path: "/kundli/", expectedHeading: /Free Kundli Report/i },
  { path: "/about/", expectedHeading: /about/i },
  { path: "/contact/", expectedHeading: /contact/i },
  { path: "/blog/", expectedHeading: /blog/i },
  { path: "/courses/", expectedHeading: /course/i },
  { path: "/privacy-policy/", expectedHeading: /privacy/i },
  { path: "/terms/", expectedHeading: /terms/i },
  { path: "/refund-policy/", expectedHeading: /refund/i },
];

for (const { path, expectedHeading } of PUBLIC_PAGES) {
  test(`${path} renders without errors`, async ({ page }) => {
    const errors: string[] = [];
    page.on("pageerror", (err) => errors.push(err.message));
    page.on("console", (msg) => {
      if (msg.type() === "error") errors.push(msg.text());
    });

    const resp = await page.goto(path);
    expect(resp?.status(), `HTTP status for ${path}`).toBeLessThan(400);
    // Page-level heading proves the route resolved to actual content,
    // not just a 200-with-empty-body from a misrouted CDN.
    await expect(page.locator("body")).toContainText(expectedHeading, { timeout: 10_000 });
    // Filter out third-party noise (analytics, adblock-blocked requests).
    const realErrors = errors.filter(
      (e) =>
        !e.includes("Failed to load resource") &&
        !e.includes("googletagmanager") &&
        !e.includes("favicon"),
    );
    expect(realErrors, "Console errors on page").toEqual([]);
  });
}
