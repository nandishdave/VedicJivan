"use client";

import { useState } from "react";
import { Heart, Loader2, AlertCircle, Sparkles } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { PlaceOfBirthAutocomplete } from "@/components/booking/PlaceOfBirthAutocomplete";
import { kundliApi, type MatchingResult, type MatchChart, type PersonSummary } from "@/lib/api";

type Place = { name: string; lat: number; lon: number };

// North-Indian house polygons on a 0–4 grid (House 1 = top-centre diamond).
const POLY: Record<number, [number, number][]> = {
  1: [[2, 0], [3, 1], [2, 2], [1, 1]], 2: [[0, 0], [2, 0], [1, 1]], 3: [[0, 0], [1, 1], [0, 2]],
  4: [[0, 2], [1, 1], [2, 2], [1, 3]], 5: [[0, 2], [1, 3], [0, 4]], 6: [[0, 4], [1, 3], [2, 4]],
  7: [[2, 4], [1, 3], [2, 2], [3, 3]], 8: [[2, 4], [3, 3], [4, 4]], 9: [[4, 4], [3, 3], [4, 2]],
  10: [[4, 2], [3, 3], [2, 2], [3, 1]], 11: [[4, 2], [3, 1], [4, 0]], 12: [[4, 0], [3, 1], [2, 0]],
};
const CH_S = 44;
const CH_W = 4 * CH_S;
const chCentroid = (pts: [number, number][]): [number, number] => [
  (pts.reduce((a, p) => a + p[0], 0) / pts.length) * CH_S,
  (pts.reduce((a, p) => a + p[1], 0) / pts.length) * CH_S,
];

function NorthChart({ chart, title }: { chart: MatchChart; title: string }) {
  return (
    <div className="text-center">
      <div className="mb-1 text-xs font-bold text-primary-600">{title}</div>
      <svg viewBox={`0 0 ${CH_W} ${CH_W}`} className="mx-auto aspect-square w-full max-w-[170px]">
        <rect x={0} y={0} width={CH_W} height={CH_W} fill="#fff" stroke="#334155" strokeWidth={2} />
        <line x1={0} y1={0} x2={CH_W} y2={CH_W} stroke="#334155" />
        <line x1={CH_W} y1={0} x2={0} y2={CH_W} stroke="#334155" />
        <polygon points={`${2 * CH_S},0 ${CH_W},${2 * CH_S} ${2 * CH_S},${CH_W} 0,${2 * CH_S}`} fill="none" stroke="#334155" />
        {Array.from({ length: 12 }, (_, i) => i + 1).map((h) => {
          const sign = (chart.asc_sign + h - 1) % 12;
          const abbrs = chart.by_sign[String(sign)] ?? [];
          const [cx, cy] = chCentroid(POLY[h]);
          return (
            <g key={h}>
              <text x={cx} y={cy - abbrs.length * 4 - 2} textAnchor="middle" className="fill-gray-300 text-[8px]">
                {sign + 1}
              </text>
              {abbrs.map((a, i) => (
                <text key={a} x={cx} y={cy + 4 + i * 9} textAnchor="middle" className="fill-vedic-dark text-[9px] font-semibold">
                  {a}
                </text>
              ))}
            </g>
          );
        })}
      </svg>
    </div>
  );
}

function SummaryCard({ label, s }: { label: string; s: PersonSummary }) {
  const rows: [string, string][] = [
    ["Lagna", `${s.lagna} (${s.lagna_lord})`],
    ["Rāśi", `${s.rashi} (${s.rashi_lord})`],
    ["Nakṣatra", `${s.nakshatra} – ${s.pada} (${s.nakshatra_lord})`],
    ["Gana", s.gana],
    ["Nadi", s.nadi],
    ["Yoni", s.yoni],
    ["Varna", s.varna],
    ["Vasya", s.vasya],
  ];
  return (
    <div className="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm dark:border-white/10 dark:bg-dark-surface-card">
      <div className="mb-3 text-sm font-bold uppercase tracking-wide text-primary-600">{label}</div>
      <dl className="grid grid-cols-[auto_1fr] gap-x-4 gap-y-1.5 text-sm">
        {rows.map(([k, v]) => (
          <div key={k} className="contents">
            <dt className="text-gray-500 dark:text-gray-400">{k}</dt>
            <dd className="font-medium text-vedic-dark dark:text-gray-200">{v}</dd>
          </div>
        ))}
      </dl>
    </div>
  );
}

