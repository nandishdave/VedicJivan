"use client";

import { useState } from "react";
import { Sparkles, Loader2, AlertCircle, Star } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { PlaceOfBirthAutocomplete } from "@/components/booking/PlaceOfBirthAutocomplete";
import {
  muhurtaApi,
  type MuhurtaResult,
  type MuhurtaVerdict,
} from "@/lib/api";

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

const VERDICT_CELL: Record<MuhurtaVerdict, string> = {
  good: "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300",
  moderate: "bg-amber-50 text-amber-700 dark:bg-amber-900/20 dark:text-amber-300",
  challenging: "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300",
};
const VERDICT_LETTER: Record<MuhurtaVerdict, string> = {
  good: "G",
  moderate: "M",
  challenging: "W",
};

function todayISO(): string {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

export default function MuhurtaPage() {
  const [date, setDate] = useState(todayISO());
  const [place, setPlace] = useState<{ name: string; lat: number; lon: number } | null>(null);
  const [priorities, setPriorities] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<MuhurtaResult | null>(null);

  const canSubmit = !!date && !!place && !loading;

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
    setResult(null);
    try {
      const r = await muhurtaApi.analyzeBirth({
        date,
        lat: place.lat,
        lon: place.lon,
        place_name: place.name,
        priorities: priorities.size ? Array.from(priorities) : null,
      });
      setResult(r);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container className="py-12">
      <div className="mx-auto max-w-6xl">
        {/* Header */}
        <div className="mb-8 text-center">
          <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-primary-100 dark:bg-primary-900/30">
            <Sparkles className="h-7 w-7 text-primary-600" />
          </div>
          <h1 className="mb-2 text-3xl font-bold text-gray-900 dark:text-white">
            Auspicious Birth-Time Calculator
          </h1>
          <p className="mx-auto max-w-2xl text-gray-600 dark:text-gray-400">
            For a chosen day and place, see every rising ascendant (Lagna) ranked by strength —
            and how each one favours or challenges every area of life. No Lagna is perfect; pick the
            window that matches what matters most.
          </p>
        </div>

        {/* Form */}
        <form
          onSubmit={handleSubmit}
          className="mb-10 grid gap-5 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-white/5 p-6 shadow-sm sm:grid-cols-2"
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
            <label className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">
              Place
            </label>
            <PlaceOfBirthAutocomplete
              value={place?.name ?? ""}
              onPlaceSelect={(p) => setPlace({ name: p.name, lat: p.latitude, lon: p.longitude })}
            />
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
              className="w-full rounded-lg bg-primary-600 px-6 py-3 text-sm font-medium text-white hover:bg-primary-700 disabled:cursor-not-allowed disabled:opacity-50 transition-colors"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Analysing the 12 ascendant windows…
                </span>
              ) : (
                "Find Auspicious Windows"
              )}
            </button>
          </div>
        </form>

        {result && <Results result={result} />}
      </div>
    </Container>
  );
}

function StrengthBar({ value }: { value: number }) {
  const color = value >= 70 ? "bg-green-500" : value >= 55 ? "bg-amber-500" : "bg-red-400";
  return (
    <div className="flex items-center gap-2">
      <div className="h-2 w-14 overflow-hidden rounded-full bg-gray-200 dark:bg-gray-700">
        <div className={`h-full ${color}`} style={{ width: `${value}%` }} />
      </div>
      <span className="text-xs font-semibold text-gray-700 dark:text-gray-300">{Math.round(value)}</span>
    </div>
  );
}

