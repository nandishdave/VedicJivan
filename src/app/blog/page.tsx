import type { Metadata } from "next";
import Link from "next/link";
import { ArrowRight, Calendar, Clock, Tag } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { Button } from "@/components/ui/Button";
import { Card, CardContent } from "@/components/ui/Card";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { Badge } from "@/components/ui/Badge";
import { AnimateOnScroll } from "@/components/ui/AnimateOnScroll";
import { FloatingElements } from "@/components/ui/FloatingElements";
import { GradientText } from "@/components/ui/GradientText";
import { blogPosts, blogCategories } from "@/data/blog";

export const metadata: Metadata = {
  title: "Blog",
  description:
    "Explore articles on Vedic astrology, numerology, Vastu Shastra, planetary transits, and spiritual wisdom from VedicJivan.",
  alternates: { canonical: "/blog" },
  openGraph: {
    title: "Blog | VedicJivan",
    description:
      "Explore articles on Vedic astrology, numerology, Vastu Shastra, planetary transits, and spiritual wisdom from VedicJivan.",
    url: "/blog",
  },
};

export default function BlogPage() {
  const featured = blogPosts.find((p) => p.featured);
  const regularPosts = blogPosts.filter((p) => !p.featured);

  return (
    <>
      {/* ===== HERO ===== */}
      <section className="relative overflow-hidden vedic-hero-gradient py-20 sm:py-28">
        <FloatingElements />
        <Container className="relative z-10">
          <AnimateOnScroll animation="fadeIn">
            <div className="mx-auto max-w-3xl text-center">
              <span className="mb-3 inline-block text-sm font-semibold uppercase tracking-widest text-gold-400">
                VedicJivan Blog
              </span>
              <h1 className="font-heading text-4xl font-bold text-white sm:text-5xl lg:text-6xl">
                Wisdom, Insights &{" "}
                <GradientText variant="gold">Guidance</GradientText>
              </h1>
              <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-300">
                Explore articles on Vedic astrology, planetary transits,
                remedies, numerology, and more. Deepen your understanding of
                the cosmic influences in your life.
              </p>
            </div>
          </AnimateOnScroll>
        </Container>
      </section>

      {/* ===== CATEGORIES ===== */}
      <section className="border-b border-gray-100 bg-white py-4">
        <Container>
          <div className="flex flex-wrap gap-2">
            {blogCategories.map((cat) => (
              <button
                key={cat}
                className={`rounded-full px-4 py-1.5 text-sm font-medium transition-colors ${
                  cat === "All"
                    ? "bg-primary-600 text-white"
                    : "bg-gray-100 text-gray-600 hover:bg-primary-50 hover:text-primary-600"
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </Container>
      </section>

      {/* ===== FEATURED POST ===== */}
      {featured && (
        <section className="vedic-section bg-cream">
          <Container>
            <AnimateOnScroll animation="fadeUp">
              <Link href={`/blog/${featured.slug}`}>
                <div className="group overflow-hidden rounded-2xl border border-gray-100 bg-white shadow-sm transition-all hover:shadow-lg">
                  <div className="grid lg:grid-cols-2">
                    <div className="flex h-48 items-center justify-center bg-gradient-to-br from-primary-100 to-gold-100 lg:h-full">
                      <span className="font-heading text-6xl text-primary-200">
                        {featured.title.charAt(0)}
                      </span>
                    </div>
                    <div className="p-8 lg:p-10">
                      <Badge variant="gold">Featured</Badge>
                      <h2 className="mt-4 font-heading text-2xl font-bold text-vedic-dark transition-colors group-hover:text-primary-600 sm:text-3xl">
                        {featured.title}
                      </h2>
                      <p className="mt-3 text-gray-600">{featured.excerpt}</p>
                      <div className="mt-6 flex flex-wrap items-center gap-4 text-sm text-gray-500">
                        <span className="flex items-center gap-1">
                          <Calendar className="h-4 w-4" />
                          {new Date(featured.date).toLocaleDateString("en-IN", {
                            day: "numeric",
                            month: "long",
                            year: "numeric",
                          })}
                        </span>
                        <span className="flex items-center gap-1">
                          <Clock className="h-4 w-4" />
                          {featured.readTime}
                        </span>
                        <span className="flex items-center gap-1">
                          <Tag className="h-4 w-4" />
                          {featured.category}
                        </span>
                      </div>
                      <div className="mt-6">
                        <Button variant="primary" size="sm">
                          Read Article
                          <ArrowRight className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  </div>
                </div>
              </Link>
            </AnimateOnScroll>
          </Container>
        </section>
      )}

      {/* ===== ALL POSTS ===== */}
      <section className="vedic-section">
        <Container>
          <AnimateOnScroll animation="fadeUp">
            <SectionHeading
              subtitle="Latest Articles"
              title="Expand Your Knowledge"
            />
          </AnimateOnScroll>

          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {regularPosts.map((post, i) => (
              <AnimateOnScroll key={post.slug} animation="fadeUp" delay={i * 0.08}>
                <Link href={`/blog/${post.slug}`}>
                  <Card className="group h-full cursor-pointer">
                    <div className="flex h-40 items-center justify-center rounded-t-2xl bg-gradient-to-br from-primary-50 to-gold-50">
                      <span className="font-heading text-5xl text-primary-200">
                        {post.title.charAt(0)}
                      </span>
                    </div>
                    <CardContent className="pt-4">
                      <Badge variant="primary" className="mb-2">
                        {post.category}
                      </Badge>
                      <h3 className="font-heading text-lg font-bold text-vedic-dark transition-colors group-hover:text-primary-600">
                        {post.title}
                      </h3>
                      <p className="mt-2 line-clamp-2 text-sm text-gray-600">
                        {post.excerpt}
                      </p>
                      <div className="mt-4 flex items-center justify-between text-xs text-gray-500">
                        <span>
                          {new Date(post.date).toLocaleDateString("en-IN", {
                            day: "numeric",
                            month: "short",
                            year: "numeric",
                          })}
                        </span>
                        <span>{post.readTime}</span>
                      </div>
                    </CardContent>
                  </Card>
                </Link>
              </AnimateOnScroll>
            ))}
          </div>
        </Container>
      </section>

      {/* ===== CTA ===== */}
      <section className="relative overflow-hidden vedic-cta-gradient py-20">
        <Container className="relative z-10">
          <AnimateOnScroll animation="scaleIn">
            <div className="mx-auto max-w-3xl text-center">
              <h2 className="font-heading text-3xl font-bold text-white sm:text-4xl">
                Want Personalized Guidance?
              </h2>
              <p className="mx-auto mt-4 max-w-xl text-lg text-primary-200">
                While our blog offers general insights, a personal consultation
                provides answers tailored specifically to your birth chart.
              </p>
              <div className="mt-8">
                <Link href="/services">
                  <Button variant="gold" size="lg">
                    Book a Consultation
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
