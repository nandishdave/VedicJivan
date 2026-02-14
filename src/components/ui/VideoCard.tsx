"use client";

import { useState } from "react";
import { Play } from "lucide-react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils/cn";

interface VideoCardProps {
  id: string;
  title: string;
  thumbnail: string;
  publishedAt: string;
  variant?: "video" | "short";
}

export function VideoCard({
  id,
  title,
  thumbnail,
  publishedAt,
  variant = "video",
}: VideoCardProps) {
  const [playing, setPlaying] = useState(false);

  const isShort = variant === "short";
  const aspectClass = isShort ? "aspect-[9/16]" : "aspect-video";

  const formattedDate = new Date(publishedAt).toLocaleDateString("en-IN", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });

  return (
    <motion.div
      whileHover={{ y: -4 }}
      transition={{ type: "spring", stiffness: 300, damping: 20 }}
      className="group overflow-hidden rounded-2xl border border-gray-100 bg-white shadow-sm transition-shadow hover:shadow-lg"
    >
      <div className={cn("relative w-full overflow-hidden bg-gray-900", aspectClass)}>
        {playing ? (
          <iframe
            src={`https://www.youtube.com/embed/${id}?autoplay=1&rel=0`}
            title={title}
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
            className="absolute inset-0 h-full w-full"
          />
        ) : (
          <button
            onClick={() => setPlaying(true)}
            className="absolute inset-0 h-full w-full"
            aria-label={`Play ${title}`}
          >
            <img
              src={thumbnail}
              alt={title}
              className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
              loading="lazy"
            />
            <div className="absolute inset-0 flex items-center justify-center bg-black/20 transition-colors group-hover:bg-black/30">
              <div className="flex h-14 w-14 items-center justify-center rounded-full bg-red-600 text-white shadow-lg transition-transform group-hover:scale-110">
                <Play className="h-6 w-6 fill-current" />
              </div>
            </div>
          </button>
        )}
      </div>
      <div className="p-4">
        <h3 className="line-clamp-2 text-sm font-semibold text-vedic-dark">
          {title}
        </h3>
        <p className="mt-1 text-xs text-gray-500">{formattedDate}</p>
      </div>
    </motion.div>
  );
}

export function VideoCardSkeleton({ variant = "video" }: { variant?: "video" | "short" }) {
  const aspectClass = variant === "short" ? "aspect-[9/16]" : "aspect-video";
  return (
    <div className="overflow-hidden rounded-2xl border border-gray-100 bg-white shadow-sm">
      <div className={cn("w-full animate-pulse bg-gray-200", aspectClass)} />
      <div className="p-4 space-y-2">
        <div className="h-4 w-3/4 animate-pulse rounded bg-gray-200" />
        <div className="h-3 w-1/3 animate-pulse rounded bg-gray-200" />
      </div>
    </div>
  );
}
