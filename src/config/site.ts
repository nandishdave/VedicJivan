export const siteConfig = {
  name: "VedicJivan",
  tagline: "Transform Your Life Through Vedic Wisdom",
  description:
    "VedicJivan offers authentic Vedic astrology consultations, personalized Kundli reports, numerology, Vastu guidance, and astrology courses. Book your consultation today.",
  url: process.env.NEXT_PUBLIC_APP_URL || "https://vedicjivan.nandishdave.world",
  ogImage: "/images/og/default.jpg",
  contact: {
    email: "contact@vedicjivan.com",
    phone: "+91 98765 43210",
    whatsapp: "+919876543210",
    address: "New Delhi, India",
  },
  social: {
    instagram: "https://instagram.com/vedicjivan",
    youtube: "https://youtube.com/@vedicjivan",
    facebook: "https://facebook.com/vedicjivan",
    twitter: "https://twitter.com/vedicjivan",
  },
  stats: {
    consultations: "50,000+",
    countries: "40+",
    experience: "15+",
    awards: "10+",
    students: "2,000+",
  },
};

export const navLinks = [
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
