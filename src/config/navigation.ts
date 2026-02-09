export interface NavItem {
  label: string;
  href: string;
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
    ],
  },
  { label: "Courses", href: "/courses" },
  { label: "Blog", href: "/blog" },
  { label: "Contact", href: "/contact" },
];

export const footerNav = {
  services: [
    { label: "Call Consultation", href: "/services/call-consultation" },
    { label: "Video Consultation", href: "/services/video-consultation" },
    { label: "Premium Kundli", href: "/services/premium-kundli" },
    { label: "Numerology Report", href: "/services/numerology-report" },
    { label: "Vastu Consultation", href: "/services/vastu-consultation" },
  ],
  company: [
    { label: "About Us", href: "/about" },
    { label: "Blog", href: "/blog" },
    { label: "Courses", href: "/courses" },
    { label: "Contact", href: "/contact" },
    { label: "Podcast", href: "/podcast" },
  ],
  legal: [
    { label: "Privacy Policy", href: "/privacy-policy" },
    { label: "Terms of Service", href: "/terms" },
    { label: "Refund Policy", href: "/refund-policy" },
  ],
};
