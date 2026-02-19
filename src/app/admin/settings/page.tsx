"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, Settings, Globe } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { Button } from "@/components/ui/Button";
import { availabilityApi, type DayHours } from "@/lib/api";
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
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [timezone, setTimezone] = useState("Asia/Kolkata");
  const [weeklyHours, setWeeklyHours] = useState<DayHours[]>(
    Array.from({ length: 7 }, (_, i) => ({
      day: i,
      is_open: i < 6,
      open_time: "10:00",
      close_time: "18:00",
    }))
  );

  useEffect(() => {
    availabilityApi
      .getSettings()
      .then((data) => {
        setTimezone(data.timezone);
        setWeeklyHours(data.weekly_hours);
      })
      .catch(() => {
        /* use defaults */
      })
      .finally(() => setLoading(false));
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

  const updateDay = (dayIndex: number, updates: Partial<DayHours>) => {
    setWeeklyHours((prev) =>
      prev.map((d) => (d.day === dayIndex ? { ...d, ...updates } : d))
    );
  };

  if (loading) {
    return (
      <section className="min-h-screen bg-gray-50 py-8">
        <Container>
          <div className="animate-pulse space-y-6">
            <div className="h-8 w-48 rounded bg-gray-200" />
            <div className="h-64 rounded-xl bg-gray-200" />
          </div>
        </Container>
      </section>
    );
  }

  return (
    <section className="min-h-screen bg-gray-50 py-[var(--space-lg)]">
      <Container>
        {/* Header */}
        <div className="mb-[var(--space-md)]">
          <Link
            href="/admin"
            className="mb-2 inline-flex items-center gap-1 text-[var(--text-sm)] text-gray-500 hover:text-gray-700"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to Dashboard
          </Link>
          <div className="flex items-center gap-[var(--space-sm)]">
            <Settings className="h-6 w-6 text-primary-600" />
            <h1 className="font-heading text-[var(--text-xl)] font-bold">
              Business Hours Settings
            </h1>
          </div>
        </div>

        {/* Messages */}
        {message && (
          <div className="mb-[var(--space-sm)] rounded-lg border border-green-200 bg-green-50 p-[var(--space-sm)] text-[var(--text-sm)] text-green-700">
            {message}
          </div>
        )}
        {error && (
          <div className="mb-[var(--space-sm)] rounded-lg border border-red-200 bg-red-50 p-[var(--space-sm)] text-[var(--text-sm)] text-red-700">
            {error}
          </div>
        )}

        {/* Timezone */}
        <div className="mb-[var(--space-md)] rounded-xl border border-gray-200 bg-white p-[var(--space-md)]">
          <h2 className="mb-[var(--space-sm)] flex items-center gap-2 font-heading text-[var(--text-lg)] font-semibold">
            <Globe className="h-5 w-5 text-gray-500" />
            Timezone
          </h2>
          <select
            value={timezone}
            onChange={(e) => setTimezone(e.target.value)}
            className="w-full max-w-xs rounded-lg border border-gray-300 px-[var(--space-sm)] py-2 text-[var(--text-sm)] focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
          >
            {TIMEZONE_OPTIONS.map((tz) => (
              <option key={tz} value={tz}>
                {tz}
              </option>
            ))}
          </select>
        </div>

        {/* Weekly Hours */}
        <div className="mb-[var(--space-md)] rounded-xl border border-gray-200 bg-white p-[var(--space-md)]">
          <h2 className="mb-[var(--space-sm)] font-heading text-[var(--text-lg)] font-semibold">
            Weekly Schedule
          </h2>
          <div className="space-y-[var(--space-xs)]">
            {weeklyHours.map((day) => (
              <div
                key={day.day}
                className={`rounded-lg border p-[var(--space-sm)] ${
                  day.is_open
                    ? "border-green-200 bg-green-50"
                    : "border-gray-200 bg-gray-50"
                }`}
              >
                <div className="flex items-center gap-[var(--space-sm)]">
                  {/* Day name */}
                  <span className="min-w-[5rem] text-[var(--text-sm)] font-medium text-gray-700">
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
                        : "bg-gray-300 text-gray-600"
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
                        className="rounded-lg border border-gray-300 px-2 py-1 text-[var(--text-sm)] focus:border-primary-500 focus:outline-none"
                      />
                      <span className="text-[var(--text-sm)] text-gray-500">to</span>
                      <input
                        type="time"
                        value={day.close_time}
                        onChange={(e) =>
                          updateDay(day.day, { close_time: e.target.value })
                        }
                        className="rounded-lg border border-gray-300 px-2 py-1 text-[var(--text-sm)] focus:border-primary-500 focus:outline-none"
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
                      className="w-full rounded-lg border border-gray-300 px-2 py-1.5 text-[var(--text-sm)] focus:border-primary-500 focus:outline-none"
                    />
                    <span className="text-[var(--text-sm)] text-gray-500">to</span>
                    <input
                      type="time"
                      value={day.close_time}
                      onChange={(e) =>
                        updateDay(day.day, { close_time: e.target.value })
                      }
                      className="w-full rounded-lg border border-gray-300 px-2 py-1.5 text-[var(--text-sm)] focus:border-primary-500 focus:outline-none"
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
      </Container>
    </section>
  );
}
