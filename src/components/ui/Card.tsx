"use client";

import { cn } from "@/lib/utils/cn";
import { motion } from "framer-motion";
import { HTMLAttributes } from "react";

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  hover?: boolean;
}

function Card({ className, hover = true, children }: CardProps) {
  if (!hover) {
    return (
      <div
        className={cn(
          "rounded-2xl border border-gray-100 bg-white p-6 shadow-sm",
          className
        )}
      >
        {children}
      </div>
    );
  }

  return (
    <motion.div
      whileHover={{
        y: -8,
        transition: { type: "spring", stiffness: 300, damping: 20 },
      }}
      className={cn(
        "group/card relative rounded-2xl border border-gray-100 bg-white p-6 shadow-sm transition-shadow duration-300 hover:border-primary-200 hover:shadow-xl hover:shadow-primary-200/40",
        className
      )}
    >
      {/* Top gradient accent line on hover */}
      <div className="absolute left-0 right-0 top-0 h-0.5 rounded-t-2xl bg-vedic-gradient opacity-0 transition-opacity duration-300 group-hover/card:opacity-100" />
      {children}
    </motion.div>
  );
}

function CardHeader({
  className,
  children,
  ...props
}: HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={cn("mb-4", className)} {...props}>
      {children}
    </div>
  );
}

function CardTitle({
  className,
  children,
  ...props
}: HTMLAttributes<HTMLHeadingElement>) {
  return (
    <h3
      className={cn(
        "font-heading text-xl font-bold text-vedic-dark",
        className
      )}
      {...props}
    >
      {children}
    </h3>
  );
}

function CardDescription({
  className,
  children,
  ...props
}: HTMLAttributes<HTMLParagraphElement>) {
  return (
    <p className={cn("text-sm text-gray-600", className)} {...props}>
      {children}
    </p>
  );
}

function CardContent({
  className,
  children,
  ...props
}: HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={cn(className)} {...props}>
      {children}
    </div>
  );
}

function CardFooter({
  className,
  children,
  ...props
}: HTMLAttributes<HTMLDivElement>) {
  return (
    <div className={cn("mt-4 pt-4 border-t border-gray-100", className)} {...props}>
      {children}
    </div>
  );
}

export { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter };
