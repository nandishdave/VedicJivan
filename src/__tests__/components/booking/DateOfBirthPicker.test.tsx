import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, cleanup } from "@testing-library/react";
import { DateOfBirthPicker } from "@/components/booking/DateOfBirthPicker";

describe("DateOfBirthPicker", () => {
  beforeEach(() => {
    cleanup();
    vi.clearAllMocks();
  });

  it("renders day-of-week headers", () => {
    render(<DateOfBirthPicker selectedDate="" onDateSelect={vi.fn()} />);
    expect(screen.getByText("Sun")).toBeInTheDocument();
    expect(screen.getByText("Mon")).toBeInTheDocument();
    expect(screen.getByText("Sat")).toBeInTheDocument();
  });

  it("renders month and year dropdowns", () => {
    render(<DateOfBirthPicker selectedDate="" onDateSelect={vi.fn()} />);
    const selects = screen.getAllByRole("combobox");
    expect(selects.length).toBe(2); // month + year
    expect(screen.getByText("January")).toBeInTheDocument();
    expect(screen.getByText("December")).toBeInTheDocument();
  });

  it("calls onDateSelect when a day is clicked", () => {
    const onDateSelect = vi.fn();
    // Use a past month to ensure all days are clickable
    render(<DateOfBirthPicker selectedDate="" onDateSelect={onDateSelect} />);

    // Navigate to Jan 2000
    const [monthSelect, yearSelect] = screen.getAllByRole("combobox");
    fireEvent.change(yearSelect, { target: { value: "2000" } });
    fireEvent.change(monthSelect, { target: { value: "0" } }); // January

    const day15 = screen.getByText("15");
    fireEvent.click(day15);
    expect(onDateSelect).toHaveBeenCalledWith("2000-01-15");
  });

  it("highlights the selected date", () => {
    render(<DateOfBirthPicker selectedDate="2000-01-15" onDateSelect={vi.fn()} />);

    const day15 = screen.getByText("15");
    expect(day15.className).toContain("bg-primary-600");
  });

  it("disables future dates", () => {
    const onDateSelect = vi.fn();
    render(<DateOfBirthPicker selectedDate="" onDateSelect={onDateSelect} />);

    // Navigate to the current month — future days should be disabled
    const today = new Date();
    const lastDay = new Date(today.getFullYear(), today.getMonth() + 1, 0).getDate();

    // If today isn't the last day of the month, the last day should be disabled
    if (today.getDate() < lastDay) {
      const futureDayBtn = screen.getByText(String(lastDay));
      expect(futureDayBtn).toBeDisabled();
      fireEvent.click(futureDayBtn);
      expect(onDateSelect).not.toHaveBeenCalled();
    }
  });

  it("navigates to previous month with chevron", () => {
    render(<DateOfBirthPicker selectedDate="2000-06-10" onDateSelect={vi.fn()} />);

    // Should start showing June 2000
    expect(screen.getByText("10")).toBeInTheDocument();

    // Click prev month button (first button with chevron icon)
    const buttons = screen.getAllByRole("button");
    const prevBtn = buttons[0]; // First button is prev month
    fireEvent.click(prevBtn);

    // Month dropdown should now show May (value 4)
    const [monthSelect] = screen.getAllByRole("combobox");
    expect(monthSelect).toHaveValue("4"); // May = 4
  });

  it("navigates to next month with chevron", () => {
    render(<DateOfBirthPicker selectedDate="2000-06-10" onDateSelect={vi.fn()} />);

    // Click next month button (last navigation button)
    const buttons = screen.getAllByRole("button");
    // Find the nav button after the dropdowns
    const nextBtn = buttons.find((b) => {
      // Next button is the one right after month/year dropdowns in the header
      const parent = b.parentElement;
      return parent?.className?.includes("justify-between") && b !== buttons[0];
    });
    if (nextBtn) {
      fireEvent.click(nextBtn);
      const [monthSelect] = screen.getAllByRole("combobox");
      expect(monthSelect).toHaveValue("6"); // July = 6
    }
  });

  it("changes year via year dropdown", () => {
    render(<DateOfBirthPicker selectedDate="" onDateSelect={vi.fn()} />);
    const [, yearSelect] = screen.getAllByRole("combobox");
    fireEvent.change(yearSelect, { target: { value: "1990" } });
    expect(yearSelect).toHaveValue("1990");
  });

  it("changes month via month dropdown", () => {
    render(<DateOfBirthPicker selectedDate="2000-06-10" onDateSelect={vi.fn()} />);
    const [monthSelect] = screen.getAllByRole("combobox");
    fireEvent.change(monthSelect, { target: { value: "2" } }); // March
    expect(monthSelect).toHaveValue("2");
  });

  it("initializes to selected date's month/year when provided", () => {
    render(<DateOfBirthPicker selectedDate="1985-03-20" onDateSelect={vi.fn()} />);
    const [monthSelect, yearSelect] = screen.getAllByRole("combobox");
    expect(monthSelect).toHaveValue("2"); // March = 2
    expect(yearSelect).toHaveValue("1985");
  });
});
