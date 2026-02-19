import React from "react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor, cleanup } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import AdminLoginPage from "@/app/admin/login/page";

const { mockPush, mockLogin, mockMe, mockSetTokens } = vi.hoisted(() => ({
  mockPush: vi.fn(),
  mockLogin: vi.fn(),
  mockMe: vi.fn(),
  mockSetTokens: vi.fn(),
}));

vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: mockPush,
    replace: vi.fn(),
    back: vi.fn(),
    prefetch: vi.fn(),
  }),
  usePathname: () => "/admin/login",
}));

vi.mock("@/lib/api", () => ({
  authApi: {
    login: mockLogin,
    me: mockMe,
  },
}));

vi.mock("@/lib/auth", () => ({
  setTokens: mockSetTokens,
}));

vi.mock("@/components/ui/Container", () => ({
  Container: (props: { children: React.ReactNode }) =>
    React.createElement("div", null, props.children),
}));

describe("AdminLoginPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    cleanup();
  });

  it("renders login form with heading and inputs", () => {
    render(<AdminLoginPage />);
    expect(screen.getByText("Admin Login")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("admin@vedicjivan.com")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("Enter your password")).toBeInTheDocument();
    expect(screen.getByText("Sign in to manage VedicJivan")).toBeInTheDocument();
  });

  it("has a sign in button", () => {
    render(<AdminLoginPage />);
    const buttons = screen.getAllByRole("button");
    const signInBtn = buttons.find(b => b.textContent?.includes("Sign In"));
    expect(signInBtn).toBeTruthy();
  });

  it("logs in successfully and redirects to admin", async () => {
    mockLogin.mockResolvedValue({
      access_token: "access-123",
      refresh_token: "refresh-456",
    });
    mockMe.mockResolvedValue({ role: "admin", name: "Admin" });

    const user = userEvent.setup();
    render(<AdminLoginPage />);

    await user.type(screen.getByPlaceholderText("admin@vedicjivan.com"), "admin@test.com");
    await user.type(screen.getByPlaceholderText("Enter your password"), "password123");

    const form = screen.getByPlaceholderText("admin@vedicjivan.com").closest("form")!;
    fireEvent.submit(form);

    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith({
        email: "admin@test.com",
        password: "password123",
      });
      expect(mockSetTokens).toHaveBeenCalledWith("access-123", "refresh-456");
      expect(mockPush).toHaveBeenCalledWith("/admin");
    });
  });

  it("shows error for non-admin user", async () => {
    mockLogin.mockResolvedValue({ access_token: "a", refresh_token: "r" });
    mockMe.mockResolvedValue({ role: "user", name: "User" });

    const user = userEvent.setup();
    render(<AdminLoginPage />);

    await user.type(screen.getByPlaceholderText("admin@vedicjivan.com"), "user@test.com");
    await user.type(screen.getByPlaceholderText("Enter your password"), "pass");

    const form = screen.getByPlaceholderText("admin@vedicjivan.com").closest("form")!;
    fireEvent.submit(form);

    await waitFor(() => {
      expect(screen.getByText(/access denied/i)).toBeInTheDocument();
    });
  });

  it("shows error on login failure", async () => {
    mockLogin.mockRejectedValue(new Error("Invalid credentials"));

    const user = userEvent.setup();
    render(<AdminLoginPage />);

    await user.type(screen.getByPlaceholderText("admin@vedicjivan.com"), "bad@test.com");
    await user.type(screen.getByPlaceholderText("Enter your password"), "wrong");

    const form = screen.getByPlaceholderText("admin@vedicjivan.com").closest("form")!;
    fireEvent.submit(form);

    await waitFor(() => {
      expect(screen.getByText("Invalid credentials")).toBeInTheDocument();
    });
  });
});
