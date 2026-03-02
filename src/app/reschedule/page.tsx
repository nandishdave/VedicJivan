"use client";

import { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import { CheckCircle2, Calendar, Clock, ArrowLeft, Loader2, AlertTriangle } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { BookingCalendar } from "@/components/booking/BookingCalendar";
import { TimeSlotPicker } from "@/components/booking/TimeSlotPicker";
import { bookingsApi, type Booking } from "@/lib/api";

function RescheduleContent() {
  const searchParams = useSearchParams();
  const bookingId = searchParams.get("id") ?? "";

  const [booking, setBooking] = useState<Booking | null>(null);
  const [loadError, setLoadError] = useState("");
  const [selectedDate, setSelectedDate] = useState("");
  const [selectedSlot, setSelectedSlot] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState("");
  const [success, setSuccess] = useState(false);
  const [newDate, setNewDate] = useState("");
  const [newSlot, setNewSlot] = useState("");

  useEffect(() => {
    if (!bookingId) {
      setLoadError("No booking ID provided.");
      return;
    }
    bookingsApi
      .view(bookingId)
      .then(setBooking)
      .catch((e) => setLoadError(e.message || "Booking not found"));
  }, [bookingId]);

  const formatDate = (dateStr: string) =>
    new Date(dateStr + "T00:00:00").toLocaleDateString("en-IN", {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
    });

  const handleReschedule = async () => {
    if (!selectedDate || !selectedSlot || !booking) return;
    setSubmitting(true);
    setSubmitError("");
    try {
      await bookingsApi.reschedule(bookingId, {
        date: selectedDate,
        time_slot: selectedSlot,
        duration_minutes: booking.duration_minutes,
      });
      setNewDate(selectedDate);
      setNewSlot(selectedSlot);
      setSuccess(true);
    } catch (e: unknown) {
      setSubmitError(e instanceof Error ? e.message : "Failed to reschedule");
    } finally {
      setSubmitting(false);
    }
  };

  if (loadError) {
    return (
      <Container className="py-20 text-center">
        <p className="text-red-600 dark:text-red-400 font-medium">{loadError}</p>
        <Link href="/services" className="mt-4 inline-block text-sm text-primary-600 underline">
          Browse Services
        </Link>
      </Container>
    );
  }

  if (!booking) {
    return (
      <Container className="py-20 text-center">
        <Loader2 className="mx-auto h-8 w-8 animate-spin text-primary-600" />
        <p className="mt-3 text-gray-500">Loading booking details...</p>
      </Container>
    );
  }

  // 24-hour cutoff check — booking times are stored in IST (UTC+5:30)
  const bookingIST = new Date(`${booking.date}T${booking.time_slot}:00+05:30`);
  const isWithin24Hours = bookingIST.getTime() - Date.now() < 24 * 60 * 60 * 1000;

  if (isWithin24Hours) {
    return (
      <Container className="py-20">
        <div className="mx-auto max-w-lg text-center">
          <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-amber-100 dark:bg-amber-900/30">
            <AlertTriangle className="h-8 w-8 text-amber-600 dark:text-amber-400" />
          </div>
          <h1 className="font-heading text-2xl font-bold text-vedic-dark dark:text-gray-100">
            Rescheduling Not Available
          </h1>
          <p className="mt-3 text-gray-600 dark:text-gray-400">
            Your <strong>{booking.service_title}</strong> session is scheduled for{" "}
            <strong>{formatDate(booking.date)}</strong> at <strong>{booking.time_slot}</strong>.
          </p>
          <p className="mt-2 text-gray-500 dark:text-gray-400 text-sm">
            Rescheduling must be requested more than 24 hours before your session. This window has passed.
          </p>
          <div className="mt-8 flex justify-center gap-4">
            <Link
              href="/contact"
              className="rounded-lg bg-primary-600 px-6 py-2.5 text-sm font-medium text-white hover:bg-primary-700"
            >
              Contact Us
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

  if (success) {
    return (
      <Container className="py-20">
        <div className="mx-auto max-w-lg text-center">
          <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-green-100 dark:bg-green-900/30">
            <CheckCircle2 className="h-8 w-8 text-green-600 dark:text-green-400" />
          </div>
          <h1 className="font-heading text-2xl font-bold text-vedic-dark dark:text-gray-100">
            Booking Rescheduled!
          </h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">
            Your session has been moved to{" "}
            <strong>{formatDate(newDate)}</strong> at <strong>{newSlot}</strong>.
            A confirmation email has been sent to you.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-4">
            <button
              onClick={() => { setSuccess(false); setSelectedDate(""); setSelectedSlot(""); }}
              className="rounded-lg bg-primary-600 px-6 py-2.5 text-sm font-medium text-white hover:bg-primary-700"
            >
              Reschedule Again
            </button>
            <Link
              href="/services"
              className="rounded-lg border border-gray-300 dark:border-gray-600 px-6 py-2.5 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-white/5"
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

  return (
    <Container className="py-12">
      <div className="mx-auto max-w-2xl">
        <Link
          href="/"
          className="mb-6 inline-flex items-center gap-2 text-sm text-gray-500 hover:text-primary-600 dark:text-gray-400 dark:hover:text-primary-400"
        >
          <ArrowLeft className="h-4 w-4" />
          Back to Home
        </Link>

        <h1 className="font-heading text-2xl font-bold text-vedic-dark dark:text-gray-100 mb-2">
          Reschedule Your Session
        </h1>

        {/* Current booking summary */}
        <div className="mb-6 rounded-xl border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-dark-surface-raised p-4">
          <p className="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
            {booking.service_title}
          </p>
          <div className="flex flex-wrap gap-4 text-sm text-gray-500 dark:text-gray-400">
            <span className="flex items-center gap-1.5">
              <Calendar className="h-4 w-4" />
              Current: <strong className="text-gray-700 dark:text-gray-200">{formatDate(booking.date)}</strong>
            </span>
            <span className="flex items-center gap-1.5">
              <Clock className="h-4 w-4" />
              <strong className="text-gray-700 dark:text-gray-200">{booking.time_slot}</strong>
              &nbsp;({booking.duration_minutes} min)
            </span>
          </div>
        </div>

        {/* Date picker */}
        <div className="mb-6">
          <h2 className="font-heading text-lg font-semibold text-vedic-dark dark:text-gray-100 mb-3">
            Select New Date
          </h2>
          <BookingCalendar
            selectedDate={selectedDate}
            onDateSelect={(d) => { setSelectedDate(d); setSelectedSlot(""); }}
          />
        </div>

        {/* Time slot picker */}
        {selectedDate && (
          <div className="mb-6">
            <h2 className="font-heading text-lg font-semibold text-vedic-dark dark:text-gray-100 mb-3">
              Select New Time
            </h2>
            <TimeSlotPicker
              date={selectedDate}
              selectedSlot={selectedSlot}
              onSlotSelect={setSelectedSlot}
            />
          </div>
        )}

        {submitError && (
          <p className="mb-4 rounded-lg bg-red-50 dark:bg-red-900/20 px-4 py-3 text-sm text-red-700 dark:text-red-400">
            {submitError}
          </p>
        )}

        <button
          onClick={handleReschedule}
          disabled={!selectedDate || !selectedSlot || submitting}
          className="w-full rounded-xl bg-primary-600 py-3 text-base font-semibold text-white hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          {submitting ? (
            <>
              <Loader2 className="h-5 w-5 animate-spin" />
              Rescheduling...
            </>
          ) : (
            "Confirm Reschedule"
          )}
        </button>
      </div>
    </Container>
  );
}

export default function ReschedulePage() {
  return (
    <Suspense
      fallback={
        <Container className="py-20 text-center">
          <Loader2 className="mx-auto h-8 w-8 animate-spin text-primary-600" />
        </Container>
      }
    >
      <RescheduleContent />
    </Suspense>
  );
}
