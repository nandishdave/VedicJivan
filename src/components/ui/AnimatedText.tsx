"use client";

import { motion } from "framer-motion";
import { useInView } from "react-intersection-observer";
import { cn } from "@/lib/utils/cn";

interface AnimatedTextProps {
  text: string;
  className?: string;
  once?: boolean;
  delay?: number;
  as?: "h1" | "h2" | "h3" | "p" | "span";
}

function AnimatedText({
  text,
  className,
  once = true,
  delay = 0,
  as: Tag = "h1",
}: AnimatedTextProps) {
  const { ref, inView } = useInView({
    triggerOnce: once,
    threshold: 0.1,
  });

  const words = text.split(" ");

  const container = {
    hidden: { opacity: 0 },
    visible: () => ({
      opacity: 1,
      transition: {
        staggerChildren: 0.08,
        delayChildren: delay,
      },
    }),
  };

  const child = {
    hidden: {
      opacity: 0,
      y: 20,
      filter: "blur(4px)",
    },
    visible: {
      opacity: 1,
      y: 0,
      filter: "blur(0px)",
      transition: {
        type: "spring" as const,
        damping: 12,
        stiffness: 100,
      },
    },
  };

  return (
    <motion.div
      ref={ref}
      className={cn("flex flex-wrap", className)}
      variants={container}
      initial="hidden"
      animate={inView ? "visible" : "hidden"}
    >
      {words.map((word, i) => (
        <motion.span
          key={i}
          variants={child}
          className="mr-[0.25em] inline-block"
        >
          {Tag === "h1" || Tag === "h2" || Tag === "h3" ? (
            <span className="font-heading">{word}</span>
          ) : (
            word
          )}
        </motion.span>
      ))}
    </motion.div>
  );
}

export { AnimatedText };
