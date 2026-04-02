"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { NAV_LINKS, SITE } from "@/lib/constants";

export default function Header() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-50 border-b border-slate-800 bg-slate-950/90 backdrop-blur-md">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2 text-xl font-bold">
          <span className="text-2xl">🏠</span>
          <span className="font-heading">
            Roofers&nbsp;<span className="text-brand-500">AI</span>
          </span>
        </Link>

        {/* Desktop Nav */}
        <nav className="hidden items-center gap-8 md:flex">
          {NAV_LINKS.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className={`text-sm font-medium transition-colors hover:text-brand-400 ${
                pathname === link.href ? "text-brand-500" : "text-slate-300"
              }`}
            >
              {link.label}
            </Link>
          ))}
        </nav>

        {/* CTA + Mobile Toggle */}
        <div className="flex items-center gap-4">
          <a
            href={SITE.phoneHref}
            className="hidden rounded-lg bg-brand-500 px-5 py-2.5 text-sm font-semibold text-slate-900 transition-colors hover:bg-brand-400 sm:inline-block"
          >
            {SITE.phone}
          </a>

          {/* Hamburger */}
          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="flex flex-col gap-1.5 md:hidden"
            aria-label="Toggle menu"
          >
            <span
              className={`h-0.5 w-6 bg-slate-300 transition-transform ${
                mobileOpen ? "translate-y-2 rotate-45" : ""
              }`}
            />
            <span
              className={`h-0.5 w-6 bg-slate-300 transition-opacity ${
                mobileOpen ? "opacity-0" : ""
              }`}
            />
            <span
              className={`h-0.5 w-6 bg-slate-300 transition-transform ${
                mobileOpen ? "-translate-y-2 -rotate-45" : ""
              }`}
            />
          </button>
        </div>
      </div>

      {/* Mobile Nav */}
      {mobileOpen && (
        <nav className="border-t border-slate-800 bg-slate-950 px-4 pb-6 pt-4 md:hidden">
          {NAV_LINKS.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              onClick={() => setMobileOpen(false)}
              className={`block py-3 text-base font-medium ${
                pathname === link.href ? "text-brand-500" : "text-slate-300"
              }`}
            >
              {link.label}
            </Link>
          ))}
          <a
            href={SITE.phoneHref}
            className="mt-4 block rounded-lg bg-brand-500 px-5 py-3 text-center text-sm font-semibold text-slate-900"
          >
            Call {SITE.phone}
          </a>
        </nav>
      )}
    </header>
  );
}
