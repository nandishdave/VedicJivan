"use client";

import { Fragment, useState } from "react";
import { Sparkles, Loader2, AlertCircle, ChevronDown } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { PlaceOfBirthAutocomplete } from "@/components/booking/PlaceOfBirthAutocomplete";
import {
  kundliApi,
  type ArgalaResult,
  type ArgalaHouse,
  type ArgalaPair,
  type ArgalaPosition,
} from "@/lib/api";

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

function Verdict({ h }: { h: ArgalaHouse }) {
  if (h.verdict === "null") {
    return <span className="text-xs italic text-gray-400 dark:text-gray-500">no argala</span>;
  }
  if (h.verdict === "neutral") {
    return (
      <span className="text-xs font-semibold text-gray-500 dark:text-gray-400">
        neutral · obstructed
      </span>
    );
  }
  const pos = h.verdict === "positive";
  const width = Math.min(100, Math.abs(h.strength));
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
          pos ? "text-green-700 dark:text-green-400" : "text-red-700 dark:text-red-400"
        }`}
      >
        {signed(h.strength)}%
      </span>
    </div>
  );
}

function PositionsTable({ rows }: { rows: ArgalaPosition[] }) {
  return (
    <div className="mt-8 overflow-hidden rounded-2xl border border-gray-100 bg-white shadow-sm dark:border-white/10 dark:bg-dark-surface-card">
      <div className="border-b border-gray-100 px-4 py-3 dark:border-white/10">
        <h2 className="font-heading text-sm font-bold uppercase tracking-wide text-gray-500 dark:text-gray-400">
          Planetary Positions
        </h2>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-gray-500 dark:text-gray-400">
              <th className="px-4 py-2 text-left font-medium">Body</th>
              <th className="px-4 py-2 text-left font-medium">Sign</th>
              <th className="px-4 py-2 text-right font-medium">Degree</th>
              <th className="px-4 py-2 text-right font-medium">House</th>
            </tr>
          </thead>
          <tbody className="tabular-nums">
            {rows.map((r) => (
              <tr
                key={r.body}
                className={
                  "border-t border-gray-100 dark:border-white/10 " +
                  (r.body === "Ascendant" ? "bg-primary-50/50 dark:bg-primary-900/20" : "")
                }
              >
                <td className="px-4 py-1.5 font-medium text-vedic-dark dark:text-white">
                  {r.body}
                  {r.retrograde && (
                    <span className="ml-1 text-xs font-semibold text-red-500" title="Retrograde">
                      ℞
                    </span>
                  )}
                </td>
                <td className="px-4 py-1.5 text-gray-600 dark:text-gray-400">{r.sign}</td>
                <td className="px-4 py-1.5 text-right text-gray-600 dark:text-gray-400">
                  {r.degree.toFixed(2)}°
                </td>
                <td className="px-4 py-1.5 text-right text-gray-600 dark:text-gray-400">{r.house}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
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

function Pair({ pair }: { pair: ArgalaPair }) {
  const survivePct = Math.round(pair.survive * 100);
  const surviveLabel =
    survivePct > 0 ? `survives ${survivePct}%` : survivePct < 0 ? `reversed ${-survivePct}%` : "neutralised";
  const surviveColor =
    survivePct > 0
      ? "text-green-700 dark:text-green-400"
      : survivePct < 0
      ? "text-red-700 dark:text-red-400"
      : "text-gray-400 dark:text-gray-500";
  return (
    <div className="overflow-hidden rounded-lg border border-gray-100 dark:border-white/10">
      <div className="flex items-center justify-between gap-2 border-b border-gray-100 bg-gray-50 px-3 py-1.5 text-xs dark:border-white/10 dark:bg-white/5">
        <span className="font-medium text-gray-600 dark:text-gray-300">
          Argala from the {ord(pair.argala_from)} · counter (virodha) from the {ord(pair.virodha_from)}
        </span>
        <span className={`font-bold tabular-nums ${surviveColor}`}>{surviveLabel}</span>
      </div>

      {pair.argala.length > 0 && (
        <div className="overflow-x-auto">
          <table className="w-full text-xs">
            <thead>
              <tr className="text-gray-500 dark:text-gray-400">
                <th className="px-2 py-1 text-left font-medium">Planet</th>
                <th className="px-2 py-1 text-left font-medium">Sign</th>
                <th className="px-2 py-1 text-left font-medium">Dignity</th>
                <th className="px-2 py-1 text-right font-medium">Dignity</th>
                <th className="px-2 py-1 text-right font-medium">Role-fit</th>
                <th className="px-2 py-1 text-right font-medium">Shadbala</th>
                <th className="px-2 py-1 text-right font-medium">Contribution</th>
              </tr>
            </thead>
            <tbody className="tabular-nums">
              {pair.argala.map((r, i) => (
                <tr key={`${r.planet}-${i}`} className="border-t border-gray-100 dark:border-white/5">
                  <td className="px-2 py-1 font-semibold text-vedic-dark dark:text-white">{r.planet}</td>
                  <td className="px-2 py-1 text-gray-500 dark:text-gray-400">{r.sign}</td>
                  <td className="px-2 py-1 text-gray-500 dark:text-gray-400">{r.dignity}</td>
                  <td className={`px-2 py-1 text-right ${r.dignity_score >= 0 ? "text-green-700 dark:text-green-400" : "text-red-700 dark:text-red-400"}`}>
                    {signed(r.dignity_score)}
                  </td>
                  <td className={`px-2 py-1 text-right ${r.role_fit >= 0 ? "text-green-700 dark:text-green-400" : "text-red-700 dark:text-red-400"}`}>
                    {signed(r.role_fit)}
                  </td>
                  <td className="px-2 py-1 text-right text-gray-500 dark:text-gray-400">{r.shadbala.toFixed(1)}</td>
                  <td className={`px-2 py-1 text-right font-semibold ${r.contribution > 0 ? "text-green-700 dark:text-green-400" : r.contribution < 0 ? "text-red-700 dark:text-red-400" : "text-gray-400"}`}>
                    {signed(Math.round(r.contribution))}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {pair.virodha.length > 0 && (
        <div className="border-t border-gray-100 px-3 py-1.5 text-xs text-gray-500 dark:border-white/10 dark:text-gray-400">
          <span className="font-medium">Counter:</span>{" "}
          {pair.virodha.map((v) => `${v.planet} (SB ${v.shadbala.toFixed(0)})`).join(", ")}
          {pair.argala.length === 0 && " — no argala to obstruct"}
        </div>
      )}
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
              in its 2nd, 4th, 5th and 11th — each countered by its Virodha (12th, 10th, 9th, 3rd).
              Every house is a tug-of-war: <span className="font-semibold text-green-700 dark:text-green-400">green helps</span>,{" "}
              <span className="font-semibold text-red-700 dark:text-red-400">red harms</span>, and a
              matched counter leaves it <span className="font-semibold">neutral</span>. Tap a row for
              the pair-by-pair breakdown.
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
            <>
              <PositionsTable rows={result.positions} />

              <div className="mt-6 overflow-hidden rounded-2xl border border-gray-100 bg-white shadow-sm dark:border-white/10 dark:bg-dark-surface-card">
                <div className="border-b border-gray-100 px-4 py-3 dark:border-white/10">
                  <h2 className="font-heading text-sm font-bold uppercase tracking-wide text-gray-500 dark:text-gray-400">
                    Argala by House
                  </h2>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="bg-primary-600 text-white">
                        <th className="px-4 py-3 text-left font-semibold">House</th>
                      <th className="px-4 py-3 text-left font-semibold">Net Argala</th>
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
                              <div className="font-semibold text-vedic-dark dark:text-white">{ord(h.house)}</div>
                              <div className="text-xs text-gray-400 dark:text-gray-500">
                                {HOUSE_MEANING[h.house - 1]}
                              </div>
                            </td>
                            <td className="px-4 py-2.5">
                              <Verdict h={h} />
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
                                <ChevronDown className={`h-4 w-4 transition-transform ${open ? "rotate-180" : ""}`} />
                              </button>
                            </td>
                          </tr>
                          {open && (
                            <tr className="bg-gray-50/60 dark:bg-white/5">
                              <td colSpan={5} className="p-3">
                                {h.pairs.length ? (
                                  <div className="space-y-3">
                                    {h.pairs.map((pair, i) => (
                                      <Pair key={i} pair={pair} />
                                    ))}
                                  </div>
                                ) : (
                                  <p className="text-xs italic text-gray-400 dark:text-gray-500">
                                    No planet in this house&rsquo;s 2nd / 4th / 5th / 11th (or their counters) — nothing intervenes.
                                  </p>
                                )}
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
                Each argala is scaled by its Virodha counter —{" "}
                <span className="font-semibold">survives = (argala − counter) ÷ argala</span> of the
                Shadbala: unopposed it survives fully, a matched counter{" "}
                <span className="font-semibold">neutralises</span> it, and a stronger counter{" "}
                <span className="font-semibold">reverses</span> it (a defeated benefic argala becomes a
                loss, a defeated malefic argala becomes relief). Each argala then scores{" "}
                <span className="font-semibold">Dignity</span> toward the house (Exalted +2 · Own +1.5 ·
                Friend +1 · Enemy −1, or +0.5 if a functional benefic · Debilitated −2) plus{" "}
                <span className="font-semibold">Role-fit</span> (benefic on kendra/trikona/2/11, or
                malefic on upachaya 3/6/10/11, +1; malefic on 8/12, −1), weighted by{" "}
                <span className="font-semibold">Shadbala</span>. A strong exalted malefic on a career
                house reads green, not red. Guidance only — consult an astrologer.
              </p>
              </div>
            </>
          )}
        </div>
      </Container>
    </div>
  );
}
