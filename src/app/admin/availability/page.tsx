"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, CalendarOff, Clock, Trash2, Plus } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { Button } from "@/components/ui/Button";
import { availabilityApi, type Unavailability } from "@/lib/api";
import { getToken } from "@/lib/auth";

export default function AvailabilityPage() {
  const router = useRouter();

  // Form state
  const [mode, setMode] = useState<"time-block" | "holiday">("time-block");
  const [date, setDate] = useState("");
  const [startTime, setStartTime] = useState("00:00");
  const [endTime, setEndTime] = useState("10:00");
  const [reason, setReason] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  // View existing blocks
  const [viewStart, setViewStart] = useState("");
  const [viewEnd, setViewEnd] = useState("");
  const [blocks, setBlocks] = useState<Unavailability[]>([]);
  const [viewLoading, setViewLoading] = useState(false);

  // Initialize view range to current month
  useEffect(() => {
    const now = new Date();
    const year = now.getFullYear();
    const month = now.getMonth();
    const start = `${year}-${String(month + 1).padStart(2, "0")}-01`;
    const lastDay = new Date(year, month + 1, 0).getDate();
    const end = `${year}-${String(month + 1).padStart(2, "0")}-${String(lastDay).padStart(2, "0")}`;
    setViewStart(start);
    setViewEnd(end);
  }, []);

  const fetchBlocks = useCallback(async () => {
    if (!viewStart || !viewEnd) return;
    setViewLoading(true);
    try {
      const data = await availabilityApi.getUnavailableRange(viewStart, viewEnd);
      setBlocks(data);
    } catch {
      setBlocks([]);
    } finally {
      setViewLoading(false);
    }
  }, [viewStart, viewEnd]);

  useEffect(() => {
    fetchBlocks();
  }, [fetchBlocks]);

  const handleAdd = async () => {
    const token = getToken();
    if (!token) { router.push("/admin/login"); return; }

    if (!date) {
      setMessage("Please select a date");
      return;
    }

    setLoading(true);
    setMessage("");
    try {
      if (mode === "holiday") {
        await availabilityApi.addUnavailable(
          { date, is_holiday: true, reason },
          token
        );
        setMessage(`${date} marked as holiday`);
      } else {
        await availabilityApi.addUnavailable(
          { date, start_time: startTime, end_time: endTime, reason },
          token
        );
        setMessage(`Blocked ${startTime} - ${endTime} on ${date}`);
      }
      setDate("");
      setReason("");
      fetchBlocks();
    } catch (err) {
      setMessage(err instanceof Error ? err.message : "Failed");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    const token = getToken();
    if (!token) { router.push("/admin/login"); return; }

    try {
      await availabilityApi.removeUnavailable(id, token);
      setBlocks(blocks.filter((b) => b.id !== id));
    } catch (err) {
      setMessage(err instanceof Error ? err.message : "Failed to remove");
    }
  };

  return (
    <section className="min-h-screen bg-gray-50 py-[var(--space-lg)]">
      <Container>
        <div className="mb-[var(--space-md)] flex items-center gap-[var(--space-sm)]">
          <Link href="/admin" className="rounded-lg p-2 hover:bg-gray-200">
            <ArrowLeft className="h-5 w-5" />
          </Link>
          <h1 className="font-heading text-[var(--text-xl)] font-bold">Manage Availability</h1>
        </div>

        <p className="mb-[var(--space-md)] text-[var(--text-sm)] text-gray-500">
          You are available 24/7 by default. Use this page to mark specific dates or time periods as unavailable.
        </p>

        {message && (
          <div className="mb-[var(--space-sm)] rounded-lg bg-green-50 border border-green-200 p-[var(--space-sm)] text-[var(--text-sm)] text-green-700">
            {message}
          </div>
        )}

        {/* Add unavailability form */}
        <div className="mb-[var(--space-lg)] rounded-xl border border-gray-200 bg-white p-[var(--space-md)]">
          <h2 className="mb-[var(--space-sm)] font-heading text-[var(--text-lg)] font-semibold flex items-center gap-2">
            <Plus className="h-5 w-5" />
            Block Time
          </h2>

          {/* Mode toggle */}
          <div className="mb-[var(--space-md)] flex flex-wrap gap-[var(--space-xs)]">
            <button
              onClick={() => setMode("time-block")}
              className={`rounded-full px-4 py-1.5 text-[var(--text-sm)] font-medium ${
                mode === "time-block" ? "bg-primary-600 text-white" : "bg-white text-gray-600 border"
              }`}
            >
              <Clock className="mr-1 inline h-3.5 w-3.5" />
              Time Block
            </button>
            <button
              onClick={() => setMode("holiday")}
              className={`rounded-full px-4 py-1.5 text-[var(--text-sm)] font-medium ${
                mode === "holiday" ? "bg-red-600 text-white" : "bg-white text-gray-600 border"
              }`}
            >
              <CalendarOff className="mr-1 inline h-3.5 w-3.5" />
              Full Day Holiday
            </button>
          </div>

          <div className="grid gap-[var(--space-sm)] sm:grid-cols-2">
            <div>
              <label className="mb-1 block text-[var(--text-sm)] font-medium">Date</label>
              <input
                type="date"
                value={date}
                onChange={(e) => setDate(e.target.value)}
                className="w-full rounded-lg border border-gray-300 px-[var(--space-sm)] py-2.5"
              />
            </div>

            {mode === "time-block" && (
              <>
                <div>
                  <label className="mb-1 block text-[var(--text-sm)] font-medium">Reason (optional)</label>
                  <input
                    type="text"
                    value={reason}
                    onChange={(e) => setReason(e.target.value)}
                    placeholder="e.g. Personal, Meeting"
                    className="w-full rounded-lg border border-gray-300 px-[var(--space-sm)] py-2.5"
                  />
                </div>
                <div>
                  <label className="mb-1 block text-[var(--text-sm)] font-medium">From</label>
                  <input
                    type="time"
                    value={startTime}
                    onChange={(e) => setStartTime(e.target.value)}
                    className="w-full rounded-lg border border-gray-300 px-[var(--space-sm)] py-2.5"
                  />
                </div>
                <div>
                  <label className="mb-1 block text-[var(--text-sm)] font-medium">To</label>
                  <input
                    type="time"
                    value={endTime}
                    onChange={(e) => setEndTime(e.target.value)}
                    className="w-full rounded-lg border border-gray-300 px-[var(--space-sm)] py-2.5"
                  />
                </div>
              </>
            )}

            {mode === "holiday" && (
              <div>
                <label className="mb-1 block text-[var(--text-sm)] font-medium">Reason (optional)</label>
                <input
                  type="text"
                  value={reason}
                  onChange={(e) => setReason(e.target.value)}
                  placeholder="e.g. Diwali, Personal day"
                  className="w-full rounded-lg border border-gray-300 px-[var(--space-sm)] py-2.5"
                />
              </div>
            )}
          </div>

          <div className="mt-[var(--space-md)]">
            <Button
              variant="primary"
              onClick={handleAdd}
              disabled={loading || !date}
            >
              {loading
                ? "Saving..."
                : mode === "holiday"
                  ? "Mark as Holiday"
                  : "Block Time Period"}
            </Button>
          </div>
        </div>

        {/* View existing blocks */}
        <div className="rounded-xl border border-gray-200 bg-white p-[var(--space-md)]">
          <h2 className="mb-[var(--space-sm)] font-heading text-[var(--text-lg)] font-semibold">Blocked Periods</h2>

          <div className="mb-[var(--space-sm)] flex flex-wrap items-center gap-[var(--space-sm)]">
            <div>
              <label className="mb-1 block text-xs text-gray-500">From</label>
              <input
                type="date"
                value={viewStart}
                onChange={(e) => setViewStart(e.target.value)}
                className="w-full rounded-lg border border-gray-300 px-[var(--space-sm)] py-2 text-[var(--text-sm)]"
              />
            </div>
            <div>
              <label className="mb-1 block text-xs text-gray-500">To</label>
              <input
                type="date"
                value={viewEnd}
                onChange={(e) => setViewEnd(e.target.value)}
                className="w-full rounded-lg border border-gray-300 px-[var(--space-sm)] py-2 text-[var(--text-sm)]"
              />
            </div>
          </div>

          {viewLoading ? (
            <div className="space-y-[var(--space-sm)]">
              {[1, 2, 3].map((i) => (
                <div key={i} className="h-14 animate-pulse rounded-lg bg-gray-100" />
              ))}
            </div>
          ) : blocks.length === 0 ? (
            <p className="py-[var(--space-lg)] text-center text-[var(--text-sm)] text-gray-400">
              No blocked periods in this range. You are fully available!
            </p>
          ) : (
            <div className="space-y-[var(--space-xs)]">
              {blocks.map((block) => (
                <div
                  key={block.id}
                  className={`flex items-center justify-between rounded-lg border p-[var(--space-sm)] ${
                    block.is_holiday
                      ? "border-red-200 bg-red-50"
                      : "border-orange-200 bg-orange-50"
                  }`}
                >
                  <div>
                    <span className="font-medium text-[var(--text-sm)]">{block.date}</span>
                    {block.is_holiday ? (
                      <span className="ml-2 rounded-full bg-red-100 px-2 py-0.5 text-xs font-medium text-red-700">
                        Holiday
                      </span>
                    ) : (
                      <span className="ml-2 text-[var(--text-sm)] text-gray-600">
                        {block.start_time} - {block.end_time}
                      </span>
                    )}
                    {block.reason && (
                      <span className="ml-2 text-xs text-gray-500">({block.reason})</span>
                    )}
                  </div>
                  <button
                    onClick={() => handleDelete(block.id)}
                    className="rounded-lg p-2 text-gray-400 hover:bg-white hover:text-red-600"
                    title="Remove block (make available again)"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </Container>
    </section>
  );
}
