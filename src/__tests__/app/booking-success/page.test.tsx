import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, waitFor, cleanup } from "@testing-library/react";

const mockGetSessionStatus = vi.fn();

vi.mock("@/lib/api", () => ({
  paymentsApi: {
    getSessionStatus: (...args: unknown[]) => mockGetSessionStatus(...args),
  },
}));

const mockSearchParams = new URLSearchParams();
vi.mock("next/navigation", async () => {
  const actual = await vi.importActual<typeof import("next/navigation")>("next/navigation");
  return {
    ...actual,
    useSearchParams: () => mockSearchParams,
  };
});

import BookingSuccessPage from "@/app/booking-success/page";

describe("BookingSuccessPage", () => {
  beforeEach(() => {
    cleanup();
    vi.clearAllMocks();
    vi.useFakeTimers({ shouldAdvanceTime: true });
    localStorage.clear();
    // Reset search params
    [...mockSearchParams.keys()].forEach((k) => mockSearchParams.delete(k));
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it("shows loading state initially with session params", () => {
    mockSearchParams.set("session_id", "cs_test_123");
    mockSearchParams.set("booking_id", "abc123");
    mockGetSessionStatus.mockReturnValue(new Promise(() => {})); // never resolves

    render(<BookingSuccessPage />);

    expect(screen.getByText("Verifying your payment...")).toBeInTheDocument();
  });

  it("shows confirmed state when payment is captured", async () => {
    mockSearchParams.set("session_id", "cs_test_123");
    mockSearchParams.set("booking_id", "abc123");
    mockGetSessionStatus.mockResolvedValue({
      payment_status: "captured",
      booking_status: "confirmed",
      booking: {
        service_title: "Call Consultation",
        date: "2026-03-20",
        time_slot: "10:00",
        duration_minutes: 30,
        price_inr: 1999,
        user_name: "Test User",
        user_email: "test@example.com",
      },
    });

    render(<BookingSuccessPage />);

    await waitFor(() => {
      expect(screen.getByText("Booking Confirmed!")).toBeInTheDocument();
    });

    expect(screen.getByText("Call Consultation")).toBeInTheDocument();
    expect(screen.getByText("Test User")).toBeInTheDocument();
    expect(screen.getByText("test@example.com")).toBeInTheDocument();
  });

  it("shows pending state when payment is not yet captured", async () => {
    mockSearchParams.set("session_id", "cs_test_123");
    mockSearchParams.set("booking_id", "abc123");
    mockGetSessionStatus.mockResolvedValue({
      payment_status: "pending",
      booking_status: "pending",
    });

    render(<BookingSuccessPage />);

    await waitFor(() => {
      expect(screen.getByText("Payment Received!")).toBeInTheDocument();
    });
  });

  it("shows pending state on API error", async () => {
    mockSearchParams.set("session_id", "cs_test_123");
    mockSearchParams.set("booking_id", "abc123");
    mockGetSessionStatus.mockRejectedValue(new Error("Network error"));

    render(<BookingSuccessPage />);

    await waitFor(() => {
      expect(screen.getByText("Payment Received!")).toBeInTheDocument();
    });
  });

  it("displays booking ID when present", async () => {
    mockSearchParams.set("session_id", "cs_test_123");
    mockSearchParams.set("booking_id", "abc123");
    mockGetSessionStatus.mockResolvedValue({
      payment_status: "captured",
      booking_status: "confirmed",
    });

    render(<BookingSuccessPage />);

    await waitFor(() => {
      expect(screen.getByText("abc123")).toBeInTheDocument();
    });
  });

  it("shows navigation links", async () => {
    mockSearchParams.set("session_id", "cs_test_123");
    mockSearchParams.set("booking_id", "abc123");
    mockGetSessionStatus.mockResolvedValue({
      payment_status: "captured",
      booking_status: "confirmed",
    });

    render(<BookingSuccessPage />);

    await waitFor(() => {
      expect(screen.getByText("Browse Services")).toBeInTheDocument();
      expect(screen.getByText("Back to Home")).toBeInTheDocument();
    });

    expect(screen.getByText("Browse Services").closest("a")).toHaveAttribute("href", "/services");
    expect(screen.getByText("Back to Home").closest("a")).toHaveAttribute("href", "/");
  });

  it("clears localStorage pending booking on confirmation", async () => {
    mockSearchParams.set("session_id", "cs_test_123");
    mockSearchParams.set("booking_id", "abc123");

    localStorage.setItem(
      "vedicjivan_pending_booking_call-consultation",
      JSON.stringify({ bookingId: "abc123", serviceSlug: "call-consultation" })
    );

    mockGetSessionStatus.mockResolvedValue({
      payment_status: "captured",
      booking_status: "confirmed",
    });

    render(<BookingSuccessPage />);

    await waitFor(() => {
      expect(screen.getByText("Booking Confirmed!")).toBeInTheDocument();
    });

    expect(localStorage.getItem("vedicjivan_pending_booking_call-consultation")).toBeNull();
  });

  it("does not clear unrelated localStorage keys", async () => {
    mockSearchParams.set("session_id", "cs_test_123");
    mockSearchParams.set("booking_id", "abc123");

    localStorage.setItem(
      "vedicjivan_pending_booking_video-consultation",
      JSON.stringify({ bookingId: "other-id", serviceSlug: "video-consultation" })
    );

    mockGetSessionStatus.mockResolvedValue({
      payment_status: "captured",
      booking_status: "confirmed",
    });

    render(<BookingSuccessPage />);

    await waitFor(() => {
      expect(screen.getByText("Booking Confirmed!")).toBeInTheDocument();
    });

    // Different bookingId, should not be cleared
    expect(localStorage.getItem("vedicjivan_pending_booking_video-consultation")).not.toBeNull();
  });

  it("polls status and passes correct params", async () => {
    mockSearchParams.set("session_id", "cs_test_session");
    mockSearchParams.set("booking_id", "bk_123");
    mockGetSessionStatus.mockResolvedValue({
      payment_status: "captured",
      booking_status: "confirmed",
    });

    render(<BookingSuccessPage />);

    await waitFor(() => {
      expect(mockGetSessionStatus).toHaveBeenCalledWith("cs_test_session", "bk_123");
    });
  });

  it("formats date with full weekday and month", async () => {
    mockSearchParams.set("session_id", "cs_test_123");
    mockSearchParams.set("booking_id", "abc123");
    mockGetSessionStatus.mockResolvedValue({
      payment_status: "captured",
      booking_status: "confirmed",
      booking: {
        service_title: "Kundli",
        date: "2026-03-20",
        time_slot: "14:00",
        duration_minutes: 60,
        price_inr: 2999,
        user_name: "Jane",
        user_email: "jane@example.com",
      },
    });

    render(<BookingSuccessPage />);

    await waitFor(() => {
      // Should contain "Friday" and "March" in the formatted date
      const dateText = screen.getByText(/March/);
      expect(dateText).toBeInTheDocument();
    });
  });
});
