"use client";

import { useEffect, useState } from "react";
import { Clock } from "lucide-react";
import { availabilityApi, type AvailableSlot } from "@/lib/api";

interface TimeSlotPickerProps {
  date: string;
  onSlotSelect: (slot: string) => void;
  onSlotsLoaded?: (slots: AvailableSlot[]) => void;
  selectedSlot: string;
}

export function TimeSlotPicker({ date, onSlotSelect, onSlotsLoaded, selectedSlot }: TimeSlotPickerProps) {
  const [slots, setSlots] = useState<AvailableSlot[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!date) return;

    const fetchSlots = async () => {
      setLoading(true);
      try {
        const data = await availabilityApi.getSlots(date);

        // Filter out past slots if the selected date is today
        const today = new Date().toISOString().split("T")[0];
        let filtered = data;
        if (date === today) {
          const now = new Date();
          const nowMinutes = now.getHours() * 60 + now.getMinutes();
          filtered = data.filter((slot) => {
            const [h, m] = slot.start.split(":").map(Number);
            return h * 60 + m > nowMinutes;
          });
        }

        setSlots(filtered);
        onSlotsLoaded?.(filtered);
      } catch {
        setSlots([]);
        onSlotsLoaded?.([]);
      } finally {
        setLoading(false);
      }
    };

    fetchSlots();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [date]);

  if (loading) {
    return (
      <div className="grid grid-cols-3 gap-3 sm:grid-cols-4">
        {Array.from({ length: 8 }, (_, i) => (
          <div key={i} className="h-12 animate-pulse rounded-lg bg-gray-100 dark:bg-gray-800" />
        ))}
      </div>
    );
  }

  if (slots.length === 0) {
    return (
      <p className="text-center text-sm text-gray-500 dark:text-gray-400 py-8">
        No available slots for this date. Please select another date.
      </p>
    );
  }

  return (
    <div className="grid grid-cols-3 gap-3 sm:grid-cols-4">
      {slots.map((slot) => (
        <button
          key={slot.start}
          onClick={() => onSlotSelect(slot.start)}
          className={`
            flex items-center justify-center gap-2 rounded-lg border-2 px-3 py-3 text-sm font-medium transition-colors
            ${
              selectedSlot === slot.start
                ? "border-primary-600 bg-primary-50 dark:bg-primary-900/20 text-primary-700"
                : "border-gray-200 dark:border-gray-600 hover:border-primary-300 dark:hover:border-primary-600 hover:bg-primary-50 dark:hover:bg-primary-900/20 dark:text-gray-300"
            }
          `}
        >
          <Clock className="h-4 w-4" />
          {slot.start}
        </button>
      ))}
    </div>
  );
}
