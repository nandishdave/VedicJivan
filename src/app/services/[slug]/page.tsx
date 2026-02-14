import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import {
  Phone,
  Video,
  FileText,
  Hash,
  Home,
  Heart,
  ArrowRight,
  Clock,
  CheckCircle2,
} from "lucide-react";
import { Container } from "@/components/ui/Container";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { AnimateOnScroll } from "@/components/ui/AnimateOnScroll";
import { FAQAccordion } from "@/components/ui/FAQAccordion";
import { FloatingElements } from "@/components/ui/FloatingElements";
import { TiltCard } from "@/components/ui/TiltCard";
import { services, getServiceBySlug, getRelatedServices } from "@/data/services";
import { ServiceJsonLd, FAQJsonLd, BreadcrumbJsonLd } from "@/components/seo/JsonLd";

const iconMap: Record<string, React.ReactNode> = {
  Phone: <Phone className="h-8 w-8" />,
  Video: <Video className="h-8 w-8" />,
  FileText: <FileText className="h-8 w-8" />,
  Hash: <Hash className="h-8 w-8" />,
  Home: <Home className="h-8 w-8" />,
  Heart: <Heart className="h-8 w-8" />,
};

const iconMapSmall: Record<string, React.ReactNode> = {
  Phone: <Phone className="h-6 w-6" />,
  Video: <Video className="h-6 w-6" />,
  FileText: <FileText className="h-6 w-6" />,
  Hash: <Hash className="h-6 w-6" />,
  Home: <Home className="h-6 w-6" />,
  Heart: <Heart className="h-6 w-6" />,
};

export function generateStaticParams() {
  return services.map((s) => ({ slug: s.slug }));
}

export function generateMetadata({
  params,
}: {
  params: { slug: string };
}): Metadata {
  const service = getServiceBySlug(params.slug);
  if (!service) return { title: "Service Not Found" };

  return {
    title: service.title,
    description: service.shortDescription,
    alternates: {
      canonical: `/services/${params.slug}`,
    },
    openGraph: {
      title: service.title,
      description: service.shortDescription,
      type: "website",
      url: `/services/${params.slug}`,
    },
  };
}

