"use client";

import { useState } from "react";
import { Sparkles, Loader2, AlertCircle, CheckCircle, Mail } from "lucide-react";
import Link from "next/link";
import { Container } from "@/components/ui/Container";
import { PlaceOfBirthAutocomplete } from "@/components/booking/PlaceOfBirthAutocomplete";
import { muhurtaApi } from "@/lib/api";

const ASPECTS: { key: string; label: string; short: string; group: string }[] = [
  { key: "health", label: "Health & Vitality", short: "Health", group: "Self & Body" },
  { key: "longevity", label: "Longevity", short: "Longevity", group: "Self & Body" },
  { key: "wealth", label: "Wealth & Finances", short: "Wealth", group: "Material" },
  { key: "career", label: "Career & Status", short: "Career", group: "Material" },
  { key: "property", label: "Property & Comforts", short: "Property", group: "Material" },
  { key: "marriage", label: "Marriage & Spouse", short: "Marriage", group: "Relationships" },
  { key: "children", label: "Children & Progeny", short: "Children", group: "Relationships" },
  { key: "family", label: "Family Harmony", short: "Family", group: "Relationships" },
  { key: "education", label: "Education & Intellect", short: "Education", group: "Mind & Growth" },
  { key: "fortune", label: "Fortune & Dharma", short: "Fortune", group: "Mind & Growth" },
  { key: "foreign", label: "Foreign & Travel", short: "Foreign", group: "Beyond" },
  { key: "spiritual", label: "Spirituality", short: "Spiritual", group: "Beyond" },
];

function todayISO(): string {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

export default function MuhurtaPage() {
  const [date, setDate] = useState(todayISO());
  const [time, setTime] = useState("");
  const [place, setPlace] = useState<{ name: string; lat: number; lon: number } | null>(null);
  const [email, setEmail] = useState("");
  const [priorities, setPriorities] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [sent, setSent] = useState(false);

  const canSubmit = !!date && !!place && !!email && !loading;

  const togglePriority = (key: string) =>
    setPriorities((prev) => {
      const next = new Set(prev);
      if (next.has(key)) next.delete(key);
      else next.add(key);
      return next;
    });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!place) return;
    setLoading(true);
    setError("");
    try {
      await muhurtaApi.analyzeBirth({
        date,
        lat: place.lat,
        lon: place.lon,
        place_name: place.name,
        email,
        time: time || null,
        priorities: priorities.size ? Array.from(priorities) : null,
      });
      setSent(true);
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  if (sent) {
    return (
      <Container className="py-20">
        <div className="mx-auto max-w-lg text-center">
          <div className="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-full bg-green-100 dark:bg-green-900/30">
            <CheckCircle className="h-8 w-8 text-green-600" />
          </div>
          <h1 className="mb-3 text-2xl font-bold text-gray-900 dark:text-white">
            Your analysis is on its way!
          </h1>
          <p className="mb-2 text-gray-600 dark:text-gray-400">
            We&apos;re calculating every rising Lagna for <strong className="text-gray-900 dark:text-white">{date}</strong>{" "}
            and will email the full report to{" "}
            <strong className="text-gray-900 dark:text-white">{email}</strong> within a few minutes.
          </p>
          <p className="mb-8 text-sm text-gray-500 dark:text-gray-500">
            Please check your inbox (and spam folder). The detailed analysis takes a little time to compute.
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <button
              onClick={() => {
                setSent(false);
                setEmail("");
              }}
              className="rounded-lg bg-primary-600 px-6 py-2.5 text-sm font-medium text-white hover:bg-primary-700"
            >
              Run Another Date
            </button>
            <Link
              href="/services"
              className="rounded-lg border border-gray-300 dark:border-gray-600 px-6 py-2.5 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-white/5"
            >
              Book a Consultation
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
            <Sparkles className="h-7 w-7 text-primary-600" />
          </div>
          <h1 className="mb-2 text-3xl font-bold text-gray-900 dark:text-white">
            Auspicious Birth-Time Calculator
          </h1>
          <p className="mx-auto max-w-xl text-gray-600 dark:text-gray-400">
            For a chosen day and place, we rank every rising ascendant (Lagna) by strength and show how
            each favours or challenges every area of life. The full analysis is detailed, so we email it to
            you the moment it&apos;s ready.
          </p>
        </div>

        {/* Form */}
        <form
          onSubmit={handleSubmit}
          className="grid gap-5 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-white/5 p-6 shadow-sm sm:grid-cols-2"
        >
          <div>
            <label htmlFor="date" className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">
              Date
            </label>
            <input
              id="date"
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              required
              className="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2.5 text-sm text-gray-900 dark:text-white focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
            />
          </div>

          <div>
            <label htmlFor="time" className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">
              Time <span className="font-normal text-gray-400">(optional)</span>
            </label>
            <input
              id="time"
              type="time"
              value={time}
              onChange={(e) => setTime(e.target.value)}
              className="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2.5 text-sm text-gray-900 dark:text-white focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
            />
            <p className="mt-1 text-xs text-gray-500">
              Already born? Add the birth time to see which Lagna was rising &amp; how it scores. Blank = whole-day view (positions at noon).
            </p>
          </div>

          <div className="sm:col-span-2">
            <label className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">
              Place
            </label>
            <PlaceOfBirthAutocomplete
              value={place?.name ?? ""}
              onPlaceSelect={(p) => setPlace({ name: p.name, lat: p.latitude, lon: p.longitude })}
            />
          </div>

          <div className="sm:col-span-2">
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
            <p className="mt-1 text-xs text-gray-500">We&apos;ll email your full analysis here.</p>
          </div>

          {/* Priorities */}
          <div className="sm:col-span-2">
            <label className="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">
              Prioritise <span className="font-normal text-gray-400">(optional — re-ranks toward what you value)</span>
            </label>
            <div className="flex flex-wrap gap-2">
              {ASPECTS.map((a) => {
                const on = priorities.has(a.key);
                return (
                  <button
                    type="button"
                    key={a.key}
                    onClick={() => togglePriority(a.key)}
                    className={`rounded-full border px-3 py-1.5 text-xs font-medium transition-colors ${
                      on
                        ? "border-primary-600 bg-primary-600 text-white"
                        : "border-gray-300 dark:border-gray-600 text-gray-600 dark:text-gray-300 hover:border-primary-400"
                    }`}
                  >
                    {a.short}
                  </button>
                );
              })}
            </div>
          </div>

          {error && (
            <div className="sm:col-span-2 flex items-start gap-2 rounded-lg bg-red-50 dark:bg-red-900/20 p-3 text-sm text-red-700 dark:text-red-400">
              <AlertCircle className="mt-0.5 h-4 w-4 flex-shrink-0" />
              <span>{error}</span>
            </div>
          )}

          <div className="sm:col-span-2">
            <button
              type="submit"
              disabled={!canSubmit}
              className="flex w-full items-center justify-center gap-2 rounded-lg bg-primary-600 px-6 py-3 text-sm font-medium text-white hover:bg-primary-700 disabled:cursor-not-allowed disabled:opacity-50 transition-colors"
            >
              {loading ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Submitting…
                </>
              ) : (
                <>
                  <Mail className="h-4 w-4" />
                  Email My Auspicious Windows
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </Container>
  );
}
