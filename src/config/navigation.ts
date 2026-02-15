export interface NavItem {
  label: string;
  href: string;
  external?: boolean;
  children?: NavItem[];
}

export const mainNav: NavItem[] = [
  { label: "Home", href: "/" },
  { label: "About", href: "/about" },
  {
    label: "Services",
    href: "/services",
    children: [
      { label: "Call Consultation", href: "/services/call-consultation" },
      { label: "Video Consultation", href: "/services/video-consultation" },
      { label: "Premium Kundli", href: "/services/premium-kundli" },
      { label: "Numerology Report", href: "/services/numerology-report" },
      { label: "Vastu Consultation", href: "/services/vastu-consultation" },
      { label: "Kundli Matching", href: "/services/matchmaking" },
      { label: "Astrological Consulting", href: "/services/astrological-consulting" },
      { label: "Growth Coaching", href: "/services/personal-growth-coaching" },
      { label: "Therapeutic Healing", href: "/services/therapeutic-healing" },
    ],
  },
  { label: "Courses", href: "/courses" },
  {
    label: "Blog",
    href: "/blog",
    children: [
      { label: "Articles", href: "/blog" },
      { label: "Nandish Dave Blog", href: "https://blog.nandishdave.world/vedicjivan/", external: true },
    ],
  },
  { label: "Videos", href: "/videos" },
  { label: "Contact", href: "/contact" },
];

export const footerNav: Record<string, NavItem[]> = {
  services: [
    { label: "Call Consultation", href: "/services/call-consultation" },
    { label: "Video Consultation", href: "/services/video-consultation" },
    { label: "Premium Kundli", href: "/services/premium-kundli" },
    { label: "Numerology Report", href: "/services/numerology-report" },
    { label: "Vastu Consultation", href: "/services/vastu-consultation" },
    { label: "Kundli Matching", href: "/services/matchmaking" },
    { label: "Astrological Consulting", href: "/services/astrological-consulting" },
    { label: "Growth Coaching", href: "/services/personal-growth-coaching" },
    { label: "Therapeutic Healing", href: "/services/therapeutic-healing" },
  ],
  company: [
    { label: "About Us", href: "/about" },
    { label: "Blog", href: "/blog" },
    { label: "Nandish Dave Blog", href: "https://blog.nandishdave.world/vedicjivan/", external: true },
    { label: "Courses", href: "/courses" },
    { label: "Contact", href: "/contact" },
    { label: "Videos", href: "/videos" },
  ],
  legal: [
    { label: "Privacy Policy", href: "/privacy-policy" },
    { label: "Terms of Service", href: "/terms" },
    { label: "Refund Policy", href: "/refund-policy" },
  ],
};
