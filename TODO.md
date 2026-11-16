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

## Direction (decided 2026-11-16)

Not ready to go live as-is: too broad, with unfinished pieces a visitor can see.
The plan is to launch around ONE clear thing and add the rest back one at a time.

- Birth Muhurta / Unshakable finder stay as a **side item**, not the headline:
  people trust a named astrologer rather than a tool, and choosing a birth time
  is a sensitive subject for some.
- Candidate headline under evaluation: a **daily Panchang + planetary transits**
  section (in the spirit of Drik Panchang and aaps.space/transits) — factual,
  checkable, daily-use content, grown through SEO and tested with display ads.
- Anything unfinished is **hidden from the frontend, never deleted**: backend
  code, data and tests stay for future expansion.

## Parked — hide from the frontend, bring back when finished

Each item returns only when it works end to end and has a clear reason to exist.

- [ ] **Courses** — four courses with prices and "Enroll Now" buttons but no
      enrolment, payment or delivery behind them. Needs the course platform
      (see Product) before it comes back.
- [ ] **Contact form** — the page only has an email link. Needs a real form
      with an API endpoint and spam protection.
- [ ] **Homepage numbers** — "50,000+ consultations, 40+ countries, 2,000+
      students". Bring back only with real, defensible figures.
- [ ] **Testimonials** — seven entries that read like template content. Bring
      back only with real client testimonials (with permission).
- [ ] **Breadth** — nine services (incl. Vastu, coaching, healing), eight
      calculators, two chart galleries, blog and videos. Decide per item what
      supports the headline; hide the rest from navigation until then.

## Local development

- [ ] Playwright browser download hangs on this laptop — e2e tests can't run
      locally yet.
- [ ] Add a `.gitattributes` rule so `npm run dev` / `npm run build` stop
      marking `src/data/*-index.json` as modified on Windows (line endings).
- [ ] Terraform state was lost with the old laptop (it was never in a remote
      backend). Re-import the existing AWS resources for test and prod, then
      move state to S3. Do not run `terraform apply` or `switch-env.sh` before.

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
