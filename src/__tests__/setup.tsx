/* eslint-disable react/display-name */
import "@testing-library/jest-dom/vitest";
import React from "react";
import { vi } from "vitest";

// Mock window.gtag for analytics tests
Object.defineProperty(window, "gtag", {
  value: vi.fn(),
  writable: true,
  configurable: true,
});

// Mock next/navigation
vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
    back: vi.fn(),
    prefetch: vi.fn(),
  }),
  usePathname: () => "/",
  useSearchParams: () => new URLSearchParams(),
}));

// Mock next/link
vi.mock("next/link", () => ({
  default: (props: Record<string, unknown>) =>
    React.createElement("a", { href: props.href }, props.children as React.ReactNode),
}));

// Mock framer-motion to render plain elements
vi.mock("framer-motion", () => {
  const forwardComponent = (tag: string) =>
    React.forwardRef((props: Record<string, unknown>, ref: React.Ref<unknown>) => {
      const { whileHover, whileTap, transition, whileInView, initial, animate, exit, variants, ...rest } = props;
      void whileHover; void whileTap; void transition; void whileInView; void initial; void animate; void exit; void variants;
      return React.createElement(tag, { ...rest, ref });
    });

  return {
    motion: {
      div: forwardComponent("div"),
      button: forwardComponent("button"),
      span: forwardComponent("span"),
      section: forwardComponent("section"),
      p: forwardComponent("p"),
      h1: forwardComponent("h1"),
      h2: forwardComponent("h2"),
      h3: forwardComponent("h3"),
      a: forwardComponent("a"),
    },
    AnimatePresence: (props: Record<string, unknown>) => props.children,
    useInView: () => true,
  };
});

// Mock lucide-react icons as simple spans — explicit exports instead of Proxy
vi.mock("lucide-react", () => {
  const icon = (name: string) => (props: Record<string, unknown>) =>
    React.createElement("span", { "data-testid": `icon-${name}`, ...props });

  return {
    __esModule: true,
    // BookingCalendar
    ChevronLeft: icon("ChevronLeft"),
    ChevronRight: icon("ChevronRight"),
    // TimeSlotPicker
    Clock: icon("Clock"),
    // BookingWizard
    Calendar: icon("Calendar"),
    User: icon("User"),
    CreditCard: icon("CreditCard"),
    CheckCircle2: icon("CheckCircle2"),
    ArrowLeft: icon("ArrowLeft"),
    ArrowRight: icon("ArrowRight"),
    // Admin pages
    Lock: icon("Lock"),
    Users: icon("Users"),
    TrendingUp: icon("TrendingUp"),
    Settings: icon("Settings"),
    LayoutDashboard: icon("LayoutDashboard"),
    LogOut: icon("LogOut"),
    ExternalLink: icon("ExternalLink"),
    // Availability page
    CalendarOff: icon("CalendarOff"),
    Trash2: icon("Trash2"),
    Plus: icon("Plus"),
    // Settings page
    Globe: icon("Globe"),
    Save: icon("Save"),
    // Mobile nav
    Menu: icon("Menu"),
    X: icon("X"),
    // Button
    Loader2: icon("Loader2"),
  };
});
