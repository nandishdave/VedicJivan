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
    let message: string;
    if (typeof error.detail === "string") {
      message = error.detail;
    } else if (Array.isArray(error.detail)) {
      // FastAPI validation errors: [{loc, msg, type}, ...]
      message = error.detail.map((e: { msg?: string }) => e.msg || "Validation error").join("; ");
    } else {
      message = error.message || `HTTP ${response.status}`;
    }
    throw new Error(message);
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

export interface DayHours {
  day: number; // 0=Mon, 1=Tue, ..., 6=Sun
  is_open: boolean;
  open_time: string; // "HH:MM"
  close_time: string; // "HH:MM"
}

export interface BusinessHoursSettings {
  timezone: string;
  weekly_hours: DayHours[];
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

  getSettings: () =>
    apiRequest<BusinessHoursSettings>("/api/availability/settings"),

  updateSettings: (data: BusinessHoursSettings, token: string) =>
    apiRequest<BusinessHoursSettings>("/api/availability/settings", {
      method: "PUT",
      body: data,
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
  price_eur: number;
  status: "pending" | "confirmed" | "completed" | "cancelled";
  payment_id: string | null;
  notes: string;
  created_at: string;
  date_of_birth: string;
  time_of_birth: string | null;
  birth_time_unknown: boolean;
  place_of_birth: string;
  birth_latitude: number;
  birth_longitude: number;
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
    notes: string;
    date_of_birth: string;
    time_of_birth: string | null;
    birth_time_unknown: boolean;
    place_of_birth: string;
    birth_latitude: number;
    birth_longitude: number;
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

  resume: (id: string) =>
    apiRequest<Booking>(`/api/bookings/${id}/resume`),

  view: (id: string) =>
    apiRequest<Booking>(`/api/bookings/${id}/view`),

  reschedule: (id: string, data: { date: string; time_slot: string; duration_minutes: number }) =>
    apiRequest<Booking>(`/api/bookings/${id}/reschedule`, {
      method: "PATCH",
      body: data,
    }),
};

// ── Payments ──
export const paymentsApi = {
  createCheckoutSession: (data: { booking_id: string; currency?: string }) =>
    apiRequest<{ checkout_url: string }>("/api/payments/create-checkout-session", {
      method: "POST",
      body: data,
    }),

  getSessionStatus: (sessionId: string, bookingId: string) =>
    apiRequest<{
      payment_status: string;
      booking_status: string;
      booking?: {
        service_title: string;
        date: string;
        time_slot: string;
        duration_minutes: number;
        price_inr: number;
        user_name: string;
        user_email: string;
      };
    }>(`/api/payments/session-status?session_id=${sessionId}&booking_id=${bookingId}`),

  list: (token: string) =>
    apiRequest<
      {
        id: string;
        booking_id: string;
        stripe_session_id: string;
        stripe_payment_intent_id: string | null;
        amount: number;
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
      daily_bookings: { date: string; bookings: number }[];
      daily_revenue: { date: string; revenue: number }[];
    }>("/api/admin/stats", { token }),
};
