import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { MDXRemote } from "next-mdx-remote/rsc";
import remarkGfm from "remark-gfm";
import rehypeSlug from "rehype-slug";
import rehypeAutolinkHeadings from "rehype-autolink-headings";
import { getAllPosts, getPostBySlug, getRelatedPosts } from "@/lib/blog";
import { articleSchema, breadcrumbSchema } from "@/lib/schemas";
import SchemaMarkup from "@/components/SchemaMarkup";
import BlogCard from "@/components/BlogCard";
import CTABanner from "@/components/CTABanner";

const mdxComponents = {
  h2: (props: React.ComponentProps<"h2">) => (
    <h2
      className="mb-4 mt-12 scroll-mt-24 font-heading text-2xl font-bold text-white sm:text-3xl"
      {...props}
    />
  ),
  h3: (props: React.ComponentProps<"h3">) => (
    <h3
      className="mb-3 mt-8 scroll-mt-24 font-heading text-xl font-bold text-white"
      {...props}
    />
  ),
  p: (props: React.ComponentProps<"p">) => (
    <p className="mb-4 leading-relaxed text-slate-300" {...props} />
  ),
  ul: (props: React.ComponentProps<"ul">) => (
    <ul className="mb-4 list-disc space-y-2 pl-6 text-slate-300" {...props} />
  ),
  ol: (props: React.ComponentProps<"ol">) => (
    <ol className="mb-4 list-decimal space-y-2 pl-6 text-slate-300" {...props} />
  ),
  li: (props: React.ComponentProps<"li">) => (
    <li className="leading-relaxed" {...props} />
  ),
  a: (props: React.ComponentProps<"a">) => (
    <a className="text-brand-400 underline hover:text-brand-300" {...props} />
  ),
  blockquote: (props: React.ComponentProps<"blockquote">) => (
    <blockquote
      className="my-6 border-l-4 border-brand-500 bg-slate-900/50 py-4 pl-6 pr-4 italic text-slate-300"
      {...props}
    />
  ),
  strong: (props: React.ComponentProps<"strong">) => (
    <strong className="font-semibold text-white" {...props} />
  ),
};

export async function generateStaticParams() {
  return getAllPosts().map((post) => ({ slug: post.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const post = getPostBySlug(slug);
  if (!post) return {};

  return {
    title: post.title,
    description: post.description,
    alternates: { canonical: `/blog/${post.slug}` },
    openGraph: {
      type: "article",
      title: post.title,
      description: post.description,
      publishedTime: post.date,
      authors: [post.author],
    },
  };
}

export default async function BlogPostPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const post = getPostBySlug(slug);
  if (!post) notFound();

  const related = getRelatedPosts(slug, 3);

  return (
    <>
      <SchemaMarkup schema={articleSchema(post)} />
      <SchemaMarkup
        schema={breadcrumbSchema([
          { name: "Home", url: "https://roofers-ai.io" },
          { name: "Blog", url: "https://roofers-ai.io/blog" },
          { name: post.title, url: `https://roofers-ai.io/blog/${post.slug}` },
        ])}
      />

      <article className="py-20">
        <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="mb-12 text-center">
            <div className="mb-4 flex items-center justify-center gap-3">
              <span className="rounded-full bg-brand-500/10 px-3 py-1 text-sm font-semibold text-brand-400">
                {post.category}
              </span>
              <span className="text-sm text-slate-500">{post.readingTime}</span>
            </div>
            <h1 className="font-heading text-3xl font-extrabold leading-tight sm:text-4xl lg:text-5xl">
              {post.title}
            </h1>
            <p className="mt-4 text-lg text-slate-400">{post.description}</p>
            <div className="mt-6 flex items-center justify-center gap-4 text-sm text-slate-500">
              <span>By {post.author}</span>
              <span>&middot;</span>
              <time dateTime={post.date}>
                {new Date(post.date).toLocaleDateString("en-US", {
                  month: "long",
                  day: "numeric",
                  year: "numeric",
                })}
              </time>
            </div>
          </div>

          {/* Content */}
          <div className="prose-custom">
            <MDXRemote
              source={post.content}
              components={mdxComponents}
              options={{
                mdxOptions: {
                  remarkPlugins: [remarkGfm],
                  rehypePlugins: [rehypeSlug, rehypeAutolinkHeadings],
                },
              }}
            />
          </div>

          {/* Author */}
          <div className="mt-16 rounded-xl border border-slate-800 bg-slate-900/50 p-6">
            <div className="flex items-center gap-4">
              <div className="flex h-14 w-14 items-center justify-center rounded-full bg-brand-500/20 text-2xl">
                👤
              </div>
              <div>
                <p className="font-heading font-bold">{post.author}</p>
                <p className="text-sm text-slate-400">
                  Founder &amp; CEO at Roofers AI
                </p>
              </div>
            </div>
            <p className="mt-4 text-sm leading-relaxed text-slate-400">
              Derek Lee is the founder of Roofers AI, helping roofing companies
              across the country grow with artificial intelligence. Have a
              question?{" "}
              <Link href="/contact" className="text-brand-400 underline">
                Get in touch
              </Link>
              .
            </p>
          </div>
        </div>
      </article>

      {/* Related Posts */}
      {related.length > 0 && (
        <section className="border-t border-slate-800 bg-slate-900/30 py-20">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <h2 className="mb-12 text-center font-heading text-3xl font-bold">
              Related Articles
            </h2>
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {related.map((p) => (
                <BlogCard key={p.slug} post={p} />
              ))}
            </div>
          </div>
        </section>
      )}

      <CTABanner title="Want Results Like These for Your Roofing Company?" />
    </>
  );
}
