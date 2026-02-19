import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor, cleanup } from "@testing-library/react";
import AvailabilityPage from "@/app/admin/availability/page";

const { mockPush, mockGetToken, mockGetUnavailableRange, mockAddUnavailable, mockRemoveUnavailable } = vi.hoisted(() => ({
  mockPush: vi.fn(),
  mockGetToken: vi.fn(),
  mockGetUnavailableRange: vi.fn(),
  mockAddUnavailable: vi.fn(),
  mockRemoveUnavailable: vi.fn(),
}));

vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: mockPush,
    replace: vi.fn(),
    back: vi.fn(),
    prefetch: vi.fn(),
  }),
  usePathname: () => "/admin/availability",
}));

vi.mock("@/lib/api", () => ({
  availabilityApi: {
    getUnavailableRange: mockGetUnavailableRange,
    addUnavailable: mockAddUnavailable,
    removeUnavailable: mockRemoveUnavailable,
  },
}));

vi.mock("@/lib/auth", () => ({
  getToken: mockGetToken,
}));

vi.mock("@/components/ui/Container", () => ({
  Container: (props: { children: React.ReactNode }) =>
    <div>{props.children}</div>,
}));

vi.mock("@/components/ui/Button", () => ({
  Button: (props: { children: React.ReactNode; onClick?: () => void; disabled?: boolean }) =>
    <button onClick={props.onClick} disabled={props.disabled}>{props.children}</button>,
}));

import React from "react";

