import type { Metadata } from "next";
import Link from "next/link";
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
  Compass,
  Leaf,
  HeartHandshake,
} from "lucide-react";
import { Container } from "@/components/ui/Container";
import { Button } from "@/components/ui/Button";
import { Card, CardContent } from "@/components/ui/Card";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Badge } from "@/components/ui/Badge";
import { AnimateOnScroll } from "@/components/ui/AnimateOnScroll";
import { FAQAccordion } from "@/components/ui/FAQAccordion";
import { FloatingElements } from "@/components/ui/FloatingElements";
import { GradientText } from "@/components/ui/GradientText";
import { services } from "@/data/services";

const astrologyServices = services.filter((s) => s.category !== "wellness");
const wellnessServices = services.filter((s) => s.category === "wellness");

export const metadata: Metadata = {
  title: "Services",
  description:
    "Explore VedicJivan's astrology and wellness services — consultations, Kundli reports, numerology, Vastu, personal growth coaching, and therapeutic healing.",
  alternates: { canonical: "/services" },
  openGraph: {
    title: "Services | VedicJivan",
    description:
      "Explore VedicJivan's astrology and wellness services — consultations, Kundli reports, numerology, Vastu, personal growth coaching, and therapeutic healing.",
    url: "/services",
  },
};

const iconMap: Record<string, React.ReactNode> = {
  Phone: <Phone className="h-6 w-6" />,
  Video: <Video className="h-6 w-6" />,
  FileText: <FileText className="h-6 w-6" />,
  Hash: <Hash className="h-6 w-6" />,
  Home: <Home className="h-6 w-6" />,
  Heart: <Heart className="h-6 w-6" />,
  Compass: <Compass className="h-6 w-6" />,
  Leaf: <Leaf className="h-6 w-6" />,
  HeartHandshake: <HeartHandshake className="h-6 w-6" />,
};

