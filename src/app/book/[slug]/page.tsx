import type { Metadata } from "next";
import { services, getServiceBySlug } from "@/data/services";
import { BookingContent } from "./BookingContent";

export function generateStaticParams() {
  return services.map((s) => ({ slug: s.slug }));
}

export function generateMetadata({
  params,
}: {
  params: { slug: string };
}): Metadata {
  const service = getServiceBySlug(params.slug);
  if (!service) return { title: "Book a Service" };

  return {
    title: `Book ${service.title}`,
    description: `Book your ${service.title} with VedicJivan. ${service.shortDescription}`,
    alternates: { canonical: `/book/${params.slug}` },
  };
}

export default function BookingPage({
  params,
}: {
  params: { slug: string };
}) {
  return <BookingContent slug={params.slug} />;
}
