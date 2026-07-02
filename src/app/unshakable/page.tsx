"use client";

import { useState } from "react";
import { Gem, Loader2, AlertCircle, CheckCircle, Mail } from "lucide-react";
import Link from "next/link";
import { Container } from "@/components/ui/Container";
import { PlaceOfBirthAutocomplete } from "@/components/booking/PlaceOfBirthAutocomplete";
import { unshakableApi } from "@/lib/api";

function todayISO(): string {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

export default function UnshakablePage() {
  const [startDate, setStartDate] = useState(todayISO());
  const [days, setDays] = useState(7);
  const [place, setPlace] = useState<{ name: string; lat: number; lon: number } | null>(null);
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [sent, setSent] = useState(false);

  const canSubmit = !!startDate && !!place && !!email && !loading;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!place) return;
    setLoading(true);
    setError("");
    try {
      await unshakableApi.find({
        start_date: startDate,
        days,
        lat: place.lat,
        lon: place.lon,
        place_name: place.name,
        email,
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
            Your search is running!
          </h1>
          <p className="mb-2 text-gray-600 dark:text-gray-400">
            We&apos;re scanning every rising Lagna across{" "}
            <strong className="text-gray-900 dark:text-white">{days} day(s)</strong> from{" "}
            <strong className="text-gray-900 dark:text-white">{startDate}</strong> and will email the
            ranked charts — each with its 0–100 strength score — to{" "}
            <strong className="text-gray-900 dark:text-white">{email}</strong>.
          </p>
          <p className="mb-8 text-sm text-gray-500 dark:text-gray-500">
            This is a deep calculation — it can take a few minutes. Check your inbox (and spam).
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <button
              onClick={() => {
                setSent(false);
                setEmail("");
              }}
              className="rounded-lg bg-primary-600 px-6 py-2.5 text-sm font-medium text-white hover:bg-primary-700"
            >
              Run Another Search
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
        <div className="mb-8 text-center">
          <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-primary-100 dark:bg-primary-900/30">
            <Gem className="h-7 w-7 text-primary-600" />
          </div>
          <h1 className="mb-2 text-3xl font-bold text-gray-900 dark:text-white">
            Unshakable Chart Finder
          </h1>
          <p className="mx-auto max-w-xl text-gray-600 dark:text-gray-400">
            Search a span of days for the birth moments whose chart is classically <em>exceptional</em> —
            strong Shadbala, high Ashtakavarga, powerful yogas, good longevity. We rank every qualifying
            chart and email you the results.
          </p>
        </div>

        <form
          onSubmit={handleSubmit}
          className="grid gap-5 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-white/5 p-6 shadow-sm sm:grid-cols-2"
        >
          <div>
            <label htmlFor="start" className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">
              Start date
            </label>
            <input
              id="start"
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              required
              className="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2.5 text-sm text-gray-900 dark:text-white focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
            />
          </div>

          <div>
            <label htmlFor="days" className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">
              Span
            </label>
            <select
              id="days"
              value={days}
              onChange={(e) => setDays(Number(e.target.value))}
              className="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 px-4 py-2.5 text-sm text-gray-900 dark:text-white focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
            >
              <option value={1}>1 day</option>
              <option value={3}>3 days</option>
              <option value={7}>7 days (a week)</option>
              <option value={30}>30 days (a month)</option>
            </select>
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
          </div>

          <div className="sm:col-span-2">
            <p className="text-xs text-gray-500">
              Every rising moment is ranked by an honest <strong>0–100 strength score</strong>. The metric tops
              out around ~78, so <strong>~72+</strong> marks a genuinely strong chart — those are starred in
              your emailed results.
            </p>
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
                  Email My Unshakable Charts
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </Container>
  );
}
