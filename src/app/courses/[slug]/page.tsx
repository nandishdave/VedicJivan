import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import {
  ArrowRight,
  BookOpen,
  Clock,
  Star,
  Users,
  CheckCircle2,
  ChevronDown,
  Award,
  Play,
} from "lucide-react";
import { Container } from "@/components/ui/Container";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { AnimateOnScroll } from "@/components/ui/AnimateOnScroll";
import { courses, getCourseBySlug } from "@/data/courses";
import { CourseJsonLd, BreadcrumbJsonLd } from "@/components/seo/JsonLd";

export function generateStaticParams() {
  return courses.map((c) => ({ slug: c.slug }));
}

export function generateMetadata({
  params,
}: {
  params: { slug: string };
}): Metadata {
  const course = getCourseBySlug(params.slug);
  if (!course) return { title: "Course Not Found" };

  return {
    title: course.title,
    description: course.shortDescription,
    alternates: {
      canonical: `/courses/${params.slug}`,
    },
    openGraph: {
      title: course.title,
      description: course.shortDescription,
      type: "website",
      url: `/courses/${params.slug}`,
    },
  };
}

export default function CourseDetailPage({
  params,
}: {
  params: { slug: string };
}) {
  const course = getCourseBySlug(params.slug);
  if (!course) notFound();

  const totalLessons = course.curriculum.reduce(
    (acc, m) => acc + m.lessons.length,
    0
  );

  const BASE_URL = "https://vedicjivan.nandishdave.world";

  return (
    <>
      <CourseJsonLd
        name={course.title}
        description={course.shortDescription}
        priceINR={course.priceINR}
        url={`${BASE_URL}/courses/${course.slug}`}
      />
      <BreadcrumbJsonLd
        items={[
          { name: "Home", url: BASE_URL },
          { name: "Courses", url: `${BASE_URL}/courses` },
          { name: course.title, url: `${BASE_URL}/courses/${course.slug}` },
        ]}
      />

      {/* ===== HERO ===== */}
      <section className="relative overflow-hidden vedic-hero-gradient py-16 sm:py-24">
        <div className="pointer-events-none absolute inset-0 opacity-10">
          <div className="absolute -left-40 top-0 h-80 w-80 rounded-full bg-primary-500 blur-3xl" />
        </div>
        <Container className="relative z-10">
          <AnimateOnScroll animation="fadeIn">
            <div className="mx-auto max-w-5xl">
              <Link
                href="/courses"
                className="mb-6 inline-flex items-center gap-1 text-sm text-gray-400 hover:text-gold-400"
              >
                <ArrowRight className="h-3 w-3 rotate-180" />
                All Courses
              </Link>

              <div className="grid gap-8 lg:grid-cols-3">
                <div className="lg:col-span-2">
                  <div className="flex flex-wrap gap-2">
                    <Badge variant="primary">{course.level}</Badge>
                    <Badge variant="gold">{course.category}</Badge>
                  </div>

                  <h1 className="mt-4 font-heading text-3xl font-bold text-white sm:text-4xl lg:text-5xl">
                    {course.title}
                  </h1>
                  <p className="mt-4 text-lg text-gray-300">
                    {course.shortDescription}
                  </p>

                  <div className="mt-6 flex flex-wrap gap-6 text-sm text-gray-400">
                    <span className="flex items-center gap-1.5">
                      <Clock className="h-4 w-4" />
                      {course.duration}
                    </span>
                    <span className="flex items-center gap-1.5">
                      <BookOpen className="h-4 w-4" />
                      {totalLessons} lessons
                    </span>
                    <span className="flex items-center gap-1.5">
                      <Users className="h-4 w-4" />
                      {course.students.toLocaleString()} students
                    </span>
                    <span className="flex items-center gap-1.5">
                      <Star className="h-4 w-4 fill-gold-400 text-gold-400" />
                      {course.rating} rating
                    </span>
                  </div>
                </div>

                {/* Pricing Card */}
                <div className="rounded-2xl border border-white/10 bg-white/5 p-8 backdrop-blur-sm">
                  <p className="text-sm text-gray-400">Course Fee</p>
                  <p className="mt-1 font-heading text-4xl font-bold text-white">
                    {course.priceINR}
                  </p>
                  <p className="text-sm text-gray-400">{course.priceEUR}</p>

                  <Button variant="gold" size="lg" className="mt-6 w-full">
                    Enroll Now
                    <ArrowRight className="h-5 w-5" />
                  </Button>

                  <ul className="mt-6 space-y-3">
                    {course.features.map((f, i) => (
                      <li
                        key={i}
                        className="flex items-center gap-2 text-sm text-gray-300"
                      >
                        <CheckCircle2 className="h-4 w-4 shrink-0 text-green-400" />
                        {f}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          </AnimateOnScroll>
        </Container>
      </section>

      {/* ===== WHAT YOU'LL LEARN ===== */}
      <section className="vedic-section">
        <Container>
          <div className="mx-auto max-w-4xl">
            <AnimateOnScroll animation="fadeUp">
              <h2 className="font-heading text-2xl font-bold text-vedic-dark sm:text-3xl">
                What You&apos;ll Learn
              </h2>
              <div className="mt-6 grid gap-3 sm:grid-cols-2">
                {course.whatYouLearn.map((item, i) => (
                  <div
                    key={i}
                    className="flex items-start gap-3 rounded-xl border border-gray-100 bg-cream p-4"
                  >
                    <CheckCircle2 className="mt-0.5 h-5 w-5 shrink-0 text-primary-600" />
                    <p className="text-sm text-gray-700">{item}</p>
                  </div>
                ))}
              </div>
            </AnimateOnScroll>

            {/* Description */}
            <AnimateOnScroll animation="fadeUp" delay={0.2}>
              <div className="mt-12">
                <h2 className="font-heading text-2xl font-bold text-vedic-dark sm:text-3xl">
                  Course Description
                </h2>
                <p className="mt-4 leading-relaxed text-gray-600">
                  {course.description}
                </p>
              </div>
            </AnimateOnScroll>
          </div>
        </Container>
      </section>

      {/* ===== CURRICULUM ===== */}
      <section className="vedic-section bg-cream">
        <Container>
          <div className="mx-auto max-w-4xl">
            <AnimateOnScroll animation="fadeUp">
              <h2 className="mb-2 font-heading text-2xl font-bold text-vedic-dark sm:text-3xl">
                Course Curriculum
              </h2>
              <p className="mb-8 text-gray-600">
                {course.curriculum.length} modules &middot; {totalLessons} lessons
                &middot; {course.duration} total
              </p>
            </AnimateOnScroll>

            <div className="space-y-4">
              {course.curriculum.map((module, i) => (
                <AnimateOnScroll key={i} animation="fadeUp" delay={i * 0.08}>
                  <details className="group rounded-2xl border border-gray-200 bg-white" open={i === 0}>
                    <summary className="flex cursor-pointer items-center justify-between p-5">
                      <div className="flex items-center gap-3">
                        <span className="flex h-8 w-8 items-center justify-center rounded-full bg-primary-100 text-sm font-bold text-primary-600">
                          {i + 1}
                        </span>
                        <div>
                          <h3 className="font-semibold text-vedic-dark">
                            {module.module}
                          </h3>
                          <p className="text-xs text-gray-500">
                            {module.lessons.length} lessons
                          </p>
                        </div>
                      </div>
                      <ChevronDown className="h-5 w-5 shrink-0 text-gray-400 transition-transform group-open:rotate-180" />
                    </summary>
                    <div className="border-t border-gray-100 px-5 pb-5 pt-3">
                      <ul className="space-y-2">
                        {module.lessons.map((lesson, j) => (
                          <li
                            key={j}
                            className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm text-gray-600 hover:bg-gray-50"
                          >
                            <Play className="h-3.5 w-3.5 shrink-0 text-primary-400" />
                            {lesson}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </details>
                </AnimateOnScroll>
              ))}
            </div>
          </div>
        </Container>
      </section>

      {/* ===== INSTRUCTOR ===== */}
      <section className="vedic-section">
        <Container>
          <div className="mx-auto max-w-4xl">
            <AnimateOnScroll animation="fadeUp">
              <h2 className="mb-8 font-heading text-2xl font-bold text-vedic-dark sm:text-3xl">
                Your Instructor
              </h2>
              <div className="flex flex-col gap-6 rounded-2xl border border-gray-100 bg-white p-8 shadow-sm sm:flex-row">
                <div className="flex h-20 w-20 shrink-0 items-center justify-center rounded-full bg-primary-100 text-primary-600">
                  <Award className="h-8 w-8" />
                </div>
                <div>
                  <h3 className="font-heading text-xl font-bold text-vedic-dark">
                    VedicJivan Astrology Team
                  </h3>
                  <p className="mt-1 text-sm text-gold-600">
                    Jyotish Acharya &middot; 15+ Years Experience
                  </p>
                  <p className="mt-3 leading-relaxed text-gray-600">
                    Our courses are crafted by our team of experienced Vedic
                    astrologers who have trained under traditional Guru-Shishya
                    parampara. With over 50,000 consultations and 15+ years of
                    practice, they bring a wealth of real-world experience to
                    every lesson.
                  </p>
                </div>
              </div>
            </AnimateOnScroll>
          </div>
        </Container>
      </section>

      {/* ===== CTA ===== */}
      <section className="relative overflow-hidden vedic-cta-gradient py-16">
        <Container className="relative z-10">
          <AnimateOnScroll animation="scaleIn">
            <div className="mx-auto max-w-3xl text-center">
              <h2 className="font-heading text-3xl font-bold text-white sm:text-4xl">
                Start Learning Today
              </h2>
              <p className="mx-auto mt-4 max-w-xl text-lg text-primary-200">
                Enroll in {course.title} and begin your journey into the world
                of Vedic sciences.
              </p>
              <div className="mt-8 flex flex-col items-center justify-center gap-4 sm:flex-row">
                <Button variant="gold" size="lg">
                  Enroll Now — {course.priceINR}
                  <ArrowRight className="h-5 w-5" />
                </Button>
                <Link href="/courses">
                  <Button
                    variant="outline"
                    size="lg"
                    className="border-white/30 text-white hover:bg-white/10"
                  >
                    Browse All Courses
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
