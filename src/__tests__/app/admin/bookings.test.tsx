import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor, cleanup } from "@testing-library/react";
import BookingsPage from "@/app/admin/bookings/page";

const { mockPush, mockGetToken, mockClearTokens, mockList, mockUpdateStatus } = vi.hoisted(() => ({
  mockPush: vi.fn(),
  mockGetToken: vi.fn(),
  mockClearTokens: vi.fn(),
  mockList: vi.fn(),
  mockUpdateStatus: vi.fn(),
}));

vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: mockPush,
    replace: vi.fn(),
    back: vi.fn(),
    prefetch: vi.fn(),
  }),
  usePathname: () => "/admin/bookings",
}));

vi.mock("@/lib/api", () => ({
  bookingsApi: {
    list: mockList,
    updateStatus: mockUpdateStatus,
  },
}));

vi.mock("@/lib/auth", () => ({
  getToken: mockGetToken,
  clearTokens: mockClearTokens,
}));

vi.mock("@/components/ui/Container", () => ({
  Container: (props: { children: React.ReactNode }) =>
    <div>{props.children}</div>,
}));

vi.mock("@/components/ui/Button", () => ({
  Button: (props: { children: React.ReactNode; onClick?: () => void; variant?: string; size?: string; className?: string }) =>
    <button onClick={props.onClick} className={props.className}>{props.children}</button>,
}));

import React from "react";

const mockBookings = [
  {
    id: "b1",
    user_name: "John Doe",
    user_email: "john@test.com",
    service_title: "Call Consultation",
    date: "2026-03-15",
    time_slot: "10:00",
    duration_minutes: 30,
    price_inr: 1999,
    status: "pending",
  },
  {
    id: "b2",
    user_name: "Jane Smith",
    user_email: "jane@test.com",
    service_title: "Video Consultation",
    date: "2026-03-16",
    time_slot: "14:00",
    duration_minutes: 45,
    price_inr: 2999,
    status: "confirmed",
  },
];

describe("BookingsPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    cleanup();
  });

  it("redirects to login when no token", async () => {
    mockGetToken.mockReturnValue(null);
    render(<BookingsPage />);
    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith("/admin/login");
    });
  });

  it("renders bookings table with data", async () => {
    mockGetToken.mockReturnValue("admin-token");
    mockList.mockResolvedValue(mockBookings);
    render(<BookingsPage />);
    await waitFor(() => {
      expect(screen.getAllByText("John Doe").length).toBeGreaterThanOrEqual(1);
      expect(screen.getAllByText("Jane Smith").length).toBeGreaterThanOrEqual(1);
      expect(screen.getAllByText("Call Consultation").length).toBeGreaterThanOrEqual(1);
    });
  });

  it("shows loading skeleton initially", () => {
    mockGetToken.mockReturnValue("admin-token");
    mockList.mockReturnValue(new Promise(() => {}));
    render(<BookingsPage />);
    const pulseElements = document.querySelectorAll(".animate-pulse");
    expect(pulseElements.length).toBeGreaterThan(0);
  });

  it("shows empty state when no bookings", async () => {
    mockGetToken.mockReturnValue("admin-token");
    mockList.mockResolvedValue([]);
    render(<BookingsPage />);
    await waitFor(() => {
      expect(screen.getAllByText("No bookings found").length).toBeGreaterThanOrEqual(1);
    });
  });

  it("renders filter buttons", async () => {
    mockGetToken.mockReturnValue("admin-token");
    mockList.mockResolvedValue(mockBookings);
    render(<BookingsPage />);
    await waitFor(() => {
      expect(screen.getAllByText("All").length).toBeGreaterThanOrEqual(1);
      expect(screen.getAllByText("pending").length).toBeGreaterThanOrEqual(1);
      expect(screen.getAllByText("confirmed").length).toBeGreaterThanOrEqual(1);
    });
  });

  it("clears tokens on API error", async () => {
    mockGetToken.mockReturnValue("bad-token");
    mockList.mockRejectedValue(new Error("Unauthorized"));
    render(<BookingsPage />);
    await waitFor(() => {
      expect(mockClearTokens).toHaveBeenCalled();
      expect(mockPush).toHaveBeenCalledWith("/admin/login");
    });
  });

  it("shows Confirm button for pending bookings", async () => {
    mockGetToken.mockReturnValue("admin-token");
    mockList.mockResolvedValue([mockBookings[0]]);
    render(<BookingsPage />);
    await waitFor(() => {
      expect(screen.getAllByText("Confirm").length).toBeGreaterThanOrEqual(1);
    });
  });

  it("shows Complete button for confirmed bookings", async () => {
    mockGetToken.mockReturnValue("admin-token");
    mockList.mockResolvedValue([mockBookings[1]]);
    render(<BookingsPage />);
    await waitFor(() => {
      expect(screen.getAllByText("Complete").length).toBeGreaterThanOrEqual(1);
    });
  });

  it("calls updateStatus on Confirm click", async () => {
    mockGetToken.mockReturnValue("admin-token");
    mockList.mockResolvedValue([mockBookings[0]]);
    mockUpdateStatus.mockResolvedValue({ ...mockBookings[0], status: "confirmed" });
    render(<BookingsPage />);

    await waitFor(() => {
      expect(screen.getAllByText("Confirm").length).toBeGreaterThanOrEqual(1);
    });
    fireEvent.click(screen.getAllByText("Confirm")[0]);

    await waitFor(() => {
      expect(mockUpdateStatus).toHaveBeenCalledWith("b1", "confirmed", "admin-token");
    });
  });

  it("renders page heading", async () => {
    mockGetToken.mockReturnValue("admin-token");
    mockList.mockResolvedValue([]);
    render(<BookingsPage />);
    await waitFor(() => {
      expect(screen.getAllByText("Manage Bookings").length).toBeGreaterThanOrEqual(1);
    });
  });

  it("clicking filter re-fetches bookings", async () => {
    mockGetToken.mockReturnValue("admin-token");
    mockList.mockResolvedValue(mockBookings);
    render(<BookingsPage />);

    await waitFor(() => {
      expect(screen.getAllByText("pending").length).toBeGreaterThanOrEqual(1);
    });

    // Click the "pending" filter
    const filterButtons = screen.getAllByRole("button");
    const pendingFilter = filterButtons.find(b => b.textContent === "pending");
    if (pendingFilter) {
      fireEvent.click(pendingFilter);
      await waitFor(() => {
        // list should be called at least twice (initial + filter)
        expect(mockList.mock.calls.length).toBeGreaterThanOrEqual(2);
      });
    }
  });

  it("shows Cancel button for pending bookings", async () => {
    mockGetToken.mockReturnValue("admin-token");
    mockList.mockResolvedValue([mockBookings[0]]);
    render(<BookingsPage />);
    await waitFor(() => {
      expect(screen.getAllByText("Cancel").length).toBeGreaterThanOrEqual(1);
    });
  });
});
