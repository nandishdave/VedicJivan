"use client";

import { useEffect, useState, useCallback, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import { CheckCircle2, Clock } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { paymentsApi } from "@/lib/api";

function BookingSuccessContent() {
  const searchParams = useSearchParams();
  const sessionId = searchParams.get("session_id");
  const bookingId = searchParams.get("booking_id");
  const [status, setStatus] = useState<"loading" | "confirmed" | "pending">("loading");

  const checkStatus = useCallback(async () => {
    if (!sessionId || !bookingId) return;
    try {
      const result = await paymentsApi.getSessionStatus(sessionId, bookingId);
      if (result.payment_status === "captured") {
        setStatus("confirmed");
      } else {
        setStatus("pending");
      }
    } catch {
      setStatus("pending");
    }
  }, [sessionId, bookingId]);

  useEffect(() => {
    checkStatus();
    const interval = setInterval(checkStatus, 2000);
    const timeout = setTimeout(() => clearInterval(interval), 10000);
    return () => {
      clearInterval(interval);
      clearTimeout(timeout);
    };
  }, [checkStatus]);

  // Clear localStorage pending booking for all services
  useEffect(() => {
    if (status === "confirmed") {
      Object.keys(localStorage).forEach((key) => {
        if (key.startsWith("vedicjivan_pending_booking_")) {
          try {
            const data = JSON.parse(localStorage.getItem(key) || "{}");
            if (data.bookingId === bookingId) {
              localStorage.removeItem(key);
            }
          } catch {
            // ignore parse errors
          }
        }
      });
    }
  }, [status, bookingId]);

  if (status === "loading") {
    return (
      <Container className="py-20 text-center">
        <Clock className="mx-auto mb-4 h-12 w-12 animate-pulse text-primary-600" />
        <h1 className="font-heading text-2xl font-bold dark:text-gray-100">
          Verifying your payment...
        </h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
          Please wait while we confirm your payment.
        </p>
      </Container>
    );
  }

  return (
    <Container className="py-20 text-center">
      <div className="mx-auto max-w-lg">
        <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-green-100 dark:bg-green-900/30">
          <CheckCircle2 className="h-8 w-8 text-green-600 dark:text-green-400" />
        </div>
        <h1 className="font-heading text-2xl font-bold text-vedic-dark dark:text-gray-100">
          {status === "confirmed" ? "Booking Confirmed!" : "Payment Received!"}
        </h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
          {status === "confirmed"
            ? "Your booking has been confirmed. A confirmation email with details has been sent to your email address."
            : "Your payment has been received and is being processed. You will receive a confirmation email shortly."}
        </p>
        {bookingId && (
          <div className="mt-4 rounded-lg bg-gray-50 dark:bg-dark-surface-raised p-4 text-sm text-gray-700 dark:text-gray-300">
            <p>
              <strong>Booking ID:</strong>{" "}
              <span className="font-mono text-xs">{bookingId}</span>
            </p>
          </div>
        )}
        <p className="mt-4 text-xs text-gray-400 dark:text-gray-500">
          Please save your Booking ID for reference.
        </p>
        <div className="mt-8 flex justify-center gap-4">
          <Link
            href="/services"
            className="rounded-lg bg-primary-600 px-6 py-2.5 text-sm font-medium text-white hover:bg-primary-700"
          >
            Browse Services
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

export default function BookingSuccessPage() {
  return (
    <Suspense
      fallback={
        <Container className="py-20 text-center">
          <p className="text-gray-500">Loading...</p>
        </Container>
      }
    >
      <BookingSuccessContent />
    </Suspense>
  );
}
