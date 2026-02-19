import { describe, it, expect, vi, beforeEach } from "vitest";
import {
  trackEvent,
  trackButtonClick,
  trackFormSubmit,
  trackServiceView,
  trackCourseView,
  trackSocialClick,
  trackWhatsAppClick,
  trackPhoneClick,
  trackCTAClick,
  trackScrollDepth,
} from "@/lib/analytics";

describe("analytics", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
    window.gtag = vi.fn();
  });

  describe("trackEvent", () => {
    it("calls window.gtag with correct parameters", () => {
      trackEvent({ action: "test_action", category: "test_cat", label: "test_label", value: 42 });
      expect(window.gtag).toHaveBeenCalledWith("event", "test_action", {
        event_category: "test_cat",
        event_label: "test_label",
        value: 42,
      });
    });

    it("does not call gtag when window.gtag is undefined", () => {
      const original = window.gtag;
      window.gtag = undefined as unknown as typeof window.gtag;
      // Should not throw
      trackEvent({ action: "test", category: "test" });
      window.gtag = original;
    });

    it("handles missing optional fields", () => {
      trackEvent({ action: "simple", category: "cat" });
      expect(window.gtag).toHaveBeenCalledWith("event", "simple", {
        event_category: "cat",
        event_label: undefined,
        value: undefined,
      });
    });
  });

  describe("trackButtonClick", () => {
    it("tracks button click with page", () => {
      trackButtonClick("cta-btn", "home");
      expect(window.gtag).toHaveBeenCalledWith("event", "button_click", {
        event_category: "engagement",
        event_label: "cta-btn | home",
        value: undefined,
      });
    });

    it("tracks button click without page", () => {
      trackButtonClick("menu");
      expect(window.gtag).toHaveBeenCalledWith("event", "button_click", {
        event_category: "engagement",
        event_label: "menu",
        value: undefined,
      });
    });
  });

  describe("trackFormSubmit", () => {
    it("tracks form submission", () => {
      trackFormSubmit("contact");
      expect(window.gtag).toHaveBeenCalledWith("event", "form_submit", {
        event_category: "conversion",
        event_label: "contact",
        value: undefined,
      });
    });
  });

  describe("trackServiceView", () => {
    it("tracks service view", () => {
      trackServiceView("call-consultation");
      expect(window.gtag).toHaveBeenCalledWith("event", "service_view", {
        event_category: "engagement",
        event_label: "call-consultation",
        value: undefined,
      });
    });
  });

  describe("trackCourseView", () => {
    it("tracks course view", () => {
      trackCourseView("vedic-astrology-101");
      expect(window.gtag).toHaveBeenCalledWith("event", "course_view", {
        event_category: "engagement",
        event_label: "vedic-astrology-101",
        value: undefined,
      });
    });
  });

  describe("trackSocialClick", () => {
    it("tracks social click", () => {
      trackSocialClick("instagram");
      expect(window.gtag).toHaveBeenCalledWith("event", "social_click", {
        event_category: "engagement",
        event_label: "instagram",
        value: undefined,
      });
    });
  });

  describe("trackWhatsAppClick", () => {
    it("tracks whatsapp click", () => {
      trackWhatsAppClick();
      expect(window.gtag).toHaveBeenCalledWith("event", "whatsapp_click", {
        event_category: "conversion",
        event_label: "whatsapp_chat",
        value: undefined,
      });
    });
  });

  describe("trackPhoneClick", () => {
    it("tracks phone click", () => {
      trackPhoneClick();
      expect(window.gtag).toHaveBeenCalledWith("event", "phone_click", {
        event_category: "conversion",
        event_label: "phone_call",
        value: undefined,
      });
    });
  });

  describe("trackCTAClick", () => {
    it("tracks CTA click with page", () => {
      trackCTAClick("book-now", "services");
      expect(window.gtag).toHaveBeenCalledWith("event", "cta_click", {
        event_category: "conversion",
        event_label: "book-now | services",
        value: undefined,
      });
    });
  });

  describe("trackScrollDepth", () => {
    it("tracks scroll depth with value", () => {
      trackScrollDepth(75, "home");
      expect(window.gtag).toHaveBeenCalledWith("event", "scroll_depth", {
        event_category: "engagement",
        event_label: "home",
        value: 75,
      });
    });
  });
});
