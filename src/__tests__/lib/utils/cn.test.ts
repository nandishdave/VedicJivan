import { describe, it, expect } from "vitest";
import { cn } from "@/lib/utils/cn";

describe("cn", () => {
  it("merges class names", () => {
    expect(cn("foo", "bar")).toBe("foo bar");
  });

  it("handles conditional classes via clsx", () => {
    expect(cn("base", false && "hidden", "visible")).toBe("base visible");
  });

  it("merges tailwind classes correctly", () => {
    expect(cn("px-4 py-2", "px-8")).toBe("py-2 px-8");
  });

  it("handles undefined and null inputs", () => {
    expect(cn("foo", undefined, null, "bar")).toBe("foo bar");
  });

  it("handles empty inputs", () => {
    expect(cn()).toBe("");
  });

  it("merges conflicting tailwind colors", () => {
    expect(cn("text-red-500", "text-blue-500")).toBe("text-blue-500");
  });
});
