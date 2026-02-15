"use client";

import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { FloatingElements } from "@/components/ui/FloatingElements";
import { GradientText } from "@/components/ui/GradientText";
import { BookingWizard } from "@/components/booking/BookingWizard";
import { getServiceBySlug } from "@/data/services";

export function BookingContent({ slug }: { slug: string }) {
  const service = getServiceBySlug(slug);

  if (!service) {
    return (
      <Container className="py-20 text-center">
        <h1 className="font-heading text-2xl font-bold">Service Not Found</h1>
        <Link href="/services" className="mt-4 inline-block text-primary-600 hover:underline">
          View all services
        </Link>
      </Container>
    );
  }

  return (
    <>
      {/* Hero */}
      <section className="relative overflow-hidden vedic-hero-gradient py-16 sm:py-20">
        <FloatingElements />
        <Container className="relative z-10">
          <div className="mx-auto max-w-3xl text-center">
            <Link
              href={`/services/${slug}`}
              className="mb-4 inline-flex items-center gap-1 text-sm text-gray-300 hover:text-white"
            >
              <ArrowLeft className="h-4 w-4" />
              Back to {service.title}
            </Link>
            <h1 className="font-heading text-3xl font-bold text-white sm:text-4xl">
              Book <GradientText variant="gold">{service.title}</GradientText>
            </h1>
            <p className="mx-auto mt-3 max-w-xl text-gray-300">
              {service.shortDescription}
            </p>
            <p className="mt-2 text-lg font-semibold text-gold-400">
              Starting from {service.priceINR}
            </p>
          </div>
        </Container>
      </section>

      {/* Booking wizard */}
      <section className="vedic-section">
        <Container>
          <BookingWizard service={service} />
        </Container>
      </section>
    </>
  );
}
