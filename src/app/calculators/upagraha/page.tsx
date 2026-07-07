"use client";

import { useState } from "react";
import { Sparkles, Loader2, AlertCircle } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { PlaceOfBirthAutocomplete } from "@/components/booking/PlaceOfBirthAutocomplete";
import { kundliApi, type UpagrahaResult } from "@/lib/api";

const SIGN_ABBR = ["Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"];

// North-Indian house polygons on a 0–4 grid (House 1 = top-centre diamond).
const POLY: Record<number, [number, number][]> = {
  1: [[2, 0], [3, 1], [2, 2], [1, 1]], 2: [[0, 0], [2, 0], [1, 1]], 3: [[0, 0], [1, 1], [0, 2]],
  4: [[0, 2], [1, 1], [2, 2], [1, 3]], 5: [[0, 2], [1, 3], [0, 4]], 6: [[0, 4], [1, 3], [2, 4]],
  7: [[2, 4], [1, 3], [2, 2], [3, 3]], 8: [[2, 4], [3, 3], [4, 4]], 9: [[4, 4], [3, 3], [4, 2]],
  10: [[4, 2], [3, 3], [2, 2], [3, 1]], 11: [[4, 2], [3, 1], [4, 0]], 12: [[4, 0], [3, 1], [2, 0]],
};
const S = 60;
const W = 4 * S;
const centroid = (pts: [number, number][]): [number, number] => [
  (pts.reduce((a, p) => a + p[0], 0) / pts.length) * S,
  (pts.reduce((a, p) => a + p[1], 0) / pts.length) * S,
];

function UpagrahaChart({ result }: { result: UpagrahaResult }) {
  return (
    <svg viewBox={`0 0 ${W} ${W}`} className="mx-auto h-[300px] w-[300px]">
      <rect x={0} y={0} width={W} height={W} fill="#fff" stroke="#334155" strokeWidth={2} />
      <line x1={0} y1={0} x2={W} y2={W} stroke="#334155" />
      <line x1={W} y1={0} x2={0} y2={W} stroke="#334155" />
      <polygon points={`${2 * S},0 ${W},${2 * S} ${2 * S},${W} 0,${2 * S}`} fill="none" stroke="#334155" />
      {Array.from({ length: 12 }, (_, i) => i + 1).map((h) => {
        const sign = (result.lagna_sign + h - 1) % 12;
        const abbrs = result.by_sign[String(sign)] ?? [];
        const [cx, cy] = centroid(POLY[h]);
        return (
          <g key={h}>
            <text x={cx} y={cy - 8} textAnchor="middle" className="fill-gray-400 text-[9px]">
              {sign + 1}
            </text>
            {abbrs.map((a, i) => (
              <text
                key={a}
                x={cx}
                y={cy + 6 + i * 11}
                textAnchor="middle"
                className="fill-primary-600 text-[10px] font-semibold"
              >
                {a}
              </text>
            ))}
          </g>
        );
      })}
    </svg>
  );
}

export default function UpagrahaCalculatorPage() {
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
  const [result, setResult] = useState<UpagrahaResult | null>(null);

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
      const res = await kundliApi.upagraha({ dob: date, tob: time, lat: place.lat, lon: place.lon });
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
              Upagrahas (Sub-Planets)
            </h1>
            <p className="mx-auto mt-3 max-w-2xl text-sm text-gray-600 dark:text-gray-400">
              The eleven upagrahas — five Sun-derived shadow points (Dhūma, Vyatīpāta, Parivesha,
              Indrachāpa, Upaketu) and six time-based ones (Kāla, Mṛtyu, Arthaprahāra, Yamaghaṇṭaka,
              Māndi, Gulika). Their sign, longitude and nakṣatra, plus the Upagraha chart.
            </p>
          </div>

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
                {loading ? "Calculating…" : "Calculate Upagrahas"}
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
            <div className="mt-8 grid gap-6 lg:grid-cols-[1fr_auto]">
              <div className="overflow-hidden rounded-2xl border border-gray-100 bg-white shadow-sm dark:border-white/10 dark:bg-dark-surface-card">
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-sm">
                    <thead>
                      <tr className="bg-primary-600 text-white">
                        <th className="px-3 py-2.5 font-semibold">Upagraha</th>
                        <th className="px-3 py-2.5 font-semibold">Rāśi</th>
                        <th className="px-3 py-2.5 font-semibold tabular-nums">Longitude</th>
                        <th className="px-3 py-2.5 font-semibold">Nakṣatra</th>
                        <th className="px-3 py-2.5 text-center font-semibold">Pada</th>
                      </tr>
                    </thead>
                    <tbody>
                      {result.upagrahas.map((u) => (
                        <tr key={u.name} className="border-t border-gray-100 dark:border-white/10">
                          <td className="px-3 py-1.5 font-semibold text-vedic-dark dark:text-white">
                            {u.label}
                            <span className="ml-1.5 text-xs font-normal text-gray-400">{u.abbr}</span>
                          </td>
                          <td className="px-3 py-1.5 text-gray-600 dark:text-gray-300">
                            {SIGN_ABBR[u.sign]}
                          </td>
                          <td className="px-3 py-1.5 tabular-nums text-gray-600 dark:text-gray-300">
                            {u.dms}
                          </td>
                          <td className="px-3 py-1.5 text-gray-600 dark:text-gray-300">{u.nakshatra}</td>
                          <td className="px-3 py-1.5 text-center tabular-nums text-gray-600 dark:text-gray-300">
                            {u.pada}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              <div className="rounded-2xl border border-gray-100 bg-white p-4 shadow-sm dark:border-white/10 dark:bg-dark-surface-card">
                <div className="mb-2 text-center text-sm font-bold text-primary-600">Upagraha Chart</div>
                <UpagrahaChart result={result} />
              </div>
            </div>
          )}

          {result && (
            <div className="mt-4 rounded-xl border border-amber-200 bg-amber-50 p-4 text-xs text-amber-800 dark:border-amber-900/40 dark:bg-amber-900/20 dark:text-amber-200">
              <b>Method note.</b> The five Sun-derived upagrahas and Gulika use exact classical
              formulas. Kāla, Mṛtyu, Arthaprahāra, Yamaghaṇṭaka and Māndi follow the classical
              Parāśara Kālavelā method (the Ascendant at the start of each ruling planet&rsquo;s
              day/night portion); other software may place these by a different convention. Guidance
              only — consult an astrologer.
            </div>
          )}
        </div>
      </Container>
    </div>
  );
}
