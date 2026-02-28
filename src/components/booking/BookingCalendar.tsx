"use client";

import { useEffect, useState } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { availabilityApi } from "@/lib/api";

interface BookingCalendarProps {
  onDateSelect: (date: string) => void;
  selectedDate: string;
}

export function BookingCalendar({ onDateSelect, selectedDate }: BookingCalendarProps) {
  const [currentMonth, setCurrentMonth] = useState(new Date());
  const [holidays, setHolidays] = useState<Set<string>>(new Set());
  const [closedDays, setClosedDays] = useState<Set<number>>(new Set());
  const [loading, setLoading] = useState(false);
  const [todayFullyBooked, setTodayFullyBooked] = useState(false);

  // Fetch closed days from business hours settings (once)
  useEffect(() => {
    availabilityApi
      .getSettings()
      .then((settings) => {
        const closed = new Set(
          settings.weekly_hours
            .filter((d) => !d.is_open)
            .map((d) => (d.day + 1) % 7) // Convert Mon=0 to JS Sun=0 convention
        );
        setClosedDays(closed);
      })
      .catch(() => {});
  }, []);

  // Check whether today still has any future slots (once on mount)
  useEffect(() => {
    const todayStr = new Date().toISOString().split("T")[0];
    availabilityApi
      .getSlots(todayStr)
      .then((slots) => {
        const now = new Date();
        const nowMinutes = now.getHours() * 60 + now.getMinutes();
        const hasFutureSlot = slots.some((slot) => {
          const [h, m] = slot.start.split(":").map(Number);
          return h * 60 + m > nowMinutes;
        });
        setTodayFullyBooked(!hasFutureSlot);
      })
      .catch(() => {});
  }, []);

  useEffect(() => {
    const fetchHolidays = async () => {
      setLoading(true);
      const year = currentMonth.getFullYear();
      const month = currentMonth.getMonth();
      const start = `${year}-${String(month + 1).padStart(2, "0")}-01`;
      const lastDay = new Date(year, month + 1, 0).getDate();
      const end = `${year}-${String(month + 1).padStart(2, "0")}-${String(lastDay).padStart(2, "0")}`;

      try {
        const data = await availabilityApi.getHolidays(start, end);
        setHolidays(new Set(data));
      } catch {
        setHolidays(new Set());
      } finally {
        setLoading(false);
      }
    };

    fetchHolidays();
  }, [currentMonth]);

  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const year = currentMonth.getFullYear();
  const month = currentMonth.getMonth();
  const firstDayOfMonth = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  const prevMonth = () => setCurrentMonth(new Date(year, month - 1, 1));
  const nextMonth = () => setCurrentMonth(new Date(year, month + 1, 1));

  const days = [];
  for (let i = 0; i < firstDayOfMonth; i++) {
    days.push(<div key={`empty-${i}`} />);
  }

  for (let day = 1; day <= daysInMonth; day++) {
    const dateStr = `${year}-${String(month + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
    const date = new Date(year, month, day);
    const isPast = date < today;
    const isToday = date.getTime() === today.getTime();
    const isHoliday = holidays.has(dateStr);
    const isClosed = closedDays.has(date.getDay());
    const isAvailable = !isPast && !isHoliday && !isClosed && !(isToday && todayFullyBooked);
    const isSelected = dateStr === selectedDate;

    days.push(
      <button
        key={day}
        onClick={() => isAvailable && onDateSelect(dateStr)}
        disabled={!isAvailable}
        className={`
          flex h-10 w-10 items-center justify-center rounded-lg text-sm font-medium transition-colors
          ${isSelected ? "bg-primary-600 text-white" : ""}
          ${!isSelected && isAvailable ? "bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400 hover:bg-green-100 dark:hover:bg-green-900/30" : ""}
          ${isHoliday && !isPast ? "bg-red-50 dark:bg-red-900/20 text-red-400 cursor-not-allowed" : ""}
          ${isClosed && !isPast && !isHoliday ? "text-gray-400 cursor-not-allowed" : ""}
          ${isPast ? "text-gray-300 dark:text-gray-600 cursor-not-allowed" : ""}
        `}
      >
        {day}
      </button>
    );
  }

  const monthName = currentMonth.toLocaleString("en-US", { month: "long", year: "numeric" });

  return (
    <div className="rounded-xl border border-gray-200 dark:border-gray-600 bg-white dark:bg-dark-surface-card p-4 sm:p-6">
      <div className="mb-4 flex items-center justify-between">
        <button onClick={prevMonth} className="rounded-lg p-2 hover:bg-gray-100 dark:hover:bg-white/10">
          <ChevronLeft className="h-5 w-5 dark:text-gray-300" />
        </button>
        <h3 className="font-heading text-lg font-semibold dark:text-gray-100">{monthName}</h3>
        <button onClick={nextMonth} className="rounded-lg p-2 hover:bg-gray-100 dark:hover:bg-white/10">
          <ChevronRight className="h-5 w-5 dark:text-gray-300" />
        </button>
      </div>

      <div className="mb-2 grid grid-cols-7 text-center text-xs font-medium text-gray-500 dark:text-gray-400">
        {["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].map((d) => (
          <div key={d} className="py-1">{d}</div>
        ))}
      </div>

      <div className="grid grid-cols-7 place-items-center gap-y-1">
        {loading
          ? Array.from({ length: 35 }, (_, i) => (
              <div key={i} className="h-10 w-10 animate-pulse rounded-lg bg-gray-100 dark:bg-gray-800" />
            ))
          : days}
      </div>

      <div className="mt-4 flex flex-wrap items-center gap-4 text-xs text-gray-500 dark:text-gray-400">
        <span className="flex items-center gap-1">
          <span className="inline-block h-3 w-3 rounded bg-green-50 dark:bg-green-900/20 border border-green-200" /> Available
        </span>
        <span className="flex items-center gap-1">
          <span className="inline-block h-3 w-3 rounded bg-red-50 dark:bg-red-900/20 border border-red-200" /> Holiday
        </span>
        <span className="flex items-center gap-1">
          <span className="inline-block h-3 w-3 rounded border border-gray-300 dark:border-gray-600" /> Closed
        </span>
        <span className="flex items-center gap-1">
          <span className="inline-block h-3 w-3 rounded bg-gray-100 dark:bg-gray-800" /> Past
        </span>
      </div>
    </div>
  );
}
