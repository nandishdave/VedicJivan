"use client";

import { useState } from "react";
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
import { bookingsApi, paymentsApi } from "@/lib/api";
import type { Service } from "@/data/services";

interface BookingWizardProps {
  service: Service;
}

type Step = "date" | "time" | "duration" | "details" | "review" | "payment" | "confirmed";

const DURATION_OPTIONS: Record<string, { label: string; minutes: number }[]> = {
  "call-consultation": [
    { label: "30 minutes", minutes: 30 },
    { label: "45 minutes", minutes: 45 },
    { label: "60 minutes", minutes: 60 },
  ],
  "video-consultation": [
    { label: "30 minutes", minutes: 30 },
    { label: "45 minutes", minutes: 45 },
    { label: "60 minutes", minutes: 60 },
  ],
  "vastu-consultation": [
    { label: "30 minutes", minutes: 30 },
    { label: "45 minutes", minutes: 45 },
    { label: "60 minutes", minutes: 60 },
  ],
  "astrological-consulting": [
    { label: "30 minutes", minutes: 30 },
    { label: "45 minutes", minutes: 45 },
    { label: "60 minutes", minutes: 60 },
  ],
  "personal-growth-coaching": [
    { label: "30 minutes", minutes: 30 },
    { label: "45 minutes", minutes: 45 },
    { label: "60 minutes", minutes: 60 },
  ],
  "therapeutic-healing": [
    { label: "45 minutes", minutes: 45 },
    { label: "60 minutes", minutes: 60 },
    { label: "75 minutes", minutes: 75 },
  ],
};

// Reports don't need scheduling
const REPORT_SERVICES = ["premium-kundli", "numerology-report", "matchmaking"];

declare global {
  interface Window {
    Razorpay: new (options: Record<string, unknown>) => { open: () => void };
  }
}

