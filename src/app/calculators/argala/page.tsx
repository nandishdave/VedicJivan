"use client";

import { useState } from "react";
import { Sparkles, Loader2, AlertCircle } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { PlaceOfBirthAutocomplete } from "@/components/booking/PlaceOfBirthAutocomplete";
import { kundliApi, type ArgalaResult } from "@/lib/api";

const ORDINAL = [
  "1st", "2nd", "3rd", "4th", "5th", "6th",
  "7th", "8th", "9th", "10th", "11th", "12th",
];
const HOUSE_MEANING = [
  "Self & body", "Wealth & family", "Courage & siblings", "Home & mother",
  "Children & mind", "Health & debts", "Partner", "Longevity & change",
  "Fortune & dharma", "Career & status", "Gains & network", "Loss & moksha",
];

function StrengthBar({ v }: { v: number }) {
  const neutral = v === 0;
  const pos = v > 0;
  const width = Math.min(100, Math.abs(v));
  return (
    <div className="flex items-center justify-center gap-2">
      <div className="h-2.5 w-24 overflow-hidden rounded-full bg-gray-100 dark:bg-white/10">
        <div
          className={`h-full rounded-full ${pos ? "bg-green-500" : "bg-red-500"}`}
          style={{ width: `${width}%` }}
        />
      </div>
      <span
        className={`w-12 text-right text-xs font-bold tabular-nums ${
          neutral
            ? "text-gray-400 dark:text-gray-500"
            : pos
            ? "text-green-700 dark:text-green-400"
            : "text-red-700 dark:text-red-400"
        }`}
      >
        {v > 0 ? "+" : ""}
        {v}%
      </span>
    </div>
  );
}

function PlanetChips({ names, tone }: { names: string[]; tone: "pos" | "neg" }) {
  if (!names.length) return <span className="text-gray-300 dark:text-gray-600">–</span>;
  const cls =
    tone === "pos"
      ? "bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300"
      : "bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300";
  return (
    <div className="flex flex-wrap gap-1">
      {names.map((n) => (
        <span key={n} className={`rounded-md px-1.5 py-0.5 text-xs font-semibold ${cls}`}>
          {n}
        </span>
      ))}
    </div>
  );
}

