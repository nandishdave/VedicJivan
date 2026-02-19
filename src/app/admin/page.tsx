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
} from "lucide-react";
import { adminApi, authApi } from "@/lib/api";
import { getToken, clearTokens } from "@/lib/auth";

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

export default function AdminDashboard() {
  const router = useRouter();
  const [data, setData] = useState<DashboardData | null>(null);
  const [userName, setUserName] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = getToken();
    if (!token) {
      router.push("/admin/login");
      return;
    }

    const fetchData = async () => {
      try {
        const [user, dashboard] = await Promise.all([
          authApi.me(token),
          adminApi.dashboard(token),
        ]);

        if (user.role !== "admin") {
          router.push("/admin/login");
          return;
        }

        setUserName(user.name);
        setData(dashboard);
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
      <section className="min-h-screen bg-gray-50 py-[var(--space-lg)]">
        <div className="mx-auto max-w-6xl px-[var(--space-md)]">
          <div className="animate-pulse space-y-6">
            <div className="h-8 w-48 rounded bg-gray-200" />
            <div className="grid gap-[var(--space-sm)] sm:grid-cols-2 lg:grid-cols-4">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="h-24 rounded-xl bg-gray-200" />
              ))}
            </div>
          </div>
        </div>
      </section>
    );
  }

  if (!data) return null;

  const statusColors: Record<string, string> = {
    pending: "bg-yellow-100 text-yellow-700",
    confirmed: "bg-green-100 text-green-700",
    completed: "bg-blue-100 text-blue-700",
    cancelled: "bg-red-100 text-red-700",
  };

  return (
    <section className="min-h-screen bg-gray-50 py-[var(--space-lg)]">
      <div className="mx-auto max-w-6xl px-[var(--space-md)]">
        {/* Header */}
        <div className="mb-[var(--space-lg)]">
          <h1 className="font-heading text-[var(--text-xl)] font-bold text-vedic-dark">
            Dashboard
          </h1>
          <p className="text-[var(--text-sm)] text-gray-500">Welcome back, {userName}</p>
        </div>

        {/* Stats cards */}
        <div className="mb-[var(--space-lg)] grid gap-[var(--space-sm)] sm:grid-cols-2 lg:grid-cols-4">
          <div className="rounded-xl border border-gray-200 bg-white p-[var(--space-md)]">
            <div className="flex items-center gap-[var(--space-sm)]">
              <div className="rounded-lg bg-blue-100 p-2">
                <Calendar className="h-5 w-5 text-blue-600" />
              </div>
              <div>
                <p className="text-2xl font-bold">{data.today_bookings}</p>
                <p className="text-[var(--text-sm)] text-gray-500">Today&apos;s Bookings</p>
              </div>
            </div>
          </div>
          <div className="rounded-xl border border-gray-200 bg-white p-[var(--space-md)]">
            <div className="flex items-center gap-[var(--space-sm)]">
              <div className="rounded-lg bg-green-100 p-2">
                <Clock className="h-5 w-5 text-green-600" />
              </div>
              <div>
                <p className="text-2xl font-bold">{data.upcoming_bookings}</p>
                <p className="text-[var(--text-sm)] text-gray-500">Upcoming</p>
              </div>
            </div>
          </div>
          <div className="rounded-xl border border-gray-200 bg-white p-[var(--space-md)]">
            <div className="flex items-center gap-[var(--space-sm)]">
              <div className="rounded-lg bg-purple-100 p-2">
                <TrendingUp className="h-5 w-5 text-purple-600" />
              </div>
              <div>
                <p className="text-2xl font-bold">{"\u20B9"}{data.total_revenue.toLocaleString()}</p>
                <p className="text-[var(--text-sm)] text-gray-500">Total Revenue</p>
              </div>
            </div>
          </div>
          <div className="rounded-xl border border-gray-200 bg-white p-[var(--space-md)]">
            <div className="flex items-center gap-[var(--space-sm)]">
              <div className="rounded-lg bg-yellow-100 p-2">
                <Users className="h-5 w-5 text-yellow-600" />
              </div>
              <div>
                <p className="text-2xl font-bold">
                  {Object.values(data.bookings_by_status).reduce((a, b) => a + b, 0)}
                </p>
                <p className="text-[var(--text-sm)] text-gray-500">Total Bookings</p>
              </div>
            </div>
          </div>
        </div>

        {/* Quick links */}
        <div className="mb-[var(--space-lg)] grid gap-[var(--space-sm)] sm:grid-cols-3">
          <Link
            href="/admin/bookings"
            className="flex items-center gap-[var(--space-sm)] rounded-xl border border-gray-200 bg-white p-[var(--space-md)] transition-colors hover:border-primary-300"
          >
            <Calendar className="h-5 w-5 text-primary-600" />
            <span className="font-medium">Manage Bookings</span>
          </Link>
          <Link
            href="/admin/availability"
            className="flex items-center gap-[var(--space-sm)] rounded-xl border border-gray-200 bg-white p-[var(--space-md)] transition-colors hover:border-primary-300"
          >
            <Settings className="h-5 w-5 text-primary-600" />
            <span className="font-medium">Set Availability</span>
          </Link>
          <Link
            href="/admin/payments"
            className="flex items-center gap-[var(--space-sm)] rounded-xl border border-gray-200 bg-white p-[var(--space-md)] transition-colors hover:border-primary-300"
          >
            <CreditCard className="h-5 w-5 text-primary-600" />
            <span className="font-medium">Payment History</span>
          </Link>
        </div>

        {/* Recent bookings */}
        <div className="rounded-xl border border-gray-200 bg-white">
          <div className="border-b border-gray-200 px-[var(--space-md)] py-[var(--space-sm)]">
            <h2 className="font-heading text-[var(--text-lg)] font-semibold">Recent Bookings</h2>
          </div>

          {/* Mobile cards */}
          <div className="divide-y divide-gray-100 sm:hidden">
            {data.recent_bookings.map((booking) => (
              <div key={booking.id} className="p-[var(--space-md)]">
                <div className="flex items-center justify-between">
                  <p className="font-medium text-[var(--text-base)]">{booking.user_name}</p>
                  <span className={`inline-block rounded-full px-2 py-0.5 text-xs font-medium ${statusColors[booking.status] || "bg-gray-100"}`}>
                    {booking.status}
                  </span>
                </div>
                <p className="mt-1 text-[var(--text-sm)] text-gray-500">{booking.service_title}</p>
                <div className="mt-1 flex items-center justify-between text-[var(--text-sm)] text-gray-500">
                  <span>{booking.date} at {booking.time_slot}</span>
                  <span className="font-medium text-gray-700">{"\u20B9"}{booking.price_inr}</span>
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
              <thead className="bg-gray-50 text-left text-xs uppercase text-gray-500">
                <tr>
                  <th className="px-[var(--space-md)] py-[var(--space-sm)]">Customer</th>
                  <th className="px-[var(--space-md)] py-[var(--space-sm)]">Service</th>
                  <th className="px-[var(--space-md)] py-[var(--space-sm)]">Date & Time</th>
                  <th className="px-[var(--space-md)] py-[var(--space-sm)]">Amount</th>
                  <th className="px-[var(--space-md)] py-[var(--space-sm)]">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {data.recent_bookings.map((booking) => (
                  <tr key={booking.id} className="hover:bg-gray-50">
                    <td className="px-[var(--space-md)] py-[var(--space-sm)] font-medium">{booking.user_name}</td>
                    <td className="px-[var(--space-md)] py-[var(--space-sm)]">{booking.service_title}</td>
                    <td className="px-[var(--space-md)] py-[var(--space-sm)]">
                      {booking.date} at {booking.time_slot}
                    </td>
                    <td className="px-[var(--space-md)] py-[var(--space-sm)]">{"\u20B9"}{booking.price_inr}</td>
                    <td className="px-[var(--space-md)] py-[var(--space-sm)]">
                      <span className={`inline-block rounded-full px-2 py-0.5 text-xs font-medium ${statusColors[booking.status] || "bg-gray-100"}`}>
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
