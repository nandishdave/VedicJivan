import { cn } from "@/lib/utils/cn";

interface SectionDividerProps {
  variant?: "wave" | "gradient-line" | "dots";
  flip?: boolean;
  className?: string;
}

function SectionDivider({
  variant = "gradient-line",
  flip = false,
  className,
}: SectionDividerProps) {
  if (variant === "wave") {
    return (
      <div className={cn("overflow-hidden", flip && "rotate-180", className)}>
        <svg
          viewBox="0 0 1440 80"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          className="w-full"
          preserveAspectRatio="none"
        >
          <path
            d="M0 40C240 80 480 0 720 40C960 80 1200 0 1440 40V80H0V40Z"
            className="fill-current text-cream"
          />
        </svg>
      </div>
    );
  }

  if (variant === "dots") {
    return (
      <div
        className={cn(
          "flex items-center justify-center gap-2 py-8",
          className
        )}
      >
        <div className="h-1.5 w-1.5 rounded-full bg-primary-300 animate-pulse" />
        <div className="h-2 w-2 rounded-full bg-gold-400 animate-pulse [animation-delay:0.2s]" />
        <div className="h-1.5 w-16 rounded-full bg-gold-gradient" />
        <div className="h-2 w-2 rounded-full bg-gold-400 animate-pulse [animation-delay:0.4s]" />
        <div className="h-1.5 w-1.5 rounded-full bg-primary-300 animate-pulse [animation-delay:0.6s]" />
      </div>
    );
  }

  // Default: gradient-line
  return (
    <div className={cn("flex items-center justify-center py-4", className)}>
      <div className="h-px w-24 bg-gradient-to-r from-transparent to-primary-300" />
      <div className="mx-3 h-2 w-2 rotate-45 bg-gold-gradient" />
      <div className="h-px w-24 bg-gradient-to-l from-transparent to-primary-300" />
    </div>
  );
}

export { SectionDivider };