describe("AvailabilityPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    cleanup();
    mockGetUnavailableRange.mockResolvedValue([]);
  });

  it("renders page heading", async () => {
    render(<AvailabilityPage />);
    await waitFor(() => {
      expect(screen.getAllByText("Manage Availability").length).toBeGreaterThanOrEqual(1);
    });
  });

  it("renders mode toggle buttons", async () => {
    render(<AvailabilityPage />);
    await waitFor(() => {
      expect(screen.getAllByText("Time Block").length).toBeGreaterThanOrEqual(1);
      expect(screen.getAllByText("Full Day Holiday").length).toBeGreaterThanOrEqual(1);
    });
  });

  it("shows empty state when no blocks", async () => {
    mockGetUnavailableRange.mockResolvedValue([]);
    render(<AvailabilityPage />);
    await waitFor(() => {
      expect(screen.getAllByText(/fully available/i).length).toBeGreaterThanOrEqual(1);
    });
  });

  it("renders existing unavailability blocks", async () => {
    mockGetUnavailableRange.mockResolvedValue([
      { id: "u1", date: "2026-03-01", is_holiday: true, reason: "Holi" },
      { id: "u2", date: "2026-03-05", is_holiday: false, start_time: "09:00", end_time: "12:00", reason: "Meeting" },
    ]);
    render(<AvailabilityPage />);
    await waitFor(() => {
      expect(screen.getAllByText("2026-03-01").length).toBeGreaterThanOrEqual(1);
      expect(screen.getAllByText("2026-03-05").length).toBeGreaterThanOrEqual(1);
      expect(screen.getAllByText("Holiday").length).toBeGreaterThanOrEqual(1);
    });
  });

  it("adds a holiday block", async () => {
    mockGetToken.mockReturnValue("admin-token");
    mockAddUnavailable.mockResolvedValue({});
    render(<AvailabilityPage />);

    // Switch to holiday mode
    await waitFor(() => {
      expect(screen.getAllByText("Full Day Holiday").length).toBeGreaterThanOrEqual(1);
    });
    fireEvent.click(screen.getAllByText("Full Day Holiday")[0]);

    // Set date
    const dateInput = document.querySelector('input[type="date"]') as HTMLInputElement;
    fireEvent.change(dateInput, { target: { value: "2026-04-01" } });

    // Click add button
    const addBtn = screen.getAllByText("Mark as Holiday")[0];
    fireEvent.click(addBtn);

    await waitFor(() => {
      expect(mockAddUnavailable).toHaveBeenCalledWith(
        { date: "2026-04-01", is_holiday: true, reason: "" },
        "admin-token"
      );
    });
  });

  it("redirects to login when no token on add", async () => {
    mockGetToken.mockReturnValue(null);
    render(<AvailabilityPage />);

    // Set date
    const dateInput = document.querySelector('input[type="date"]') as HTMLInputElement;
    fireEvent.change(dateInput, { target: { value: "2026-04-01" } });

    const addBtn = screen.getAllByText(/Block Time Period/i)[0];
    fireEvent.click(addBtn);

    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith("/admin/login");
    });
  });

  it("shows loading skeleton when fetching blocks", () => {
    mockGetUnavailableRange.mockReturnValue(new Promise(() => {}));
    render(<AvailabilityPage />);
    const pulseElements = document.querySelectorAll(".animate-pulse");
    expect(pulseElements.length).toBeGreaterThan(0);
  });

  it("handles delete block with confirmation dialog", async () => {
    mockGetToken.mockReturnValue("admin-token");
    mockRemoveUnavailable.mockResolvedValue({});
    mockGetUnavailableRange.mockResolvedValue([
      { id: "u1", date: "2026-03-01", is_holiday: true, reason: "Holi" },
    ]);
    render(<AvailabilityPage />);

    await waitFor(() => {
      expect(screen.getAllByText("2026-03-01").length).toBeGreaterThanOrEqual(1);
    });

    // Click delete button (the trash icon button) — opens confirmation dialog
    const deleteBtn = document.querySelector('button[title*="Remove"]') as HTMLButtonElement;
    fireEvent.click(deleteBtn);

    // Confirmation dialog should appear
    await waitFor(() => {
      expect(screen.getByText("Confirm Deletion")).toBeInTheDocument();
      expect(screen.getByText(/Are you sure/)).toBeInTheDocument();
    });

    // Click "Delete" in the confirmation dialog
    fireEvent.click(screen.getByText("Delete"));

    await waitFor(() => {
      expect(mockRemoveUnavailable).toHaveBeenCalledWith("u1", "admin-token");
    });
  });

  it("cancels delete when clicking Cancel in confirmation dialog", async () => {
    mockGetToken.mockReturnValue("admin-token");
    mockGetUnavailableRange.mockResolvedValue([
      { id: "u1", date: "2026-03-01", is_holiday: true, reason: "Holi" },
    ]);
    render(<AvailabilityPage />);

    await waitFor(() => {
      expect(screen.getAllByText("2026-03-01").length).toBeGreaterThanOrEqual(1);
    });

    // Click delete button — opens confirmation dialog
    const deleteBtn = document.querySelector('button[title*="Remove"]') as HTMLButtonElement;
    fireEvent.click(deleteBtn);

    await waitFor(() => {
      expect(screen.getByText("Confirm Deletion")).toBeInTheDocument();
    });

    // Click "Cancel" — dialog should close, no delete
    fireEvent.click(screen.getByText("Cancel"));

    await waitFor(() => {
      expect(screen.queryByText("Confirm Deletion")).not.toBeInTheDocument();
    });
    expect(mockRemoveUnavailable).not.toHaveBeenCalled();
  });

  it("adds a time block", async () => {
    mockGetToken.mockReturnValue("admin-token");
    mockAddUnavailable.mockResolvedValue({});
    render(<AvailabilityPage />);

    // Default mode is time-block
    const dateInput = document.querySelector('input[type="date"]') as HTMLInputElement;
    fireEvent.change(dateInput, { target: { value: "2026-04-01" } });

    // Set time inputs
    const timeInputs = document.querySelectorAll('input[type="time"]');
    if (timeInputs.length >= 2) {
      fireEvent.change(timeInputs[0], { target: { value: "09:00" } });
      fireEvent.change(timeInputs[1], { target: { value: "12:00" } });
    }

    const addBtn = screen.getAllByText(/Block Time Period/i)[0];
    fireEvent.click(addBtn);

    await waitFor(() => {
      expect(mockAddUnavailable).toHaveBeenCalledWith(
        expect.objectContaining({ date: "2026-04-01", start_time: "09:00", end_time: "12:00" }),
        "admin-token"
      );
    });
  });

  it("shows validation message when no date selected", async () => {
    mockGetToken.mockReturnValue("admin-token");
    render(<AvailabilityPage />);

    // Don't set date, just click add (button should be disabled when no date, but let's verify)
    const addBtn = screen.getAllByText(/Block Time Period/i)[0];
    // The button should be disabled when no date
    expect(addBtn.closest("button")?.disabled).toBe(true);
  });

  it("shows error message on API failure", async () => {
    mockGetToken.mockReturnValue("admin-token");
    mockAddUnavailable.mockRejectedValue(new Error("Server error"));
    render(<AvailabilityPage />);

    const dateInput = document.querySelector('input[type="date"]') as HTMLInputElement;
    fireEvent.change(dateInput, { target: { value: "2026-04-01" } });

    const addBtn = screen.getAllByText(/Block Time Period/i)[0];
    fireEvent.click(addBtn);

    await waitFor(() => {
      expect(screen.getAllByText("Server error").length).toBeGreaterThanOrEqual(1);
    });
  });

  it("shows reason inputs in both modes", async () => {
    render(<AvailabilityPage />);
    // Time block mode shows reason
    expect(screen.getAllByPlaceholderText(/Personal, Meeting/i).length).toBeGreaterThanOrEqual(1);

    // Switch to holiday mode
    fireEvent.click(screen.getAllByText("Full Day Holiday")[0]);
    await waitFor(() => {
      expect(screen.getAllByPlaceholderText(/Diwali/i).length).toBeGreaterThanOrEqual(1);
    });
  });
});