export default function ArgalaCalculatorPage() {
  const [date, setDate] = useState("1988-11-11");
  const [time, setTime] = useState("12:55");
  const [place, setPlace] = useState<{ name: string; lat: number; lon: number } | null>({
    name: "Jetpur, Gujarat, India",
    lat: 21.7333,
    lon: 70.6167,
  });
  const [placeInput, setPlaceInput] = useState("Jetpur, Gujarat, India");
  const [mode, setMode] = useState<"natural" | "functional">("natural");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<ArgalaResult | null>(null);

  const canSubmit = !!date && !!time && !!place && !loading;

  const run = async (m: "natural" | "functional") => {
    if (!place) {
      setError("Please choose a birth place.");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const res = await kundliApi.argalaAnalysis({
        dob: date,
        tob: time,
        lat: place.lat,
        lon: place.lon,
        functional: m === "functional",
      });
      setResult(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not calculate. Check the inputs.");
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    run(mode);
  };

  // Toggling re-runs immediately when a result is already on screen.
  const onMode = (m: "natural" | "functional") => {
    setMode(m);
    if (result && !loading) run(m);
  };

  return (
    <div className="bg-vedic-bg py-12 dark:bg-dark-bg lg:py-16">
      <Container>
        <div className="mx-auto max-w-4xl">
          <div className="mb-8 text-center">
            <span className="inline-flex items-center gap-1.5 rounded-full bg-primary-50 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-primary-600 dark:bg-primary-900/20">
              <Sparkles className="h-3.5 w-3.5" /> Free Calculator
            </span>
            <h1 className="mt-4 font-heading text-3xl font-bold text-vedic-dark dark:text-white lg:text-4xl">
              Argala Calculator
            </h1>
            <p className="mx-auto mt-3 max-w-2xl text-sm text-gray-600 dark:text-gray-400">
              Argala (अर्गला, &ldquo;the bolt&rdquo;) is the Jaimini intervention on a house by
              planets in its 2nd, 4th, 5th and 11th — countered by their Virodha (12th, 10th,
              9th, 3rd). For each house you get the Shadbala-weighted{" "}
              <span className="font-semibold text-green-700 dark:text-green-400">benefic (śubha)</span>{" "}
              vs{" "}
              <span className="font-semibold text-red-700 dark:text-red-400">malefic (pāpa)</span>{" "}
              tilt — counting only argalas that outweigh their counter.
            </p>
          </div>

          {/* Form */}
          <form
            onSubmit={onSubmit}
            className="grid gap-4 rounded-2xl border border-gray-100 bg-white p-6 shadow-sm dark:border-white/10 dark:bg-dark-surface-card sm:grid-cols-2"
          >
            <label className="flex flex-col gap-1.5 text-sm font-medium text-gray-700 dark:text-gray-300">
              Date of Birth
              <input
                type="date"
                value={date}
                onChange={(e) => setDate(e.target.value)}
                required
                className="rounded-lg border border-gray-200 px-3 py-2.5 text-sm text-vedic-dark focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500 dark:border-white/10 dark:bg-dark-surface dark:text-white"
              />
            </label>
            <label className="flex flex-col gap-1.5 text-sm font-medium text-gray-700 dark:text-gray-300">
              Time of Birth
              <input
                type="time"
                value={time}
                onChange={(e) => setTime(e.target.value)}
                required
                className="rounded-lg border border-gray-200 px-3 py-2.5 text-sm text-vedic-dark focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500 dark:border-white/10 dark:bg-dark-surface dark:text-white"
              />
            </label>
            <div className="sm:col-span-2">
              <label className="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-300">
                Place of Birth
              </label>
              <PlaceOfBirthAutocomplete
                value={placeInput}
                onPlaceSelect={(p) => {
                  setPlace({ name: p.name, lat: p.latitude, lon: p.longitude });
                  setPlaceInput(p.name);
                }}
              />
            </div>
            {/* Benefic/malefic scheme toggle */}
            <div className="sm:col-span-2">
              <span className="mb-1.5 block text-sm font-medium text-gray-700 dark:text-gray-300">
                Benefic / malefic scheme
              </span>
              <div
                role="group"
                aria-label="Benefic and malefic classification scheme"
                className="inline-flex rounded-lg border border-gray-200 p-0.5 dark:border-white/10"
              >
                {(["natural", "functional"] as const).map((m) => (
                  <button
                    key={m}
                    type="button"
                    onClick={() => onMode(m)}
                    aria-pressed={mode === m}
                    className={`rounded-md px-3.5 py-1.5 text-sm font-semibold capitalize transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 ${
                      mode === m
                        ? "bg-primary-600 text-white"
                        : "text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-white/10"
                    }`}
                  >
                    {m}
                  </button>
                ))}
              </div>
              <p className="mt-1.5 text-xs text-gray-400 dark:text-gray-500">
                {mode === "natural"
                  ? "Natural: Jupiter, Venus, Mercury (+ bright-fortnight Moon) are benefic."
                  : "Functional: benefic/malefic by your ascendant group (lagna-specific)."}
              </p>
            </div>

            <div className="sm:col-span-2">
              <button
                type="submit"
                disabled={!canSubmit}
                aria-busy={loading}
                className="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-primary-600 px-5 py-3 text-sm font-semibold text-white transition-colors hover:bg-primary-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-60 sm:w-auto"
              >
                {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Sparkles className="h-4 w-4" />}
                {loading ? "Calculating…" : "Calculate Argala"}
              </button>
            </div>
          </form>

          {error && (
            <div
              role="alert"
              className="mt-4 flex items-start gap-2 rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700 dark:border-red-900/40 dark:bg-red-900/20 dark:text-red-300"
            >
              <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" />
              {error}
            </div>
          )}

          {/* Result */}
          {result && (
            <div className="mt-8 overflow-hidden rounded-2xl border border-gray-100 bg-white shadow-sm dark:border-white/10 dark:bg-dark-surface-card">
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="bg-primary-600 text-white">
                      <th className="px-4 py-3 text-left font-semibold">House</th>
                      <th className="px-4 py-3 font-semibold">Argala Strength</th>
                      <th className="px-4 py-3 text-left font-semibold text-green-100">Planets (+)</th>
                      <th className="px-4 py-3 text-left font-semibold text-red-100">Planets (−)</th>
                    </tr>
                  </thead>
                  <tbody>
                    {result.houses.map((h) => (
                      <tr key={h.house} className="border-t border-gray-100 dark:border-white/10">
                        <td className="px-4 py-2.5">
                          <div className="font-semibold text-vedic-dark dark:text-white">
                            {ORDINAL[h.house - 1]}
                          </div>
                          <div className="text-xs text-gray-400 dark:text-gray-500">
                            {HOUSE_MEANING[h.house - 1]}
                          </div>
                        </td>
                        <td className="px-4 py-2.5">
                          <StrengthBar v={h.strength} />
                        </td>
                        <td className="px-4 py-2.5">
                          <PlanetChips names={h.positive} tone="pos" />
                        </td>
                        <td className="px-4 py-2.5">
                          <PlanetChips names={h.negative} tone="neg" />
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <p className="border-t border-gray-100 px-4 py-4 text-xs leading-relaxed text-gray-500 dark:border-white/10 dark:text-gray-400">
                Strength % = (benefic − malefic) ÷ (benefic + malefic) of the Shadbala-weighted
                interveners, so <span className="font-semibold text-green-700 dark:text-green-400">+100%</span> means
                every effective argala is a strong benefic and{" "}
                <span className="font-semibold text-red-700 dark:text-red-400">−100%</span> every one a strong
                malefic. Only argalas that outweigh their Virodha (counter) house are counted.{" "}
                {result.functional
                  ? "Benefic/malefic here follows the lagna-specific functional scheme."
                  : `Natural benefics — the Moon counts as benefic only in the bright (Shukla) fortnight${
                      result.moon_bright ? " — bright here" : " — waning here"
                    }.`}{" "}
                Guidance only — consult an astrologer.
              </p>
            </div>
          )}
        </div>
      </Container>
    </div>
  );
}
