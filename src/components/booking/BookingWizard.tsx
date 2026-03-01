"use client";

import { useState, useEffect, useRef } from "react";
import {
  Calendar,
  Clock,
  User,
  CreditCard,
  CheckCircle2,
  ArrowLeft,
  ArrowRight,
} from "lucide-react";
import { Button } from "@/components/ui/Button";
import { BookingCalendar } from "./BookingCalendar";
import { TimeSlotPicker } from "./TimeSlotPicker";
import { DateOfBirthPicker } from "./DateOfBirthPicker";
import { TimeOfBirthPicker } from "./TimeOfBirthPicker";
import { PlaceOfBirthAutocomplete } from "./PlaceOfBirthAutocomplete";
import { bookingsApi, paymentsApi, type Booking } from "@/lib/api";
import type { Service } from "@/data/services";

interface BookingWizardProps {
  service: Service;
}

type Step = "date" | "time" | "details" | "review" | "payment" | "confirmed";

/** Parse the service.duration string (e.g. "30 min") into minutes, or 0 if null */
function parseDurationMinutes(duration: string | null): number {
  if (!duration) return 0;
  const match = duration.match(/(\d+)/);
  return match ? parseInt(match[1], 10) : 0;
}

// Reports don't need scheduling
const REPORT_SERVICES = ["premium-kundli", "numerology-report", "matchmaking", "test-payment"];

declare global {
  interface Window {
    Razorpay: new (options: Record<string, unknown>) => { open: () => void };
  }
}

const USER_DETAILS_KEY = "vedicjivan_user_details";

/** Load previously saved user details from localStorage (excludes booking-specific notes). */
function loadSavedUserDetails() {
  try {
    const stored = localStorage.getItem(USER_DETAILS_KEY);
    if (!stored) return null;
    return JSON.parse(stored);
  } catch {
    return null;
  }
}

/** Save personal details so they pre-fill on future bookings. */
function saveUserDetails(formData: Record<string, unknown>) {
  const { notes, ...details } = formData;
  void notes; // notes are booking-specific, not saved
  localStorage.setItem(USER_DETAILS_KEY, JSON.stringify(details));
}

