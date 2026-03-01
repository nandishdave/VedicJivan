import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, cleanup } from "@testing-library/react";

const mockSearchParams = new URLSearchParams();
vi.mock("next/navigation", async () => {
  const actual = await vi.importActual<typeof import("next/navigation")>("next/navigation");
  return {
    ...actual,
    useSearchParams: () => mockSearchParams,
  };
});

import BookingCancelledPage from "@/app/booking-cancelled/page";

describe("BookingCancelledPage", () => {
  beforeEach(() => {
    cleanup();
    [...mockSearchParams.keys()].forEach((k) => mockSearchParams.delete(k));
  });

  it("renders the cancellation message", () => {
    render(<BookingCancelledPage />);

    expect(screen.getByText("Payment Not Completed")).toBeInTheDocument();
    expect(screen.getByText(/Your payment was not completed/)).toBeInTheDocument();
    expect(screen.getByText(/reserved for 15 minutes/)).toBeInTheDocument();
  });

  it("shows booking ID when present in URL params", () => {
    mockSearchParams.set("booking_id", "bk_test_456");
    render(<BookingCancelledPage />);

    expect(screen.getByText("bk_test_456")).toBeInTheDocument();
  });

  it("does not show booking ID section when param is missing", () => {
    render(<BookingCancelledPage />);

    expect(screen.queryByText("Booking ID:")).not.toBeInTheDocument();
  });

  it("renders Try Again link to services page", () => {
    render(<BookingCancelledPage />);

    const tryAgainLink = screen.getByText("Try Again");
    expect(tryAgainLink).toBeInTheDocument();
    expect(tryAgainLink.closest("a")).toHaveAttribute("href", "/services");
  });

  it("renders Back to Home link", () => {
    render(<BookingCancelledPage />);

    const homeLink = screen.getByText("Back to Home");
    expect(homeLink).toBeInTheDocument();
    expect(homeLink.closest("a")).toHaveAttribute("href", "/");
  });
});
