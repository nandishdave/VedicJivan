import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, cleanup } from "@testing-library/react";
import { Button } from "@/components/ui/Button";

describe("Button", () => {
  beforeEach(() => {
    cleanup();
  });

  it("renders children text", () => {
    render(<Button>Click Me</Button>);
    expect(screen.getByText("Click Me")).toBeInTheDocument();
  });

  it("applies primary variant styles by default", () => {
    render(<Button>Primary</Button>);
    const btn = screen.getByText("Primary").closest("button");
    expect(btn?.className).toContain("bg-primary-600");
  });

  it("applies secondary variant styles", () => {
    render(<Button variant="secondary">Secondary</Button>);
    const btn = screen.getByText("Secondary").closest("button");
    expect(btn?.className).toContain("bg-vedic-dark");
  });

  it("applies outline variant styles", () => {
    render(<Button variant="outline">Outline</Button>);
    const btn = screen.getByText("Outline").closest("button");
    expect(btn?.className).toContain("border-primary-600");
  });

  it("applies ghost variant styles", () => {
    render(<Button variant="ghost">Ghost</Button>);
    const btn = screen.getByText("Ghost").closest("button");
    expect(btn?.className).toContain("text-primary-600");
    expect(btn?.className).not.toContain("bg-primary-600");
  });

  it("applies gold variant styles", () => {
    render(<Button variant="gold">Gold</Button>);
    const btn = screen.getByText("Gold").closest("button");
    expect(btn?.className).toContain("bg-gold-gradient");
  });

  it("applies danger variant styles", () => {
    render(<Button variant="danger">Danger</Button>);
    const btn = screen.getByText("Danger").closest("button");
    expect(btn?.className).toContain("bg-red-600");
  });

  it("applies sm size styles", () => {
    render(<Button size="sm">Small</Button>);
    const btn = screen.getByText("Small").closest("button");
    expect(btn?.className).toContain("px-4");
    expect(btn?.className).toContain("py-2");
    expect(btn?.className).toContain("text-sm");
  });

  it("applies md size styles by default", () => {
    render(<Button>Medium</Button>);
    const btn = screen.getByText("Medium").closest("button");
    expect(btn?.className).toContain("px-6");
    expect(btn?.className).toContain("py-3");
  });

  it("applies lg size styles", () => {
    render(<Button size="lg">Large</Button>);
    const btn = screen.getByText("Large").closest("button");
    expect(btn?.className).toContain("px-8");
    expect(btn?.className).toContain("py-4");
    expect(btn?.className).toContain("text-lg");
  });

  it("shows loading spinner when isLoading is true", () => {
    render(<Button isLoading>Loading</Button>);
    const btn = screen.getByText("Loading").closest("button");
    // Should have an SVG spinner
    const spinner = btn?.querySelector("svg.animate-spin");
    expect(spinner).toBeTruthy();
  });

  it("disables button when isLoading is true", () => {
    render(<Button isLoading>Submit</Button>);
    const btn = screen.getByText("Submit").closest("button");
    expect(btn).toBeDisabled();
  });

  it("disables button when disabled prop is true", () => {
    render(<Button disabled>Disabled</Button>);
    const btn = screen.getByText("Disabled").closest("button");
    expect(btn).toBeDisabled();
  });

  it("handles click events", () => {
    const onClick = vi.fn();
    render(<Button onClick={onClick}>Click</Button>);
    fireEvent.click(screen.getByText("Click"));
    expect(onClick).toHaveBeenCalledOnce();
  });

  it("does not fire click when disabled", () => {
    const onClick = vi.fn();
    render(<Button disabled onClick={onClick}>Click</Button>);
    fireEvent.click(screen.getByText("Click"));
    expect(onClick).not.toHaveBeenCalled();
  });

  it("merges custom className", () => {
    render(<Button className="custom-class">Custom</Button>);
    const btn = screen.getByText("Custom").closest("button");
    expect(btn?.className).toContain("custom-class");
  });

  it("passes type attribute", () => {
    render(<Button type="submit">Submit</Button>);
    const btn = screen.getByText("Submit").closest("button");
    expect(btn).toHaveAttribute("type", "submit");
  });

  it("forwards ref", () => {
    const ref = vi.fn();
    render(<Button ref={ref}>Ref</Button>);
    expect(ref).toHaveBeenCalled();
  });
});