export function BookingWizard({ service }: BookingWizardProps) {
  const isReport = REPORT_SERVICES.includes(service.slug);

  const [step, setStep] = useState<Step>(isReport ? "details" : "date");
  const [selectedDate, setSelectedDate] = useState("");
  const [selectedSlot, setSelectedSlot] = useState("");
  const [selectedDuration, setSelectedDuration] = useState(0);
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone: "",
    notes: "",
    dateOfBirth: "",
    birthTimeHour: "12",
    birthTimeMinute: "00",
    birthTimePeriod: "AM" as "AM" | "PM",
    birthTimeUnknown: false,
    placeOfBirth: "",
    birthLatitude: 0,
    birthLongitude: 0,
  });
  const [bookingId, setBookingId] = useState("");
  const [price, setPrice] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const durations = DURATION_OPTIONS[service.slug] || [];

  const steps: { key: Step; label: string; icon: React.ReactNode }[] = isReport
    ? [
        { key: "details", label: "Your Details", icon: <User className="h-4 w-4" /> },
        { key: "review", label: "Review", icon: <CheckCircle2 className="h-4 w-4" /> },
        { key: "payment", label: "Payment", icon: <CreditCard className="h-4 w-4" /> },
      ]
    : [
        { key: "date", label: "Date", icon: <Calendar className="h-4 w-4" /> },
        { key: "time", label: "Time", icon: <Clock className="h-4 w-4" /> },
        { key: "duration", label: "Duration", icon: <Clock className="h-4 w-4" /> },
        { key: "details", label: "Details", icon: <User className="h-4 w-4" /> },
        { key: "review", label: "Review", icon: <CheckCircle2 className="h-4 w-4" /> },
        { key: "payment", label: "Payment", icon: <CreditCard className="h-4 w-4" /> },
      ];

  const currentStepIndex = steps.findIndex((s) => s.key === step);

  const handleNext = () => {
    if (currentStepIndex < steps.length - 1) {
      setStep(steps[currentStepIndex + 1].key);
    }
  };

  const handleBack = () => {
    if (currentStepIndex > 0) {
      setStep(steps[currentStepIndex - 1].key);
    }
  };

  const handleCreateBooking = async () => {
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

  if (step === "confirmed") {
    return (
      <div className="mx-auto max-w-lg text-center py-12">
        <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-green-100">
          <CheckCircle2 className="h-8 w-8 text-green-600" />
        </div>
        <h2 className="font-heading text-2xl font-bold text-vedic-dark">Booking Confirmed!</h2>
        <p className="mt-2 text-gray-600">
          Thank you, {formData.name}. Your {service.title} has been booked successfully.
        </p>
        <div className="mt-4 rounded-lg bg-gray-50 p-4 text-sm text-gray-700 space-y-1">
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
        <p className="mt-4 text-sm text-gray-500">
          A confirmation email with meeting details has been sent to {formData.email}.
        </p>
        <p className="mt-1 text-xs text-gray-400">
          Please save your Booking ID for reference.
        </p>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-2xl">
      {/* Progress bar */}
      <div className="mb-8 flex items-center justify-center gap-2">
        {steps.map((s, i) => (
          <div key={s.key} className="flex items-center">
            <div
              className={`flex items-center gap-1 rounded-full px-3 py-1.5 text-xs font-medium ${
                i <= currentStepIndex
                  ? "bg-primary-100 text-primary-700"
                  : "bg-gray-100 text-gray-400"
              }`}
            >
              {s.icon}
              <span className="hidden sm:inline">{s.label}</span>
            </div>
            {i < steps.length - 1 && (
              <div
                className={`mx-1 h-0.5 w-4 sm:w-8 ${
                  i < currentStepIndex ? "bg-primary-400" : "bg-gray-200"
                }`}
              />
            )}
          </div>
        ))}
      </div>

      {error && (
        <div className="mb-4 rounded-lg bg-red-50 border border-red-200 p-3 text-sm text-red-700">
          {error}
        </div>
      )}

      {/* Step content */}
      <div className="min-h-[300px]">
        {step === "date" && (
          <div>
            <h3 className="mb-4 font-heading text-xl font-bold">Select a Date</h3>
            <BookingCalendar
              selectedDate={selectedDate}
              onDateSelect={(date) => {
                setSelectedDate(date);
                setSelectedSlot("");
              }}
            />
          </div>
        )}

        {step === "time" && (
          <div>
            <h3 className="mb-4 font-heading text-xl font-bold">
              Select a Time Slot
            </h3>
            <p className="mb-4 text-sm text-gray-500">Date: {selectedDate}</p>
            <TimeSlotPicker
              date={selectedDate}
              selectedSlot={selectedSlot}
              onSlotSelect={setSelectedSlot}
            />
          </div>
        )}

        {step === "duration" && (
          <div>
            <h3 className="mb-4 font-heading text-xl font-bold">Select Duration</h3>
            <div className="grid gap-3 sm:grid-cols-3">
              {durations.map((d) => (
                <button
                  key={d.minutes}
                  onClick={() => setSelectedDuration(d.minutes)}
                  className={`rounded-xl border-2 p-4 text-center transition-colors ${
                    selectedDuration === d.minutes
                      ? "border-primary-600 bg-primary-50"
                      : "border-gray-200 hover:border-primary-300"
                  }`}
                >
                  <Clock className="mx-auto mb-2 h-6 w-6 text-primary-600" />
                  <p className="font-semibold">{d.label}</p>
                </button>
              ))}
            </div>
          </div>
        )}

        {step === "details" && (
          <div>
            <h3 className="mb-4 font-heading text-xl font-bold">Your Details</h3>
            <div className="space-y-4">
              <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">Full Name *</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                  placeholder="Enter your full name"
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">Email *</label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                  placeholder="you@example.com"
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">Phone *</label>
                <input
                  type="tel"
                  value={formData.phone}
                  onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                  className="w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                  placeholder="+91 98765 43210"
                />
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium text-gray-700">Notes *</label>
                <textarea
                  value={formData.notes}
                  onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
                  rows={3}
                  className="w-full rounded-lg border border-gray-300 px-4 py-2.5 focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
                  placeholder="Please describe what you'd like to discuss or need help with"
                />
              </div>

              <div>
                <label className="mb-2 block text-sm font-medium text-gray-700">Date of Birth *</label>
                <DateOfBirthPicker
                  selectedDate={formData.dateOfBirth}
                  onDateSelect={(date) => setFormData({ ...formData, dateOfBirth: date })}
                />
              </div>

              <div>
                <label className="mb-2 block text-sm font-medium text-gray-700">Time of Birth</label>
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
                <label className="mb-2 block text-sm font-medium text-gray-700">Place of Birth *</label>
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
            <h3 className="mb-4 font-heading text-xl font-bold">Review Your Booking</h3>
            <div className="rounded-xl border border-gray-200 bg-gray-50 p-6 space-y-3">
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Service</span>
                <span className="font-medium">{service.title}</span>
              </div>
              {!isReport && (
                <>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500">Date</span>
                    <span className="font-medium">{selectedDate}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500">Time</span>
                    <span className="font-medium">{selectedSlot}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500">Duration</span>
                    <span className="font-medium">{selectedDuration} minutes</span>
                  </div>
                </>
              )}
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Name</span>
                <span className="font-medium">{formData.name}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Email</span>
                <span className="font-medium">{formData.email}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Phone</span>
                <span className="font-medium">{formData.phone}</span>
              </div>
              {formData.notes && (
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">Notes</span>
                  <span className="font-medium max-w-[60%] text-right">{formData.notes}</span>
                </div>
              )}
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Date of Birth</span>
                <span className="font-medium">{formData.dateOfBirth}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Time of Birth</span>
                <span className="font-medium">
                  {formData.birthTimeUnknown
                    ? "Unknown"
                    : `${formData.birthTimeHour}:${formData.birthTimeMinute} ${formData.birthTimePeriod}`}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-500">Place of Birth</span>
                <span className="font-medium max-w-[60%] text-right">{formData.placeOfBirth}</span>
              </div>
              <hr className="border-gray-200" />
              <div className="flex justify-between text-base font-bold">
                <span>Price</span>
                <span className="text-primary-600">{service.priceINR}</span>
              </div>
            </div>
          </div>
        )}

        {step === "payment" && (
          <div className="text-center py-8">
            <CreditCard className="mx-auto mb-4 h-12 w-12 text-primary-600" />
            <h3 className="mb-2 font-heading text-xl font-bold">Complete Payment</h3>
            <p className="mb-6 text-gray-600">
              Amount: <strong className="text-primary-600">{"\u20B9"}{price}</strong>
            </p>
            <Button
              variant="gold"
              size="lg"
              onClick={handlePayment}
              disabled={loading}
            >
              {loading ? "Processing..." : `Pay \u20B9${price}`}
            </Button>
            <p className="mt-4 text-xs text-gray-400">
              Secured by Razorpay. Supports UPI, Cards, Wallets & Netbanking.
            </p>
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
                (step === "duration" && !selectedDuration) ||
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
