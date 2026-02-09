import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import {
  ArrowRight,
  ArrowLeft,
  Calendar,
  Clock,
  Tag,
  Share2,
} from "lucide-react";
import { Container } from "@/components/ui/Container";
import { Button } from "@/components/ui/Button";
import { Card, CardContent } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { AnimateOnScroll } from "@/components/ui/AnimateOnScroll";
import { blogPosts, getBlogPostBySlug, getRelatedPosts } from "@/data/blog";

export function generateStaticParams() {
  return blogPosts.map((p) => ({ slug: p.slug }));
}

export function generateMetadata({
  params,
}: {
  params: { slug: string };
}): Metadata {
  const post = getBlogPostBySlug(params.slug);
  if (!post) return { title: "Post Not Found" };

  return {
    title: post.title,
    description: post.excerpt,
  };
}

export default function BlogPostPage({
  params,
}: {
  params: { slug: string };
}) {
  const post = getBlogPostBySlug(params.slug);
  if (!post) notFound();

  const related = getRelatedPosts(params.slug);

  return (
    <>
      {/* ===== HEADER ===== */}
      <section className="relative overflow-hidden bg-dark-gradient py-16 sm:py-24">
        <div className="pointer-events-none absolute inset-0 opacity-10">
          <div className="absolute -left-40 top-0 h-80 w-80 rounded-full bg-primary-500 blur-3xl" />
        </div>
        <Container className="relative z-10">
          <AnimateOnScroll animation="fadeIn">
            <div className="mx-auto max-w-3xl">
              <Link
                href="/blog"
                className="mb-6 inline-flex items-center gap-1 text-sm text-gray-400 hover:text-gold-400"
              >
                <ArrowLeft className="h-3 w-3" />
                Back to Blog
              </Link>

              <Badge variant="gold" className="mb-4">
                {post.category}
              </Badge>

              <h1 className="font-heading text-3xl font-bold text-white sm:text-4xl lg:text-5xl">
                {post.title}
              </h1>

              <div className="mt-6 flex flex-wrap items-center gap-4 text-sm text-gray-400">
                <span className="flex items-center gap-1.5">
                  <Calendar className="h-4 w-4" />
                  {new Date(post.date).toLocaleDateString("en-IN", {
                    day: "numeric",
                    month: "long",
                    year: "numeric",
                  })}
                </span>
                <span className="flex items-center gap-1.5">
                  <Clock className="h-4 w-4" />
                  {post.readTime}
                </span>
                <span className="flex items-center gap-1.5">
                  <Tag className="h-4 w-4" />
                  {post.category}
                </span>
              </div>
            </div>
          </AnimateOnScroll>
        </Container>
      </section>

      {/* ===== ARTICLE CONTENT ===== */}
      <section className="vedic-section">
        <Container>
          <div className="mx-auto max-w-3xl">
            <AnimateOnScroll animation="fadeUp">
              <article className="prose prose-lg max-w-none prose-headings:font-heading prose-headings:text-vedic-dark prose-p:text-gray-600 prose-a:text-primary-600 prose-strong:text-vedic-dark">
                <p className="lead text-xl text-gray-700">{post.excerpt}</p>

                <h2>Introduction</h2>
                <p>
                  Vedic astrology, also known as Jyotish Shastra, is one of the
                  oldest and most comprehensive systems of astrology in the world.
                  Rooted in the ancient Vedic scriptures, it offers profound
                  insights into human life, destiny, and the cosmic forces that
                  shape our experiences.
                </p>
                <p>
                  In this article, we explore the key concepts, practical
                  applications, and transformative potential of this ancient
                  science. Whether you&apos;re a curious beginner or a seasoned
                  practitioner, there&apos;s something here for everyone.
                </p>

                <h2>Understanding the Fundamentals</h2>
                <p>
                  At the heart of Vedic astrology lies the birth chart, or Kundli
                  — a precise map of the sky at the exact moment of your birth.
                  This chart contains the positions of the 9 planets across the
                  12 houses and 12 signs, creating a unique cosmic fingerprint
                  that influences every aspect of your life.
                </p>
                <p>
                  The beauty of Vedic astrology is in its specificity. Unlike
                  sun-sign based horoscopes, Vedic astrology considers the Moon
                  sign (Rashi), the rising sign (Lagna), planetary periods (Dashas),
                  and numerous other factors to provide highly personalized and
                  accurate insights.
                </p>

                <blockquote>
                  <p>
                    &ldquo;The stars incline, they do not compel. Vedic astrology
                    illuminates the path; the choice to walk it remains
                    yours.&rdquo;
                  </p>
                </blockquote>

                <h2>Practical Applications</h2>
                <p>
                  Modern practitioners use Vedic astrology for a wide range of
                  life decisions — from choosing auspicious dates for important
                  events to understanding career aptitudes, from evaluating
                  marriage compatibility to identifying health vulnerabilities.
                </p>
                <ul>
                  <li>
                    <strong>Career guidance:</strong> The 10th house and its lord
                    reveal your professional potential and ideal career path.
                  </li>
                  <li>
                    <strong>Relationship insights:</strong> The 7th house, Venus,
                    and Jupiter placement indicate marriage timing and partner
                    characteristics.
                  </li>
                  <li>
                    <strong>Health awareness:</strong> The 6th house and specific
                    planetary combinations can highlight health vulnerabilities.
                  </li>
                  <li>
                    <strong>Financial planning:</strong> The 2nd and 11th houses
                    guide wealth accumulation and income timing.
                  </li>
                </ul>

                <h2>The Role of Remedies</h2>
                <p>
                  One of the unique aspects of Vedic astrology is its emphasis on
                  remedies — practical actions that can mitigate negative
                  planetary influences and enhance positive ones. These include
                  gemstone therapy, mantra recitation, charitable acts, and
                  specific rituals designed to harmonize your relationship with
                  cosmic energies.
                </p>
                <p>
                  It&apos;s important to note that remedies should always be
                  recommended by a qualified astrologer after thorough chart
                  analysis. Generic remedies without proper analysis can sometimes
                  be counterproductive.
                </p>

                <h2>Conclusion</h2>
                <p>
                  Vedic astrology is not about fatalism or fear — it&apos;s about
                  awareness, preparation, and empowerment. By understanding the
                  cosmic influences in your life, you can make more informed
                  decisions, prepare for challenges, and maximize your potential
                  during favorable periods.
                </p>
                <p>
                  If you&apos;d like personalized insights based on your own birth
                  chart, consider booking a consultation with our expert Vedic
                  astrologers at VedicJivan.
                </p>
              </article>
            </AnimateOnScroll>

            {/* Tags */}
            <AnimateOnScroll animation="fadeUp" delay={0.1}>
              <div className="mt-10 flex flex-wrap gap-2 border-t border-gray-100 pt-6">
                {post.tags.map((tag) => (
                  <span
                    key={tag}
                    className="rounded-full bg-gray-100 px-3 py-1 text-sm text-gray-600"
                  >
                    #{tag}
                  </span>
                ))}
              </div>
            </AnimateOnScroll>

            {/* Share */}
            <AnimateOnScroll animation="fadeUp" delay={0.15}>
              <div className="mt-6 flex items-center gap-4 border-t border-gray-100 pt-6">
                <span className="text-sm font-semibold text-vedic-dark">
                  Share this article:
                </span>
                <div className="flex gap-2">
                  <button className="flex h-9 w-9 items-center justify-center rounded-full bg-gray-100 text-gray-600 hover:bg-primary-100 hover:text-primary-600">
                    <Share2 className="h-4 w-4" />
                  </button>
                </div>
              </div>
            </AnimateOnScroll>

            {/* Author */}
            <AnimateOnScroll animation="fadeUp" delay={0.2}>
              <div className="mt-10 rounded-2xl border border-gray-100 bg-cream p-6">
                <div className="flex items-center gap-4">
                  <div className="flex h-14 w-14 items-center justify-center rounded-full bg-primary-600 font-heading text-xl font-bold text-white">
                    V
                  </div>
                  <div>
                    <h4 className="font-heading text-lg font-bold text-vedic-dark">
                      {post.author}
                    </h4>
                    <p className="text-sm text-gray-600">
                      Authentic Vedic astrology insights, articles, and guidance
                      from the VedicJivan team.
                    </p>
                  </div>
                </div>
              </div>
            </AnimateOnScroll>
          </div>
        </Container>
      </section>

      {/* ===== RELATED POSTS ===== */}
      {related.length > 0 && (
        <section className="vedic-section bg-cream">
          <Container>
            <AnimateOnScroll animation="fadeUp">
              <h2 className="mb-8 text-center font-heading text-2xl font-bold text-vedic-dark sm:text-3xl">
                Related Articles
              </h2>
            </AnimateOnScroll>

            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {related.map((p, i) => (
                <AnimateOnScroll key={p.slug} animation="fadeUp" delay={i * 0.1}>
                  <Link href={`/blog/${p.slug}`}>
                    <Card className="group h-full cursor-pointer">
                      <CardContent>
                        <Badge variant="primary" className="mb-2">
                          {p.category}
                        </Badge>
                        <h3 className="font-heading text-lg font-bold text-vedic-dark transition-colors group-hover:text-primary-600">
                          {p.title}
                        </h3>
                        <p className="mt-2 line-clamp-2 text-sm text-gray-600">
                          {p.excerpt}
                        </p>
                        <div className="mt-3 flex items-center justify-between text-xs text-gray-500">
                          <span>
                            {new Date(p.date).toLocaleDateString("en-IN", {
                              day: "numeric",
                              month: "short",
                              year: "numeric",
                            })}
                          </span>
                          <span>{p.readTime}</span>
                        </div>
                      </CardContent>
                    </Card>
                  </Link>
                </AnimateOnScroll>
              ))}
            </div>
          </Container>
        </section>
      )}

      {/* ===== CTA ===== */}
      <section className="relative overflow-hidden bg-vedic-gradient py-16">
        <Container className="relative z-10">
          <AnimateOnScroll animation="scaleIn">
            <div className="mx-auto max-w-3xl text-center">
              <h2 className="font-heading text-3xl font-bold text-white sm:text-4xl">
                Get Personalized Insights
              </h2>
              <p className="mx-auto mt-4 max-w-xl text-lg text-primary-200">
                Want guidance tailored specifically to your birth chart? Book a
                consultation with our expert Vedic astrologers.
              </p>
              <div className="mt-8 flex flex-col items-center justify-center gap-4 sm:flex-row">
                <Link href="/services">
                  <Button variant="gold" size="lg">
                    Book Consultation
                    <ArrowRight className="h-5 w-5" />
                  </Button>
                </Link>
                <Link href="/blog">
                  <Button
                    variant="outline"
                    size="lg"
                    className="border-white/30 text-white hover:bg-white/10"
                  >
                    More Articles
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
