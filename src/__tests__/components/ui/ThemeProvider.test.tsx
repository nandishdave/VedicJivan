import { describe, it, expect, beforeEach, vi } from "vitest";
import { render, screen, act, cleanup } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import React from "react";

// Use real ThemeProvider, not the global mock
vi.unmock("@/components/ui/ThemeProvider");
import { ThemeProvider, useTheme } from "@/components/ui/ThemeProvider";

// Mock matchMedia for jsdom (not available by default)
const mockMatchMedia = vi.fn().mockImplementation((query: string) => ({
  matches: false,
  media: query,
  onchange: null,
  addListener: vi.fn(),
  removeListener: vi.fn(),
  addEventListener: vi.fn(),
  removeEventListener: vi.fn(),
  dispatchEvent: vi.fn(),
}));
Object.defineProperty(window, "matchMedia", {
  writable: true,
  value: mockMatchMedia,
});

// Helper component to expose theme context values
function ThemeConsumer() {
  const { theme, resolvedTheme, setTheme, toggleTheme } = useTheme();
  return (
    <div>
      <span data-testid="theme">{theme}</span>
      <span data-testid="resolved">{resolvedTheme}</span>
      <button data-testid="toggle" onClick={toggleTheme}>
        Toggle
      </button>
      <button data-testid="set-dark" onClick={() => setTheme("dark")}>
        Dark
      </button>
      <button data-testid="set-light" onClick={() => setTheme("light")}>
        Light
      </button>
      <button data-testid="set-system" onClick={() => setTheme("system")}>
        System
      </button>
    </div>
  );
}

describe("ThemeProvider", () => {
  beforeEach(() => {
    cleanup();
    localStorage.clear();
    document.documentElement.classList.remove("dark", "no-transitions");
  });

  it("renders children", () => {
    render(
      <ThemeProvider>
        <span>Hello</span>
      </ThemeProvider>
    );
    expect(screen.getByText("Hello")).toBeInTheDocument();
  });

  it("defaults to system theme (light) when no stored preference", () => {
    render(
      <ThemeProvider>
        <ThemeConsumer />
      </ThemeProvider>
    );
    expect(screen.getByTestId("theme")).toHaveTextContent("system");
    expect(screen.getByTestId("resolved")).toHaveTextContent("light");
  });

  it("reads stored theme from localStorage on mount", () => {
    localStorage.setItem("vedicjivan_theme", "dark");
    render(
      <ThemeProvider>
        <ThemeConsumer />
      </ThemeProvider>
    );
    expect(screen.getByTestId("theme")).toHaveTextContent("dark");
    expect(screen.getByTestId("resolved")).toHaveTextContent("dark");
    expect(document.documentElement.classList.contains("dark")).toBe(true);
  });

  it("toggleTheme switches from light to dark", async () => {
    const user = userEvent.setup();
    render(
      <ThemeProvider>
        <ThemeConsumer />
      </ThemeProvider>
    );

    expect(screen.getByTestId("resolved")).toHaveTextContent("light");

    await act(async () => {
      await user.click(screen.getByTestId("toggle"));
    });

    expect(screen.getByTestId("resolved")).toHaveTextContent("dark");
    expect(document.documentElement.classList.contains("dark")).toBe(true);
    expect(localStorage.getItem("vedicjivan_theme")).toBe("dark");
  });

  it("toggleTheme switches from dark to light", async () => {
    localStorage.setItem("vedicjivan_theme", "dark");
    const user = userEvent.setup();
    render(
      <ThemeProvider>
        <ThemeConsumer />
      </ThemeProvider>
    );

    expect(screen.getByTestId("resolved")).toHaveTextContent("dark");

    await act(async () => {
      await user.click(screen.getByTestId("toggle"));
    });

    expect(screen.getByTestId("resolved")).toHaveTextContent("light");
    expect(document.documentElement.classList.contains("dark")).toBe(false);
    expect(localStorage.getItem("vedicjivan_theme")).toBe("light");
  });

  it("setTheme persists preference to localStorage", async () => {
    const user = userEvent.setup();
    render(
      <ThemeProvider>
        <ThemeConsumer />
      </ThemeProvider>
    );

    await act(async () => {
      await user.click(screen.getByTestId("set-dark"));
    });

    expect(localStorage.getItem("vedicjivan_theme")).toBe("dark");
    expect(screen.getByTestId("theme")).toHaveTextContent("dark");

    await act(async () => {
      await user.click(screen.getByTestId("set-light"));
    });

    expect(localStorage.getItem("vedicjivan_theme")).toBe("light");
    expect(screen.getByTestId("theme")).toHaveTextContent("light");
  });

  it("adds dark class to documentElement when dark theme is set", async () => {
    const user = userEvent.setup();
    render(
      <ThemeProvider>
        <ThemeConsumer />
      </ThemeProvider>
    );

    expect(document.documentElement.classList.contains("dark")).toBe(false);

    await act(async () => {
      await user.click(screen.getByTestId("set-dark"));
    });

    expect(document.documentElement.classList.contains("dark")).toBe(true);

    await act(async () => {
      await user.click(screen.getByTestId("set-light"));
    });

    expect(document.documentElement.classList.contains("dark")).toBe(false);
  });

  it("removes no-transitions class after mount", async () => {
    document.documentElement.classList.add("no-transitions");

    render(
      <ThemeProvider>
        <ThemeConsumer />
      </ThemeProvider>
    );

    // requestAnimationFrame runs after paint — flush it
    await act(async () => {
      await vi.waitFor(() => {
        expect(document.documentElement.classList.contains("no-transitions")).toBe(false);
      });
    });
  });

  it("throws error when useTheme is used outside ThemeProvider", () => {
    // Suppress React error boundary noise
    const spy = vi.spyOn(console, "error").mockImplementation(() => {});

    expect(() => render(<ThemeConsumer />)).toThrow(
      "useTheme must be used within ThemeProvider"
    );

    spy.mockRestore();
  });
});
