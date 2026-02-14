"use client";

import { MessageCircle } from "lucide-react";
import { motion } from "framer-motion";
import { siteConfig } from "@/config/site";

export function WhatsAppFloat() {
  return (
    <motion.a
      href={`https://wa.me/${siteConfig.contact.whatsapp}`}
      target="_blank"
      rel="noopener noreferrer"
      aria-label="Chat on WhatsApp"
      className="fixed bottom-6 right-6 z-50 flex h-14 w-14 items-center justify-center rounded-full bg-green-500 text-white shadow-lg shadow-green-500/30 transition-colors hover:bg-green-600 lg:hidden"
      initial={{ scale: 0, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ delay: 1, type: "spring", stiffness: 300, damping: 20 }}
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.95 }}
    >
      <MessageCircle className="h-7 w-7" />
    </motion.a>
  );
}
