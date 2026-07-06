"use client";

import { Fragment, useState } from "react";
import { Sparkles, Loader2, AlertCircle, ChevronDown } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { PlaceOfBirthAutocomplete } from "@/components/booking/PlaceOfBirthAutocomplete";
import { kundliApi, type ShadbalaResult, type SbPlanet } from "@/lib/api";

const BALAS: { key: keyof SbPlanet["balas"]; label: string }[] = [
  { key: "sthana", label: "Sthāna" },
  { key: "dig", label: "Dig" },
  { key: "kala", label: "Kāla" },
  { key: "cheshta", label: "Cheṣṭā" },
  { key: "naisargika", label: "Naisargika" },
  { key: "drik", label: "Dṛk" },
];

function num(v: number): string {
  return v.toFixed(2);
}

function SubTable({ title, parts }: { title: string; parts: Record<string, number> }) {
  return (
    <div>
      <div className="px-1 pb-1 pt-2 text-[11px] font-bold uppercase tracking-wide text-gray-400 dark:text-gray-500">
        {title} Bala
      </div>
      <table className="w-full text-xs">
        <tbody className="tabular-nums">
          {Object.entries(parts).map(([label, v]) => (
            <tr key={label} className="border-t border-gray-100 dark:border-white/5">
              <td className="px-2 py-0.5 text-gray-600 dark:text-gray-400">{label}</td>
              <td className="px-2 py-0.5 text-right text-gray-700 dark:text-gray-300">{num(v)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default function ShadbalaCalculatorPage() {
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
  const [result, setResult] = useState<ShadbalaResult | null>(null);
  const [open, setOpen] = useState<Set<string>>(new Set());

  const canSubmit = !!date && !!time && !!place && !loading;

  const toggle = (planet: string) =>
    setOpen((prev) => {
      const next = new Set(prev);
      if (next.has(planet)) next.delete(planet);
      else next.add(planet);
      return next;
    });

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!place) {
      setError("Please choose a birth place.");
      return;
    }
    setLoading(true);
    setError("");
    setOpen(new Set());
    try {
      const res = await kundliApi.shadbala({ dob: date, tob: time, lat: place.lat, lon: place.lon });
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
              Shadbala Calculator
            </h1>
            <p className="mx-auto mt-3 max-w-2xl text-sm text-gray-600 dark:text-gray-400">
              Shadbala is a planet&rsquo;s <span className="font-semibold">six-fold strength</span> —
              Sthāna, Dig, Kāla, Cheṣṭā, Naisargika and Dṛk bala — summed in Rūpas and compared to a
              classical minimum. A ratio ≥{" "}
              <span className="font-semibold text-green-700 dark:text-green-400">1</span> means the
              planet is sufficiently strong. Tap a planet for the sub-bala breakdown.
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
                {loading ? "Calculating…" : "Calculate Shadbala"}
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
                      <th className="px-3 py-3 text-left font-semibold">Planet</th>
                      {BALAS.map((b) => (
                        <th key={b.key} className="px-2 py-3 font-semibold">{b.label}</th>
                      ))}
                      <th className="px-2 py-3 font-semibold">Total</th>
                      <th className="px-2 py-3 font-semibold">Req.</th>
                      <th className="px-2 py-3 font-semibold">Ratio</th>
                      <th className="px-2 py-3" aria-label="Expand" />
                    </tr>
                  </thead>
                  <tbody>
                    {result.planets.map((p) => {
                      const isOpen = open.has(p.planet);
                      return (
                        <Fragment key={p.planet}>
                          <tr
                            onClick={() => toggle(p.planet)}
                            className="cursor-pointer border-t border-gray-100 hover:bg-gray-50 dark:border-white/10 dark:hover:bg-white/5"
                          >
                            <td className="px-3 py-2 text-left font-semibold text-vedic-dark dark:text-white">
                              {p.planet}
                              <span className="ml-1.5 text-xs font-normal text-gray-400">#{p.rank}</span>
                            </td>
                            {BALAS.map((b) => (
                              <td
                                key={b.key}
                                className={`px-2 py-2 ${p.balas[b.key] < 0 ? "text-red-600 dark:text-red-400" : "text-gray-600 dark:text-gray-300"}`}
                              >
                                {num(p.balas[b.key])}
                              </td>
                            ))}
                            <td className="px-2 py-2 font-bold text-vedic-dark dark:text-white">{num(p.total)}</td>
                            <td className="px-2 py-2 text-gray-500 dark:text-gray-400">{num(p.required)}</td>
                            <td className="px-2 py-2">
                              <span
                                className={`inline-block rounded px-1.5 py-0.5 text-xs font-bold ${
                                  p.sufficient
                                    ? "bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300"
                                    : "bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300"
                                }`}
                              >
                                {num(p.ratio)}
                              </span>
                            </td>
                            <td className="px-2 py-2 text-right">
                              <ChevronDown
                                className={`ml-auto h-4 w-4 text-gray-400 transition-transform ${isOpen ? "rotate-180" : ""}`}
                              />
                            </td>
                          </tr>
                          {isOpen && (
                            <tr className="bg-gray-50/60 dark:bg-white/5">
                              <td colSpan={11} className="px-4 py-3">
                                <div className="grid gap-4 sm:grid-cols-2">
                                  <SubTable title="Sthāna" parts={p.sthana_parts} />
                                  <SubTable title="Kāla" parts={p.kala_parts} />
                                </div>
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
                All values in <span className="font-semibold">Rūpas</span> (1 Rūpa = 60 Virūpas). The six
                balas sum to the Total; <span className="font-semibold">Ratio = Total ÷ Required</span> —{" "}
                <span className="font-semibold text-green-700 dark:text-green-400">green ≥ 1</span> is strong,{" "}
                <span className="font-semibold text-red-700 dark:text-red-400">red &lt; 1</span> is weak. Dṛk
                (aspect) bala can be negative when malefics aspect the planet. #rank is the strength order.
                Guidance only — consult an astrologer.
              </p>
            </div>
          )}
        </div>
      </Container>
    </div>
  );
}
