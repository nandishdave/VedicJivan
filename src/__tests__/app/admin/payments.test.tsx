import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor, cleanup } from "@testing-library/react";
import PaymentsPage from "@/app/admin/payments/page";

const { mockPush, mockGetToken, mockClearTokens, mockPaymentsList } = vi.hoisted(() => ({
  mockPush: vi.fn(),
  mockGetToken: vi.fn(),
  mockClearTokens: vi.fn(),
  mockPaymentsList: vi.fn(),
}));

vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: mockPush,
    replace: vi.fn(),
    back: vi.fn(),
    prefetch: vi.fn(),
  }),
  usePathname: () => "/admin/payments",
}));

vi.mock("@/lib/api", () => ({
  paymentsApi: {
    list: mockPaymentsList,
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

import React from "react";

const mockPayments = [
  {
    id: "p1",
    booking_id: "b1",
    razorpay_order_id: "order_abc123",
    razorpay_payment_id: "pay_xyz789",
    amount_inr: 1999,
    currency: "INR",
    status: "captured",
    created_at: "2026-03-15T10:30:00Z",
  },
  {
    id: "p2",
    booking_id: "b2",
    razorpay_order_id: "order_def456",
    razorpay_payment_id: null,
    amount_inr: 2999,
    currency: "INR",
    status: "created",
    created_at: "2026-03-16T14:00:00Z",
  },
];

describe("PaymentsPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    cleanup();
  });

  it("redirects to login when no token", async () => {
    mockGetToken.mockReturnValue(null);
    render(<PaymentsPage />);
    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith("/admin/login");
    });
  });

  it("renders page heading", async () => {
    mockGetToken.mockReturnValue("admin-token");
    mockPaymentsList.mockResolvedValue([]);
    render(<PaymentsPage />);
    await waitFor(() => {
      expect(screen.getAllByText("Payment History").length).toBeGreaterThanOrEqual(1);
    });
  });

  it("shows loading skeleton initially", () => {
    mockGetToken.mockReturnValue("admin-token");
    mockPaymentsList.mockReturnValue(new Promise(() => {}));
    render(<PaymentsPage />);
    const pulseElements = document.querySelectorAll(".animate-pulse");
    expect(pulseElements.length).toBeGreaterThan(0);
  });

  it("renders payments table with data", async () => {
    mockGetToken.mockReturnValue("admin-token");
    mockPaymentsList.mockResolvedValue(mockPayments);
    render(<PaymentsPage />);
    await waitFor(() => {
      expect(screen.getAllByText("order_abc123").length).toBeGreaterThanOrEqual(1);
      expect(screen.getAllByText("pay_xyz789").length).toBeGreaterThanOrEqual(1);
      expect(screen.getAllByText("captured").length).toBeGreaterThanOrEqual(1);
    });
  });

  it("shows dash for missing payment ID", async () => {
    mockGetToken.mockReturnValue("admin-token");
    mockPaymentsList.mockResolvedValue([mockPayments[1]]);
    render(<PaymentsPage />);
    await waitFor(() => {
      expect(screen.getAllByText("-").length).toBeGreaterThanOrEqual(1);
    });
  });

  it("shows empty state when no payments", async () => {
    mockGetToken.mockReturnValue("admin-token");
    mockPaymentsList.mockResolvedValue([]);
    render(<PaymentsPage />);
    await waitFor(() => {
      expect(screen.getAllByText("No payments yet").length).toBeGreaterThanOrEqual(1);
    });
  });

  it("clears tokens on API error", async () => {
    mockGetToken.mockReturnValue("bad-token");
    mockPaymentsList.mockRejectedValue(new Error("Unauthorized"));
    render(<PaymentsPage />);
    await waitFor(() => {
      expect(mockClearTokens).toHaveBeenCalled();
      expect(mockPush).toHaveBeenCalledWith("/admin/login");
    });
  });

  it("renders table headers", async () => {
    mockGetToken.mockReturnValue("admin-token");
    mockPaymentsList.mockResolvedValue(mockPayments);
    render(<PaymentsPage />);
    await waitFor(() => {
      expect(screen.getAllByText("Order ID").length).toBeGreaterThanOrEqual(1);
      expect(screen.getAllByText("Payment ID").length).toBeGreaterThanOrEqual(1);
      expect(screen.getAllByText("Amount").length).toBeGreaterThanOrEqual(1);
      expect(screen.getAllByText("Status").length).toBeGreaterThanOrEqual(1);
    });
  });
});
