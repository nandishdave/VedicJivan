import { test, expect, type Page } from "@playwright/test";

/**
 * Kundli form E2E flow.
 *
 * The form uses custom date / time / place pickers (not standard <input>s).
 * The date picker is plain <select>s + day buttons (drivable), the time picker
 * has an "unknown" checkbox (sidesteps the time selects), and the place field
 * is a Google-Places autocomplete. We stub the Google Maps Places SDK so the
 * birthplace resolves to fixed lat/lon with no network or live API — letting us
 * drive the form into a genuinely submittable state.
 *
 * NOTE: the deployed build must expose NEXT_PUBLIC_GOOGLE_PLACES_API_KEY
 * (injected by .github/workflows/deploy.yml). Without it the place input is
 * rendered `disabled` and cannot be driven — the stub only replaces the SDK's
 * network layer, not the build-time key gate.
 */

const PLACE_LABEL = "Mumbai, Maharashtra, India";

/**
 * Inject a deterministic Google Maps Places stub before the app's scripts run.
 * Constructors return plain objects (so `new` yields them) to avoid `this`.
 */
async function stubGooglePlaces(page: Page) {
  await page.addInitScript((label: string) => {
    const OK = "OK";
    type Cb = (results: unknown, status: string) => void;
    const places = {
      PlacesServiceStatus: { OK },
      AutocompleteSessionToken: function () {
        return {};
      },
      AutocompleteService: function () {
        return {
          getPlacePredictions: (_req: unknown, cb: Cb) =>
            cb([{ place_id: "stub-place", description: label }], OK),
        };
      },
      PlacesService: function () {
        return {
          getDetails: (_req: unknown, cb: Cb) =>
            cb({ geometry: { location: { lat: () => 19.076, lng: () => 72.8777 } } }, OK),
        };
      },
    };
    (window as unknown as { google: { maps: { places: typeof places } } }).google = {
      maps: { places },
    };
  }, PLACE_LABEL);
}

/** Fill every required field so `canSubmit` becomes true. */
async function fillValidForm(page: Page) {
  await page.fill("#name", "E2E Test User");
  await page.selectOption("#gender", "male");
  await page.fill("#email", "e2e@example.com");

  // Date of birth: pick the year first (clears the future-date guard), then the
  // month, then a day. These selects have no ids, so match them by their option
  // text — only the year select contains "1990", only the month select "January".
  await page.locator('select:has-text("1990")').selectOption("1990");
  await page.locator('select:has-text("January")').selectOption({ label: "June" });
  await page.getByRole("button", { name: "15", exact: true }).click();

  // Time of birth: tick "I don't know my exact birth time" so (tob || tobUnknown).
  await page.getByRole("checkbox").check();

  // Place of birth: type a city, then click the stubbed suggestion → sets lat/lon.
  await page.getByPlaceholder("Start typing a city name...").fill("Mumbai");
  await page.getByText(PLACE_LABEL).click();
}

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

  test("happy path: valid form + mocked 202 shows the success card", async ({ page }) => {
    // Intercept the backend call so the test does not generate a PDF / send email.
    await page.route("**/api/kundli/generate", async (route) => {
      await route.fulfill({
        status: 202,
        contentType: "application/json",
        body: JSON.stringify({ message: "Your Kundli report is being generated." }),
      });
    });

    await stubGooglePlaces(page);
    await page.goto("/kundli/");
    await fillValidForm(page);

    const submit = page.getByRole("button", { name: /Generate My Free Kundli/i });
    await expect(submit).toBeEnabled();
    await submit.click();

    // The component swaps to its own static success view (it does NOT echo the
    // API message), so assert on that heading rather than the response body.
    await expect(
      page.getByRole("heading", { name: /Your Kundli is on its way/i }),
    ).toBeVisible({ timeout: 15_000 });
  });

  test("API failure surfaces the server error message to the user", async ({ page }) => {
    await page.route("**/api/kundli/generate", async (route) => {
      await route.fulfill({
        status: 500,
        contentType: "application/json",
        body: JSON.stringify({ detail: "Server error, please try again later." }),
      });
    });

    await stubGooglePlaces(page);
    await page.goto("/kundli/");
    await fillValidForm(page);

    await page.getByRole("button", { name: /Generate My Free Kundli/i }).click();

    // apiRequest throws Error(detail); the page renders {error} verbatim in the
    // red alert box — assert the exact server message reaches the UI.
    await expect(
      page.getByText("Server error, please try again later."),
    ).toBeVisible({ timeout: 15_000 });
  });
});
