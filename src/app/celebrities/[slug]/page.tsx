import { notFound } from "next/navigation";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { NorthIndianChart } from "@/components/charts/NorthIndianChart";
import { celebrities, chartHouses, getCelebrity, ABBR } from "@/lib/celebrities";

export function generateStaticParams() {
  return celebrities.map((c) => ({ slug: c.slug }));
}

export function generateMetadata({ params }: { params: { slug: string } }) {
  const c = getCelebrity(params.slug);
  return c
    ? { title: `${c.name} — Vedic Birth Chart | VedicJivan`, description: c.bio.slice(0, 155) }
    : { title: "Celebrity Chart | VedicJivan" };
}

const VARGAS: { key: "D1" | "D9" | "D10" | "D60"; label: string }[] = [
  { key: "D1", label: "D1 · Rāśi" },
  { key: "D9", label: "D9 · Navāṁśa" },
  { key: "D10", label: "D10 · Daśāṁśa" },
  { key: "D60", label: "D60 · Ṣaṣṭyāṁśa" },
];

export default function CelebrityPage({ params }: { params: { slug: string } }) {
  const c = getCelebrity(params.slug);
  if (!c) notFound();

  return (
    <Container className="py-10">
      <Link
        href="/celebrities"
        className="mb-6 inline-flex items-center gap-1 text-sm text-primary-600 hover:underline"
      >
        <ArrowLeft className="h-4 w-4" /> All celebrities
      </Link>

      <div className="mb-2 flex flex-wrap items-center gap-3">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">{c.name}</h1>
        <span className="rounded-md bg-primary-600 px-2 py-0.5 text-xs font-semibold text-white">
          {c.rating}-rated
        </span>
      </div>
      <p className="mb-1 text-gray-600 dark:text-gray-400">{c.category}</p>
      <p className="mb-6 text-sm text-gray-500 dark:text-gray-500">
        {c.birth.date} · {c.birth.time} · {c.birth.place} &nbsp;|&nbsp; <strong>{c.lagna}</strong> Lagna
        (lord {c.lagna_lord}) · {c.nakshatra} nakshatra
      </p>

      <p className="mb-8 max-w-3xl leading-relaxed text-gray-700 dark:text-gray-300">{c.bio}</p>

      {/* Charts */}
      <div className="mb-10 grid gap-6 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-white/5 p-6 sm:grid-cols-2 lg:grid-cols-4">
        {VARGAS.map((v) => (
          <NorthIndianChart key={v.key} title={v.label} data={chartHouses(c, v.key)} />
        ))}
      </div>

      {/* Dasha timeline */}
      <h2 className="mb-2 text-lg font-semibold text-gray-900 dark:text-white">Vimshottari Dasha</h2>
      <p className="mb-3 text-sm text-gray-500 dark:text-gray-400">
        Shaded = the productive years (18–50), when a chart&apos;s potential most tends to manifest.
      </p>
      <div className="flex overflow-hidden rounded-lg border border-gray-200 dark:border-gray-700 text-xs">
        {c.dasha.map((d, i) => {
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
        Lahiri ayanamsha · Whole-Sign houses · Swiss Ephemeris. Birth time AA-rated (birth certificate /
        official record). For study &amp; interest — a chart shows potential, not destiny.
      </p>
    </Container>
  );
}
