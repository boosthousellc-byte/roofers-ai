import Link from "next/link";
import type { BlogPost } from "@/types";

export default function BlogCard({ post }: { post: BlogPost }) {
  return (
    <article className="group flex flex-col rounded-xl border border-slate-800 bg-slate-900/50 transition-colors hover:border-slate-700">
      <div className="flex flex-1 flex-col p-6">
        <div className="mb-3 flex items-center gap-3">
          <span className="rounded-full bg-brand-500/10 px-3 py-1 text-xs font-semibold text-brand-400">
            {post.category}
          </span>
          <span className="text-xs text-slate-500">{post.readingTime}</span>
        </div>
        <h3 className="font-heading text-xl font-bold text-white group-hover:text-brand-400 transition-colors">
          <Link href={`/blog/${post.slug}`}>{post.title}</Link>
        </h3>
        <p className="mt-2 flex-1 text-sm leading-relaxed text-slate-400">
          {post.description}
        </p>
        <div className="mt-4 flex items-center justify-between text-xs text-slate-500">
          <span>{post.author}</span>
          <time dateTime={post.date}>
            {new Date(post.date).toLocaleDateString("en-US", {
              month: "short",
              day: "numeric",
              year: "numeric",
            })}
          </time>
        </div>
      </div>
    </article>
  );
}
