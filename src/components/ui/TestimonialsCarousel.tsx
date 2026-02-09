"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Star, ChevronLeft, ChevronRight, Quote } from "lucide-react";
import { cn } from "@/lib/utils/cn";

interface Testimonial {
  name: string;
  title: string;
  content: string;
  rating: number;
  service?: string;
}

interface TestimonialsCarouselProps {
  testimonials: Testimonial[];
}

function TestimonialsCarousel({ testimonials }: TestimonialsCarouselProps) {
  const [current, setCurrent] = useState(0);
  const [direction, setDirection] = useState(0);

  const next = () => {
    setDirection(1);
    setCurrent((prev) => (prev + 1) % testimonials.length);
  };

  const prev = () => {
    setDirection(-1);
    setCurrent(
      (prev) => (prev - 1 + testimonials.length) % testimonials.length
    );
  };

  const variants = {
    enter: (direction: number) => ({
      x: direction > 0 ? 200 : -200,
      opacity: 0,
      scale: 0.95,
    }),
    center: {
      x: 0,
      opacity: 1,
      scale: 1,
    },
    exit: (direction: number) => ({
      x: direction < 0 ? 200 : -200,
      opacity: 0,
      scale: 0.95,
    }),
  };

  const t = testimonials[current];

  return (
    <div className="mx-auto max-w-3xl">
      {/* Main Testimonial */}
      <div className="relative min-h-[280px] overflow-hidden rounded-2xl border border-white/10 bg-white/5 p-8 backdrop-blur-sm sm:p-10">
        <Quote className="absolute right-6 top-6 h-12 w-12 text-white/5" />

        <AnimatePresence mode="wait" custom={direction}>
          <motion.div
            key={current}
            custom={direction}
            variants={variants}
            initial="enter"
            animate="center"
            exit="exit"
            transition={{ type: "spring", stiffness: 300, damping: 30 }}
          >
            <div className="mb-4 flex gap-1">
              {[...Array(t.rating)].map((_, j) => (
                <Star
                  key={j}
                  className="h-5 w-5 fill-gold-400 text-gold-400"
                />
              ))}
            </div>

            <p className="text-lg italic leading-relaxed text-gray-200 sm:text-xl">
              &ldquo;{t.content}&rdquo;
            </p>

            <div className="mt-6 flex items-center gap-4">
              <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary-600 text-lg font-bold text-white">
                {t.name.charAt(0)}
              </div>
              <div>
                <p className="font-semibold text-white">{t.name}</p>
                <p className="text-sm text-gray-400">{t.title}</p>
                {t.service && (
                  <p className="text-xs text-gold-400">{t.service}</p>
                )}
              </div>
            </div>
          </motion.div>
        </AnimatePresence>
      </div>

      {/* Navigation */}
      <div className="mt-6 flex items-center justify-center gap-4">
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={prev}
          className="flex h-10 w-10 items-center justify-center rounded-full border border-white/20 text-white/60 transition-colors hover:border-gold-400 hover:text-gold-400"
          aria-label="Previous testimonial"
        >
          <ChevronLeft className="h-5 w-5" />
        </motion.button>

        <div className="flex gap-2">
          {testimonials.map((_, i) => (
            <button
              key={i}
              onClick={() => {
                setDirection(i > current ? 1 : -1);
                setCurrent(i);
              }}
              className={cn(
                "h-2 rounded-full transition-all duration-300",
                i === current
                  ? "w-8 bg-gold-400"
                  : "w-2 bg-white/20 hover:bg-white/40"
              )}
              aria-label={`Go to testimonial ${i + 1}`}
            />
          ))}
        </div>

        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={next}
          className="flex h-10 w-10 items-center justify-center rounded-full border border-white/20 text-white/60 transition-colors hover:border-gold-400 hover:text-gold-400"
          aria-label="Next testimonial"
        >
          <ChevronRight className="h-5 w-5" />
        </motion.button>
      </div>
    </div>
  );
}

export { TestimonialsCarousel };
