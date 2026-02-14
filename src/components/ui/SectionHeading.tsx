"use client";

import { motion } from "framer-motion";
import { useInView } from "react-intersection-observer";
import { cn } from "@/lib/utils/cn";

interface SectionHeadingProps {
  subtitle?: string;
  title: string;
  description?: string;
  align?: "left" | "center";
  light?: boolean;
  className?: string;
}

function SectionHeading({
  subtitle,
  title,
  description,
  align = "center",
  light = false,
  className,
}: SectionHeadingProps) {
  const { ref, inView } = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });

  return (
    <div
      ref={ref}
      className={cn(
        "mb-12",
        align === "center" && "text-center",
        className
      )}
    >
      {subtitle && (
        <motion.div
          className={cn(
            "mb-3 flex items-center gap-3",
            align === "center" && "justify-center"
          )}
          initial={{ opacity: 0, y: 10 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.5, ease: "easeOut" }}
        >
          <div
            className={cn(
              "h-px w-8",
              light ? "bg-gold-400/50" : "bg-gold-500/50"
            )}
          />
          <span
            className={cn(
              "inline-block text-sm font-semibold uppercase tracking-widest",
              light ? "text-gold-400" : "text-gold-600"
            )}
          >
            {subtitle}
          </span>
          <div
            className={cn(
              "h-px w-8",
              light ? "bg-gold-400/50" : "bg-gold-500/50"
            )}
          />
        </motion.div>
      )}
      <motion.h2
        className={cn(
          "font-heading text-3xl font-bold sm:text-4xl lg:text-5xl",
          light ? "text-white" : "text-vedic-dark"
        )}
        initial={{ opacity: 0, y: 20 }}
        animate={inView ? { opacity: 1, y: 0 } : {}}
        transition={{ duration: 0.6, delay: 0.1, ease: "easeOut" }}
      >
        {title}
      </motion.h2>
      {description && (
        <motion.p
          className={cn(
            "mx-auto mt-4 max-w-2xl text-lg",
            light ? "text-gray-300" : "text-gray-600"
          )}
          initial={{ opacity: 0, y: 15 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.6, delay: 0.2, ease: "easeOut" }}
        >
          {description}
        </motion.p>
      )}
    </div>
  );
}

export { SectionHeading };
