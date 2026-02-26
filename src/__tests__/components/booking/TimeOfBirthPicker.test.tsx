import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, cleanup } from "@testing-library/react";
import { TimeOfBirthPicker } from "@/components/booking/TimeOfBirthPicker";

describe("TimeOfBirthPicker", () => {
  beforeEach(() => {
    cleanup();
    vi.clearAllMocks();
  });

  it("renders hour, minute selects and AM/PM buttons", () => {
    render(
      <TimeOfBirthPicker
        value={{ hour: "12", minute: "00", period: "AM" }}
        isUnknown={false}
        onTimeChange={vi.fn()}
        onUnknownChange={vi.fn()}
      />
    );

    expect(screen.getByLabelText("Hour")).toBeInTheDocument();
    expect(screen.getByLabelText("Minute")).toBeInTheDocument();
    expect(screen.getByText("AM")).toBeInTheDocument();
    expect(screen.getByText("PM")).toBeInTheDocument();
  });

  it("renders unknown checkbox", () => {
    render(
      <TimeOfBirthPicker
        value={{ hour: "12", minute: "00", period: "AM" }}
        isUnknown={false}
        onTimeChange={vi.fn()}
        onUnknownChange={vi.fn()}
      />
    );

    expect(screen.getByText(/don.*t know my exact birth time/i)).toBeInTheDocument();
    expect(screen.getByRole("checkbox")).not.toBeChecked();
  });

  it("calls onTimeChange when hour changes", () => {
    const onTimeChange = vi.fn();
    render(
      <TimeOfBirthPicker
        value={{ hour: "12", minute: "30", period: "AM" }}
        isUnknown={false}
        onTimeChange={onTimeChange}
        onUnknownChange={vi.fn()}
      />
    );

    fireEvent.change(screen.getByLabelText("Hour"), { target: { value: "05" } });
    expect(onTimeChange).toHaveBeenCalledWith({ hour: "05", minute: "30", period: "AM" });
  });

  it("calls onTimeChange when minute changes", () => {
    const onTimeChange = vi.fn();
    render(
      <TimeOfBirthPicker
        value={{ hour: "08", minute: "00", period: "PM" }}
        isUnknown={false}
        onTimeChange={onTimeChange}
        onUnknownChange={vi.fn()}
      />
    );

    fireEvent.change(screen.getByLabelText("Minute"), { target: { value: "45" } });
    expect(onTimeChange).toHaveBeenCalledWith({ hour: "08", minute: "45", period: "PM" });
  });

  it("calls onTimeChange when AM button clicked", () => {
    const onTimeChange = vi.fn();
    render(
      <TimeOfBirthPicker
        value={{ hour: "08", minute: "30", period: "PM" }}
        isUnknown={false}
        onTimeChange={onTimeChange}
        onUnknownChange={vi.fn()}
      />
    );

    fireEvent.click(screen.getByText("AM"));
    expect(onTimeChange).toHaveBeenCalledWith({ hour: "08", minute: "30", period: "AM" });
  });

  it("calls onTimeChange when PM button clicked", () => {
    const onTimeChange = vi.fn();
    render(
      <TimeOfBirthPicker
        value={{ hour: "08", minute: "30", period: "AM" }}
        isUnknown={false}
        onTimeChange={onTimeChange}
        onUnknownChange={vi.fn()}
      />
    );

    fireEvent.click(screen.getByText("PM"));
    expect(onTimeChange).toHaveBeenCalledWith({ hour: "08", minute: "30", period: "PM" });
  });

  it("calls onUnknownChange when checkbox toggled", () => {
    const onUnknownChange = vi.fn();
    render(
      <TimeOfBirthPicker
        value={{ hour: "12", minute: "00", period: "AM" }}
        isUnknown={false}
        onTimeChange={vi.fn()}
        onUnknownChange={onUnknownChange}
      />
    );

    fireEvent.click(screen.getByRole("checkbox"));
    expect(onUnknownChange).toHaveBeenCalledWith(true);
  });

  it("disables time selects when isUnknown is true", () => {
    render(
      <TimeOfBirthPicker
        value={null}
        isUnknown={true}
        onTimeChange={vi.fn()}
        onUnknownChange={vi.fn()}
      />
    );

    expect(screen.getByLabelText("Hour")).toBeDisabled();
    expect(screen.getByLabelText("Minute")).toBeDisabled();
    expect(screen.getByText("AM")).toBeDisabled();
    expect(screen.getByText("PM")).toBeDisabled();
    expect(screen.getByRole("checkbox")).toBeChecked();
  });

  it("defaults to 12:00 AM when value is null", () => {
    render(
      <TimeOfBirthPicker
        value={null}
        isUnknown={false}
        onTimeChange={vi.fn()}
        onUnknownChange={vi.fn()}
      />
    );

    expect(screen.getByLabelText("Hour")).toHaveValue("12");
    expect(screen.getByLabelText("Minute")).toHaveValue("00");
  });

  it("has all 12 hour options and 60 minute options", () => {
    render(
      <TimeOfBirthPicker
        value={{ hour: "01", minute: "00", period: "AM" }}
        isUnknown={false}
        onTimeChange={vi.fn()}
        onUnknownChange={vi.fn()}
      />
    );

    const hourSelect = screen.getByLabelText("Hour");
    const minuteSelect = screen.getByLabelText("Minute");
    expect(hourSelect.querySelectorAll("option").length).toBe(12);
    expect(minuteSelect.querySelectorAll("option").length).toBe(60);
  });
});
