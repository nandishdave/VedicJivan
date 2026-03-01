"use client";

import { Suspense } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import { XCircle } from "lucide-react";
import { Container } from "@/components/ui/Container";

function BookingCancelledContent() {
  const searchParams = useSearchParams();
  const bookingId = searchParams.get("booking_id");

  return (
    <Container className="py-20 text-center">
      <div className="mx-auto max-w-lg">
        <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-amber-100 dark:bg-amber-900/30">
          <XCircle className="h-8 w-8 text-amber-600 dark:text-amber-400" />
        </div>
        <h1 className="font-heading text-2xl font-bold text-vedic-dark dark:text-gray-100">
          Payment Not Completed
        </h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
          Your payment was not completed. Don&apos;t worry — your booking is still
          reserved for 15 minutes. You can go back and try again.
        </p>
        {bookingId && (
          <p className="mt-2 text-xs text-gray-400 dark:text-gray-500">
            Booking ID: <span className="font-mono">{bookingId}</span>
          </p>
        )}
        <div className="mt-8 flex justify-center gap-4">
          <Link
            href="/services"
            className="rounded-lg bg-primary-600 px-6 py-2.5 text-sm font-medium text-white hover:bg-primary-700"
          >
            Try Again
          </Link>
          <Link
            href="/"
            className="rounded-lg border border-gray-300 dark:border-gray-600 px-6 py-2.5 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-white/5"
          >
            Back to Home
          </Link>
        </div>
      </div>
    </Container>
  );
}

export default function BookingCancelledPage() {
  return (
    <Suspense
      fallback={
        <Container className="py-20 text-center">
          <p className="text-gray-500">Loading...</p>
        </Container>
      }
    >
      <BookingCancelledContent />
    </Suspense>
  );
}
