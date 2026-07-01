import { notFound } from "next/navigation";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { NorthIndianChart } from "@/components/charts/NorthIndianChart";
import { chartHouses, ABBR, type VargaKey } from "@/lib/celebrities";
import { ordinary, getOrdinary } from "@/lib/ordinary";

export function generateStaticParams() {
  return ordinary.map((p) => ({ slug: p.slug }));
}

export function generateMetadata({ params }: { params: { slug: string } }) {
  const p = getOrdinary(params.slug);
  return { title: p ? `${p.name} — Birth Chart | VedicJivan` : "Ordinary Chart | VedicJivan" };
}

const VARGAS: { key: VargaKey; label: string; note: string }[] = [
  { key: "D1", label: "D1 · Rāśi", note: "body & life" },
  { key: "D2", label: "D2 · Horā", note: "wealth" },
  { key: "D4", label: "D4 · Chaturthāṁśa", note: "property & fortune" },
  { key: "D9", label: "D9 · Navāṁśa", note: "strength & fortune" },
  { key: "D10", label: "D10 · Daśāṁśa", note: "career & power" },
  { key: "D11", label: "D11 · Rudrāṁśa", note: "gains & income" },
  { key: "D16", label: "D16 · Ṣoḍaśāṁśa", note: "luxuries & comforts" },
  { key: "D24", label: "D24 · Siddhāṁśa", note: "knowledge & skill" },
  { key: "D60", label: "D60 · Ṣaṣṭyāṁśa", note: "karma (finest)" },
];

export default function OrdinaryChartPage({ params }: { params: { slug: string } }) {
  const p = getOrdinary(params.slug);
  if (!p) notFound();

  return (
    <Container className="py-10">
      <Link href="/ordinary" className="mb-6 inline-flex items-center gap-1 text-sm text-primary-600 hover:underline">
        <ArrowLeft className="h-4 w-4" /> All ordinary charts
      </Link>

      <h1 className="mb-1 text-3xl font-bold text-gray-900 dark:text-white">{p.name}</h1>
      <p className="mb-6 text-sm text-gray-500 dark:text-gray-500">
        {p.sex} · {p.birth.date} · {p.birth.time} · {p.birth.place} &nbsp;|&nbsp; <strong>{p.lagna}</strong> Lagna
        (lord {p.lagna_lord}) · {p.nakshatra} nakshatra
      </p>

      <div className="mb-10 grid gap-6 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-white/5 p-6 sm:grid-cols-2 lg:grid-cols-4">
        {VARGAS.map((v) => (
          <NorthIndianChart key={v.key} title={v.label} subtitle={v.note} data={chartHouses(p, v.key)} />
        ))}
      </div>

      <h2 className="mb-2 text-lg font-semibold text-gray-900 dark:text-white">Vimshottari Dasha</h2>
      <p className="mb-3 text-sm text-gray-500 dark:text-gray-400">Shaded = the productive years (18–50).</p>
      <div className="flex overflow-hidden rounded-lg border border-gray-200 dark:border-gray-700 text-xs">
        {p.dasha.map((d, i) => {
          const hot = d.age_start < 50 && d.age_end > 18;
          const w = Math.max(d.age_end - d.age_start, 1);
          return (
            <div
              key={i}
              title={`${d.planet}: ages ${d.age_start}–${d.age_end} (${d.start.slice(0, 4)}–${d.end.slice(0, 4)})`}
              style={{ flex: w }}
              className={`border-r border-white/60 py-2 text-center ${
                hot ? "bg-primary-100 dark:bg-primary-900/40 font-bold text-primary-700 dark:text-primary-300" : "bg-gray-50 dark:bg-white/5 text-gray-500"
              }`}
            >
              {ABBR[d.planet] ?? d.planet.slice(0, 2)}
              <div className="text-[9px] text-gray-400">{d.age_start}</div>
            </div>
          );
        })}
      </div>

      <p className="mt-8 text-xs text-gray-400">
        Lahiri ayanamsha · Whole-Sign houses · Swiss Ephemeris. Part of the control set for chart-analysis
        research — a chart shows potential, not destiny.
      </p>
    </Container>
  );
}
