const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Abort a request that stalls past this, so the UI never hangs forever on a
// dropped connection. Overridable per call via RequestOptions.timeoutMs.
const DEFAULT_TIMEOUT_MS = 15000;
const RETRY_DELAY_MS = 400;

interface RequestOptions {
  method?: string;
  body?: unknown;
  token?: string;
  timeoutMs?: number;
}

const _delay = (ms: number) => new Promise((r) => setTimeout(r, ms));
const _isAbort = (err: unknown) => err instanceof DOMException && err.name === "AbortError";

/** One fetch attempt with an AbortController-backed timeout. */
async function _fetchWithTimeout(
  url: string,
  init: RequestInit,
  timeoutMs: number
): Promise<Response> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    return await fetch(url, { ...init, signal: controller.signal });
  } finally {
    clearTimeout(timer);
  }
}

export async function apiRequest<T>(
  endpoint: string,
  options: RequestOptions = {}
): Promise<T> {
  const { method = "GET", body, token, timeoutMs = DEFAULT_TIMEOUT_MS } = options;

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const url = `${API_URL}${endpoint}`;
  const init: RequestInit = {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  };

  // Retry transport failures (network drop / timeout) once — but only for GET,
  // which is idempotent. A server that DID respond (any status, incl. 5xx) is
  // handled below without a retry, so non-idempotent writes never double-fire.
  const maxAttempts = method === "GET" ? 2 : 1;

  let response: Response | undefined;
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      response = await _fetchWithTimeout(url, init, timeoutMs);
      break;
    } catch (err) {
      if (attempt < maxAttempts) {
        await _delay(RETRY_DELAY_MS);
        continue;
      }
      throw new Error(
        _isAbort(err)
          ? "Request timed out. Please try again."
          : "Network error. Please check your connection and try again."
      );
    }
  }
  // maxAttempts >= 1, so the loop either assigned `response` or threw above.
  const res = response as Response;

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: "Request failed" }));
    let message: string;
    if (typeof error.detail === "string") {
      message = error.detail;
    } else if (Array.isArray(error.detail)) {
      // FastAPI validation errors: [{loc, msg, type}, ...]
      message = error.detail.map((e: { msg?: string }) => e.msg || "Validation error").join("; ");
    } else {
      message = error.message || `HTTP ${res.status}`;
    }
    throw new Error(message);
  }

  return res.json();
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

export interface ReportSection {
  id: string;
  label: string;
  description: string;
  is_paid: boolean;
  enabled: boolean;
  order: number;
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

  getReportSections: () =>
    apiRequest<ReportSection[]>("/api/availability/settings/report-sections"),

