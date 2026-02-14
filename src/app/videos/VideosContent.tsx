"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { ArrowRight, Youtube } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { Button } from "@/components/ui/Button";
import { SectionHeading } from "@/components/ui/SectionHeading";
import { AnimateOnScroll } from "@/components/ui/AnimateOnScroll";
import { FloatingElements } from "@/components/ui/FloatingElements";
import { GradientText } from "@/components/ui/GradientText";
import { VideoCard, VideoCardSkeleton } from "@/components/ui/VideoCard";
import { fetchChannelVideos, type YouTubeVideo } from "@/lib/youtube";
import { siteConfig } from "@/config/site";

const API_KEY = process.env.NEXT_PUBLIC_YOUTUBE_API_KEY;
const CHANNEL_ID = process.env.NEXT_PUBLIC_YOUTUBE_CHANNEL_ID;

export function VideosContent() {
  const [videos, setVideos] = useState<YouTubeVideo[]>([]);
  const [shorts, setShorts] = useState<YouTubeVideo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    if (!API_KEY || !CHANNEL_ID) {
      setLoading(false);
      setError(true);
      return;
    }

    fetchChannelVideos(API_KEY, CHANNEL_ID)
      .then((data) => {
        setVideos(data.videos);
        setShorts(data.shorts);
      })
      .catch(() => {
        setError(true);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  return (
    <>
      {/* ===== HERO ===== */}
      <section className="relative overflow-hidden vedic-hero-gradient py-20 sm:py-28">
        <FloatingElements />
        <Container className="relative z-10">
          <AnimateOnScroll animation="fadeIn">
            <div className="mx-auto max-w-3xl text-center">
              <span className="mb-3 inline-block text-sm font-semibold uppercase tracking-widest text-gold-400">
                Our Channel
              </span>
              <h1 className="font-heading text-4xl font-bold text-white sm:text-5xl lg:text-6xl">
                Watch Our{" "}
                <GradientText variant="gold">Videos</GradientText>
              </h1>
              <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-300">
                Explore Vedic astrology insights, numerology tips, spiritual
                guidance, and more through our YouTube videos and shorts.
              </p>
              <div className="mt-8">
                <a
                  href={siteConfig.social.youtube}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <Button variant="gold" size="lg">
                    <Youtube className="h-5 w-5" />
                    Subscribe on YouTube
                  </Button>
                </a>
              </div>
            </div>
          </AnimateOnScroll>
        </Container>
      </section>

      {/* ===== VIDEOS SECTION ===== */}
      <section className="vedic-section">
        <Container>
          <AnimateOnScroll animation="fadeUp">
            <SectionHeading
              subtitle="Latest"
              title="Videos"
              description="Full-length videos on Vedic astrology, consultations, and spiritual wisdom."
            />
          </AnimateOnScroll>

          {loading ? (
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {[...Array(6)].map((_, i) => (
                <VideoCardSkeleton key={i} variant="video" />
              ))}
            </div>
          ) : error || videos.length === 0 ? (
            <FallbackSection type="videos" />
          ) : (
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {videos.map((video, i) => (
                <AnimateOnScroll key={video.id} animation="fadeUp" delay={i * 0.05}>
                  <VideoCard {...video} variant="video" />
                </AnimateOnScroll>
              ))}
            </div>
          )}
        </Container>
      </section>

      {/* ===== SHORTS SECTION ===== */}
      <section className="vedic-section bg-cream">
        <Container>
          <AnimateOnScroll animation="fadeUp">
            <SectionHeading
              subtitle="Quick Bites"
              title="Shorts"
              description="Quick Vedic astrology tips and insights in under 60 seconds."
            />
          </AnimateOnScroll>

          {loading ? (
            <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5">
              {[...Array(5)].map((_, i) => (
                <VideoCardSkeleton key={i} variant="short" />
              ))}
            </div>
          ) : error || shorts.length === 0 ? (
            <FallbackSection type="shorts" />
          ) : (
            <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5">
              {shorts.map((short, i) => (
                <AnimateOnScroll key={short.id} animation="fadeUp" delay={i * 0.05}>
                  <VideoCard {...short} variant="short" />
                </AnimateOnScroll>
              ))}
            </div>
          )}
        </Container>
      </section>

      {/* ===== CTA ===== */}
      <section className="relative overflow-hidden vedic-cta-gradient py-20">
        <Container className="relative z-10">
          <AnimateOnScroll animation="scaleIn">
            <div className="mx-auto max-w-3xl text-center">
              <h2 className="font-heading text-3xl font-bold text-white sm:text-4xl">
                Don&apos;t Miss New Uploads
              </h2>
              <p className="mx-auto mt-4 max-w-xl text-lg text-primary-200">
                Subscribe to our YouTube channel for weekly videos on Vedic
                astrology, numerology, and spiritual growth.
              </p>
              <div className="mt-8 flex flex-wrap items-center justify-center gap-4">
                <a
                  href={siteConfig.social.youtube}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <Button variant="gold" size="lg">
                    <Youtube className="h-5 w-5" />
                    Subscribe Now
                  </Button>
                </a>
                <Link href="/services">
                  <Button variant="outline" size="lg" className="border-white text-white hover:bg-white/10">
                    Explore Services
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

function FallbackSection({ type }: { type: "videos" | "shorts" }) {
  return (
    <div className="mx-auto max-w-md text-center py-12">
      <Youtube className="mx-auto h-12 w-12 text-red-500" />
      <h3 className="mt-4 font-heading text-lg font-bold text-vedic-dark">
        Watch on YouTube
      </h3>
      <p className="mt-2 text-sm text-gray-600">
        {type === "videos"
          ? "Visit our YouTube channel to watch our latest full-length videos."
          : "Check out our YouTube channel for quick astrology tips and shorts."}
      </p>
      <div className="mt-6">
        <a
          href={siteConfig.social.youtube}
          target="_blank"
          rel="noopener noreferrer"
        >
          <Button variant="primary" size="md">
            <Youtube className="h-4 w-4" />
            Visit Channel
          </Button>
        </a>
      </div>
    </div>
  );
}
