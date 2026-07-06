"use client";

import { useState } from "react";
import { Sparkles, Loader2, AlertCircle } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { PlaceOfBirthAutocomplete } from "@/components/booking/PlaceOfBirthAutocomplete";
import { kundliApi, type AshtakavargaResult } from "@/lib/api";

const ORD = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th"];
const PLANET_ABBR: Record<string, string> = {
  Sun: "Su", Moon: "Mo", Mars: "Ma", Mercury: "Me", Jupiter: "Ju", Venus: "Ve", Saturn: "Sa",
};

// SAV bar: baseline is 28 (337 ÷ 12). Above = strong, below = weak.
function savTone(v: number): string {
  if (v >= 30) return "bg-green-500";
  if (v >= 26) return "bg-amber-400";
  return "bg-red-500";
}
function savText(v: number): string {
  if (v >= 30) return "text-green-700 dark:text-green-400";
  if (v >= 26) return "text-amber-600 dark:text-amber-400";
  return "text-red-700 dark:text-red-400";
}

// BAV cell heat (0–8 bindus): high = supportive, low = weak.
function bavCell(v: number): string {
  if (v >= 6) return "bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300";
  if (v >= 4) return "text-gray-600 dark:text-gray-300";
  if (v >= 2) return "bg-amber-50 text-amber-700 dark:bg-amber-900/20 dark:text-amber-300";
  return "bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300";
}

export default function AshtakavargaCalculatorPage() {
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
  const [result, setResult] = useState<AshtakavargaResult | null>(null);

  const canSubmit = !!date && !!time && !!place && !loading;

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!place) {
      setError("Please choose a birth place.");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const res = await kundliApi.ashtakavarga({ dob: date, tob: time, lat: place.lat, lon: place.lon });
      setResult(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not calculate. Check the inputs.");
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const maxSav = result ? Math.max(...result.houses.map((h) => h.sav), 40) : 40;

  return (
    <div className="bg-vedic-bg py-12 dark:bg-dark-bg lg:py-16">
      <Container>
        <div className="mx-auto max-w-4xl">
          <div className="mb-8 text-center">
            <span className="inline-flex items-center gap-1.5 rounded-full bg-primary-50 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-primary-600 dark:bg-primary-900/20">
              <Sparkles className="h-3.5 w-3.5" /> Free Calculator
            </span>
            <h1 className="mt-4 font-heading text-3xl font-bold text-vedic-dark dark:text-white lg:text-4xl">
              Ashtakavarga Calculator
            </h1>
            <p className="mx-auto mt-3 max-w-2xl text-sm text-gray-600 dark:text-gray-400">
              Ashtakavarga scores every house by benefic points (bindus). The{" "}
              <span className="font-semibold text-green-700 dark:text-green-400">Sarvashtakavarga</span>{" "}
              is the total per house (baseline 28 — above is strong, below is weak); each planet&rsquo;s{" "}
              <span className="font-semibold">Bhinnashtakavarga</span> gives its own 0–8 points per house.
              The whole chart always sums to 337.
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
                {loading ? "Calculating…" : "Calculate Ashtakavarga"}
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

          {result && (
            <>
              {/* Sarvashtakavarga */}
              <div className="mt-8 overflow-hidden rounded-2xl border border-gray-100 bg-white shadow-sm dark:border-white/10 dark:bg-dark-surface-card">
                <div className="flex items-center justify-between border-b border-gray-100 px-4 py-3 dark:border-white/10">
                  <h2 className="font-heading text-sm font-bold uppercase tracking-wide text-gray-500 dark:text-gray-400">
                    Sarvashtakavarga <span className="font-normal normal-case">(per house)</span>
                  </h2>
                  <span className="text-xs text-gray-400 dark:text-gray-500">
                    Total {result.grand_total} · baseline 28
                  </span>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="text-gray-500 dark:text-gray-400">
                        <th className="px-4 py-2 text-left font-medium">House</th>
                        <th className="px-4 py-2 text-left font-medium">Sign</th>
                        <th className="px-4 py-2 text-left font-medium">Bindus</th>
                      </tr>
                    </thead>
                    <tbody className="tabular-nums">
                      {result.houses.map((h) => (
                        <tr key={h.house} className="border-t border-gray-100 dark:border-white/10">
                          <td className="px-4 py-1.5 font-medium text-vedic-dark dark:text-white">
                            {ORD[h.house - 1]}
                          </td>
                          <td className="px-4 py-1.5 text-gray-600 dark:text-gray-400">{h.sign}</td>
                          <td className="px-4 py-1.5">
                            <div className="flex items-center gap-2">
                              <div className="h-2.5 w-32 overflow-hidden rounded-full bg-gray-100 dark:bg-white/10">
                                <div
                                  className={`h-full rounded-full ${savTone(h.sav)}`}
                                  style={{ width: `${(h.sav / maxSav) * 100}%` }}
                                />
                              </div>
                              <span className={`w-6 text-right font-bold ${savText(h.sav)}`}>{h.sav}</span>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Bhinnashtakavarga grid */}
              <div className="mt-6 overflow-hidden rounded-2xl border border-gray-100 bg-white shadow-sm dark:border-white/10 dark:bg-dark-surface-card">
                <div className="border-b border-gray-100 px-4 py-3 dark:border-white/10">
                  <h2 className="font-heading text-sm font-bold uppercase tracking-wide text-gray-500 dark:text-gray-400">
                    Bhinnashtakavarga <span className="font-normal normal-case">(each planet&rsquo;s points per house)</span>
                  </h2>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full text-center text-sm tabular-nums">
                    <thead>
                      <tr className="bg-primary-600 text-white">
                        <th className="px-3 py-2 text-left font-semibold">Planet</th>
                        {ORD.map((_, i) => (
                          <th key={i} className="px-2 py-2 font-semibold">{i + 1}</th>
                        ))}
                        <th className="px-3 py-2 font-semibold">Total</th>
                      </tr>
                    </thead>
                    <tbody>
                      {result.bav.map((b) => (
                        <tr key={b.planet} className="border-t border-gray-100 dark:border-white/10">
                          <td className="px-3 py-1.5 text-left font-semibold text-vedic-dark dark:text-white">
                            {b.planet}
                            <span className="ml-1 text-xs text-gray-400">{PLANET_ABBR[b.planet]}</span>
                          </td>
                          {b.per_house.map((v, i) => (
                            <td key={i} className="px-1 py-0.5">
                              <span className={`inline-block w-6 rounded py-0.5 text-xs font-semibold ${bavCell(v)}`}>
                                {v}
                              </span>
                            </td>
                          ))}
                          <td className="px-3 py-1.5 font-bold text-gray-700 dark:text-gray-300">{b.total}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                <p className="border-t border-gray-100 px-4 py-4 text-xs leading-relaxed text-gray-500 dark:border-white/10 dark:text-gray-400">
                  Each column is a house from the Ascendant. A planet&rsquo;s transit through a house
                  tends to give better results where that house holds{" "}
                  <span className="font-semibold text-green-700 dark:text-green-400">more of its own bindus</span>{" "}
                  (and the Sarva score is high). Guidance only — consult an astrologer.
                </p>
              </div>
            </>
          )}
        </div>
      </Container>
    </div>
  );
}
