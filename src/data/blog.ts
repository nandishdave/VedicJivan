export interface BlogPost {
  slug: string;
  title: string;
  excerpt: string;
  category: string;
  author: string;
  date: string;
  readTime: string;
  featured?: boolean;
  tags: string[];
}

export const blogPosts: BlogPost[] = [
  {
    slug: "understanding-your-birth-chart",
    title: "Understanding Your Birth Chart: A Complete Beginner's Guide",
    excerpt:
      "Your birth chart is a cosmic snapshot of the sky at the exact moment you were born. Learn how to read the planets, houses, and signs that shape your destiny.",
    category: "Astrology Basics",
    author: "Nandish Dave",
    date: "2025-01-15",
    readTime: "8 min read",
    featured: true,
    tags: ["birth chart", "kundli", "beginners", "astrology basics"],
  },
  {
    slug: "saturn-sade-sati-guide",
    title: "Saturn's Sade Sati: What It Means and How to Navigate It",
    excerpt:
      "Sade Sati is one of the most feared transit periods in Vedic astrology. But is it really all bad? Learn what happens during Sade Sati and effective remedies.",
    category: "Planetary Transits",
    author: "Nandish Dave",
    date: "2025-01-08",
    readTime: "10 min read",
    tags: ["saturn", "sade sati", "transits", "remedies"],
  },
  {
    slug: "mangal-dosha-truth",
    title: "Mangal Dosha: Separating Facts from Myths",
    excerpt:
      "Mangal Dosha affects nearly 50% of people. Before panicking, understand what it truly means, when it matters, and the genuine remedies that work.",
    category: "Doshas & Remedies",
    author: "Nandish Dave",
    date: "2024-12-28",
    readTime: "7 min read",
    tags: ["mangal dosha", "marriage", "remedies", "myths"],
  },
  {
    slug: "career-astrology-guide",
    title: "Career Guidance Through Astrology: Finding Your True Calling",
    excerpt:
      "Which career suits you according to your birth chart? Learn how the 10th house, its lord, and planetary placements can guide your professional path.",
    category: "Career & Finance",
    author: "Nandish Dave",
    date: "2024-12-20",
    readTime: "9 min read",
    tags: ["career", "10th house", "profession", "guidance"],
  },
  {
    slug: "gemstone-guide-vedic-astrology",
    title: "The Complete Guide to Gemstones in Vedic Astrology",
    excerpt:
      "Gemstones can amplify planetary energies in your chart. But wearing the wrong stone can be harmful. Learn which gemstone suits your chart and how to wear it.",
    category: "Remedies",
    author: "Nandish Dave",
    date: "2024-12-12",
    readTime: "11 min read",
    tags: ["gemstones", "remedies", "planets", "healing"],
  },
  {
    slug: "numerology-life-path-number",
    title: "Your Life Path Number: What It Reveals About Your Destiny",
    excerpt:
      "Your Life Path Number is the most important number in numerology. Calculate yours and discover what it reveals about your personality, purpose, and life journey.",
    category: "Numerology",
    author: "Nandish Dave",
    date: "2024-12-05",
    readTime: "6 min read",
    tags: ["numerology", "life path", "destiny", "numbers"],
  },
  {
    slug: "vastu-tips-home",
    title: "10 Essential Vastu Tips for a Harmonious Home",
    excerpt:
      "Simple Vastu changes can transform the energy of your home. Here are 10 practical tips you can implement today without any structural modifications.",
    category: "Vastu",
    author: "Nandish Dave",
    date: "2024-11-28",
    readTime: "5 min read",
    tags: ["vastu", "home", "tips", "energy"],
  },
  {
    slug: "rahu-ketu-nodes-astrology",
    title: "Rahu and Ketu: The Shadow Planets That Shape Your Karma",
    excerpt:
      "Rahu and Ketu are the most mysterious forces in Vedic astrology. Understand their role in your chart, their effects in different houses, and how to manage them.",
    category: "Planetary Transits",
    author: "Nandish Dave",
    date: "2024-11-20",
    readTime: "12 min read",
    tags: ["rahu", "ketu", "nodes", "karma", "planets"],
  },
  {
    slug: "marriage-prediction-astrology",
    title: "Marriage Prediction in Astrology: Timing and Compatibility",
    excerpt:
      "When will you get married? Vedic astrology can predict marriage timing using the 7th house, Venus, Jupiter, and Dasha periods. Learn the key indicators.",
    category: "Relationships",
    author: "Nandish Dave",
    date: "2024-11-12",
    readTime: "8 min read",
    tags: ["marriage", "relationships", "7th house", "venus", "prediction"],
  },
];

export const blogCategories = [
  "All",
  "Astrology Basics",
  "Planetary Transits",
  "Doshas & Remedies",
  "Career & Finance",
  "Remedies",
  "Numerology",
  "Vastu",
  "Relationships",
];

export function getBlogPostBySlug(slug: string): BlogPost | undefined {
  return blogPosts.find((p) => p.slug === slug);
}

export function getRelatedPosts(currentSlug: string): BlogPost[] {
  const current = getBlogPostBySlug(currentSlug);
  if (!current) return blogPosts.slice(0, 3);
  return blogPosts
    .filter((p) => p.slug !== currentSlug)
    .filter((p) => p.category === current.category || p.tags.some((t) => current.tags.includes(t)))
    .slice(0, 3);
}
