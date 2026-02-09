"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import Image from "next/image";
import { Menu, X, ChevronDown, Phone } from "lucide-react";
import { cn } from "@/lib/utils/cn";
import { mainNav, type NavItem } from "@/config/navigation";
import { siteConfig } from "@/config/site";
import { Container } from "@/components/ui/Container";
import { Button } from "@/components/ui/Button";

function Header() {
  const [isOpen, setIsOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  const [openDropdown, setOpenDropdown] = useState<string | null>(null);
  const pathname = usePathname();

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  useEffect(() => {
    setIsOpen(false);
    setOpenDropdown(null);
  }, [pathname]);

  return (
    <>
      {/* Top Bar */}
      <div className="hidden bg-vedic-dark py-2 text-sm text-gray-300 lg:block">
        <Container>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <a
                href={`tel:${siteConfig.contact.phone}`}
                className="flex items-center gap-1.5 transition-colors hover:text-gold-400"
              >
                <Phone className="h-3.5 w-3.5" />
                {siteConfig.contact.phone}
              </a>
              <span className="text-gray-600">|</span>
              <a
                href={`mailto:${siteConfig.contact.email}`}
                className="transition-colors hover:text-gold-400"
              >
                {siteConfig.contact.email}
              </a>
            </div>
            <div className="flex items-center gap-3">
              <a
                href={siteConfig.social.instagram}
                target="_blank"
                rel="noopener noreferrer"
                className="transition-colors hover:text-gold-400"
              >
                Instagram
              </a>
              <span className="text-gray-600">|</span>
              <a
                href={siteConfig.social.youtube}
                target="_blank"
                rel="noopener noreferrer"
                className="transition-colors hover:text-gold-400"
              >
                YouTube
              </a>
            </div>
          </div>
        </Container>
      </div>

      {/* Main Navigation */}
      <header
        className={cn(
          "sticky top-0 z-50 w-full transition-all duration-300",
          isScrolled
            ? "bg-white/95 shadow-lg shadow-primary-900/5 backdrop-blur-md"
            : "bg-white"
        )}
      >
        <Container>
          <nav className="flex h-20 items-center justify-between lg:h-24">
            {/* Logo */}
            <Link href="/" className="flex items-center">
              <Image
                src="/images/logo/logo-final.png"
                alt="VedicJivan — Connect The Divine Within"
                width={336}
                height={142}
                className="h-14 w-auto sm:h-16 lg:h-[72px]"
                priority
              />
            </Link>

            {/* Desktop Navigation */}
            <div className="hidden items-center gap-1 lg:flex">
              {mainNav.map((item) => (
                <NavLink
                  key={item.href}
                  item={item}
                  pathname={pathname}
                  openDropdown={openDropdown}
                  setOpenDropdown={setOpenDropdown}
                />
              ))}
            </div>

            {/* Desktop CTA */}
            <div className="hidden items-center gap-3 lg:flex">
              <Link href="/login">
                <Button variant="ghost" size="sm">
                  Login
                </Button>
              </Link>
              <Link href="/services">
                <Button variant="gold" size="sm">
                  Book Consultation
                </Button>
              </Link>
            </div>

            {/* Mobile Menu Button */}
            <button
              className="rounded-lg p-2 text-vedic-dark transition-colors hover:bg-gray-100 lg:hidden"
              onClick={() => setIsOpen(!isOpen)}
              aria-label={isOpen ? "Close menu" : "Open menu"}
            >
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </nav>
        </Container>

        {/* Mobile Navigation */}
        <div
          className={cn(
            "overflow-hidden border-t border-gray-100 bg-white transition-all duration-300 lg:hidden",
            isOpen ? "max-h-[80vh] opacity-100" : "max-h-0 opacity-0"
          )}
        >
          <Container>
            <div className="space-y-1 py-4">
              {mainNav.map((item) => (
                <MobileNavLink
                  key={item.href}
                  item={item}
                  pathname={pathname}
                  openDropdown={openDropdown}
                  setOpenDropdown={setOpenDropdown}
                />
              ))}
              <div className="mt-4 flex flex-col gap-2 border-t border-gray-100 pt-4">
                <Link href="/login">
                  <Button variant="outline" size="sm" className="w-full">
                    Login
                  </Button>
                </Link>
                <Link href="/services">
                  <Button variant="gold" size="sm" className="w-full">
                    Book Consultation
                  </Button>
                </Link>
              </div>
            </div>
          </Container>
        </div>
      </header>
    </>
  );
}

function NavLink({
  item,
  pathname,
  openDropdown,
  setOpenDropdown,
}: {
  item: NavItem;
  pathname: string;
  openDropdown: string | null;
  setOpenDropdown: (key: string | null) => void;
}) {
  const isActive =
    pathname === item.href || pathname.startsWith(item.href + "/");
  const hasChildren = item.children && item.children.length > 0;
  const isDropdownOpen = openDropdown === item.href;

  if (hasChildren) {
    return (
      <div
        className="relative"
        onMouseEnter={() => setOpenDropdown(item.href)}
        onMouseLeave={() => setOpenDropdown(null)}
      >
        <button
          className={cn(
            "flex items-center gap-1 rounded-lg px-4 py-2 text-sm font-medium transition-colors",
            isActive
              ? "text-primary-600"
              : "text-vedic-text hover:bg-primary-50 hover:text-primary-600"
          )}
        >
          {item.label}
          <ChevronDown
            className={cn(
              "h-4 w-4 transition-transform",
              isDropdownOpen && "rotate-180"
            )}
          />
        </button>
        <div
          className={cn(
            "absolute left-0 top-full min-w-[220px] rounded-xl border border-gray-100 bg-white py-2 shadow-xl shadow-primary-900/10 transition-all duration-200",
            isDropdownOpen
              ? "visible translate-y-0 opacity-100"
              : "invisible -translate-y-2 opacity-0"
          )}
        >
          {item.children!.map((child) => (
            <Link
              key={child.href}
              href={child.href}
              className={cn(
                "block px-4 py-2.5 text-sm transition-colors",
                pathname === child.href
                  ? "bg-primary-50 text-primary-600"
                  : "text-vedic-text hover:bg-primary-50 hover:text-primary-600"
              )}
            >
              {child.label}
            </Link>
          ))}
        </div>
      </div>
    );
  }

  return (
    <Link
      href={item.href}
      className={cn(
        "rounded-lg px-4 py-2 text-sm font-medium transition-colors",
        isActive
          ? "text-primary-600"
          : "text-vedic-text hover:bg-primary-50 hover:text-primary-600"
      )}
    >
      {item.label}
    </Link>
  );
}

function MobileNavLink({
  item,
  pathname,
  openDropdown,
  setOpenDropdown,
}: {
  item: NavItem;
  pathname: string;
  openDropdown: string | null;
  setOpenDropdown: (key: string | null) => void;
}) {
  const isActive =
    pathname === item.href || pathname.startsWith(item.href + "/");
  const hasChildren = item.children && item.children.length > 0;
  const isDropdownOpen = openDropdown === item.href;

  if (hasChildren) {
    return (
      <div>
        <button
          onClick={() =>
            setOpenDropdown(isDropdownOpen ? null : item.href)
          }
          className={cn(
            "flex w-full items-center justify-between rounded-lg px-4 py-3 text-sm font-medium transition-colors",
            isActive
              ? "bg-primary-50 text-primary-600"
              : "text-vedic-text hover:bg-gray-50"
          )}
        >
          {item.label}
          <ChevronDown
            className={cn(
              "h-4 w-4 transition-transform",
              isDropdownOpen && "rotate-180"
            )}
          />
        </button>
        <div
          className={cn(
            "overflow-hidden transition-all duration-200",
            isDropdownOpen ? "max-h-96 opacity-100" : "max-h-0 opacity-0"
          )}
        >
          <div className="ml-4 space-y-1 border-l-2 border-primary-200 pl-4 pt-1">
            {item.children!.map((child) => (
              <Link
                key={child.href}
                href={child.href}
                className={cn(
                  "block rounded-lg px-3 py-2 text-sm transition-colors",
                  pathname === child.href
                    ? "text-primary-600 font-medium"
                    : "text-gray-600 hover:text-primary-600"
                )}
              >
                {child.label}
              </Link>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <Link
      href={item.href}
      className={cn(
        "block rounded-lg px-4 py-3 text-sm font-medium transition-colors",
        isActive
          ? "bg-primary-50 text-primary-600"
          : "text-vedic-text hover:bg-gray-50"
      )}
    >
      {item.label}
    </Link>
  );
}

export { Header };
