import { cn } from "@/lib/utils/cn";

interface GradientTextProps {
  children: React.ReactNode;
  variant?: "purple" | "gold" | "mixed";
  animated?: boolean;
  className?: string;
}

function GradientText({
  children,
  variant = "mixed",
  animated = true,
  className,
}: GradientTextProps) {
  return (
    <span
      className={cn(
        "bg-clip-text text-transparent",
        variant === "purple" &&
          "bg-gradient-to-r from-primary-400 via-primary-600 to-primary-400",
        variant === "gold" &&
          "bg-gradient-to-r from-gold-300 via-gold-500 to-gold-300",
        variant === "mixed" &&
          "bg-gradient-to-r from-gold-400 via-primary-500 to-gold-400",
        animated && "animate-gradient-text bg-[length:200%_auto]",
        className
      )}
    >
      {children}
    </span>
  );
}

export { GradientText };