export default function ServiceDetailPage({
  params,
}: {
  params: { slug: string };
}) {
  const service = getServiceBySlug(params.slug);
  if (!service) notFound();

  const related = getRelatedServices(params.slug);

  const BASE_URL = "https://vedicjivan.nandishdave.world";

  return (
    <>
      <ServiceJsonLd
        name={service.title}
        description={service.shortDescription}
        priceINR={service.priceINR}
        url={`${BASE_URL}/services/${service.slug}`}
      />
      <FAQJsonLd faqs={service.faqs} />
      <BreadcrumbJsonLd
        items={[
          { name: "Home", url: BASE_URL },
          { name: "Services", url: `${BASE_URL}/services` },
          { name: service.title, url: `${BASE_URL}/services/${service.slug}` },
        ]}
      />

      {/* ===== HERO ===== */}
      <section className="relative overflow-hidden bg-dark-gradient py-16 sm:py-24">
        <FloatingElements />
        <Container className="relative z-10">
          <AnimateOnScroll animation="fadeIn">
            <div className="mx-auto max-w-4xl">
              <Link
                href="/services"
                className="mb-6 inline-flex items-center gap-1 text-sm text-gray-400 hover:text-gold-400"
              >
                <ArrowRight className="h-3 w-3 rotate-180" />
                All Services
              </Link>

              <div className="flex flex-col gap-8 lg:flex-row lg:items-start lg:justify-between">
                <div className="flex-1">
                  <div className="mb-4 flex items-center gap-3">
                    <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-white/10 text-gold-400">
                      {iconMap[service.icon] || (
                        <FileText className="h-8 w-8" />
                      )}
                    </div>
                    <Badge variant="gold">{service.category}</Badge>
                  </div>

                  <h1 className="font-heading text-3xl font-bold text-white sm:text-4xl lg:text-5xl">
                    {service.title}
                  </h1>
                  <p className="mt-4 max-w-2xl text-lg text-gray-300">
                    {service.shortDescription}
                  </p>

                  {service.duration && (
                    <div className="mt-4 flex items-center gap-2 text-gray-400">
                      <Clock className="h-4 w-4" />
                      <span>{service.duration} session</span>
                    </div>
                  )}
                </div>

                <div className="shrink-0 rounded-2xl border border-white/10 bg-white/5 p-8 text-center backdrop-blur-sm">
                  <p className="text-sm text-gray-400">Starting at</p>
                  <p className="mt-1 font-heading text-4xl font-bold text-white">
                    {service.priceINR}
                  </p>
                  <p className="text-sm text-gray-400">{service.priceEUR}</p>
                  <Button variant="gold" size="lg" className="mt-6 w-full">
                    Book Now
                    <ArrowRight className="h-5 w-5" />
                  </Button>
                </div>
              </div>
            </div>
          </AnimateOnScroll>
        </Container>
      </section>

      {/* ===== DESCRIPTION ===== */}
      <section className="vedic-section">
        <Container>
          <div className="mx-auto max-w-4xl">
            <div className="grid gap-12 lg:grid-cols-3">
              <div className="lg:col-span-2">
                <AnimateOnScroll animation="fadeUp">
                  <h2 className="font-heading text-2xl font-bold text-vedic-dark sm:text-3xl">
                    About This Service
                  </h2>
                  <p className="mt-4 leading-relaxed text-gray-600">
                    {service.description}
                  </p>
                </AnimateOnScroll>

                {/* Process Steps */}
                <AnimateOnScroll animation="fadeUp" delay={0.2}>
                  <h3 className="mt-12 font-heading text-xl font-bold text-vedic-dark">
                    How It Works
                  </h3>
                  <div className="mt-6 space-y-6">
                    {service.process.map((step) => (
                      <div key={step.step} className="flex gap-4">
                        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-primary-100 font-bold text-primary-600">
                          {step.step}
                        </div>
                        <div>
                          <h4 className="font-semibold text-vedic-dark">
                            {step.title}
                          </h4>
                          <p className="mt-1 text-sm text-gray-600">
                            {step.description}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </AnimateOnScroll>
              </div>

              {/* Features Sidebar */}
              <div>
                <AnimateOnScroll animation="fadeRight">
                  <div className="rounded-2xl border border-gray-100 bg-cream p-6">
                    <h3 className="font-heading text-lg font-bold text-vedic-dark">
                      What&apos;s Included
                    </h3>
                    <ul className="mt-4 space-y-3">
                      {service.features.map((feature, i) => (
                        <li
                          key={i}
                          className="flex items-start gap-2 text-sm text-gray-600"
                        >
                          <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-green-500" />
                          {feature}
                        </li>
                      ))}
                    </ul>
                  </div>
                </AnimateOnScroll>
              </div>
            </div>
          </div>
        </Container>
      </section>

      {/* ===== FAQ ===== */}
      <section className="vedic-section bg-cream">
        <Container>
          <div className="mx-auto max-w-3xl">
            <AnimateOnScroll animation="fadeUp">
              <h2 className="mb-8 text-center font-heading text-2xl font-bold text-vedic-dark sm:text-3xl">
                Frequently Asked Questions
              </h2>
            </AnimateOnScroll>

            <AnimateOnScroll animation="fadeUp" delay={0.1}>
              <FAQAccordion items={service.faqs} />
            </AnimateOnScroll>
          </div>
        </Container>
      </section>

      {/* ===== RELATED SERVICES ===== */}
      <section className="vedic-section">
        <Container>
          <AnimateOnScroll animation="fadeUp">
            <h2 className="mb-8 text-center font-heading text-2xl font-bold text-vedic-dark sm:text-3xl">
              You May Also Like
            </h2>
          </AnimateOnScroll>

          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {related.map((s, i) => (
              <AnimateOnScroll key={s.slug} animation="fadeUp" delay={i * 0.1}>
                <Link href={`/services/${s.slug}`} className="block h-full">
                  <TiltCard className="h-full rounded-2xl border border-gray-100 bg-white p-6 shadow-sm transition-shadow hover:shadow-lg" tiltDegree={6}>
                    <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-xl bg-primary-100 text-primary-600">
                      {iconMapSmall[s.icon] || (
                        <FileText className="h-6 w-6" />
                      )}
                    </div>
                    <h3 className="font-heading text-xl font-bold text-vedic-dark">
                      {s.title}
                    </h3>
                    <p className="mt-2 text-sm text-gray-600">
                      {s.shortDescription}
                    </p>
                    <div className="mt-4 flex items-center gap-2">
                      <span className="text-lg font-bold text-primary-600">
                        {s.priceINR}
                      </span>
                      {s.duration && (
                        <span className="text-sm text-gray-400">
                          / {s.duration}
                        </span>
                      )}
                    </div>
                  </TiltCard>
                </Link>
              </AnimateOnScroll>
            ))}
          </div>
        </Container>
      </section>

      {/* ===== CTA ===== */}
      <section className="relative overflow-hidden bg-vedic-gradient py-16">
        <Container className="relative z-10">
          <AnimateOnScroll animation="scaleIn">
            <div className="mx-auto max-w-3xl text-center">
              <h2 className="font-heading text-3xl font-bold text-white sm:text-4xl">
                Ready to Book Your {service.title}?
              </h2>
              <p className="mx-auto mt-4 max-w-xl text-lg text-primary-200">
                Take the first step towards clarity and guidance. Book your
                session today.
              </p>
              <div className="mt-8 flex flex-col items-center justify-center gap-4 sm:flex-row">
                <Button variant="gold" size="lg">
                  Book Now — {service.priceINR}
                  <ArrowRight className="h-5 w-5" />
                </Button>
                <Link href="/contact">
                  <Button
                    variant="outline"
                    size="lg"
                    className="border-white/30 text-white hover:bg-white/10"
                  >
                    Have Questions?
                  </Button>
                </Link>
              </div>
            </div>
          </AnimateOnScroll>
        </Container>
      </section>
    </>
  );
}
