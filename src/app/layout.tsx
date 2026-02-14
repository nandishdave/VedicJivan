import type { Metadata } from "next";
import { Inter, Playfair_Display } from "next/font/google";
import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { ScrollProgress } from "@/components/ui/ScrollProgress";
import { BackToTop } from "@/components/ui/BackToTop";
import { siteConfig } from "@/config/site";
import { OrganizationJsonLd, WebSiteJsonLd } from "@/components/seo/JsonLd";
import { PageTransition } from "@/components/ui/PageTransition";
import { GoogleAnalytics } from "@/components/analytics/GoogleAnalytics";
import { WhatsAppFloat } from "@/components/ui/WhatsAppFloat";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const playfair = Playfair_Display({
  subsets: ["latin"],
  variable: "--font-playfair",
  display: "swap",
});

export const metadata: Metadata = {
  title: {
    default: `${siteConfig.name} — ${siteConfig.tagline}`,
    template: `%s | ${siteConfig.name}`,
  },
  description: siteConfig.description,
  keywords: [
    "astrology",
    "vedic astrology",
    "kundli",
    "horoscope",
    "numerology",
    "vastu",
    "consultation",
    "jyotish",
    "birth chart",
    "vedic wisdom",
  ],
  authors: [{ name: siteConfig.name }],
  icons: {
    icon: [
      { url: "/icon.svg", type: "image/svg+xml" },
    ],
    apple: "/icon.svg",
  },
  metadataBase: new URL(siteConfig.url),
  alternates: {
    canonical: "/",
  },
  openGraph: {
    type: "website",
    locale: "en_IN",
    url: siteConfig.url,
    siteName: siteConfig.name,
    title: `${siteConfig.name} — ${siteConfig.tagline}`,
    description: siteConfig.description,
  },
  twitter: {
    card: "summary_large_image",
    title: `${siteConfig.name} — ${siteConfig.tagline}`,
    description: siteConfig.description,
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${inter.variable} ${playfair.variable}`}>
      <body className="flex min-h-screen flex-col">
        <GoogleAnalytics />
        <OrganizationJsonLd />
        <WebSiteJsonLd />
        <ScrollProgress />
        <Header />
        <main className="flex-1">
          <PageTransition>{children}</PageTransition>
        </main>
        <Footer />
        <BackToTop />
        <WhatsAppFloat />
      </body>
    </html>
  );
}
