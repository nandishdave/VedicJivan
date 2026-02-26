import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#f5f0ff",
          100: "#ede5ff",
          200: "#daccff",
          300: "#c4a6ff",
          400: "#b366ff",
          500: "#9333ea",
          600: "#7c3aed",
          700: "#6025c0",
          800: "#5119a8",
          900: "#441390",
          950: "#2a0b5e",
        },
        gold: {
          50: "#fff9eb",
          100: "#ffefc2",
          200: "#ffe08a",
          300: "#fbbf24",
          400: "#f5a623",
          500: "#e88d00",
          600: "#c96800",
          700: "#a34e04",
          800: "#873e08",
          900: "#72340c",
        },
        saffron: {
          300: "#fdba74",
          400: "#fb923c",
          500: "#f97316",
          600: "#ea580c",
        },
        cream: "#fdf8f0",
        vedic: {
          dark: "#1a0a2e",
          text: "#2d1b4e",
        },
      },
      fontFamily: {
        heading: ["var(--font-playfair)", "serif"],
        body: ["var(--font-inter)", "sans-serif"],
      },
      backgroundImage: {
        "vedic-gradient":
          "linear-gradient(135deg, #6025c0 0%, #9333ea 50%, #b366ff 100%)",
        "gold-gradient":
          "linear-gradient(135deg, #f5a623 0%, #e88d00 100%)",
        "dark-gradient":
          "linear-gradient(180deg, #1e0f3d 0%, #2d1b4e 100%)",
      },
      animation: {
        "fade-in": "fadeIn 0.6s ease-out forwards",
        "slide-up": "slideUp 0.6s ease-out forwards",
        "float": "float 6s ease-in-out infinite",
        "gradient-text": "gradientText 4s ease infinite",
        "slide-in-up": "slideInUp 0.5s cubic-bezier(0.16,1,0.3,1) forwards",
        "pulse-glow": "pulseGlow 2s ease-in-out infinite",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideUp: {
          "0%": { opacity: "0", transform: "translateY(30px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        float: {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-10px)" },
        },
        gradientText: {
          "0%, 100%": { backgroundPosition: "0% center" },
          "50%": { backgroundPosition: "100% center" },
        },
        slideInUp: {
          "0%": { opacity: "0", transform: "translateY(100%)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        pulseGlow: {
          "0%, 100%": { boxShadow: "0 0 8px 2px rgba(180, 130, 255, 0.4)" },
          "50%": { boxShadow: "0 0 20px 6px rgba(180, 130, 255, 0.7)" },
        },
      },
    },
  },
  plugins: [],
};
export default config;
