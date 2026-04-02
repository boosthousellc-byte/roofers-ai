import Link from "next/link";
import { SITE, SERVICES, NAV_LINKS } from "@/lib/constants";

export default function Footer() {
  return (
    <footer className="border-t border-slate-800 bg-slate-950">
      <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="grid gap-12 sm:grid-cols-2 lg:grid-cols-4">
          {/* Company */}
          <div>
            <Link href="/" className="flex items-center gap-2 text-xl font-bold">
              <span className="text-2xl">🏠</span>
              <span className="font-heading">
                Roofers&nbsp;<span className="text-brand-500">AI</span>
              </span>
            </Link>
            <p className="mt-4 text-sm leading-relaxed text-slate-400">
              AI-powered growth tools built exclusively for roofing companies.
              More leads, more reviews, less busywork.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-heading text-sm font-semibold uppercase tracking-wider text-slate-300">
              Quick Links
            </h3>
            <ul className="mt-4 space-y-3">
              {NAV_LINKS.map((link) => (
                <li key={link.href}>
                  <Link
                    href={link.href}
                    className="text-sm text-slate-400 transition-colors hover:text-brand-400"
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Services */}
          <div>
            <h3 className="font-heading text-sm font-semibold uppercase tracking-wider text-slate-300">
              Services
            </h3>
            <ul className="mt-4 space-y-3">
              {SERVICES.map((svc) => (
                <li key={svc.slug}>
                  <Link
                    href="/services"
                    className="text-sm text-slate-400 transition-colors hover:text-brand-400"
                  >
                    {svc.title}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h3 className="font-heading text-sm font-semibold uppercase tracking-wider text-slate-300">
              Contact
            </h3>
            <ul className="mt-4 space-y-3 text-sm text-slate-400">
              <li>
                <a
                  href={SITE.phoneHref}
                  className="transition-colors hover:text-brand-400"
                >
                  {SITE.phone}
                </a>
              </li>
              <li>
                <a
                  href={`mailto:${SITE.email}`}
                  className="transition-colors hover:text-brand-400"
                >
                  {SITE.email}
                </a>
              </li>
              <li>{SITE.location}</li>
            </ul>
          </div>
        </div>

        {/* Bottom */}
        <div className="mt-12 border-t border-slate-800 pt-8 text-center text-sm text-slate-500">
          &copy; {new Date().getFullYear()} {SITE.name}. All rights reserved.
        </div>
      </div>
    </footer>
  );
}
