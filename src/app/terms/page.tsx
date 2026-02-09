import type { Metadata } from "next";
import { Container } from "@/components/ui/Container";

export const metadata: Metadata = {
  title: "Terms of Service",
  description: "VedicJivan's terms of service — the rules and guidelines governing your use of our website and services.",
};

export default function TermsPage() {
  return (
    <>
      <section className="bg-dark-gradient py-16 sm:py-20">
        <Container>
          <div className="mx-auto max-w-3xl text-center">
            <h1 className="font-heading text-3xl font-bold text-white sm:text-4xl lg:text-5xl">
              Terms of Service
            </h1>
            <p className="mt-4 text-gray-400">Last updated: January 1, 2025</p>
          </div>
        </Container>
      </section>

      <section className="vedic-section">
        <Container size="narrow">
          <div className="prose prose-lg max-w-none prose-headings:font-heading prose-headings:text-vedic-dark prose-p:text-gray-600 prose-li:text-gray-600 prose-strong:text-vedic-dark">
            <h2>1. Acceptance of Terms</h2>
            <p>
              By accessing or using the VedicJivan website and services, you agree
              to be bound by these Terms of Service. If you do not agree to these
              terms, please do not use our services.
            </p>

            <h2>2. Description of Services</h2>
            <p>VedicJivan provides the following services:</p>
            <ul>
              <li>Vedic astrology consultations (phone and video)</li>
              <li>Personalized Kundli and numerology reports</li>
              <li>Vastu Shastra consultation</li>
              <li>Kundli matching services</li>
              <li>Online courses in Vedic astrology, numerology, and Vastu</li>
              <li>Educational blog content</li>
            </ul>

            <h2>3. User Accounts</h2>
            <p>
              To book consultations, purchase reports, or enroll in courses, you
              may need to create an account. You are responsible for:
            </p>
            <ul>
              <li>Maintaining the confidentiality of your account credentials</li>
              <li>All activities that occur under your account</li>
              <li>Providing accurate and up-to-date information</li>
              <li>Notifying us immediately of any unauthorized access</li>
            </ul>

            <h2>4. Booking and Appointments</h2>
            <ul>
              <li>All appointments must be booked through our official website</li>
              <li>Accurate birth details (date, time, and place) must be provided for consultations</li>
              <li>Appointments are subject to availability</li>
              <li>You will receive confirmation via email upon successful booking</li>
            </ul>

            <h2>5. Payments</h2>
            <ul>
              <li>All prices are displayed in INR and EUR</li>
              <li>Payments are processed securely through Razorpay (for INR) and Stripe (for EUR)</li>
              <li>Full payment is required at the time of booking</li>
              <li>We do not store your payment card details</li>
              <li>Prices may be updated from time to time without prior notice</li>
            </ul>

            <h2>6. Cancellation and Rescheduling</h2>
            <ul>
              <li><strong>Rescheduling:</strong> Free rescheduling is available up to 24 hours before the appointment</li>
              <li><strong>Cancellation:</strong> Cancellations made 48+ hours before the appointment are eligible for a full refund</li>
              <li><strong>Late cancellation:</strong> Cancellations within 24 hours may be subject to a 50% fee</li>
              <li><strong>No-shows:</strong> No refund will be provided for missed appointments</li>
            </ul>

            <h2>7. Nature of Services</h2>
            <p>
              <strong>Important Disclaimer:</strong> Vedic astrology is an ancient
              predictive science. Our services are provided for guidance and
              informational purposes. We do not guarantee the accuracy of
              predictions, and our advice should not replace professional medical,
              legal, or financial consultation. Users should exercise their own
              judgment when making life decisions.
            </p>

            <h2>8. Intellectual Property</h2>
            <p>
              All content on the VedicJivan website — including text, graphics,
              logos, images, course materials, reports, and software — is the
              property of VedicJivan and is protected by intellectual property laws.
              You may not:
            </p>
            <ul>
              <li>Reproduce, distribute, or create derivative works from our content</li>
              <li>Share course materials or reports with third parties</li>
              <li>Use our branding without written permission</li>
            </ul>

            <h2>9. Course Enrollment</h2>
            <ul>
              <li>Course access is granted upon successful payment</li>
              <li>Access is for the enrolled individual only and is non-transferable</li>
              <li>Course materials may not be recorded, downloaded, or redistributed</li>
              <li>Certificates are issued upon course completion</li>
            </ul>

            <h2>10. Limitation of Liability</h2>
            <p>
              To the maximum extent permitted by law, VedicJivan shall not be
              liable for any indirect, incidental, special, or consequential
              damages arising from the use of our services, including but not
              limited to decisions made based on astrological advice.
            </p>

            <h2>11. Governing Law</h2>
            <p>
              These Terms of Service are governed by and construed in accordance
              with the laws of India. Any disputes arising from these terms shall
              be subject to the exclusive jurisdiction of the courts in New Delhi,
              India.
            </p>

            <h2>12. Changes to Terms</h2>
            <p>
              We reserve the right to modify these terms at any time. Changes
              will be effective immediately upon posting on the website. Continued
              use of our services after changes constitutes acceptance of the
              updated terms.
            </p>

            <h2>13. Contact</h2>
            <p>
              For questions about these Terms of Service, contact us at:
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
