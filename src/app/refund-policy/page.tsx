import type { Metadata } from "next";
import { Container } from "@/components/ui/Container";

export const metadata: Metadata = {
  title: "Refund Policy",
  description: "VedicJivan's refund policy — understand our refund terms for consultations, reports, and courses.",
  alternates: { canonical: "/refund-policy" },
};

export default function RefundPolicyPage() {
  return (
    <>
      <section className="vedic-hero-gradient py-16 sm:py-20">
        <Container>
          <div className="mx-auto max-w-3xl text-center">
            <h1 className="font-heading text-3xl font-bold text-white sm:text-4xl lg:text-5xl">
              Refund Policy
            </h1>
            <p className="mt-4 text-gray-400">Last updated: January 1, 2025</p>
          </div>
        </Container>
      </section>

      <section className="vedic-section">
        <Container size="narrow">
          <div className="prose prose-lg max-w-none prose-headings:font-heading prose-headings:text-vedic-dark prose-p:text-gray-600 prose-li:text-gray-600 prose-strong:text-vedic-dark">
            <h2>1. Overview</h2>
            <p>
              At VedicJivan, we strive to provide the highest quality astrology
              services and educational content. This Refund Policy outlines the
              terms and conditions for refunds across our different service
              categories.
            </p>

            <h2>2. Consultation Refunds</h2>
            <h3>Phone & Video Consultations</h3>
            <ul>
              <li>
                <strong>Cancellation 48+ hours before appointment:</strong> Full
                refund, processed within 5-7 business days
              </li>
              <li>
                <strong>Cancellation 24-48 hours before appointment:</strong> 50%
                refund, or free rescheduling to another available slot
              </li>
              <li>
                <strong>Cancellation less than 24 hours before:</strong> No
                refund, but one-time free rescheduling may be offered at our
                discretion
              </li>
              <li>
                <strong>No-show:</strong> No refund will be provided
              </li>
              <li>
                <strong>Technical issues on our end:</strong> Full refund or free
                rescheduling, at your choice
              </li>
            </ul>

            <h3>Rescheduling</h3>
            <p>
              You may reschedule your appointment free of charge up to 24 hours
              before the scheduled time. Each booking allows up to 2 free
              reschedules. Additional reschedules may incur an administrative fee.
            </p>

            <h2>3. Report Refunds</h2>
            <h3>Kundli Reports, Numerology Reports & Matchmaking</h3>
            <ul>
              <li>
                <strong>Before report generation begins:</strong> Full refund if
                requested within 24 hours of placing the order
              </li>
              <li>
                <strong>After report generation has started:</strong> No refund,
                as the report involves significant manual effort by our astrologers
              </li>
              <li>
                <strong>Incorrect birth details:</strong> If incorrect details
                were provided by you, a revised report can be generated at 50% of
                the original price
              </li>
              <li>
                <strong>Quality issues:</strong> If you believe the report does
                not meet the described standards, contact us within 7 days of
                delivery for review
              </li>
            </ul>

            <h2>4. Course Refunds</h2>
            <ul>
              <li>
                <strong>Within 7 days of enrollment (less than 20% content accessed):</strong>{" "}
                Full refund
              </li>
              <li>
                <strong>Within 7 days of enrollment (more than 20% content accessed):</strong>{" "}
                50% refund
              </li>
              <li>
                <strong>After 7 days of enrollment:</strong> No refund, as you
                have lifetime access to the course materials
              </li>
              <li>
                <strong>Technical access issues:</strong> If you cannot access the
                course due to technical issues on our end, a full refund will be
                provided after troubleshooting attempts
              </li>
            </ul>

            <h2>5. How to Request a Refund</h2>
            <p>To request a refund, please:</p>
            <ol>
              <li>
                Email us at <strong>contact@vedicjivan.com</strong> with the
                subject line &ldquo;Refund Request — [Order ID]&rdquo;
              </li>
              <li>Include your name, order ID, and reason for the refund</li>
              <li>
                Our team will review your request and respond within 2 business
                days
              </li>
            </ol>

            <h2>6. Refund Processing</h2>
            <ul>
              <li>
                Approved refunds are processed within 5-7 business days
              </li>
              <li>
                Refunds are issued to the original payment method (credit card,
                debit card, UPI, etc.)
              </li>
              <li>
                For international payments (Stripe), the refund may take up to
                10 business days to reflect in your account
              </li>
              <li>
                Currency conversion fees charged by your bank are non-refundable
              </li>
            </ul>

            <h2>7. Non-Refundable Items</h2>
            <ul>
              <li>Completed consultations</li>
              <li>Delivered and accepted reports</li>
              <li>Courses accessed beyond the refund window</li>
              <li>Custom or expedited service fees</li>
              <li>Payment gateway transaction fees</li>
            </ul>

            <h2>8. Disputes</h2>
            <p>
              If you are not satisfied with our refund decision, you may escalate
              the matter by contacting us directly. We are committed to resolving
              disputes fairly and promptly.
            </p>

            <h2>9. Contact Us</h2>
            <p>
              For refund-related queries, please contact us at:
            </p>
            <ul>
              <li>Email: contact@vedicjivan.com</li>
              <li>Phone: +91 98765 43210</li>
              <li>Working Hours: Mon-Sat, 10:00 AM - 7:00 PM IST</li>
            </ul>
          </div>
        </Container>
      </section>
    </>
  );
}
