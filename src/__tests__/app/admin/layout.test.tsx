import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor, fireEvent, cleanup } from "@testing-library/react";
import AdminLayout from "@/app/admin/layout";

const { mockPush, mockGetToken, mockClearTokens, mockAuthMe, mockPathname } = vi.hoisted(() => ({
  mockPush: vi.fn(),
  mockGetToken: vi.fn(),
  mockClearTokens: vi.fn(),
  mockAuthMe: vi.fn(),
  mockPathname: { value: "/admin" },
}));

vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: mockPush,
    replace: vi.fn(),
    back: vi.fn(),
    prefetch: vi.fn(),
  }),
  usePathname: () => mockPathname.value,
}));

vi.mock("@/lib/api", () => ({
  authApi: { me: mockAuthMe },
}));

vi.mock("@/lib/auth", () => ({
  getToken: mockGetToken,
  clearTokens: mockClearTokens,
}));

describe("AdminLayout", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    cleanup();
    mockPathname.value = "/admin";
  });

  it("renders children directly on login page", () => {
    mockPathname.value = "/admin/login";
    render(
      <AdminLayout>
        <div>Login Form</div>
      </AdminLayout>
    );
    expect(screen.getByText("Login Form")).toBeInTheDocument();
  });

  it("redirects to login when no token on non-login page", async () => {
    mockGetToken.mockReturnValue(null);
    render(
      <AdminLayout>
        <div>Dashboard</div>
      </AdminLayout>
    );
    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith("/admin/login");
    });
  });

  it("shows sidebar navigation for admin users", async () => {
    mockGetToken.mockReturnValue("admin-token");
    mockAuthMe.mockResolvedValue({ role: "admin", name: "Admin" });
    render(
      <AdminLayout>
        <div>Content</div>
      </AdminLayout>
    );
    await waitFor(() => {
      expect(screen.getAllByText("Bookings").length).toBeGreaterThanOrEqual(1);
      expect(screen.getAllByText("Availability").length).toBeGreaterThanOrEqual(1);
      expect(screen.getAllByText("Payments").length).toBeGreaterThanOrEqual(1);
    });
  });

  it("shows logout button for admin", async () => {
    mockGetToken.mockReturnValue("admin-token");
    mockAuthMe.mockResolvedValue({ role: "admin", name: "Admin" });
    render(
      <AdminLayout>
        <div>Content</div>
      </AdminLayout>
    );
    await waitFor(() => {
      expect(screen.getAllByText("Logout").length).toBeGreaterThanOrEqual(1);
    });
  });

  it("clears tokens and redirects on logout click", async () => {
    mockGetToken.mockReturnValue("admin-token");
    mockAuthMe.mockResolvedValue({ role: "admin", name: "Admin" });
    render(
      <AdminLayout>
        <div>Content</div>
      </AdminLayout>
    );
    await waitFor(() => {
      expect(screen.getAllByText("Logout").length).toBeGreaterThanOrEqual(1);
    });
    // Click the first Logout button
    fireEvent.click(screen.getAllByText("Logout")[0]);
    expect(mockClearTokens).toHaveBeenCalled();
    expect(mockPush).toHaveBeenCalledWith("/admin/login");
  });

  it("redirects non-admin users to login", async () => {
    mockGetToken.mockReturnValue("user-token");
    mockAuthMe.mockResolvedValue({ role: "user", name: "User" });
    render(
      <AdminLayout>
        <div>Content</div>
      </AdminLayout>
    );
    await waitFor(() => {
      expect(mockClearTokens).toHaveBeenCalled();
      expect(mockPush).toHaveBeenCalledWith("/admin/login");
    });
  });
});
