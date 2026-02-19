import { describe, it, expect, vi, beforeEach } from "vitest";
import {
  apiRequest,
  authApi,
  availabilityApi,
  bookingsApi,
  paymentsApi,
  adminApi,
} from "@/lib/api";

describe("apiRequest", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it("makes a GET request by default", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ data: "ok" }),
    });
    vi.stubGlobal("fetch", fetchMock);

    await apiRequest("/api/test");

    expect(fetchMock).toHaveBeenCalledWith(
      expect.stringContaining("/api/test"),
      expect.objectContaining({ method: "GET" })
    );
  });

  it("includes Authorization header when token is provided", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({}),
    });
    vi.stubGlobal("fetch", fetchMock);

    await apiRequest("/api/test", { token: "my-token" });

    const callArgs = fetchMock.mock.calls[0][1];
    expect(callArgs.headers.Authorization).toBe("Bearer my-token");
  });

  it("does not include Authorization header without token", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({}),
    });
    vi.stubGlobal("fetch", fetchMock);

    await apiRequest("/api/test");

    const callArgs = fetchMock.mock.calls[0][1];
    expect(callArgs.headers.Authorization).toBeUndefined();
  });

  it("sends JSON body for POST requests", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({}),
    });
    vi.stubGlobal("fetch", fetchMock);

    await apiRequest("/api/test", { method: "POST", body: { name: "test" } });

    const callArgs = fetchMock.mock.calls[0][1];
    expect(callArgs.body).toBe('{"name":"test"}');
    expect(callArgs.headers["Content-Type"]).toBe("application/json");
  });

  it("throws error with detail from response", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: false,
      status: 400,
      json: () => Promise.resolve({ detail: "Bad request" }),
    });
    vi.stubGlobal("fetch", fetchMock);

    await expect(apiRequest("/api/test")).rejects.toThrow("Bad request");
  });

  it("throws HTTP status when no detail in response", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: false,
      status: 500,
      json: () => Promise.reject(new Error("not json")),
    });
    vi.stubGlobal("fetch", fetchMock);

    await expect(apiRequest("/api/test")).rejects.toThrow("Request failed");
  });

  it("does not send body for GET requests", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({}),
    });
    vi.stubGlobal("fetch", fetchMock);

    await apiRequest("/api/test");

    const callArgs = fetchMock.mock.calls[0][1];
    expect(callArgs.body).toBeUndefined();
  });
});

describe("authApi", () => {
  beforeEach(() => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve({ access_token: "a", refresh_token: "r" }),
      })
    );
  });

  it("register calls POST /api/auth/register", async () => {
    await authApi.register({ name: "John", email: "j@t.com", password: "pass123", phone: "123" });
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/api/auth/register"),
      expect.objectContaining({ method: "POST" })
    );
  });

  it("login calls POST /api/auth/login", async () => {
    await authApi.login({ email: "j@t.com", password: "pass" });
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/api/auth/login"),
      expect.objectContaining({ method: "POST" })
    );
  });

  it("me calls GET /api/auth/me with token", async () => {
    await authApi.me("token123");
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/api/auth/me"),
      expect.objectContaining({
        method: "GET",
        headers: expect.objectContaining({ Authorization: "Bearer token123" }),
      })
    );
  });
});

