import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, cleanup } from "@testing-library/react";
import { Input } from "@/components/ui/Input";

describe("Input", () => {
  beforeEach(() => {
    cleanup();
  });

  it("renders an input element", () => {
    render(<Input placeholder="Enter text" />);
    expect(screen.getByPlaceholderText("Enter text")).toBeInTheDocument();
  });

  it("renders label when provided", () => {
    render(<Input label="Email" id="email" />);
    expect(screen.getByText("Email")).toBeInTheDocument();
    expect(screen.getByLabelText("Email")).toBeInTheDocument();
  });

  it("does not render label when not provided", () => {
    render(<Input placeholder="No label" />);
    expect(screen.queryByRole("label")).not.toBeInTheDocument();
  });

  it("shows error message when error prop is set", () => {
    render(<Input error="This field is required" />);
    expect(screen.getByText("This field is required")).toBeInTheDocument();
  });

  it("applies error styles to input when error prop is set", () => {
    render(<Input error="Invalid" data-testid="err-input" />);
    const input = screen.getByTestId("err-input");
    expect(input.className).toContain("border-red-500");
  });

  it("does not show error message when error is not set", () => {
    render(<Input placeholder="Valid" />);
    const errorEl = document.querySelector(".text-red-600");
    expect(errorEl).toBeNull();
  });

  it("handles value changes", () => {
    const onChange = vi.fn();
    render(<Input onChange={onChange} placeholder="Type here" />);
    const input = screen.getByPlaceholderText("Type here");
    fireEvent.change(input, { target: { value: "hello" } });
    expect(onChange).toHaveBeenCalled();
  });

  it("passes HTML input attributes", () => {
    render(<Input type="email" name="user-email" required placeholder="email" />);
    const input = screen.getByPlaceholderText("email");
    expect(input).toHaveAttribute("type", "email");
    expect(input).toHaveAttribute("name", "user-email");
    expect(input).toBeRequired();
  });

  it("merges custom className", () => {
    render(<Input className="my-custom-class" data-testid="custom" />);
    const input = screen.getByTestId("custom");
    expect(input.className).toContain("my-custom-class");
  });

  it("forwards ref", () => {
    const ref = vi.fn();
    render(<Input ref={ref} />);
    expect(ref).toHaveBeenCalled();
  });

  it("associates label with input via id", () => {
    render(<Input label="Username" id="username" />);
    const label = screen.getByText("Username");
    expect(label).toHaveAttribute("for", "username");
  });

  it("is disabled when disabled prop is true", () => {
    render(<Input disabled placeholder="disabled" />);
    expect(screen.getByPlaceholderText("disabled")).toBeDisabled();
  });
});
