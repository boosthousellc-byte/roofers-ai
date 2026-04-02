import type { Testimonial } from "@/types";

export default function TestimonialCard({ t }: { t: Testimonial }) {
  return (
    <div className="flex flex-col rounded-xl border border-slate-800 bg-slate-900/50 p-6">
      <div className="mb-3 text-brand-500">
        {"★".repeat(t.rating)}
      </div>
      <p className="flex-1 text-slate-300 leading-relaxed">
        &ldquo;{t.quote}&rdquo;
      </p>
      <div className="mt-4 border-t border-slate-800 pt-4">
        <p className="font-semibold text-white">{t.name}</p>
        <p className="text-sm text-slate-500">
          {t.title}, {t.company}
        </p>
      </div>
    </div>
  );
}
