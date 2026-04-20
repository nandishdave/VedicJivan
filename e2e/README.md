# E2E tests (Playwright)

End-to-end tests that drive a real browser against a deployed environment.
These are the slowest and most expensive tests, but they catch what unit and
integration tests can't: CORS, CSP, Stripe redirects, CDN caching, real Google
Maps autocomplete, real Resend email delivery.

## Setup (one-time)

```bash
npm install
npx playwright install chromium
```

## Running

```bash
# Run all E2E against staging (default)
npm run test:e2e

# Run against a local dev server (start `npm run dev` in another terminal first)
E2E_BASE_URL=http://localhost:3000 npm run test:e2e

# Open the interactive UI runner — best for writing new tests
npm run test:e2e:ui

# Watch the browser (headed mode) instead of running headless
npm run test:e2e:headed

# Run a single spec
npx playwright test smoke.spec.ts

# Show last run's HTML report
npx playwright show-report
```

## Test files

- `smoke.spec.ts` — every public page loads and shows expected copy
- `kundli-form.spec.ts` — Kundli form renders, validates, and reaches success state with mocked API
- `admin-login.spec.ts` — login form renders, rejects bad creds, redirects unauthed users
- `visual.spec.ts` — pixel-diff screenshot regression on a small set of stable pages

## Visual regression

`visual.spec.ts` uses Playwright's `toHaveScreenshot()` to detect unintended
UI changes. Baselines live in `e2e/__screenshots__/visual.spec.ts/`.

```bash
# First run on a new machine (or new screen) — generate baselines
npm run test:e2e -- --update-snapshots

# Subsequent runs — fail on pixel diff > 2%
npm run test:e2e visual.spec.ts

# Review failure diffs (saved as side-by-side PNGs)
ls test-results/
```

**Caveats:**
- Browsers and OS render fonts differently. Don't run baselines on Mac and
  expect them to pass on Linux CI — generate per environment, or run all
  baselines from a single Docker image.
- Currently kept narrow on purpose: only stable marketing pages and form
  empty-states. Don't add screenshots for the Kundli PDF report — it's
  iterating fast and would create constant churn. Use the structural snapshot
  in `api/tests/test_kundli_pdf_golden.py` instead.

## Patterns

- **Mock the backend with `page.route()`** for happy-path flows so tests don't actually
  send emails or write to MongoDB.
- **Use `getByRole` / `getByText` / `getByLabel`** rather than CSS selectors — they're
  resilient to styling changes.
- **Filter console errors** by domain to ignore third-party noise (analytics, adblock).
- **Don't drive the custom date / time / place pickers in E2E**; they depend on
  Google Maps and are tested in vitest component tests instead.

## When E2E flakes

1. Bump per-action timeout in `playwright.config.ts` (`actionTimeout`).
2. Add `retries: 1` for CI.
3. Use `await expect(...).toBeVisible({ timeout: 30_000 })` for known-slow elements.
4. If still flaky, the underlying app is the problem — don't paper over it.
