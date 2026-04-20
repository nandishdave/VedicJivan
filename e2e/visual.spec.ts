import { test, expect } from "@playwright/test";

/**
 * Visual regression tests using Playwright's built-in screenshot comparison.
 *
 * How it works
 * ────────────
 * `toHaveScreenshot()` snapshots a baseline PNG on first run, then on every
 * subsequent run compares the rendered page to the baseline pixel-by-pixel
 * with a configurable tolerance. Diffs are saved as side-by-side PNGs in
 * `test-results/`.
 *
 * To accept intentional UI changes:
 *   npm run test:e2e -- --update-snapshots
 *
 * Scope (intentionally narrow)
 * ────────────────────────────
 * We snapshot ONLY pages that are visually stable (homepage hero, services
 * landing, kundli form's empty state). The Kundli PDF report is iterating
 * fast, so it's NOT visually-snapshotted — it has structural snapshots in
 * `api/tests/test_kundli_pdf_golden.py` instead.
 *
 * Mitigations against false positives
 * ───────────────────────────────────
 * - `mask` is used to blacken dynamic regions (timestamps, "current dasha",
 *   user counters, anything that changes per visit) so they don't trigger
 *   pixel diffs.
 * - `animations: "disabled"` freezes any framer-motion intros.
 * - `fullPage: true` captures everything below the fold but slows tests —
 *   use only on key pages.
 * - `maxDiffPixelRatio: 0.01` allows 1% pixel drift — covers font-rendering
 *   variations between OS / Chromium versions.
 */

test.describe("Visual regression", () => {
  test("homepage above the fold", async ({ page }) => {
    await page.goto("/");
    // Wait for the hero to settle (lazy-loaded images, font swap, framer-motion).
    await page.waitForLoadState("networkidle");
    await expect(page).toHaveScreenshot("homepage-hero.png", {
      fullPage: false,                  // viewport only — fast and stable
      animations: "disabled",
      maxDiffPixelRatio: 0.01,
    });
  });

  test("services landing page", async ({ page }) => {
    await page.goto("/services/");
    await page.waitForLoadState("networkidle");
    await expect(page).toHaveScreenshot("services-landing.png", {
      fullPage: true,
      animations: "disabled",
      maxDiffPixelRatio: 0.01,
    });
  });

  test("kundli form empty state", async ({ page }) => {
    await page.goto("/kundli/");
    await page.waitForLoadState("networkidle");
    // The form itself is the focal element; full-page would include footer
    // (which contains social links / dynamic copy).
    const form = page.locator("form").first();
    await expect(form).toHaveScreenshot("kundli-form-empty.png", {
      animations: "disabled",
      maxDiffPixelRatio: 0.01,
    });
  });

  test("admin login form", async ({ page }) => {
    await page.goto("/admin/login/");
    await page.waitForLoadState("networkidle");
    const form = page.locator("form").first();
    await expect(form).toHaveScreenshot("admin-login-form.png", {
      animations: "disabled",
      maxDiffPixelRatio: 0.01,
    });
  });
});
