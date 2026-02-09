"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronDown } from "lucide-react";
import { cn } from "@/lib/utils/cn";

interface FAQItem {
  question: string;
  answer: string;
}

interface FAQAccordionProps {
  items: FAQItem[];
  className?: string;
}

function FAQAccordion({ items, className }: FAQAccordionProps) {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  return (
    <div className={cn("space-y-3", className)}>
      {items.map((item, i) => {
        const isOpen = openIndex === i;
        return (
          <motion.div
            key={i}
            initial={false}
            className={cn(
              "rounded-2xl border bg-white transition-colors",
              isOpen ? "border-primary-200 shadow-md shadow-primary-100/50" : "border-gray-200"
            )}
          >
            <button
              onClick={() => setOpenIndex(isOpen ? null : i)}
              className="flex w-full items-center justify-between p-5 text-left sm:p-6"
            >
              <span className="pr-4 font-semibold text-vedic-dark">
                {item.question}
              </span>
              <motion.div
                animate={{ rotate: isOpen ? 180 : 0 }}
                transition={{ duration: 0.3, ease: "easeInOut" }}
              >
                <ChevronDown className="h-5 w-5 shrink-0 text-gray-400" />
              </motion.div>
            </button>

            <AnimatePresence initial={false}>
              {isOpen && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: "auto", opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: 0.3, ease: "easeInOut" }}
                  className="overflow-hidden"
                >
                  <div className="border-t border-gray-100 px-5 pb-5 pt-4 text-sm leading-relaxed text-gray-600 sm:px-6 sm:pb-6">
                    {item.answer}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>
        );
      })}
    </div>
  );
}

export { FAQAccordion };
