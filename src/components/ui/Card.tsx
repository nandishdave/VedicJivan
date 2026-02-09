import { cn } from "@/lib/utils/cn";
import { HTMLAttributes } from "react";

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  hover?: boolean;
}

function Card({ className, hover = true, children, ...props }: CardProps) {
  return (
    <div
      className={cn(
        "rounded-2xl border border-gray-100 bg-white p-6 shadow-sm",
        hover &&
          "transition-all duration-300 hover:-translate-y-1 hover:shadow-lg hover:shadow-primary-100/50",
        className
      )}
      {...props}
    >
      {children}
    </div>
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
