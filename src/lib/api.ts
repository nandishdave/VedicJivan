const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface RequestOptions {
  method?: string;
  body?: unknown;
  token?: string;
}

export async function apiRequest<T>(
  endpoint: string,
  options: RequestOptions = {}
): Promise<T> {
  const { method = "GET", body, token } = options;

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json();
}

// ── Auth ──
export const authApi = {
  register: (data: { name: string; email: string; password: string; phone: string }) =>
    apiRequest<{ access_token: string; refresh_token: string }>("/api/auth/register", {
      method: "POST",
      body: data,
    }),

  login: (data: { email: string; password: string }) =>
    apiRequest<{ access_token: string; refresh_token: string }>("/api/auth/login", {
      method: "POST",
      body: data,
    }),

  me: (token: string) =>
    apiRequest<{
      id: string;
      name: string;
      email: string;
      phone: string;
      role: string;
    }>("/api/auth/me", { token }),
};

// ── Availability ──
export interface AvailableSlot {
  start: string;
  end: string;
}

export interface Unavailability {
  id: string;
  date: string;
  start_time: string | null;
  end_time: string | null;
  is_holiday: boolean;
  reason: string;
}

export const availabilityApi = {
  getSlots: (date: string) =>
    apiRequest<AvailableSlot[]>(`/api/availability/slots?date=${date}`),

  getHolidays: (start: string, end: string) =>
    apiRequest<string[]>(`/api/availability/holidays?start=${start}&end=${end}`),

  getUnavailable: (date: string) =>
    apiRequest<Unavailability[]>(`/api/availability/unavailable?date=${date}`),

  getUnavailableRange: (start: string, end: string) =>
    apiRequest<Unavailability[]>(
      `/api/availability/unavailable/range?start=${start}&end=${end}`
    ),

  addUnavailable: (
    data: {
      date: string;
      start_time?: string;
      end_time?: string;
      is_holiday?: boolean;
      reason?: string;
    },
    token: string
  ) =>
    apiRequest<Unavailability>("/api/availability/unavailable", {
      method: "POST",
      body: data,
      token,
    }),

  removeUnavailable: (id: string, token: string) =>
    apiRequest<{ message: string }>(`/api/availability/unavailable/${id}`, {
      method: "DELETE",
      token,
    }),
};

// ── Bookings ──
export interface Booking {
  id: string;
  user_name: string;
  user_email: string;
  user_phone: string;
  service_slug: string;
  service_title: string;
  date: string;
  time_slot: string;
  duration_minutes: number;
  price_inr: number;
  status: "pending" | "confirmed" | "completed" | "cancelled";
  payment_id: string | null;
  notes: string;
  created_at: string;
}

export const bookingsApi = {
  create: (data: {
    service_slug: string;
    service_title: string;
    date: string;
    time_slot: string;
    duration_minutes: number;
    user_name: string;
    user_email: string;
    user_phone: string;
    notes?: string;
  }) =>
    apiRequest<Booking>("/api/bookings", { method: "POST", body: data }),

  list: (token: string, params?: { status?: string; date?: string }) => {
    const query = new URLSearchParams();
    if (params?.status) query.set("status", params.status);
    if (params?.date) query.set("date", params.date);
    const qs = query.toString();
    return apiRequest<Booking[]>(`/api/bookings${qs ? `?${qs}` : ""}`, { token });
  },

  getById: (id: string, token: string) =>
    apiRequest<Booking>(`/api/bookings/${id}`, { token }),

  cancel: (id: string, token: string) =>
    apiRequest<Booking>(`/api/bookings/${id}/cancel`, { method: "PATCH", token }),

  updateStatus: (id: string, status: string, token: string) =>
    apiRequest<Booking>(`/api/bookings/${id}/status`, {
      method: "PATCH",
      body: { status },
      token,
    }),
};

// ── Payments ──
export const paymentsApi = {
  createOrder: (data: { booking_id: string; amount_inr: number }) =>
    apiRequest<{
      order_id: string;
      amount: number;
      currency: string;
      key_id: string;
    }>("/api/payments/create-order", { method: "POST", body: data }),

  verify: (data: {
    razorpay_order_id: string;
    razorpay_payment_id: string;
    razorpay_signature: string;
    booking_id: string;
  }) =>
    apiRequest<{ status: string; message: string }>("/api/payments/verify", {
      method: "POST",
      body: data,
    }),

  list: (token: string) =>
    apiRequest<
      {
        id: string;
        booking_id: string;
        razorpay_order_id: string;
        razorpay_payment_id: string | null;
        amount_inr: number;
        currency: string;
        status: string;
        created_at: string;
      }[]
    >("/api/payments", { token }),
};

// ── Admin ──
export const adminApi = {
  dashboard: (token: string) =>
    apiRequest<{
      today_bookings: number;
      upcoming_bookings: number;
      total_revenue: number;
      bookings_by_status: Record<string, number>;
      recent_bookings: {
        id: string;
        user_name: string;
        service_title: string;
        date: string;
        time_slot: string;
        status: string;
        price_inr: number;
      }[];
    }>("/api/admin/dashboard", { token }),

  stats: (token: string) =>
    apiRequest<{
      total_users: number;
      total_bookings: number;
      total_payments: number;
      revenue_by_service: {
        service: string;
        bookings: number;
        revenue: number;
      }[];
    }>("/api/admin/stats", { token }),
};
