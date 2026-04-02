"use client";

import { useState } from "react";

export default function ContactForm() {
  const [submitted, setSubmitted] = useState(false);

  if (submitted) {
    return (
      <div className="rounded-xl border border-green-800 bg-green-900/20 p-8 text-center">
        <div className="text-4xl">✅</div>
        <h3 className="mt-4 font-heading text-2xl font-bold">
          Message Sent!
        </h3>
        <p className="mt-2 text-slate-400">
          We&apos;ll get back to you within 24 hours.
        </p>
      </div>
    );
  }

  return (
    <form
      name="contact"
      data-netlify="true"
      onSubmit={(e) => {
        e.preventDefault();
        const form = e.currentTarget;
        const formData = new FormData(form);
        fetch("/", {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: new URLSearchParams(formData as unknown as Record<string, string>).toString(),
        })
          .then(() => setSubmitted(true))
          .catch(() => setSubmitted(true));
      }}
      className="space-y-5"
    >
      <input type="hidden" name="form-name" value="contact" />

      <div className="grid gap-5 sm:grid-cols-2">
        <div>
          <label htmlFor="name" className="mb-1.5 block text-sm font-medium text-slate-300">
            Full Name *
          </label>
          <input
            type="text"
            id="name"
            name="name"
            required
            className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-3 text-white placeholder-slate-500 focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
            placeholder="John Smith"
          />
        </div>
        <div>
          <label htmlFor="email" className="mb-1.5 block text-sm font-medium text-slate-300">
            Email *
          </label>
          <input
            type="email"
            id="email"
            name="email"
            required
            className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-3 text-white placeholder-slate-500 focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
            placeholder="john@roofingco.com"
          />
        </div>
      </div>

      <div className="grid gap-5 sm:grid-cols-2">
        <div>
          <label htmlFor="phone" className="mb-1.5 block text-sm font-medium text-slate-300">
            Phone
          </label>
          <input
            type="tel"
            id="phone"
            name="phone"
            className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-3 text-white placeholder-slate-500 focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
            placeholder="(555) 123-4567"
          />
        </div>
        <div>
          <label htmlFor="company" className="mb-1.5 block text-sm font-medium text-slate-300">
            Company Name
          </label>
          <input
            type="text"
            id="company"
            name="company"
            className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-3 text-white placeholder-slate-500 focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
            placeholder="ABC Roofing"
          />
        </div>
      </div>

      <div>
        <label htmlFor="message" className="mb-1.5 block text-sm font-medium text-slate-300">
          How can we help? *
        </label>
        <textarea
          id="message"
          name="message"
          required
          rows={4}
          className="w-full rounded-lg border border-slate-700 bg-slate-800 px-4 py-3 text-white placeholder-slate-500 focus:border-brand-500 focus:outline-none focus:ring-1 focus:ring-brand-500"
          placeholder="Tell us about your roofing business and what you're looking for..."
        />
      </div>

      <button
        type="submit"
        className="w-full rounded-lg bg-brand-500 px-8 py-4 text-lg font-semibold text-slate-900 transition-colors hover:bg-brand-400"
      >
        Send Message
      </button>
    </form>
  );
}
