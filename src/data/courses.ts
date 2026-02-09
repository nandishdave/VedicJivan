export interface Course {
  slug: string;
  title: string;
  shortDescription: string;
  description: string;
  priceINR: string;
  priceEUR: string;
  level: "Beginner" | "Intermediate" | "Advanced";
  category: string;
  duration: string;
  lessons: number;
  students: number;
  rating: number;
  curriculum: { module: string; lessons: string[] }[];
  features: string[];
  whatYouLearn: string[];
}

export const courses: Course[] = [
  {
    slug: "vedic-astrology-basics",
    title: "Vedic Astrology Basics",
    shortDescription:
      "Learn the fundamentals of Vedic astrology — planets, houses, signs, and basic chart reading.",
    description:
      "Start your journey into the ancient science of Jyotish Shastra with this comprehensive beginner course. You'll learn about the 9 planets (Navagraha), 12 zodiac signs (Rashis), 12 houses (Bhavas), and 27 Nakshatras. By the end, you'll be able to read a basic birth chart and understand planetary influences in your own life.",
    priceINR: "\u20B94,999",
    priceEUR: "\u20AC59",
    level: "Beginner",
    category: "Astrology",
    duration: "12 hours",
    lessons: 24,
    students: 1250,
    rating: 4.8,
    curriculum: [
      {
        module: "Introduction to Vedic Astrology",
        lessons: [
          "What is Jyotish Shastra?",
          "Difference between Vedic and Western astrology",
          "The cosmic connection — karma and destiny",
        ],
      },
      {
        module: "The 9 Planets (Navagraha)",
        lessons: [
          "Sun, Moon & Mars — qualities and significations",
          "Mercury, Jupiter & Venus — qualities and significations",
          "Saturn, Rahu & Ketu — qualities and significations",
          "Planetary friendships and enmities",
        ],
      },
      {
        module: "The 12 Signs (Rashis)",
        lessons: [
          "Fire & Earth signs — Aries, Taurus, Leo, Virgo, Sagittarius, Capricorn",
          "Air & Water signs — Gemini, Cancer, Libra, Scorpio, Aquarius, Pisces",
          "Sign lords and characteristics",
        ],
      },
      {
        module: "The 12 Houses (Bhavas)",
        lessons: [
          "Houses 1-4: Self, wealth, siblings, home",
          "Houses 5-8: Children, enemies, spouse, longevity",
          "Houses 9-12: Fortune, career, gains, liberation",
          "House lords and their significance",
        ],
      },
      {
        module: "Reading Your First Chart",
        lessons: [
          "Understanding the North & South Indian chart formats",
          "Identifying planetary placements",
          "Basic chart interpretation exercise",
          "Practice with example charts",
        ],
      },
    ],
    features: [
      "12 hours of HD video content",
      "Certificate of completion",
      "Lifetime access to materials",
      "Practice charts and worksheets",
      "Community discussion forum",
    ],
    whatYouLearn: [
      "Understand the fundamental principles of Vedic astrology",
      "Identify planets, signs, and houses in a birth chart",
      "Read and interpret a basic Kundli",
      "Understand planetary strengths and weaknesses",
      "Apply basic astrology to everyday life decisions",
    ],
  },
  {
    slug: "kundli-mastery",
    title: "Kundli Mastery Course",
    shortDescription:
      "Deep dive into Kundli reading — Dashas, Yogas, Doshas, transits, and predictive techniques.",
    description:
      "Take your astrology skills to the next level with this intermediate course focused on predictive techniques. Master the Vimshottari Dasha system, learn to identify powerful Yogas and challenging Doshas, understand planetary transits, and develop the ability to make accurate predictions. Includes live Q&A sessions and practice with real charts.",
    priceINR: "\u20B99,999",
    priceEUR: "\u20AC119",
    level: "Intermediate",
    category: "Astrology",
    duration: "24 hours",
    lessons: 36,
    students: 680,
    rating: 4.9,
    curriculum: [
      {
        module: "Planetary Strengths",
        lessons: [
          "Shadbala — the six strengths of planets",
          "Exaltation, debilitation & Moolatrikona",
          "Combustion, retrogression & aspects",
          "Dig Bala & directional strength",
        ],
      },
      {
        module: "The Dasha System",
        lessons: [
          "Vimshottari Dasha — complete understanding",
          "Mahadasha, Antardasha & Pratyantardasha",
          "Predicting events from Dasha periods",
          "Dasha analysis with real examples",
        ],
      },
      {
        module: "Yogas & Special Combinations",
        lessons: [
          "Raj Yoga — combinations for power & success",
          "Dhan Yoga — wealth combinations",
          "Viparit Raj Yoga & Neech Bhang Raj Yoga",
          "Negative yogas — Kaal Sarpa, Grahan, Pitra Dosha",
        ],
      },
      {
        module: "Doshas & Remedies",
        lessons: [
          "Mangal Dosha — analysis and remedies",
          "Shani Sade Sati — understanding Saturn's transit",
          "Kaal Sarpa Dosha & Pitra Dosha",
          "Gemstones, mantras & ritual remedies",
        ],
      },
      {
        module: "Transits & Predictions",
        lessons: [
          "Understanding planetary transits (Gochar)",
          "Transit effects through houses",
          "Combining Dasha with transits for predictions",
          "Annual predictions using Varshaphal",
        ],
      },
      {
        module: "Live Practice Sessions",
        lessons: [
          "Chart reading workshop — career predictions",
          "Chart reading workshop — marriage & relationships",
          "Chart reading workshop — health & timing events",
          "Final assessment & certification",
        ],
      },
    ],
    features: [
      "24 hours of in-depth video content",
      "Live Q&A sessions (monthly)",
      "Real chart practice with solutions",
      "Advanced certificate of completion",
      "Direct access to instructor for doubts",
      "Bonus: 100+ practice charts",
    ],
    whatYouLearn: [
      "Master the Vimshottari Dasha system for timing events",
      "Identify Raj Yogas, Dhan Yogas, and Doshas in any chart",
      "Make accurate predictions using Dashas and transits",
      "Recommend appropriate remedies for planetary afflictions",
      "Analyze career, marriage, and health from a birth chart",
      "Prepare a complete Kundli analysis report",
    ],
  },
  {
    slug: "professional-numerology",
    title: "Professional Numerology",
    shortDescription:
      "Master the science of numbers. Learn name correction, lucky numbers, and business numerology.",
    description:
      "Become a professional numerologist with this comprehensive course covering Pythagorean and Chaldean systems. Learn to calculate and interpret Life Path Numbers, Expression Numbers, Soul Urge Numbers, and more. Master the art of name correction, business name analysis, and personal year predictions. Ideal for beginners and practitioners looking to add numerology to their skill set.",
    priceINR: "\u20B93,999",
    priceEUR: "\u20AC49",
    level: "Beginner",
    category: "Numerology",
    duration: "8 hours",
    lessons: 16,
    students: 890,
    rating: 4.7,
    curriculum: [
      {
        module: "Foundations of Numerology",
        lessons: [
          "History and principles of numerology",
          "Pythagorean vs Chaldean systems",
          "Numbers 1-9: meanings and vibrations",
          "Master Numbers: 11, 22, 33",
        ],
      },
      {
        module: "Core Numbers",
        lessons: [
          "Life Path Number — calculation and meaning",
          "Expression Number — your natural abilities",
          "Soul Urge Number — your inner desires",
          "Personality Number — how others see you",
        ],
      },
      {
        module: "Predictive Numerology",
        lessons: [
          "Personal Year, Month & Day calculations",
          "Pinnacle & Challenge numbers",
          "Lucky numbers, colors & days",
          "Timing important life events",
        ],
      },
      {
        module: "Practical Applications",
        lessons: [
          "Name correction techniques",
          "Business name numerology",
          "Compatibility analysis by numbers",
          "Building a numerology consultation practice",
        ],
      },
    ],
    features: [
      "8 hours of focused content",
      "Real case studies and examples",
      "Certificate of completion",
      "Name correction templates",
      "Lifetime access",
    ],
    whatYouLearn: [
      "Calculate all core numerology numbers accurately",
      "Interpret personality traits from numbers",
      "Predict favorable and challenging periods",
      "Perform name corrections for individuals and businesses",
      "Conduct professional numerology consultations",
    ],
  },
  {
    slug: "vastu-shastra-fundamentals",
    title: "Vastu Shastra Fundamentals",
    shortDescription:
      "Learn the ancient science of architecture and space energy. Practical Vastu for homes and offices.",
    description:
      "Discover the ancient Indian science of architecture and spatial harmony. This course teaches you the principles of Vastu Shastra — directional influences, five elements, energy flow, and practical remedies. Learn to analyze any property for Vastu compliance and suggest non-structural corrections. Perfect for homeowners, real estate professionals, and aspiring Vastu consultants.",
    priceINR: "\u20B95,999",
    priceEUR: "\u20AC69",
    level: "Beginner",
    category: "Vastu",
    duration: "10 hours",
    lessons: 20,
    students: 520,
    rating: 4.6,
    curriculum: [
      {
        module: "Introduction to Vastu Shastra",
        lessons: [
          "Origins and philosophy of Vastu",
          "The five elements (Pancha Tatva)",
          "8 directions and their deities",
          "The Vastu Purusha Mandala",
        ],
      },
      {
        module: "Residential Vastu",
        lessons: [
          "Main entrance — direction and placement",
          "Kitchen, bedroom & living room Vastu",
          "Bathroom, pooja room & study room",
          "Garden, parking & underground water tank",
        ],
      },
      {
        module: "Commercial Vastu",
        lessons: [
          "Office layout and desk placement",
          "Shop & showroom Vastu principles",
          "Factory & industrial Vastu",
          "Financial growth through Vastu",
        ],
      },
      {
        module: "Remedies & Corrections",
        lessons: [
          "Non-structural Vastu remedies",
          "Color therapy in Vastu",
          "Crystal and pyramid placements",
          "Vastu for rented properties",
        ],
      },
    ],
    features: [
      "10 hours of practical content",
      "Real property case studies",
      "Floor plan analysis templates",
      "Certificate of completion",
      "Lifetime access",
    ],
    whatYouLearn: [
      "Understand the core principles of Vastu Shastra",
      "Analyze any property for Vastu compliance",
      "Suggest practical remedies without demolition",
      "Apply Vastu principles to homes and offices",
      "Start offering Vastu consultation services",
    ],
  },
];

export function getCourseBySlug(slug: string): Course | undefined {
  return courses.find((c) => c.slug === slug);
}
