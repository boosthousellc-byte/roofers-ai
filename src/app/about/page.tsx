import type { Metadata } from "next";
import Link from "next/link";
import { SITE } from "@/lib/constants";
import CTABanner from "@/components/CTABanner";

export const metadata: Metadata = {
  title: "About Roofers AI - Derek Lee",
  description:
    "Meet Derek Lee, founder of Roofers AI. Learn how we help roofing companies grow with artificial intelligence.",
  alternates: { canonical: "/about" },
};

export default function AboutPage() {
  return (
    <>
      {/* Hero */}
      <section className="bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 py-20 sm:py-28">
        <div className="mx-auto max-w-4xl px-4 text-center sm:px-6 lg:px-8">
          <span className="text-sm font-semibold uppercase tracking-widest text-brand-500">
            About Us
          </span>
          <h1 className="mt-3 font-heading text-4xl font-extrabold sm:text-5xl">
            Built by Someone Who Gets{" "}
            <span className="text-gradient">the Roofing Business</span>
          </h1>
        </div>
      </section>

      {/* Founder */}
      <section className="py-20">
        <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col gap-12 lg:flex-row lg:items-center">
            {/* Photo placeholder */}
            <div className="flex shrink-0 items-center justify-center">
              <div className="flex h-64 w-64 items-center justify-center rounded-2xl border border-slate-800 bg-slate-900/50">
                <div className="text-center">
                  <div className="text-6xl">👤</div>
                  <p className="mt-2 font-heading font-semibold text-slate-400">
                    Derek Lee
                  </p>
                  <p className="text-sm text-slate-500">Founder &amp; CEO</p>
                </div>
              </div>
            </div>

            {/* Story */}
            <div>
              <h2 className="font-heading text-3xl font-bold">
                Meet Derek Lee
              </h2>
              <div className="mt-6 space-y-4 leading-relaxed text-slate-400">
                <p>
                  I started Roofers AI after seeing too many great roofing
                  companies struggle with the same problems: outdated websites
                  that didn&apos;t convert, missed calls that turned into lost
                  jobs, and marketing agencies that charged a fortune without
                  delivering real results.
                </p>
                <p>
                  The roofing industry is built on hard work and reputation.
                  But in today&apos;s digital world, the best roofers don&apos;t
                  always get the most business — the most visible ones do. I
                  built Roofers AI to close that gap.
                </p>
                <p>
                  We use artificial intelligence to give small and mid-size
                  roofing companies the same digital tools that billion-dollar
                  companies use — at a fraction of the cost. From AI chatbots
                  that book estimates while you&apos;re on the roof, to
                  automated follow-up systems that catch every lead, everything
                  we build is designed for one thing: helping roofers grow.
                </p>
                <p>
                  Based in Utah and serving roofing companies nationwide, we&apos;re
                  not a generic marketing agency. We&apos;re a team of AI
                  specialists who chose the roofing industry because we believe
                  in the people who keep roofs over everyone&apos;s heads.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Mission */}
      <section className="border-y border-slate-800 bg-slate-900/30 py-20">
        <div className="mx-auto max-w-3xl px-4 text-center sm:px-6 lg:px-8">
          <span className="text-sm font-semibold uppercase tracking-widest text-brand-500">
            Our Mission
          </span>
          <h2 className="mt-3 font-heading text-3xl font-bold sm:text-4xl">
            Make AI Accessible for Every Roofer
          </h2>
          <p className="mt-6 text-lg leading-relaxed text-slate-400">
            We believe every roofing company deserves technology that works. Our
            mission is to make AI accessible, affordable, and effective for the
            roofing industry — so that the best roofers get the business they
            deserve.
          </p>
        </div>
      </section>

      {/* Values */}
      <section className="py-20">
        <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
          <h2 className="text-center font-heading text-3xl font-bold sm:text-4xl">
            What We Stand For
          </h2>
          <div className="mt-12 grid gap-6 sm:grid-cols-2">
            {[
              {
                icon: "📊",
                title: "Results-Driven",
                desc: "We measure everything. If it doesn't generate leads or save you time, we don't do it.",
              },
              {
                icon: "🏠",
                title: "Roofer-First",
                desc: "Every tool, every feature, every decision is made with roofers in mind. We don't do generic.",
              },
              {
                icon: "💡",
                title: "Transparent",
                desc: "No hidden fees, no confusing contracts, no vanity metrics. You'll always know exactly what you're paying for and what you're getting.",
              },
              {
                icon: "🚀",
                title: "Always Innovating",
                desc: "AI moves fast. We stay on the cutting edge so your roofing company always has the best tools available.",
              },
            ].map((v) => (
              <div
                key={v.title}
                className="rounded-xl border border-slate-800 bg-slate-900/50 p-6"
              >
                <div className="text-3xl">{v.icon}</div>
                <h3 className="mt-3 font-heading text-xl font-bold">{v.title}</h3>
                <p className="mt-2 text-sm leading-relaxed text-slate-400">
                  {v.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Contact CTA */}
      <section className="border-t border-slate-800 bg-slate-900/30 py-20">
        <div className="mx-auto max-w-3xl px-4 text-center sm:px-6 lg:px-8">
          <h2 className="font-heading text-3xl font-bold">
            Let&apos;s Talk
          </h2>
          <p className="mt-4 text-slate-400">
            Have questions? Want to learn more about how AI can grow your
            roofing business? Reach out directly.
          </p>
          <div className="mt-8 flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
            <a
              href={SITE.phoneHref}
              className="rounded-lg bg-brand-500 px-8 py-4 font-semibold text-slate-900 transition-colors hover:bg-brand-400"
            >
              Call {SITE.phone}
            </a>
            <Link
              href="/contact"
              className="rounded-lg border border-slate-700 px-8 py-4 font-semibold text-white transition-colors hover:bg-slate-800"
            >
              Send a Message
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}
