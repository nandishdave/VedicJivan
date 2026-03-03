"use client";

import { useEffect, useState, useCallback, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import { CheckCircle2, Clock, Calendar, User, Mail, IndianRupee } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { paymentsApi } from "@/lib/api";

interface BookingDetails {
  service_title: string;
  date: string;
  time_slot: string;
  duration_minutes: number;
  price_inr: number;
  user_name: string;
  user_email: string;
}

function BookingSuccessContent() {
  const searchParams = useSearchParams();
  const sessionId = searchParams.get("session_id");
  const bookingId = searchParams.get("booking_id");
  const [status, setStatus] = useState<"loading" | "confirmed" | "pending">("loading");
  const [booking, setBooking] = useState<BookingDetails | null>(null);

  const checkStatus = useCallback(async () => {
    if (!sessionId || !bookingId) return;
    try {
      const result = await paymentsApi.getSessionStatus(sessionId, bookingId);
      if (result.booking) {
        setBooking(result.booking);
      }
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

  // Clear localStorage pending booking — Stripe only redirects here after
  // successful payment, so clear regardless of webhook confirmation status
  useEffect(() => {
    if (status === "confirmed" || status === "pending") {
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

  const formatDate = (dateStr: string) => {
    try {
      return new Date(dateStr + "T00:00:00").toLocaleDateString("en-IN", {
        weekday: "long",
        year: "numeric",
        month: "long",
        day: "numeric",
      });
    } catch {
      return dateStr;
    }
  };

  return (
    <Container className="py-20">
      <div className="mx-auto max-w-lg">
        <div className="text-center">
          <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-green-100 dark:bg-green-900/30">
            <CheckCircle2 className="h-8 w-8 text-green-600 dark:text-green-400" />
          </div>
          <h1 className="font-heading text-2xl font-bold text-vedic-dark dark:text-gray-100">
            {status === "confirmed" ? "Booking Confirmed!" : "Payment Received!"}
          </h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">
            {status === "confirmed"
              ? "Your booking has been confirmed. A confirmation email has been sent to your email address."
              : "Your payment has been received and is being processed. You will receive a confirmation email shortly."}
          </p>
        </div>

        {booking && (
          <div className="mt-8 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-dark-surface-card overflow-hidden">
            <div className="bg-primary-50 dark:bg-primary-900/20 px-6 py-4 border-b border-gray-200 dark:border-gray-700">
              <h2 className="font-heading text-lg font-semibold text-vedic-dark dark:text-gray-100">
                {booking.service_title}
              </h2>
            </div>
            <div className="px-6 py-4 space-y-3">
              <div className="flex items-center gap-3 text-sm">
                <Calendar className="h-4 w-4 flex-shrink-0 text-primary-600 dark:text-primary-400" />
                <span className="text-gray-700 dark:text-gray-300">
                  {formatDate(booking.date)}
                  {booking.duration_minutes > 0 && (
                    <> at <strong>{booking.time_slot}</strong> ({booking.duration_minutes} min)</>
                  )}
                </span>
              </div>
              <div className="flex items-center gap-3 text-sm">
                <User className="h-4 w-4 flex-shrink-0 text-primary-600 dark:text-primary-400" />
                <span className="text-gray-700 dark:text-gray-300">{booking.user_name}</span>
              </div>
              <div className="flex items-center gap-3 text-sm">
                <Mail className="h-4 w-4 flex-shrink-0 text-primary-600 dark:text-primary-400" />
                <span className="text-gray-700 dark:text-gray-300">{booking.user_email}</span>
              </div>
              <div className="flex items-center gap-3 text-sm">
                <IndianRupee className="h-4 w-4 flex-shrink-0 text-primary-600 dark:text-primary-400" />
                <span className="font-semibold text-gray-900 dark:text-gray-100">
                  {"\u20B9"}{booking.price_inr.toLocaleString("en-IN")}
                </span>
              </div>
            </div>
          </div>
        )}

        {bookingId && (
          <div className="mt-4 rounded-lg bg-gray-50 dark:bg-dark-surface-raised p-4 text-center text-sm text-gray-700 dark:text-gray-300">
            <p>
              <strong>Booking ID:</strong>{" "}
              <span className="font-mono text-xs">{bookingId}</span>
            </p>
          </div>
        )}
        <p className="mt-3 text-center text-xs text-gray-400 dark:text-gray-500">
          Please save your Booking ID for reference.
        </p>
        <div className="mt-8 flex flex-wrap justify-center gap-4">
          {bookingId && booking && booking.duration_minutes > 0 && (
            <Link
              href={`/reschedule/?id=${bookingId}`}
              className="rounded-lg border border-primary-300 dark:border-primary-700 px-6 py-2.5 text-sm font-medium text-primary-700 dark:text-primary-300 hover:bg-primary-50 dark:hover:bg-primary-900/20"
            >
              Reschedule
            </Link>
          )}
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
