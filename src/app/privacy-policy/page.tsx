import type { Metadata } from "next";
import { Container } from "@/components/ui/Container";

export const metadata: Metadata = {
  title: "Privacy Policy",
  description: "VedicJivan's privacy policy — how we collect, use, and protect your personal information.",
  alternates: { canonical: "/privacy-policy" },
};

export default function PrivacyPolicyPage() {
  return (
    <>
      <section className="bg-dark-gradient py-16 sm:py-20">
        <Container>
          <div className="mx-auto max-w-3xl text-center">
            <h1 className="font-heading text-3xl font-bold text-white sm:text-4xl lg:text-5xl">
              Privacy Policy
            </h1>
            <p className="mt-4 text-gray-400">Last updated: January 1, 2025</p>
          </div>
        </Container>
      </section>

      <section className="vedic-section">
        <Container size="narrow">
          <div className="prose prose-lg max-w-none prose-headings:font-heading prose-headings:text-vedic-dark prose-p:text-gray-600 prose-li:text-gray-600 prose-strong:text-vedic-dark">
            <h2>1. Introduction</h2>
            <p>
              VedicJivan (&ldquo;we,&rdquo; &ldquo;our,&rdquo; or &ldquo;us&rdquo;) is committed to
              protecting your privacy. This Privacy Policy explains how we
              collect, use, disclose, and safeguard your information when you
              visit our website or use our services.
            </p>

            <h2>2. Information We Collect</h2>
            <h3>Personal Information</h3>
            <p>We may collect the following personal information:</p>
            <ul>
              <li>Name, email address, and phone number</li>
              <li>Date of birth, time of birth, and place of birth</li>
              <li>Payment information (processed securely by Razorpay/Stripe)</li>
              <li>Communication preferences</li>
              <li>Any information you provide during consultations</li>
            </ul>

            <h3>Automatically Collected Information</h3>
            <ul>
              <li>IP address and approximate location (for currency detection)</li>
              <li>Browser type and device information</li>
              <li>Pages visited and time spent on our website</li>
              <li>Cookies and similar tracking technologies</li>
            </ul>

            <h2>3. How We Use Your Information</h2>
            <p>We use your information to:</p>
            <ul>
              <li>Provide astrology consultations and generate reports</li>
              <li>Process payments and manage appointments</li>
              <li>Send appointment confirmations and reminders</li>
              <li>Deliver course content and track progress</li>
              <li>Respond to your inquiries and support requests</li>
              <li>Improve our website and services</li>
              <li>Send promotional emails (only with your consent)</li>
            </ul>

            <h2>4. Data Security</h2>
            <p>
              We implement appropriate technical and organizational measures to
              protect your personal data against unauthorized access, alteration,
              disclosure, or destruction. Payment data is handled exclusively by
              PCI-DSS compliant payment processors (Razorpay and Stripe).
            </p>

            <h2>5. Third-Party Services</h2>
            <p>
              We may share your data with trusted third-party services for the
              following purposes:
            </p>
            <ul>
              <li><strong>Payment Processing:</strong> Razorpay (India) and Stripe (International)</li>
              <li><strong>Email Communication:</strong> For sending transactional emails</li>
              <li><strong>Analytics:</strong> To understand website usage patterns</li>
              <li><strong>Cloud Storage:</strong> For secure data storage</li>
            </ul>
            <p>We do not sell your personal information to third parties.</p>

            <h2>6. Your Rights</h2>
            <p>You have the right to:</p>
            <ul>
              <li>Access and receive a copy of your personal data</li>
              <li>Request correction of inaccurate data</li>
              <li>Request deletion of your data (subject to legal requirements)</li>
              <li>Withdraw consent for marketing communications</li>
              <li>Lodge a complaint with a data protection authority</li>
            </ul>

            <h2>7. Cookies</h2>
            <p>
              We use cookies to improve your browsing experience, analyze website
              traffic, and personalize content. You can control cookie preferences
              through your browser settings.
            </p>

            <h2>8. Data Retention</h2>
            <p>
              We retain your personal data for as long as necessary to fulfill the
              purposes outlined in this policy, or as required by law. Consultation
              records are retained for a period of 5 years.
            </p>

            <h2>9. Children&apos;s Privacy</h2>
            <p>
              Our services are not directed to individuals under the age of 18.
              We do not knowingly collect personal information from children.
            </p>

            <h2>10. Changes to This Policy</h2>
            <p>
              We may update this Privacy Policy from time to time. We will notify
              you of any changes by posting the new policy on this page with an
              updated revision date.
            </p>

            <h2>11. Contact Us</h2>
            <p>
              If you have any questions about this Privacy Policy, please contact
              us at:
            </p>
            <ul>
              <li>Email: contact@vedicjivan.com</li>
              <li>Phone: +91 98765 43210</li>
            </ul>
          </div>
        </Container>
      </section>
    </>
  );
}
