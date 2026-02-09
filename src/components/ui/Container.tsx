import { cn } from "@/lib/utils/cn";
import { HTMLAttributes } from "react";

interface ContainerProps extends HTMLAttributes<HTMLDivElement> {
  size?: "default" | "narrow" | "wide";
}

function Container({
  className,
  size = "default",
  children,
  ...props
}: ContainerProps) {
  return (
    <div
      className={cn(
        "mx-auto w-full px-4 sm:px-6 lg:px-8",
        size === "narrow" && "max-w-4xl",
        size === "default" && "max-w-7xl",
        size === "wide" && "max-w-[1400px]",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}

export { Container };
