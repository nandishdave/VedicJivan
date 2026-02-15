"use client";

import { useEffect, useState } from "react";
import { Clock } from "lucide-react";
import { availabilityApi, type TimeSlot } from "@/lib/api";

interface TimeSlotPickerProps {
  date: string;
  onSlotSelect: (slot: string) => void;
  selectedSlot: string;
}

export function TimeSlotPicker({ date, onSlotSelect, selectedSlot }: TimeSlotPickerProps) {
  const [slots, setSlots] = useState<TimeSlot[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!date) return;

    const fetchSlots = async () => {
      setLoading(true);
      try {
        const data = await availabilityApi.getByDate(date);
        setSlots(data?.slots || []);
      } catch {
        setSlots([]);
      } finally {
        setLoading(false);
      }
    };

    fetchSlots();
  }, [date]);

  if (loading) {
    return (
      <div className="grid grid-cols-3 gap-3 sm:grid-cols-4">
        {Array.from({ length: 8 }, (_, i) => (
          <div key={i} className="h-12 animate-pulse rounded-lg bg-gray-100" />
        ))}
      </div>
    );
  }

  const availableSlots = slots.filter((s) => !s.booked);

  if (availableSlots.length === 0) {
    return (
      <p className="text-center text-sm text-gray-500 py-8">
        No available slots for this date. Please select another date.
      </p>
    );
  }

  return (
    <div className="grid grid-cols-3 gap-3 sm:grid-cols-4">
      {availableSlots.map((slot) => (
        <button
          key={slot.start}
          onClick={() => onSlotSelect(slot.start)}
          className={`
            flex items-center justify-center gap-2 rounded-lg border-2 px-3 py-3 text-sm font-medium transition-colors
            ${
              selectedSlot === slot.start
                ? "border-primary-600 bg-primary-50 text-primary-700"
                : "border-gray-200 hover:border-primary-300 hover:bg-primary-50"
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
