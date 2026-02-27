import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor, cleanup } from "@testing-library/react";
import { PendingBookingBanner } from "@/components/booking/PendingBookingBanner";

const mockPathname = vi.fn();
vi.mock("next/navigation", () => ({
  usePathname: () => mockPathname(),
}));

// Mock next/link as a simple anchor
vi.mock("next/link", () => ({
  default: ({ href, children, ...props }: { href: string; children: React.ReactNode }) => (
    <a href={href} {...props}>{children}</a>
  ),
}));

describe("PendingBookingBanner", () => {
  beforeEach(() => {
    cleanup();
    vi.clearAllMocks();
    localStorage.clear();
    mockPathname.mockReturnValue("/");
  });

  it("renders nothing when no pending booking in localStorage", () => {
    const { container } = render(<PendingBookingBanner />);
    expect(container.innerHTML).toBe("");
  });

  it("shows banner with Continue Booking button for partial progress", async () => {
    localStorage.setItem(
      "vedicjivan_pending_booking_call-consultation",
      JSON.stringify({
        serviceSlug: "call-consultation",
        serviceTitle: "Call Consultation",
        date: "2026-03-20",
        timeSlot: "10:00",
        savedAt: new Date().toISOString(),
      })
    );

    render(<PendingBookingBanner />);

    await waitFor(() => {
      expect(screen.getByText(/unfinished/i)).toBeInTheDocument();
      expect(screen.getByText(/Call Consultation/)).toBeInTheDocument();
    });

    const link = screen.getByText(/Continue Booking/i);
    expect(link).toBeInTheDocument();
    expect(link.closest("a")).toHaveAttribute("href", "/book/call-consultation");
  });

  it("shows banner with Complete Payment button for pending-payment booking", async () => {
    localStorage.setItem(
      "vedicjivan_pending_booking_call-consultation",
      JSON.stringify({
        serviceSlug: "call-consultation",
        serviceTitle: "Call Consultation",
        bookingId: "booking-123",
        createdAt: new Date().toISOString(),
      })
    );

    render(<PendingBookingBanner />);

    await waitFor(() => {
      expect(screen.getByText(/waiting/i)).toBeInTheDocument();
      expect(screen.getByText(/Call Consultation/)).toBeInTheDocument();
      expect(screen.getByText(/Expires in/i)).toBeInTheDocument();
    });

    const link = screen.getByText(/Complete Payment/i);
    expect(link).toBeInTheDocument();
    expect(link.closest("a")).toHaveAttribute("href", "/book/call-consultation");
  });

  it("hides banner on /book/* pages", () => {
    mockPathname.mockReturnValue("/book/call-consultation");

    localStorage.setItem(
      "vedicjivan_pending_booking_call-consultation",
      JSON.stringify({
        serviceSlug: "call-consultation",
        serviceTitle: "Call Consultation",
        date: "2026-03-20",
        timeSlot: "10:00",
        savedAt: new Date().toISOString(),
      })
    );

    const { container } = render(<PendingBookingBanner />);
    expect(container.innerHTML).toBe("");
  });

  it("dismisses banner when X is clicked", async () => {
    localStorage.setItem(
      "vedicjivan_pending_booking_call-consultation",
      JSON.stringify({
        serviceSlug: "call-consultation",
        serviceTitle: "Call Consultation",
        date: "2026-03-20",
        timeSlot: "10:00",
        savedAt: new Date().toISOString(),
      })
    );

    render(<PendingBookingBanner />);

    await waitFor(() => {
      expect(screen.getByText(/unfinished/i)).toBeInTheDocument();
    });

    const dismissBtn = screen.getByLabelText("Dismiss");
    fireEvent.click(dismissBtn);

    expect(screen.queryByText(/unfinished/i)).not.toBeInTheDocument();
  });

  it("removes expired pending-payment booking from localStorage", async () => {
    // Booking created 16 minutes ago — expired
    const expiredTime = new Date(Date.now() - 16 * 60 * 1000).toISOString();
    localStorage.setItem(
      "vedicjivan_pending_booking_call-consultation",
      JSON.stringify({
        serviceSlug: "call-consultation",
        serviceTitle: "Call Consultation",
        bookingId: "booking-expired",
        createdAt: expiredTime,
      })
    );

    const { container } = render(<PendingBookingBanner />);

    // Banner should not render for expired booking
    expect(container.innerHTML).toBe("");

    // localStorage entry should be cleaned up
    expect(localStorage.getItem("vedicjivan_pending_booking_call-consultation")).toBeNull();
  });

  it("removes expired partial progress from localStorage after 2 hours", () => {
    // Partial progress saved 3 hours ago — expired
    const expiredTime = new Date(Date.now() - 3 * 60 * 60 * 1000).toISOString();
    localStorage.setItem(
      "vedicjivan_pending_booking_call-consultation",
      JSON.stringify({
        serviceSlug: "call-consultation",
        serviceTitle: "Call Consultation",
        date: "2026-03-20",
        timeSlot: "10:00",
        savedAt: expiredTime,
      })
    );

    const { container } = render(<PendingBookingBanner />);

    // Banner should not render for expired partial progress
    expect(container.innerHTML).toBe("");

    // localStorage entry should be cleaned up
    expect(localStorage.getItem("vedicjivan_pending_booking_call-consultation")).toBeNull();
  });
});
