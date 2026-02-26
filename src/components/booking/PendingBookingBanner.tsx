"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Clock, X } from "lucide-react";

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
const EXPIRY_MS = 15 * 60 * 1000; // 15 minutes

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

        // For bookings with bookingId, check 15-min expiry
        if (data.bookingId && Date.now() - timestamp > EXPIRY_MS) {
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
        setMinutesLeft(Math.max(1, Math.ceil((EXPIRY_MS - elapsed) / 60000)));
      }
    }
  }, [isBookingPage, pathname]);

  // Live countdown for pending-payment bookings
  useEffect(() => {
    if (!record?.bookingId || !record.createdAt) return;

    const interval = setInterval(() => {
      const elapsed = Date.now() - new Date(record.createdAt!).getTime();
      const remaining = Math.ceil((EXPIRY_MS - elapsed) / 60000);
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

  return (
    <div className="bg-amber-50 border-b border-amber-200">
      <div className="mx-auto max-w-7xl px-4 py-3 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between gap-4">
          <div className="flex items-center gap-3 min-w-0">
            <Clock className="h-5 w-5 flex-shrink-0 text-amber-600" />
            <p className="text-sm text-amber-800 truncate">
              {isPendingPayment ? (
                <>
                  Your <strong>{record.serviceTitle || "booking"}</strong> expires in{" "}
                  <strong>{minutesLeft} min</strong> —{" "}
                  <Link
                    href={`/book/${record.serviceSlug}`}
                    className="font-semibold underline hover:text-amber-900"
                  >
                    click here to complete payment
                  </Link>
                </>
              ) : (
                <>
                  You have an unfinished <strong>{record.serviceTitle || "booking"}</strong> —{" "}
                  <Link
                    href={`/book/${record.serviceSlug}`}
                    className="font-semibold underline hover:text-amber-900"
                  >
                    click here to continue
                  </Link>
                </>
              )}
            </p>
          </div>
          <button
            onClick={() => setDismissed(true)}
            className="flex-shrink-0 rounded p-1 text-amber-600 hover:bg-amber-100 hover:text-amber-800"
            aria-label="Dismiss"
          >
            <X className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
