import type { Metadata } from "next";
import { SITE, CONTACT_FAQS } from "@/lib/constants";
import ContactForm from "@/components/ContactForm";
import FAQAccordion from "@/components/FAQAccordion";

export const metadata: Metadata = {
  title: "Contact Roofers AI - Get Your Free AI Audit",
  description: `Ready to grow your roofing business with AI? Contact Derek Lee at ${SITE.phone} or ${SITE.email} for a free consultation.`,
  alternates: { canonical: "/contact" },
};

export default function ContactPage() {
  return (
    <>
      {/* Hero */}
      <section className="bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 py-20 sm:py-28">
        <div className="mx-auto max-w-4xl px-4 text-center sm:px-6 lg:px-8">
          <span className="text-sm font-semibold uppercase tracking-widest text-brand-500">
            Get In Touch
          </span>
          <h1 className="mt-3 font-heading text-4xl font-extrabold sm:text-5xl">
            Let&apos;s Grow Your{" "}
            <span className="text-gradient">Roofing Business</span>
          </h1>
          <p className="mt-6 text-lg text-slate-400">
            Book your free AI audit. We&apos;ll show you exactly how AI can
            generate more leads and save you hours every week.
          </p>
        </div>
      </section>

      {/* Contact Section */}
      <section className="py-20">
        <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
          <div className="grid gap-12 lg:grid-cols-5">
            {/* Form */}
            <div className="lg:col-span-3">
              <h2 className="font-heading text-2xl font-bold">
                Send Us a Message
              </h2>
              <p className="mt-2 text-slate-400">
                Fill out the form and we&apos;ll get back to you within 24 hours.
              </p>
              <div className="mt-8">
                <ContactForm />
              </div>
            </div>

            {/* Contact Info */}
            <div className="lg:col-span-2">
              <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-8">
                <h3 className="font-heading text-xl font-bold">
                  Contact Info
                </h3>
                <div className="mt-6 space-y-6">
                  <div>
                    <p className="text-sm font-medium text-slate-500">Phone</p>
                    <a
                      href={SITE.phoneHref}
                      className="mt-1 block text-lg font-semibold text-brand-400 hover:text-brand-300"
                    >
                      {SITE.phone}
                    </a>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-slate-500">Email</p>
                    <a
                      href={`mailto:${SITE.email}`}
                      className="mt-1 block text-lg font-semibold text-brand-400 hover:text-brand-300"
                    >
                      {SITE.email}
                    </a>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-slate-500">
                      Location
                    </p>
                    <p className="mt-1 text-lg text-slate-300">
                      {SITE.location} (Serving Nationwide)
                    </p>
                  </div>
                </div>

                <div className="mt-8 border-t border-slate-800 pt-8">
                  <h4 className="font-heading font-semibold">
                    What to Expect
                  </h4>
                  <ul className="mt-4 space-y-3 text-sm text-slate-400">
                    <li className="flex items-start gap-2">
                      <span className="mt-0.5 text-brand-500">1.</span>
                      We&apos;ll respond within 24 hours
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="mt-0.5 text-brand-500">2.</span>
                      Free audit of your current online presence
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="mt-0.5 text-brand-500">3.</span>
                      Custom growth plan tailored to your market
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="mt-0.5 text-brand-500">4.</span>
                      No pressure, no obligation
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ */}
      <FAQAccordion faqs={CONTACT_FAQS} />
    </>
  );
}
