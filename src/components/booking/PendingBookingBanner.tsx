"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Clock, X, ArrowRight } from "lucide-react";

interface PendingRecord {
  serviceSlug: string;
  serviceTitle?: string;
  date?: string;
  timeSlot?: string;
  bookingId?: string;
  createdAt?: string;
  savedAt?: string;
}

const STORAGE_PREFIX = "vedicjivan_pending_booking_";
const PAYMENT_EXPIRY_MS = 15 * 60 * 1000; // 15 minutes for pending-payment
const PARTIAL_EXPIRY_MS = 2 * 60 * 60 * 1000; // 2 hours for partial progress

export function PendingBookingBanner() {
  const pathname = usePathname();
  const [record, setRecord] = useState<PendingRecord | null>(null);
  const [dismissed, setDismissed] = useState(false);
  const [minutesLeft, setMinutesLeft] = useState(0);

  // Hide on booking pages — BookingWizard handles resume there
  const isBookingPage = pathname.startsWith("/book");

  useEffect(() => {
    if (isBookingPage) return;

    // Scan localStorage for any pending booking key
    let best: { key: string; data: PendingRecord; timestamp: number } | null = null;

    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (!key?.startsWith(STORAGE_PREFIX)) continue;

      try {
        const data: PendingRecord = JSON.parse(localStorage.getItem(key) || "");
        const timestamp = data.createdAt
          ? new Date(data.createdAt).getTime()
          : data.savedAt
            ? new Date(data.savedAt).getTime()
            : 0;

        if (!timestamp) continue;

        const age = Date.now() - timestamp;

        // Pending-payment bookings expire after 15 min
        if (data.bookingId && age > PAYMENT_EXPIRY_MS) {
          localStorage.removeItem(key);
          continue;
        }

        // Partial progress expires after 2 hours
        if (!data.bookingId && age > PARTIAL_EXPIRY_MS) {
          localStorage.removeItem(key);
          continue;
        }

        // Keep the most recent entry
        if (!best || timestamp > best.timestamp) {
          best = { key, data, timestamp };
        }
      } catch {
        localStorage.removeItem(key!);
      }
    }

    if (best) {
      setRecord(best.data);
      if (best.data.bookingId && best.data.createdAt) {
        const elapsed = Date.now() - new Date(best.data.createdAt).getTime();
        setMinutesLeft(Math.max(1, Math.ceil((PAYMENT_EXPIRY_MS - elapsed) / 60000)));
      }
    }
  }, [isBookingPage, pathname]);

  // Live countdown for pending-payment bookings
  useEffect(() => {
    if (!record?.bookingId || !record.createdAt) return;

    const interval = setInterval(() => {
      const elapsed = Date.now() - new Date(record.createdAt!).getTime();
      const remaining = Math.ceil((PAYMENT_EXPIRY_MS - elapsed) / 60000);
      if (remaining <= 0) {
        // Expired — remove from localStorage and hide
        const key = `${STORAGE_PREFIX}${record.serviceSlug}`;
        localStorage.removeItem(key);
        setRecord(null);
      } else {
        setMinutesLeft(remaining);
      }
    }, 30000);

    return () => clearInterval(interval);
  }, [record]);

  if (isBookingPage || dismissed || !record) return null;

  const isPendingPayment = !!record.bookingId;
  const serviceLabel = record.serviceTitle || "booking";

  return (
    <div className="fixed bottom-0 inset-x-0 z-40 animate-slide-in-up pointer-events-none">
      <div className="pointer-events-auto mx-0 sm:mx-4 sm:mb-4 mb-0">
        <div className="bg-gradient-to-r from-primary-800 via-primary-700 to-primary-900 text-white shadow-2xl shadow-primary-900/40 sm:rounded-xl">
          <div className="mx-auto max-w-7xl px-4 py-3.5 sm:px-6">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
              {/* Left: icon + message */}
              <div className="flex items-center gap-3 min-w-0">
                <div className="flex-shrink-0 rounded-full bg-white/15 p-2">
                  <Clock className="h-5 w-5 text-gold-300" />
                </div>
                <div className="min-w-0">
                  <p className="font-medium text-sm sm:text-base truncate">
                    {isPendingPayment ? (
                      <>
                        Your <strong>{serviceLabel}</strong> is waiting!
                      </>
                    ) : (
                      <>
                        You have an unfinished <strong>{serviceLabel}</strong>
                      </>
                    )}
                  </p>
                  <p className="text-xs sm:text-sm text-white/70 truncate">
                    {isPendingPayment ? (
                      <>
                        <span className="inline-flex items-center gap-1.5">
                          Expires in{" "}
                          <span className="relative inline-block rounded-full bg-white/20 px-2 py-0.5 text-xs font-bold text-gold-200">
                            <span className="banner-shimmer absolute inset-0 rounded-full" />
                            <span className="relative">{minutesLeft} min</span>
                          </span>
                          {" "}— complete your payment
                        </span>
                      </>
                    ) : (
                      "Continue where you left off"
                    )}
                  </p>
                </div>
              </div>

              {/* Right: CTA + dismiss */}
              <div className="flex items-center gap-2 sm:gap-3 flex-shrink-0">
                <Link
                  href={`/book/${record.serviceSlug}`}
                  className="banner-glow-btn inline-flex items-center gap-2 rounded-full bg-white px-5 py-2.5 text-sm font-semibold text-primary-800 transition-all hover:bg-gold-100 hover:scale-105 active:scale-95 w-full sm:w-auto justify-center"
                >
                  {isPendingPayment ? "Complete Payment" : "Continue Booking"}
                  <ArrowRight className="h-4 w-4" />
                </Link>
                <button
                  onClick={() => setDismissed(true)}
                  className="flex-shrink-0 rounded-full p-2 text-white/60 hover:text-white hover:bg-white/10 transition-colors"
                  aria-label="Dismiss"
                >
                  <X className="h-4 w-4" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
