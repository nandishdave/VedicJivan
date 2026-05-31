"use client";

import { useEffect, useState } from "react";
import { bookingsApi, type Booking } from "@/lib/api";

const PENDING_BOOKING_TTL_MS = 15 * 60 * 1000; // matches API PENDING_EXPIRY_MINUTES
const PARTIAL_PROGRESS_TTL_MS = 2 * 60 * 60 * 1000;

export interface PartialProgress {
  date?: string;
  timeSlot?: string;
  duration?: number;
}

export interface UseResumableBooking {
  /** True until the localStorage scan + server-side resume check finishes. */
  checking: boolean;
  /** The full booking the user can resume (server-confirmed pending). */
  resumeBooking: Booking | null;
  /** Whether to show the "Resume your booking?" banner. */
  showResumePrompt: boolean;
  /** Partial date/time selections found in localStorage (pre-booking-create). */
  partialProgress: PartialProgress | null;
  /** Hide the resume banner and start fresh. */
  startFresh: () => void;
  /** Drop the resume banner without clearing storage (after the user accepted resume). */
  acceptResume: () => void;
}

/** On mount, check localStorage for an in-progress booking under
 * `vedicjivan_pending_booking_{slug}` and resolve to one of:
 *
 *   1. A confirmed-pending Booking the user can pay for (15-min TTL).
 *   2. Partial date/time selections that pre-fill the wizard (2-hour TTL).
 *   3. Nothing — clean state.
 *
 * Expired records are deleted. Server-side validation runs for case (1)
 * via `bookingsApi.resume(id)`; on any error the storage entry is dropped.
 */
export function useResumableBooking(storageKey: string): UseResumableBooking {
  const [checking, setChecking] = useState(true);
  const [resumeBooking, setResumeBooking] = useState<Booking | null>(null);
  const [showResumePrompt, setShowResumePrompt] = useState(false);
  const [partialProgress, setPartialProgress] = useState<PartialProgress | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function check() {
      try {
        if (typeof window === "undefined") {
          if (!cancelled) setChecking(false);
          return;
        }
        const stored = localStorage.getItem(storageKey);
        if (!stored) {
          if (!cancelled) setChecking(false);
          return;
        }

        const record = JSON.parse(stored);

        if (record.bookingId) {
          // Full booking — check 15-min expiry then validate against the API.
          const elapsed = Date.now() - new Date(record.createdAt).getTime();
          if (elapsed > PENDING_BOOKING_TTL_MS) {
            localStorage.removeItem(storageKey);
            if (!cancelled) setChecking(false);
            return;
          }
          const booking = await bookingsApi.resume(record.bookingId);
          if (!cancelled) {
            setResumeBooking(booking);
            setShowResumePrompt(true);
          }
        } else {
          // Partial progress — check 2-hour TTL then surface for pre-fill.
          const savedAt = record.savedAt ? new Date(record.savedAt).getTime() : 0;
          if (savedAt && Date.now() - savedAt > PARTIAL_PROGRESS_TTL_MS) {
            localStorage.removeItem(storageKey);
            if (!cancelled) setChecking(false);
            return;
          }
          if (!cancelled) {
            setPartialProgress({
              date: record.date,
              timeSlot: record.timeSlot,
              duration: record.duration,
            });
          }
        }
      } catch {
        if (typeof window !== "undefined") localStorage.removeItem(storageKey);
      } finally {
        if (!cancelled) setChecking(false);
      }
    }

    void check();
    return () => {
      cancelled = true;
    };
  }, [storageKey]);

  return {
    checking,
    resumeBooking,
    showResumePrompt,
    partialProgress,
    startFresh: () => {
      if (typeof window !== "undefined") localStorage.removeItem(storageKey);
      setShowResumePrompt(false);
      setResumeBooking(null);
    },
    acceptResume: () => {
      setShowResumePrompt(false);
    },
  };
}
