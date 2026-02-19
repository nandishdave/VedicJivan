"use client";

import { useEffect, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import Link from "next/link";
import {
  LayoutDashboard,
  Calendar,
  Clock,
  CreditCard,
  Settings,
  LogOut,
  ExternalLink,
  Menu,
  X,
} from "lucide-react";
import { getToken, clearTokens } from "@/lib/auth";
import { authApi } from "@/lib/api";

const adminNav = [
  { label: "Dashboard", href: "/admin", icon: LayoutDashboard },
  { label: "Bookings", href: "/admin/bookings", icon: Calendar },
  { label: "Availability", href: "/admin/availability", icon: Clock },
  { label: "Payments", href: "/admin/payments", icon: CreditCard },
  { label: "Settings", href: "/admin/settings", icon: Settings },
];

const hideChrome = `.site-header, .site-footer, .site-whatsapp-float, .site-back-to-top, .site-scroll-progress { display: none !important; }`;

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const router = useRouter();
  const isLoginPage = pathname === "/admin/login";
  const [isAdmin, setIsAdmin] = useState(false);
  const [checking, setChecking] = useState(true);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Close sidebar on route change
  useEffect(() => {
    setSidebarOpen(false);
  }, [pathname]);

  useEffect(() => {
    if (isLoginPage) {
      setChecking(false);
      return;
    }

    const token = getToken();
    if (!token) {
      router.push("/admin/login");
      setChecking(false);
      return;
    }

    authApi
      .me(token)
      .then((user) => {
        if (user.role === "admin") {
          setIsAdmin(true);
        } else {
          clearTokens();
          router.push("/admin/login");
        }
      })
      .catch(() => {
        clearTokens();
        router.push("/admin/login");
      })
      .finally(() => setChecking(false));
  }, [isLoginPage, router]);

  const handleLogout = () => {
    clearTokens();
    router.push("/admin/login");
  };

  // Login page gets no admin shell
  if (isLoginPage) {
    return (
      <>
        <style>{hideChrome}</style>
        {children}
      </>
    );
  }

  // Still verifying auth — show loading skeleton
  if (checking) {
    return (
      <>
        <style>{hideChrome}</style>
        <section className="min-h-screen bg-gray-50 py-12">
          <div className="mx-auto max-w-6xl px-6">
            <div className="animate-pulse space-y-6">
              <div className="h-8 w-48 rounded bg-gray-200" />
              <div className="h-64 rounded-xl bg-gray-200" />
            </div>
          </div>
        </section>
      </>
    );
  }

  // Not admin — children will handle their own redirect, render nothing extra
  if (!isAdmin) {
    return (
      <>
        <style>{hideChrome}</style>
        {children}
      </>
    );
  }

  const sidebarContent = (
    <div className="flex h-full flex-col">
      {/* Logo / Brand */}
      <div className="flex items-center justify-between border-b border-gray-200 px-4 py-5">
        <div>
          <Link href="/admin" className="font-heading text-lg font-bold text-primary-600">
            VedicJivan
          </Link>
          <p className="text-xs text-gray-400">Admin Panel</p>
        </div>
        {/* Close button — mobile only */}
        <button
          onClick={() => setSidebarOpen(false)}
          className="rounded-lg p-1.5 text-gray-400 hover:bg-gray-100 lg:hidden"
        >
          <X className="h-5 w-5" />
        </button>
      </div>

      {/* Nav Links */}
      <nav className="flex-1 space-y-1 px-3 py-4">
        {adminNav.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors ${
                isActive
                  ? "bg-primary-50 text-primary-600"
                  : "text-gray-600 hover:bg-gray-100 hover:text-gray-900"
              }`}
            >
              <item.icon className="h-4 w-4" />
              {item.label}
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="border-t border-gray-200 p-3 space-y-1">
        <Link
          href="/"
          className="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-gray-600 hover:bg-gray-100"
        >
          <ExternalLink className="h-4 w-4" />
          View Site
        </Link>
        <button
          onClick={handleLogout}
          className="flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm text-red-600 hover:bg-red-50"
        >
          <LogOut className="h-4 w-4" />
          Logout
        </button>
      </div>
    </div>
  );

  return (
    <>
      <style>{`${hideChrome} main { padding: 0 !important; }`}</style>
      <div className="flex min-h-screen bg-gray-50">
        {/* Mobile top bar */}
        <div className="fixed left-0 right-0 top-0 z-30 flex items-center border-b border-gray-200 bg-white px-[var(--space-md)] py-[var(--space-sm)] lg:hidden">
          <button
            onClick={() => setSidebarOpen(true)}
            className="rounded-lg p-1.5 text-gray-600 hover:bg-gray-100"
            aria-label="Open menu"
          >
            <Menu className="h-5 w-5" />
          </button>
          <span className="ml-3 font-heading text-sm font-bold text-primary-600">
            VedicJivan Admin
          </span>
        </div>

        {/* Mobile overlay */}
        {sidebarOpen && (
          <div
            className="fixed inset-0 z-40 bg-black/50 lg:hidden"
            onClick={() => setSidebarOpen(false)}
          />
        )}

        {/* Sidebar — desktop: always visible, mobile: slide-in overlay */}
        <aside
          className={`fixed left-0 top-0 z-50 h-screen w-64 border-r border-gray-200 bg-white transition-transform duration-200 ease-in-out lg:z-40 lg:w-56 lg:translate-x-0 ${
            sidebarOpen ? "translate-x-0" : "-translate-x-full"
          }`}
        >
          {sidebarContent}
        </aside>

        {/* Main Content — offset for desktop sidebar, padded-top for mobile bar */}
        <div className="min-w-0 flex-1 pt-14 lg:ml-56 lg:pt-0">
          {children}
        </div>
      </div>
    </>
  );
}