describe("availabilityApi", () => {
  beforeEach(() => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve([]),
      })
    );
  });

  it("getSlots calls correct endpoint with date", async () => {
    await availabilityApi.getSlots("2026-03-15");
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/api/availability/slots?date=2026-03-15"),
      expect.anything()
    );
  });

  it("getHolidays calls correct endpoint with date range", async () => {
    await availabilityApi.getHolidays("2026-03-01", "2026-03-31");
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/api/availability/holidays?start=2026-03-01&end=2026-03-31"),
      expect.anything()
    );
  });

  it("getUnavailable calls correct endpoint", async () => {
    await availabilityApi.getUnavailable("2026-03-15");
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/api/availability/unavailable?date=2026-03-15"),
      expect.anything()
    );
  });

  it("getUnavailableRange calls correct endpoint", async () => {
    await availabilityApi.getUnavailableRange("2026-03-01", "2026-03-31");
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/api/availability/unavailable/range?start=2026-03-01&end=2026-03-31"),
      expect.anything()
    );
  });

  it("addUnavailable calls POST with token", async () => {
    await availabilityApi.addUnavailable(
      { date: "2026-03-15", is_holiday: true },
      "admin-token"
    );
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/api/availability/unavailable"),
      expect.objectContaining({
        method: "POST",
        headers: expect.objectContaining({ Authorization: "Bearer admin-token" }),
      })
    );
  });

  it("removeUnavailable calls DELETE with token", async () => {
    await availabilityApi.removeUnavailable("abc123", "admin-token");
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/api/availability/unavailable/abc123"),
      expect.objectContaining({
        method: "DELETE",
        headers: expect.objectContaining({ Authorization: "Bearer admin-token" }),
      })
    );
  });
});

describe("bookingsApi", () => {
  beforeEach(() => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve({}),
      })
    );
  });

  it("create calls POST /api/bookings", async () => {
    await bookingsApi.create({
      service_slug: "call-consultation",
      service_title: "Call",
      date: "2026-03-15",
      time_slot: "10:00",
      duration_minutes: 30,
      user_name: "John",
      user_email: "j@t.com",
      user_phone: "123",
    });
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/api/bookings"),
      expect.objectContaining({ method: "POST" })
    );
  });

  it("list calls GET /api/bookings with token", async () => {
    await bookingsApi.list("token");
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/api/bookings"),
      expect.objectContaining({
        headers: expect.objectContaining({ Authorization: "Bearer token" }),
      })
    );
  });

  it("list appends query params for status filter", async () => {
    await bookingsApi.list("token", { status: "pending" });
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("status=pending"),
      expect.anything()
    );
  });

  it("getById calls GET /api/bookings/:id", async () => {
    await bookingsApi.getById("b123", "token");
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/api/bookings/b123"),
      expect.anything()
    );
  });

  it("cancel calls PATCH /api/bookings/:id/cancel", async () => {
    await bookingsApi.cancel("b123", "token");
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/api/bookings/b123/cancel"),
      expect.objectContaining({ method: "PATCH" })
    );
  });

  it("updateStatus calls PATCH with body", async () => {
    await bookingsApi.updateStatus("b123", "confirmed", "token");
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/api/bookings/b123/status"),
      expect.objectContaining({
        method: "PATCH",
        body: expect.stringContaining("confirmed"),
      })
    );
  });
});

describe("paymentsApi", () => {
  beforeEach(() => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve({}),
      })
    );
  });

  it("createOrder calls POST /api/payments/create-order", async () => {
    await paymentsApi.createOrder({ booking_id: "b1", amount_inr: 1999 });
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/api/payments/create-order"),
      expect.objectContaining({ method: "POST" })
    );
  });

  it("verify calls POST /api/payments/verify", async () => {
    await paymentsApi.verify({
      razorpay_order_id: "o1",
      razorpay_payment_id: "p1",
      razorpay_signature: "sig",
      booking_id: "b1",
    });
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/api/payments/verify"),
      expect.objectContaining({ method: "POST" })
    );
  });

  it("list calls GET /api/payments with token", async () => {
    await paymentsApi.list("token");
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/api/payments"),
      expect.objectContaining({
        headers: expect.objectContaining({ Authorization: "Bearer token" }),
      })
    );
  });
});

describe("adminApi", () => {
  beforeEach(() => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve({}),
      })
    );
  });

  it("dashboard calls GET /api/admin/dashboard with token", async () => {
    await adminApi.dashboard("admin-token");
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/api/admin/dashboard"),
      expect.objectContaining({
        headers: expect.objectContaining({ Authorization: "Bearer admin-token" }),
      })
    );
  });

  it("stats calls GET /api/admin/stats with token", async () => {
    await adminApi.stats("admin-token");
    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("/api/admin/stats"),
      expect.objectContaining({
        headers: expect.objectContaining({ Authorization: "Bearer admin-token" }),
      })
    );
  });
});
