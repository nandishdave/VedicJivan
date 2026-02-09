"use client";

import { motion, type Variants } from "framer-motion";
import { useInView } from "react-intersection-observer";
import { cn } from "@/lib/utils/cn";

type AnimationType = "fadeUp" | "fadeIn" | "fadeLeft" | "fadeRight" | "scaleIn";

interface AnimateOnScrollProps {
  children: React.ReactNode;
  animation?: AnimationType;
  delay?: number;
  duration?: number;
  className?: string;
  once?: boolean;
}

const animations: Record<AnimationType, Variants> = {
  fadeUp: {
    hidden: { opacity: 0, y: 40 },
    visible: { opacity: 1, y: 0 },
  },
  fadeIn: {
    hidden: { opacity: 0 },
    visible: { opacity: 1 },
  },
  fadeLeft: {
    hidden: { opacity: 0, x: -40 },
    visible: { opacity: 1, x: 0 },
  },
  fadeRight: {
    hidden: { opacity: 0, x: 40 },
    visible: { opacity: 1, x: 0 },
  },
  scaleIn: {
    hidden: { opacity: 0, scale: 0.9 },
    visible: { opacity: 1, scale: 1 },
  },
};

function AnimateOnScroll({
  children,
  animation = "fadeUp",
  delay = 0,
  duration = 0.6,
  className,
  once = true,
}: AnimateOnScrollProps) {
  const { ref, inView } = useInView({
    triggerOnce: once,
    threshold: 0.1,
  });

  return (
    <motion.div
      ref={ref}
      initial="hidden"
      animate={inView ? "visible" : "hidden"}
      variants={animations[animation]}
      transition={{ duration, delay, ease: "easeOut" }}
      className={cn(className)}
    >
      {children}
    </motion.div>
  );
}

export { AnimateOnScroll };
