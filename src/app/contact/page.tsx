import type { Metadata } from "next";
import Link from "next/link";
import {
  Phone,
  Mail,
  MapPin,
  Clock,
  Send,
  MessageCircle,
  ArrowRight,
  Instagram,
  Youtube,
  Facebook,
} from "lucide-react";
import { Container } from "@/components/ui/Container";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { AnimateOnScroll } from "@/components/ui/AnimateOnScroll";
import { FloatingElements } from "@/components/ui/FloatingElements";
import { GradientText } from "@/components/ui/GradientText";
import { siteConfig } from "@/config/site";

export const metadata: Metadata = {
  title: "Contact Us",
  description:
    "Get in touch with VedicJivan. Reach out for consultations, course queries, or any questions about our Vedic astrology services.",
  alternates: { canonical: "/contact" },
  openGraph: {
    title: "Contact Us | VedicJivan",
    description:
      "Get in touch with VedicJivan. Reach out for consultations, course queries, or any questions about our Vedic astrology services.",
    url: "/contact",
  },
};

export default function ContactPage() {
  return (
    <>
      {/* ===== HERO ===== */}
      <section className="relative overflow-hidden vedic-hero-gradient py-20 sm:py-28">
        <FloatingElements />
        <Container className="relative z-10">
          <AnimateOnScroll animation="fadeIn">
            <div className="mx-auto max-w-3xl text-center">
              <span className="mb-3 inline-block text-sm font-semibold uppercase tracking-widest text-gold-400">
                Get In Touch
              </span>
              <h1 className="font-heading text-4xl font-bold text-white sm:text-5xl lg:text-6xl">
                We&apos;d Love to{" "}
                <GradientText variant="gold">Hear From You</GradientText>
              </h1>
              <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-300">
                Have questions about our services, courses, or need guidance on
                which consultation is right for you? Reach out and we&apos;ll
                get back to you promptly.
              </p>
            </div>
          </AnimateOnScroll>
        </Container>
      </section>

      {/* ===== CONTACT SECTION ===== */}
      <section className="vedic-section">
        <Container>
          <div className="grid gap-12 lg:grid-cols-5">
            {/* Contact Form */}
            <div className="lg:col-span-3">
              <AnimateOnScroll animation="fadeLeft">
                <h2 className="font-heading text-2xl font-bold text-vedic-dark sm:text-3xl">
                  Send Us a Message
                </h2>
                <p className="mt-2 text-gray-600">
                  Fill out the form below and we&apos;ll respond within 24 hours.
                </p>

                <form className="mt-8 space-y-5">
                  <div className="grid gap-5 sm:grid-cols-2">
                    <Input
                      label="Full Name"
                      name="name"
                      placeholder="Your full name"
                      required
                    />
                    <Input
                      label="Email Address"
                      name="email"
                      type="email"
                      placeholder="your@email.com"
                      required
                    />
                  </div>
                  <div className="grid gap-5 sm:grid-cols-2">
                    <Input
                      label="Phone Number"
                      name="phone"
                      type="tel"
                      placeholder="+91 98765 43210"
                    />
                    <div>
                      <label className="mb-1.5 block text-sm font-medium text-vedic-dark">
                        Subject
                      </label>
                      <select
                        name="subject"
                        className="w-full rounded-lg border border-gray-300 px-4 py-3 text-sm text-vedic-text outline-none transition-colors focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20"
                      >
                        <option value="">Select a subject</option>
                        <option value="consultation">Consultation Query</option>
                        <option value="course">Course Inquiry</option>
                        <option value="report">Report Query</option>
                        <option value="feedback">Feedback</option>
                        <option value="other">Other</option>
                      </select>
                    </div>
                  </div>
                  <div>
                    <label className="mb-1.5 block text-sm font-medium text-vedic-dark">
                      Message
                    </label>
                    <textarea
                      name="message"
                      rows={5}
                      placeholder="Tell us how we can help you..."
                      className="w-full resize-none rounded-lg border border-gray-300 px-4 py-3 text-sm text-vedic-text outline-none transition-colors focus:border-primary-500 focus:ring-2 focus:ring-primary-500/20"
                      required
                    />
                  </div>
                  <Button variant="gold" size="lg" type="submit">
                    Send Message
                    <Send className="h-4 w-4" />
                  </Button>
                </form>
              </AnimateOnScroll>
            </div>

            {/* Contact Info */}
            <div className="lg:col-span-2">
              <AnimateOnScroll animation="fadeRight">
                <div className="space-y-6">
                  <div className="rounded-2xl border border-gray-100 bg-cream p-6">
                    <h3 className="font-heading text-lg font-bold text-vedic-dark">
                      Contact Information
                    </h3>
                    <div className="mt-5 space-y-4">
                      <a
                        href={`https://wa.me/${siteConfig.contact.whatsapp}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-start gap-3 text-gray-600 hover:text-primary-600"
                      >
                        <Phone className="mt-0.5 h-5 w-5 shrink-0 text-primary-600" />
                        <div>
                          <p className="font-semibold text-vedic-dark">WhatsApp</p>
                          <p className="text-sm">{siteConfig.contact.phone}</p>
                        </div>
                      </a>
                      <a
                        href={`mailto:${siteConfig.contact.email}`}
                        className="flex items-start gap-3 text-gray-600 hover:text-primary-600"
                      >
                        <Mail className="mt-0.5 h-5 w-5 shrink-0 text-primary-600" />
                        <div>
                          <p className="font-semibold text-vedic-dark">Email</p>
                          <p className="text-sm">{siteConfig.contact.email}</p>
                        </div>
                      </a>
                      <div className="flex items-start gap-3 text-gray-600">
                        <MapPin className="mt-0.5 h-5 w-5 shrink-0 text-primary-600" />
                        <div>
                          <p className="font-semibold text-vedic-dark">
                            Location
                          </p>
                          {siteConfig.contact.address.map((line, i) => (
                            <p key={i} className="text-sm">{line}</p>
                          ))}
                        </div>
                      </div>
                      <div className="flex items-start gap-3 text-gray-600">
                        <Clock className="mt-0.5 h-5 w-5 shrink-0 text-primary-600" />
                        <div>
                          <p className="font-semibold text-vedic-dark">
                            Working Hours
                          </p>
                          <p className="text-sm">Mon - Sat: 10:00 AM - 7:00 PM</p>
                          <p className="text-sm">Sunday: Closed</p>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* WhatsApp */}
                  <a
                    href={`https://wa.me/${siteConfig.contact.whatsapp}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-3 rounded-2xl border border-green-200 bg-green-50 p-6 transition-colors hover:bg-green-100"
                  >
                    <MessageCircle className="h-8 w-8 text-green-600" />
                    <div>
                      <p className="font-semibold text-green-800">
                        Chat on WhatsApp
                      </p>
                      <p className="text-sm text-green-600">
                        Quick responses, typically within minutes
                      </p>
                    </div>
                  </a>

                  {/* Social Links */}
                  <div className="rounded-2xl border border-gray-100 bg-cream p-6">
                    <h3 className="font-heading text-lg font-bold text-vedic-dark">
                      Follow Us
                    </h3>
                    <div className="mt-4 flex flex-wrap gap-3">
                      {socialLinks.map((social) => (
                        <a
                          key={social.name}
                          href={social.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center gap-2 rounded-lg bg-white px-4 py-2 text-sm font-medium text-gray-600 shadow-sm transition-colors hover:text-primary-600"
                        >
                          {social.icon}
                          {social.name}
                        </a>
                      ))}
                    </div>
                  </div>
                </div>
              </AnimateOnScroll>
            </div>
          </div>
        </Container>
      </section>

      {/* ===== MAP PLACEHOLDER ===== */}
      <section className="bg-gray-100">
        <div className="flex h-64 items-center justify-center lg:h-80">
          <div className="text-center">
            <MapPin className="mx-auto h-10 w-10 text-gray-300" />
            <p className="mt-2 text-sm text-gray-400">
              Google Maps integration will be added here
            </p>
          </div>
        </div>
      </section>

      {/* ===== CTA ===== */}
      <section className="relative overflow-hidden vedic-cta-gradient py-20">
        <Container className="relative z-10">
          <AnimateOnScroll animation="scaleIn">
            <div className="mx-auto max-w-3xl text-center">
              <h2 className="font-heading text-3xl font-bold text-white sm:text-4xl">
                Ready to Book a Consultation?
              </h2>
              <p className="mx-auto mt-4 max-w-xl text-lg text-primary-200">
                Skip the wait — book a consultation directly and get personalized
                Vedic astrology guidance.
              </p>
              <div className="mt-8">
                <Link href="/services">
                  <Button variant="gold" size="lg">
                    Browse Services
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

const socialLinks = [
  { name: "Instagram", url: siteConfig.social.instagram, icon: <Instagram className="h-4 w-4" /> },
  { name: "YouTube", url: siteConfig.social.youtube, icon: <Youtube className="h-4 w-4" /> },
  { name: "Facebook", url: siteConfig.social.facebook, icon: <Facebook className="h-4 w-4" /> },
];
