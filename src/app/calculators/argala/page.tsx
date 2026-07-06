"use client";

import { Fragment, useState } from "react";
import { Sparkles, Loader2, AlertCircle, ChevronDown } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { PlaceOfBirthAutocomplete } from "@/components/booking/PlaceOfBirthAutocomplete";
import { kundliApi, type ArgalaResult, type ArgalaIntervener } from "@/lib/api";

const ORDINAL = [
  "1st", "2nd", "3rd", "4th", "5th", "6th",
  "7th", "8th", "9th", "10th", "11th", "12th",
];
const HOUSE_MEANING = [
  "Self & body", "Wealth & family", "Courage & siblings", "Home & mother",
  "Children & mind", "Health & debts", "Partner", "Longevity & change",
  "Fortune & dharma", "Career & status", "Gains & network", "Loss & moksha",
];
const ord = (n: number) => ORDINAL[n - 1] ?? `${n}th`;
const signed = (n: number) => (n > 0 ? `+${n}` : `${n}`);

function StrengthBar({ v }: { v: number }) {
  const neutral = v === 0;
  const pos = v > 0;
  const width = Math.min(100, Math.abs(v));
  return (
    <div className="flex items-center gap-2">
      <div className="h-2.5 w-20 overflow-hidden rounded-full bg-gray-100 dark:bg-white/10">
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
        {signed(v)}%
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

function Breakdown({ rows }: { rows: ArgalaIntervener[] }) {
  if (!rows.length) {
    return (
      <p className="px-6 py-3 text-xs italic text-gray-400 dark:text-gray-500">
        No effective argala on this house (none, or all obstructed by their virodha).
      </p>
    );
  }
  return (
    <div className="overflow-x-auto px-2 py-2">
      <table className="w-full text-xs">
        <thead>
          <tr className="text-gray-500 dark:text-gray-400">
            <th className="px-2 py-1 text-left font-medium">Planet</th>
            <th className="px-2 py-1 text-left font-medium">From</th>
            <th className="px-2 py-1 text-left font-medium">Sign</th>
            <th className="px-2 py-1 text-left font-medium">Dignity</th>
            <th className="px-2 py-1 text-right font-medium">Dignity</th>
            <th className="px-2 py-1 text-right font-medium">Role-fit</th>
            <th className="px-2 py-1 text-right font-medium">Shadbala</th>
            <th className="px-2 py-1 text-right font-medium">Contribution</th>
          </tr>
        </thead>
        <tbody className="tabular-nums">
          {rows.map((r, i) => (
            <tr key={`${r.planet}-${i}`} className="border-t border-gray-100 dark:border-white/5">
              <td className="px-2 py-1 font-semibold text-vedic-dark dark:text-white">{r.planet}</td>
              <td className="px-2 py-1 text-gray-500 dark:text-gray-400">{ord(r.from_house)}</td>
              <td className="px-2 py-1 text-gray-500 dark:text-gray-400">{r.sign}</td>
              <td className="px-2 py-1 text-gray-500 dark:text-gray-400">{r.dignity}</td>
              <td className={`px-2 py-1 text-right ${r.dignity_score >= 0 ? "text-green-700 dark:text-green-400" : "text-red-700 dark:text-red-400"}`}>
                {signed(r.dignity_score)}
              </td>
              <td className={`px-2 py-1 text-right ${r.role_fit >= 0 ? "text-green-700 dark:text-green-400" : "text-red-700 dark:text-red-400"}`}>
                {signed(r.role_fit)}
              </td>
              <td className="px-2 py-1 text-right text-gray-500 dark:text-gray-400">{r.shadbala.toFixed(1)}</td>
              <td className={`px-2 py-1 text-right font-semibold ${r.contribution >= 0 ? "text-green-700 dark:text-green-400" : "text-red-700 dark:text-red-400"}`}>
                {signed(Math.round(r.contribution))}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
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
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<ArgalaResult | null>(null);
  const [expanded, setExpanded] = useState<Set<number>>(new Set());

  const canSubmit = !!date && !!time && !!place && !loading;

  const toggleRow = (house: number) => {
    setExpanded((prev) => {
      const next = new Set(prev);
      if (next.has(house)) next.delete(house);
      else next.add(house);
      return next;
    });
  };

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!place) {
      setError("Please choose a birth place.");
      return;
    }
    setLoading(true);
    setError("");
    setExpanded(new Set());
    try {
      const res = await kundliApi.argalaAnalysis({ dob: date, tob: time, lat: place.lat, lon: place.lon });
      setResult(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not calculate. Check the inputs.");
      setResult(null);
    } finally {
      setLoading(false);
    }
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
              Argala (अर्गला, &ldquo;the bolt&rdquo;) is the Jaimini intervention on a house by planets
              in its 2nd, 4th, 5th and 11th — countered by their Virodha (12th, 10th, 9th, 3rd). Each
              house is scored on whether the intervention actually <em>helps</em> it:{" "}
              <span className="font-semibold text-green-700 dark:text-green-400">green helps</span>,{" "}
              <span className="font-semibold text-red-700 dark:text-red-400">red harms</span>. Tap a
              row to see why.
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
                      <th className="px-4 py-3 text-left font-semibold">Argala Strength</th>
                      <th className="px-4 py-3 text-left font-semibold text-green-100">Helps (+)</th>
                      <th className="px-4 py-3 text-left font-semibold text-red-100">Harms (−)</th>
                      <th className="px-2 py-3" aria-label="Expand" />
                    </tr>
                  </thead>
                  <tbody>
                    {result.houses.map((h) => {
                      const open = expanded.has(h.house);
                      return (
                        <Fragment key={h.house}>
                          <tr
                            onClick={() => toggleRow(h.house)}
                            className="cursor-pointer border-t border-gray-100 hover:bg-gray-50 dark:border-white/10 dark:hover:bg-white/5"
                          >
                            <td className="px-4 py-2.5">
                              <div className="font-semibold text-vedic-dark dark:text-white">
                                {ord(h.house)}
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
                            <td className="px-2 py-2.5 text-right">
                              <button
                                type="button"
                                aria-expanded={open}
                                aria-label={`${open ? "Hide" : "Show"} breakdown for the ${ord(h.house)} house`}
                                onClick={(e) => {
                                  e.stopPropagation();
                                  toggleRow(h.house);
                                }}
                                className="rounded p-1 text-gray-400 hover:text-primary-600 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500"
                              >
                                <ChevronDown
                                  className={`h-4 w-4 transition-transform ${open ? "rotate-180" : ""}`}
                                />
                              </button>
                            </td>
                          </tr>
                          {open && (
                            <tr className="bg-gray-50/60 dark:bg-white/5">
                              <td colSpan={5} className="p-0">
                                <Breakdown rows={h.interveners} />
                              </td>
                            </tr>
                          )}
                        </Fragment>
                      );
                    })}
                  </tbody>
                </table>
              </div>
              <p className="border-t border-gray-100 px-4 py-4 text-xs leading-relaxed text-gray-500 dark:border-white/10 dark:text-gray-400">
                Each intervener scores <span className="font-semibold">Dignity</span> toward the house
                it locks (Exalted +2 · Own +1.5 · Friend +1 · Enemy −1, or +0.5 if it is a functional
                benefic · Debilitated −2) plus <span className="font-semibold">Role-fit</span> (a
                benefic on a kendra/trikona/2nd/11th, or a malefic on an upachaya 3/6/10/11, adds +1;
                a malefic on the 8th/12th subtracts 1), weighted by its{" "}
                <span className="font-semibold">Shadbala</span>. So a strong exalted malefic — like
                Saturn on a career house — reads green, not red. Only argalas that outweigh their
                Virodha counter count. Guidance only — consult an astrologer.
              </p>
            </div>
          )}
        </div>
      </Container>
    </div>
  );
}
