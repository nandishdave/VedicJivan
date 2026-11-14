# VedicJivan — TODO

Working list of what to do next. Drafted 2026-11-14 from a review of the full
commit history, the docs and the code layout. Tick items off here as they land.

## Where things stand

- `staging` is 162 commits ahead of `main`; the last merge to `main` was 2026-06-07.
  Birth Muhurta, the Unshakable finder, the celebrity/ordinary galleries, all
  calculators and the July security fixes are not in production yet.
- Last feature commit before this file: 2026-07-08 (Kundli Matching calculator).
- Fame model: 18 factors, CV-AUC about 0.775 — see `ReadMe/experiment-ledger.md`.

## Now

- [ ] Verify staging on `vedicjivan-test.nandishdave.world`, then merge
      `staging` → `main` (the security fixes alone justify it: PyJWT migration,
      CORS, constant-time secret compare).
- [ ] Refresh the root `README.md`: the roadmap still lists built features as
      unchecked (Swiss Ephemeris, yogas, doshas, PDF generation, Stripe,
      reschedule, reminders, Google Calendar, matching); tech stack still says
      python-jose; page and test counts are out of date.
- [ ] Refresh `ReadMe/README.md`: it still describes the 8-factor, 0.57-AUC
      model and 37 famous charts; the ledger has the current 18-factor model on
      225 famous charts.

## Quality debt

- [ ] Make the ruff lint check blocking in CI (`.github/workflows/test-backend.yml`
      runs it with `continue-on-error` today).
- [ ] Add frontend and e2e tests for the calculator, muhurta and unshakable
      pages; none exist.
- [ ] Split `api/app/services/pdf_sections/sections.py` (still about 2,400 lines).

## Product

Still open from the old README roadmap and `ReadMe/data/unshakable-chart-finder-plan.md`:

- [ ] Paid detailed report tier (free sample → paid conversion).
- [ ] AI-written interpretive text in reports.
- [ ] Unshakable finder: per-job charging and year-scale scans
      (on-demand ECS RunTask / Batch).
- [ ] Contact form API endpoint with spam protection.
- [ ] User accounts: registration, saved birth charts, report downloads,
      booking/payment history, Google OAuth.
- [ ] Course platform: enrolment with payment, video hosting, progress tracking.
- [ ] Admin: customer management, content CRUD (blog, services, courses,
      testimonials), refund management.
- [ ] Mobile app reusing the FastAPI backend (future consideration).

## Research (fame study)

- [ ] Add more charts in the domains the model reads well (science, business,
      politics) — the ledger names this as the main lever, not more rules.
- [ ] Handle local mean time for pre-1910 births (may be off by ±30 min today).
- [ ] Before testing any new factor, check the "Rejected" table in
      `ReadMe/experiment-ledger.md` so it is not re-tested.