export default function ServicesPage() {
  return (
    <>
      {/* ===== HERO ===== */}
      <section className="relative overflow-hidden vedic-hero-gradient py-20 sm:py-28">
        <FloatingElements />
        <Container className="relative z-10">
          <AnimateOnScroll animation="fadeIn">
            <div className="mx-auto max-w-3xl text-center">
              <span className="mb-3 inline-block text-sm font-semibold uppercase tracking-widest text-gold-400">
                Our Services
              </span>
              <h1 className="font-heading text-4xl font-bold text-white sm:text-5xl lg:text-6xl">
                Astrology & Wellness{" "}
                <GradientText variant="gold">Services</GradientText>
              </h1>
              <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-300">
                From astrology consultations and Kundli reports to personal growth
                coaching and therapeutic healing — choose the service that supports
                your journey to clarity and well-being.
              </p>
            </div>
          </AnimateOnScroll>
        </Container>
      </section>

      {/* ===== ASTROLOGY SERVICES ===== */}
      <section className="vedic-section">
        <Container>
          <AnimateOnScroll animation="fadeUp">
            <SectionHeading
              subtitle="Astrology"
              title="Vedic Astrology Services"
              description="Authentic consultations, detailed reports, and expert guidance rooted in time-tested Vedic traditions."
            />
          </AnimateOnScroll>

          <div className="grid gap-8 lg:grid-cols-2">
            {astrologyServices.map((service, i) => (
              <AnimateOnScroll key={service.slug} animation="fadeUp" delay={i * 0.08}>
                <Card className="group h-full overflow-hidden" hover={false}>
                  <div className="relative h-48 overflow-hidden">
                    <img
                      src={service.image}
                      alt={service.title}
                      className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
                      loading="lazy"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent" />
                    <Badge variant="gold" className="absolute left-4 top-4">
                      {service.category}
                    </Badge>
                  </div>
                  <CardContent>
                    <div className="flex flex-wrap items-start justify-between gap-2">
                      <h3 className="font-heading text-2xl font-bold text-vedic-dark">
                        {service.title}
                      </h3>
                      <div className="text-right">
                        <p className="text-2xl font-bold text-primary-600">
                          {service.priceINR}
                        </p>
                        <p className="text-sm text-gray-400">
                          {service.priceEUR}
                        </p>
                      </div>
                    </div>

                    <p className="mt-3 text-sm leading-relaxed text-gray-600">
                      {service.shortDescription}
                    </p>

                    {service.duration && (
                      <div className="mt-3 flex items-center gap-1.5 text-sm text-gray-500">
                        <Clock className="h-4 w-4" />
                        {service.duration}
                      </div>
                    )}

                    <ul className="mt-4 grid gap-2 sm:grid-cols-2">
                      {service.features.slice(0, 4).map((feature, j) => (
                        <li
                          key={j}
                          className="flex items-center gap-2 text-sm text-gray-600"
                        >
                          <CheckCircle2 className="h-4 w-4 shrink-0 text-green-500" />
                          {feature}
                        </li>
                      ))}
                    </ul>

                    <div className="mt-6 flex flex-wrap gap-3">
                      <Link href={`/services/${service.slug}`}>
                        <Button variant="primary" size="sm">
                          Learn More
                          <ArrowRight className="h-4 w-4" />
                        </Button>
                      </Link>
                      <Link href={`/services/${service.slug}`}>
                        <Button variant="gold" size="sm">
                          Book Now
                        </Button>
                      </Link>
                    </div>
                  </CardContent>
                </Card>
              </AnimateOnScroll>
            ))}
          </div>
        </Container>
      </section>

      {/* ===== WELLNESS SERVICES ===== */}
      <section className="vedic-section bg-cream">
        <Container>
          <AnimateOnScroll animation="fadeUp">
            <SectionHeading
              subtitle="Wellness"
              title="Holistic Wellness Services"
              description="Integrating astrological guidance, personal growth coaching, and therapeutic healing to support transformation and well-being."
            />
          </AnimateOnScroll>

          <div className="grid gap-8 lg:grid-cols-3">
            {wellnessServices.map((service, i) => (
              <AnimateOnScroll key={service.slug} animation="fadeUp" delay={i * 0.1}>
                <Card className="group h-full overflow-hidden" hover={false}>
                  <div className="relative h-52 overflow-hidden">
                    <img
                      src={service.image}
                      alt={service.title}
                      className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
                      loading="lazy"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent" />
                    <div className="absolute bottom-4 left-4 flex h-10 w-10 items-center justify-center rounded-xl bg-white/90 text-gold-600">
                      {iconMap[service.icon] || <FileText className="h-5 w-5" />}
                    </div>
                  </div>
                  <CardContent>
                    <h3 className="font-heading text-2xl font-bold text-vedic-dark">
                      {service.title}
                    </h3>

                    <p className="mt-3 text-sm leading-relaxed text-gray-600">
                      {service.shortDescription}
                    </p>

                    <div className="mt-4 flex items-center justify-between">
                      <div>
                        <p className="text-xl font-bold text-primary-600">
                          {service.priceINR}
                        </p>
                        <p className="text-xs text-gray-400">{service.priceEUR}</p>
                      </div>
                      {service.duration && (
                        <div className="flex items-center gap-1.5 text-sm text-gray-500">
                          <Clock className="h-4 w-4" />
                          {service.duration}
                        </div>
                      )}
                    </div>

                    <ul className="mt-4 space-y-2">
                      {service.features.slice(0, 4).map((feature, j) => (
                        <li
                          key={j}
                          className="flex items-center gap-2 text-sm text-gray-600"
                        >
                          <CheckCircle2 className="h-4 w-4 shrink-0 text-green-500" />
                          {feature}
                        </li>
                      ))}
                    </ul>

                    <div className="mt-6">
                      <Link href={`/services/${service.slug}`}>
                        <Button variant="primary" size="sm" className="w-full">
                          Learn More
                          <ArrowRight className="h-4 w-4" />
                        </Button>
                      </Link>
                    </div>
                  </CardContent>
                </Card>
              </AnimateOnScroll>
            ))}
          </div>
        </Container>
      </section>

      {/* ===== FAQ ===== */}
      <section className="vedic-section bg-cream">
        <Container>
          <AnimateOnScroll animation="fadeUp">
            <SectionHeading
              subtitle="FAQ"
              title="Frequently Asked Questions"
              description="Got questions? Here are answers to the most common queries about our services."
            />
          </AnimateOnScroll>

          <AnimateOnScroll animation="fadeUp" delay={0.1}>
            <FAQAccordion items={faqs} className="mx-auto max-w-3xl" />
          </AnimateOnScroll>
        </Container>
      </section>

      {/* ===== CTA ===== */}
      <section className="relative overflow-hidden vedic-cta-gradient py-20">
        <Container className="relative z-10">
          <AnimateOnScroll animation="scaleIn">
            <div className="mx-auto max-w-3xl text-center">
              <h2 className="font-heading text-3xl font-bold text-white sm:text-4xl">
                Not Sure Which Service You Need?
              </h2>
              <p className="mx-auto mt-4 max-w-xl text-lg text-primary-200">
                Reach out to us and we&apos;ll help you choose the right service
                based on your specific concerns and needs.
              </p>
              <div className="mt-8">
                <Link href="/contact">
                  <Button variant="gold" size="lg">
                    Contact Us for Guidance
                    <ArrowRight className="h-5 w-5" />
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

const faqs = [
  {
    question: "How do I book a consultation?",
    answer:
      "Simply choose your desired service, select a date and time slot, provide your birth details, and complete the payment. You'll receive a confirmation email with all the details.",
  },
  {
    question: "What birth details do I need to provide?",
    answer:
      "For accurate Vedic astrology analysis, we need your date of birth, exact time of birth, and place of birth. The more precise the birth time, the more accurate the predictions.",
  },
  {
    question: "Do you offer consultations in languages other than English?",
    answer:
      "Yes, we offer consultations in English and Hindi. If you have a preference, please mention it while booking.",
  },
  {
    question: "What payment methods do you accept?",
    answer:
      "We accept all major credit/debit cards, UPI, net banking, and wallets for Indian clients (via Razorpay), and credit cards and bank transfers for international clients (via Stripe).",
  },
  {
    question: "Can I reschedule or cancel my appointment?",
    answer:
      "Yes, you can reschedule up to 24 hours before the appointment at no extra charge. Cancellations made 48+ hours before are eligible for a full refund.",
  },
  {
    question: "Is my information kept confidential?",
    answer:
      "Absolutely. We take privacy very seriously. All personal information and consultation details are kept strictly confidential and never shared with third parties.",
  },
];
