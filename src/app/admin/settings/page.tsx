"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, Settings, Globe, FileText, Lock, Unlock } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { Button } from "@/components/ui/Button";
import { availabilityApi, type DayHours, type ReportSection } from "@/lib/api";
import { getToken } from "@/lib/auth";

const DAY_LABELS = [
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday",
  "Sunday",
];

const TIMEZONE_OPTIONS = [
  "Asia/Kolkata",
  "America/New_York",
  "America/Chicago",
  "America/Denver",
  "America/Los_Angeles",
  "Europe/London",
  "Europe/Berlin",
  "Europe/Paris",
  "Asia/Dubai",
  "Asia/Singapore",
  "Asia/Tokyo",
  "Australia/Sydney",
  "Pacific/Auckland",
];

export default function SettingsPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [savingReportSections, setSavingReportSections] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [reportSectionsMessage, setReportSectionsMessage] = useState("");
  const [reportSectionsError, setReportSectionsError] = useState("");
  const [timezone, setTimezone] = useState("Asia/Kolkata");
  const [weeklyHours, setWeeklyHours] = useState<DayHours[]>(
    Array.from({ length: 7 }, (_, i) => ({
      day: i,
      is_open: i < 6,
      open_time: "10:00",
      close_time: "18:00",
    }))
  );
  const [reportSections, setReportSections] = useState<ReportSection[]>([]);

  useEffect(() => {
    Promise.all([
      availabilityApi.getSettings().catch(() => null),
      availabilityApi.getReportSections().catch(() => null),
    ]).then(([hoursData, sectionsData]) => {
      if (hoursData) {
        setTimezone(hoursData.timezone);
        setWeeklyHours(hoursData.weekly_hours);
      }
      if (sectionsData) {
        setReportSections(sectionsData);
      }
    }).finally(() => setLoading(false));
  }, []);

  const handleSave = async () => {
    const token = getToken();
    if (!token) {
      router.push("/admin/login");
      return;
    }

    setSaving(true);
    setMessage("");
    setError("");
    try {
      await availabilityApi.updateSettings(
        { timezone, weekly_hours: weeklyHours },
        token
      );
      setMessage("Business hours updated successfully!");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save settings");
    } finally {
      setSaving(false);
    }
  };

  const handleSaveReportSections = async () => {
    const token = getToken();
    if (!token) { router.push("/admin/login"); return; }
    setSavingReportSections(true);
    setReportSectionsMessage("");
    setReportSectionsError("");
    try {
      await availabilityApi.updateReportSections(reportSections, token);
      setReportSectionsMessage("Report sections updated successfully!");
    } catch (err) {
      setReportSectionsError(err instanceof Error ? err.message : "Failed to save");
    } finally {
      setSavingReportSections(false);
    }
  };

  const updateSection = (id: string, updates: Partial<ReportSection>) => {
    setReportSections((prev) =>
      prev.map((s) => (s.id === id ? { ...s, ...updates } : s))
    );
  };

  const updateDay = (dayIndex: number, updates: Partial<DayHours>) => {
    setWeeklyHours((prev) =>
      prev.map((d) => (d.day === dayIndex ? { ...d, ...updates } : d))
    );
  };

  if (loading) {
    return (
      <section className="min-h-screen bg-gray-50 dark:bg-dark-surface py-8">
        <Container>
          <div className="animate-pulse space-y-6">
            <div className="h-8 w-48 rounded bg-gray-200 dark:bg-gray-700" />
            <div className="h-64 rounded-xl bg-gray-200 dark:bg-gray-700" />
          </div>
        </Container>
      </section>
    );
  }

  return (
    <section className="min-h-screen bg-gray-50 dark:bg-dark-surface py-[var(--space-lg)]">
      <Container>
        {/* Header */}
        <div className="mb-[var(--space-md)]">
          <Link
            href="/admin"
            className="mb-2 inline-flex items-center gap-1 text-[var(--text-sm)] text-gray-500 hover:text-gray-700 dark:hover:text-gray-300"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to Dashboard
          </Link>
          <div className="flex items-center gap-[var(--space-sm)]">
            <Settings className="h-6 w-6 text-primary-600 dark:text-primary-400" />
            <h1 className="font-heading text-[var(--text-xl)] font-bold">
              Business Hours Settings
            </h1>
          </div>
        </div>

        {/* Messages */}
        {message && (
          <div className="mb-[var(--space-sm)] rounded-lg border border-green-200 dark:border-green-800 bg-green-50 dark:bg-green-900/20 p-[var(--space-sm)] text-[var(--text-sm)] text-green-700 dark:text-green-400">
            {message}
          </div>
        )}
        {error && (
          <div className="mb-[var(--space-sm)] rounded-lg border border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-900/20 p-[var(--space-sm)] text-[var(--text-sm)] text-red-700 dark:text-red-400">
            {error}
          </div>
        )}

        {/* Timezone */}
        <div className="mb-[var(--space-md)] rounded-xl border border-gray-200 dark:border-gray-600 bg-white dark:bg-dark-surface-card p-[var(--space-md)]">
          <h2 className="mb-[var(--space-sm)] flex items-center gap-2 font-heading text-[var(--text-lg)] font-semibold">
            <Globe className="h-5 w-5 text-gray-500" />
            Timezone
          </h2>
          <select
            value={timezone}
            onChange={(e) => setTimezone(e.target.value)}
            className="w-full max-w-xs rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-dark-surface-raised px-[var(--space-sm)] py-2 text-[var(--text-sm)] text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
          >
            {TIMEZONE_OPTIONS.map((tz) => (
              <option key={tz} value={tz}>
                {tz}
              </option>
            ))}
          </select>
        </div>

        {/* Weekly Hours */}
        <div className="mb-[var(--space-md)] rounded-xl border border-gray-200 dark:border-gray-600 bg-white dark:bg-dark-surface-card p-[var(--space-md)]">
          <h2 className="mb-[var(--space-sm)] font-heading text-[var(--text-lg)] font-semibold">
            Weekly Schedule
          </h2>
          <div className="space-y-[var(--space-xs)]">
            {weeklyHours.map((day) => (
              <div
                key={day.day}
                className={`rounded-lg border p-[var(--space-sm)] ${
                  day.is_open
                    ? "border-green-200 dark:border-green-800 bg-green-50 dark:bg-green-900/20"
                    : "border-gray-200 dark:border-gray-600 bg-gray-50 dark:bg-dark-surface"
                }`}
              >
                <div className="flex items-center gap-[var(--space-sm)]">
                  {/* Day name */}
                  <span className="min-w-[5rem] text-[var(--text-sm)] font-medium text-gray-700 dark:text-gray-300">
                    {DAY_LABELS[day.day]}
                  </span>

                  {/* Open/Closed toggle */}
                  <button
                    type="button"
                    onClick={() =>
                      updateDay(day.day, { is_open: !day.is_open })
                    }
                    className={`rounded-full px-3 py-1 text-xs font-medium transition-colors ${
                      day.is_open
                        ? "bg-green-600 text-white"
                        : "bg-gray-300 dark:bg-gray-600 text-gray-600 dark:text-gray-300"
                    }`}
                  >
                    {day.is_open ? "Open" : "Closed"}
                  </button>

                  {/* Time inputs — inline on desktop */}
                  {day.is_open && (
                    <div className="hidden items-center gap-2 sm:flex">
                      <input
                        type="time"
                        value={day.open_time}
                        onChange={(e) =>
                          updateDay(day.day, { open_time: e.target.value })
                        }
                        className="rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-dark-surface-raised px-2 py-1 text-[var(--text-sm)] text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:outline-none"
                      />
                      <span className="text-[var(--text-sm)] text-gray-500">to</span>
                      <input
                        type="time"
                        value={day.close_time}
                        onChange={(e) =>
                          updateDay(day.day, { close_time: e.target.value })
                        }
                        className="rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-dark-surface-raised px-2 py-1 text-[var(--text-sm)] text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:outline-none"
                      />
                    </div>
                  )}
                </div>

                {/* Time inputs — stacked below on mobile */}
                {day.is_open && (
                  <div className="mt-2 flex items-center gap-2 sm:hidden">
                    <input
                      type="time"
                      value={day.open_time}
                      onChange={(e) =>
                        updateDay(day.day, { open_time: e.target.value })
                      }
                      className="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-dark-surface-raised px-2 py-1.5 text-[var(--text-sm)] text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:outline-none"
                    />
                    <span className="text-[var(--text-sm)] text-gray-500">to</span>
                    <input
                      type="time"
                      value={day.close_time}
                      onChange={(e) =>
                        updateDay(day.day, { close_time: e.target.value })
                      }
                      className="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-dark-surface-raised px-2 py-1.5 text-[var(--text-sm)] text-gray-900 dark:text-gray-100 focus:border-primary-500 focus:outline-none"
                    />
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Save button */}
        <Button onClick={handleSave} disabled={saving}>
          {saving ? "Saving..." : "Save Settings"}
        </Button>

        {/* ── Report Sections ── */}
        <div className="mt-[var(--space-xl)]">
          <div className="mb-[var(--space-md)] flex items-center gap-[var(--space-sm)]">
            <FileText className="h-6 w-6 text-primary-600 dark:text-primary-400" />
            <h1 className="font-heading text-[var(--text-xl)] font-bold">
              Report Sections
            </h1>
          </div>
          <p className="mb-[var(--space-md)] text-[var(--text-sm)] text-gray-500 dark:text-gray-400">
            Control which sections appear in the Kundli report and whether they require payment.
            Any new section added in the future will also appear here.
          </p>

          {reportSectionsMessage && (
            <div className="mb-[var(--space-sm)] rounded-lg border border-green-200 dark:border-green-800 bg-green-50 dark:bg-green-900/20 p-[var(--space-sm)] text-[var(--text-sm)] text-green-700 dark:text-green-400">
              {reportSectionsMessage}
            </div>
          )}
          {reportSectionsError && (
            <div className="mb-[var(--space-sm)] rounded-lg border border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-900/20 p-[var(--space-sm)] text-[var(--text-sm)] text-red-700 dark:text-red-400">
              {reportSectionsError}
            </div>
          )}

          <div className="mb-[var(--space-md)] rounded-xl border border-gray-200 dark:border-gray-600 bg-white dark:bg-dark-surface-card overflow-hidden">
            {/* Table header */}
            <div className="grid grid-cols-[1fr_auto_auto] gap-4 border-b border-gray-200 dark:border-gray-600 bg-gray-50 dark:bg-dark-surface px-[var(--space-md)] py-[var(--space-xs)]">
              <span className="text-xs font-semibold uppercase tracking-wide text-gray-500 dark:text-gray-400">Section</span>
              <span className="text-xs font-semibold uppercase tracking-wide text-gray-500 dark:text-gray-400 text-center">Access</span>
              <span className="text-xs font-semibold uppercase tracking-wide text-gray-500 dark:text-gray-400 text-center">Enabled</span>
            </div>

            {reportSections.map((section, idx) => (
              <div
                key={section.id}
                className={`grid grid-cols-[1fr_auto_auto] items-center gap-4 px-[var(--space-md)] py-[var(--space-sm)] ${
                  idx < reportSections.length - 1
                    ? "border-b border-gray-100 dark:border-gray-700"
                    : ""
                } ${!section.enabled ? "opacity-50" : ""}`}
              >
                {/* Section info */}
                <div>
                  <p className="text-[var(--text-sm)] font-medium text-gray-900 dark:text-gray-100">
                    {section.label}
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">
                    {section.description}
                  </p>
                </div>

                {/* Free / Paid toggle */}
                <button
                  type="button"
                  onClick={() => updateSection(section.id, { is_paid: !section.is_paid })}
                  className={`flex items-center gap-1.5 rounded-full px-3 py-1.5 text-xs font-medium transition-colors whitespace-nowrap ${
                    section.is_paid
                      ? "bg-amber-100 dark:bg-amber-900/30 text-amber-700 dark:text-amber-400 border border-amber-300 dark:border-amber-700"
                      : "bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 border border-green-300 dark:border-green-700"
                  }`}
                >
                  {section.is_paid ? (
                    <><Lock className="h-3 w-3" /> Paid</>
                  ) : (
                    <><Unlock className="h-3 w-3" /> Free</>
                  )}
                </button>

                {/* Enabled toggle */}
                <button
                  type="button"
                  onClick={() => updateSection(section.id, { enabled: !section.enabled })}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                    section.enabled ? "bg-primary-600" : "bg-gray-300 dark:bg-gray-600"
                  }`}
                  aria-label={`Toggle ${section.label}`}
                >
                  <span
                    className={`inline-block h-4 w-4 transform rounded-full bg-white shadow transition-transform ${
                      section.enabled ? "translate-x-6" : "translate-x-1"
                    }`}
                  />
                </button>
              </div>
            ))}
          </div>

          <Button onClick={handleSaveReportSections} disabled={savingReportSections}>
            {savingReportSections ? "Saving..." : "Save Report Sections"}
          </Button>
        </div>
      </Container>
    </section>
  );
}