export function BookingWizard({ service }: BookingWizardProps) {
  const isReport = REPORT_SERVICES.includes(service.slug);

  const [step, setStep] = useState<Step>(isReport ? "details" : "date");
  const [selectedDate, setSelectedDate] = useState("");
  const [selectedSlot, setSelectedSlot] = useState("");
  const [selectedDuration, setSelectedDuration] = useState(0);
  const [formData, setFormData] = useState(() => {
    const saved = loadSavedUserDetails();
    return {
      name: saved?.name ?? "",
      email: saved?.email ?? "",
      phone: saved?.phone ?? "",
      notes: "", // always blank — booking-specific
      dateOfBirth: saved?.dateOfBirth ?? "",
      birthTimeHour: saved?.birthTimeHour ?? "12",
      birthTimeMinute: saved?.birthTimeMinute ?? "00",
      birthTimePeriod: (saved?.birthTimePeriod ?? "AM") as "AM" | "PM",
      birthTimeUnknown: saved?.birthTimeUnknown ?? false,
      placeOfBirth: saved?.placeOfBirth ?? "",
      birthLatitude: saved?.birthLatitude ?? 0,
      birthLongitude: saved?.birthLongitude ?? 0,
    };
  });
  const [bookingId, setBookingId] = useState("");
  const [price, setPrice] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [resumeBooking, setResumeBooking] = useState<Booking | null>(null);
  const [showResumePrompt, setShowResumePrompt] = useState(false);
  const [checkingResume, setCheckingResume] = useState(true);
  const wizardRef = useRef<HTMLDivElement>(null);

  const storageKey = `vedicjivan_pending_booking_${service.slug}`;

  // Check for a pending booking in localStorage on mount
  useEffect(() => {
    const checkPendingBooking = async () => {
      try {
        const stored = localStorage.getItem(storageKey);
        if (!stored) {
          setCheckingResume(false);
          return;
        }

        const record = JSON.parse(stored);

        if (record.bookingId) {
          // Full booking exists — check 15-min expiry
          const elapsed = Date.now() - new Date(record.createdAt).getTime();
          if (elapsed > 15 * 60 * 1000) {
            localStorage.removeItem(storageKey);
            setCheckingResume(false);
            return;
          }

          // Server-side validation
          const booking = await bookingsApi.resume(record.bookingId);
          setResumeBooking(booking);
          setShowResumePrompt(true);
        } else {
          // Partial progress — check 2-hour expiry
          const savedAt = record.savedAt ? new Date(record.savedAt).getTime() : 0;
          if (savedAt && Date.now() - savedAt > 2 * 60 * 60 * 1000) {
            localStorage.removeItem(storageKey);
            setCheckingResume(false);
            return;
          }
          // Restore selections
          if (record.date) setSelectedDate(record.date);
          if (record.timeSlot) setSelectedSlot(record.timeSlot);
          if (record.duration) setSelectedDuration(record.duration);

          // Jump to the furthest step
          if (record.timeSlot) {
            setStep("details");
          } else if (record.date) {
            setStep("time");
          }
        }
      } catch {
        localStorage.removeItem(storageKey);
      } finally {
        setCheckingResume(false);
      }
    };

    checkPendingBooking();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Fixed duration from the service definition (e.g. "30 min" → 30)
  const fixedDuration = parseDurationMinutes(service.duration);

  const steps: { key: Step; label: string; icon: React.ReactNode }[] = isReport
    ? [
        { key: "details", label: "Your Details", icon: <User className="h-4 w-4" /> },
        { key: "review", label: "Review", icon: <CheckCircle2 className="h-4 w-4" /> },
        { key: "payment", label: "Payment", icon: <CreditCard className="h-4 w-4" /> },
      ]
    : [
        { key: "date", label: "Date", icon: <Calendar className="h-4 w-4" /> },
        { key: "time", label: "Time", icon: <Clock className="h-4 w-4" /> },
        // Skip the duration step — service already defines a fixed duration
        { key: "details", label: "Details", icon: <User className="h-4 w-4" /> },
        { key: "review", label: "Review", icon: <CheckCircle2 className="h-4 w-4" /> },
        { key: "payment", label: "Payment", icon: <CreditCard className="h-4 w-4" /> },
      ];

  const currentStepIndex = steps.findIndex((s) => s.key === step);

  // Scroll to the top of the wizard when the step changes
  useEffect(() => {
    if (wizardRef.current && typeof wizardRef.current.scrollIntoView === "function") {
      wizardRef.current.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }, [step]);

  const handleNext = () => {
    // Persist personal details when leaving the details step
    if (step === "details") {
      saveUserDetails(formData);
    }
    if (currentStepIndex < steps.length - 1) {
      setStep(steps[currentStepIndex + 1].key);
    }
  };

  const handleBack = () => {
    if (currentStepIndex > 0) {
      setStep(steps[currentStepIndex - 1].key);
    }
  };

  const handleResumeBooking = () => {
    if (!resumeBooking) return;
    setBookingId(resumeBooking.id);
    setPrice(resumeBooking.price_inr);
    setSelectedDate(resumeBooking.date);
    setSelectedSlot(resumeBooking.time_slot);
    setSelectedDuration(resumeBooking.duration_minutes);
    setFormData((prev) => ({
      ...prev,
      name: resumeBooking.user_name,
      email: resumeBooking.user_email,
      phone: resumeBooking.user_phone,
    }));
    setShowResumePrompt(false);
    setStep("payment");
  };

  const handleStartFresh = () => {
    localStorage.removeItem(storageKey);
    setShowResumePrompt(false);
    setResumeBooking(null);
  };

  const handleCreateBooking = async () => {
    // If booking was already created (user came back from payment), skip to payment
    if (bookingId) {
      setStep("payment");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const booking = await bookingsApi.create({
        service_slug: service.slug,
        service_title: service.title,
        date: isReport ? new Date().toISOString().split("T")[0] : selectedDate,
        time_slot: isReport ? "00:00" : selectedSlot,
        duration_minutes: isReport ? 0 : selectedDuration,
        user_name: formData.name,
        user_email: formData.email,
        user_phone: formData.phone,
        notes: formData.notes,
        date_of_birth: formData.dateOfBirth,
        time_of_birth: formData.birthTimeUnknown
          ? null
          : `${formData.birthTimeHour}:${formData.birthTimeMinute} ${formData.birthTimePeriod}`,
        birth_time_unknown: formData.birthTimeUnknown,
        place_of_birth: formData.placeOfBirth,
        birth_latitude: formData.birthLatitude,
        birth_longitude: formData.birthLongitude,
      });

      setBookingId(booking.id);
      setPrice(booking.price_inr);

      // Save to localStorage so user can resume if they leave
      localStorage.setItem(
        storageKey,
        JSON.stringify({
          bookingId: booking.id,
          createdAt: new Date().toISOString(),
          serviceSlug: service.slug,
          serviceTitle: service.title,
        })
      );

      setStep("payment");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create booking");
    } finally {
      setLoading(false);
    }
  };

  const handlePayment = async () => {
    setLoading(true);
    setError("");

    try {
      const order = await paymentsApi.createOrder({
        booking_id: bookingId,
        amount_inr: price,
      });

      // Load Razorpay script
      const script = document.createElement("script");
      script.src = "https://checkout.razorpay.com/v1/checkout.js";
      script.onload = () => {
        const rzp = new window.Razorpay({
          key: order.key_id,
          amount: order.amount,
          currency: order.currency,
          order_id: order.order_id,
          name: "VedicJivan",
          description: service.title,
          handler: async (response: { razorpay_order_id: string; razorpay_payment_id: string; razorpay_signature: string }) => {
            try {
              await paymentsApi.verify({
                razorpay_order_id: response.razorpay_order_id,
                razorpay_payment_id: response.razorpay_payment_id,
                razorpay_signature: response.razorpay_signature,
                booking_id: bookingId,
              });
              localStorage.removeItem(storageKey);
              setStep("confirmed");
            } catch {
              setError("Payment verification failed. Please contact support.");
            }
          },
          prefill: {
            name: formData.name,
            email: formData.email,
            contact: formData.phone,
          },
          theme: { color: "#7c3aed" },
        });
        rzp.open();
        setLoading(false);
      };
      document.body.appendChild(script);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create payment");
      setLoading(false);
    }
  };

  if (checkingResume) {
    return (
      <div className="mx-auto max-w-2xl text-center py-8 text-gray-500 dark:text-gray-400">
        Loading...
      </div>
    );
  }

  if (step === "confirmed") {
    return (
      <div className="mx-auto max-w-lg text-center py-12">
        <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-green-100 dark:bg-green-900/30">
          <CheckCircle2 className="h-8 w-8 text-green-600 dark:text-green-400" />
        </div>
        <h2 className="font-heading text-2xl font-bold text-vedic-dark dark:text-gray-100">Booking Confirmed!</h2>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
          Thank you, {formData.name}. Your {service.title} has been booked successfully.
        </p>
        <div className="mt-4 rounded-lg bg-gray-50 dark:bg-dark-surface-raised p-4 text-sm text-gray-700 dark:text-gray-300 space-y-1">
          <p><strong>Booking ID:</strong> <span className="font-mono text-xs">{bookingId}</span></p>
          {!isReport && (
            <>
              <p><strong>Date:</strong> {selectedDate}</p>
              <p><strong>Time:</strong> {selectedSlot}</p>
              <p><strong>Duration:</strong> {selectedDuration} minutes</p>
            </>
          )}
          <p><strong>Amount Paid:</strong> {"\u20B9"}{price}</p>
        </div>
        <p className="mt-4 text-sm text-gray-500 dark:text-gray-400">
          A confirmation email with meeting details has been sent to {formData.email}.
        </p>
        <p className="mt-1 text-xs text-gray-400 dark:text-gray-500">
          Please save your Booking ID for reference.
        </p>
      </div>
    );
  }

  return (
    <div ref={wizardRef} className="mx-auto max-w-2xl scroll-mt-24">
      {/* Progress bar */}
      <div className="mb-8 flex items-center justify-center gap-2">
        {steps.map((s, i) => (
          <div key={s.key} className="flex items-center">
            <div
              className={`flex items-center gap-1 rounded-full px-3 py-1.5 text-xs font-medium ${
                i <= currentStepIndex
                  ? "bg-primary-100 dark:bg-primary-900/30 text-primary-700"
                  : "bg-gray-100 dark:bg-gray-800 text-gray-400"
              }`}
            >
              {s.icon}
              <span className="hidden sm:inline">{s.label}</span>
            </div>
            {i < steps.length - 1 && (
              <div
                className={`mx-1 h-0.5 w-4 sm:w-8 ${
                  i < currentStepIndex ? "bg-primary-400" : "bg-gray-200 dark:bg-gray-700"
                }`}
              />
            )}
          </div>
        ))}
      </div>

      {showResumePrompt && resumeBooking && (
        <div className="mb-6 rounded-xl border-2 border-amber-300 dark:border-amber-600 bg-amber-50 dark:bg-amber-900/20 p-5">
          <h3 className="font-heading text-lg font-bold text-amber-800 dark:text-amber-300">
            Resume Your Booking?
          </h3>
          <p className="mt-1 text-sm text-amber-700 dark:text-amber-300">
            You have a pending {resumeBooking.service_title} booking
            {resumeBooking.duration_minutes > 0 && ` for ${resumeBooking.date} at ${resumeBooking.time_slot}`}.
            Would you like to continue to payment?
          </p>
          <div className="mt-4 flex gap-3">
            <Button variant="primary" onClick={handleResumeBooking}>
              Resume & Pay
            </Button>
            <Button variant="ghost" onClick={handleStartFresh}>
              Start Fresh
            </Button>
          </div>
        </div>
      )}

      {error && (
        <div className="mb-4 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 p-3 text-sm text-red-700 dark:text-red-400">
          {error}
        </div>
      )}

      {/* Step content */}
      <div className="min-h-[300px]">
        {step === "date" && (
          <div>
            <h3 className="mb-4 font-heading text-xl font-bold dark:text-gray-100">Select a Date</h3>
            <BookingCalendar
              selectedDate={selectedDate}
              onDateSelect={(date) => {
                setSelectedDate(date);
                setSelectedSlot("");
                setSelectedDuration(0);
              }}
            />
          </div>
        )}

        {step === "time" && (
          <div>
            <h3 className="mb-4 font-heading text-xl font-bold dark:text-gray-100">
              Select a Time Slot
            </h3>
            <p className="mb-4 text-sm text-gray-500 dark:text-gray-400">Date: {selectedDate}</p>
            <TimeSlotPicker
              date={selectedDate}
              selectedSlot={selectedSlot}
              onSlotSelect={(slot) => {
                setSelectedSlot(slot);
                setSelectedDuration(fixedDuration);
                // Save partial progress
                localStorage.setItem(
                  storageKey,
                  JSON.stringify({
                    serviceSlug: service.slug,
                    serviceTitle: service.title,
                    date: selectedDate,
                    timeSlot: slot,
                    duration: fixedDuration,
                    savedAt: new Date().toISOString(),
                  })
                );
              }}
            />
          </div>
        )}

        {step === "details" && (
          <div>
            <h3 className="mb-4 font-heading text-xl font-bold dark:text-gray-100">Your Details</h3>
            <div className="space-y-4">
              <div>
                <label className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">Full Name *</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500 dark:border-gray-600 dark:bg-dark-surface-card dark:text-gray-200"
                  placeholder="Enter your full name"
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">Email *</label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500 dark:border-gray-600 dark:bg-dark-surface-card dark:text-gray-200"
                  placeholder="you@example.com"
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">Phone *</label>
                <input
                  type="tel"
                  value={formData.phone}
                  onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                  className="w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500 dark:border-gray-600 dark:bg-dark-surface-card dark:text-gray-200"
                  placeholder="+91 98765 43210"
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">Notes *</label>
                <textarea
                  value={formData.notes}
                  onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                  rows={3}
                  className="w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500 dark:border-gray-600 dark:bg-dark-surface-card dark:text-gray-200"
                  placeholder="Please describe what you'd like to discuss or need help with"
                />
              </div>

              <div>
                <label className="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">Date of Birth *</label>
                <DateOfBirthPicker
                  selectedDate={formData.dateOfBirth}
                  onDateSelect={(date) => setFormData({ ...formData, dateOfBirth: date })}
                />
              </div>

              <div>
                <label className="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">Time of Birth</label>
                <TimeOfBirthPicker
                  value={
                    formData.birthTimeUnknown
                      ? null
                      : {
                          hour: formData.birthTimeHour,
                          minute: formData.birthTimeMinute,
                          period: formData.birthTimePeriod,
                        }
                  }
                  isUnknown={formData.birthTimeUnknown}
                  onTimeChange={(time) =>
                    setFormData({
                      ...formData,
                      birthTimeHour: time.hour,
                      birthTimeMinute: time.minute,
                      birthTimePeriod: time.period,
                    })
                  }
                  onUnknownChange={(unknown) =>
                    setFormData({ ...formData, birthTimeUnknown: unknown })
                  }
                />
              </div>

              <div>
                <label className="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">Place of Birth *</label>
                <PlaceOfBirthAutocomplete
                  value={formData.placeOfBirth}
                  onPlaceSelect={(place) =>
                    setFormData({
                      ...formData,
                      placeOfBirth: place.name,
                      birthLatitude: place.latitude,
                      birthLongitude: place.longitude,
                    })
                  }
                />
              </div>
            </div>
          </div>
        )}

        {step === "review" && (
          <div>
            <h3 className="mb-4 font-heading text-xl font-bold dark:text-gray-100">Review Your Booking</h3>
            <div className="rounded-xl border border-gray-200 dark:border-gray-600 bg-gray-50 dark:bg-dark-surface-raised p-6 space-y-3">
              <div className="flex justify-between text-sm dark:text-gray-300">
                <span className="text-gray-500 dark:text-gray-400">Service</span>
                <span className="font-medium">{service.title}</span>
              </div>
              {!isReport && (
                <>
                  <div className="flex justify-between text-sm dark:text-gray-300">
                    <span className="text-gray-500 dark:text-gray-400">Date</span>
                    <span className="font-medium">{selectedDate}</span>
                  </div>
                  <div className="flex justify-between text-sm dark:text-gray-300">
                    <span className="text-gray-500 dark:text-gray-400">Time</span>
                    <span className="font-medium">{selectedSlot}</span>
                  </div>
                  <div className="flex justify-between text-sm dark:text-gray-300">
                    <span className="text-gray-500 dark:text-gray-400">Duration</span>
                    <span className="font-medium">{selectedDuration} minutes</span>
                  </div>
                </>
              )}
              <div className="flex justify-between text-sm dark:text-gray-300">
                <span className="text-gray-500 dark:text-gray-400">Name</span>
                <span className="font-medium">{formData.name}</span>
              </div>
              <div className="flex justify-between text-sm dark:text-gray-300">
                <span className="text-gray-500 dark:text-gray-400">Email</span>
                <span className="font-medium">{formData.email}</span>
              </div>
              <div className="flex justify-between text-sm dark:text-gray-300">
                <span className="text-gray-500 dark:text-gray-400">Phone</span>
                <span className="font-medium">{formData.phone}</span>
              </div>
              {formData.notes && (
                <div className="flex justify-between text-sm dark:text-gray-300">
                  <span className="text-gray-500 dark:text-gray-400">Notes</span>
                  <span className="font-medium max-w-[60%] text-right">{formData.notes}</span>
                </div>
              )}
              <div className="flex justify-between text-sm dark:text-gray-300">
                <span className="text-gray-500 dark:text-gray-400">Date of Birth</span>
                <span className="font-medium">{formData.dateOfBirth}</span>
              </div>
              <div className="flex justify-between text-sm dark:text-gray-300">
                <span className="text-gray-500 dark:text-gray-400">Time of Birth</span>
                <span className="font-medium">
                  {formData.birthTimeUnknown
                    ? "Unknown"
                    : `${formData.birthTimeHour}:${formData.birthTimeMinute} ${formData.birthTimePeriod}`}
                </span>
              </div>
              <div className="flex justify-between text-sm dark:text-gray-300">
                <span className="text-gray-500 dark:text-gray-400">Place of Birth</span>
                <span className="font-medium max-w-[60%] text-right">{formData.placeOfBirth}</span>
              </div>
              <hr className="border-gray-200 dark:border-gray-600" />
              <div className="flex justify-between text-base font-bold dark:text-gray-100">
                <span>Price</span>
                <span className="text-primary-600 dark:text-primary-400">{service.priceINR}</span>
              </div>
            </div>
          </div>
        )}

        {step === "payment" && (
          <div className="text-center py-8">
            <CreditCard className="mx-auto mb-4 h-12 w-12 text-primary-600 dark:text-primary-400" />
            <h3 className="mb-2 font-heading text-xl font-bold dark:text-gray-100">Complete Payment</h3>
            <p className="mb-6 text-gray-600 dark:text-gray-400">
              Amount: <strong className="text-primary-600 dark:text-primary-400">{"\u20B9"}{price}</strong>
            </p>
            <Button
              variant="gold"
              size="lg"
              onClick={handlePayment}
              disabled={loading}
            >
              {loading ? "Processing..." : `Pay \u20B9${price}`}
            </Button>
            <p className="mt-4 text-xs text-gray-400 dark:text-gray-500">
              Secured by Razorpay. Supports UPI, Cards, Wallets & Netbanking.
            </p>
            <button
              type="button"
              onClick={() => setStep("review")}
              className="mt-4 inline-flex items-center gap-1 text-sm text-primary-600 dark:text-primary-400 hover:text-primary-800 dark:hover:text-primary-300 underline"
            >
              <ArrowLeft className="h-3 w-3" />
              Go back & edit details
            </button>
          </div>
        )}
      </div>

      {/* Navigation buttons */}
      {step !== "payment" && (
        <div className="mt-8 flex items-center justify-between">
          <Button
            variant="ghost"
            onClick={handleBack}
            disabled={currentStepIndex === 0}
          >
            <ArrowLeft className="h-4 w-4" />
            Back
          </Button>

          {step === "review" ? (
            <Button
              variant="primary"
              onClick={handleCreateBooking}
              disabled={loading}
            >
              {loading ? "Creating..." : "Proceed to Payment"}
              <ArrowRight className="h-4 w-4" />
            </Button>
          ) : (
            <Button
              variant="primary"
              onClick={handleNext}
              disabled={
                (step === "date" && !selectedDate) ||
                (step === "time" && !selectedSlot) ||
                (step === "details" &&
                  (!formData.name ||
                    !formData.email ||
                    !formData.phone ||
                    !formData.notes ||
                    !formData.dateOfBirth ||
                    !formData.placeOfBirth))
              }
            >
              Next
              <ArrowRight className="h-4 w-4" />
            </Button>
          )}
        </div>
      )}
    </div>
  );
}
