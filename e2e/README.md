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
