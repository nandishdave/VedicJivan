export const siteConfig = {
  name: "VedicJivan",
  tagline: "Transform Your Life Through Vedic Wisdom",
  description:
    "VedicJivan offers authentic Vedic astrology consultations, personalized Kundli reports, numerology, Vastu guidance, and astrology courses. Book your consultation today.",
  url: process.env.NEXT_PUBLIC_APP_URL || "https://vedicjivan.nandishdave.world",
  ogImage: "/images/og/default.jpg",
  contact: {
    email: "vedic.jivan33@gmail.com",
    phone: "+91 98242 92212",
    whatsapp: "+919824292212",
    address: ["Ahmedabad, Gujarat", "Eindhoven, Netherlands"],
  },
  social: {
    instagram: "https://www.instagram.com/vedicjivan333",
    youtube: "https://www.youtube.com/@VedicJivan333",
    facebook: "https://www.facebook.com/groups/1625796561636761",
    blog: "https://blog.nandishdave.world/vedicjivan/",
  },
  stats: {
    consultations: "50,000+",
    countries: "40+",
    experience: "15+",
    services: "9+",
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
  { label: "Nandish Dave Blog", href: "https://blog.nandishdave.world/vedicjivan/" },
  { label: "Contact", href: "/contact" },
];
