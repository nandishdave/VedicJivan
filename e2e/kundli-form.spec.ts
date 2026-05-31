import { test, expect } from "@playwright/test";

/**
 * Kundli form E2E flow.
 *
 * The form uses custom date / time / place pickers (not standard <input>s),
 * which makes a full happy-path fill brittle in E2E. We focus on what's
 * cheap and high-signal:
 *
 * 1. Form renders all expected fields.
 * 2. Submit button stays disabled until the bare-minimum inputs are filled.
 * 3. With a mocked API response, submission flows to the success state.
 *
 * The full integration (real birthplace autocomplete + Google Maps lookup +
 * real backend) is exercised manually via /preview during development.
 */

test.describe("Kundli form", () => {
  test("renders all expected form fields", async ({ page }) => {
    await page.goto("/kundli/");
    await expect(page.getByRole("heading", { name: /Free Kundli Report/i })).toBeVisible();
    await expect(page.locator("#name")).toBeVisible();
    await expect(page.locator("#email")).toBeVisible();
    await expect(page.locator("#gender")).toBeVisible();
    await expect(page.getByText(/Date of Birth/i).first()).toBeVisible();
    await expect(page.getByText(/Time of Birth/i).first()).toBeVisible();
    await expect(page.getByText(/Place of Birth/i).first()).toBeVisible();
    await expect(page.getByRole("button", { name: /Generate My Free Kundli/i })).toBeVisible();
  });

  test("submit button is disabled when required fields are empty", async ({ page }) => {
    await page.goto("/kundli/");
    const submit = page.getByRole("button", { name: /Generate My Free Kundli/i });
    await expect(submit).toBeDisabled();

    // Filling only name+email is not enough — DOB / TOB / Place are required.
    await page.fill("#name", "Test User");
    await page.fill("#email", "test@example.com");
    await expect(submit).toBeDisabled();
  });

  test("happy path: mocked API returns 202, success message shown", async ({ page }) => {
    // Intercept the backend call so the test does not actually generate a
    // PDF or send an email.
    await page.route("**/api/kundli/generate", async (route) => {
      await route.fulfill({
        status: 202,
        contentType: "application/json",
        body: JSON.stringify({
          message: "Your Kundli report is being generated and will arrive in your email within a minute.",
        }),
      });
    });

    await page.goto("/kundli/");

    // Drive the form via underlying React state where pickers are custom.
    // Names and email use plain <input>s.
    await page.fill("#name", "E2E Test User");
    await page.selectOption("#gender", "male");
    await page.fill("#email", "e2e@example.com");

    // The submit button stays disabled until DOB/TOB/Place state are set,
    // which requires interacting with the custom pickers. Since those
    // pickers depend on Google Maps (API key + network), driving them
    // headlessly is fragile. Instead, dispatch the form submit directly
    // by force-clicking — the API mock above proves the wire format.
    //
    // For the rare regression that would survive this test (e.g. "validation
    // gate is wrong"), the canSubmit logic itself is unit-tested in vitest.
    await page.evaluate(() => {
      const form = document.querySelector("form");
      form?.requestSubmit();
    });

    // The component shows a success card or toast after a 202 response.
    await expect(page.getByText(/being generated|will arrive in your email/i)).toBeVisible({
      timeout: 15_000,
    });
  });

  test("API failure (5xx) surfaces a user-facing error", async ({ page }) => {
    await page.route("**/api/kundli/generate", async (route) => {
      await route.fulfill({
        status: 500,
        contentType: "application/json",
        body: JSON.stringify({ detail: "Server exploded" }),
      });
    });

    await page.goto("/kundli/");
    await page.fill("#name", "User");
    await page.fill("#email", "u@example.com");
    await page.evaluate(() => {
      const form = document.querySelector("form");
      form?.requestSubmit();
    });

    // The exact copy may vary; we just want SOME error indicator.
    await expect(page.getByText(/error|failed|something went wrong/i)).toBeVisible({
      timeout: 15_000,
    });
  });
});
