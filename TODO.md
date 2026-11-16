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
- Headline: a **daily Panchang + planetary transits** section (in the spirit
  of Drik Panchang and aaps.space/transits) — factual, checkable, daily-use
  content, grown through SEO and tested with display ads — plus a
  **personalised** view against the visitor's own chart, which neither of
  those sites does well. See "Headline build" below.
- Anything unfinished is **hidden from the frontend, never deleted**: backend
  code, data and tests stay for future expansion.

## Headline build — Panchang, transits and the sky view

Agreed 2026-11-16. The backend already computes panchang, sunrise/sunset, daily
planetary positions and transits over a natal chart, so this is mostly
presentation plus a few new endpoints. Suggested build order:

- [ ] **Static daily Panchang** — tithi, nakshatra, yoga, karana, vara,
      sunrise/sunset, and the day's planetary positions for a chosen city.
      One page per date (and per city) so search engines can index them.
- [ ] **Static transit pages** — for the year: sign changes per planet,
      retrogrades, nakshatra transits, conjunctions; a "current transits"
      summary. Per-planet and per-month pages for search.
- [ ] **Interactive sky view** — a picture of the planets around the zodiac,
      each labelled with its rashi and degree, with a date slider at the bottom
      that moves the planets and updates the degrees as the date changes.
      - Draw it Earth-centred (the astrological view): a true Sun-centred
        solar-system picture would show different longitudes from the rashi
        positions and has no place for the Moon, Rahu or Ketu.
      - Show retrograde motion and mark sign changes on the slider.
      - For a smooth slider, load a precomputed table of daily positions from
        the backend engine and interpolate in the browser, so the numbers
        match the rest of the site exactly.
- [ ] **Personalised Panchang** (the differentiator) — today's panchang and
      transits read against the visitor's own chart: transits by house from
      their Moon sign and Lagna, current dasha, tara bala / chandra bala for
      the day. Leads to a consultation with the named astrologer.
- [ ] Decide how date/city pages get indexed: the site is a pre-built static
      export, so pages must be generated ahead of time or rendered on request.
- [ ] Languages for the top pages: Hindi and Gujarati first.
- [ ] Display ads on these information pages only (never on service or
      booking pages), once the section is live and has content.
- [ ] Measure: page views, returning visitors and bookmarks per page type.

## Parked — hidden from the frontend, bring back when finished

Each item returns only when it works end to end and has a clear reason to exist.
Hidden on 2026-11-16. Nothing was deleted: pages, data and backend are intact.
The switches live in `src/config/features.ts` — flip a flag (or add a slug to
`PUBLIC_SERVICE_SLUGS`) and restore the menu link in `src/config/navigation.ts`.

- [ ] **Courses** (`features.courses`) — four courses with prices and "Enroll
      Now" buttons but no enrolment, payment or delivery behind them. The
      `/courses` pages now return "not found" and are out of the menus and the
      sitemap. Needs the course platform (see Product) before it comes back.
- [ ] **Headline numbers** (`features.stats`) — "50,000+ consultations, 40+
      countries, 15+ years, 2,000+ students". Hidden: the homepage stats bar and,
      on the About page, the stats grid, the milestones timeline and the
      credentials block (all built on the same figures). Bring back only with
      real, defensible figures.
- [ ] **Testimonials** (`features.testimonials`) — the homepage carousel of
      entries that read like template content. Bring back only with real client
      testimonials (with permission).
- [ ] **Five services** — hidden from menus, listings, sitemap and booking;
      their full descriptions stay in `src/data/services.ts` and the backend
      catalogue. Bring each back when you are ready to deliver it:
      - [ ] Numerology Report (`numerology-report`)
      - [ ] Vastu Consultation (`vastu-consultation`)
      - [ ] Astrological Consulting (`astrological-consulting`)
      - [ ] Personal Growth Coaching (`personal-growth-coaching`)
      - [ ] Therapeutic Healing (`therapeutic-healing`)
- [ ] **Contact form** — the page only has an email link. Needs a real form
      with an API endpoint and spam protection.
- [ ] **Still visible, to decide** — eight calculators, the celebrity and
      ordinary chart galleries, blog and videos. Decide per item what supports
      the headline; hide the rest from navigation until then.

Still visible and worth your review, because only you know what is accurate:

- [ ] About page "Our Story" (founder's training, Guru-Shishya lineage, global
      reach) and the homepage badge "Trusted Vedic Astrology Since Generations".
- [ ] Blog posts on numerology and Vastu remain published although those
      services are hidden.
- [ ] Terms and Refund Policy still mention courses.
- [ ] The "Test Payment" service was listed publicly on the Services page; it
      is now unlisted (direct URL only) for testing the payment flow.

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
