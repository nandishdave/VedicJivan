export interface Testimonial {
  name: string;
  title: string;
  content: string;
  rating: number;
  service: string;
}

export const testimonials: Testimonial[] = [
  {
    name: "Priya Sharma",
    title: "Mumbai, India",
    content:
      "The Kundli report was incredibly detailed and accurate. The remedies suggested for my career helped me land my dream job within 3 months. Highly recommended!",
    rating: 5,
    service: "Premium Kundli Report",
  },
  {
    name: "Rajesh Kumar",
    title: "London, UK",
    content:
      "I was skeptical at first, but the video consultation changed my perspective. The astrologer identified issues I was facing and provided practical solutions.",
    rating: 5,
    service: "Video Consultation",
  },
  {
    name: "Anita Desai",
    title: "New Delhi, India",
    content:
      "The matchmaking service was thorough and gave us complete confidence in our decision. The detailed analysis of both charts was very insightful.",
    rating: 5,
    service: "Kundli Matching",
  },
  {
    name: "Vikram Singh",
    title: "Dubai, UAE",
    content:
      "The Vastu consultation for our new office was a game-changer. Simple changes in arrangement and colors made a noticeable difference in team productivity.",
    rating: 5,
    service: "Vastu Consultation",
  },
  {
    name: "Meera Patel",
    title: "Bangalore, India",
    content:
      "I've been learning through VedicJivan's courses for 6 months now. The quality of teaching is exceptional — I can now read basic charts on my own!",
    rating: 5,
    service: "Vedic Astrology Basics Course",
  },
  {
    name: "David Morrison",
    title: "Berlin, Germany",
    content:
      "As a European exploring Vedic astrology, I was impressed by how the consultation was tailored to my Western perspective while staying authentic to Vedic traditions.",
    rating: 5,
    service: "Call Consultation",
  },
];
