import type { Metadata } from "next";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import SchemaMarkup from "@/components/SchemaMarkup";
import { localBusinessSchema, websiteSchema } from "@/lib/schemas";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    template: "%s | Roofers AI",
    default: "Roofers AI - AI-Powered Websites & Lead Generation for Roofing Companies",
  },
  description:
    "Get more roofing leads with AI-powered websites, 24/7 chatbots, automated follow-ups, and reputation management. Built exclusively for roofing companies.",
  metadataBase: new URL("https://roofers-ai.io"),
  alternates: { canonical: "/" },
  openGraph: {
    type: "website",
    siteName: "Roofers AI",
    title: "Roofers AI - AI-Powered Growth for Roofing Companies",
    description:
      "AI-powered websites, chatbots, and lead generation built exclusively for roofing companies.",
    url: "https://roofers-ai.io",
  },
  twitter: {
    card: "summary_large_image",
    title: "Roofers AI - AI-Powered Growth for Roofing Companies",
    description:
      "AI-powered websites, chatbots, and lead generation built exclusively for roofing companies.",
  },
  robots: { index: true, follow: true },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="font-sans">
        <SchemaMarkup schema={localBusinessSchema()} />
        <SchemaMarkup schema={websiteSchema()} />
        <Header />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}
