import { describe, it, expect, beforeEach } from "vitest";
import { render, screen, fireEvent, cleanup } from "@testing-library/react";
import { FAQAccordion } from "@/components/ui/FAQAccordion";

const faqItems = [
  { question: "What is Vedic astrology?", answer: "Vedic astrology is an ancient Indian science." },
  { question: "How do I book?", answer: "Visit the services page to book." },
  { question: "What is the refund policy?", answer: "Refunds are processed within 7 days." },
];

describe("FAQAccordion", () => {
  beforeEach(() => {
    cleanup();
  });

  it("renders all questions", () => {
    render(<FAQAccordion items={faqItems} />);

    expect(screen.getByText("What is Vedic astrology?")).toBeInTheDocument();
    expect(screen.getByText("How do I book?")).toBeInTheDocument();
    expect(screen.getByText("What is the refund policy?")).toBeInTheDocument();
  });

  it("does not show any answer initially", () => {
    render(<FAQAccordion items={faqItems} />);

    expect(screen.queryByText("Vedic astrology is an ancient Indian science.")).not.toBeInTheDocument();
    expect(screen.queryByText("Visit the services page to book.")).not.toBeInTheDocument();
  });

  it("shows answer when question is clicked", () => {
    render(<FAQAccordion items={faqItems} />);

    fireEvent.click(screen.getByText("What is Vedic astrology?"));

    expect(screen.getByText("Vedic astrology is an ancient Indian science.")).toBeInTheDocument();
  });

  it("hides answer when same question is clicked again", () => {
    render(<FAQAccordion items={faqItems} />);

    fireEvent.click(screen.getByText("What is Vedic astrology?"));
    expect(screen.getByText("Vedic astrology is an ancient Indian science.")).toBeInTheDocument();

    fireEvent.click(screen.getByText("What is Vedic astrology?"));
    expect(screen.queryByText("Vedic astrology is an ancient Indian science.")).not.toBeInTheDocument();
  });

  it("only shows one answer at a time", () => {
    render(<FAQAccordion items={faqItems} />);

    // Open first
    fireEvent.click(screen.getByText("What is Vedic astrology?"));
    expect(screen.getByText("Vedic astrology is an ancient Indian science.")).toBeInTheDocument();

    // Open second — first should close
    fireEvent.click(screen.getByText("How do I book?"));
    expect(screen.getByText("Visit the services page to book.")).toBeInTheDocument();
    expect(screen.queryByText("Vedic astrology is an ancient Indian science.")).not.toBeInTheDocument();
  });

  it("renders with empty items array", () => {
    const { container } = render(<FAQAccordion items={[]} />);
    expect(container.querySelector("button")).toBeNull();
  });

  it("applies custom className", () => {
    const { container } = render(<FAQAccordion items={faqItems} className="my-class" />);
    expect(container.firstElementChild?.className).toContain("my-class");
  });
});
