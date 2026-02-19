import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  test: {
    environment: "jsdom",
    pool: "threads",
    setupFiles: ["./src/__tests__/setup.tsx"],
    include: ["src/__tests__/**/*.test.{ts,tsx}"],
    coverage: {
      provider: "v8",
      include: ["src/lib/**", "src/components/booking/**", "src/app/admin/**"],
      exclude: ["src/__tests__/**"],
    },
  },
});
