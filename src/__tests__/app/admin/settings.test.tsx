import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor, cleanup } from "@testing-library/react";
import SettingsPage from "@/app/admin/settings/page";

const { mockPush, mockGetToken, mockGetSettings, mockUpdateSettings } = vi.hoisted(() => ({
  mockPush: vi.fn(),
  mockGetToken: vi.fn(),
  mockGetSettings: vi.fn(),
  mockUpdateSettings: vi.fn(),
}));

vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: mockPush,
    replace: vi.fn(),
    back: vi.fn(),
    prefetch: vi.fn(),
  }),
  usePathname: () => "/admin/settings",
}));

vi.mock("@/lib/api", () => ({
  availabilityApi: {
    getSettings: mockGetSettings,
    updateSettings: mockUpdateSettings,
  },
}));

vi.mock("@/lib/auth", () => ({
  getToken: mockGetToken,
}));

vi.mock("@/components/ui/Container", () => ({
  Container: (props: { children: React.ReactNode }) =>
    <div>{props.children}</div>,
}));

vi.mock("@/components/ui/Button", () => ({
  Button: (props: { children: React.ReactNode; onClick?: () => void; disabled?: boolean }) =>
    <button onClick={props.onClick} disabled={props.disabled}>{props.children}</button>,
}));

import React from "react";

const DEFAULT_SETTINGS = {
  timezone: "Asia/Kolkata",
  weekly_hours: Array.from({ length: 7 }, (_, i) => ({
    day: i,
    is_open: i < 6,
    open_time: "10:00",
    close_time: "18:00",
  })),
};

describe("SettingsPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    cleanup();
    mockGetSettings.mockResolvedValue(DEFAULT_SETTINGS);
  });

  it("renders page heading", async () => {
    render(<SettingsPage />);
    await waitFor(() => {
      expect(screen.getAllByText("Business Hours Settings").length).toBeGreaterThanOrEqual(1);
    });
  });

  it("renders timezone selector", async () => {
    render(<SettingsPage />);
    await waitFor(() => {
      expect(screen.getAllByText("Timezone").length).toBeGreaterThanOrEqual(1);
    });
  });

  it("renders all 7 day labels", async () => {
    render(<SettingsPage />);
    await waitFor(() => {
      expect(screen.getByText("Monday")).toBeInTheDocument();
      expect(screen.getByText("Tuesday")).toBeInTheDocument();
      expect(screen.getByText("Wednesday")).toBeInTheDocument();
      expect(screen.getByText("Thursday")).toBeInTheDocument();
      expect(screen.getByText("Friday")).toBeInTheDocument();
      expect(screen.getByText("Saturday")).toBeInTheDocument();
      expect(screen.getByText("Sunday")).toBeInTheDocument();
    });
  });

  it("shows Sunday as Closed by default", async () => {
    render(<SettingsPage />);
    await waitFor(() => {
      const closedButtons = screen.getAllByText("Closed");
      expect(closedButtons.length).toBeGreaterThanOrEqual(1);
    });
  });

  it("saves settings with token", async () => {
    mockGetToken.mockReturnValue("admin-token");
    mockUpdateSettings.mockResolvedValue(DEFAULT_SETTINGS);

    render(<SettingsPage />);
    await waitFor(() => {
      expect(screen.getByText("Save Settings")).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText("Save Settings"));

    await waitFor(() => {
      expect(mockUpdateSettings).toHaveBeenCalledWith(
        expect.objectContaining({ timezone: "Asia/Kolkata" }),
        "admin-token"
      );
    });
  });

  it("redirects to login when no token on save", async () => {
    mockGetToken.mockReturnValue(null);

    render(<SettingsPage />);
    await waitFor(() => {
      expect(screen.getByText("Save Settings")).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText("Save Settings"));

    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith("/admin/login");
    });
  });

  it("shows success message after save", async () => {
    mockGetToken.mockReturnValue("admin-token");
    mockUpdateSettings.mockResolvedValue(DEFAULT_SETTINGS);

    render(<SettingsPage />);
    await waitFor(() => {
      expect(screen.getByText("Save Settings")).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText("Save Settings"));

    await waitFor(() => {
      expect(screen.getByText("Business hours updated successfully!")).toBeInTheDocument();
    });
  });

  it("shows error message on save failure", async () => {
    mockGetToken.mockReturnValue("admin-token");
    mockUpdateSettings.mockRejectedValue(new Error("Server error"));

    render(<SettingsPage />);
    await waitFor(() => {
      expect(screen.getByText("Save Settings")).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText("Save Settings"));

    await waitFor(() => {
      expect(screen.getByText("Server error")).toBeInTheDocument();
    });
  });
});
