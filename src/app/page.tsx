import Link from "next/link";
import {
  SITE,
  SERVICES,
  TESTIMONIALS,
  STATS,
  HOME_FAQS,
} from "@/lib/constants";
import TestimonialCard from "@/components/TestimonialCard";
import FAQAccordion from "@/components/FAQAccordion";
import CTABanner from "@/components/CTABanner";

export default function HomePage() {
  return (
    <>
      {/* ── Hero ── */}
      <section className="relative overflow-hidden bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 py-24 sm:py-32 lg:py-40">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-brand-500/10 via-transparent to-transparent" />
        <div className="relative mx-auto max-w-7xl px-4 text-center sm:px-6 lg:px-8">
          <span className="inline-block rounded-full border border-brand-500/30 bg-brand-500/10 px-4 py-1.5 text-sm font-semibold text-brand-400">
            AI-Powered Growth for Roofers
          </span>
          <h1 className="mx-auto mt-6 max-w-4xl font-heading text-4xl font-extrabold leading-tight sm:text-5xl lg:text-6xl">
            Your Roofing Company Deserves a Website That Works{" "}
            <span className="text-gradient">as Hard as You Do</span>
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg text-slate-400 sm:text-xl">
            AI-powered websites, chatbots, and lead generation built
            exclusively for roofing companies. More leads, more reviews, less
            busywork.
          </p>
          <div className="mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row">
            <Link
              href="/contact"
              className="rounded-lg bg-brand-500 px-8 py-4 text-lg font-semibold text-slate-900 transition-colors hover:bg-brand-400"
            >
              Get Your Free AI Audit
            </Link>
            <Link
              href="/services"
              className="rounded-lg border border-slate-700 px-8 py-4 text-lg font-semibold text-white transition-colors hover:border-slate-500 hover:bg-slate-800"
            >
              See How It Works
            </Link>
          </div>
        </div>
      </section>

      {/* ── Trust Bar ── */}
      <section className="border-y border-slate-800 bg-slate-900/50 py-8">
        <div className="mx-auto flex max-w-5xl flex-wrap items-center justify-center gap-8 px-4 text-center sm:gap-12">
          {[
            { icon: "🏗️", text: "50+ Roofing Companies Served" },
            { icon: "⭐", text: "5-Star Rated" },
            { icon: "📍", text: "Utah Based, Nationwide Service" },
            { icon: "🤖", text: "AI-Powered Technology" },
          ].map((badge) => (
            <div key={badge.text} className="flex items-center gap-2 text-sm text-slate-400">
              <span className="text-lg">{badge.icon}</span>
              <span className="font-medium">{badge.text}</span>
            </div>
          ))}
        </div>
      </section>

      {/* ── Services Overview ── */}
      <section className="py-20 sm:py-28">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <span className="text-sm font-semibold uppercase tracking-widest text-brand-500">
              What We Do
            </span>
            <h2 className="mt-3 font-heading text-3xl font-bold sm:text-4xl">
              Everything Your Roofing Company Needs to Grow
            </h2>
            <p className="mx-auto mt-4 max-w-2xl text-slate-400">
              From your first click to your next closed deal — our AI suite
              handles the entire customer journey.
            </p>
          </div>

          <div className="mt-16 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {SERVICES.map((svc) => (
              <div
                key={svc.slug}
                className="rounded-xl border border-slate-800 bg-slate-900/50 p-6 transition-colors hover:border-slate-700"
              >
                <div className="mb-4 text-3xl">{svc.icon}</div>
                <h3 className="font-heading text-xl font-bold">{svc.title}</h3>
                <p className="mt-2 text-sm leading-relaxed text-slate-400">
                  {svc.description}
                </p>
              </div>
            ))}
          </div>

          <div className="mt-12 text-center">
            <Link
              href="/services"
              className="inline-block rounded-lg border border-brand-500 px-6 py-3 font-semibold text-brand-400 transition-colors hover:bg-brand-500/10"
            >
              View All Services
            </Link>
          </div>
        </div>
      </section>

      {/* ── Stats ── */}
      <section className="border-y border-slate-800 bg-slate-900/30 py-20">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
            {STATS.map((stat) => (
              <div key={stat.label} className="text-center">
                <div className="font-heading text-4xl font-extrabold text-brand-500 sm:text-5xl">
                  {stat.value}
                </div>
                <div className="mt-2 font-semibold text-white">{stat.label}</div>
                <p className="mt-1 text-sm text-slate-500">{stat.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Testimonials ── */}
      <section className="py-20 sm:py-28">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <span className="text-sm font-semibold uppercase tracking-widest text-brand-500">
              Social Proof
            </span>
            <h2 className="mt-3 font-heading text-3xl font-bold sm:text-4xl">
              Roofers Love What We Build
            </h2>
            <p className="mx-auto mt-4 max-w-2xl text-slate-400">
              Don&apos;t take our word for it — hear from roofing companies who
              transformed their business with AI.
            </p>
          </div>

          <div className="mt-16 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {TESTIMONIALS.map((t) => (
              <TestimonialCard key={t.name} t={t} />
            ))}
          </div>
        </div>
      </section>

      {/* ── How It Works ── */}
      <section className="border-y border-slate-800 bg-slate-900/30 py-20 sm:py-28">
        <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <span className="text-sm font-semibold uppercase tracking-widest text-brand-500">
              Simple Process
            </span>
            <h2 className="mt-3 font-heading text-3xl font-bold sm:text-4xl">
              How It Works
            </h2>
          </div>

          <div className="mt-16 grid gap-8 sm:grid-cols-3">
            {[
              {
                step: "1",
                title: "Book a Free Call",
                desc: "We\u2019ll audit your current online presence and identify the biggest growth opportunities for your roofing business.",
              },
              {
                step: "2",
                title: "We Build Your AI Suite",
                desc: "Our team builds your custom AI-powered website, chatbot, and marketing automation system \u2014 tailored to your market.",
              },
              {
                step: "3",
                title: "Watch Leads Roll In",
                desc: "Your AI tools work 24/7 to generate leads, follow up automatically, and help you close more roofing jobs.",
              },
            ].map((s) => (
              <div key={s.step} className="text-center">
                <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-brand-500 text-2xl font-bold text-slate-900">
                  {s.step}
                </div>
                <h3 className="mt-4 font-heading text-xl font-bold">{s.title}</h3>
                <p className="mt-2 text-sm leading-relaxed text-slate-400">
                  {s.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── FAQ ── */}
      <FAQAccordion faqs={HOME_FAQS} />

      {/* ── CTA ── */}
      <CTABanner />
    </>
  );
}
