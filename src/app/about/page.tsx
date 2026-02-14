import type { Metadata } from "next";
import Link from "next/link";
import {
  Award,
  BookOpen,
  Globe,
  Heart,
  Star,
  Users,
  ArrowRight,
  CheckCircle2,
} from "lucide-react";
import { Container } from "@/components/ui/Container";
import { Button } from "@/components/ui/Button";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { AnimateOnScroll } from "@/components/ui/AnimateOnScroll";
import { AnimatedText } from "@/components/ui/AnimatedText";
import { FloatingElements } from "@/components/ui/FloatingElements";
import { TiltCard } from "@/components/ui/TiltCard";

export const metadata: Metadata = {
  title: "About Us",
  description:
    "Learn about VedicJivan's journey, philosophy, and mission to bring authentic Vedic astrology wisdom to seekers worldwide.",
  alternates: { canonical: "/about" },
  openGraph: {
    title: "About Us | VedicJivan",
    description:
      "Learn about VedicJivan's journey, philosophy, and mission to bring authentic Vedic astrology wisdom to seekers worldwide.",
    url: "/about",
  },
};

export default function AboutPage() {
  return (
    <>
      {/* ===== HERO ===== */}
      <section className="relative overflow-hidden bg-dark-gradient py-20 sm:py-28">
        <FloatingElements />
        <Container className="relative z-10">
          <AnimateOnScroll animation="fadeIn">
            <div className="mx-auto max-w-3xl text-center">
              <span className="mb-3 inline-block text-sm font-semibold uppercase tracking-widest text-gold-400">
                About VedicJivan
              </span>
              <AnimatedText
                text="Guiding Lives Through Ancient Wisdom"
                className="justify-center text-4xl font-bold text-white sm:text-5xl lg:text-6xl"
              />
              <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-300">
                For over 15 years, VedicJivan has been a trusted name in Vedic
                astrology, helping thousands of individuals across 40+ countries
                find clarity, direction, and purpose in their lives.
              </p>
            </div>
          </AnimateOnScroll>
        </Container>
      </section>

      {/* ===== OUR STORY ===== */}
      <section className="vedic-section">
        <Container>
          <div className="grid items-center gap-12 lg:grid-cols-2">
            <AnimateOnScroll animation="fadeLeft">
              <div>
                <span className="mb-3 inline-block text-sm font-semibold uppercase tracking-widest text-gold-600">
                  Our Story
                </span>
                <h2 className="font-heading text-3xl font-bold text-vedic-dark sm:text-4xl">
                  A Legacy of Vedic Knowledge
                </h2>
                <div className="mt-6 space-y-4 text-gray-600">
                  <p>
                    VedicJivan was founded with a simple yet profound mission — to
                    make the timeless wisdom of Vedic astrology accessible to every
                    seeker, regardless of where they are in the world.
                  </p>
                  <p>
                    Our founder, trained in the traditional Guru-Shishya parampara
                    (teacher-student lineage), spent years studying ancient texts
                    including Brihat Parashara Hora Shastra, Jataka Parijata, and
                    Phaladeepika under the guidance of renowned Jyotish masters.
                  </p>
                  <p>
                    What started as personal consultations for a small community
                    has grown into a global platform serving clients across India,
                    Europe, the Middle East, and North America. Today, VedicJivan
                    combines the authenticity of ancient Vedic methods with the
                    convenience of modern technology.
                  </p>
                </div>
              </div>
            </AnimateOnScroll>

            <AnimateOnScroll animation="fadeRight">
              <div className="grid grid-cols-2 gap-4">
                {stats.map((stat, i) => (
                  <TiltCard
                    key={i}
                    className="rounded-2xl border border-gray-100 bg-white p-6 text-center shadow-sm"
                    tiltDegree={6}
                  >
                    <div className="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-full bg-primary-100 text-primary-600">
                      {stat.icon}
                    </div>
                    <p className="font-heading text-2xl font-bold text-vedic-dark">
                      {stat.value}
                    </p>
                    <p className="mt-1 text-sm text-gray-500">{stat.label}</p>
                  </TiltCard>
                ))}
              </div>
            </AnimateOnScroll>
          </div>
        </Container>
      </section>

      {/* ===== JOURNEY / TIMELINE ===== */}
      <section className="vedic-section bg-cream">
        <Container>
          <AnimateOnScroll animation="fadeUp">
            <SectionHeading
              subtitle="Our Journey"
              title="Milestones That Shaped VedicJivan"
            />
          </AnimateOnScroll>

          <div className="mx-auto max-w-3xl">
            {timeline.map((item, i) => (
              <AnimateOnScroll key={i} animation="fadeUp" delay={i * 0.1}>
                <div className="relative flex gap-6 pb-10 last:pb-0">
                  {/* Timeline line */}
                  <div className="flex flex-col items-center">
                    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-primary-600 text-sm font-bold text-white">
                      {item.year.slice(-2)}
                    </div>
                    {i < timeline.length - 1 && (
                      <div className="w-0.5 flex-1 bg-primary-200" />
                    )}
                  </div>
                  <div className="pb-2">
                    <span className="text-sm font-semibold text-gold-600">
                      {item.year}
                    </span>
                    <h3 className="mt-1 font-heading text-lg font-bold text-vedic-dark">
                      {item.title}
                    </h3>
                    <p className="mt-1 text-sm text-gray-600">
                      {item.description}
                    </p>
                  </div>
                </div>
              </AnimateOnScroll>
            ))}
          </div>
        </Container>
      </section>

      {/* ===== PHILOSOPHY ===== */}
      <section className="vedic-section">
        <Container>
          <AnimateOnScroll animation="fadeUp">
            <SectionHeading
              subtitle="Our Philosophy"
              title="What We Believe In"
              description="At VedicJivan, our approach is rooted in authenticity, empathy, and a deep respect for the ancient science of Jyotish."
            />
          </AnimateOnScroll>

          <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
            {philosophies.map((item, i) => (
              <AnimateOnScroll key={i} animation="fadeUp" delay={i * 0.1}>
                <div className="rounded-2xl border border-gray-100 bg-white p-8 shadow-sm">
                  <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-xl bg-gold-100 text-gold-600">
                    {item.icon}
                  </div>
                  <h3 className="font-heading text-xl font-bold text-vedic-dark">
                    {item.title}
                  </h3>
                  <p className="mt-3 text-sm leading-relaxed text-gray-600">
                    {item.description}
                  </p>
                </div>
              </AnimateOnScroll>
            ))}
          </div>
        </Container>
      </section>

      {/* ===== CREDENTIALS ===== */}
      <section className="vedic-section-dark">
        <Container>
          <AnimateOnScroll animation="fadeUp">
            <SectionHeading
              subtitle="Credentials"
              title="Recognized Excellence in Vedic Astrology"
              light
            />
          </AnimateOnScroll>

          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {credentials.map((item, i) => (
              <AnimateOnScroll key={i} animation="fadeUp" delay={i * 0.1}>
                <div className="flex items-start gap-4 rounded-xl border border-white/10 bg-white/5 p-6 backdrop-blur-sm">
                  <CheckCircle2 className="mt-0.5 h-5 w-5 shrink-0 text-gold-400" />
                  <div>
                    <h4 className="font-semibold text-white">{item.title}</h4>
                    <p className="mt-1 text-sm text-gray-400">
                      {item.description}
                    </p>
                  </div>
                </div>
              </AnimateOnScroll>
            ))}
          </div>
        </Container>
      </section>

      {/* ===== CTA ===== */}
      <section className="relative overflow-hidden bg-vedic-gradient py-20">
        <Container className="relative z-10">
          <AnimateOnScroll animation="scaleIn">
            <div className="mx-auto max-w-3xl text-center">
              <h2 className="font-heading text-3xl font-bold text-white sm:text-4xl">
                Ready to Begin Your Journey?
              </h2>
              <p className="mx-auto mt-4 max-w-xl text-lg text-primary-200">
                Whether you seek answers about your career, relationships, or
                life path — we&apos;re here to guide you with authentic Vedic wisdom.
              </p>
              <div className="mt-8 flex flex-col items-center justify-center gap-4 sm:flex-row">
                <Link href="/services">
                  <Button variant="gold" size="lg">
                    Explore Our Services
                    <ArrowRight className="h-5 w-5" />
                  </Button>
                </Link>
                <Link href="/contact">
                  <Button
                    variant="outline"
                    size="lg"
                    className="border-white/30 text-white hover:bg-white/10"
                  >
                    Get In Touch
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

/* ===== Static Data ===== */

const stats = [
  {
    icon: <Users className="h-5 w-5" />,
    value: "50,000+",
    label: "Consultations",
  },
  { icon: <Globe className="h-5 w-5" />, value: "40+", label: "Countries" },
  {
    icon: <BookOpen className="h-5 w-5" />,
    value: "15+",
    label: "Years Experience",
  },
  { icon: <Award className="h-5 w-5" />, value: "10+", label: "Awards" },
];

const timeline = [
  {
    year: "2009",
    title: "The Beginning",
    description:
      "Started offering personal Vedic astrology consultations to the local community, following years of rigorous study under traditional Jyotish gurus.",
  },
  {
    year: "2013",
    title: "Going Online",
    description:
      "Launched phone and video consultations, reaching clients across India. Started the first batch of astrology students.",
  },
  {
    year: "2016",
    title: "International Expansion",
    description:
      "Expanded services to serve the Indian diaspora in the UK, USA, and Middle East. Crossed 10,000 consultations.",
  },
  {
    year: "2019",
    title: "Course Platform Launch",
    description:
      "Launched structured online courses in Vedic astrology, numerology, and Vastu Shastra. Over 1,000 students enrolled in the first year.",
  },
  {
    year: "2022",
    title: "50,000+ Consultations",
    description:
      "Crossed the milestone of 50,000 consultations spanning 40+ countries. Received multiple awards for excellence in Vedic astrology.",
  },
  {
    year: "2024",
    title: "VedicJivan Platform",
    description:
      "Launched the VedicJivan digital platform — a complete destination for consultations, courses, reports, and Vedic wisdom content.",
  },
];

const philosophies = [
  {
    icon: <BookOpen className="h-6 w-6" />,
    title: "Rooted in Scriptures",
    description:
      "Every prediction and analysis is based on classical Vedic texts — Parashara, Jaimini, and Nadi systems — not generic interpretations.",
  },
  {
    icon: <Heart className="h-6 w-6" />,
    title: "Empathy First",
    description:
      "We understand that people come to astrology during vulnerable moments. Our consultations are conducted with care, sensitivity, and confidentiality.",
  },
  {
    icon: <Star className="h-6 w-6" />,
    title: "Actionable Guidance",
    description:
      "We don't just predict — we provide practical remedies and actionable steps that you can implement in your daily life.",
  },
  {
    icon: <Users className="h-6 w-6" />,
    title: "Personalized Approach",
    description:
      "No two charts are alike. Every consultation is uniquely tailored to your birth chart, current Dashas, and specific life questions.",
  },
  {
    icon: <Globe className="h-6 w-6" />,
    title: "Modern Accessibility",
    description:
      "Ancient wisdom, delivered through modern technology. Consult from anywhere via phone, video, or detailed written reports.",
  },
  {
    icon: <Award className="h-6 w-6" />,
    title: "Continuous Learning",
    description:
      "Our astrologers are lifelong students of Jyotish, constantly studying, researching, and refining their knowledge and techniques.",
  },
];

const credentials = [
  {
    title: "Jyotish Acharya Certification",
    description: "Advanced degree in Vedic Astrology from a recognized institution.",
  },
  {
    title: "15+ Years of Practice",
    description:
      "Over a decade and a half of dedicated practice in Vedic astrology and allied sciences.",
  },
  {
    title: "50,000+ Consultations",
    description:
      "A track record of helping tens of thousands of clients across the globe.",
  },
  {
    title: "10+ Industry Awards",
    description:
      "Recognized by leading astrology organizations for accuracy and service excellence.",
  },
  {
    title: "Published Author",
    description:
      "Articles and research published in leading astrology journals and magazines.",
  },
  {
    title: "Global Speaker",
    description:
      "Invited speaker at astrology conferences and seminars in India and abroad.",
  },
];
