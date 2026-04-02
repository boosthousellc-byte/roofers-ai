import type { Metadata } from "next";
import { getAllPosts } from "@/lib/blog";
import BlogCard from "@/components/BlogCard";

export const metadata: Metadata = {
  title: "Roofing AI Blog - Tips, Guides & Industry Insights",
  description:
    "Learn how AI is transforming the roofing industry. Tips on lead generation, chatbots, reputation management, and more.",
  alternates: { canonical: "/blog" },
};

export default function BlogPage() {
  const posts = getAllPosts();

  return (
    <>
      {/* Hero */}
      <section className="bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 py-20 sm:py-28">
        <div className="mx-auto max-w-4xl px-4 text-center sm:px-6 lg:px-8">
          <span className="text-sm font-semibold uppercase tracking-widest text-brand-500">
            Blog
          </span>
          <h1 className="mt-3 font-heading text-4xl font-extrabold sm:text-5xl">
            AI Insights for{" "}
            <span className="text-gradient">Roofing Professionals</span>
          </h1>
          <p className="mt-6 text-lg text-slate-400">
            Tips, guides, and strategies to help your roofing company grow with
            artificial intelligence.
          </p>
        </div>
      </section>

      {/* Posts Grid */}
      <section className="py-20">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          {posts.length === 0 ? (
            <p className="text-center text-slate-500">
              Blog posts coming soon.
            </p>
          ) : (
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {posts.map((post) => (
                <BlogCard key={post.slug} post={post} />
              ))}
            </div>
          )}
        </div>
      </section>
    </>
  );
}
