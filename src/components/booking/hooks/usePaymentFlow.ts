"use client";

import { useEffect, useState } from "react";
import { bookingsApi, paymentsApi } from "@/lib/api";

export type Currency = "INR" | "EUR";

export interface CreateBookingPayload {
  service_slug: string;
  service_title: string;
  date: string;
  time_slot: string;
  duration_minutes: number;
  user_name: string;
  user_email: string;
  user_phone: string;
  notes: string;
  date_of_birth: string;
  time_of_birth: string | null;
  birth_time_unknown: boolean;
  place_of_birth: string;
  birth_latitude: number;
  birth_longitude: number;
}

export interface UsePaymentFlow {
  bookingId: string;
  setBookingId: React.Dispatch<React.SetStateAction<string>>;
  price: number;
  setPrice: React.Dispatch<React.SetStateAction<number>>;
  priceEur: number;
  setPriceEur: React.Dispatch<React.SetStateAction<number>>;
  currency: Currency;
  setCurrency: React.Dispatch<React.SetStateAction<Currency>>;
  loading: boolean;
  error: string;
  /** Reset error state; useful when the user navigates between steps. */
  clearError: () => void;
  /** Create the booking server-side, persist a 15-min resume token, return the
   * booking id. Returns null on failure (error state is set). */
  createBooking: (
    payload: CreateBookingPayload,
    storageKey: string,
    serviceSlug: string,
    serviceTitle: string,
  ) => Promise<string | null>;
  /** Open a Stripe Checkout session and redirect the browser. */
  startCheckout: () => Promise<void>;
}

/** Owns currency detection, booking creation, and Stripe checkout redirect.
 *
 * Currency defaults to INR; on mount we ping ipapi.co and switch to EUR
 * for non-IN users. Failure to detect leaves us on INR.
 */
export function usePaymentFlow(): UsePaymentFlow {
  const [bookingId, setBookingId] = useState("");
  const [price, setPrice] = useState(0);
  const [priceEur, setPriceEur] = useState(0);
  const [currency, setCurrency] = useState<Currency>("INR");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // IP-based currency detection — silent fallback to INR on any failure.
  useEffect(() => {
    fetch("https://ipapi.co/json/")
      .then((r) => r.json())
      .then((data) => {
        if (data.country_code !== "IN") setCurrency("EUR");
      })
      .catch(() => {
        /* keep default INR */
      });
  }, []);

  async function createBooking(
    payload: CreateBookingPayload,
    storageKey: string,
    serviceSlug: string,
    serviceTitle: string,
  ): Promise<string | null> {
    setLoading(true);
    setError("");
    try {
      const booking = await bookingsApi.create(payload);
      setBookingId(booking.id);
      setPrice(booking.price_inr);
      setPriceEur(booking.price_eur ?? 0);

      if (typeof window !== "undefined") {
        localStorage.setItem(
          storageKey,
          JSON.stringify({
            bookingId: booking.id,
            createdAt: new Date().toISOString(),
            serviceSlug,
            serviceTitle,
          }),
        );
      }
      return booking.id;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create booking");
      return null;
    } finally {
      setLoading(false);
    }
  }

  async function startCheckout(): Promise<void> {
    if (!bookingId) {
      setError("Cannot start payment: no booking id");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const { checkout_url } = await paymentsApi.createCheckoutSession({
        booking_id: bookingId,
        currency,
      });
      if (typeof window !== "undefined") {
        window.location.href = checkout_url;
      }
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to create payment session",
      );
      setLoading(false);
    }
  }

  return {
    bookingId,
    setBookingId,
    price,
    setPrice,
    priceEur,
    setPriceEur,
    currency,
    setCurrency,
    loading,
    error,
    clearError: () => setError(""),
    createBooking,
    startCheckout,
  };
}