function Results({ result }: { result: MuhurtaResult }) {
  return (
    <div className="space-y-10">
      {/* Summary */}
      <div className="rounded-xl bg-primary-50 dark:bg-primary-900/10 px-5 py-4 text-sm text-gray-700 dark:text-gray-300">
        <strong className="text-primary-700 dark:text-primary-300">Auspicious birth windows</strong> for{" "}
        <strong>{result.date}</strong> at <strong>{result.place_name}</strong>
        {result.priorities.length > 0 && (
          <> — ranked for: <strong>{result.priorities.join(", ")}</strong></>
        )}
        . Each row is one rising Lagna; cells show how that ascendant favours each life area.
      </div>

      {/* Ranked grid */}
      <div>
        <h2 className="mb-3 text-xl font-bold text-gray-900 dark:text-white">Rising Lagna Windows</h2>
        <div className="overflow-x-auto rounded-lg border border-gray-200 dark:border-gray-700">
          <table className="min-w-full border-collapse text-sm">
            <thead>
              <tr className="bg-primary-600 text-white">
                <th className="px-2 py-2 text-left font-semibold">#</th>
                <th className="px-2 py-2 text-left font-semibold">Lagna</th>
                <th className="px-2 py-2 text-left font-semibold">Lord</th>
                <th className="px-2 py-2 text-left font-semibold whitespace-nowrap">Window</th>
                <th className="px-2 py-2 text-left font-semibold">Strength</th>
                {ASPECTS.map((a) => (
                  <th key={a.key} title={a.label} className="px-1.5 py-2 text-center text-[11px] font-semibold whitespace-nowrap">
                    {a.short}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {result.windows.map((w) => (
                <tr key={w.lagna_sign} className="border-t border-gray-100 dark:border-gray-800">
                  <td className="px-2 py-2 font-bold text-primary-600">{w.rank}</td>
                  <td className="px-2 py-2 font-semibold text-gray-900 dark:text-white whitespace-nowrap">
                    {w.lagna_name}
                  </td>
                  <td className="px-2 py-2 text-gray-600 dark:text-gray-300 whitespace-nowrap">
                    {w.lagna_lord}
                    {w.lord_retrograde && <span className="text-red-500"> (R)</span>}
                  </td>
                  <td className="px-2 py-2 text-gray-600 dark:text-gray-300 whitespace-nowrap">
                    {w.window.start}–{w.window.end}
                  </td>
                  <td className="px-2 py-2"><StrengthBar value={w.overall} /></td>
                  {ASPECTS.map((a) => {
                    const v = w.aspects[a.key]?.verdict ?? "moderate";
                    return (
                      <td key={a.key} className="px-1 py-1.5 text-center">
                        <span
                          className={`inline-flex h-6 w-6 items-center justify-center rounded-full text-xs font-bold ${VERDICT_CELL[v]}`}
                          title={`${a.label}: ${Math.round(w.aspects[a.key]?.score ?? 0)}`}
                        >
                          {VERDICT_LETTER[v]}
                        </span>
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="mt-3 flex flex-wrap items-center gap-x-4 gap-y-2 text-xs text-gray-500">
          <span className="font-medium text-gray-600 dark:text-gray-400">Legend:</span>
          <span className="inline-flex items-center gap-1.5">
            <span className={`inline-flex h-5 w-5 items-center justify-center rounded-full text-[10px] font-bold ${VERDICT_CELL.good}`}>G</span> = Good
          </span>
          <span className="inline-flex items-center gap-1.5">
            <span className={`inline-flex h-5 w-5 items-center justify-center rounded-full text-[10px] font-bold ${VERDICT_CELL.moderate}`}>M</span> = Moderate
          </span>
          <span className="inline-flex items-center gap-1.5">
            <span className={`inline-flex h-5 w-5 items-center justify-center rounded-full text-[10px] font-bold ${VERDICT_CELL.challenging}`}>W</span> = Weak
          </span>
          <span className="text-gray-400">· (R) = Lagna-lord retrograde · hover a cell for its 0–100 score</span>
        </div>
      </div>

      {/* Planetary positions */}
      <div>
        <h2 className="mb-3 flex items-center gap-2 text-xl font-bold text-gray-900 dark:text-white">
          <Star className="h-5 w-5 text-primary-600" /> Planetary Positions
          <span className="text-sm font-normal text-gray-400">({result.date}, noon)</span>
        </h2>
        <div className="overflow-x-auto rounded-lg border border-gray-200 dark:border-gray-700">
          <table className="min-w-full border-collapse text-sm">
            <thead>
              <tr className="bg-primary-600 text-white">
                <th className="px-3 py-2 text-left font-semibold">Planet</th>
                <th className="px-3 py-2 text-left font-semibold">Rashi (Sign)</th>
                <th className="px-3 py-2 text-left font-semibold">Degree</th>
                <th className="px-3 py-2 text-left font-semibold">Motion</th>
              </tr>
            </thead>
            <tbody>
              {result.planet_positions.map((p, i) => (
                <tr
                  key={p.planet}
                  className={`border-t border-gray-100 dark:border-gray-800 ${i % 2 ? "bg-gray-50 dark:bg-white/5" : ""}`}
                >
                  <td className="px-3 py-2 font-semibold text-gray-900 dark:text-white">{p.planet}</td>
                  <td className="px-3 py-2 text-gray-700 dark:text-gray-300">{p.sign}</td>
                  <td className="px-3 py-2 text-gray-700 dark:text-gray-300">{p.degree_dms}</td>
                  <td className="px-3 py-2">
                    <span className={p.retrograde ? "font-medium text-red-600 dark:text-red-400" : "text-green-700 dark:text-green-400"}>
                      {p.motion}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <p className="text-center text-xs text-gray-400">
        Computed with Lahiri ayanamsha (Swiss Ephemeris), Whole-Sign houses, Ashtakavarga &amp; Shadbala.
        Verdicts are guidance, not absolutes — consult an astrologer for a final decision.
      </p>
    </div>
  );
}
