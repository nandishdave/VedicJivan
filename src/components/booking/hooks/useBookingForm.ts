"use client";

import { useState } from "react";

const USER_DETAILS_KEY = "vedicjivan_user_details";

export interface BookingFormData {
  name: string;
  email: string;
  phone: string;
  /** Notes are booking-specific — never persisted across bookings. */
  notes: string;
  dateOfBirth: string;
  birthTimeHour: string;
  birthTimeMinute: string;
  birthTimePeriod: "AM" | "PM";
  birthTimeUnknown: boolean;
  placeOfBirth: string;
  birthLatitude: number;
  birthLongitude: number;
}

const EMPTY_FORM: BookingFormData = {
  name: "",
  email: "",
  phone: "",
  notes: "",
  dateOfBirth: "",
  birthTimeHour: "12",
  birthTimeMinute: "00",
  birthTimePeriod: "AM",
  birthTimeUnknown: false,
  placeOfBirth: "",
  birthLatitude: 0,
  birthLongitude: 0,
};

/** Load previously saved personal details so a returning user doesn't
 * have to re-type them. Notes are NOT included — they're per-booking. */
function loadSavedUserDetails(): Partial<BookingFormData> | null {
  if (typeof window === "undefined") return null;
  try {
    const stored = localStorage.getItem(USER_DETAILS_KEY);
    if (!stored) return null;
    return JSON.parse(stored) as Partial<BookingFormData>;
  } catch {
    return null;
  }
}

/** Persist personal details so they pre-fill on future bookings. Drops
 * `notes` because notes are booking-specific. */
function saveUserDetails(formData: BookingFormData): void {
  if (typeof window === "undefined") return;
  const { notes: _notes, ...details } = formData;
  void _notes;
  localStorage.setItem(USER_DETAILS_KEY, JSON.stringify(details));
}

/** Returns true when every required field on the details step has a value. */
function isFormComplete(form: BookingFormData): boolean {
  return Boolean(
    form.name &&
      form.email &&
      form.phone &&
      form.notes &&
      form.dateOfBirth &&
      form.placeOfBirth
  );
}

export interface UseBookingForm {
  formData: BookingFormData;
  setFormData: React.Dispatch<React.SetStateAction<BookingFormData>>;
  /** Persist current values to localStorage (call when leaving the details step). */
  persistDetails: () => void;
  /** True iff every required field is filled. */
  isComplete: boolean;
}

/** Owns the personal-details form state for the booking wizard.
 *
 * Initialises from `localStorage` (excluding `notes`) so a returning user
 * sees their previous name/email/phone/DOB/place pre-filled. Exposes a
 * `persistDetails()` callback to be invoked when the user leaves the
 * details step.
 */
export function useBookingForm(): UseBookingForm {
  const [formData, setFormData] = useState<BookingFormData>(() => {
    const saved = loadSavedUserDetails();
    if (!saved) return EMPTY_FORM;
    return {
      ...EMPTY_FORM,
      name: saved.name ?? "",
      email: saved.email ?? "",
      phone: saved.phone ?? "",
      dateOfBirth: saved.dateOfBirth ?? "",
      birthTimeHour: saved.birthTimeHour ?? "12",
      birthTimeMinute: saved.birthTimeMinute ?? "00",
      birthTimePeriod: saved.birthTimePeriod ?? "AM",
      birthTimeUnknown: saved.birthTimeUnknown ?? false,
      placeOfBirth: saved.placeOfBirth ?? "",
      birthLatitude: saved.birthLatitude ?? 0,
      birthLongitude: saved.birthLongitude ?? 0,
    };
  });

  return {
    formData,
    setFormData,
    persistDetails: () => saveUserDetails(formData),
    isComplete: isFormComplete(formData),
  };
}
