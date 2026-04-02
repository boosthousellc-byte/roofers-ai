import Link from "next/link";

export default function NotFound() {
  return (
    <section className="flex min-h-[60vh] items-center justify-center py-20">
      <div className="text-center">
        <h1 className="font-heading text-6xl font-extrabold text-brand-500">
          404
        </h1>
        <p className="mt-4 text-xl text-slate-400">Page not found</p>
        <Link
          href="/"
          className="mt-8 inline-block rounded-lg bg-brand-500 px-6 py-3 font-semibold text-slate-900 transition-colors hover:bg-brand-400"
        >
          Back to Home
        </Link>
      </div>
    </section>
  );
}