function ChartTrio({ label, charts }: { label: string; charts: Record<string, MatchChart> }) {
  return (
    <div className="rounded-2xl border border-gray-100 bg-white p-4 shadow-sm dark:border-white/10 dark:bg-dark-surface-card">
      <div className="mb-2 text-sm font-bold uppercase tracking-wide text-primary-600">{label}</div>
      <div className="grid grid-cols-3 gap-2">
        <NorthChart chart={charts.D1} title="Lagna" />
        <NorthChart chart={charts.D9} title="Navāṁśa" />
        <NorthChart chart={charts.Moon} title="Chandra" />
      </div>
    </div>
  );
}

function PersonFields({
  label,
  date,
  setDate,
  time,
  setTime,
  placeInput,
  setPlace,
  setPlaceInput,
}: {
  label: string;
  date: string;
  setDate: (v: string) => void;
  time: string;
  setTime: (v: string) => void;
  placeInput: string;
  setPlace: (p: Place | null) => void;
  setPlaceInput: (v: string) => void;
}) {
  return (
    <div className="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm dark:border-white/10 dark:bg-dark-surface-card">
      <div className="mb-3 text-sm font-bold uppercase tracking-wide text-primary-600">{label}</div>
      <div className="grid gap-3">
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
        <div>
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
      </div>
    </div>
  );
}

function MangalBadge({ grade }: { grade: string }) {
  const color =
    grade === "No"
      ? "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300"
      : grade === "Low"
        ? "bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300"
        : "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300";
  return <span className={`rounded-full px-2.5 py-0.5 text-xs font-semibold ${color}`}>{grade} Dosha</span>;
}

