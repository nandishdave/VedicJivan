# VedicJivan

**Vedic astrology and holistic wellness platform** offering consultations, automated horoscope/Kundli report generation, numerology, Vastu guidance, personal growth coaching, therapeutic healing, and astrology courses.

*Transform Your Life Through Vedic Wisdom*

| | Production | Test |
|---|---|---|
| Frontend | https://vedicjivan.nandishdave.world | https://vedicjivan-test.nandishdave.world |
| API | https://api.vedicjivan.nandishdave.world | https://api.vedicjivan-test.nandishdave.world |

---

## Table of Contents

- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Local Development](#local-development)
- [Testing](#testing)
- [Infrastructure](#infrastructure)
- [CI/CD](#cicd)
- [Environment Toggle](#environment-toggle)
- [Maintenance Mode](#maintenance-mode)
- [Operations Reference](#operations-reference)
- [Features](#features)
- [Roadmap](#roadmap)

---

## Architecture

```
Internet
    |
Route 53 (DNS: *.nandishdave.world)
    |
    |--- CloudFront (CDN) ---> S3 Bucket
    |        Next.js static export
    |        HTML, CSS, JS, images
    |
    |--- API Gateway ---> ECS Fargate (via Cloud Map)
             FastAPI / Python
             api.vedicjivan.nandishdave.world
                    |
                    |--- MongoDB Atlas (Database)
                    |--- Resend (Email delivery)
                    |--- Razorpay (INR payments)
                    |--- Google Places API (Birth place autocomplete)
```

**Why separate frontend + backend?**
- Frontend stays on CDN (fast, cheap, globally distributed)
- Backend scales independently on ECS Fargate
- Core astrology engine requires Python-specific libraries (Swiss Ephemeris)
- Backend can be reused for a mobile app in the future

---

## Tech Stack

### Frontend
| Technology | Purpose |
|---|---|
| Next.js 14 (App Router) | React framework, static export (`output: "export"`) |
| TypeScript | Type safety |
| Tailwind CSS | Styling with custom Vedic theme (deep purple, sacred gold, saffron) |
| Framer Motion | Animations (page transitions, hover effects, scroll-triggered) |
| Vitest + Testing Library | Unit and component tests |

### Backend
| Technology | Purpose |
|---|---|
| Python 3.12+ | Language |
| FastAPI | Async web framework with auto-generated OpenAPI docs |
| Motor | Async MongoDB driver |
| Pydantic | Request/response validation |
| python-jose + bcrypt | JWT authentication + password hashing |
| Razorpay SDK | INR payment processing |
| Resend | Transactional email delivery |
| Docker | Containerization for ECS Fargate |

### Infrastructure
| Service | Purpose |
|---|---|
| AWS S3 + CloudFront | Frontend hosting (CDN, HTTP/3, gzip) |
| AWS ECS Fargate | Backend hosting (0.25 vCPU, 512 MiB) |
| AWS API Gateway + Cloud Map | API routing and service discovery |
| AWS ECR | Docker image registry |
| AWS Route 53 | DNS management |
| AWS ACM | SSL certificates (frontend + API) |
| AWS SSM Parameter Store | Secrets (MongoDB URI, JWT secret, API keys) |
| AWS CloudWatch | Logs, alarms (5XX errors, CPU, unhealthy hosts) |
| MongoDB Atlas | Managed database (M0 free tier) |
| Terraform | Infrastructure as Code (workspace-based multi-env) |
| GitHub Actions | CI/CD pipelines |

---

## Project Structure

```
VedicJivan/
|-- src/                        # Next.js frontend source
|   |-- app/                    # App Router pages (36 pages)
|   |   |-- admin/              # Admin panel (dashboard, bookings, availability, payments, settings)
|   |   |-- book/[slug]/        # Booking wizard per service
|   |   |-- services/[slug]/    # Service detail pages (9 services)
|   |   |-- courses/[slug]/     # Course detail pages (4 courses)
|   |   |-- blog/[slug]/        # Blog post pages (8+ articles)
|   |   |-- contact/            # Contact page
|   |   +-- ...                 # About, legal, etc.
|   |-- components/             # React components
|   |   |-- booking/            # BookingWizard, Calendar, TimeSlotPicker, PendingBookingBanner
|   |   |-- ui/                 # Button, Card, Input, Badge, etc.
|   |   |-- layout/             # Header, Footer, navigation
|   |   |-- seo/                # JSON-LD structured data
|   |   +-- analytics/          # Google Analytics 4
|   |-- data/                   # Static data (services, courses, blog posts, testimonials)
|   |-- lib/                    # API client, auth, analytics helpers
|   +-- config/                 # Site configuration (brand, contact, social)
|
|-- api/                        # FastAPI backend
|   |-- app/
|   |   |-- main.py             # FastAPI app, CORS, router registration
|   |   |-- config.py           # Settings (pydantic-settings)
|   |   |-- database.py         # Motor async MongoDB connection
|   |   |-- dependencies.py     # Auth dependencies (get_current_user, require_admin)
|   |   |-- routers/            # API route handlers
|   |   |   |-- auth.py         # Register, login, me, refresh
|   |   |   |-- bookings.py     # Booking CRUD, pricing, slot validation
|   |   |   |-- payments.py     # Razorpay order creation, verification, webhook
|   |   |   |-- availability.py # Slot management, business hours, holidays
|   |   |   +-- admin.py        # Dashboard stats endpoint
|   |   |-- models/             # Pydantic models
|   |   |-- services/           # Email service (confirmation, notification, cancellation)
|   |   +-- utils/              # Security, exceptions
|   |-- tests/                  # pytest + httpx async tests
|   |-- Dockerfile.prod         # Production Docker image
|   +-- docker-compose.yml      # Local dev (API + MongoDB)
|
|-- terraform/                  # Infrastructure as Code
|   |-- locals.tf               # Workspace-aware naming (central logic)
|   |-- provider.tf             # AWS provider (ap-south-1 + us-east-1 alias)
|   |-- variables.tf            # Input variables
|   |-- prod.tfvars             # Production overrides (ACM cert, maintenance_mode)
|   |-- test.tfvars             # Test overrides (basic auth credentials)
|   |-- switch-env.sh           # Environment toggle script
|   |-- s3.tf                   # S3 bucket for static site
|   |-- cloudfront.tf           # CloudFront CDN + maintenance page + basic auth
|   |-- ecs.tf                  # ECS cluster, task definition, service
|   |-- ecr.tf                  # ECR Docker repository
|   |-- alb.tf                  # API Gateway, VPC Link, Cloud Map
|   |-- route53.tf              # DNS records + ACM certificates
|   |-- iam.tf                  # IAM deployer user, ECS roles
|   |-- secrets.tf              # SSM parameter placeholders
|   |-- security_groups.tf      # ECS security group
|   |-- autoscaling.tf          # ECS auto scaling (CPU-based, 1-2 tasks)
|   |-- cloudwatch.tf           # Log groups, SNS alerts, CloudWatch alarms
|   |-- outputs.tf              # Terraform outputs (bucket, CloudFront ID, etc.)
|   +-- vpc.tf                  # Default VPC data sources
|
|-- .github/workflows/
|   |-- deploy.yml              # Frontend CI/CD (S3 + CloudFront)
|   +-- deploy-api.yml          # Backend CI/CD (ECR + ECS)
|
+-- public/                     # Static assets (images, logos, favicons)
```

---

## Local Development

### Prerequisites
- Node.js 20+
- Python 3.12+
- Docker (for local MongoDB)

### Frontend

```bash
# Install dependencies
npm install

# Start dev server (http://localhost:3000)
npm run dev
```

Create `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_GA_ID=                           # Optional: Google Analytics
NEXT_PUBLIC_YOUTUBE_API_KEY=                  # Optional: YouTube integration
NEXT_PUBLIC_YOUTUBE_CHANNEL_ID=               # Optional
NEXT_PUBLIC_GOOGLE_PLACES_API_KEY=            # For birth place autocomplete
```

### Backend

```bash
cd api

# Start API + MongoDB via Docker
docker compose up

# Or run directly (requires local MongoDB)
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Create `api/.env`:
```env
APP_ENV=development
APP_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
MONGODB_URI=mongodb://vedicjivan-mongo:27017/vedicjivan
JWT_SECRET=<openssl rand -hex 32>
RAZORPAY_KEY_ID=<test key>
RAZORPAY_KEY_SECRET=<test secret>
RESEND_API_KEY=<api key>
ADMIN_EMAIL=vedic.jivan33@gmail.com
```

API docs available at http://localhost:8000/docs (Swagger UI).

---

## Testing

### Frontend (202 tests, ~88% coverage)

```bash
npm run test           # Run once
npm run test:watch     # Watch mode
npm run test:cov       # With coverage report
```

Key test areas: BookingWizard flow, admin pages, API client, auth, analytics, birth detail pickers.

### Backend (219 tests, ~97% coverage)

```bash
cd api
pytest                 # Run all tests
pytest --cov=app       # With coverage
```

Key test areas: Booking CRUD, availability, payments (Razorpay), auth, admin dashboard.

---

## Infrastructure

### Multi-Environment with Terraform Workspaces

The same Terraform code manages both production and test environments using workspaces:

| Workspace | Environment | Frontend | API |
|---|---|---|---|
| `default` | prod | vedicjivan.nandishdave.world | api.vedicjivan.nandishdave.world |
| `test` | test | vedicjivan-test.nandishdave.world | api.vedicjivan-test.nandishdave.world |

All resource names are derived from `terraform/locals.tf`:
- **Prod**: `vedicjivan-website`, `vedicjivan-api`, `/vedicjivan/MONGODB_URI`, etc.
- **Test**: `vedicjivan-test-website`, `vedicjivan-test-api`, `/vedicjivan-test/MONGODB_URI`, etc.

### What's shared between environments
- Default VPC and subnets
- Route 53 hosted zone (`nandishdave.world`)

### What's separate per environment
S3 bucket, CloudFront distribution, ACM certificates, ECR repository, ECS cluster/service/task, API Gateway, Cloud Map namespace, SSM parameters, IAM deployer user, security groups, CloudWatch log groups and alarms, auto scaling policies, Route 53 records.

### Test Environment Protections
- **Basic Auth**: CloudFront Function prompts for username/password before loading the site
- **noindex headers**: `X-Robots-Tag: noindex, nofollow, noarchive` prevents search engine indexing
- Both are conditional and only active for non-production workspaces

### Terraform Commands

```bash
cd terraform

# Production
terraform workspace select default
terraform plan -var-file=prod.tfvars
terraform apply -var-file=prod.tfvars

# Test
terraform workspace select test
terraform plan -var-file=test.tfvars
terraform apply -var-file=test.tfvars
```

### SSM Parameters (per environment)

Each environment needs these parameters in AWS SSM Parameter Store:

| Parameter | Description |
|---|---|
| `/<prefix>/MONGODB_URI` | MongoDB Atlas connection string |
| `/<prefix>/JWT_SECRET` | JWT signing secret |
| `/<prefix>/RAZORPAY_KEY_ID` | Razorpay API key |
| `/<prefix>/RAZORPAY_KEY_SECRET` | Razorpay API secret |
| `/<prefix>/RAZORPAY_WEBHOOK_SECRET` | Razorpay webhook secret |
| `/<prefix>/RESEND_API_KEY` | Resend email API key |
| `/<prefix>/ADMIN_EMAIL` | Admin notification email |

Where `<prefix>` is `vedicjivan` (prod) or `vedicjivan-test` (test).

Set via AWS CLI:
```bash
MSYS_NO_PATHCONV=1 aws ssm put-parameter \
  --name "/vedicjivan-test/MONGODB_URI" \
  --value "mongodb+srv://..." \
  --type SecureString --overwrite \
  --region ap-south-1 --profile nandishdave-personal-1
```

> Note: `MSYS_NO_PATHCONV=1` is required on Git Bash for Windows to prevent path conversion of the `--name` argument.

---

## CI/CD

### Branch-to-Environment Mapping

| Branch | Environment | Secrets prefix |
|---|---|---|
| `main` | Production | `AWS_ACCESS_KEY_ID`, `S3_BUCKET_NAME`, etc. |
| `staging` | Test | `TEST_AWS_ACCESS_KEY_ID`, `TEST_S3_BUCKET_NAME`, etc. |

### Frontend Deployment (`.github/workflows/deploy.yml`)

Triggered on push to `main` or `staging`:
1. Install dependencies + build static site
2. Determine environment from branch name
3. Sync `./out` to the correct S3 bucket
4. Invalidate the correct CloudFront distribution

### Backend Deployment (`.github/workflows/deploy-api.yml`)

Triggered on push to `main` or `staging` with changes in `api/**`:
1. Determine environment from branch name
2. Build Docker image + push to the correct ECR repository
3. Force new ECS deployment on the correct cluster/service

### GitHub Secrets Required

**Production** (from `terraform output` in `default` workspace):
`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`, `S3_BUCKET_NAME`, `CLOUDFRONT_DISTRIBUTION_ID`, `ECR_REPOSITORY`, `ECS_CLUSTER`, `ECS_SERVICE`

**Test** (from `terraform output` in `test` workspace):
`TEST_AWS_ACCESS_KEY_ID`, `TEST_AWS_SECRET_ACCESS_KEY`, `TEST_S3_BUCKET_NAME`, `TEST_CLOUDFRONT_DISTRIBUTION_ID`, `TEST_ECR_REPOSITORY`, `TEST_ECS_CLUSTER`, `TEST_ECS_SERVICE`

**Shared** (user-managed):
`NEXT_PUBLIC_GA_ID`, `NEXT_PUBLIC_YOUTUBE_API_KEY`, `NEXT_PUBLIC_YOUTUBE_CHANNEL_ID`, `NEXT_PUBLIC_GOOGLE_PLACES_API_KEY`

---

## Environment Toggle

A single script switches between production and test environments. Only one environment runs at a time to minimize costs (~$9-12/month for ECS Fargate per environment).

```bash
cd terraform

# Activate production, shut down test
./switch-env.sh prod

# Activate test, shut down production
./switch-env.sh test
```

**What happens when an environment is shut down:**
- CloudFront serves an animated maintenance page (503) with the VedicJivan lotus logo
- ECS auto scaling target is set to min=0, max=0 (Fargate tasks stop = $0 cost)
- All other resources (S3, CloudFront, Route 53, etc.) remain but cost nothing when idle

**What happens when an environment is activated:**
- Maintenance page is removed, CloudFront serves normally
- ECS auto scaling target is restored to min=1, max=2

The script applies Terraform to both workspaces sequentially with `-var "maintenance_mode=true/false"` overrides, so no file edits are needed.

### Typical workflow

1. Ready to develop/test: `./switch-env.sh test` (prod shows maintenance page, test is live)
2. Push changes to `staging` branch (CI/CD deploys to test environment)
3. Verify on https://vedicjivan-test.nandishdave.world (password-protected)
4. Merge `staging` into `main` (CI/CD deploys to production)
5. Go live: `./switch-env.sh prod` (test shuts down, prod is live)

---

## Maintenance Mode

Maintenance mode can be enabled per environment independently via the `maintenance_mode` Terraform variable.

When enabled:
- CloudFront returns a **503 Service Temporarily Unavailable** page with:
  - Animated starfield background
  - Floating VedicJivan lotus logo (inline SVG)
  - "We will be back soon" message with spinner
  - Contact email link
  - `Retry-After: 3600` and `Cache-Control: no-store` headers
- ECS Fargate tasks scale to 0 (no compute cost)

### Enable/disable manually

```bash
cd terraform

# Enable maintenance on prod
terraform workspace select default
terraform apply -var-file=prod.tfvars -var "maintenance_mode=true"

# Disable maintenance on prod
terraform apply -var-file=prod.tfvars -var "maintenance_mode=false"
```

Or use the toggle script (`./switch-env.sh`) which manages both environments together.

---

## Operations Reference

### Force ECS redeployment (picks up new SSM values)

```bash
aws ecs update-service \
  --cluster vedicjivan-cluster \
  --service vedicjivan-api \
  --force-new-deployment \
  --region ap-south-1 --profile nandishdave-personal-1
```

### View ECS container logs

```bash
aws logs tail /ecs/vedicjivan-api --follow \
  --region ap-south-1 --profile nandishdave-personal-1
```

### Check API health

```bash
curl https://api.vedicjivan.nandishdave.world/api/health
curl https://api.vedicjivan-test.nandishdave.world/api/health
```

### Import an existing Route 53 record into Terraform

```bash
terraform import -var-file=prod.tfvars \
  'aws_route53_record.frontend' \
  '<ZONE_ID>_vedicjivan.nandishdave.world_A'
```

### Estimated monthly costs

| Service | Cost |
|---|---|
| ECS Fargate (1 task, 0.25 vCPU, 512 MiB) | ~$9-12 |
| S3 + CloudFront | ~$1-5 (low traffic) |
| MongoDB Atlas (M0) | Free |
| Route 53 | ~$0.50 |
| Everything else (ECR, SSM, CloudWatch, API Gateway) | Free tier |
| **Total (one environment active)** | **~$10-18/month** |

> With the environment toggle, only one ECS environment runs at a time, keeping costs at ~$10-18/month total rather than ~$20-36 for both.

---

## Features

### Customer-Facing Website (36 pages)
- Homepage with animated hero, services grid, testimonials carousel, course preview
- 9 service detail pages (6 astrology + 3 wellness) with pricing, FAQs, process steps
- 4 course detail pages with full curriculum
- 8+ blog articles with social sharing (WhatsApp, X, Facebook, LinkedIn)
- Contact page with WhatsApp integration
- Legal pages (privacy policy, terms of service, refund policy)

### Booking System
- Multi-step booking wizard: select date > pick time slot > choose duration > enter details > review > pay > confirmation
- Server-side price calculation with service-specific pricing by duration
- Available slot management with bulk creation (date range, working days, time range)
- Smart slot validation: past time filtering, business hours checking, overlap detection
- Auto-expire unpaid bookings after 15 minutes (query-time filtering)
- Resume unfinished bookings via localStorage (global banner with countdown)
- Birth details collection: DOB picker, time of birth (with "unknown" option), place of birth (Google Places autocomplete with lat/lng)
- Report-type services (Kundli, Numerology, Matchmaking) skip scheduling steps

### Payments (Razorpay - INR)
- Order creation, HMAC SHA256 signature verification, webhook handling
- Frontend Razorpay checkout widget with customer prefill
- Test mode with test API keys (test environment shows "Test Mode" badge)

### Emails
- Customer booking confirmation (service, date, time, amount)
- Admin notification on new booking
- Booking cancellation email

### Admin Panel (`/admin`)
- JWT-protected with admin role check
- Dashboard: today's bookings, upcoming count, total revenue, revenue chart, bookings trend
- Booking management: filter by status, confirm/complete/cancel actions
- Availability management: bulk slot creation, single day editor
- Payment history table
- Settings: business hours per day, holiday management

### SEO & Analytics
- Auto-generated sitemap.xml and robots.txt
- JSON-LD structured data (Organization, WebSite, Service, FAQ, Course, BlogPosting, BreadcrumbList, Person)
- OpenGraph + Twitter Card metadata on every page
- Google Analytics 4 with custom event tracking
- Google Search Console and Bing Webmaster Tools verified

### Animations & UX
- Spring-powered buttons, card hover effects (lift + glow), page transitions
- Scroll-triggered entrance animations (fadeUp, fadeLeft, scaleIn, blurIn)
- Animated gradient text, floating sparkle particles, magnetic CTA buttons
- Staggered grid reveals, section dividers (wave, dots)

---

## Roadmap

### In Progress / Partially Complete
- [ ] Stripe integration (EUR/USD for international customers)
- [ ] Contact form API endpoint with spam protection
- [ ] Additional email templates (welcome, payment receipt, booking reminder)
- [ ] Google OAuth authentication
- [ ] Rate limiting on auth endpoints

### Planned - Astrology Engine (Phase 3)
The core product differentiator - automated Vedic astrology calculations:
- [ ] Swiss Ephemeris integration (`pyswisseph`)
- [ ] Birth chart (Rashi) calculation with Lahiri Ayanamsa
- [ ] Nakshatra, house (Bhava), and Dasha period calculations
- [ ] Yoga detection (Raj Yoga, Dhan Yoga, etc.)
- [ ] Dosha detection (Mangal, Kaal Sarp, Pitra, etc.)
- [ ] Transit (Gochar) analysis
- [ ] Kundli matching (Ashtakoot/Gun Milan)
- [ ] Numerology calculations

### Planned - Report Generation (Phase 4)
Free sample to paid conversion flow:
- [ ] Free sample report (basic chart overview)
- [ ] Paid detailed report (full Kundli, Dasha timeline, predictions, remedies)
- [ ] PDF generation with branded template (ReportLab/WeasyPrint)
- [ ] AI-powered interpretive text (Claude API)
- [ ] Report storage and email delivery

### Planned - User Accounts (Phase 8)
- [ ] User registration (email/password + Google OAuth)
- [ ] User dashboard with booking history and report downloads
- [ ] Saved birth charts for family members
- [ ] Order/payment history

### Planned - Course Platform (Phase 9)
- [ ] Course enrollment with payment
- [ ] Video hosting integration
- [ ] Progress tracking and completion certificates

### Planned - Admin Enhancements
- [ ] Customer management (search, view history)
- [ ] Content management (blog CRUD, service/course editing)
- [ ] Refund management
- [ ] Testimonial CRUD
- [ ] GA4 visitor stats on dashboard

### Future Considerations
- [ ] Geolocation-based currency auto-detection (INR vs EUR)
- [ ] Google Calendar integration for bookings
- [ ] Booking reminder emails (24h before)
- [ ] Reschedule flow
- [ ] Mobile app (React Native, reusing the FastAPI backend)
