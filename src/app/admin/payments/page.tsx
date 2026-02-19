"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";
import { Container } from "@/components/ui/Container";
import { paymentsApi } from "@/lib/api";
import { getToken, clearTokens } from "@/lib/auth";

interface Payment {
  id: string;
  booking_id: string;
  razorpay_order_id: string;
  razorpay_payment_id: string | null;
  amount_inr: number;
  currency: string;
  status: string;
  created_at: string;
}

export default function PaymentsPage() {
  const router = useRouter();
  const [payments, setPayments] = useState<Payment[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = getToken();
    if (!token) {
      router.push("/admin/login");
      return;
    }

    const fetchPayments = async () => {
      try {
        const data = await paymentsApi.list(token);
        setPayments(data);
      } catch {
        clearTokens();
        router.push("/admin/login");
      } finally {
        setLoading(false);
      }
    };

    fetchPayments();
  }, [router]);

  const statusColors: Record<string, string> = {
    created: "bg-yellow-100 text-yellow-700",
    captured: "bg-green-100 text-green-700",
    failed: "bg-red-100 text-red-700",
    refunded: "bg-purple-100 text-purple-700",
  };

  return (
    <section className="min-h-screen bg-gray-50 py-[var(--space-lg)]">
      <Container>
        <div className="mb-[var(--space-md)] flex items-center gap-[var(--space-sm)]">
          <Link href="/admin" className="rounded-lg p-2 hover:bg-gray-200">
            <ArrowLeft className="h-5 w-5" />
          </Link>
          <h1 className="font-heading text-[var(--text-xl)] font-bold">Payment History</h1>
        </div>

        {loading ? (
          <div className="space-y-[var(--space-sm)]">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="h-14 animate-pulse rounded-xl bg-gray-200" />
            ))}
          </div>
        ) : (
          <div className="rounded-xl border border-gray-200 bg-white">
            {/* Mobile card layout */}
            <div className="divide-y divide-gray-100 sm:hidden">
              {payments.map((payment) => (
                <div key={payment.id} className="p-[var(--space-md)]">
                  <div className="flex items-center justify-between">
                    <span className="font-medium text-[var(--text-base)]">
                      {"\u20B9"}{payment.amount_inr}
                    </span>
                    <span className={`inline-block rounded-full px-2 py-0.5 text-xs font-medium ${statusColors[payment.status] || ""}`}>
                      {payment.status}
                    </span>
                  </div>
                  <p className="mt-1 text-[var(--text-sm)] text-gray-500">
                    {new Date(payment.created_at).toLocaleDateString()}
                  </p>
                  <p className="mt-0.5 break-all font-mono text-xs text-gray-400">
                    {payment.razorpay_order_id}
                  </p>
                  {payment.razorpay_payment_id && (
                    <p className="break-all font-mono text-xs text-gray-400">
                      {payment.razorpay_payment_id}
                    </p>
                  )}
                </div>
              ))}
              {payments.length === 0 && (
                <div className="p-[var(--space-lg)] text-center text-[var(--text-sm)] text-gray-400">
                  No payments yet
                </div>
              )}
            </div>

            {/* Desktop table */}
            <div className="hidden overflow-x-auto sm:block">
              <table className="w-full text-[var(--text-sm)]">
                <thead className="bg-gray-50 text-left text-xs uppercase text-gray-500">
                  <tr>
                    <th className="px-[var(--space-md)] py-[var(--space-sm)]">Date</th>
                    <th className="px-[var(--space-md)] py-[var(--space-sm)]">Order ID</th>
                    <th className="hidden px-[var(--space-md)] py-[var(--space-sm)] md:table-cell">Payment ID</th>
                    <th className="px-[var(--space-md)] py-[var(--space-sm)]">Amount</th>
                    <th className="px-[var(--space-md)] py-[var(--space-sm)]">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {payments.map((payment) => (
                    <tr key={payment.id} className="hover:bg-gray-50">
                      <td className="px-[var(--space-md)] py-[var(--space-sm)] whitespace-nowrap">
                        {new Date(payment.created_at).toLocaleDateString()}
                      </td>
                      <td className="px-[var(--space-md)] py-[var(--space-sm)] font-mono text-xs">{payment.razorpay_order_id}</td>
                      <td className="hidden px-[var(--space-md)] py-[var(--space-sm)] font-mono text-xs md:table-cell">
                        {payment.razorpay_payment_id || "-"}
                      </td>
                      <td className="px-[var(--space-md)] py-[var(--space-sm)] font-medium whitespace-nowrap">
                        {"\u20B9"}{payment.amount_inr}
                      </td>
                      <td className="px-[var(--space-md)] py-[var(--space-sm)]">
                        <span className={`inline-block rounded-full px-2 py-0.5 text-xs font-medium ${statusColors[payment.status] || ""}`}>
                          {payment.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                  {payments.length === 0 && (
                    <tr>
                      <td colSpan={5} className="px-[var(--space-md)] py-[var(--space-lg)] text-center text-gray-400">
                        No payments yet
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
