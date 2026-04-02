import type { Metadata } from "next";
import Link from "next/link";
import { SERVICES, SERVICES_FAQS } from "@/lib/constants";
import { serviceSchema } from "@/lib/schemas";
import SchemaMarkup from "@/components/SchemaMarkup";
import FAQAccordion from "@/components/FAQAccordion";
import CTABanner from "@/components/CTABanner";

export const metadata: Metadata = {
  title: "AI Services for Roofing Companies",
  description:
    "Explore our full AI suite: websites, chatbots, lead generation, CRM, automated follow-ups, and reputation management for roofing contractors.",
  alternates: { canonical: "/services" },
};

export default function ServicesPage() {
  return (
    <>
      {/* Hero */}
      <section className="bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 py-20 sm:py-28">
        <div className="mx-auto max-w-4xl px-4 text-center sm:px-6 lg:px-8">
          <span className="text-sm font-semibold uppercase tracking-widest text-brand-500">
            Our Services
          </span>
          <h1 className="mt-3 font-heading text-4xl font-extrabold sm:text-5xl">
            The Complete AI Toolkit for{" "}
            <span className="text-gradient">Modern Roofing Companies</span>
          </h1>
          <p className="mt-6 text-lg text-slate-400">
            Stop losing leads to slow responses and outdated websites. Our AI
            suite handles everything from first impression to five-star review.
          </p>
        </div>
      </section>

      {/* Services Detail */}
      <section className="py-20">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="space-y-24">
            {SERVICES.map((svc, i) => (
              <div
                key={svc.slug}
                id={svc.slug}
                className={`flex flex-col gap-12 lg:flex-row lg:items-center ${
                  i % 2 === 1 ? "lg:flex-row-reverse" : ""
                }`}
              >
                <SchemaMarkup
                  schema={serviceSchema(svc.title, svc.description)}
                />

                {/* Text */}
                <div className="flex-1">
                  <div className="text-4xl">{svc.icon}</div>
                  <h2 className="mt-4 font-heading text-3xl font-bold">
                    {svc.title}
                  </h2>
                  <p className="mt-4 leading-relaxed text-slate-400">
                    {svc.description}
                  </p>
                  <ul className="mt-6 space-y-3">
                    {svc.features.map((f) => (
                      <li key={f} className="flex items-start gap-3 text-slate-300">
                        <span className="mt-0.5 text-brand-500">&#10003;</span>
                        {f}
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Visual placeholder */}
                <div className="flex flex-1 items-center justify-center rounded-2xl border border-slate-800 bg-slate-900/50 p-12">
                  <div className="text-center">
                    <div className="text-6xl">{svc.icon}</div>
                    <p className="mt-4 font-heading text-lg font-semibold text-slate-500">
                      {svc.title}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Before / After */}
      <section className="border-y border-slate-800 bg-slate-900/30 py-20">
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <h2 className="text-center font-heading text-3xl font-bold sm:text-4xl">
            Before vs. After Roofers AI
          </h2>
          <div className="mt-12 grid gap-6 sm:grid-cols-2">
            <div className="rounded-xl border border-red-900/50 bg-red-950/20 p-6">
              <h3 className="font-heading text-xl font-bold text-red-400">
                Before
              </h3>
              <ul className="mt-4 space-y-3 text-sm text-slate-400">
                <li>&#10005; Template website that doesn&apos;t convert</li>
                <li>&#10005; Missed calls and lost leads</li>
                <li>&#10005; 47-hour average response time</li>
                <li>&#10005; Handful of Google reviews</li>
                <li>&#10005; Guessing which ads work</li>
                <li>&#10005; Leads tracked on sticky notes</li>
              </ul>
            </div>
            <div className="rounded-xl border border-green-900/50 bg-green-950/20 p-6">
              <h3 className="font-heading text-xl font-bold text-green-400">
                After
              </h3>
              <ul className="mt-4 space-y-3 text-sm text-slate-400">
                <li>&#10003; AI-optimized site generating leads 24/7</li>
                <li>&#10003; Chatbot books estimates while you work</li>
                <li>&#10003; Under 1-minute automated response</li>
                <li>&#10003; 4.8+ star rating on Google</li>
                <li>&#10003; AI-optimized campaigns with clear ROI</li>
                <li>&#10003; Full CRM with pipeline tracking</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ */}
      <FAQAccordion
        faqs={SERVICES_FAQS}
        title="Service Questions"
      />

      {/* CTA */}
      <CTABanner title="Let&apos;s Build Your AI Suite" />
    </>
  );
}
