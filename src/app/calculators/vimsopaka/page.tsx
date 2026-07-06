"use client";

import { useState } from "react";
import { Sparkles, Loader2, AlertCircle, Star } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { PlaceOfBirthAutocomplete } from "@/components/booking/PlaceOfBirthAutocomplete";
import { kundliApi, type VimsopakaResult, type VimsopakaPlanet } from "@/lib/api";

const PLANET_ORDER = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"];
const NODE_ORDER = ["Rahu", "Ketu"];
const OUTER_ORDER = ["Uranus", "Neptune", "Pluto"];

const BAND_CLASS: Record<string, string> = {
  "Very strong": "bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300",
  "Moderately strong": "bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300",
  Weak: "bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-300",
  "Very weak": "bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300",
};

function renderRow(name: string, x: VimsopakaPlanet | undefined, isTop: boolean, muted: boolean) {
  if (!x) return null;
  return (
    <tr
      key={name}
      className={
        "border-t border-gray-100 text-center dark:border-white/10 " +
        (isTop ? "bg-primary-50 dark:bg-primary-900/20 " : "") +
        (muted ? "opacity-70" : "")
      }
    >
      <td className="px-4 py-2.5 text-left font-medium text-vedic-dark dark:text-white">
        {name}
        {isTop && <Star className="ml-1 inline h-3.5 w-3.5 fill-gold-400 text-gold-500" />}
      </td>
      <td className="px-4 py-2.5 text-gray-600 dark:text-gray-400">{x.sign}</td>
      <td className="px-4 py-2.5 text-gray-600 dark:text-gray-400">{x.house}</td>
      <td className="px-4 py-2.5">
        <span className="font-bold text-vedic-dark dark:text-white">{x.vimsopaka.toFixed(2)}</span>
        <span className="ml-2 inline-block h-2 w-16 overflow-hidden rounded-full bg-gray-100 align-middle dark:bg-white/10">
          <span
            className="block h-full bg-gradient-to-r from-primary-300 to-primary-600"
            style={{ width: `${Math.min(100, (x.vimsopaka / 20) * 100)}%` }}
          />
        </span>
      </td>
      <td className="px-4 py-2.5">
        <span className={"inline-block rounded px-2 py-0.5 text-xs font-semibold " + (BAND_CLASS[x.band] || "")}>
          {x.band}
        </span>
      </td>
    </tr>
  );
}

export default function VimsopakaCalculatorPage() {
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
  const [result, setResult] = useState<VimsopakaResult | null>(null);

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
      const res = await kundliApi.vimsopaka({ dob: date, tob: time, lat: place.lat, lon: place.lon });
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
        <div className="mx-auto max-w-3xl">
          <div className="mb-8 text-center">
            <span className="inline-flex items-center gap-1.5 rounded-full bg-primary-50 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-primary-600 dark:bg-primary-900/20">
              <Sparkles className="h-3.5 w-3.5" /> Free Calculator
            </span>
            <h1 className="mt-4 font-heading text-3xl font-bold text-vedic-dark dark:text-white lg:text-4xl">
              Vimśopaka Bala Calculator
            </h1>
            <p className="mx-auto mt-3 max-w-xl text-sm text-gray-600 dark:text-gray-400">
              Each planet&apos;s cross-divisional strength (0–20) across the sixteen Shodashavarga charts.
              The strongest planet in a prominence seat (1st/2nd/4th/5th/11th) is a marker of worldly potential.
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
                {loading ? "Calculating…" : "Calculate Vimśopaka Bala"}
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
                      <th className="px-4 py-3 text-left font-semibold">Planet</th>
                      <th className="px-4 py-3 font-semibold">Sign</th>
                      <th className="px-4 py-3 font-semibold">House</th>
                      <th className="px-4 py-3 font-semibold">Vimśopaka / 20</th>
                      <th className="px-4 py-3 font-semibold">Strength</th>
                    </tr>
                  </thead>
                  <tbody>
                    {PLANET_ORDER.map((p) => renderRow(p, result.planets[p], p === result.strongest.planet, false))}
                    <tr className="border-t border-gray-100 dark:border-white/10">
                      <td
                        colSpan={5}
                        className="bg-gray-50 px-4 py-1.5 text-left text-[11px] font-semibold uppercase tracking-wide text-gray-400 dark:bg-white/5 dark:text-gray-500"
                      >
                        Nodes — reference only (Parāśara dignities; not in the average or the strongest pick)
                      </td>
                    </tr>
                    {NODE_ORDER.map((p) => renderRow(p, result.planets[p], false, true))}
                    {OUTER_ORDER.every((p) => result.planets[p]) && (
                      <>
                        <tr className="border-t border-gray-100 dark:border-white/10">
                          <td
                            colSpan={5}
                            className="bg-gray-50 px-4 py-1.5 text-left text-[11px] font-semibold uppercase tracking-wide text-gray-400 dark:bg-white/5 dark:text-gray-500"
                          >
                            Outer planets — reference only (modern rulerships; not in the average or the strongest pick)
                          </td>
                        </tr>
                        {OUTER_ORDER.map((p) => renderRow(p, result.planets[p], false, true))}
                      </>
                    )}
                  </tbody>
                </table>
              </div>
              <div className="space-y-2 border-t border-gray-100 p-5 text-sm text-gray-600 dark:border-white/10 dark:text-gray-400">
                <p>
                  Lagna <b className="text-vedic-dark dark:text-white">{result.lagna}</b> · chart average{" "}
                  <b className="text-vedic-dark dark:text-white">{result.average.toFixed(2)}</b> / 20.
                </p>
                <p>
                  Strongest planet: <b className="text-vedic-dark dark:text-white">{result.strongest.planet}</b> (
                  {result.strongest.vimsopaka.toFixed(2)}) in house {result.strongest.house} —{" "}
                  {result.strongest.in_prominence_seat ? (
                    <span className="font-semibold text-green-700 dark:text-green-400">
                      in a prominence seat (1/2/4/5/11) ✓
                    </span>
                  ) : (
                    <span>not in a prominence seat (1/2/4/5/11).</span>
                  )}
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-500">
                  Band per planet: 15–20 very strong · 10–15 moderately strong · 5–10 weak · below 5 very weak.
                  Vimśopaka grades a planet&apos;s dignity across all sixteen divisional charts (D60/D1/D9 weighted most).
                  Rāhu &amp; Ketu are shown for reference (Parāśara node dignities) — classical Vimśopaka is a 7-graha
                  measure, so the nodes are excluded from the average and the strongest-planet pick.
                </p>
              </div>
            </div>
          )}
        </div>
      </Container>
    </div>
  );
}
