import fs from "fs";
import path from "path";
import matter from "gray-matter";
import type { BlogPost } from "@/types";

const BLOG_DIR = path.join(process.cwd(), "src/content/blog");

export function getAllPosts(): BlogPost[] {
  if (!fs.existsSync(BLOG_DIR)) return [];

  const files = fs.readdirSync(BLOG_DIR).filter((f) => f.endsWith(".mdx"));

  const posts = files.map((filename) => {
    const slug = filename.replace(/\.mdx$/, "");
    const filePath = path.join(BLOG_DIR, filename);
    const fileContents = fs.readFileSync(filePath, "utf8");
    const { data, content } = matter(fileContents);

    return {
      slug,
      title: data.title || "",
      description: data.description || "",
      date: data.date || "",
      author: data.author || "Derek Lee",
      category: data.category || "",
      tags: data.tags || [],
      readingTime: data.readingTime || "5 min read",
      content,
    };
  });

  return posts.sort(
    (a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()
  );
}

export function getPostBySlug(slug: string): BlogPost | null {
  const filePath = path.join(BLOG_DIR, `${slug}.mdx`);
  if (!fs.existsSync(filePath)) return null;

  const fileContents = fs.readFileSync(filePath, "utf8");
  const { data, content } = matter(fileContents);

  return {
    slug,
    title: data.title || "",
    description: data.description || "",
    date: data.date || "",
    author: data.author || "Derek Lee",
    category: data.category || "",
    tags: data.tags || [],
    readingTime: data.readingTime || "5 min read",
    content,
  };
}

export function getRelatedPosts(slug: string, limit = 3): BlogPost[] {
  const allPosts = getAllPosts();
  const currentPost = allPosts.find((p) => p.slug === slug);
  if (!currentPost) return allPosts.filter((p) => p.slug !== slug).slice(0, limit);

  return allPosts
    .filter((p) => p.slug !== slug)
    .sort((a, b) => {
      const aShared = a.tags.filter((t) => currentPost.tags.includes(t)).length;
      const bShared = b.tags.filter((t) => currentPost.tags.includes(t)).length;
      return bShared - aShared;
    })
    .slice(0, limit);
}
