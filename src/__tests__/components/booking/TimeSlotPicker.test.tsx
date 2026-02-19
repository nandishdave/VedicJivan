import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor, cleanup } from "@testing-library/react";
import { TimeSlotPicker } from "@/components/booking/TimeSlotPicker";

const { mockGetSlots } = vi.hoisted(() => ({
  mockGetSlots: vi.fn(),
}));

vi.mock("@/lib/api", () => ({
  availabilityApi: {
    getSlots: mockGetSlots,
  },
}));

describe("TimeSlotPicker", () => {
  const mockOnSlotSelect = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
    cleanup();
    mockGetSlots.mockResolvedValue([]);
  });

  it("shows loading skeleton while fetching", () => {
    mockGetSlots.mockReturnValue(new Promise(() => {}));
    render(
      <TimeSlotPicker date="2026-03-15" onSlotSelect={mockOnSlotSelect} selectedSlot="" />
    );
    const pulseElements = document.querySelectorAll(".animate-pulse");
    expect(pulseElements.length).toBeGreaterThan(0);
  });

  it("shows empty message when no slots available", async () => {
    mockGetSlots.mockResolvedValue([]);
    render(
      <TimeSlotPicker date="2026-03-15" onSlotSelect={mockOnSlotSelect} selectedSlot="" />
    );
    await waitFor(() => {
      expect(screen.getByText(/no available slots/i)).toBeInTheDocument();
    });
  });

  it("renders slot buttons when slots are available", async () => {
    mockGetSlots.mockResolvedValue([
      { start: "09:00", end: "09:30" },
      { start: "10:00", end: "10:30" },
    ]);
    render(
      <TimeSlotPicker date="2026-03-15" onSlotSelect={mockOnSlotSelect} selectedSlot="" />
    );
    await waitFor(() => {
      expect(screen.getByText("09:00")).toBeInTheDocument();
      expect(screen.getByText("10:00")).toBeInTheDocument();
    });
  });

  it("calls onSlotSelect when a slot is clicked", async () => {
    mockGetSlots.mockResolvedValue([{ start: "14:00", end: "14:30" }]);
    render(
      <TimeSlotPicker date="2026-03-15" onSlotSelect={mockOnSlotSelect} selectedSlot="" />
    );
    await waitFor(() => {
      expect(screen.getByText("14:00")).toBeInTheDocument();
    });
    fireEvent.click(screen.getByText("14:00"));
    expect(mockOnSlotSelect).toHaveBeenCalledWith("14:00");
  });

  it("applies selected styling to selected slot", async () => {
    mockGetSlots.mockResolvedValue([
      { start: "09:00", end: "09:30" },
      { start: "10:00", end: "10:30" },
    ]);
    const { container } = render(
      <TimeSlotPicker date="2026-03-15" onSlotSelect={mockOnSlotSelect} selectedSlot="09:00" />
    );
    await waitFor(() => {
      expect(screen.getByText("09:00")).toBeInTheDocument();
    });
    const buttons = container.querySelectorAll("button");
    const hasSelectedClass = Array.from(buttons).some(btn =>
      btn.className.includes("border-primary-600")
    );
    expect(hasSelectedClass).toBe(true);
  });

  it("does not fetch when date is empty", () => {
    render(
      <TimeSlotPicker date="" onSlotSelect={mockOnSlotSelect} selectedSlot="" />
    );
    expect(mockGetSlots).not.toHaveBeenCalled();
  });

  it("shows empty state when API returns error", async () => {
    mockGetSlots.mockRejectedValue(new Error("fail"));
    render(
      <TimeSlotPicker date="2026-03-15" onSlotSelect={mockOnSlotSelect} selectedSlot="" />
    );
    await waitFor(() => {
      expect(screen.getByText(/no available slots/i)).toBeInTheDocument();
    });
  });
});
