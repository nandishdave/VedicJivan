"use client";

import { useState } from "react";
import { CheckCircle, Loader2, Star, AlertCircle } from "lucide-react";
import Link from "next/link";
import { Container } from "@/components/ui/Container";
import { DateOfBirthPicker } from "@/components/booking/DateOfBirthPicker";
import { TimeOfBirthPicker } from "@/components/booking/TimeOfBirthPicker";
import { PlaceOfBirthAutocomplete } from "@/components/booking/PlaceOfBirthAutocomplete";
import { kundliApi } from "@/lib/api";

export default function KundliPage() {
  const [name, setName] = useState("");
  const [gender, setGender] = useState("");
  const [email, setEmail] = useState("");
  const [dob, setDob] = useState("");
  const [tob, setTob] = useState<{ hour: string; minute: string; period: "AM" | "PM" } | null>(null);
  const [tobUnknown, setTobUnknown] = useState(false);
  const [placeName, setPlaceName] = useState("");
  const [lat, setLat] = useState<number | null>(null);
  const [lon, setLon] = useState<number | null>(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const canSubmit = name && gender && email && dob && (tob || tobUnknown) && lat !== null && lon !== null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!canSubmit) return;
    setLoading(true);
    setError("");

    // Convert 12h → 24h time
    let timeStr = "12:00";
    if (tob && !tobUnknown) {
      let h = parseInt(tob.hour, 10);
      const m = tob.minute;
      if (tob.period === "AM" && h === 12) h = 0;
      else if (tob.period === "PM" && h !== 12) h += 12;
      timeStr = `${h.toString().padStart(2, "0")}:${m}`;
    }

    try {
      await kundliApi.generate({
        name,
        gender,
        email,
        dob,
        tob: timeStr,
        lat: lat!,
        lon: lon!,
        place_name: placeName,
      });
      setSuccess(true);
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <Container className="py-20">
        <div className="mx-auto max-w-lg text-center">
          <div className="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-full bg-green-100 dark:bg-green-900/30">
            <CheckCircle className="h-8 w-8 text-green-600" />
          </div>
          <h1 className="mb-3 text-2xl font-bold text-gray-900 dark:text-white">
            Your Kundli is on its way!
          </h1>
          <p className="mb-2 text-gray-600 dark:text-gray-400">
            We&apos;ve sent your personalised Kundli report to <strong className="text-gray-900 dark:text-white">{email}</strong>.
          </p>
          <p className="mb-8 text-sm text-gray-500 dark:text-gray-500">
            Please check your inbox (and spam folder). The report may take a minute to arrive.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <Link
              href="/services"
              className="rounded-lg bg-primary-600 px-6 py-2.5 text-sm font-medium text-white hover:bg-primary-700"
            >
              Book a Consultation
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
        {/* Header */}
        <div className="mb-8 text-center">
          <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-primary-100 dark:bg-primary-900/30">
            <Star className="h-7 w-7 text-primary-600" />
          </div>
          <h1 className="mb-2 text-3xl font-bold text-gray-900 dark:text-white">
            Free Kundli Report
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Enter your birth details to receive a comprehensive Vedic birth chart report via email.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-white/5 p-6 shadow-sm">
          {/* Name */}
          <div>
            <label htmlFor="name" className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">
              Full Name
            </label>
            <input
              id="name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Enter your full name"
              required
              className="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2.5 text-sm text-gray-900 dark:text-white placeholder-gray-400 focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
            />
          </div>

          {/* Gender */}
          <div>
            <label htmlFor="gender" className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">
              Gender
            </label>
            <select
              id="gender"
              value={gender}
              onChange={(e) => setGender(e.target.value)}
              required
              className="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2.5 text-sm text-gray-900 dark:text-white focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
            >
              <option value="">Select gender</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
            </select>
          </div>

          {/* Date of Birth */}
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">
              Date of Birth
            </label>
            <DateOfBirthPicker selectedDate={dob} onDateSelect={setDob} />
          </div>

          {/* Time of Birth */}
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">
              Time of Birth
            </label>
            <TimeOfBirthPicker
              value={tob}
              isUnknown={tobUnknown}
              onTimeChange={setTob}
              onUnknownChange={setTobUnknown}
            />
          </div>

          {/* Place of Birth */}
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">
              Place of Birth
            </label>
            <PlaceOfBirthAutocomplete
              value={placeName}
              onPlaceSelect={(place) => {
                setPlaceName(place.name);
                setLat(place.latitude);
                setLon(place.longitude);
              }}
            />
          </div>

          {/* Email */}
          <div>
            <label htmlFor="email" className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">
              Email Address
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="your@email.com"
              required
              className="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2.5 text-sm text-gray-900 dark:text-white placeholder-gray-400 focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
            />
            <p className="mt-1 text-xs text-gray-500">Your Kundli report will be sent to this email address.</p>
          </div>

          {/* Error */}
          {error && (
            <div className="flex items-start gap-2 rounded-lg bg-red-50 dark:bg-red-900/20 p-3 text-sm text-red-700 dark:text-red-400">
              <AlertCircle className="mt-0.5 h-4 w-4 flex-shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {/* Submit */}
          <button
            type="submit"
            disabled={!canSubmit || loading}
            className="w-full rounded-lg bg-primary-600 px-6 py-3 text-sm font-medium text-white hover:bg-primary-700 disabled:cursor-not-allowed disabled:opacity-50 transition-colors"
          >
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <Loader2 className="h-4 w-4 animate-spin" />
                Calculating your birth chart...
              </span>
            ) : (
              "Generate My Free Kundli"
            )}
          </button>

          <p className="text-center text-xs text-gray-400">
            Your report includes planetary positions, Nakshatra analysis, Dasha periods, Manglik Dosha, Sade Sati, and more.
          </p>
        </form>
      </div>
    </Container>
  );
}
