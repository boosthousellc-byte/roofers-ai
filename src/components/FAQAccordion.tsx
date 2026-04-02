"use client";

import { useState } from "react";
import type { FAQ } from "@/types";
import SchemaMarkup from "./SchemaMarkup";
import { faqSchema } from "@/lib/schemas";

export default function FAQAccordion({
  faqs,
  title = "Frequently Asked Questions",
}: {
  faqs: FAQ[];
  title?: string;
}) {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  return (
    <section className="py-20">
      <SchemaMarkup schema={faqSchema(faqs)} />
      <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8">
        <h2 className="mb-12 text-center font-heading text-3xl font-bold sm:text-4xl">
          {title}
        </h2>
        <div className="space-y-4">
          {faqs.map((faq, i) => (
            <div
              key={i}
              className="rounded-xl border border-slate-800 bg-slate-900/50"
            >
              <button
                onClick={() => setOpenIndex(openIndex === i ? null : i)}
                className="flex w-full items-center justify-between px-6 py-5 text-left"
              >
                <span className="pr-4 font-heading text-lg font-semibold text-slate-100">
                  {faq.question}
                </span>
                <span
                  className={`shrink-0 text-2xl text-brand-500 transition-transform ${
                    openIndex === i ? "rotate-45" : ""
                  }`}
                >
                  +
                </span>
              </button>
              {openIndex === i && (
                <div className="px-6 pb-5">
                  <p className="leading-relaxed text-slate-400">{faq.answer}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
