import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import {
  ArrowRight,
  ArrowLeft,
  Calendar,
  Clock,
  Tag,
} from "lucide-react";
import { Container } from "@/components/ui/Container";
import { Button } from "@/components/ui/Button";
import { Card, CardContent } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { AnimateOnScroll } from "@/components/ui/AnimateOnScroll";
import { blogPosts, getBlogPostBySlug, getRelatedPosts } from "@/data/blog";
import { BlogPostJsonLd, BreadcrumbJsonLd } from "@/components/seo/JsonLd";

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
    alternates: {
      canonical: `/blog/${params.slug}`,
    },
    openGraph: {
      title: post.title,
      description: post.excerpt,
      type: "article",
      url: `/blog/${params.slug}`,
      publishedTime: post.date,
      authors: [post.author],
    },
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

  const BASE_URL = "https://vedicjivan.nandishdave.world";

  return (
    <>
      <BlogPostJsonLd
        title={post.title}
        excerpt={post.excerpt}
        author={post.author}
        date={post.date}
        url={`${BASE_URL}/blog/${post.slug}`}
      />
      <BreadcrumbJsonLd
        items={[
          { name: "Home", url: BASE_URL },
          { name: "Blog", url: `${BASE_URL}/blog` },
          { name: post.title, url: `${BASE_URL}/blog/${post.slug}` },
        ]}
      />

      {/* ===== HEADER ===== */}
      <section className="relative overflow-hidden vedic-hero-gradient py-16 sm:py-24">
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
                  <a
                    href={`https://api.whatsapp.com/send?text=${encodeURIComponent(post.title + " " + BASE_URL + "/blog/" + post.slug)}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex h-9 w-9 items-center justify-center rounded-full bg-green-100 text-green-600 hover:bg-green-200"
                    aria-label="Share on WhatsApp"
                  >
                    <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
                  </a>
                  <a
                    href={`https://twitter.com/intent/tweet?text=${encodeURIComponent(post.title)}&url=${encodeURIComponent(BASE_URL + "/blog/" + post.slug)}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex h-9 w-9 items-center justify-center rounded-full bg-gray-100 text-gray-700 hover:bg-gray-200"
                    aria-label="Share on X"
                  >
                    <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                  </a>
                  <a
                    href={`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(BASE_URL + "/blog/" + post.slug)}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex h-9 w-9 items-center justify-center rounded-full bg-blue-100 text-blue-600 hover:bg-blue-200"
                    aria-label="Share on Facebook"
                  >
                    <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
                  </a>
                  <a
                    href={`https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(BASE_URL + "/blog/" + post.slug)}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex h-9 w-9 items-center justify-center rounded-full bg-blue-100 text-blue-700 hover:bg-blue-200"
                    aria-label="Share on LinkedIn"
                  >
                    <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
                  </a>
                </div>
              </div>
            </AnimateOnScroll>

            {/* Author */}
            <AnimateOnScroll animation="fadeUp" delay={0.2}>
              <div className="mt-10 rounded-2xl border border-gray-100 bg-cream p-6">
                <div className="flex items-center gap-4">
                  <div className="flex h-14 w-14 items-center justify-center rounded-full bg-primary-600 font-heading text-xl font-bold text-white">
                    ND
                  </div>
                  <div>
                    <h4 className="font-heading text-lg font-bold text-vedic-dark">
                      {post.author}
                    </h4>
                    <p className="text-sm text-gray-600">
                      Vedic Astrologer, Numerologist & Founder of VedicJivan.
                      Helping people navigate life through ancient Vedic wisdom.
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
      <section className="relative overflow-hidden vedic-cta-gradient py-16">
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
