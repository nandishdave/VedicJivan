"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { Button } from "@/components/ui/Button";
import { bookingsApi, type Booking } from "@/lib/api";
import { getToken, clearTokens } from "@/lib/auth";

export default function BookingsPage() {
  const router = useRouter();
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<string>("");

  useEffect(() => {
    const token = getToken();
    if (!token) {
      router.push("/admin/login");
      return;
    }

    const fetchBookings = async () => {
      try {
        const data = await bookingsApi.list(token, filter ? { status: filter } : undefined);
        setBookings(data);
      } catch {
        clearTokens();
        router.push("/admin/login");
      } finally {
        setLoading(false);
      }
    };

    fetchBookings();
  }, [router, filter]);

  const handleStatusUpdate = async (id: string, status: string) => {
    const token = getToken();
    if (!token) return;

    try {
      const updated = await bookingsApi.updateStatus(id, status, token);
      setBookings((prev) => prev.map((b) => (b.id === id ? updated : b)));
    } catch (err) {
      alert(err instanceof Error ? err.message : "Failed to update status");
    }
  };

  const statusColors: Record<string, string> = {
    pending: "bg-yellow-100 text-yellow-700",
    confirmed: "bg-green-100 text-green-700",
    completed: "bg-blue-100 text-blue-700",
    cancelled: "bg-red-100 text-red-700",
  };

  return (
    <section className="min-h-screen bg-gray-50 py-8">
      <Container>
        <div className="mb-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Link href="/admin" className="rounded-lg p-2 hover:bg-gray-200">
              <ArrowLeft className="h-5 w-5" />
            </Link>
            <h1 className="font-heading text-2xl font-bold">Manage Bookings</h1>
          </div>
        </div>

        {/* Filters */}
        <div className="mb-6 flex gap-2">
          {["", "pending", "confirmed", "completed", "cancelled"].map((s) => (
            <button
              key={s}
              onClick={() => setFilter(s)}
              className={`rounded-full px-4 py-1.5 text-sm font-medium transition-colors ${
                filter === s
                  ? "bg-primary-600 text-white"
                  : "bg-white text-gray-600 hover:bg-gray-100"
              }`}
            >
              {s || "All"}
            </button>
          ))}
        </div>

        {loading ? (
          <div className="space-y-3">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="h-16 animate-pulse rounded-xl bg-gray-200" />
            ))}
          </div>
        ) : (
          <div className="rounded-xl border border-gray-200 bg-white overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-gray-50 text-left text-xs uppercase text-gray-500">
                <tr>
                  <th className="px-4 py-3">Customer</th>
                  <th className="px-4 py-3">Service</th>
                  <th className="px-4 py-3">Date</th>
                  <th className="px-4 py-3">Time</th>
                  <th className="px-4 py-3">Duration</th>
                  <th className="px-4 py-3">Amount</th>
                  <th className="px-4 py-3">Status</th>
                  <th className="px-4 py-3">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {bookings.map((booking) => (
                  <tr key={booking.id} className="hover:bg-gray-50">
                    <td className="px-4 py-3">
                      <p className="font-medium">{booking.user_name}</p>
                      <p className="text-xs text-gray-400">{booking.user_email}</p>
                    </td>
                    <td className="px-4 py-3">{booking.service_title}</td>
                    <td className="px-4 py-3">{booking.date}</td>
                    <td className="px-4 py-3">{booking.time_slot}</td>
                    <td className="px-4 py-3">{booking.duration_minutes}m</td>
                    <td className="px-4 py-3">{"\u20B9"}{booking.price_inr}</td>
                    <td className="px-4 py-3">
                      <span className={`inline-block rounded-full px-2 py-0.5 text-xs font-medium ${statusColors[booking.status] || ""}`}>
                        {booking.status}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex gap-1">
                        {booking.status === "pending" && (
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleStatusUpdate(booking.id, "confirmed")}
                          >
                            Confirm
                          </Button>
                        )}
                        {booking.status === "confirmed" && (
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleStatusUpdate(booking.id, "completed")}
                          >
                            Complete
                          </Button>
                        )}
                        {!["completed", "cancelled"].includes(booking.status) && (
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => handleStatusUpdate(booking.id, "cancelled")}
                            className="text-red-600 hover:text-red-700"
                          >
                            Cancel
                          </Button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
                {bookings.length === 0 && (
                  <tr>
                    <td colSpan={8} className="px-4 py-8 text-center text-gray-400">
                      No bookings found
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </Container>
    </section>
  );
}
