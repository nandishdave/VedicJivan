import Link from "next/link";
import {
  Phone,
  Video,
  FileText,
  Star,
  Users,
  Globe,
  Briefcase,
  ArrowRight,
  Sparkles,
  CheckCircle2,
  Compass,
  Leaf,
  HeartHandshake,
} from "lucide-react";
import { Container } from "@/components/ui/Container";
import { Button } from "@/components/ui/Button";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Badge } from "@/components/ui/Badge";
import { AnimateOnScroll } from "@/components/ui/AnimateOnScroll";
import { AnimatedCounter } from "@/components/ui/AnimatedCounter";
import { AnimatedText } from "@/components/ui/AnimatedText";
import { TestimonialsCarousel } from "@/components/ui/TestimonialsCarousel";
import { TiltCard } from "@/components/ui/TiltCard";
import { FloatingElements } from "@/components/ui/FloatingElements";
import { SectionDivider } from "@/components/ui/SectionDivider";
import { MagneticWrapper } from "@/components/ui/MagneticWrapper";

export default function HomePage() {
  return (
    <>
      {/* ===== HERO SECTION ===== */}
      <section className="relative overflow-hidden vedic-hero-gradient py-20 sm:py-28 lg:py-36">
        <FloatingElements />

        <Container className="relative z-10">
          <div className="mx-auto max-w-4xl text-center">
            <AnimateOnScroll animation="fadeIn" duration={0.6}>
              <Badge variant="gold" className="mb-6">
                <Sparkles className="mr-1.5 h-3 w-3" />
                Trusted Vedic Astrology Since Generations
              </Badge>
            </AnimateOnScroll>

            <AnimatedText
              text="Transform Your Life Through Vedic Wisdom"
              className="justify-center text-4xl font-bold leading-tight text-white sm:text-5xl lg:text-6xl xl:text-7xl"
              delay={0.2}
            />

            <AnimateOnScroll animation="fadeUp" delay={0.6}>
              <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-300 sm:text-xl">
                Authentic Vedic astrology consultations, holistic wellness coaching,
                and expert guidance for career, relationships, personal growth, and
                well-being.
              </p>
            </AnimateOnScroll>

            <AnimateOnScroll animation="fadeUp" delay={0.8}>
              <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
                <MagneticWrapper strength={8}>
                  <Link href="/services">
                    <Button variant="gold" size="lg">
                      Book Consultation
                      <ArrowRight className="h-5 w-5" />
                    </Button>
                  </Link>
                </MagneticWrapper>
                <MagneticWrapper strength={8}>
                  <Link href="/services/premium-kundli">
                    <Button variant="outline" size="lg" className="border-white/30 text-white hover:bg-white/10">
                      Get Kundli Report
                    </Button>
                  </Link>
                </MagneticWrapper>
              </div>
            </AnimateOnScroll>
          </div>

          {/* Stats Bar */}
          <AnimateOnScroll animation="fadeUp" delay={1.0}>
            <div className="mx-auto mt-16 grid max-w-3xl grid-cols-2 gap-6 sm:grid-cols-4">
              <div className="text-center">
                <p className="font-heading text-3xl font-bold text-gold-400 sm:text-4xl">
                  <AnimatedCounter end={50000} suffix="+" />
                </p>
                <p className="mt-1 text-sm text-gray-400">Consultations</p>
              </div>
              <div className="text-center">
                <p className="font-heading text-3xl font-bold text-gold-400 sm:text-4xl">
                  <AnimatedCounter end={40} suffix="+" />
                </p>
                <p className="mt-1 text-sm text-gray-400">Countries</p>
              </div>
              <div className="text-center">
                <p className="font-heading text-3xl font-bold text-gold-400 sm:text-4xl">
                  <AnimatedCounter end={15} suffix="+" />
                </p>
                <p className="mt-1 text-sm text-gray-400">Years Experience</p>
              </div>
              <div className="text-center">
                <p className="font-heading text-3xl font-bold text-gold-400 sm:text-4xl">
                  <AnimatedCounter end={9} suffix="+" />
                </p>
                <p className="mt-1 text-sm text-gray-400">Services Offered</p>
              </div>
            </div>
          </AnimateOnScroll>
        </Container>
      </section>

      <SectionDivider variant="wave" />

      {/* ===== SERVICES OVERVIEW ===== */}
      <section className="vedic-section bg-cream">
        <Container>
          <AnimateOnScroll animation="fadeUp">
            <SectionHeading
              subtitle="Astrology Services"
              title="Expert Vedic Guidance For Every Aspect of Life"
              description="Choose from our range of authentic astrology services tailored to bring clarity, direction, and peace to your life."
            />
          </AnimateOnScroll>

          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {services.map((service, i) => (
              <AnimateOnScroll key={service.slug} animation="fadeUp" delay={i * 0.1}>
                <Link href={`/services/${service.slug}`} className="group block h-full">
                  <TiltCard className="h-full overflow-hidden rounded-2xl border border-gray-100 bg-white shadow-sm transition-shadow hover:shadow-lg">
                    <div className="relative h-40 overflow-hidden">
                      <img
                        src={service.image}
                        alt={service.title}
                        className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
                        loading="lazy"
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-black/30 to-transparent" />
                    </div>
                    <div className="p-6">
                      <h3 className="font-heading text-xl font-bold text-vedic-dark">
                        {service.title}
                      </h3>
                      <p className="mt-2 line-clamp-2 text-sm text-gray-600">
                        {service.description}
                      </p>
                      <div className="mt-4 flex items-center gap-2">
                        <span className="text-lg font-bold text-primary-600">
                          {service.price}
                        </span>
                        {service.duration && (
                          <span className="text-sm text-gray-400">
                            / {service.duration}
                          </span>
                        )}
                      </div>
                    </div>
                  </TiltCard>
                </Link>
              </AnimateOnScroll>
            ))}
          </div>

          <AnimateOnScroll animation="fadeIn" delay={0.4}>
            <div className="mt-10 text-center">
              <Link href="/services">
                <Button variant="primary">
                  View All Services
                  <ArrowRight className="h-4 w-4" />
                </Button>
              </Link>
            </div>
          </AnimateOnScroll>
        </Container>
      </section>

      {/* ===== WELLNESS SERVICES ===== */}
      <section className="vedic-section">
        <Container>
          <AnimateOnScroll animation="fadeUp">
            <SectionHeading
              subtitle="Wellness Services"
              title="Holistic Wellness & Transformative Growth"
              description="Beyond astrology, we offer professional consulting in holistic wellness — integrating astrological guidance, personal growth coaching, and therapeutic healing to support your transformation and well-being."
            />
          </AnimateOnScroll>

          <div className="grid gap-8 sm:grid-cols-3">
            {wellnessServices.map((service, i) => (
              <AnimateOnScroll key={service.slug} animation="fadeUp" delay={i * 0.15}>
                <Link href={`/services/${service.slug}`} className="group block h-full">
                  <TiltCard className="h-full overflow-hidden rounded-2xl border border-gray-100 bg-white shadow-sm transition-shadow hover:shadow-lg" tiltDegree={5}>
                    <div className="relative h-48 overflow-hidden">
                      <img
                        src={service.image}
                        alt={service.title}
                        className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
                        loading="lazy"
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent" />
                      <div className="absolute bottom-4 left-4 flex h-12 w-12 items-center justify-center rounded-xl bg-white/90 text-gold-600">
                        {service.icon}
                      </div>
                    </div>
                    <div className="p-6">
                      <h3 className="font-heading text-xl font-bold text-vedic-dark">
                        {service.title}
                      </h3>
                      <p className="mt-3 text-sm leading-relaxed text-gray-600">
                        {service.description}
                      </p>
                      <div className="mt-5 inline-flex items-center gap-1.5 text-sm font-semibold text-primary-600">
                        Learn More
                        <ArrowRight className="h-4 w-4" />
                      </div>
                    </div>
                  </TiltCard>
                </Link>
              </AnimateOnScroll>
            ))}
          </div>
        </Container>
      </section>

      <SectionDivider variant="dots" />

      {/* ===== WHY CHOOSE US ===== */}
      <section className="vedic-section">
        <Container>
          <AnimateOnScroll animation="fadeUp">
            <SectionHeading
              subtitle="Why VedicJivan"
              title="Rooted in Tradition, Powered by Trust"
              description="Discover what makes VedicJivan the preferred choice for thousands of seekers worldwide."
            />
          </AnimateOnScroll>

          <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
            {features.map((feature, i) => (
              <AnimateOnScroll key={i} animation="fadeUp" delay={i * 0.15}>
                <TiltCard className="h-full rounded-2xl border border-gray-100 bg-white p-6 text-center shadow-sm" tiltDegree={6}>
                  <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-gold-100 text-gold-600">
                    {feature.icon}
                  </div>
                  <h3 className="font-heading text-lg font-bold text-vedic-dark">
                    {feature.title}
                  </h3>
                  <p className="mt-2 text-sm text-gray-600">{feature.description}</p>
                </TiltCard>
              </AnimateOnScroll>
            ))}
          </div>
        </Container>
      </section>

      {/* ===== TESTIMONIALS ===== */}
      <section className="vedic-section-dark vedic-hero-gradient">
        <Container>
          <AnimateOnScroll animation="fadeUp">
            <SectionHeading
              subtitle="Testimonials"
              title="What Our Clients Say"
              description="Hear from thousands of satisfied clients who transformed their lives with VedicJivan."
              light
            />
          </AnimateOnScroll>

          <AnimateOnScroll animation="fadeUp" delay={0.2}>
            <TestimonialsCarousel testimonials={testimonials} />
          </AnimateOnScroll>
        </Container>
      </section>

      {/* ===== COURSES PREVIEW ===== */}
      <section className="vedic-section bg-cream">
        <Container>
          <AnimateOnScroll animation="fadeUp">
            <SectionHeading
              subtitle="Learn Astrology"
              title="Master the Ancient Science of Vedic Astrology"
              description="Join thousands of students learning authentic Vedic astrology through our structured courses."
            />
          </AnimateOnScroll>

          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {courses.map((course, i) => (
              <AnimateOnScroll key={i} animation="fadeUp" delay={i * 0.15}>
                <TiltCard className="h-full rounded-2xl border border-gray-100 bg-white p-6 shadow-sm" tiltDegree={5}>
                  <Badge variant="primary" className="mb-3">
                    {course.level}
                  </Badge>
                  <h3 className="font-heading text-xl font-bold text-vedic-dark">
                    {course.title}
                  </h3>
                  <p className="mt-2 text-sm text-gray-600">
                    {course.description}
                  </p>
                  <ul className="mt-4 space-y-2">
                    {course.features.map((feature, j) => (
                      <li key={j} className="flex items-center gap-2 text-sm text-gray-600">
                        <CheckCircle2 className="h-4 w-4 shrink-0 text-green-500" />
                        {feature}
                      </li>
                    ))}
                  </ul>
                  <div className="mt-5 flex items-center justify-between border-t border-gray-100 pt-4">
                    <span className="text-xl font-bold text-primary-600">
                      {course.price}
                    </span>
                    <Link href="/courses">
                      <Button variant="ghost" size="sm">
                        Learn More
                        <ArrowRight className="h-3 w-3" />
                      </Button>
                    </Link>
                  </div>
                </TiltCard>
              </AnimateOnScroll>
            ))}
          </div>
        </Container>
      </section>

      {/* ===== CTA SECTION ===== */}
      <section className="relative overflow-hidden vedic-cta-gradient py-20">
        <FloatingElements />
        <Container className="relative z-10">
          <AnimateOnScroll animation="scaleIn">
            <div className="mx-auto max-w-3xl text-center">
              <h2 className="font-heading text-3xl font-bold text-white sm:text-4xl lg:text-5xl">
                Ready to Know Your Destiny?
              </h2>
              <p className="mx-auto mt-4 max-w-xl text-lg text-primary-200">
                Take the first step towards clarity and guidance. Book a personalized
                consultation with our expert Vedic astrologers today.
              </p>
              <div className="mt-8 flex flex-col items-center justify-center gap-4 sm:flex-row">
                <Link href="/services">
                  <Button variant="gold" size="lg">
                    Book Your Consultation
                    <ArrowRight className="h-5 w-5" />
                  </Button>
                </Link>
                <Link href="/contact">
                  <Button
                    variant="outline"
                    size="lg"
                    className="border-white/30 text-white hover:bg-white/10"
                  >
                    Contact Us
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

/* ===== Static Data (will be replaced with DB data later) ===== */

const services = [
  {
    slug: "call-consultation",
    title: "Call Consultation",
    description:
      "Get personalized astrology guidance over a phone call. Discuss your career, relationships, health, and more.",
    price: "\u20B91,999",
    duration: "30 min",
    icon: <Phone className="h-6 w-6" />,
    image: "https://images.unsplash.com/photo-1655947716360-eee99bc3b056?w=600&q=80",
  },
  {
    slug: "video-consultation",
    title: "Video Consultation",
    description:
      "Face-to-face video session with our expert astrologer. Get detailed analysis with screen-shared birth chart.",
    price: "\u20B92,999",
    duration: "45 min",
    icon: <Video className="h-6 w-6" />,
    image: "https://images.unsplash.com/photo-1521624213010-9fb0f30dcd20?w=600&q=80",
  },
  {
    slug: "premium-kundli",
    title: "Premium Kundli Report",
    description:
      "Comprehensive 40+ page personalized Kundli report covering all aspects of your life — career, marriage, health, and remedies.",
    price: "\u20B94,999",
    duration: null,
    icon: <FileText className="h-6 w-6" />,
    image: "https://images.unsplash.com/photo-1533294455009-a77b7557d2d1?w=600&q=80",
  },
  {
    slug: "numerology-report",
    title: "Numerology Report",
    description:
      "Discover the power of numbers in your life. Get a detailed numerology analysis based on your name and date of birth.",
    price: "\u20B91,499",
    duration: null,
    icon: <Star className="h-6 w-6" />,
    image: "https://images.unsplash.com/photo-1561148493-89acae53e6a1?w=600&q=80",
  },
  {
    slug: "vastu-consultation",
    title: "Vastu Consultation",
    description:
      "Expert Vastu Shastra guidance for your home or office. Optimize your living space for prosperity and well-being.",
    price: "\u20B93,499",
    duration: "60 min",
    icon: <Globe className="h-6 w-6" />,
    image: "https://images.unsplash.com/photo-1628744876490-19b035ecf9c3?w=600&q=80",
  },
  {
    slug: "matchmaking",
    title: "Kundli Matching",
    description:
      "Comprehensive compatibility analysis for marriage. Detailed Guna Milan, Mangal Dosha check, and remedies if needed.",
    price: "\u20B92,499",
    duration: null,
    icon: <Users className="h-6 w-6" />,
    image: "https://images.unsplash.com/photo-1583878545126-2f1ca0142714?w=600&q=80",
  },
];

const wellnessServices = [
  {
    slug: "astrological-consulting",
    title: "Astrological Consulting",
    description:
      "Birth chart analysis, planetary transits, and astrological timing. Personalized guidance for life decisions, relationships, career, and personal growth through cosmic wisdom.",
    icon: <Compass className="h-7 w-7" />,
    image: "https://images.unsplash.com/photo-1444703686981-a3abbc4d4fe3?w=600&q=80",
  },
  {
    slug: "personal-growth-coaching",
    title: "Personal Growth Coaching",
    description:
      "Mindfulness, philosophy, and transformative practices. Guidance for personal development, building resilience, and creating a meaningful life aligned with your values.",
    icon: <Leaf className="h-7 w-7" />,
    image: "https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=600&q=80",
  },
  {
    slug: "therapeutic-healing",
    title: "Therapeutic Healing",
    description:
      "Professional therapeutic support for emotional well-being. Integrated counseling techniques, mindfulness practices, and transformative methodologies for genuine healing.",
    icon: <HeartHandshake className="h-7 w-7" />,
    image: "https://images.unsplash.com/photo-1556760544-74068565f05c?w=600&q=80",
  },
];

const features = [
  {
    icon: <Briefcase className="h-7 w-7" />,
    title: "Comprehensive Services",
    description:
      "9+ specialized services spanning astrology, numerology, Vastu, healing, and personal growth coaching.",
  },
  {
    icon: <Star className="h-7 w-7" />,
    title: "Accurate Predictions",
    description:
      "Time-tested Vedic methods combined with deep planetary analysis for precise readings.",
  },
  {
    icon: <Globe className="h-7 w-7" />,
    title: "Global Clientele",
    description:
      "Trusted by clients across 40+ countries for life-transforming guidance.",
  },
  {
    icon: <Users className="h-7 w-7" />,
    title: "Personalized Approach",
    description:
      "Every consultation is tailored to your unique birth chart and life situation.",
  },
];

const testimonials = [
  {
    name: "Priya Sharma",
    title: "Mumbai, India",
    content:
      "The Kundli report was incredibly detailed and accurate. The remedies suggested for my career helped me land my dream job within 3 months. Highly recommended!",
    rating: 5,
    service: "Premium Kundli Report",
  },
  {
    name: "Rajesh Kumar",
    title: "London, UK",
    content:
      "I was skeptical at first, but the video consultation changed my perspective. The astrologer identified issues I was facing and provided practical solutions.",
    rating: 5,
    service: "Video Consultation",
  },
  {
    name: "Anita Desai",
    title: "New Delhi, India",
    content:
      "The matchmaking service was thorough and gave us complete confidence in our decision. The detailed analysis of both charts was very insightful.",
    rating: 5,
    service: "Kundli Matching",
  },
  {
    name: "Vikram Singh",
    title: "Dubai, UAE",
    content:
      "The Vastu consultation for our new office was a game-changer. Simple changes in arrangement and colors made a noticeable difference in team productivity.",
    rating: 5,
    service: "Vastu Consultation",
  },
  {
    name: "David Morrison",
    title: "Berlin, Germany",
    content:
      "As a European exploring Vedic astrology, I was impressed by how the consultation was tailored to my Western perspective while staying authentic to Vedic traditions.",
    rating: 5,
    service: "Call Consultation",
  },
];

const courses = [
  {
    title: "Vedic Astrology Basics",
    level: "Beginner",
    description:
      "Learn the fundamentals of Vedic astrology — planets, houses, signs, and basic chart reading.",
    price: "\u20B94,999",
    features: ["12 hours of content", "Certificate included", "Lifetime access"],
  },
  {
    title: "Kundli Mastery Course",
    level: "Intermediate",
    description:
      "Deep dive into Kundli reading — Dashas, Yogas, Doshas, transits, and predictive techniques.",
    price: "\u20B99,999",
    features: ["24 hours of content", "Live Q&A sessions", "Practice charts"],
  },
  {
    title: "Professional Numerology",
    level: "Beginner",
    description:
      "Master the science of numbers. Learn name correction, lucky numbers, and business numerology.",
    price: "\u20B93,999",
    features: ["8 hours of content", "Real case studies", "Certificate included"],
  },
];
