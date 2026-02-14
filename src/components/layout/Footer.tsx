import Link from "next/link";
import Image from "next/image";
import {
  Phone,
  Mail,
  MapPin,
  Instagram,
  Youtube,
  Facebook,
} from "lucide-react";
import { Container } from "@/components/ui/Container";
import { siteConfig } from "@/config/site";
import { footerNav } from "@/config/navigation";

function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-vedic-dark text-gray-300">
      {/* Main Footer */}
      <div className="border-b border-white/10 py-16">
        <Container>
          <div className="grid gap-10 sm:grid-cols-2 lg:grid-cols-4">
            {/* Brand Column */}
            <div className="lg:col-span-1">
              <Link href="/" className="inline-flex items-center">
                <Image
                  src="/images/logo/logo-final.png"
                  alt="VedicJivan"
                  width={336}
                  height={142}
                  className="h-14 w-auto sm:h-16 lg:h-[72px] brightness-0 invert"
                />
              </Link>
              <p className="mt-4 text-sm leading-relaxed text-gray-400">
                {siteConfig.description}
              </p>
              <div className="mt-6 space-y-3">
                <a
                  href={`tel:${siteConfig.contact.phone}`}
                  className="flex items-center gap-2 text-sm transition-colors hover:text-gold-400"
                >
                  <Phone className="h-4 w-4 text-gold-500" />
                  {siteConfig.contact.phone}
                </a>
                <a
                  href={`mailto:${siteConfig.contact.email}`}
                  className="flex items-center gap-2 text-sm transition-colors hover:text-gold-400"
                >
                  <Mail className="h-4 w-4 text-gold-500" />
                  {siteConfig.contact.email}
                </a>
                <div className="flex items-start gap-2 text-sm">
                  <MapPin className="mt-0.5 h-4 w-4 shrink-0 text-gold-500" />
                  <div>
                    {siteConfig.contact.address.map((line, i) => (
                      <p key={i}>{line}</p>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Services Column */}
            <div>
              <h3 className="mb-4 font-heading text-lg font-semibold text-white">
                Our Services
              </h3>
              <ul className="space-y-2.5">
                {footerNav.services.map((link) => (
                  <li key={link.href}>
                    <Link
                      href={link.href}
                      className="text-sm transition-colors hover:text-gold-400"
                    >
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>

            {/* Company Column */}
            <div>
              <h3 className="mb-4 font-heading text-lg font-semibold text-white">
                Company
              </h3>
              <ul className="space-y-2.5">
                {footerNav.company.map((link) => (
                  <li key={link.href}>
                    <Link
                      href={link.href}
                      className="text-sm transition-colors hover:text-gold-400"
                    >
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>

            {/* Newsletter + Social Column */}
            <div>
              <h3 className="mb-4 font-heading text-lg font-semibold text-white">
                Stay Connected
              </h3>
              <p className="text-sm text-gray-400">
                Follow us for daily horoscope updates and Vedic wisdom.
              </p>
              <div className="mt-5 flex gap-3">
                <SocialLink
                  href={siteConfig.social.instagram}
                  icon={<Instagram className="h-4 w-4" />}
                  label="Instagram"
                />
                <SocialLink
                  href={siteConfig.social.youtube}
                  icon={<Youtube className="h-4 w-4" />}
                  label="YouTube"
                />
                <SocialLink
                  href={siteConfig.social.facebook}
                  icon={<Facebook className="h-4 w-4" />}
                  label="Facebook"
                />
              </div>

              {/* Legal Links */}
              <div className="mt-8">
                <h4 className="mb-3 text-sm font-semibold text-white">Legal</h4>
                <ul className="space-y-2">
                  {footerNav.legal.map((link) => (
                    <li key={link.href}>
                      <Link
                        href={link.href}
                        className="text-xs text-gray-500 transition-colors hover:text-gold-400"
                      >
                        {link.label}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </Container>
      </div>

      {/* Bottom Bar */}
      <div className="py-5">
        <Container>
          <div className="flex flex-col items-center justify-between gap-3 sm:flex-row">
            <p className="text-xs text-gray-500">
              &copy; {currentYear} {siteConfig.name}. All rights reserved.
            </p>
            <p className="text-xs text-gray-600">
              Crafted with ancient wisdom &amp; modern technology
            </p>
          </div>
        </Container>
      </div>
    </footer>
  );
}

function SocialLink({
  href,
  icon,
  label,
}: {
  href: string;
  icon: React.ReactNode;
  label: string;
}) {
  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      aria-label={label}
      className="flex h-10 w-10 items-center justify-center rounded-full border border-white/10 text-gray-400 transition-all hover:border-gold-500 hover:bg-gold-500/10 hover:text-gold-400"
    >
      {icon}
    </a>
  );
}

export { Footer };