  updateReportSections: (sections: ReportSection[], token: string) =>
    apiRequest<ReportSection[]>("/api/availability/settings/report-sections", {
      method: "PUT",
      body: sections,
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

// ── Kundli ──
export const kundliApi = {
  generate: (data: {
    name: string;
    gender: string;
    dob: string;
    tob: string;
    lat: number;
    lon: number;
    place_name: string;
    email: string;
    timezone?: string;
  }) =>
    apiRequest<{ message: string }>("/api/kundli/generate", {
      method: "POST",
      body: data,
    }),

  // Per-planet Vimśopaka Bala (0-20) — read-only, no email, no DB write.
  vimsopaka: (data: { dob: string; tob: string; lat: number; lon: number }) => {
    const q = new URLSearchParams({
      dob: data.dob,
      tob: data.tob,
      lat: String(data.lat),
      lon: String(data.lon),
    });
    return apiRequest<VimsopakaResult>(`/api/kundli/vimsopaka?${q.toString()}`);
  },

  // Auspicious/poison degree analysis — Pushkara/Vish Navāṁśa + Pushkara/Mṛtyu Bhāga.
  degreeAnalysis: (data: { dob: string; tob: string; lat: number; lon: number }) => {
    const q = new URLSearchParams({
      dob: data.dob,
      tob: data.tob,
      lat: String(data.lat),
      lon: String(data.lon),
    });
    return apiRequest<DegreeAnalysisResult>(`/api/kundli/degree-analysis?${q.toString()}`);
  },

  argalaAnalysis: (data: { dob: string; tob: string; lat: number; lon: number }) => {
    const q = new URLSearchParams({
      dob: data.dob,
      tob: data.tob,
      lat: String(data.lat),
      lon: String(data.lon),
    });
    return apiRequest<ArgalaResult>(`/api/kundli/argala-analysis?${q.toString()}`);
  },

  ashtakavarga: (data: { dob: string; tob: string; lat: number; lon: number }) => {
    const q = new URLSearchParams({
      dob: data.dob,
      tob: data.tob,
      lat: String(data.lat),
      lon: String(data.lon),
    });
    return apiRequest<AshtakavargaResult>(`/api/kundli/ashtakavarga?${q.toString()}`);
  },

  shadbala: (data: { dob: string; tob: string; lat: number; lon: number }) => {
    const q = new URLSearchParams({
      dob: data.dob,
      tob: data.tob,
      lat: String(data.lat),
      lon: String(data.lon),
    });
    return apiRequest<ShadbalaResult>(`/api/kundli/shadbala?${q.toString()}`);
  },

  divisionalCharts: (data: {
    dob: string;
    tob: string;
    lat: number;
    lon: number;
    upagrahas?: boolean;
  }) => {
    const q = new URLSearchParams({
      dob: data.dob,
      tob: data.tob,
      lat: String(data.lat),
      lon: String(data.lon),
    });
    if (data.upagrahas) q.set("upagrahas", "true");
    return apiRequest<DivisionalResult>(`/api/kundli/divisional-charts?${q.toString()}`);
  },

  upagraha: (data: { dob: string; tob: string; lat: number; lon: number }) => {
    const q = new URLSearchParams({
      dob: data.dob,
      tob: data.tob,
      lat: String(data.lat),
      lon: String(data.lon),
    });
    return apiRequest<UpagrahaResult>(`/api/kundli/upagraha?${q.toString()}`);
  },
};

// ── Vimśopaka Bala calculator ──
export interface VimsopakaPlanet {
  vimsopaka: number;
  band: string;
  house: number;
  sign: string;
  is_node?: boolean; // Rāhu/Ketu — display only, excluded from average + strongest
  is_outer?: boolean; // Uranus/Neptune/Pluto — display only, excluded too
}

export interface VimsopakaResult {
  lagna: string;
  planets: Record<string, VimsopakaPlanet>;
  strongest: {
    planet: string;
    vimsopaka: number;
    house: number;
    in_prominence_seat: boolean;
  };
  average: number;
}

// ── Auspicious/poison degree calculator ──
export interface DegreeBody {
  body: string;
  sign: string;
  degree: number;
  navamsa: number;
  pushkara_navamsa: boolean;
  pushkara_bhaga: boolean;
  vish_navamsa: boolean;
  mrityu_bhaga: boolean | null; // null for the outer planets (no classical table)
}

export interface DegreeAnalysisResult {
  bodies: DegreeBody[];
  totals: {
    pushkara_navamsa: number;
    pushkara_bhaga: number;
    vish_navamsa: number;
    mrityu_bhaga: number;
  };
}

// ── Argala (Jaimini intervention) calculator ──
export interface ArgalaArgRow {
  planet: string;
  from_house: number; // sits in the 2/4/5/11 from the reference house
  sign: string; // sign of the house it locks
  dignity: string; // dignity of the planet in that sign
  dignity_score: number; // +2 exalted … −2 debilitated (layers 1–5)
  role_fit: number; // +1 / 0 / −1 by natural nature × house type (layers 6–9)
  shadbala: number;
  polarity: number; // dignity_score + role_fit
  contribution: number; // shadbala × polarity × survive
}

export interface ArgalaVirodha {
  planet: string;
  shadbala: number;
}

export interface ArgalaPair {
  argala_from: number; // 2/4/5/11
  virodha_from: number; // 12/10/9/3
  argala_shadbala: number;
  virodha_shadbala: number;
  survive: number; // 0..1 — fraction of the argala left after the counter
  argala: ArgalaArgRow[];
  virodha: ArgalaVirodha[];
}

export type ArgalaVerdict = "null" | "neutral" | "positive" | "negative";

export interface ArgalaHouse {
  house: number;
  strength: number; // -100..+100; sign drives the colour (green +, red -)
  verdict: ArgalaVerdict;
  positive: string[]; // planets whose surviving argala helps the house
  negative: string[]; // planets whose surviving argala harms the house
  pos_weight: number;
  neg_weight: number;
  pairs: ArgalaPair[];
}

export interface ArgalaPosition {
  body: string; // Ascendant + 9 grahas + Uranus/Neptune/Pluto
  sign: string;
  degree: number; // degree within the sign
  house: number;
  retrograde: boolean;
}

export interface ArgalaResult {
  positions: ArgalaPosition[];
  houses: ArgalaHouse[];
  shadbala_used: boolean;
  lagna_sign: number;
}

// ── Ashtakavarga calculator ──
export interface AvHouse {
  house: number;
  sign: string;
  sav: number; // Sarvashtakavarga bindus for this house (baseline 28)
}

export interface AvBav {
  planet: string;
  total: number; // fixed classical total (Sun 48, Moon 49, …)
  per_house: number[]; // Bhinnashtakavarga bindus per house 1..12 (each 0–8)
}

export interface AvPrastharRow {
  contributor: string; // Su/Mo/Ma/Me/Ju/Ve/Sa/As
  cells: number[]; // 0/1 per sign (Aries…Pisces)
  total: number; // row sum
}

export interface AvPrasthar {
  planet: string;
  rows: AvPrastharRow[]; // 8 contributor rows
  column_totals: number[]; // = this planet's BAV by sign
}

export interface AshtakavargaResult {
  lagna_sign: number;
  grand_total: number; // 337
  signs: string[]; // sign abbreviations for the Prastara columns
  houses: AvHouse[];
  bav: AvBav[];
  prasthar: AvPrasthar[];
}

// ── Shadbala calculator ──
export interface SbBalas {
  sthana: number;
  dig: number;
  kala: number;
  cheshta: number;
  naisargika: number;
  drik: number;
}

export interface SbPlanet {
  planet: string;
  method: "classical" | "adapted" | "dispositor";
  via: string | null; // dispositor lord for Rahu/Ketu (else null)
  rank: number;
  balas: SbBalas; // the six balas, in Rupas
  total: number; // Rupas (sum of the six)
  required: number; // classical minimum, Rupas
  ratio: number; // total / required
  sufficient: boolean; // ratio >= 1
  sthana_parts: Record<string, number>; // 5 sub-balas of Sthana
  kala_parts: Record<string, number>; // 9 sub-balas of Kala
}

export interface ShadbalaResult {
  planets: SbPlanet[];
}

// ── Divisional Charts calculator ──
export interface DvVarga {
  key: string; // D1, D2, … D60
  name: string; // e.g. "Navāṁśa (spouse/dharma)"
}

export interface DvBody {
  body: string; // Ascendant + grahas + outer (+ upagrahas when toggled)
  signs: string[]; // sign abbreviation per varga (aligned with vargas[])
  is_upagraha?: boolean; // true for the folded-in sub-planet rows
}

export interface DivisionalResult {
  vargas: DvVarga[];
  bodies: DvBody[];
}

// ── Upagrahas (sub-planets) ──
export interface UpagrahaRow {
  name: string;
  label: string;
  abbr: string;
  sign: number;
  sign_abbr: string;
  degree: number;
  dms: string;
  nakshatra: string;
  pada: number;
}

export interface UpagrahaResult {
  upagrahas: UpagrahaRow[];
  by_sign: Record<string, string[]>;
  lagna_sign: number;
}

// ── Muhurta (Auspicious Birth-Time) ──
export type MuhurtaVerdict = "good" | "moderate" | "challenging";

export interface MuhurtaAspect {
  label: string;
  group: string;
  score: number;
  verdict: MuhurtaVerdict;
}

export interface MuhurtaWorldly {
  score: number;
  mean_z: number;
  factors: Record<string, { value: number; z: number }>;
  note: string;
}

export interface MuhurtaWindow {
  rank: number;
  lagna_sign: number;
  lagna_name: string;
  lagna_lord: string;
  lord_retrograde: boolean;
  window: { start: string; end: string; mid: string };
  overall: number;
  rank_score: number;
  highlighted: boolean;
  // Faint (~0.63 AUC) worldly-prominence-potential readout; null if unavailable.
  worldly_potential: MuhurtaWorldly | null;
  panchanga: { nakshatra: string; tithi: string; yoga: string; paksha: string };
  aspects: Record<string, MuhurtaAspect>;
}

export interface MuhurtaPlanet {
  planet: string;
  sign: string;
  sign_num: number;
  degree: number;
  degree_dms: string;
  retrograde: boolean;
  motion: string;
}

export interface MuhurtaResult {
  date: string;
  place_name: string;
  lat: number;
  lon: number;
  priorities: string[];
  optimize_prominence: boolean;
  query_time: string | null;
  highlight_lagna: string | null;
  planet_positions: MuhurtaPlanet[];
  positions_time: string;
  aspects_config: { key: string; label: string; group: string }[];
  windows: MuhurtaWindow[];
}

export const muhurtaApi = {
  // The full analysis is slow, so the backend runs it async and emails the
  // result; this returns a 202 acknowledgement, not the analysis itself.
  analyzeBirth: (data: {
    date: string;
    lat: number;
    lon: number;
    place_name: string;
    email: string;
    time?: string | null;
    priorities?: string[] | null;
    optimize_prominence?: boolean;
  }) =>
    apiRequest<{ message: string }>("/api/muhurta/birth", { method: "POST", body: data }),
};

// ── Unshakable Chart Finder ──
export const unshakableApi = {
  // Heavy scan: the backend runs it async and emails the ranked results.
  find: (data: {
    start_date: string;
    days: number;
    lat: number;
    lon: number;
    place_name: string;
    email: string;
  }) =>
    apiRequest<{ message: string }>("/api/unshakable/find", { method: "POST", body: data }),
};
