import { siteConfig } from "@/config/site";

interface JsonLdProps {
  data: Record<string, unknown>;
}

export function JsonLd({ data }: JsonLdProps) {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
    />
  );
}

export function OrganizationJsonLd() {
  const data = {
    "@context": "https://schema.org",
    "@type": "Organization",
    name: siteConfig.name,
    url: siteConfig.url,
    logo: `${siteConfig.url}/icon.svg`,
    description: siteConfig.description,
    contactPoint: {
      "@type": "ContactPoint",
      telephone: siteConfig.contact.phone,
      contactType: "customer service",
      email: siteConfig.contact.email,
      availableLanguage: ["English", "Hindi"],
    },
    sameAs: [
      siteConfig.social.instagram,
      siteConfig.social.youtube,
      siteConfig.social.facebook,
    ],
    address: {
      "@type": "PostalAddress",
      addressLocality: "New Delhi",
      addressCountry: "IN",
    },
  };

  return <JsonLd data={data} />;
}

export function WebSiteJsonLd() {
  const data = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    name: siteConfig.name,
    url: siteConfig.url,
    description: siteConfig.description,
    publisher: {
      "@type": "Organization",
      name: siteConfig.name,
      url: siteConfig.url,
    },
  };

  return <JsonLd data={data} />;
}

export function BreadcrumbJsonLd({
  items,
}: {
  items: { name: string; url: string }[];
}) {
  const data = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: items.map((item, index) => ({
      "@type": "ListItem",
      position: index + 1,
      name: item.name,
      item: item.url,
    })),
  };

  return <JsonLd data={data} />;
}

export function ServiceJsonLd({
  name,
  description,
  priceINR,
  url,
}: {
  name: string;
  description: string;
  priceINR: string;
  url: string;
}) {
  const numericPrice = priceINR.replace(/[^\d]/g, "");
  const data = {
    "@context": "https://schema.org",
    "@type": "Service",
    name,
    description,
    provider: {
      "@type": "Organization",
      name: siteConfig.name,
      url: siteConfig.url,
    },
    url,
    offers: {
      "@type": "Offer",
      price: numericPrice,
      priceCurrency: "INR",
      availability: "https://schema.org/InStock",
    },
  };

  return <JsonLd data={data} />;
}

export function CourseJsonLd({
  name,
  description,
  priceINR,
  url,
}: {
  name: string;
  description: string;
  priceINR: string;
  url: string;
}) {
  const numericPrice = priceINR.replace(/[^\d]/g, "");
  const data = {
    "@context": "https://schema.org",
    "@type": "Course",
    name,
    description,
    provider: {
      "@type": "Organization",
      name: siteConfig.name,
      url: siteConfig.url,
    },
    url,
    offers: {
      "@type": "Offer",
      price: numericPrice,
      priceCurrency: "INR",
      availability: "https://schema.org/InStock",
    },
  };

  return <JsonLd data={data} />;
}

export function PersonJsonLd() {
  const data = {
    "@context": "https://schema.org",
    "@type": "Person",
    name: "Nandish Dave",
    url: siteConfig.url,
    jobTitle: "Vedic Astrologer & Numerologist",
    worksFor: {
      "@type": "Organization",
      name: siteConfig.name,
      url: siteConfig.url,
    },
    sameAs: [
      siteConfig.social.instagram,
      siteConfig.social.youtube,
      siteConfig.social.facebook,
    ],
    knowsAbout: [
      "Vedic Astrology",
      "Numerology",
      "Vastu Shastra",
      "Kundli Reading",
      "Horoscope Analysis",
    ],
  };

  return <JsonLd data={data} />;
}

export function BlogPostJsonLd({
  title,
  excerpt,
  author,
  date,
  url,
}: {
  title: string;
  excerpt: string;
  author: string;
  date: string;
  url: string;
}) {
  const data = {
    "@context": "https://schema.org",
    "@type": "Article",
    headline: title,
    description: excerpt,
    author: {
      "@type": "Person",
      name: author,
      url: siteConfig.url,
    },
    publisher: {
      "@type": "Organization",
      name: siteConfig.name,
      url: siteConfig.url,
    },
    datePublished: date,
    url,
  };

  return <JsonLd data={data} />;
}

export function FAQJsonLd({
  faqs,
}: {
  faqs: { question: string; answer: string }[];
}) {
  const data = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: faqs.map((faq) => ({
      "@type": "Question",
      name: faq.question,
      acceptedAnswer: {
        "@type": "Answer",
        text: faq.answer,
      },
    })),
  };

  return <JsonLd data={data} />;
}
