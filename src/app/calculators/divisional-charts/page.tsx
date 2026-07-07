"use client";

import { useState } from "react";
import { Sparkles, Loader2, AlertCircle } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { PlaceOfBirthAutocomplete } from "@/components/booking/PlaceOfBirthAutocomplete";
import { kundliApi, type DivisionalResult } from "@/lib/api";

const PLANET_ABBR: Record<string, string> = {
  Ascendant: "Asc", Sun: "Su", Moon: "Mo", Mars: "Ma", Mercury: "Me", Jupiter: "Ju",
  Venus: "Ve", Saturn: "Sa", Rahu: "Ra", Ketu: "Ke", Uranus: "Ur", Neptune: "Ne", Pluto: "Pl",
};

export default function DivisionalChartsCalculatorPage() {
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
  const [result, setResult] = useState<DivisionalResult | null>(null);
  const [showUpagrahas, setShowUpagrahas] = useState(false);

  const canSubmit = !!date && !!time && !!place && !loading;

  const fetchCharts = async (withUpagrahas: boolean) => {
    if (!place) {
      setError("Please choose a birth place.");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const res = await kundliApi.divisionalCharts({
        dob: date,
        tob: time,
        lat: place.lat,
        lon: place.lon,
        upagrahas: withUpagrahas,
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
    fetchCharts(showUpagrahas);
  };

  const onToggleUpagrahas = (checked: boolean) => {
    setShowUpagrahas(checked);
    if (result) fetchCharts(checked); // live-refresh when a result is already shown
  };

  return (
    <div className="bg-vedic-bg py-12 dark:bg-dark-bg lg:py-16">
      <Container>
        <div className="mx-auto max-w-5xl">
          <div className="mb-8 text-center">
            <span className="inline-flex items-center gap-1.5 rounded-full bg-primary-50 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-primary-600 dark:bg-primary-900/20">
              <Sparkles className="h-3.5 w-3.5" /> Free Calculator
            </span>
            <h1 className="mt-4 font-heading text-3xl font-bold text-vedic-dark dark:text-white lg:text-4xl">
              Divisional Charts (D1–D60)
            </h1>
            <p className="mx-auto mt-3 max-w-2xl text-sm text-gray-600 dark:text-gray-400">
              Each divisional chart (varga) splits every sign into finer parts to read a specific
              area of life — <span className="font-semibold">D9 (Navāṁśa)</span> for marriage &amp;
              dharma, <span className="font-semibold">D10 (Daśāṁśa)</span> for career,{" "}
              <span className="font-semibold">D60 (Ṣaṣṭyāṁśa)</span> for past karma. Below is every
              body&rsquo;s sign in each varga.
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
            <label className="flex cursor-pointer items-center gap-2 text-sm font-medium text-gray-700 dark:text-gray-300 sm:col-span-2">
              <input
                type="checkbox"
                checked={showUpagrahas}
                onChange={(e) => onToggleUpagrahas(e.target.checked)}
                className="h-4 w-4 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
              />
              Include the 11 upagrahas (sub-planets) in every varga
            </label>
            <div className="sm:col-span-2">
              <button
                type="submit"
                disabled={!canSubmit}
                aria-busy={loading}
                className="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-primary-600 px-5 py-3 text-sm font-semibold text-white transition-colors hover:bg-primary-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-60 sm:w-auto"
              >
                {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Sparkles className="h-4 w-4" />}
                {loading ? "Calculating…" : "Calculate Divisional Charts"}
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
            <div className="mt-8 overflow-hidden rounded-2xl border border-gray-100 bg-white shadow-sm dark:border-white/10 dark:bg-dark-surface-card">
              <div className="overflow-x-auto">
                <table className="w-full text-center text-sm tabular-nums">
                  <thead>
                    <tr className="bg-primary-600 text-white">
                      <th className="sticky left-0 z-10 bg-primary-600 px-3 py-2.5 text-left font-semibold">
                        Body
                      </th>
                      {result.vargas.map((v) => (
                        <th key={v.key} title={v.name} className="px-2 py-2.5 font-semibold">
                          {v.key}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {result.bodies.map((b) => {
                      const isAsc = b.body === "Ascendant";
                      const isUpa = b.is_upagraha;
                      const rowBg = isAsc
                        ? "bg-primary-50/60 dark:bg-primary-900/20"
                        : isUpa
                          ? "bg-amber-50/60 dark:bg-amber-900/10"
                          : "";
                      return (
                        <tr key={b.body} className={"border-t border-gray-100 dark:border-white/10 " + rowBg}>
                          <td
                            className={
                              "sticky left-0 z-10 px-3 py-1.5 text-left font-semibold text-vedic-dark dark:text-white " +
                              (rowBg || "bg-white dark:bg-dark-surface-card")
                            }
                          >
                            {b.body}
                            {!isUpa && (
                              <span className="ml-1 text-xs font-normal text-gray-400">{PLANET_ABBR[b.body]}</span>
                            )}
                          </td>
                          {b.signs.map((s, i) => (
                            <td
                              key={i}
                              className={
                                "px-2 py-1.5 " +
                                (isUpa ? "text-amber-700 dark:text-amber-300" : "text-gray-600 dark:text-gray-300")
                              }
                            >
                              {s}
                            </td>
                          ))}
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
              <div className="border-t border-gray-100 px-4 py-4 dark:border-white/10">
                <div className="mb-1.5 text-[11px] font-bold uppercase tracking-wide text-gray-400 dark:text-gray-500">
                  Vargas
                </div>
                <div className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-gray-500 dark:text-gray-400">
                  {result.vargas.map((v) => (
                    <span key={v.key}>
                      <b className="text-gray-600 dark:text-gray-300">{v.key}</b> {v.name}
                    </span>
                  ))}
                </div>
                <p className="mt-3 text-xs text-gray-400 dark:text-gray-500">
                  Signs are two-letter abbreviations (Ar Ta Ge Cn Le Vi Li Sc Sg Cp Aq Pi). D1 is the
                  birth (Rāśi) chart. Guidance only — consult an astrologer.
                </p>
              </div>
            </div>
          )}
        </div>
      </Container>
    </div>
  );
}
