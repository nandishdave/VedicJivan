import { defineConfig, devices } from "@playwright/test";

/**
 * Playwright config for VedicJivan E2E tests.
 *
 * Default target is the staging deployment so a developer can run `npm run
 * test:e2e` and immediately get useful signal on the deployed system.
 * Override with E2E_BASE_URL=http://localhost:3000 to test a local dev server.
 *
 * In CI, `webServer` block can be uncommented to spin up `next start` on the
 * production-built app and run E2E against it before deploy.
 */
export default defineConfig({
  testDir: "./e2e",
  // Each test file runs in parallel by default; specs within a file are serial.
  fullyParallel: true,
  // Don't allow .only() to slip into CI runs.
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  // Single worker locally for clearer output; CI benefits from more.
  workers: process.env.CI ? 4 : 2,
  // HTML report viewable with `npx playwright show-report`.
  reporter: process.env.CI ? "github" : [["html", { open: "never" }], ["list"]],

  use: {
    baseURL: process.env.E2E_BASE_URL ?? "https://vedicjivan-test.nandishdave.world",
    // Capture artifacts on failure — invaluable for debugging flaky CI.
    trace: "on-first-retry",
    screenshot: "only-on-failure",
    video: "retain-on-failure",
    // Realistic viewport.
    viewport: { width: 1280, height: 800 },
    // 30s default per action — staging can be slow to cold-start.
    actionTimeout: 30_000,
  },

  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
    // Add Firefox / WebKit / mobile viewports here as needed:
    // { name: "firefox", use: { ...devices["Desktop Firefox"] } },
    // { name: "mobile-chrome", use: { ...devices["Pixel 5"] } },
  ],

  // Uncomment to auto-start a local dev server for tests (slow start-up):
  // webServer: {
  //   command: "npm run dev",
  //   url: "http://localhost:3000",
  //   reuseExistingServer: !process.env.CI,
  //   timeout: 120_000,
  // },
});
