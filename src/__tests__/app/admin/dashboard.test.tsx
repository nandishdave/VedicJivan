import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor, cleanup } from "@testing-library/react";
import AdminDashboard from "@/app/admin/page";

const { mockPush, mockGetToken, mockClearTokens, mockAuthMe, mockDashboard } = vi.hoisted(() => ({
  mockPush: vi.fn(),
  mockGetToken: vi.fn(),
  mockClearTokens: vi.fn(),
  mockAuthMe: vi.fn(),
  mockDashboard: vi.fn(),
}));

vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: mockPush,
    replace: vi.fn(),
    back: vi.fn(),
    prefetch: vi.fn(),
  }),
  usePathname: () => "/admin",
}));

vi.mock("@/lib/api", () => ({
  adminApi: { dashboard: mockDashboard },
  authApi: { me: mockAuthMe },
}));

vi.mock("@/lib/auth", () => ({
  getToken: mockGetToken,
  clearTokens: mockClearTokens,
}));

const mockDashboardData = {
  today_bookings: 5,
  upcoming_bookings: 12,
  total_revenue: 45000,
  bookings_by_status: { pending: 3, confirmed: 7, completed: 10, cancelled: 2 },
  recent_bookings: [
    {
      id: "b1",
      user_name: "John Doe",
      service_title: "Call Consultation",
      date: "2026-03-15",
      time_slot: "10:00",
      status: "confirmed",
      price_inr: 1999,
    },
  ],
};

describe("AdminDashboard", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    cleanup();
  });

  it("redirects to login when no token", async () => {
    mockGetToken.mockReturnValue(null);
    render(<AdminDashboard />);
    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith("/admin/login");
    });
  });

  it("redirects to login when user is not admin", async () => {
    mockGetToken.mockReturnValue("token-123");
    mockAuthMe.mockResolvedValue({ name: "User", role: "user" });
    mockDashboard.mockResolvedValue(mockDashboardData);
    render(<AdminDashboard />);
    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith("/admin/login");
    });
  });

  it("renders dashboard data when authenticated as admin", async () => {
    mockGetToken.mockReturnValue("admin-token");
    mockAuthMe.mockResolvedValue({ name: "Admin User", role: "admin" });
    mockDashboard.mockResolvedValue(mockDashboardData);
    render(<AdminDashboard />);
    await waitFor(() => {
      expect(screen.getAllByText("Dashboard").length).toBeGreaterThanOrEqual(1);
      expect(screen.getByText("Welcome back, Admin User")).toBeInTheDocument();
    });
  });

  it("displays stats cards with correct data", async () => {
    mockGetToken.mockReturnValue("admin-token");
    mockAuthMe.mockResolvedValue({ name: "Admin", role: "admin" });
    mockDashboard.mockResolvedValue(mockDashboardData);
    render(<AdminDashboard />);
    await waitFor(() => {
      expect(screen.getByText("5")).toBeInTheDocument();
      expect(screen.getByText("12")).toBeInTheDocument();
      expect(screen.getByText("22")).toBeInTheDocument();
    });
  });

  it("displays recent bookings table", async () => {
    mockGetToken.mockReturnValue("admin-token");
    mockAuthMe.mockResolvedValue({ name: "Admin", role: "admin" });
    mockDashboard.mockResolvedValue(mockDashboardData);
    render(<AdminDashboard />);
    await waitFor(() => {
      expect(screen.getAllByText("Recent Bookings").length).toBeGreaterThanOrEqual(1);
      expect(screen.getAllByText("John Doe").length).toBeGreaterThanOrEqual(1);
    });
  });

  it("clears tokens and redirects on API error", async () => {
    mockGetToken.mockReturnValue("bad-token");
    mockAuthMe.mockRejectedValue(new Error("Unauthorized"));
    render(<AdminDashboard />);
    await waitFor(() => {
      expect(mockClearTokens).toHaveBeenCalled();
      expect(mockPush).toHaveBeenCalledWith("/admin/login");
    });
  });

  it("shows loading skeleton initially", () => {
    mockGetToken.mockReturnValue("token");
    mockAuthMe.mockReturnValue(new Promise(() => {}));
    mockDashboard.mockReturnValue(new Promise(() => {}));
    render(<AdminDashboard />);
    const pulseElements = document.querySelectorAll(".animate-pulse");
    expect(pulseElements.length).toBeGreaterThan(0);
  });
});