export default function HoroscopeMatchingPage() {
  // Boy
  const [bDate, setBDate] = useState("1988-04-22");
  const [bTime, setBTime] = useState("16:15");
  const [bPlace, setBPlace] = useState<Place | null>({ name: "Ahmedabad, Gujarat, India", lat: 23.033, lon: 72.583 });
  const [bPlaceInput, setBPlaceInput] = useState("Ahmedabad, Gujarat, India");
  // Girl
  const [gDate, setGDate] = useState("1988-09-24");
  const [gTime, setGTime] = useState("12:45");
  const [gPlace, setGPlace] = useState<Place | null>({ name: "Mumbai, Maharashtra, India", lat: 19.067, lon: 72.867 });
  const [gPlaceInput, setGPlaceInput] = useState("Mumbai, Maharashtra, India");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<MatchingResult | null>(null);

  const canSubmit = !!bDate && !!bTime && !!bPlace && !!gDate && !!gTime && !!gPlace && !loading;

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!bPlace || !gPlace) {
      setError("Please choose a birth place for both people.");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const res = await kundliApi.horoscopeMatching({
        boy: { dob: bDate, tob: bTime, lat: bPlace.lat, lon: bPlace.lon },
        girl: { dob: gDate, tob: gTime, lat: gPlace.lat, lon: gPlace.lon },
      });
      setResult(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not calculate. Check the inputs.");
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  const pct = result ? Math.round((result.total / result.max_total) * 100) : 0;

  return (
    <div className="bg-vedic-bg py-12 dark:bg-dark-bg lg:py-16">
      <Container>
        <div className="mx-auto max-w-4xl">
          <div className="mb-8 text-center">
            <span className="inline-flex items-center gap-1.5 rounded-full bg-primary-50 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-primary-600 dark:bg-primary-900/20">
              <Sparkles className="h-3.5 w-3.5" /> Free Calculator
            </span>
            <h1 className="mt-4 font-heading text-3xl font-bold text-vedic-dark dark:text-white lg:text-4xl">
              Kundli Matching (Guna Milap)
            </h1>
            <p className="mx-auto mt-3 max-w-2xl text-sm text-gray-600 dark:text-gray-400">
              The classical Ashtakoota compatibility method — eight kootas out of 36 points (Varna,
              Vasya, Tara, Yoni, Graha-Maitri, Gana, Bhakoot, Nadi) plus Mangal (Manglik) Dosha.
            </p>
          </div>

          <form onSubmit={onSubmit} className="grid gap-4 sm:grid-cols-2">
            <PersonFields
              label="Groom (Boy)"
              date={bDate}
              setDate={setBDate}
              time={bTime}
              setTime={setBTime}
              placeInput={bPlaceInput}
              setPlace={setBPlace}
              setPlaceInput={setBPlaceInput}
            />
            <PersonFields
              label="Bride (Girl)"
              date={gDate}
              setDate={setGDate}
              time={gTime}
              setTime={setGTime}
              placeInput={gPlaceInput}
              setPlace={setGPlace}
              setPlaceInput={setGPlaceInput}
            />
            <div className="sm:col-span-2">
              <button
                type="submit"
                disabled={!canSubmit}
                aria-busy={loading}
                className="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-primary-600 px-5 py-3 text-sm font-semibold text-white transition-colors hover:bg-primary-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-60"
              >
                {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Heart className="h-4 w-4" />}
                {loading ? "Matching…" : "Match Horoscopes"}
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
            <div className="mt-8 space-y-6">
              {/* Score header */}
              <div className="flex flex-col items-center gap-3 rounded-2xl border border-gray-100 bg-white p-6 text-center shadow-sm dark:border-white/10 dark:bg-dark-surface-card">
                <div className="text-5xl font-bold text-primary-600">
                  {result.total}
                  <span className="text-2xl text-gray-400"> / {result.max_total}</span>
                </div>
                <div className="h-2 w-full max-w-md overflow-hidden rounded-full bg-gray-100 dark:bg-white/10">
                  <div className="h-full rounded-full bg-primary-500" style={{ width: `${pct}%` }} />
                </div>
                <div className="flex flex-wrap items-center justify-center gap-3 text-sm">
                  <span className="text-gray-500 dark:text-gray-400">Groom:</span>
                  <MangalBadge grade={result.boy_mangal} />
                  <span className="text-gray-500 dark:text-gray-400">Bride:</span>
                  <MangalBadge grade={result.girl_mangal} />
                </div>
                <p className="max-w-xl text-sm font-medium text-vedic-dark dark:text-gray-200">{result.verdict}</p>
              </div>

              {/* Birth details */}
              <div className="grid gap-4 sm:grid-cols-2">
                <SummaryCard label="Groom (Boy)" s={result.boy_summary} />
                <SummaryCard label="Bride (Girl)" s={result.girl_summary} />
              </div>

              {/* Charts */}
              <div className="grid gap-4 sm:grid-cols-2">
                <ChartTrio label="Groom (Boy)" charts={result.boy_charts} />
                <ChartTrio label="Bride (Girl)" charts={result.girl_charts} />
              </div>

              {/* Koota table */}
              <div className="overflow-hidden rounded-2xl border border-gray-100 bg-white shadow-sm dark:border-white/10 dark:bg-dark-surface-card">
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-sm">
                    <thead>
                      <tr className="bg-primary-600 text-white">
                        <th className="px-3 py-2.5 font-semibold">Koota</th>
                        <th className="px-3 py-2.5 font-semibold">Groom</th>
                        <th className="px-3 py-2.5 font-semibold">Bride</th>
                        <th className="px-3 py-2.5 text-center font-semibold tabular-nums">Points</th>
                        <th className="px-3 py-2.5 font-semibold">Area</th>
                      </tr>
                    </thead>
                    <tbody>
                      {result.kootas.map((k) => (
                        <tr key={k.koota} className="border-t border-gray-100 dark:border-white/10">
                          <td className="px-3 py-1.5 font-semibold text-vedic-dark dark:text-white">{k.koota}</td>
                          <td className="px-3 py-1.5 text-gray-600 dark:text-gray-300">{k.boy}</td>
                          <td className="px-3 py-1.5 text-gray-600 dark:text-gray-300">{k.girl}</td>
                          <td
                            className={
                              "px-3 py-1.5 text-center font-semibold tabular-nums " +
                              (k.points === 0
                                ? "text-red-600 dark:text-red-400"
                                : k.points >= k.max * 0.66
                                  ? "text-green-600 dark:text-green-400"
                                  : "text-amber-600 dark:text-amber-400")
                            }
                          >
                            {k.points} / {k.max}
                          </td>
                          <td className="px-3 py-1.5 text-gray-500 dark:text-gray-400">{k.area}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Interpretations */}
              <div className="rounded-2xl border border-gray-100 bg-white p-5 shadow-sm dark:border-white/10 dark:bg-dark-surface-card">
                <div className="mb-3 text-sm font-bold uppercase tracking-wide text-gray-500 dark:text-gray-400">
                  Interpretation of Each Koota
                </div>
                <div className="space-y-4">
                  {result.kootas.map((k) => (
                    <div key={k.koota}>
                      <div className="text-sm font-semibold text-primary-600">
                        {k.koota} — {k.points} / {k.max}
                      </div>
                      <p className="mt-0.5 text-sm text-gray-600 dark:text-gray-300">{k.interpretation}</p>
                    </div>
                  ))}
                </div>
              </div>

              <p className="text-center text-xs text-gray-400 dark:text-gray-500">
                Ashtakoota + Mangal-Dosha guidance only — consult an astrologer before any decision.
              </p>
            </div>
          )}
        </div>
      </Container>
    </div>
  );
}
