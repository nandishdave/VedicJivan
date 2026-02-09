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
  return (
    <div
      className={cn(
        "mb-12",
        align === "center" && "text-center",
        className
      )}
    >
      {subtitle && (
        <span
          className={cn(
            "mb-3 inline-block text-sm font-semibold uppercase tracking-widest",
            light ? "text-gold-400" : "text-gold-600"
          )}
        >
          {subtitle}
        </span>
      )}
      <h2
        className={cn(
          "font-heading text-3xl font-bold sm:text-4xl lg:text-5xl",
          light ? "text-white" : "text-vedic-dark"
        )}
      >
        {title}
      </h2>
      {description && (
        <p
          className={cn(
            "mx-auto mt-4 max-w-2xl text-lg",
            light ? "text-gray-300" : "text-gray-600"
          )}
        >
          {description}
        </p>
      )}
    </div>
  );
}

export { SectionHeading };
