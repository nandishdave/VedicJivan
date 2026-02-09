export interface Service {
  slug: string;
  title: string;
  shortDescription: string;
  description: string;
  priceINR: string;
  priceEUR: string;
  duration: string | null;
  icon: string;
  category: "consultation" | "report" | "guidance";
  features: string[];
  process: { step: number; title: string; description: string }[];
  faqs: { question: string; answer: string }[];
}

export const services: Service[] = [
  {
    slug: "call-consultation",
    title: "Call Consultation",
    shortDescription:
      "Get personalized astrology guidance over a phone call. Discuss your career, relationships, health, and more.",
    description:
      "Connect with our expert Vedic astrologer over a private phone call for personalized guidance. Whether you're facing career dilemmas, relationship concerns, health worries, or financial decisions — get actionable insights based on your unique birth chart. Our astrologer will analyze planetary positions, Dashas, and transits to provide you with clear, practical advice.",
    priceINR: "\u20B91,999",
    priceEUR: "\u20AC29",
    duration: "30 min",
    icon: "Phone",
    category: "consultation",
    features: [
      "30-minute private phone session",
      "Personalized birth chart analysis",
      "Career & financial guidance",
      "Relationship compatibility insights",
      "Health & wellness predictions",
      "Practical remedies & solutions",
      "Follow-up summary via email",
    ],
    process: [
      {
        step: 1,
        title: "Book Your Slot",
        description:
          "Choose a convenient date and time from our available slots.",
      },
      {
        step: 2,
        title: "Share Birth Details",
        description:
          "Provide your date, time, and place of birth for accurate chart analysis.",
      },
      {
        step: 3,
        title: "Receive Your Call",
        description:
          "Our astrologer will call you at the scheduled time for your personalized session.",
      },
      {
        step: 4,
        title: "Get Your Summary",
        description:
          "Receive a detailed email summary of predictions, remedies, and guidance.",
      },
    ],
    faqs: [
      {
        question: "What information do I need to provide?",
        answer:
          "You'll need your exact date of birth, time of birth, and place of birth. The more accurate the time, the better the predictions.",
      },
      {
        question: "Can I ask specific questions during the call?",
        answer:
          "Absolutely! You can ask about any area of life — career, marriage, health, finances, education, or specific concerns.",
      },
      {
        question: "How do I receive my consultation summary?",
        answer:
          "Within 24 hours of your session, you'll receive a detailed email with key points, predictions, and recommended remedies.",
      },
    ],
  },
  {
    slug: "video-consultation",
    title: "Video Consultation",
    shortDescription:
      "Face-to-face video session with our expert astrologer. Get detailed analysis with screen-shared birth chart.",
    description:
      "Experience an immersive face-to-face video consultation where our astrologer walks you through your birth chart in real-time via screen sharing. See the planetary positions, Dashas, and yogas as they're explained to you. This premium format ensures deeper understanding and allows for visual demonstration of chart analysis.",
    priceINR: "\u20B92,999",
    priceEUR: "\u20AC39",
    duration: "45 min",
    icon: "Video",
    category: "consultation",
    features: [
      "45-minute face-to-face video session",
      "Real-time screen-shared chart analysis",
      "Detailed Dasha period breakdown",
      "Visual planetary transit explanation",
      "Comprehensive remedies with demonstration",
      "Recorded session copy (on request)",
      "Priority email support for 7 days",
    ],
    process: [
      {
        step: 1,
        title: "Book Your Slot",
        description:
          "Select your preferred date and time for the video session.",
      },
      {
        step: 2,
        title: "Share Birth Details",
        description:
          "Provide your birth details so the chart can be prepared in advance.",
      },
      {
        step: 3,
        title: "Join Video Call",
        description:
          "Receive a meeting link via email. Join from any device at the scheduled time.",
      },
      {
        step: 4,
        title: "Interactive Session",
        description:
          "Watch your chart analyzed live with screen sharing and ask questions in real time.",
      },
    ],
    faqs: [
      {
        question: "Which platform is used for video calls?",
        answer:
          "We use Google Meet or Zoom. You'll receive the meeting link via email 30 minutes before the session.",
      },
      {
        question: "Can I record the session?",
        answer:
          "Yes, you can request a recorded copy of the session which will be shared via email within 24 hours.",
      },
      {
        question: "What if I face technical issues?",
        answer:
          "If there are connectivity issues, we'll switch to a phone call or reschedule the session at no extra cost.",
      },
    ],
  },
  {
    slug: "premium-kundli",
    title: "Premium Kundli Report",
    shortDescription:
      "Comprehensive 40+ page personalized Kundli report covering all aspects of your life.",
    description:
      "Receive an expertly crafted, 40+ page personalized Kundli report that covers every aspect of your life in extraordinary detail. From planetary positions and Dasha periods to specific predictions about career, marriage, health, finances, and education — this report is your complete life guide based on authentic Vedic astrological principles.",
    priceINR: "\u20B94,999",
    priceEUR: "\u20AC59",
    duration: null,
    icon: "FileText",
    category: "report",
    features: [
      "40+ page comprehensive report",
      "Complete birth chart with all divisional charts",
      "Detailed Dasha & Antardasha analysis",
      "Career & professional growth predictions",
      "Marriage & relationship compatibility",
      "Health & wellness forecast",
      "Financial prospects & investment timing",
      "Gemstone & mantra recommendations",
      "Auspicious dates for important decisions",
      "Lifetime validity — refer anytime",
    ],
    process: [
      {
        step: 1,
        title: "Place Your Order",
        description: "Complete the payment and provide your birth details.",
      },
      {
        step: 2,
        title: "Chart Preparation",
        description:
          "Our astrologer carefully prepares your birth chart and divisional charts.",
      },
      {
        step: 3,
        title: "Detailed Analysis",
        description:
          "Each aspect of your life is analyzed using authentic Vedic methods.",
      },
      {
        step: 4,
        title: "Report Delivery",
        description:
          "Receive your beautifully formatted PDF report via email within 5-7 business days.",
      },
    ],
    faqs: [
      {
        question: "How long does it take to receive the report?",
        answer:
          "The Premium Kundli Report is delivered within 5-7 business days via email as a beautifully formatted PDF.",
      },
      {
        question: "How is this different from free online Kundli reports?",
        answer:
          "Unlike auto-generated reports, our Premium Kundli is manually analyzed by an expert astrologer, providing personalized insights and specific predictions tailored to your life.",
      },
      {
        question: "Can I get a consultation along with the report?",
        answer:
          "Yes! You can add a 30-minute call consultation at a discounted rate to discuss the report findings in detail.",
      },
    ],
  },
  {
    slug: "numerology-report",
    title: "Numerology Report",
    shortDescription:
      "Discover the power of numbers in your life. Detailed numerology analysis based on your name and birth date.",
    description:
      "Unlock the hidden influence of numbers in your life with our comprehensive Numerology Report. Based on your full name and date of birth, we analyze your Life Path Number, Expression Number, Soul Urge Number, and more to reveal your personality traits, life purpose, career aptitude, and lucky periods.",
    priceINR: "\u20B91,499",
    priceEUR: "\u20AC19",
    duration: null,
    icon: "Hash",
    category: "report",
    features: [
      "Complete numerological profile",
      "Life Path Number analysis",
      "Expression & Soul Urge Numbers",
      "Personal Year & Month predictions",
      "Lucky numbers, colors & days",
      "Name correction suggestions",
      "Business name analysis",
      "Compatibility by numbers",
    ],
    process: [
      {
        step: 1,
        title: "Share Your Details",
        description:
          "Provide your full legal name and date of birth after payment.",
      },
      {
        step: 2,
        title: "Number Analysis",
        description:
          "Our numerologist calculates and analyzes all key numbers in your profile.",
      },
      {
        step: 3,
        title: "Report Preparation",
        description:
          "A detailed report is prepared with predictions and recommendations.",
      },
      {
        step: 4,
        title: "Delivery",
        description:
          "Receive your report via email within 3-5 business days.",
      },
    ],
    faqs: [
      {
        question: "Do I need my birth time for numerology?",
        answer:
          "No, numerology is based on your full name and date of birth. Birth time is not required.",
      },
      {
        question: "Can numerology help with business decisions?",
        answer:
          "Yes! We analyze business names, suggest lucky numbers for business, and identify favorable periods for starting new ventures.",
      },
      {
        question: "What is name correction?",
        answer:
          "Based on your numerological profile, we may suggest minor spelling adjustments to your name that can positively influence your vibrations and attract better opportunities.",
      },
    ],
  },
  {
    slug: "vastu-consultation",
    title: "Vastu Consultation",
    shortDescription:
      "Expert Vastu Shastra guidance for your home or office. Optimize your space for prosperity.",
    description:
      "Transform the energy of your living or working space with expert Vastu Shastra consultation. Our Vastu expert analyzes the layout, directions, and elemental balance of your property to identify energy blocks and provide practical remedies without major structural changes. Suitable for homes, offices, shops, and factories.",
    priceINR: "\u20B93,499",
    priceEUR: "\u20AC45",
    duration: "60 min",
    icon: "Home",
    category: "guidance",
    features: [
      "60-minute detailed consultation",
      "Complete directional analysis",
      "Room-by-room Vastu assessment",
      "Elemental balance evaluation",
      "Practical remedies (no demolition)",
      "Color & material recommendations",
      "Placement guidance for key items",
      "Written report with floor plan notes",
    ],
    process: [
      {
        step: 1,
        title: "Share Property Details",
        description:
          "Provide floor plan, photos, and compass directions of your property.",
      },
      {
        step: 2,
        title: "Vastu Analysis",
        description:
          "Our expert studies the layout, directions, and elemental balance.",
      },
      {
        step: 3,
        title: "Consultation Session",
        description:
          "Discuss findings and remedies in a 60-minute video/phone call.",
      },
      {
        step: 4,
        title: "Written Report",
        description:
          "Receive a detailed report with room-by-room recommendations.",
      },
    ],
    faqs: [
      {
        question: "Do I need to share my floor plan?",
        answer:
          "Yes, a rough floor plan with compass directions helps us provide accurate Vastu analysis. You can draw it by hand or share an architect's plan.",
      },
      {
        question: "Will I need to make structural changes?",
        answer:
          "No! Our Vastu remedies focus on practical, non-structural solutions like color changes, placement adjustments, and energy-balancing techniques.",
      },
      {
        question: "Is Vastu applicable to rented properties?",
        answer:
          "Absolutely. Most of our remedies are portable and can be implemented in rented spaces without permanent modifications.",
      },
    ],
  },
  {
    slug: "matchmaking",
    title: "Kundli Matching",
    shortDescription:
      "Comprehensive compatibility analysis for marriage. Detailed Guna Milan and Mangal Dosha check.",
    description:
      "Making the most important decision of your life? Our comprehensive Kundli Matching service analyzes both birth charts for compatibility across all 36 Gunas (Ashtakoota Milan), checks for Mangal Dosha and other critical doshas, and provides a detailed compatibility report with remedies if needed. Trusted by thousands of families worldwide.",
    priceINR: "\u20B92,499",
    priceEUR: "\u20AC35",
    duration: null,
    icon: "Heart",
    category: "guidance",
    features: [
      "Complete Ashtakoota (36 Guna) matching",
      "Mangal Dosha analysis for both charts",
      "Nadi Dosha & Bhakoot Dosha check",
      "Mental & emotional compatibility assessment",
      "Financial & family compatibility",
      "Health & progeny analysis",
      "Remedies for any doshas found",
      "Marriage timing (Muhurta) suggestions",
    ],
    process: [
      {
        step: 1,
        title: "Submit Both Charts",
        description:
          "Provide birth details (date, time, place) of both partners.",
      },
      {
        step: 2,
        title: "Guna Matching",
        description:
          "All 36 Gunas are analyzed using the Ashtakoota system.",
      },
      {
        step: 3,
        title: "Dosha Analysis",
        description:
          "Both charts are checked for Mangal Dosha, Nadi Dosha, and other compatibility issues.",
      },
      {
        step: 4,
        title: "Report & Remedies",
        description:
          "Receive a detailed compatibility report with score, analysis, and remedies if needed.",
      },
    ],
    faqs: [
      {
        question: "How many Gunas should match for a good marriage?",
        answer:
          "Traditionally, 18 or more Gunas out of 36 are considered good. However, we also consider other factors like Mangal Dosha and overall chart compatibility.",
      },
      {
        question: "What if there is Mangal Dosha?",
        answer:
          "If Mangal Dosha is found, we provide specific remedies including mantras, gemstones, and rituals that can neutralize its effects.",
      },
      {
        question: "Can this be done for couples already married?",
        answer:
          "Yes, Kundli matching can help married couples understand their dynamics better and provide remedies for any challenges they face.",
      },
    ],
  },
];

export function getServiceBySlug(slug: string): Service | undefined {
  return services.find((s) => s.slug === slug);
}

export function getRelatedServices(currentSlug: string): Service[] {
  const current = getServiceBySlug(currentSlug);
  if (!current) return services.slice(0, 3);
  return services
    .filter((s) => s.slug !== currentSlug)
    .sort((a, b) =>
      a.category === current.category ? -1 : b.category === current.category ? 1 : 0
    )
    .slice(0, 3);
}
