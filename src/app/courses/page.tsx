import type { Metadata } from "next";
import Link from "next/link";
import {
  ArrowRight,
  BookOpen,
  Clock,
  Star,
  Users,
  CheckCircle2,
} from "lucide-react";
import { Container } from "@/components/ui/Container";
import { Button } from "@/components/ui/Button";
import { Card, CardContent } from "@/components/ui/Card";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Badge } from "@/components/ui/Badge";
import { AnimateOnScroll } from "@/components/ui/AnimateOnScroll";
import { FloatingElements } from "@/components/ui/FloatingElements";
import { courses } from "@/data/courses";

export const metadata: Metadata = {
  title: "Courses",
  description:
    "Learn Vedic astrology, numerology, and Vastu Shastra from expert instructors. Structured courses for beginners to advanced learners.",
  alternates: { canonical: "/courses" },
  openGraph: {
    title: "Courses | VedicJivan",
    description:
      "Learn Vedic astrology, numerology, and Vastu Shastra from expert instructors. Structured courses for beginners to advanced learners.",
    url: "/courses",
  },
};

export default function CoursesPage() {
  return (
    <>
      {/* ===== HERO ===== */}
      <section className="relative overflow-hidden bg-dark-gradient py-20 sm:py-28">
        <FloatingElements />
        <Container className="relative z-10">
          <AnimateOnScroll animation="fadeIn">
            <div className="mx-auto max-w-3xl text-center">
              <span className="mb-3 inline-block text-sm font-semibold uppercase tracking-widest text-gold-400">
                Learn From Experts
              </span>
              <h1 className="font-heading text-4xl font-bold text-white sm:text-5xl lg:text-6xl">
                Master the Ancient{" "}
                <span className="text-gradient-gold">Vedic Sciences</span>
              </h1>
              <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-300">
                Structured, comprehensive courses in Vedic astrology, numerology,
                and Vastu Shastra. Learn at your own pace with lifetime access.
              </p>
            </div>
          </AnimateOnScroll>

          {/* Quick Stats */}
          <AnimateOnScroll animation="fadeUp" delay={0.3}>
            <div className="mx-auto mt-12 grid max-w-2xl grid-cols-3 gap-6">
              <div className="text-center">
                <p className="font-heading text-2xl font-bold text-gold-400">4</p>
                <p className="mt-1 text-sm text-gray-400">Courses</p>
              </div>
              <div className="text-center">
                <p className="font-heading text-2xl font-bold text-gold-400">2,000+</p>
                <p className="mt-1 text-sm text-gray-400">Students</p>
              </div>
              <div className="text-center">
                <p className="font-heading text-2xl font-bold text-gold-400">4.8</p>
                <p className="mt-1 text-sm text-gray-400">Avg Rating</p>
              </div>
            </div>
          </AnimateOnScroll>
        </Container>
      </section>

      {/* ===== COURSES GRID ===== */}
      <section className="vedic-section">
        <Container>
          <AnimateOnScroll animation="fadeUp">
            <SectionHeading
              subtitle="Our Courses"
              title="Choose Your Learning Path"
              description="Whether you're a complete beginner or looking to deepen your expertise, we have a course for you."
            />
          </AnimateOnScroll>

          <div className="grid gap-8 lg:grid-cols-2">
            {courses.map((course, i) => (
              <AnimateOnScroll key={course.slug} animation="fadeUp" delay={i * 0.1}>
                <Card className="group h-full">
                  <CardContent>
                    <div className="flex flex-wrap items-start gap-2">
                      <Badge variant="primary">{course.level}</Badge>
                      <Badge variant="gold">{course.category}</Badge>
                    </div>

                    <h3 className="mt-4 font-heading text-2xl font-bold text-vedic-dark">
                      {course.title}
                    </h3>
                    <p className="mt-2 text-sm leading-relaxed text-gray-600">
                      {course.shortDescription}
                    </p>

                    <div className="mt-4 flex flex-wrap gap-4 text-sm text-gray-500">
                      <span className="flex items-center gap-1">
                        <Clock className="h-4 w-4" />
                        {course.duration}
                      </span>
                      <span className="flex items-center gap-1">
                        <BookOpen className="h-4 w-4" />
                        {course.lessons} lessons
                      </span>
                      <span className="flex items-center gap-1">
                        <Users className="h-4 w-4" />
                        {course.students.toLocaleString()} students
                      </span>
                      <span className="flex items-center gap-1">
                        <Star className="h-4 w-4 fill-gold-400 text-gold-400" />
                        {course.rating}
                      </span>
                    </div>

                    <ul className="mt-4 space-y-2">
                      {course.features.slice(0, 3).map((feature, j) => (
                        <li
                          key={j}
                          className="flex items-center gap-2 text-sm text-gray-600"
                        >
                          <CheckCircle2 className="h-4 w-4 shrink-0 text-green-500" />
                          {feature}
                        </li>
                      ))}
                    </ul>

                    <div className="mt-6 flex items-center justify-between border-t border-gray-100 pt-4">
                      <div>
                        <span className="text-2xl font-bold text-primary-600">
                          {course.priceINR}
                        </span>
                        <span className="ml-2 text-sm text-gray-400">
                          {course.priceEUR}
                        </span>
                      </div>
                      <Link href={`/courses/${course.slug}`}>
                        <Button variant="primary" size="sm">
                          View Details
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

      {/* ===== WHY LEARN WITH US ===== */}
      <section className="vedic-section bg-cream">
        <Container>
          <AnimateOnScroll animation="fadeUp">
            <SectionHeading
              subtitle="Why VedicJivan"
              title="Why Learn With Us?"
            />
          </AnimateOnScroll>

          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {benefits.map((b, i) => (
              <AnimateOnScroll key={i} animation="fadeUp" delay={i * 0.1}>
                <div className="text-center">
                  <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-primary-100 text-primary-600">
                    {b.icon}
                  </div>
                  <h3 className="font-heading text-lg font-bold text-vedic-dark">
                    {b.title}
                  </h3>
                  <p className="mt-2 text-sm text-gray-600">{b.description}</p>
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
                Begin Your Journey Into Vedic Sciences
              </h2>
              <p className="mx-auto mt-4 max-w-xl text-lg text-primary-200">
                Join thousands of students worldwide who are learning the ancient
                art and science of Vedic astrology with VedicJivan.
              </p>
              <div className="mt-8">
                <Link href="/contact">
                  <Button variant="gold" size="lg">
                    Have Questions? Contact Us
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

const benefits = [
  {
    icon: <BookOpen className="h-6 w-6" />,
    title: "Expert Instructors",
    description:
      "Learn from practicing astrologers with 15+ years of real-world experience.",
  },
  {
    icon: <Clock className="h-6 w-6" />,
    title: "Lifetime Access",
    description:
      "Once enrolled, access your course materials anytime, forever.",
  },
  {
    icon: <Star className="h-6 w-6" />,
    title: "Certification",
    description:
      "Receive a recognized certificate of completion for every course.",
  },
  {
    icon: <Users className="h-6 w-6" />,
    title: "Community",
    description:
      "Join a vibrant community of learners and get your doubts resolved.",
  },
];
