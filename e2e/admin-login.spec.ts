import { test, expect } from "@playwright/test";

/**
 * Admin login E2E flow.
 *
 * The admin dashboard is the operationally most-critical surface: if it
 * breaks, you can't see bookings, mark them complete, or refund payments.
 * These tests exercise the auth boundary without needing real credentials.
 */

test.describe("Admin login", () => {
  test("login page renders form", async ({ page }) => {
    await page.goto("/admin/login/");
    await expect(page.getByRole("heading", { name: /Admin Login/i })).toBeVisible();
    await expect(page.locator("input[type='email']")).toBeVisible();
    await expect(page.locator("input[type='password']")).toBeVisible();
    await expect(page.getByRole("button", { name: /Log[ -]?in|Sign[ -]?in/i })).toBeVisible();
  });

  test("invalid credentials show error", async ({ page }) => {
    // Mock the auth endpoint so we never actually hit the real DB / brute-force gate.
    await page.route("**/api/auth/login", async (route) => {
      await route.fulfill({
        status: 401,
        contentType: "application/json",
        body: JSON.stringify({ detail: "Invalid email or password" }),
      });
    });

    await page.goto("/admin/login/");
    await page.fill("input[type='email']", "wrong@example.com");
    await page.fill("input[type='password']", "wrongpass");
    // The submit control is a styled <Button> with no literal type="submit"
    // attribute (it relies on the HTML default inside a <form>), so a
    // `button[type='submit']` selector never matches. Target it by role/name.
    await page.getByRole("button", { name: /Sign[ -]?in/i }).click();

    await expect(
      page.getByText(/invalid|incorrect|wrong|failed/i),
    ).toBeVisible({ timeout: 10_000 });
  });

  test("unauthenticated visit to /admin/ redirects to login", async ({ page, context }) => {
    // Clear any persisted token first.
    await context.clearCookies();
    await page.goto("/admin/");
    await expect(page).toHaveURL(/\/admin\/login/, { timeout: 10_000 });
  });
});
