"use client";

import { useState } from "react";
import { Sparkles, Loader2, AlertCircle } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { PlaceOfBirthAutocomplete } from "@/components/booking/PlaceOfBirthAutocomplete";
import { kundliApi, type DegreeAnalysisResult } from "@/lib/api";

function GoodCell({ v }: { v: boolean }) {
  return v ? (
    <span className="inline-block rounded-md bg-green-100 px-2 py-0.5 text-xs font-bold text-green-800 dark:bg-green-900/40 dark:text-green-300">
      Yes
    </span>
  ) : (
    <span className="text-gray-300 dark:text-gray-600">–</span>
  );
}

function BadCell({ v }: { v: boolean | null }) {
  if (v === null || v === undefined)
    return <span className="text-xs italic text-gray-400 dark:text-gray-500">n/a</span>;
  return v ? (
    <span className="inline-block rounded-md bg-red-100 px-2 py-0.5 text-xs font-bold text-red-800 dark:bg-red-900/40 dark:text-red-300">
      Yes
    </span>
  ) : (
    <span className="text-gray-300 dark:text-gray-600">–</span>
  );
}

export default function DegreeAnalysisCalculatorPage() {
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
  const [result, setResult] = useState<DegreeAnalysisResult | null>(null);

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
      const res = await kundliApi.degreeAnalysis({ dob: date, tob: time, lat: place.lat, lon: place.lon });
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
              Auspicious &amp; Poison Degrees
            </h1>
            <p className="mx-auto mt-3 max-w-2xl text-sm text-gray-600 dark:text-gray-400">
              For a birth moment, each of the nine grahas + the three outer planets + the Ascendant is checked against
              four classical degree categories — <span className="font-semibold text-green-700 dark:text-green-400">Pushkara
              Navāṁśa</span> &amp; <span className="font-semibold text-green-700 dark:text-green-400">Pushkara Bhāga</span>{" "}
              (auspicious) and <span className="font-semibold text-red-700 dark:text-red-400">Vish Navāṁśa</span> &amp;{" "}
              <span className="font-semibold text-red-700 dark:text-red-400">Mṛtyu Bhāga</span> (poison).
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
                {loading ? "Calculating…" : "Calculate Degrees"}
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
                      <th className="px-4 py-3 text-left font-semibold">Body</th>
                      <th className="px-4 py-3 font-semibold">Sign</th>
                      <th className="px-4 py-3 font-semibold">Degree</th>
                      <th className="px-4 py-3 font-semibold">Navāṁśa</th>
                      <th className="px-4 py-3 font-semibold text-green-100">Pushkara Navāṁśa</th>
                      <th className="px-4 py-3 font-semibold text-green-100">Pushkara Bhāga</th>
                      <th className="px-4 py-3 font-semibold text-red-100">Vish Navāṁśa</th>
                      <th className="px-4 py-3 font-semibold text-red-100">Mṛtyu Bhāga</th>
                    </tr>
                  </thead>
                  <tbody>
                    {result.bodies.map((b) => (
                      <tr
                        key={b.body}
                        className={
                          "border-t border-gray-100 text-center dark:border-white/10 " +
                          (b.body === "Ascendant" ? "bg-primary-50 dark:bg-primary-900/20" : "")
                        }
                      >
                        <td className="px-4 py-2.5 text-left font-medium text-vedic-dark dark:text-white">{b.body}</td>
                        <td className="px-4 py-2.5 text-gray-600 dark:text-gray-400">{b.sign}</td>
                        <td className="px-4 py-2.5 text-gray-600 dark:text-gray-400">{b.degree.toFixed(2)}°</td>
                        <td className="px-4 py-2.5 text-gray-600 dark:text-gray-400">{b.navamsa}</td>
                        <td className="px-4 py-2.5"><GoodCell v={b.pushkara_navamsa} /></td>
                        <td className="px-4 py-2.5"><GoodCell v={b.pushkara_bhaga} /></td>
                        <td className="px-4 py-2.5"><BadCell v={b.vish_navamsa} /></td>
                        <td className="px-4 py-2.5"><BadCell v={b.mrityu_bhaga} /></td>
                      </tr>
                    ))}
                    <tr className="border-t border-gray-200 bg-gray-50 text-center font-bold dark:border-white/10 dark:bg-white/5">
                      <td className="px-4 py-2.5 text-right text-xs uppercase tracking-wide text-gray-500" colSpan={4}>
                        Totals
                      </td>
                      <td className="px-4 py-2.5 text-green-700 dark:text-green-400">{result.totals.pushkara_navamsa}</td>
                      <td className="px-4 py-2.5 text-green-700 dark:text-green-400">{result.totals.pushkara_bhaga}</td>
                      <td className="px-4 py-2.5 text-red-700 dark:text-red-400">{result.totals.vish_navamsa}</td>
                      <td className="px-4 py-2.5 text-red-700 dark:text-red-400">{result.totals.mrityu_bhaga}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <p className="border-t border-gray-100 px-4 py-4 text-xs leading-relaxed text-gray-500 dark:border-white/10 dark:text-gray-400">
                <span className="font-semibold text-green-700 dark:text-green-400">Auspicious:</span> Pushkara Navāṁśa (two
                nourishing navamsas per sign, by element) · Pushkara Bhāga (one auspicious degree per sign, ±1°).{" "}
                <span className="font-semibold text-red-700 dark:text-red-400">Poison:</span> Vish Navāṁśa (the poison
                navamsa per sign) · Mṛtyu Bhāga (the fatal degree per body per sign, ±1°). Mṛtyu Bhāga has no classical
                table for the outer planets (shown <em>n/a</em>). Vish Navāṁśa + Mṛtyu Bhāga feed the worldly-potential
                model (fewer poison degrees leans prominent); the Pushkara pair are shown for completeness (tested as
                fame-noise). Guidance only — consult an astrologer.
              </p>
            </div>
          )}
        </div>
      </Container>
    </div>
  );
}
