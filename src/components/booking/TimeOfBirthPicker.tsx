"use client";

interface TimeOfBirthPickerProps {
  value: { hour: string; minute: string; period: "AM" | "PM" } | null;
  isUnknown: boolean;
  onTimeChange: (time: { hour: string; minute: string; period: "AM" | "PM" }) => void;
  onUnknownChange: (unknown: boolean) => void;
}

const HOURS = Array.from({ length: 12 }, (_, i) => String(i + 1).padStart(2, "0"));
const MINUTES = Array.from({ length: 60 }, (_, i) => String(i).padStart(2, "0"));

export function TimeOfBirthPicker({
  value,
  isUnknown,
  onTimeChange,
  onUnknownChange,
}: TimeOfBirthPickerProps) {
  const hour = value?.hour || "12";
  const minute = value?.minute || "00";
  const period = value?.period || "AM";

  return (
    <div className="space-y-3">
      {/* Unknown checkbox */}
      <label className="flex items-center gap-2 cursor-pointer">
        <input
          type="checkbox"
          checked={isUnknown}
          onChange={(e) => onUnknownChange(e.target.checked)}
          className="h-4 w-4 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
        />
        <span className="text-sm text-gray-600">I don&apos;t know my exact birth time</span>
      </label>

      {/* Time selectors */}
      <div className={`flex items-center gap-2 ${isUnknown ? "opacity-40 pointer-events-none" : ""}`}>
        {/* Hour */}
        <select
          value={hour}
          onChange={(e) => onTimeChange({ hour: e.target.value, minute, period })}
          disabled={isUnknown}
          className="rounded-lg border border-gray-300 px-3 py-2.5 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
          aria-label="Hour"
        >
          {HOURS.map((h) => (
            <option key={h} value={h}>{h}</option>
          ))}
        </select>

        <span className="text-lg font-bold text-gray-400">:</span>

        {/* Minute */}
        <select
          value={minute}
          onChange={(e) => onTimeChange({ hour, minute: e.target.value, period })}
          disabled={isUnknown}
          className="rounded-lg border border-gray-300 px-3 py-2.5 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
          aria-label="Minute"
        >
          {MINUTES.map((m) => (
            <option key={m} value={m}>{m}</option>
          ))}
        </select>

        {/* AM/PM toggle */}
        <div className="flex rounded-lg border border-gray-300 overflow-hidden">
          <button
            type="button"
            onClick={() => onTimeChange({ hour, minute, period: "AM" })}
            disabled={isUnknown}
            className={`px-3 py-2.5 text-sm font-medium transition-colors ${
              period === "AM"
                ? "bg-primary-600 text-white"
                : "bg-white text-gray-700 hover:bg-gray-50"
            }`}
          >
            AM
          </button>
          <button
            type="button"
            onClick={() => onTimeChange({ hour, minute, period: "PM" })}
            disabled={isUnknown}
            className={`px-3 py-2.5 text-sm font-medium transition-colors ${
              period === "PM"
                ? "bg-primary-600 text-white"
                : "bg-white text-gray-700 hover:bg-gray-50"
            }`}
          >
            PM
          </button>
        </div>
      </div>
    </div>
  );
}
