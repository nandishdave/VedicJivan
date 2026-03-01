import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, cleanup } from "@testing-library/react";

// Mock next/image
vi.mock("next/image", () => ({
  default: (props: Record<string, unknown>) => {
    // eslint-disable-next-line @next/next/no-img-element, jsx-a11y/alt-text
    const { priority, fill, ...rest } = props;
    void priority;
    void fill;
    return <img {...(rest as React.ImgHTMLAttributes<HTMLImageElement>)} />;
  },
}));

// Mock WhatsAppIcon
vi.mock("@/components/icons/WhatsAppIcon", () => ({
  WhatsAppIcon: (props: Record<string, unknown>) => <span data-testid="whatsapp-icon" {...props} />,
}));

// Mock navigation config
vi.mock("@/config/navigation", () => ({
  mainNav: [
    { label: "Home", href: "/" },
    { label: "About", href: "/about" },
    {
      label: "Services",
      href: "/services",
      children: [
        { label: "Call Consultation", href: "/services/call-consultation" },
        { label: "Video Consultation", href: "/services/video-consultation" },
      ],
    },
    {
      label: "Blog",
      href: "/blog",
      children: [
        { label: "Articles", href: "/blog" },
        { label: "External Blog", href: "https://example.com/blog", external: true },
      ],
    },
  ],
}));

// Mock site config
vi.mock("@/config/site", () => ({
  siteConfig: {
    contact: {
      whatsapp: "1234567890",
      phone: "+91 12345 67890",
      email: "test@example.com",
    },
    social: {
      instagram: "https://instagram.com/test",
      youtube: "https://youtube.com/test",
      facebook: "https://facebook.com/test",
    },
  },
}));

import { Header } from "@/components/layout/Header";

describe("Header", () => {
  beforeEach(() => {
    cleanup();
    vi.clearAllMocks();
  });

  it("renders the logo", () => {
    render(<Header />);

    const logo = screen.getByAltText("VedicJivan — Connect The Divine Within");
    expect(logo).toBeInTheDocument();
  });

  it("renders navigation links", () => {
    render(<Header />);

    expect(screen.getAllByText("Home").length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText("About").length).toBeGreaterThanOrEqual(1);
  });

  it("renders Book Consultation CTA", () => {
    render(<Header />);

    const ctaButtons = screen.getAllByText("Book Consultation");
    expect(ctaButtons.length).toBeGreaterThanOrEqual(1);
  });

  it("renders Login link", () => {
    render(<Header />);

    const loginButtons = screen.getAllByText("Login");
    expect(loginButtons.length).toBeGreaterThanOrEqual(1);
  });

  it("toggles mobile menu on button click", () => {
    render(<Header />);

    const menuButton = screen.getByLabelText("Open menu");
    fireEvent.click(menuButton);

    // After opening, the button label changes to "Close menu"
    expect(screen.getByLabelText("Close menu")).toBeInTheDocument();
  });

  it("closes mobile menu on second click", () => {
    render(<Header />);

    const openButton = screen.getByLabelText("Open menu");
    fireEvent.click(openButton);
    expect(screen.getByLabelText("Close menu")).toBeInTheDocument();

    fireEvent.click(screen.getByLabelText("Close menu"));
    expect(screen.getByLabelText("Open menu")).toBeInTheDocument();
  });

  it("renders social media links in top bar", () => {
    render(<Header />);

    expect(screen.getByLabelText("Instagram")).toHaveAttribute("href", "https://instagram.com/test");
    expect(screen.getByLabelText("YouTube")).toHaveAttribute("href", "https://youtube.com/test");
    expect(screen.getByLabelText("Facebook")).toHaveAttribute("href", "https://facebook.com/test");
  });

  it("renders contact info in top bar", () => {
    render(<Header />);

    expect(screen.getByText("+91 12345 67890")).toBeInTheDocument();
    expect(screen.getByText("test@example.com")).toBeInTheDocument();
  });

  it("renders theme toggle button", () => {
    render(<Header />);

    // Both desktop top bar and mobile menu have a "Dark Mode" toggle
    const darkModeElements = screen.getAllByText("Dark Mode");
    expect(darkModeElements.length).toBe(2);
  });

  it("renders dropdown items for Services", () => {
    render(<Header />);

    // Dropdown children are rendered (though visually hidden until hover)
    expect(screen.getAllByText("Call Consultation").length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText("Video Consultation").length).toBeGreaterThanOrEqual(1);
  });

  it("renders external links with target _blank", () => {
    render(<Header />);

    const externalLinks = screen.getAllByText("External Blog");
    const externalLink = externalLinks.find((el) => el.closest("a")?.getAttribute("target") === "_blank");
    expect(externalLink).toBeDefined();
  });
});
