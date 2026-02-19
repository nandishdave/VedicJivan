import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor, cleanup } from "@testing-library/react";
import { BookingCalendar } from "@/components/booking/BookingCalendar";

// Mock the API module
vi.mock("@/lib/api", () => ({
  availabilityApi: {
    getHolidays: vi.fn().mockResolvedValue([]),
    getSettings: vi.fn().mockResolvedValue({
      timezone: "Asia/Kolkata",
      weekly_hours: [
        { day: 0, is_open: true, open_time: "10:00", close_time: "18:00" },
        { day: 1, is_open: true, open_time: "10:00", close_time: "18:00" },
        { day: 2, is_open: true, open_time: "10:00", close_time: "18:00" },
        { day: 3, is_open: true, open_time: "10:00", close_time: "18:00" },
        { day: 4, is_open: true, open_time: "10:00", close_time: "18:00" },
        { day: 5, is_open: true, open_time: "10:00", close_time: "18:00" },
        { day: 6, is_open: false, open_time: "10:00", close_time: "18:00" },
      ],
    }),
  },
}));

import { availabilityApi } from "@/lib/api";

describe("BookingCalendar", () => {
  const mockOnDateSelect = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
    cleanup();
    (availabilityApi.getHolidays as ReturnType<typeof vi.fn>).mockResolvedValue([]);
  });

  it("renders day headers", async () => {
    render(<BookingCalendar selectedDate="" onDateSelect={mockOnDateSelect} />);
    await waitFor(() => {
      expect(screen.getAllByText("Sun").length).toBeGreaterThanOrEqual(1);
      expect(screen.getAllByText("Mon").length).toBeGreaterThanOrEqual(1);
      expect(screen.getAllByText("Sat").length).toBeGreaterThanOrEqual(1);
    });
  });

  it("renders month and year in header", async () => {
    render(<BookingCalendar selectedDate="" onDateSelect={mockOnDateSelect} />);
    await waitFor(() => {
      const now = new Date();
      const monthName = now.toLocaleString("en-US", { month: "long", year: "numeric" });
      expect(screen.getAllByText(monthName).length).toBeGreaterThanOrEqual(1);
    });
  });

  it("calls onDateSelect when a future date is clicked", async () => {
    render(<BookingCalendar selectedDate="" onDateSelect={mockOnDateSelect} />);

    await waitFor(() => {
      expect(screen.getAllByText("Sun").length).toBeGreaterThanOrEqual(1);
    });

    // Find a future date button
    const now = new Date();
    const lastDay = new Date(now.getFullYear(), now.getMonth() + 1, 0).getDate();
    const dayButtons = screen.getAllByText(String(lastDay));
    const clickable = dayButtons.find(btn => !btn.hasAttribute("disabled"));
    if (clickable) {
      fireEvent.click(clickable);
      expect(mockOnDateSelect).toHaveBeenCalled();
    }
  });

  it("renders navigation arrows", async () => {
    render(<BookingCalendar selectedDate="" onDateSelect={mockOnDateSelect} />);
    await waitFor(() => {
      const buttons = screen.getAllByRole("button");
      expect(buttons.length).toBeGreaterThanOrEqual(2);
    });
  });

  it("fetches holidays on mount", async () => {
    render(<BookingCalendar selectedDate="" onDateSelect={mockOnDateSelect} />);
    await waitFor(() => {
      expect(availabilityApi.getHolidays).toHaveBeenCalled();
    });
  });

  it("shows loading skeleton initially", () => {
    (availabilityApi.getHolidays as ReturnType<typeof vi.fn>).mockReturnValue(
      new Promise(() => {})
    );
    render(<BookingCalendar selectedDate="" onDateSelect={mockOnDateSelect} />);
    const pulseElements = document.querySelectorAll(".animate-pulse");
    expect(pulseElements.length).toBeGreaterThan(0);
  });

  it("renders legend items", async () => {
    render(<BookingCalendar selectedDate="" onDateSelect={mockOnDateSelect} />);
    await waitFor(() => {
      expect(screen.getAllByText("Available").length).toBeGreaterThanOrEqual(1);
      expect(screen.getAllByText("Holiday").length).toBeGreaterThanOrEqual(1);
      expect(screen.getAllByText("Closed").length).toBeGreaterThanOrEqual(1);
      expect(screen.getAllByText("Past").length).toBeGreaterThanOrEqual(1);
    });
  });

  it("handles API error gracefully", async () => {
    (availabilityApi.getHolidays as ReturnType<typeof vi.fn>).mockRejectedValue(
      new Error("fail")
    );
    render(<BookingCalendar selectedDate="" onDateSelect={mockOnDateSelect} />);
    await waitFor(() => {
      expect(screen.getAllByText("Available").length).toBeGreaterThanOrEqual(1);
    });
  });
});
