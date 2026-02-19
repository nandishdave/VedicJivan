"use client";

import { useState } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";

interface DateOfBirthPickerProps {
  selectedDate: string;
  onDateSelect: (date: string) => void;
}

const MONTHS = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December",
];

export function DateOfBirthPicker({ selectedDate, onDateSelect }: DateOfBirthPickerProps) {
  const today = new Date();
  const currentYear = today.getFullYear();
  const minYear = currentYear - 100;

  const [currentMonth, setCurrentMonth] = useState(() => {
    if (selectedDate) {
      const [y, m] = selectedDate.split("-").map(Number);
      return new Date(y, m - 1, 1);
    }
    return new Date(currentYear, today.getMonth(), 1);
  });

  const year = currentMonth.getFullYear();
  const month = currentMonth.getMonth();
  const firstDayOfMonth = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  const prevMonth = () => {
    const prev = new Date(year, month - 1, 1);
    if (prev.getFullYear() >= minYear) setCurrentMonth(prev);
  };

  const nextMonth = () => {
    const next = new Date(year, month + 1, 1);
    if (next <= today) setCurrentMonth(next);
  };

  const handleYearChange = (newYear: number) => {
    const newDate = new Date(newYear, month, 1);
    if (newDate > today) {
      setCurrentMonth(new Date(newYear, today.getMonth(), 1));
    } else {
      setCurrentMonth(newDate);
    }
  };

  const handleMonthChange = (newMonth: number) => {
    const newDate = new Date(year, newMonth, 1);
    if (newDate > today) return;
    setCurrentMonth(newDate);
  };

  const years = [];
  for (let y = currentYear; y >= minYear; y--) {
    years.push(y);
  }

  const days = [];
  for (let i = 0; i < firstDayOfMonth; i++) {
    days.push(<div key={`empty-${i}`} />);
  }

  for (let day = 1; day <= daysInMonth; day++) {
    const dateStr = `${year}-${String(month + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
    const date = new Date(year, month, day);
    const isFuture = date > today;
    const isSelected = dateStr === selectedDate;

    days.push(
      <button
        key={day}
        type="button"
        onClick={() => !isFuture && onDateSelect(dateStr)}
        disabled={isFuture}
        className={`
          flex h-10 w-10 items-center justify-center rounded-lg text-sm font-medium transition-colors
          ${isSelected ? "bg-primary-600 text-white" : ""}
          ${!isSelected && !isFuture ? "bg-green-50 text-green-700 hover:bg-green-100" : ""}
          ${isFuture ? "text-gray-300 cursor-not-allowed" : ""}
        `}
      >
        {day}
      </button>
    );
  }

  return (
    <div className="rounded-xl border border-gray-200 bg-white p-4 sm:p-6">
      {/* Year and Month dropdowns */}
      <div className="mb-4 flex items-center justify-between gap-2">
        <button type="button" onClick={prevMonth} className="rounded-lg p-2 hover:bg-gray-100">
          <ChevronLeft className="h-5 w-5" />
        </button>

        <div className="flex items-center gap-2">
          <select
            value={month}
            onChange={(e) => handleMonthChange(Number(e.target.value))}
            className="rounded-lg border border-gray-300 px-2 py-1.5 text-sm font-semibold focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
          >
            {MONTHS.map((m, i) => (
              <option key={m} value={i}>{m}</option>
            ))}
          </select>

          <select
            value={year}
            onChange={(e) => handleYearChange(Number(e.target.value))}
            className="rounded-lg border border-gray-300 px-2 py-1.5 text-sm font-semibold focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
          >
            {years.map((y) => (
              <option key={y} value={y}>{y}</option>
            ))}
          </select>
        </div>

        <button type="button" onClick={nextMonth} className="rounded-lg p-2 hover:bg-gray-100">
          <ChevronRight className="h-5 w-5" />
        </button>
      </div>

      {/* Day-of-week header */}
      <div className="mb-2 grid grid-cols-7 text-center text-xs font-medium text-gray-500">
        {["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].map((d) => (
          <div key={d} className="py-1">{d}</div>
        ))}
      </div>

      {/* Calendar grid */}
      <div className="grid grid-cols-7 place-items-center gap-y-1">
        {days}
      </div>
    </div>
  );
}
