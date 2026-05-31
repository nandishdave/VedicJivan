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
import { useBookingForm } from "./hooks/useBookingForm";
import { usePaymentFlow } from "./hooks/usePaymentFlow";
import { useResumableBooking } from "./hooks/useResumableBooking";
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

// Legacy slug list — kept as a fallback while existing service entries
// migrate to the new `isReport` flag on the Service interface.
const LEGACY_REPORT_SLUGS = ["premium-kundli", "numerology-report", "matchmaking"];

function isReportService(service: Service): boolean {
  return service.isReport === true || LEGACY_REPORT_SLUGS.includes(service.slug);
}

export function BookingWizard({ service }: BookingWizardProps) {
  const isReport = isReportService(service);
  const storageKey = `vedicjivan_pending_booking_${service.slug}`;
  const fixedDuration = parseDurationMinutes(service.duration);

  const [step, setStep] = useState<Step>(isReport ? "details" : "date");
  const [selectedDate, setSelectedDate] = useState("");
  const [selectedSlot, setSelectedSlot] = useState("");
  const [selectedDuration, setSelectedDuration] = useState(0);
  const wizardRef = useRef<HTMLDivElement>(null);

  const form = useBookingForm();
  const payment = usePaymentFlow();
  const resume = useResumableBooking(storageKey);

  // Apply restored partial progress from localStorage (date/time selections
  // saved before the booking record was created).
  useEffect(() => {
    if (!resume.partialProgress) return;
    const { date, timeSlot, duration } = resume.partialProgress;
    if (date) setSelectedDate(date);
    if (timeSlot) setSelectedSlot(timeSlot);
    if (duration) setSelectedDuration(duration);
    if (timeSlot) {
      setStep("details");
    } else if (date) {
      setStep("time");
    }
  }, [resume.partialProgress]);

  const steps: { key: Step; label: string; icon: React.ReactNode }[] = isReport
    ? [
        { key: "details", label: "Your Details", icon: <User className="h-4 w-4" /> },
        { key: "review", label: "Review", icon: <CheckCircle2 className="h-4 w-4" /> },
        { key: "payment", label: "Payment", icon: <CreditCard className="h-4 w-4" /> },
      ]
    : [
        { key: "date", label: "Date", icon: <Calendar className="h-4 w-4" /> },
        { key: "time", label: "Time", icon: <Clock className="h-4 w-4" /> },
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
    if (step === "details") {
      form.persistDetails();
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
    if (!resume.resumeBooking) return;
    const b = resume.resumeBooking;
    payment.setBookingId(b.id);
    payment.setPrice(b.price_inr);
    payment.setPriceEur(b.price_eur ?? 0);
    setSelectedDate(b.date);
    setSelectedSlot(b.time_slot);
    setSelectedDuration(b.duration_minutes);
    form.setFormData((prev) => ({
      ...prev,
      name: b.user_name,
      email: b.user_email,
      phone: b.user_phone,
    }));
    resume.acceptResume();
    setStep("payment");
  };

  const handleCreateBooking = async () => {
    // If booking was already created (user came back from payment), skip ahead.
    if (payment.bookingId) {
      setStep("payment");
      return;
    }

    const id = await payment.createBooking(
      {
        service_slug: service.slug,
        service_title: service.title,
        date: isReport ? new Date().toISOString().split("T")[0] : selectedDate,
        time_slot: isReport ? "00:00" : selectedSlot,
        duration_minutes: isReport ? 0 : selectedDuration,
        user_name: form.formData.name,
        user_email: form.formData.email,
        user_phone: form.formData.phone,
        notes: form.formData.notes,
        date_of_birth: form.formData.dateOfBirth,
        time_of_birth: form.formData.birthTimeUnknown
          ? null
          : `${form.formData.birthTimeHour}:${form.formData.birthTimeMinute} ${form.formData.birthTimePeriod}`,
        birth_time_unknown: form.formData.birthTimeUnknown,
        place_of_birth: form.formData.placeOfBirth,
        birth_latitude: form.formData.birthLatitude,
        birth_longitude: form.formData.birthLongitude,
      },
      storageKey,
      service.slug,
      service.title,
    );

    if (id) setStep("payment");
  };

  if (resume.checking) {
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
          Thank you, {form.formData.name}. Your {service.title} has been booked successfully.
        </p>
        <div className="mt-4 rounded-lg bg-gray-50 dark:bg-dark-surface-raised p-4 text-sm text-gray-700 dark:text-gray-300 space-y-1">
          <p><strong>Booking ID:</strong> <span className="font-mono text-xs">{payment.bookingId}</span></p>
          {!isReport && (
            <>
              <p><strong>Date:</strong> {selectedDate}</p>
              <p><strong>Time:</strong> {selectedSlot}</p>
              <p><strong>Duration:</strong> {selectedDuration} minutes</p>
            </>
          )}
          <p><strong>Amount Paid:</strong> {payment.currency === "EUR" ? `\u20AC${payment.priceEur}` : `\u20B9${payment.price}`}</p>
        </div>
        <p className="mt-4 text-sm text-gray-500 dark:text-gray-400">
          A confirmation email with meeting details has been sent to {form.formData.email}.
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

      {resume.showResumePrompt && resume.resumeBooking && (
        <div className="mb-6 rounded-xl border-2 border-amber-300 dark:border-amber-600 bg-amber-50 dark:bg-amber-900/20 p-5">
          <h3 className="font-heading text-lg font-bold text-amber-800 dark:text-amber-300">
            Resume Your Booking?
          </h3>
          <p className="mt-1 text-sm text-amber-700 dark:text-amber-300">
            You have a pending {resume.resumeBooking.service_title} booking
            {resume.resumeBooking.duration_minutes > 0 &&
              ` for ${resume.resumeBooking.date} at ${resume.resumeBooking.time_slot}`}
            . Would you like to continue to payment?
          </p>
          <div className="mt-4 flex gap-3">
            <Button variant="primary" onClick={handleResumeBooking}>
              Resume & Pay
            </Button>
            <Button variant="ghost" onClick={resume.startFresh}>
              Start Fresh
            </Button>
          </div>
        </div>
      )}

      {payment.error && (
        <div className="mb-4 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 p-3 text-sm text-red-700 dark:text-red-400">
          {payment.error}
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
                if (typeof window !== "undefined") {
                  localStorage.setItem(
                    storageKey,
                    JSON.stringify({
                      serviceSlug: service.slug,
                      serviceTitle: service.title,
                      date: selectedDate,
                      timeSlot: slot,
                      duration: fixedDuration,
                      savedAt: new Date().toISOString(),
                    }),
                  );
                }
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
                  value={form.formData.name}
                  onChange={(e) => form.setFormData({ ...form.formData, name: e.target.value })}
                  className="w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500 dark:border-gray-600 dark:bg-dark-surface-card dark:text-gray-200"
                  placeholder="Enter your full name"
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">Email *</label>
                <input
                  type="email"
                  value={form.formData.email}
                  onChange={(e) => form.setFormData({ ...form.formData, email: e.target.value })}
                  className="w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500 dark:border-gray-600 dark:bg-dark-surface-card dark:text-gray-200"
                  placeholder="you@example.com"
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">Phone *</label>
                <input
                  type="tel"
                  value={form.formData.phone}
                  onChange={(e) => form.setFormData({ ...form.formData, phone: e.target.value })}
                  className="w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500 dark:border-gray-600 dark:bg-dark-surface-card dark:text-gray-200"
                  placeholder="+91 98765 43210"
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">Notes *</label>
                <textarea
                  value={form.formData.notes}
                  onChange={(e) => form.setFormData({ ...form.formData, notes: e.target.value })}
                  rows={3}
                  className="w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500 dark:border-gray-600 dark:bg-dark-surface-card dark:text-gray-200"
                  placeholder="Please describe what you'd like to discuss or need help with"
                />
              </div>

              <div>
                <label className="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">Date of Birth *</label>
                <DateOfBirthPicker
                  selectedDate={form.formData.dateOfBirth}
                  onDateSelect={(date) => form.setFormData({ ...form.formData, dateOfBirth: date })}
                />
              </div>

              <div>
                <label className="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">Time of Birth</label>
                <TimeOfBirthPicker
                  value={
                    form.formData.birthTimeUnknown
                      ? null
                      : {
                          hour: form.formData.birthTimeHour,
                          minute: form.formData.birthTimeMinute,
                          period: form.formData.birthTimePeriod,
                        }
                  }
                  isUnknown={form.formData.birthTimeUnknown}
                  onTimeChange={(time) =>
                    form.setFormData({
                      ...form.formData,
                      birthTimeHour: time.hour,
                      birthTimeMinute: time.minute,
                      birthTimePeriod: time.period,
                    })
                  }
                  onUnknownChange={(unknown) =>
                    form.setFormData({ ...form.formData, birthTimeUnknown: unknown })
                  }
                />
              </div>

              <div>
                <label className="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">Place of Birth *</label>
                <PlaceOfBirthAutocomplete
                  value={form.formData.placeOfBirth}
                  onPlaceSelect={(place) =>
                    form.setFormData({
                      ...form.formData,
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
                <span className="font-medium">{form.formData.name}</span>
              </div>
              <div className="flex justify-between text-sm dark:text-gray-300">
                <span className="text-gray-500 dark:text-gray-400">Email</span>
                <span className="font-medium">{form.formData.email}</span>
              </div>
              <div className="flex justify-between text-sm dark:text-gray-300">
                <span className="text-gray-500 dark:text-gray-400">Phone</span>
                <span className="font-medium">{form.formData.phone}</span>
              </div>
              {form.formData.notes && (
                <div className="flex justify-between text-sm dark:text-gray-300">
                  <span className="text-gray-500 dark:text-gray-400">Notes</span>
                  <span className="font-medium max-w-[60%] text-right">{form.formData.notes}</span>
                </div>
              )}
              <div className="flex justify-between text-sm dark:text-gray-300">
                <span className="text-gray-500 dark:text-gray-400">Date of Birth</span>
                <span className="font-medium">{form.formData.dateOfBirth}</span>
              </div>
              <div className="flex justify-between text-sm dark:text-gray-300">
                <span className="text-gray-500 dark:text-gray-400">Time of Birth</span>
                <span className="font-medium">
                  {form.formData.birthTimeUnknown
                    ? "Unknown"
                    : `${form.formData.birthTimeHour}:${form.formData.birthTimeMinute} ${form.formData.birthTimePeriod}`}
                </span>
              </div>
              <div className="flex justify-between text-sm dark:text-gray-300">
                <span className="text-gray-500 dark:text-gray-400">Place of Birth</span>
                <span className="font-medium max-w-[60%] text-right">{form.formData.placeOfBirth}</span>
              </div>
              <hr className="border-gray-200 dark:border-gray-600" />
              <div className="flex justify-between text-base font-bold dark:text-gray-100">
                <span>Price</span>
                <span className="text-primary-600 dark:text-primary-400">
                  {payment.currency === "EUR" ? service.priceEUR : service.priceINR}
                </span>
              </div>
            </div>
          </div>
        )}

        {step === "payment" && (
          <div className="text-center py-8">
            <CreditCard className="mx-auto mb-4 h-12 w-12 text-primary-600 dark:text-primary-400" />
            <h3 className="mb-2 font-heading text-xl font-bold dark:text-gray-100">Complete Payment</h3>

            {/* Currency toggle */}
            <div className="mb-5 inline-flex items-center gap-1 rounded-full border border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-dark-surface p-1">
              <button
                type="button"
                onClick={() => payment.setCurrency("INR")}
                className={`rounded-full px-4 py-1.5 text-sm font-medium transition-colors ${payment.currency === "INR" ? "bg-primary-600 text-white shadow" : "text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"}`}
              >
                🇮🇳 ₹ INR
              </button>
              <button
                type="button"
                onClick={() => payment.setCurrency("EUR")}
                className={`rounded-full px-4 py-1.5 text-sm font-medium transition-colors ${payment.currency === "EUR" ? "bg-primary-600 text-white shadow" : "text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"}`}
              >
                🌍 € EUR
              </button>
            </div>

            <p className="mb-6 text-gray-600 dark:text-gray-400">
              Amount:{" "}
              <strong className="text-primary-600 dark:text-primary-400">
                {payment.currency === "EUR" ? `\u20AC${payment.priceEur}` : `\u20B9${payment.price}`}
              </strong>
            </p>
            <Button
              variant="gold"
              size="lg"
              onClick={payment.startCheckout}
              disabled={payment.loading}
            >
              {payment.loading
                ? "Processing..."
                : payment.currency === "EUR"
                  ? `Pay \u20AC${payment.priceEur}`
                  : `Pay \u20B9${payment.price}`}
            </Button>
            <p className="mt-4 text-xs text-gray-400 dark:text-gray-500">
              Secured by Stripe. Supports Cards & major payment methods.
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
              disabled={payment.loading}
            >
              {payment.loading ? "Creating..." : "Proceed to Payment"}
              <ArrowRight className="h-4 w-4" />
            </Button>
          ) : (
            <Button
              variant="primary"
              onClick={handleNext}
              disabled={
                (step === "date" && !selectedDate) ||
                (step === "time" && !selectedSlot) ||
                (step === "details" && !form.isComplete)
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
