"use client";

import { useEffect, useState } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { availabilityApi, type Availability } from "@/lib/api";

interface BookingCalendarProps {
  onDateSelect: (date: string) => void;
  selectedDate: string;
}

export function BookingCalendar({ onDateSelect, selectedDate }: BookingCalendarProps) {
  const [currentMonth, setCurrentMonth] = useState(new Date());
  const [availability, setAvailability] = useState<Availability[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchAvailability = async () => {
      setLoading(true);
      const year = currentMonth.getFullYear();
      const month = currentMonth.getMonth();
      const start = `${year}-${String(month + 1).padStart(2, "0")}-01`;
      const lastDay = new Date(year, month + 1, 0).getDate();
      const end = `${year}-${String(month + 1).padStart(2, "0")}-${String(lastDay).padStart(2, "0")}`;

      try {
        const data = await availabilityApi.getRange(start, end);
        setAvailability(data);
      } catch {
        setAvailability([]);
      } finally {
        setLoading(false);
      }
    };

    fetchAvailability();
  }, [currentMonth]);

  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const year = currentMonth.getFullYear();
  const month = currentMonth.getMonth();
  const firstDayOfMonth = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  const availableDates = new Set(
    availability
      .filter((a) => !a.is_holiday && a.slots.some((s) => !s.booked))
      .map((a) => a.date)
  );

  const prevMonth = () => setCurrentMonth(new Date(year, month - 1, 1));
  const nextMonth = () => setCurrentMonth(new Date(year, month + 1, 1));

  const days = [];
  // Empty cells before first day
  for (let i = 0; i < firstDayOfMonth; i++) {
    days.push(<div key={`empty-${i}`} />);
  }

  for (let day = 1; day <= daysInMonth; day++) {
    const dateStr = `${year}-${String(month + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
    const date = new Date(year, month, day);
    const isPast = date < today;
    const isAvailable = availableDates.has(dateStr);
    const isSelected = dateStr === selectedDate;

    days.push(
      <button
        key={day}
        onClick={() => isAvailable && !isPast && onDateSelect(dateStr)}
        disabled={isPast || !isAvailable}
        className={`
          flex h-10 w-10 items-center justify-center rounded-lg text-sm font-medium transition-colors
          ${isSelected ? "bg-primary-600 text-white" : ""}
          ${!isSelected && isAvailable && !isPast ? "bg-green-50 text-green-700 hover:bg-green-100" : ""}
          ${isPast || !isAvailable ? "text-gray-300 cursor-not-allowed" : "cursor-pointer"}
        `}
      >
        {day}
      </button>
    );
  }

  const monthName = currentMonth.toLocaleString("en-US", { month: "long", year: "numeric" });

  return (
    <div className="rounded-xl border border-gray-200 bg-white p-4 sm:p-6">
      <div className="mb-4 flex items-center justify-between">
        <button onClick={prevMonth} className="rounded-lg p-2 hover:bg-gray-100">
          <ChevronLeft className="h-5 w-5" />
        </button>
        <h3 className="font-heading text-lg font-semibold">{monthName}</h3>
        <button onClick={nextMonth} className="rounded-lg p-2 hover:bg-gray-100">
          <ChevronRight className="h-5 w-5" />
        </button>
      </div>

      <div className="mb-2 grid grid-cols-7 text-center text-xs font-medium text-gray-500">
        {["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].map((d) => (
          <div key={d} className="py-1">{d}</div>
        ))}
      </div>

      <div className="grid grid-cols-7 place-items-center gap-y-1">
        {loading
          ? Array.from({ length: 35 }, (_, i) => (
              <div key={i} className="h-10 w-10 animate-pulse rounded-lg bg-gray-100" />
            ))
          : days}
      </div>

      <div className="mt-4 flex items-center gap-4 text-xs text-gray-500">
        <span className="flex items-center gap-1">
          <span className="inline-block h-3 w-3 rounded bg-green-50 border border-green-200" /> Available
        </span>
        <span className="flex items-center gap-1">
          <span className="inline-block h-3 w-3 rounded bg-gray-100" /> Unavailable
        </span>
      </div>
    </div>
  );
}
