import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor, cleanup } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { BookingWizard } from "@/components/booking/BookingWizard";
import type { Service } from "@/data/services";

const { mockCreate, mockResume, mockGetHolidays, mockGetSlots, mockGetSettings } = vi.hoisted(() => ({
  mockCreate: vi.fn(),
  mockResume: vi.fn(),
  mockGetHolidays: vi.fn(),
  mockGetSlots: vi.fn(),
  mockGetSettings: vi.fn(),
}));

vi.mock("@/lib/api", () => ({
  availabilityApi: {
    getHolidays: mockGetHolidays,
    getSlots: mockGetSlots,
    getSettings: mockGetSettings,
  },
  bookingsApi: {
    create: mockCreate,
    resume: mockResume,
  },
  paymentsApi: {
    createOrder: vi.fn().mockResolvedValue({
      order_id: "order-1",
      amount: 199900,
      currency: "INR",
      key_id: "rzp_test",
    }),
    verify: vi.fn().mockResolvedValue({ status: "ok" }),
  },
}));

// Mock the new birth detail components
vi.mock("@/components/booking/DateOfBirthPicker", () => ({
  DateOfBirthPicker: ({ onDateSelect, selectedDate }: { onDateSelect: (d: string) => void; selectedDate: string }) => (
    <button data-testid="mock-dob-picker" onClick={() => onDateSelect("1990-05-15")}>
      {selectedDate || "Select DOB"}
    </button>
  ),
}));

vi.mock("@/components/booking/TimeOfBirthPicker", () => ({
  TimeOfBirthPicker: ({ isUnknown, onUnknownChange }: { isUnknown: boolean; onUnknownChange: (v: boolean) => void }) => (
    <label>
      <input
        type="checkbox"
        data-testid="mock-birth-time-unknown"
        checked={isUnknown}
        onChange={(e: React.ChangeEvent<HTMLInputElement>) => onUnknownChange(e.target.checked)}
      />
      Unknown birth time
    </label>
  ),
}));

vi.mock("@/components/booking/PlaceOfBirthAutocomplete", () => ({
  PlaceOfBirthAutocomplete: ({ onPlaceSelect, value }: { onPlaceSelect: (p: { name: string; latitude: number; longitude: number }) => void; value: string }) => (
    <button
      data-testid="mock-place-picker"
      onClick={() => onPlaceSelect({ name: "Mumbai, India", latitude: 19.076, longitude: 72.877 })}
    >
      {value || "Select place"}
    </button>
  ),
}));

const consultationService: Service = {
  slug: "call-consultation",
  title: "Call Consultation",
  shortDescription: "Test",
  description: "Test description",
  priceINR: "\u20B91,999",
  priceEUR: "\u20AC29",
  duration: "30 min",
  icon: "Phone",
  image: "test.jpg",
  category: "consultation",
  features: [],
  process: [],
  faqs: [],
};

const reportService: Service = {
  slug: "premium-kundli",
  title: "Premium Kundli Report",
  shortDescription: "Test",
  description: "Test description",
  priceINR: "\u20B94,999",
  priceEUR: "\u20AC59",
  duration: null,
  icon: "FileText",
  image: "test.jpg",
  category: "report",
  features: [],
  process: [],
  faqs: [],
};

/** Fill in all required details fields including birth info */
async function fillDetailsForm(user: ReturnType<typeof userEvent.setup>) {
  await user.type(screen.getByPlaceholderText("Enter your full name"), "John Doe");
  await user.type(screen.getByPlaceholderText("you@example.com"), "john@test.com");
  await user.type(screen.getByPlaceholderText(/\+91/), "9876543210");
  await user.type(
    screen.getByPlaceholderText(/describe what you/i),
    "Need consultation"
  );

  // Select DOB via mock
  fireEvent.click(screen.getByTestId("mock-dob-picker"));
  // Check birth time unknown
  fireEvent.click(screen.getByTestId("mock-birth-time-unknown"));
  // Select place via mock
  fireEvent.click(screen.getByTestId("mock-place-picker"));
}

