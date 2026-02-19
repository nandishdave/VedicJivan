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

  const actionButtons = (booking: Booking) => (
    <div className="flex gap-1">
      {booking.status === "pending" && (
        <Button variant="ghost" size="sm" onClick={() => handleStatusUpdate(booking.id, "confirmed")}>
          Confirm
        </Button>
      )}
      {booking.status === "confirmed" && (
        <Button variant="ghost" size="sm" onClick={() => handleStatusUpdate(booking.id, "completed")}>
          Complete
        </Button>
      )}
      {!["completed", "cancelled"].includes(booking.status) && (
        <Button variant="ghost" size="sm" onClick={() => handleStatusUpdate(booking.id, "cancelled")} className="text-red-600 hover:text-red-700">
          Cancel
        </Button>
      )}
    </div>
  );

  return (
    <section className="min-h-screen bg-gray-50 py-[var(--space-lg)]">
      <Container>
        <div className="mb-[var(--space-md)] flex items-center justify-between">
          <div className="flex items-center gap-[var(--space-sm)]">
            <Link href="/admin" className="rounded-lg p-2 hover:bg-gray-200">
              <ArrowLeft className="h-5 w-5" />
            </Link>
            <h1 className="font-heading text-[var(--text-xl)] font-bold">Manage Bookings</h1>
          </div>
        </div>

        {/* Filters */}
        <div className="mb-[var(--space-md)] flex flex-wrap gap-[var(--space-xs)]">
          {["", "pending", "confirmed", "completed", "cancelled"].map((s) => (
            <button
              key={s}
              onClick={() => setFilter(s)}
              className={`rounded-full px-4 py-1.5 text-[var(--text-sm)] font-medium transition-colors ${
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
          <div className="space-y-[var(--space-sm)]">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="h-16 animate-pulse rounded-xl bg-gray-200" />
            ))}
          </div>
        ) : (
          <div className="rounded-xl border border-gray-200 bg-white">
            {/* Mobile card layout */}
            <div className="divide-y divide-gray-100 sm:hidden">
              {bookings.map((booking) => (
                <div key={booking.id} className="p-[var(--space-md)]">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="font-medium text-[var(--text-base)]">{booking.user_name}</p>
                      <p className="text-[var(--text-sm)] text-gray-400">{booking.user_email}</p>
                    </div>
                    <span className={`inline-block rounded-full px-2 py-0.5 text-xs font-medium ${statusColors[booking.status] || ""}`}>
                      {booking.status}
                    </span>
                  </div>
                  <p className="mt-1 text-[var(--text-sm)] text-gray-600">{booking.service_title}</p>
                  <div className="mt-1 flex items-center justify-between text-[var(--text-sm)] text-gray-500">
                    <span>{booking.date} at {booking.time_slot} &middot; {booking.duration_minutes}m</span>
                    <span className="font-medium text-gray-700">{"\u20B9"}{booking.price_inr}</span>
                  </div>
                  {booking.date_of_birth && (
                    <div className="mt-1 text-[var(--text-sm)] text-gray-500">
                      <span>DOB: {booking.date_of_birth}</span>
                      {booking.place_of_birth && (
                        <span> &middot; Born: {booking.place_of_birth}</span>
                      )}
                    </div>
                  )}
                  <div className="mt-2">{actionButtons(booking)}</div>
                </div>
              ))}
              {bookings.length === 0 && (
                <div className="p-[var(--space-lg)] text-center text-[var(--text-sm)] text-gray-400">
                  No bookings found
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
                    <th className="px-[var(--space-md)] py-[var(--space-sm)]">Date</th>
                    <th className="hidden px-[var(--space-md)] py-[var(--space-sm)] md:table-cell">Time</th>
                    <th className="hidden px-[var(--space-md)] py-[var(--space-sm)] lg:table-cell">Duration</th>
                    <th className="hidden px-[var(--space-md)] py-[var(--space-sm)] xl:table-cell">DOB</th>
                    <th className="hidden px-[var(--space-md)] py-[var(--space-sm)] xl:table-cell">Birth Place</th>
                    <th className="px-[var(--space-md)] py-[var(--space-sm)]">Amount</th>
                    <th className="px-[var(--space-md)] py-[var(--space-sm)]">Status</th>
                    <th className="px-[var(--space-md)] py-[var(--space-sm)]">Actions</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {bookings.map((booking) => (
                    <tr key={booking.id} className="hover:bg-gray-50">
                      <td className="px-[var(--space-md)] py-[var(--space-sm)]">
                        <p className="font-medium">{booking.user_name}</p>
                        <p className="text-xs text-gray-400">{booking.user_email}</p>
                      </td>
                      <td className="px-[var(--space-md)] py-[var(--space-sm)]">{booking.service_title}</td>
                      <td className="px-[var(--space-md)] py-[var(--space-sm)] whitespace-nowrap">{booking.date}</td>
                      <td className="hidden px-[var(--space-md)] py-[var(--space-sm)] md:table-cell">{booking.time_slot}</td>
                      <td className="hidden px-[var(--space-md)] py-[var(--space-sm)] lg:table-cell">{booking.duration_minutes}m</td>
                      <td className="hidden px-[var(--space-md)] py-[var(--space-sm)] xl:table-cell whitespace-nowrap">{booking.date_of_birth || "—"}</td>
                      <td className="hidden px-[var(--space-md)] py-[var(--space-sm)] xl:table-cell max-w-[200px] truncate">{booking.place_of_birth || "—"}</td>
                      <td className="px-[var(--space-md)] py-[var(--space-sm)]">{"\u20B9"}{booking.price_inr}</td>
                      <td className="px-[var(--space-md)] py-[var(--space-sm)]">
                        <span className={`inline-block rounded-full px-2 py-0.5 text-xs font-medium ${statusColors[booking.status] || ""}`}>
                          {booking.status}
                        </span>
                      </td>
                      <td className="px-[var(--space-md)] py-[var(--space-sm)]">{actionButtons(booking)}</td>
                    </tr>
                  ))}
                  {bookings.length === 0 && (
                    <tr>
                      <td colSpan={10} className="px-[var(--space-md)] py-[var(--space-lg)] text-center text-gray-400">
                        No bookings found
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </Container>
    </section>
  );
}
