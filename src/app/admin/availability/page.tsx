"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { ArrowLeft, Plus, Trash2 } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { Button } from "@/components/ui/Button";
import { availabilityApi, type TimeSlot } from "@/lib/api";
import { getToken } from "@/lib/auth";

export default function AvailabilityPage() {
  const router = useRouter();
  const [mode, setMode] = useState<"single" | "bulk">("bulk");

  // Single day
  const [date, setDate] = useState("");
  const [slots, setSlots] = useState<TimeSlot[]>([
    { start: "10:00", end: "11:00", booked: false },
  ]);

  // Bulk
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [startTime, setStartTime] = useState("10:00");
  const [endTime, setEndTime] = useState("18:00");
  const [slotDuration, setSlotDuration] = useState(60);
  const [workingDays, setWorkingDays] = useState([0, 1, 2, 3, 4]); // Mon-Fri

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const addSlot = () => {
    const last = slots[slots.length - 1];
    setSlots([...slots, { start: last.end, end: last.end, booked: false }]);
  };

  const removeSlot = (index: number) => {
    setSlots(slots.filter((_, i) => i !== index));
  };

  const updateSlot = (index: number, field: "start" | "end", value: string) => {
    setSlots(slots.map((s, i) => (i === index ? { ...s, [field]: value } : s)));
  };

  const toggleDay = (day: number) => {
    setWorkingDays((prev) =>
      prev.includes(day) ? prev.filter((d) => d !== day) : [...prev, day].sort()
    );
  };

  const handleSingle = async () => {
    const token = getToken();
    if (!token) { router.push("/admin/login"); return; }

    setLoading(true);
    setMessage("");
    try {
      await availabilityApi.create({ date, slots, is_holiday: false }, token);
      setMessage(`Availability set for ${date}`);
    } catch (err) {
      setMessage(err instanceof Error ? err.message : "Failed");
    } finally {
      setLoading(false);
    }
  };

  const handleBulk = async () => {
    const token = getToken();
    if (!token) { router.push("/admin/login"); return; }

    setLoading(true);
    setMessage("");
    try {
      const result = await availabilityApi.createBulk(
        {
          start_date: startDate,
          end_date: endDate,
          working_days: workingDays,
          start_time: startTime,
          end_time: endTime,
          slot_duration_minutes: slotDuration,
        },
        token
      );
      setMessage(result.message);
    } catch (err) {
      setMessage(err instanceof Error ? err.message : "Failed");
    } finally {
      setLoading(false);
    }
  };

  const dayNames = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

  return (
    <section className="min-h-screen bg-gray-50 py-8">
      <Container>
        <div className="mb-6 flex items-center gap-3">
          <Link href="/admin" className="rounded-lg p-2 hover:bg-gray-200">
            <ArrowLeft className="h-5 w-5" />
          </Link>
          <h1 className="font-heading text-2xl font-bold">Set Availability</h1>
        </div>

        {/* Mode toggle */}
        <div className="mb-6 flex gap-2">
          <button
            onClick={() => setMode("bulk")}
            className={`rounded-full px-4 py-1.5 text-sm font-medium ${mode === "bulk" ? "bg-primary-600 text-white" : "bg-white text-gray-600"}`}
          >
            Bulk (Date Range)
          </button>
          <button
            onClick={() => setMode("single")}
            className={`rounded-full px-4 py-1.5 text-sm font-medium ${mode === "single" ? "bg-primary-600 text-white" : "bg-white text-gray-600"}`}
          >
            Single Day
          </button>
        </div>

        {message && (
          <div className="mb-4 rounded-lg bg-green-50 border border-green-200 p-3 text-sm text-green-700">
            {message}
          </div>
        )}

        <div className="rounded-xl border border-gray-200 bg-white p-6">
          {mode === "bulk" ? (
            <div className="space-y-5">
              <h2 className="font-heading text-lg font-semibold">Bulk Create Slots</h2>
              <div className="grid gap-4 sm:grid-cols-2">
                <div>
                  <label className="mb-1 block text-sm font-medium">Start Date</label>
                  <input
                    type="date"
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                    className="w-full rounded-lg border border-gray-300 px-4 py-2.5"
                  />
                </div>
                <div>
                  <label className="mb-1 block text-sm font-medium">End Date</label>
                  <input
                    type="date"
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                    className="w-full rounded-lg border border-gray-300 px-4 py-2.5"
                  />
                </div>
                <div>
                  <label className="mb-1 block text-sm font-medium">Start Time</label>
                  <input
                    type="time"
                    value={startTime}
                    onChange={(e) => setStartTime(e.target.value)}
                    className="w-full rounded-lg border border-gray-300 px-4 py-2.5"
                  />
                </div>
                <div>
                  <label className="mb-1 block text-sm font-medium">End Time</label>
                  <input
                    type="time"
                    value={endTime}
                    onChange={(e) => setEndTime(e.target.value)}
                    className="w-full rounded-lg border border-gray-300 px-4 py-2.5"
                  />
                </div>
              </div>
              <div>
                <label className="mb-1 block text-sm font-medium">Slot Duration</label>
                <select
                  value={slotDuration}
                  onChange={(e) => setSlotDuration(Number(e.target.value))}
                  className="rounded-lg border border-gray-300 px-4 py-2.5"
                >
                  <option value={30}>30 minutes</option>
                  <option value={45}>45 minutes</option>
                  <option value={60}>60 minutes</option>
                  <option value={90}>90 minutes</option>
                </select>
              </div>
              <div>
                <label className="mb-2 block text-sm font-medium">Working Days</label>
                <div className="flex gap-2">
                  {dayNames.map((name, i) => (
                    <button
                      key={name}
                      onClick={() => toggleDay(i)}
                      className={`rounded-lg px-3 py-1.5 text-sm font-medium ${
                        workingDays.includes(i)
                          ? "bg-primary-600 text-white"
                          : "bg-gray-100 text-gray-600"
                      }`}
                    >
                      {name}
                    </button>
                  ))}
                </div>
              </div>
              <Button
                variant="primary"
                onClick={handleBulk}
                disabled={loading || !startDate || !endDate}
              >
                {loading ? "Creating..." : "Create Availability"}
              </Button>
            </div>
          ) : (
            <div className="space-y-5">
              <h2 className="font-heading text-lg font-semibold">Single Day Slots</h2>
              <div>
                <label className="mb-1 block text-sm font-medium">Date</label>
                <input
                  type="date"
                  value={date}
                  onChange={(e) => setDate(e.target.value)}
                  className="rounded-lg border border-gray-300 px-4 py-2.5"
                />
              </div>
              <div className="space-y-2">
                <label className="block text-sm font-medium">Time Slots</label>
                {slots.map((slot, i) => (
                  <div key={i} className="flex items-center gap-2">
                    <input
                      type="time"
                      value={slot.start}
                      onChange={(e) => updateSlot(i, "start", e.target.value)}
                      className="rounded-lg border border-gray-300 px-3 py-2"
                    />
                    <span className="text-gray-400">to</span>
                    <input
                      type="time"
                      value={slot.end}
                      onChange={(e) => updateSlot(i, "end", e.target.value)}
                      className="rounded-lg border border-gray-300 px-3 py-2"
                    />
                    {slots.length > 1 && (
                      <button onClick={() => removeSlot(i)} className="text-red-400 hover:text-red-600">
                        <Trash2 className="h-4 w-4" />
                      </button>
                    )}
                  </div>
                ))}
                <button onClick={addSlot} className="flex items-center gap-1 text-sm text-primary-600 hover:text-primary-700">
                  <Plus className="h-4 w-4" /> Add Slot
                </button>
              </div>
              <Button
                variant="primary"
                onClick={handleSingle}
                disabled={loading || !date}
              >
                {loading ? "Saving..." : "Save Availability"}
              </Button>
            </div>
          )}
        </div>
      </Container>
    </section>
  );
}
