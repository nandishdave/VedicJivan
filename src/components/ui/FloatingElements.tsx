"use client";

import { motion } from "framer-motion";

function FloatingElements() {
  return (
    <div className="pointer-events-none absolute inset-0 overflow-hidden">
      {/* Large blurred orb - top left */}
      <motion.div
        className="absolute -left-20 -top-20 h-72 w-72 rounded-full bg-primary-500/10 blur-3xl"
        animate={{
          x: [0, 30, -10, 0],
          y: [0, -20, 15, 0],
          scale: [1, 1.1, 0.95, 1],
        }}
        transition={{
          duration: 12,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      />

      {/* Gold orb - bottom right */}
      <motion.div
        className="absolute -bottom-20 -right-20 h-80 w-80 rounded-full bg-gold-500/10 blur-3xl"
        animate={{
          x: [0, -25, 15, 0],
          y: [0, 20, -10, 0],
          scale: [1, 0.9, 1.1, 1],
        }}
        transition={{
          duration: 15,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      />

      {/* Small floating dot 1 */}
      <motion.div
        className="absolute left-[15%] top-[20%] h-2 w-2 rounded-full bg-gold-400/30"
        animate={{
          y: [0, -20, 0],
          opacity: [0.3, 0.7, 0.3],
        }}
        transition={{
          duration: 4,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      />

      {/* Small floating dot 2 */}
      <motion.div
        className="absolute right-[20%] top-[30%] h-3 w-3 rounded-full bg-primary-400/20"
        animate={{
          y: [0, 15, 0],
          x: [0, -10, 0],
          opacity: [0.2, 0.5, 0.2],
        }}
        transition={{
          duration: 5,
          repeat: Infinity,
          ease: "easeInOut",
          delay: 1,
        }}
      />

      {/* Small floating dot 3 */}
      <motion.div
        className="absolute bottom-[25%] left-[30%] h-2 w-2 rounded-full bg-gold-400/25"
        animate={{
          y: [0, -15, 0],
          x: [0, 8, 0],
          opacity: [0.2, 0.6, 0.2],
        }}
        transition={{
          duration: 6,
          repeat: Infinity,
          ease: "easeInOut",
          delay: 2,
        }}
      />

      {/* Floating ring */}
      <motion.div
        className="absolute right-[10%] top-[15%] h-16 w-16 rounded-full border border-gold-400/10"
        animate={{
          rotate: [0, 360],
          scale: [1, 1.15, 1],
        }}
        transition={{
          rotate: { duration: 20, repeat: Infinity, ease: "linear" },
          scale: { duration: 8, repeat: Infinity, ease: "easeInOut" },
        }}
      />

      {/* Floating ring 2 */}
      <motion.div
        className="absolute bottom-[15%] left-[8%] h-24 w-24 rounded-full border border-primary-400/10"
        animate={{
          rotate: [360, 0],
          scale: [1, 0.9, 1],
        }}
        transition={{
          rotate: { duration: 25, repeat: Infinity, ease: "linear" },
          scale: { duration: 10, repeat: Infinity, ease: "easeInOut" },
        }}
      />

      {/* Drifting sparkle particles */}
      {[...Array(6)].map((_, i) => (
        <motion.div
          key={`sparkle-${i}`}
          className="absolute h-1 w-1 rounded-full bg-gold-400/40"
          style={{
            left: `${15 + i * 15}%`,
            bottom: `${10 + (i % 3) * 20}%`,
          }}
          animate={{
            y: [0, -60, -120],
            opacity: [0, 0.8, 0],
            scale: [0.5, 1, 0.5],
          }}
          transition={{
            duration: 4 + i * 0.5,
            repeat: Infinity,
            delay: i * 0.8,
            ease: "easeOut",
          }}
        />
      ))}
    </div>
  );
}

export { FloatingElements };