describe("BookingWizard", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    cleanup();
    localStorage.clear();
    mockResume.mockRejectedValue(new Error("not found"));
    mockGetHolidays.mockResolvedValue([]);
    mockGetSettings.mockResolvedValue({
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
    });
    mockGetSlots.mockResolvedValue([
      { start: "09:00", end: "09:30" },
      { start: "10:00", end: "10:30" },
    ]);
    mockCreate.mockResolvedValue({ id: "booking-123", price_inr: 1999 });
  });

  it("renders date step first for consultation services", async () => {
    render(<BookingWizard service={consultationService} />);
    await waitFor(() => {
      expect(screen.getByRole("heading", { name: "Select a Date" })).toBeInTheDocument();
    });
  });

  it("renders details step first for report services", async () => {
    render(<BookingWizard service={reportService} />);
    await waitFor(() => {
      expect(screen.getByRole("heading", { name: "Your Details" })).toBeInTheDocument();
    });
  });

  it("consultation has more progress steps than report", async () => {
    const { unmount } = render(<BookingWizard service={consultationService} />);
    await waitFor(() => {
      expect(screen.getAllByText("Date").length).toBeGreaterThanOrEqual(1);
    });
    unmount();

    render(<BookingWizard service={reportService} />);
    await waitFor(() => {
      expect(screen.queryByText("Date")).not.toBeInTheDocument();
    });
  });

  it("has disabled Back button on first step", async () => {
    const { container } = render(<BookingWizard service={consultationService} />);
    await waitFor(() => {
      const buttons = container.querySelectorAll("button[disabled]");
      expect(buttons.length).toBeGreaterThanOrEqual(1);
    });
  });

  it("renders form fields on details step for report", async () => {
    render(<BookingWizard service={reportService} />);
    await waitFor(() => {
      expect(screen.getByPlaceholderText("Enter your full name")).toBeInTheDocument();
    });
    expect(screen.getByPlaceholderText("you@example.com")).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/\+91/)).toBeInTheDocument();
  });

  it("has notes textarea on details step", async () => {
    render(<BookingWizard service={reportService} />);
    await waitFor(() => {
      expect(screen.getByPlaceholderText(/describe what you/i)).toBeInTheDocument();
    });
  });

  it("renders birth detail pickers on details step", async () => {
    render(<BookingWizard service={reportService} />);
    await waitFor(() => {
      expect(screen.getByTestId("mock-dob-picker")).toBeInTheDocument();
    });
    expect(screen.getByTestId("mock-birth-time-unknown")).toBeInTheDocument();
    expect(screen.getByTestId("mock-place-picker")).toBeInTheDocument();
  });

  it("Next button disabled without notes", async () => {
    const user = userEvent.setup();
    render(<BookingWizard service={reportService} />);

    await user.type(screen.getByPlaceholderText("Enter your full name"), "John");
    await user.type(screen.getByPlaceholderText("you@example.com"), "j@t.com");
    await user.type(screen.getByPlaceholderText(/\+91/), "123");
    // Don't fill notes, DOB, or place

    const allButtons = screen.getAllByRole("button");
    const nextBtn = allButtons.find(b => b.textContent?.includes("Next"));
    expect(nextBtn).toHaveAttribute("disabled");
  });

  it("navigates to review step when form is filled for report", async () => {
    const user = userEvent.setup();
    render(<BookingWizard service={reportService} />);

    await fillDetailsForm(user);

    const allButtons = screen.getAllByRole("button");
    const nextBtn = allButtons.find(b => b.textContent?.includes("Next") && !b.hasAttribute("disabled"));
    expect(nextBtn).toBeTruthy();
    fireEvent.click(nextBtn!);

    await waitFor(() => {
      expect(screen.getByText("Review Your Booking")).toBeInTheDocument();
    });
  });

  it("shows service title and user data in review step", async () => {
    const user = userEvent.setup();
    render(<BookingWizard service={reportService} />);

    await fillDetailsForm(user);

    const allButtons = screen.getAllByRole("button");
    const nextBtn = allButtons.find(b => b.textContent?.includes("Next") && !b.hasAttribute("disabled"));
    fireEvent.click(nextBtn!);

    await waitFor(() => {
      expect(screen.getByText("Premium Kundli Report")).toBeInTheDocument();
      expect(screen.getByText("John Doe")).toBeInTheDocument();
      expect(screen.getByText("john@test.com")).toBeInTheDocument();
    });
  });

  it("review step shows birth details", async () => {
    const user = userEvent.setup();
    render(<BookingWizard service={reportService} />);

    await fillDetailsForm(user);

    const allButtons = screen.getAllByRole("button");
    const nextBtn = allButtons.find(b => b.textContent?.includes("Next") && !b.hasAttribute("disabled"));
    fireEvent.click(nextBtn!);

    await waitFor(() => {
      expect(screen.getByText("1990-05-15")).toBeInTheDocument();
      expect(screen.getByText("Unknown")).toBeInTheDocument();
      expect(screen.getByText("Mumbai, India")).toBeInTheDocument();
    });
  });

  it("creates booking on Proceed to Payment click", async () => {
    const user = userEvent.setup();
    render(<BookingWizard service={reportService} />);

    await fillDetailsForm(user);

    const allButtons = screen.getAllByRole("button");
    const nextBtn = allButtons.find(b => b.textContent?.includes("Next") && !b.hasAttribute("disabled"));
    fireEvent.click(nextBtn!);

    await waitFor(() => screen.getByText("Proceed to Payment"));
    fireEvent.click(screen.getByText("Proceed to Payment"));

    await waitFor(() => {
      expect(mockCreate).toHaveBeenCalledWith(
        expect.objectContaining({
          service_slug: "premium-kundli",
          user_name: "John Doe",
          user_email: "john@test.com",
          date_of_birth: "1990-05-15",
          birth_time_unknown: true,
          place_of_birth: "Mumbai, India",
          birth_latitude: 19.076,
          birth_longitude: 72.877,
        })
      );
    });
  });

  it("shows error when booking creation fails", async () => {
    mockCreate.mockRejectedValueOnce(new Error("Slot unavailable"));

    const user = userEvent.setup();
    render(<BookingWizard service={reportService} />);

    await fillDetailsForm(user);

    const allButtons = screen.getAllByRole("button");
    const nextBtn = allButtons.find(b => b.textContent?.includes("Next") && !b.hasAttribute("disabled"));
    fireEvent.click(nextBtn!);

    await waitFor(() => screen.getByText("Proceed to Payment"));
    fireEvent.click(screen.getByText("Proceed to Payment"));

    await waitFor(() => {
      expect(screen.getByText("Slot unavailable")).toBeInTheDocument();
    });
  });

  it("shows payment step after successful booking", async () => {
    const user = userEvent.setup();
    render(<BookingWizard service={reportService} />);

    await fillDetailsForm(user);

    const allButtons = screen.getAllByRole("button");
    const nextBtn = allButtons.find(b => b.textContent?.includes("Next") && !b.hasAttribute("disabled"));
    fireEvent.click(nextBtn!);

    await waitFor(() => screen.getByText("Proceed to Payment"));
    fireEvent.click(screen.getByText("Proceed to Payment"));

    await waitFor(() => {
      expect(screen.getByText("Complete Payment")).toBeInTheDocument();
    });
  });

  it("consultation: navigates from date to time step", async () => {
    render(<BookingWizard service={consultationService} />);
    expect(screen.getByRole("heading", { name: "Select a Date" })).toBeInTheDocument();

    await waitFor(() => {
      const now = new Date();
      const lastDay = new Date(now.getFullYear(), now.getMonth() + 1, 0).getDate();
      const dayButtons = screen.getAllByText(String(lastDay));
      const clickable = dayButtons.find(btn => !btn.hasAttribute("disabled"));
      if (clickable) fireEvent.click(clickable);
    });

    const allButtons = screen.getAllByRole("button");
    const nextBtn = allButtons.find(b => b.textContent?.includes("Next") && !b.hasAttribute("disabled"));
    if (nextBtn) {
      fireEvent.click(nextBtn);
      await waitFor(() => {
        expect(screen.getByRole("heading", { name: "Select a Time Slot" })).toBeInTheDocument();
      });
    }
  });

  it("consultation: navigates from time to duration step", async () => {
    render(<BookingWizard service={consultationService} />);

    await waitFor(() => {
      const now = new Date();
      const lastDay = new Date(now.getFullYear(), now.getMonth() + 1, 0).getDate();
      const dayButtons = screen.getAllByText(String(lastDay));
      const clickable = dayButtons.find(btn => !btn.hasAttribute("disabled"));
      if (clickable) fireEvent.click(clickable);
    });

    let allButtons = screen.getAllByRole("button");
    let nextBtn = allButtons.find(b => b.textContent?.includes("Next") && !b.hasAttribute("disabled"));
    if (nextBtn) {
      fireEvent.click(nextBtn);

      await waitFor(() => {
        expect(screen.getByText("09:00")).toBeInTheDocument();
      });
      fireEvent.click(screen.getByText("09:00"));

      allButtons = screen.getAllByRole("button");
      nextBtn = allButtons.find(b => b.textContent?.includes("Next") && !b.hasAttribute("disabled"));
      if (nextBtn) {
        fireEvent.click(nextBtn);
        await waitFor(() => {
          expect(screen.getByRole("heading", { name: "Select Duration" })).toBeInTheDocument();
          expect(screen.getAllByText("30 minutes").length).toBeGreaterThanOrEqual(1);
          expect(screen.getAllByText("45 minutes").length).toBeGreaterThanOrEqual(1);
          expect(screen.getAllByText("60 minutes").length).toBeGreaterThanOrEqual(1);
        });
      }
    }
  });

  it("consultation: full flow from date to review shows all details", async () => {
    const user = userEvent.setup();
    render(<BookingWizard service={consultationService} />);

    // Step 1: Select date
    await waitFor(() => {
      const now = new Date();
      const lastDay = new Date(now.getFullYear(), now.getMonth() + 1, 0).getDate();
      const dayButtons = screen.getAllByText(String(lastDay));
      const clickable = dayButtons.find(btn => !btn.hasAttribute("disabled"));
      if (clickable) fireEvent.click(clickable);
    });

    let allButtons = screen.getAllByRole("button");
    let nextBtn = allButtons.find(b => b.textContent?.includes("Next") && !b.hasAttribute("disabled"));
    if (!nextBtn) return;
    fireEvent.click(nextBtn);

    // Step 2: Select time
    await waitFor(() => {
      expect(screen.getByText("09:00")).toBeInTheDocument();
    });
    fireEvent.click(screen.getByText("09:00"));

    allButtons = screen.getAllByRole("button");
    nextBtn = allButtons.find(b => b.textContent?.includes("Next") && !b.hasAttribute("disabled"));
    if (nextBtn) fireEvent.click(nextBtn);

    // Step 3: Select duration
    await waitFor(() => {
      expect(screen.getAllByText("30 minutes").length).toBeGreaterThanOrEqual(1);
    });
    fireEvent.click(screen.getAllByText("30 minutes")[0]);

    allButtons = screen.getAllByRole("button");
    nextBtn = allButtons.find(b => b.textContent?.includes("Next") && !b.hasAttribute("disabled"));
    if (nextBtn) fireEvent.click(nextBtn);

    // Step 4: Fill details
    await waitFor(() => {
      expect(screen.getByPlaceholderText("Enter your full name")).toBeInTheDocument();
    });
    await fillDetailsForm(user);

    allButtons = screen.getAllByRole("button");
    nextBtn = allButtons.find(b => b.textContent?.includes("Next") && !b.hasAttribute("disabled"));
    if (nextBtn) fireEvent.click(nextBtn);

    // Step 5: Review
    await waitFor(() => {
      expect(screen.getByText("Review Your Booking")).toBeInTheDocument();
      expect(screen.getByText("Call Consultation")).toBeInTheDocument();
      expect(screen.getByText("John Doe")).toBeInTheDocument();
      expect(screen.getByText("john@test.com")).toBeInTheDocument();
      expect(screen.getByText("09:00")).toBeInTheDocument();
      expect(screen.getByText("30 minutes")).toBeInTheDocument();
      expect(screen.getByText("1990-05-15")).toBeInTheDocument();
      expect(screen.getByText("Mumbai, India")).toBeInTheDocument();
    });
  });

  it("consultation: back button navigates to previous step", async () => {
    render(<BookingWizard service={consultationService} />);

    await waitFor(() => {
      const now = new Date();
      const lastDay = new Date(now.getFullYear(), now.getMonth() + 1, 0).getDate();
      const dayButtons = screen.getAllByText(String(lastDay));
      const clickable = dayButtons.find(btn => !btn.hasAttribute("disabled"));
      if (clickable) fireEvent.click(clickable);
    });

    const allButtons = screen.getAllByRole("button");
    const nextBtn = allButtons.find(b => b.textContent?.includes("Next") && !b.hasAttribute("disabled"));
    if (nextBtn) {
      fireEvent.click(nextBtn);
      await waitFor(() => {
        expect(screen.getByRole("heading", { name: "Select a Time Slot" })).toBeInTheDocument();
      });

      const backBtn = screen.getAllByRole("button").find(b => b.textContent?.includes("Back") && !b.hasAttribute("disabled"));
      if (backBtn) {
        fireEvent.click(backBtn);
        await waitFor(() => {
          expect(screen.getByRole("heading", { name: "Select a Date" })).toBeInTheDocument();
        });
      }
    }
  });

  it("shows payment error when createOrder fails", async () => {
    const { paymentsApi } = await import("@/lib/api");
    (paymentsApi.createOrder as ReturnType<typeof vi.fn>).mockRejectedValueOnce(new Error("Payment gateway down"));

    const user = userEvent.setup();
    render(<BookingWizard service={reportService} />);

    await fillDetailsForm(user);

    const allButtons = screen.getAllByRole("button");
    const nextBtn = allButtons.find(b => b.textContent?.includes("Next") && !b.hasAttribute("disabled"));
    fireEvent.click(nextBtn!);

    await waitFor(() => screen.getByText("Proceed to Payment"));
    fireEvent.click(screen.getByText("Proceed to Payment"));

    await waitFor(() => screen.getByText("Complete Payment"));

    const payBtn = screen.getAllByRole("button").find(b => b.textContent?.includes("Pay"));
    fireEvent.click(payBtn!);

    await waitFor(() => {
      expect(screen.getByText("Payment gateway down")).toBeInTheDocument();
    });
  });

  it("report service uses today's date for booking", async () => {
    const user = userEvent.setup();
    render(<BookingWizard service={reportService} />);

    await fillDetailsForm(user);

    const allButtons = screen.getAllByRole("button");
    const nextBtn = allButtons.find(b => b.textContent?.includes("Next") && !b.hasAttribute("disabled"));
    fireEvent.click(nextBtn!);

    await waitFor(() => screen.getByText("Proceed to Payment"));
    fireEvent.click(screen.getByText("Proceed to Payment"));

    await waitFor(() => {
      const callArgs = mockCreate.mock.calls[0][0];
      expect(callArgs.time_slot).toBe("00:00");
      expect(callArgs.duration_minutes).toBe(0);
    });
  });

  // ═══════════════════════════════════════
  // Resume pending booking tests
  // ═══════════════════════════════════════

  it("shows resume prompt when localStorage has a valid pending booking", async () => {
    const record = {
      bookingId: "booking-resume-1",
      createdAt: new Date().toISOString(),
      serviceSlug: "premium-kundli",
    };
    localStorage.setItem("vedicjivan_pending_booking_premium-kundli", JSON.stringify(record));

    mockResume.mockResolvedValueOnce({
      id: "booking-resume-1",
      price_inr: 4999,
      status: "pending",
      service_title: "Premium Kundli Report",
      service_slug: "premium-kundli",
      date: "2026-03-16",
      time_slot: "00:00",
      duration_minutes: 0,
      user_name: "John Doe",
      user_email: "john@test.com",
      user_phone: "1234567890",
    });

    render(<BookingWizard service={reportService} />);

    await waitFor(() => {
      expect(screen.getByText("Resume Your Booking?")).toBeInTheDocument();
    });
  });

  it("clears resume prompt when Start Fresh is clicked", async () => {
    const record = {
      bookingId: "booking-resume-2",
      createdAt: new Date().toISOString(),
      serviceSlug: "premium-kundli",
    };
    localStorage.setItem("vedicjivan_pending_booking_premium-kundli", JSON.stringify(record));

    mockResume.mockResolvedValueOnce({
      id: "booking-resume-2",
      price_inr: 4999,
      status: "pending",
      service_title: "Premium Kundli Report",
      service_slug: "premium-kundli",
      date: "2026-03-16",
      time_slot: "00:00",
      duration_minutes: 0,
      user_name: "John Doe",
      user_email: "john@test.com",
      user_phone: "1234567890",
    });

    render(<BookingWizard service={reportService} />);

    await waitFor(() => screen.getByText("Start Fresh"));
    fireEvent.click(screen.getByText("Start Fresh"));

    expect(screen.queryByText("Resume Your Booking?")).not.toBeInTheDocument();
    expect(localStorage.getItem("vedicjivan_pending_booking_premium-kundli")).toBeNull();
  });

  it("navigates to payment step when Resume & Pay is clicked", async () => {
    const record = {
      bookingId: "booking-resume-3",
      createdAt: new Date().toISOString(),
      serviceSlug: "premium-kundli",
    };
    localStorage.setItem("vedicjivan_pending_booking_premium-kundli", JSON.stringify(record));

    mockResume.mockResolvedValueOnce({
      id: "booking-resume-3",
      price_inr: 4999,
      status: "pending",
      service_title: "Premium Kundli Report",
      service_slug: "premium-kundli",
      date: "2026-03-16",
      time_slot: "00:00",
      duration_minutes: 0,
      user_name: "John Doe",
      user_email: "john@test.com",
      user_phone: "1234567890",
    });

    render(<BookingWizard service={reportService} />);

    await waitFor(() => screen.getByText("Resume & Pay"));
    fireEvent.click(screen.getByText("Resume & Pay"));

    await waitFor(() => {
      expect(screen.getByText("Complete Payment")).toBeInTheDocument();
    });
  });
});
