// Google Analytics event tracking utility
// Use these functions to track custom user interactions

type GAEvent = {
  action: string;
  category: string;
  label?: string;
  value?: number;
};

export function trackEvent({ action, category, label, value }: GAEvent) {
  if (typeof window === "undefined" || !window.gtag) return;
  window.gtag("event", action, {
    event_category: category,
    event_label: label,
    value,
  });
}

// Pre-built event helpers for common interactions

export function trackButtonClick(buttonName: string, page?: string) {
  trackEvent({
    action: "button_click",
    category: "engagement",
    label: `${buttonName}${page ? ` | ${page}` : ""}`,
  });
}

export function trackFormSubmit(formName: string) {
  trackEvent({
    action: "form_submit",
    category: "conversion",
    label: formName,
  });
}

export function trackServiceView(serviceName: string) {
  trackEvent({
    action: "service_view",
    category: "engagement",
    label: serviceName,
  });
}

export function trackCourseView(courseName: string) {
  trackEvent({
    action: "course_view",
    category: "engagement",
    label: courseName,
  });
}

export function trackSocialClick(platform: string) {
  trackEvent({
    action: "social_click",
    category: "engagement",
    label: platform,
  });
}

export function trackWhatsAppClick() {
  trackEvent({
    action: "whatsapp_click",
    category: "conversion",
    label: "whatsapp_chat",
  });
}

export function trackPhoneClick() {
  trackEvent({
    action: "phone_click",
    category: "conversion",
    label: "phone_call",
  });
}

export function trackCTAClick(ctaName: string, page: string) {
  trackEvent({
    action: "cta_click",
    category: "conversion",
    label: `${ctaName} | ${page}`,
  });
}

export function trackScrollDepth(depth: number, page: string) {
  trackEvent({
    action: "scroll_depth",
    category: "engagement",
    label: page,
    value: depth,
  });
}
