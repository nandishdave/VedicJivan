import { cn } from "@/lib/utils/cn";
import { HTMLAttributes } from "react";

type BadgeVariant = "default" | "primary" | "gold" | "success" | "danger";

interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  variant?: BadgeVariant;
}

const variantStyles: Record<BadgeVariant, string> = {
  default: "bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300",
  primary: "bg-primary-100 text-primary-700 dark:bg-primary-900/30 dark:text-primary-300",
  gold: "bg-gold-100 text-gold-800 dark:bg-gold-900/30 dark:text-gold-300",
  success: "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300",
  danger: "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300",
};

function Badge({
  className,
  variant = "default",
  children,
  ...props
}: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold",
        variantStyles[variant],
        className
      )}
      {...props}
    >
      {children}
    </span>
  );
}

export { Badge };
