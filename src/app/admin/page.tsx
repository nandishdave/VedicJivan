"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import {
  Calendar,
  CreditCard,
  Clock,
  Users,
  TrendingUp,
  Settings,
  BarChart3,
} from "lucide-react";
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";
import { adminApi, authApi } from "@/lib/api";
import { getToken, clearTokens } from "@/lib/auth";
import { useTheme } from "@/components/ui/ThemeProvider";

interface DashboardData {
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
}

interface StatsData {
  total_users: number;
  total_bookings: number;
  total_payments: number;
  revenue_by_service: { service: string; bookings: number; revenue: number }[];
  daily_bookings: { date: string; bookings: number }[];
  daily_revenue: { date: string; revenue: number }[];
}

const STATUS_COLORS: Record<string, string> = {
  pending: "#f59e0b",
  confirmed: "#22c55e",
  completed: "#3b82f6",
  cancelled: "#ef4444",
};

const STATUS_BADGE_COLORS: Record<string, string> = {
  pending: "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/20 dark:text-yellow-300",
  confirmed: "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300",
  completed: "bg-blue-100 text-blue-700 dark:bg-blue-900/20 dark:text-blue-300",
  cancelled: "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300",
};

const SERVICE_COLORS = ["#8b5cf6", "#06b6d4", "#f59e0b", "#ef4444", "#22c55e", "#ec4899"];

function formatShortDate(dateStr: string) {
  const d = new Date(dateStr + "T00:00:00");
  return d.toLocaleDateString("en-IN", { day: "numeric", month: "short" });
}

export default function AdminDashboard() {
  const router = useRouter();
  const { resolvedTheme } = useTheme();
  const [data, setData] = useState<DashboardData | null>(null);
  const [stats, setStats] = useState<StatsData | null>(null);
  const [userName, setUserName] = useState("");
  const [loading, setLoading] = useState(true);

  const isDark = resolvedTheme === "dark";
  const gridStroke = isDark ? "#2a2535" : "#f0f0f0";
  const tickFill = isDark ? "#9ca3af" : "#6b7280";
  const tooltipStyle = isDark
    ? { backgroundColor: "#1e1730", border: "1px solid rgba(255,255,255,0.1)", color: "#e5e7eb" }
    : {};

  useEffect(() => {
    const token = getToken();
    if (!token) {
      router.push("/admin/login");
      return;
    }

    const fetchData = async () => {
      try {
        const [user, dashboard, statsData] = await Promise.all([
          authApi.me(token),
          adminApi.dashboard(token),
          adminApi.stats(token),
        ]);

        if (user.role !== "admin") {
          router.push("/admin/login");
          return;
        }

        setUserName(user.name);
        setData(dashboard);
        setStats(statsData);
      } catch {
        clearTokens();
        router.push("/admin/login");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [router]);

  if (loading) {
    return (
      <section className="min-h-screen bg-gray-50 dark:bg-dark-surface py-[var(--space-lg)]">
        <div className="mx-auto max-w-6xl px-[var(--space-md)]">
          <div className="animate-pulse space-y-6">
            <div className="h-8 w-48 rounded bg-gray-200 dark:bg-gray-700" />
            <div className="grid gap-[var(--space-sm)] sm:grid-cols-2 lg:grid-cols-4">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="h-24 rounded-xl bg-gray-200 dark:bg-gray-700" />
              ))}
            </div>
            <div className="grid gap-[var(--space-sm)] lg:grid-cols-2">
              <div className="h-72 rounded-xl bg-gray-200 dark:bg-gray-700" />
              <div className="h-72 rounded-xl bg-gray-200 dark:bg-gray-700" />
            </div>
          </div>
        </div>
      </section>
    );
  }

  if (!data) return null;

  // Prepare chart data
  const statusData = Object.entries(data.bookings_by_status).map(([name, value]) => ({
    name: name.charAt(0).toUpperCase() + name.slice(1),
    value,
    color: STATUS_COLORS[name] || "#9ca3af",
  }));

  const totalBookingsCount = Object.values(data.bookings_by_status).reduce((a, b) => a + b, 0);

  return (
    <section className="min-h-screen bg-gray-50 dark:bg-dark-surface py-[var(--space-lg)]">
      <div className="mx-auto max-w-6xl px-[var(--space-md)]">
        {/* Header */}
        <div className="mb-[var(--space-lg)]">
          <h1 className="font-heading text-[var(--text-xl)] font-bold text-vedic-dark dark:text-gray-100">
            Dashboard
          </h1>
          <p className="text-[var(--text-sm)] text-gray-500">Welcome back, {userName}</p>
        </div>

        {/* Stats cards */}
        <div className="mb-[var(--space-lg)] grid gap-[var(--space-sm)] sm:grid-cols-2 lg:grid-cols-4">
          <div className="rounded-xl border border-gray-200 dark:border-gray-600 bg-white dark:bg-dark-surface-card p-[var(--space-md)]">
            <div className="flex items-center gap-[var(--space-sm)]">
              <div className="rounded-lg bg-blue-100 dark:bg-blue-900/20 p-2">
                <Calendar className="h-5 w-5 text-blue-600" />
              </div>
              <div>
                <p className="text-2xl font-bold">{data.today_bookings}</p>
                <p className="text-[var(--text-sm)] text-gray-500">Today&apos;s Bookings</p>
              </div>
            </div>
          </div>
          <div className="rounded-xl border border-gray-200 dark:border-gray-600 bg-white dark:bg-dark-surface-card p-[var(--space-md)]">
            <div className="flex items-center gap-[var(--space-sm)]">
              <div className="rounded-lg bg-green-100 dark:bg-green-900/30 p-2">
                <Clock className="h-5 w-5 text-green-600" />
              </div>
              <div>
                <p className="text-2xl font-bold">{data.upcoming_bookings}</p>
                <p className="text-[var(--text-sm)] text-gray-500">Upcoming</p>
              </div>
            </div>
          </div>
          <div className="rounded-xl border border-gray-200 dark:border-gray-600 bg-white dark:bg-dark-surface-card p-[var(--space-md)]">
            <div className="flex items-center gap-[var(--space-sm)]">
              <div className="rounded-lg bg-purple-100 dark:bg-purple-900/20 p-2">
                <TrendingUp className="h-5 w-5 text-purple-600" />
              </div>
              <div>
                <p className="text-2xl font-bold">{"\u20B9"}{data.total_revenue.toLocaleString()}</p>
                <p className="text-[var(--text-sm)] text-gray-500">Total Revenue</p>
              </div>
            </div>
          </div>
          <div className="rounded-xl border border-gray-200 dark:border-gray-600 bg-white dark:bg-dark-surface-card p-[var(--space-md)]">
            <div className="flex items-center gap-[var(--space-sm)]">
              <div className="rounded-lg bg-yellow-100 dark:bg-yellow-900/20 p-2">
                <Users className="h-5 w-5 text-yellow-600" />
              </div>
              <div>
                <p className="text-2xl font-bold">{totalBookingsCount}</p>
                <p className="text-[var(--text-sm)] text-gray-500">Total Bookings</p>
              </div>
            </div>
          </div>
        </div>

        {/* Charts row 1: Bookings trend + Revenue trend */}
        {stats && (
          <div className="mb-[var(--space-lg)] grid gap-[var(--space-sm)] lg:grid-cols-2">
            {/* Bookings trend - last 30 days */}
            <div className="rounded-xl border border-gray-200 dark:border-gray-600 bg-white dark:bg-dark-surface-card p-[var(--space-md)]">
              <h2 className="mb-[var(--space-sm)] flex items-center gap-2 font-heading text-[var(--text-base)] font-semibold">
                <BarChart3 className="h-4 w-4 text-blue-600" />
                Bookings (Last 30 Days)
              </h2>
              <div className="h-56">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={stats.daily_bookings}>
                    <CartesianGrid strokeDasharray="3 3" stroke={gridStroke} />
                    <XAxis
                      dataKey="date"
                      tickFormatter={formatShortDate}
                      tick={{ fontSize: 11, fill: tickFill }}
                      interval="preserveStartEnd"
                    />
                    <YAxis allowDecimals={false} tick={{ fontSize: 11, fill: tickFill }} width={30} />
                    <Tooltip
                      labelFormatter={(label) => formatShortDate(label as string)}
                      formatter={(value) => [Number(value), "Bookings"]}
                      contentStyle={tooltipStyle}
                    />
                    <Bar dataKey="bookings" fill="#3b82f6" radius={[2, 2, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Revenue trend - last 30 days */}
            <div className="rounded-xl border border-gray-200 dark:border-gray-600 bg-white dark:bg-dark-surface-card p-[var(--space-md)]">
              <h2 className="mb-[var(--space-sm)] flex items-center gap-2 font-heading text-[var(--text-base)] font-semibold">
                <TrendingUp className="h-4 w-4 text-green-600" />
                Revenue (Last 30 Days)
              </h2>
              <div className="h-56">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={stats.daily_revenue}>
                    <defs>
                      <linearGradient id="revenueGradient" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#22c55e" stopOpacity={0.3} />
                        <stop offset="95%" stopColor="#22c55e" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke={gridStroke} />
                    <XAxis
                      dataKey="date"
                      tickFormatter={formatShortDate}
                      tick={{ fontSize: 11, fill: tickFill }}
                      interval="preserveStartEnd"
                    />
                    <YAxis
                      tick={{ fontSize: 11, fill: tickFill }}
                      width={50}
                      tickFormatter={(v) => `\u20B9${v}`}
                    />
                    <Tooltip
                      labelFormatter={(label) => formatShortDate(label as string)}
                      formatter={(value) => [`\u20B9${Number(value).toLocaleString()}`, "Revenue"]}
                      contentStyle={tooltipStyle}
                    />
                    <Area
                      type="monotone"
                      dataKey="revenue"
                      stroke="#22c55e"
                      strokeWidth={2}
                      fill="url(#revenueGradient)"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        )}

        {/* Charts row 2: Status distribution + Revenue by service */}
        {stats && (
          <div className="mb-[var(--space-lg)] grid gap-[var(--space-sm)] lg:grid-cols-2">
            {/* Booking status distribution */}
            <div className="rounded-xl border border-gray-200 dark:border-gray-600 bg-white dark:bg-dark-surface-card p-[var(--space-md)]">
              <h2 className="mb-[var(--space-sm)] font-heading text-[var(--text-base)] font-semibold">
                Booking Status Distribution
              </h2>
              {statusData.length > 0 ? (
                <div className="h-56">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={statusData}
                        cx="50%"
                        cy="50%"
                        innerRadius={50}
                        outerRadius={80}
                        paddingAngle={3}
                        dataKey="value"
                        nameKey="name"
                      >
                        {statusData.map((entry, index) => (
                          <Cell key={index} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip
                        formatter={(value) => [Number(value), "Bookings"]}
                        contentStyle={tooltipStyle}
                      />
                      <Legend
                        verticalAlign="bottom"
                        height={36}
                        formatter={(value) => <span className="text-xs">{value}</span>}
                      />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              ) : (
                <p className="py-[var(--space-lg)] text-center text-[var(--text-sm)] text-gray-400">
                  No booking data yet
                </p>
              )}
            </div>

            {/* Revenue by service */}
            <div className="rounded-xl border border-gray-200 dark:border-gray-600 bg-white dark:bg-dark-surface-card p-[var(--space-md)]">
              <h2 className="mb-[var(--space-sm)] font-heading text-[var(--text-base)] font-semibold">
                Revenue by Service
              </h2>
              {stats.revenue_by_service.length > 0 ? (
                <div className="h-56">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={stats.revenue_by_service} layout="vertical">
                      <CartesianGrid strokeDasharray="3 3" stroke={gridStroke} />
                      <XAxis
                        type="number"
                        tick={{ fontSize: 11, fill: tickFill }}
                        tickFormatter={(v) => `\u20B9${v}`}
                      />
                      <YAxis
                        type="category"
                        dataKey="service"
                        width={120}
                        tick={{ fontSize: 11, fill: tickFill }}
                      />
                      <Tooltip
                        formatter={(value) => [`\u20B9${Number(value).toLocaleString()}`, "Revenue"]}
                        contentStyle={tooltipStyle}
                      />
                      <Bar dataKey="revenue" radius={[0, 4, 4, 0]}>
                        {stats.revenue_by_service.map((_, index) => (
                          <Cell key={index} fill={SERVICE_COLORS[index % SERVICE_COLORS.length]} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              ) : (
                <p className="py-[var(--space-lg)] text-center text-[var(--text-sm)] text-gray-400">
                  No revenue data yet
                </p>
              )}
            </div>
          </div>
        )}

        {/* Quick links */}
        <div className="mb-[var(--space-lg)] grid gap-[var(--space-sm)] sm:grid-cols-3">
          <Link
            href="/admin/bookings"
            className="flex items-center gap-[var(--space-sm)] rounded-xl border border-gray-200 dark:border-gray-600 bg-white dark:bg-dark-surface-card p-[var(--space-md)] transition-colors hover:border-primary-300"
          >
            <Calendar className="h-5 w-5 text-primary-600 dark:text-primary-400" />
            <span className="font-medium">Manage Bookings</span>
          </Link>
          <Link
            href="/admin/availability"
            className="flex items-center gap-[var(--space-sm)] rounded-xl border border-gray-200 dark:border-gray-600 bg-white dark:bg-dark-surface-card p-[var(--space-md)] transition-colors hover:border-primary-300"
          >
            <Settings className="h-5 w-5 text-primary-600 dark:text-primary-400" />
            <span className="font-medium">Set Availability</span>
          </Link>
          <Link
            href="/admin/payments"
            className="flex items-center gap-[var(--space-sm)] rounded-xl border border-gray-200 dark:border-gray-600 bg-white dark:bg-dark-surface-card p-[var(--space-md)] transition-colors hover:border-primary-300"
          >
            <CreditCard className="h-5 w-5 text-primary-600 dark:text-primary-400" />
            <span className="font-medium">Payment History</span>
          </Link>
        </div>

        {/* Recent bookings */}
        <div className="rounded-xl border border-gray-200 dark:border-gray-600 bg-white dark:bg-dark-surface-card">
          <div className="border-b border-gray-200 dark:border-gray-600 px-[var(--space-md)] py-[var(--space-sm)]">
            <h2 className="font-heading text-[var(--text-lg)] font-semibold">Recent Bookings</h2>
          </div>

          {/* Mobile cards */}
          <div className="divide-y divide-gray-100 dark:divide-white/10 sm:hidden">
            {data.recent_bookings.map((booking) => (
              <div key={booking.id} className="p-[var(--space-md)]">
                <div className="flex items-center justify-between">
                  <p className="font-medium text-[var(--text-base)]">{booking.user_name}</p>
                  <span className={`inline-block rounded-full px-2 py-0.5 text-xs font-medium ${STATUS_BADGE_COLORS[booking.status] || "bg-gray-100 dark:bg-gray-700"}`}>
                    {booking.status}
                  </span>
                </div>
                <p className="mt-1 text-[var(--text-sm)] text-gray-500">{booking.service_title}</p>
                <div className="mt-1 flex items-center justify-between text-[var(--text-sm)] text-gray-500">
                  <span>{booking.date} at {booking.time_slot}</span>
                  <span className="font-medium text-gray-700 dark:text-gray-300">{"\u20B9"}{booking.price_inr}</span>
                </div>
              </div>
            ))}
            {data.recent_bookings.length === 0 && (
              <div className="p-[var(--space-lg)] text-center text-[var(--text-sm)] text-gray-400">
                No bookings yet
              </div>
            )}
          </div>

          {/* Desktop table */}
          <div className="hidden overflow-x-auto sm:block">
            <table className="w-full text-[var(--text-sm)]">
              <thead className="bg-gray-50 dark:bg-dark-surface text-left text-xs uppercase text-gray-500">
                <tr>
                  <th className="px-[var(--space-md)] py-[var(--space-sm)]">Customer</th>
                  <th className="px-[var(--space-md)] py-[var(--space-sm)]">Service</th>
                  <th className="px-[var(--space-md)] py-[var(--space-sm)]">Date & Time</th>
                  <th className="px-[var(--space-md)] py-[var(--space-sm)]">Amount</th>
                  <th className="px-[var(--space-md)] py-[var(--space-sm)]">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100 dark:divide-white/10">
                {data.recent_bookings.map((booking) => (
                  <tr key={booking.id} className="hover:bg-gray-50 dark:hover:bg-white/5">
                    <td className="px-[var(--space-md)] py-[var(--space-sm)] font-medium">{booking.user_name}</td>
                    <td className="px-[var(--space-md)] py-[var(--space-sm)]">{booking.service_title}</td>
                    <td className="px-[var(--space-md)] py-[var(--space-sm)]">
                      {booking.date} at {booking.time_slot}
                    </td>
                    <td className="px-[var(--space-md)] py-[var(--space-sm)]">{"\u20B9"}{booking.price_inr}</td>
                    <td className="px-[var(--space-md)] py-[var(--space-sm)]">
                      <span className={`inline-block rounded-full px-2 py-0.5 text-xs font-medium ${STATUS_BADGE_COLORS[booking.status] || "bg-gray-100 dark:bg-gray-700"}`}>
                        {booking.status}
                      </span>
                    </td>
                  </tr>
                ))}
                {data.recent_bookings.length === 0 && (
                  <tr>
                    <td colSpan={5} className="px-[var(--space-md)] py-[var(--space-lg)] text-center text-gray-400">
                      No bookings yet
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>
  );
}
