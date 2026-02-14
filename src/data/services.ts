export interface Service {
  slug: string;
  title: string;
  shortDescription: string;
  description: string;
  priceINR: string;
  priceEUR: string;
  duration: string | null;
  icon: string;
  image: string;
  category: "consultation" | "report" | "guidance" | "wellness";
  features: string[];
  process: { step: number; title: string; description: string }[];
  faqs: { question: string; answer: string }[];
}

export const services: Service[] = [
  {
    slug: "call-consultation",
    title: "Call Consultation",
    image: "https://images.unsplash.com/photo-1655947716360-eee99bc3b056?w=800&q=80",
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
    image: "https://images.unsplash.com/photo-1521624213010-9fb0f30dcd20?w=800&q=80",
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
    image: "https://images.unsplash.com/photo-1533294455009-a77b7557d2d1?w=800&q=80",
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
    image: "https://images.unsplash.com/photo-1561148493-89acae53e6a1?w=800&q=80",
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
    image: "https://images.unsplash.com/photo-1628744876490-19b035ecf9c3?w=800&q=80",
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
    image: "https://images.unsplash.com/photo-1583878545126-2f1ca0142714?w=800&q=80",
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
  {
    slug: "astrological-consulting",
    title: "Astrological Consulting",
    image: "https://images.unsplash.com/photo-1444703686981-a3abbc4d4fe3?w=800&q=80",
    shortDescription:
      "Birth chart analysis, planetary transits, and astrological timing. Personalized guidance for life decisions, relationships, career, and personal growth through cosmic wisdom.",
    description:
      "Our Astrological Consulting service goes beyond traditional horoscope readings to offer deep, transformative guidance rooted in Vedic wisdom. Through meticulous birth chart analysis, planetary transit mapping, and astrological timing techniques, we help you navigate life's most important decisions with cosmic clarity. Whether you're seeking direction in your career, understanding relationship dynamics, or looking for the right timing for major life changes — our consulting integrates ancient astrological knowledge with a modern, practical approach to personal growth.",
    priceINR: "\u20B93,499",
    priceEUR: "\u20AC45",
    duration: "60 min",
    icon: "Compass",
    category: "wellness",
    features: [
      "In-depth birth chart (Kundli) analysis",
      "Planetary transit & Dasha period guidance",
      "Astrological timing for key decisions",
      "Career & professional path insights",
      "Relationship & compatibility guidance",
      "Personalized growth roadmap",
      "Remedy recommendations (gemstones, mantras)",
      "Follow-up email summary with action steps",
    ],
    process: [
      {
        step: 1,
        title: "Initial Consultation",
        description:
          "Share your birth details and specific life areas you'd like guidance on.",
      },
      {
        step: 2,
        title: "Chart Analysis",
        description:
          "Our astrologer prepares a detailed analysis of your birth chart, transits, and Dasha periods.",
      },
      {
        step: 3,
        title: "Guidance Session",
        description:
          "A 60-minute one-on-one session covering your chart insights, practical advice, and cosmic timing.",
      },
      {
        step: 4,
        title: "Action Plan",
        description:
          "Receive a personalized summary with remedies, timing recommendations, and actionable next steps.",
      },
    ],
    faqs: [
      {
        question: "How is this different from a regular astrology consultation?",
        answer:
          "Astrological Consulting is a holistic, growth-oriented service. Beyond predictions, it focuses on using cosmic wisdom for personal development, decision-making, and life alignment — combining traditional Vedic methods with a modern coaching perspective.",
      },
      {
        question: "What areas of life can I get guidance on?",
        answer:
          "Career transitions, relationship decisions, financial timing, health awareness, relocation, education choices, spiritual growth — any area where cosmic timing and planetary influences can offer clarity.",
      },
      {
        question: "Do I need to know anything about astrology beforehand?",
        answer:
          "Not at all. Our consulting is designed for everyone, from curious beginners to seasoned astrology enthusiasts. We explain everything in simple, practical terms.",
      },
    ],
  },
  {
    slug: "personal-growth-coaching",
    title: "Personal Growth Coaching",
    image: "https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=800&q=80",
    shortDescription:
      "Mindfulness, philosophy, and transformative practices. Guidance for personal development, building resilience, and creating a meaningful life aligned with your values.",
    description:
      "Our Personal Growth Coaching service blends ancient Vedic philosophy with modern personal development methodologies to help you unlock your fullest potential. Through guided sessions on mindfulness, self-awareness, and transformative practices, we support you in building resilience, overcoming limiting beliefs, and creating a life of purpose and meaning. Whether you're navigating a life transition, seeking clarity on your values, or working towards personal goals — our coaching provides the tools and guidance to help you grow authentically.",
    priceINR: "\u20B94,999",
    priceEUR: "\u20AC59",
    duration: "60 min",
    icon: "Leaf",
    category: "wellness",
    features: [
      "One-on-one personalized coaching session",
      "Mindfulness & meditation techniques",
      "Values clarification & goal setting",
      "Resilience & stress management tools",
      "Vedic philosophy for modern living",
      "Limiting belief identification & reframing",
      "Accountability & progress tracking",
      "Guided journaling & reflection exercises",
    ],
    process: [
      {
        step: 1,
        title: "Discovery Call",
        description:
          "A brief intake to understand your goals, challenges, and what you hope to achieve through coaching.",
      },
      {
        step: 2,
        title: "Personalized Plan",
        description:
          "Based on your discovery session, a tailored coaching plan is created focusing on your growth areas.",
      },
      {
        step: 3,
        title: "Coaching Session",
        description:
          "A 60-minute deep-dive session with practical exercises, mindfulness techniques, and actionable guidance.",
      },
      {
        step: 4,
        title: "Integration Support",
        description:
          "Receive follow-up resources, exercises, and a summary to integrate learnings into your daily life.",
      },
    ],
    faqs: [
      {
        question: "Is this related to astrology?",
        answer:
          "While our coaching is rooted in Vedic wisdom and philosophy, it focuses primarily on practical personal development — mindfulness, self-awareness, goal-setting, and building resilience. Astrological insights can be optionally integrated if desired.",
      },
      {
        question: "Who is this coaching suitable for?",
        answer:
          "Anyone seeking personal growth — whether you're going through a life transition, feeling stuck, wanting to build better habits, or simply looking to live more intentionally and aligned with your values.",
      },
      {
        question: "Can I book multiple sessions?",
        answer:
          "Absolutely. Many clients benefit from a series of sessions. We offer package options for ongoing coaching support with progress tracking between sessions.",
      },
    ],
  },
  {
    slug: "therapeutic-healing",
    title: "Therapeutic Healing",
    image: "https://images.unsplash.com/photo-1556760544-74068565f05c?w=800&q=80",
    shortDescription:
      "Professional therapeutic support for emotional well-being. Integrated counseling techniques, mindfulness practices, and transformative methodologies for genuine healing.",
    description:
      "Our Therapeutic Healing service provides compassionate, professional support for emotional well-being and inner transformation. Combining integrated counseling techniques, mindfulness-based practices, and transformative healing methodologies, we create a safe space for you to process emotions, release past patterns, and cultivate genuine inner peace. Whether you're dealing with stress, anxiety, grief, relationship challenges, or simply seeking deeper emotional balance — our therapeutic approach honors both modern psychology and ancient wisdom traditions to support your healing journey.",
    priceINR: "\u20B95,999",
    priceEUR: "\u20AC69",
    duration: "75 min",
    icon: "HeartHandshake",
    category: "wellness",
    features: [
      "75-minute private therapeutic session",
      "Integrated counseling techniques",
      "Mindfulness-based stress reduction",
      "Emotional processing & release work",
      "Trauma-informed approach",
      "Guided meditation & breathwork",
      "Coping strategies & self-care tools",
      "Confidential & compassionate space",
    ],
    process: [
      {
        step: 1,
        title: "Intake & Assessment",
        description:
          "Share your concerns and goals in a confidential intake form. This helps tailor the session to your needs.",
      },
      {
        step: 2,
        title: "Therapeutic Session",
        description:
          "A 75-minute session using integrated counseling, mindfulness, and healing techniques in a safe, supportive space.",
      },
      {
        step: 3,
        title: "Healing Practices",
        description:
          "Learn personalized mindfulness exercises, breathwork, and coping strategies to continue your healing between sessions.",
      },
      {
        step: 4,
        title: "Ongoing Support",
        description:
          "Receive a follow-up care plan with resources, practices, and recommendations for continued well-being.",
      },
    ],
    faqs: [
      {
        question: "Is this a substitute for clinical therapy or psychiatric care?",
        answer:
          "Our Therapeutic Healing service is a holistic wellness offering that complements professional mental health care. It is not a replacement for clinical therapy, psychiatry, or medical treatment. If you are in crisis, please contact a licensed mental health professional.",
      },
      {
        question: "What healing methodologies are used?",
        answer:
          "We integrate mindfulness-based cognitive techniques, breathwork, guided meditation, somatic awareness, and principles from Vedic wisdom traditions — all within a compassionate, trauma-informed framework.",
      },
      {
        question: "Is everything discussed kept confidential?",
        answer:
          "Absolutely. Confidentiality is foundational to our practice. Everything shared during sessions is kept strictly private and is never disclosed to third parties.",
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
