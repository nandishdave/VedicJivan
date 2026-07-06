"use client";

import { useState } from "react";
import Link from "next/link";
import { Star } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { indexLetter } from "@/lib/chart-people";
import { celebritiesIndex as celebrities } from "@/lib/list-index";

const LETTERS = Array.from({ length: 26 }, (_, i) => String.fromCharCode(65 + i));

export default function CelebritiesPage() {
  const available = new Set(celebrities.map((c) => indexLetter(c.name)));
  const [letter, setLetter] = useState<string | null>(null);
  const list = letter ? celebrities.filter((c) => indexLetter(c.name) === letter) : celebrities;

  return (
    <Container className="py-12">
      <div className="mb-8 text-center">
        <h1 className="mb-2 text-3xl font-bold text-gray-900 dark:text-white">Celebrity Charts</h1>
        <p className="mx-auto max-w-2xl text-gray-600 dark:text-gray-400">
          Explore the Vedic birth charts (D1, D9, D10, D60) and Dasha timelines of famous figures — all from
          highly-reliable (AA birth-certificate or A family-record) birth times. Browse by the first letter of
          the surname.
        </p>
      </div>

      {/* A–Z bar */}
      <div
        className="mb-8 flex flex-wrap justify-center gap-1.5"
        role="group"
        aria-label="Filter by first letter of surname"
      >
        <button
          onClick={() => setLetter(null)}
          aria-pressed={letter === null}
          className={`rounded-md px-3 py-1.5 text-sm font-semibold focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 ${
            letter === null ? "bg-primary-600 text-white" : "bg-gray-100 dark:bg-white/10 text-gray-700 dark:text-gray-300"
          }`}
        >
          All
        </button>
        {LETTERS.map((l) => {
          const on = available.has(l);
          return (
            <button
              key={l}
              disabled={!on}
              onClick={() => setLetter(l)}
              aria-pressed={letter === l}
              aria-label={`Filter by surnames starting with ${l}`}
              className={`h-8 w-8 rounded-md text-sm font-semibold focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 ${
                letter === l
                  ? "bg-primary-600 text-white"
                  : on
                  ? "bg-gray-100 dark:bg-white/10 text-gray-700 dark:text-gray-300 hover:bg-primary-100 dark:hover:bg-primary-900/40"
                  : "cursor-not-allowed bg-gray-50 dark:bg-white/5 text-gray-300 dark:text-gray-600"
              }`}
            >
              {l}
            </button>
          );
        })}
      </div>

      {/* List */}
      <div className="mx-auto grid max-w-4xl gap-3 sm:grid-cols-2">
        {list.map((c) => (
          <Link
            key={c.slug}
            href={`/celebrities/${c.slug}`}
            className="flex items-center gap-3 rounded-xl border border-gray-200 dark:border-gray-700 bg-white dark:bg-white/5 p-4 transition-colors hover:border-primary-400"
          >
            <div className="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-full bg-primary-100 dark:bg-primary-900/30">
              <Star className="h-5 w-5 text-primary-600" />
            </div>
            <div className="min-w-0">
              <div className="truncate font-semibold text-gray-900 dark:text-white">{c.name}</div>
              <div className="truncate text-sm text-gray-500 dark:text-gray-400">
                {c.category} &middot; {c.lagna} Lagna
              </div>
            </div>
          </Link>
        ))}
      </div>
    </Container>
  );
}
