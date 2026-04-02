import Link from "next/link";
import { SITE } from "@/lib/constants";

export default function CTABanner({
  title = "Ready to 3x Your Roofing Leads?",
  subtitle = "Get your free AI audit and see exactly how we can grow your roofing business.",
}: {
  title?: string;
  subtitle?: string;
}) {
  return (
    <section className="bg-gradient-to-br from-brand-600 via-brand-500 to-brand-400 py-20">
      <div className="mx-auto max-w-4xl px-4 text-center sm:px-6 lg:px-8">
        <h2 className="font-heading text-3xl font-bold text-slate-900 sm:text-4xl lg:text-5xl">
          {title}
        </h2>
        <p className="mx-auto mt-4 max-w-2xl text-lg text-slate-800">
          {subtitle}
        </p>
        <div className="mt-8 flex flex-col items-center justify-center gap-4 sm:flex-row">
          <Link
            href="/contact"
            className="rounded-lg bg-slate-900 px-8 py-4 text-lg font-semibold text-white transition-colors hover:bg-slate-800"
          >
            Get Your Free AI Audit
          </Link>
          <a
            href={SITE.phoneHref}
            className="rounded-lg border-2 border-slate-900 px-8 py-4 text-lg font-semibold text-slate-900 transition-colors hover:bg-slate-900/10"
          >
            Call {SITE.phone}
          </a>
        </div>
      </div>
    </section>
  );
}
