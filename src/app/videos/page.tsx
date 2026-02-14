import type { Metadata } from "next";
import { VideosContent } from "./VideosContent";

export const metadata: Metadata = {
  title: "Videos",
  description:
    "Watch VedicJivan's latest YouTube videos and shorts on Vedic astrology, numerology, Vastu, and spiritual growth.",
  alternates: { canonical: "/videos" },
  openGraph: {
    title: "Videos | VedicJivan",
    description:
      "Watch VedicJivan's latest YouTube videos and shorts on Vedic astrology, numerology, Vastu, and spiritual growth.",
    url: "/videos",
  },
};

export default function VideosPage() {
  return <VideosContent />;
}
