import { Service, Testimonial, Stat, FAQ, NavLink } from "@/types";

export const SITE = {
  name: "Roofers AI",
  url: "https://roofers-ai.io",
  description:
    "AI-powered websites, chatbots, and lead generation built exclusively for roofing companies.",
  phone: "(435) 500-5651",
  phoneHref: "tel:+14355005651",
  email: "hello@roofers-ai.io",
  owner: "Derek Lee",
  location: "Utah",
};

export const NAV_LINKS: NavLink[] = [
  { label: "Home", href: "/" },
  { label: "Services", href: "/services" },
  { label: "About", href: "/about" },
  { label: "Blog", href: "/blog" },
  { label: "Contact", href: "/contact" },
];

export const SERVICES: Service[] = [
  {
    icon: "🌐",
    title: "AI-Powered Websites",
    slug: "ai-websites",
    description:
      "Custom websites that convert visitors into booked jobs. Mobile-first, SEO-optimized, and built to generate leads around the clock.",
    features: [
      "Conversion-optimized design",
      "Mobile-first responsive layouts",
      "Built-in SEO for local search",
      "Instant quote calculators",
      "Before & after project galleries",
      "Trust signals & review integration",
    ],
  },
  {
    icon: "💬",
    title: "AI Chatbot & Live Chat",
    slug: "ai-chatbot",
    description:
      "A 24/7 virtual receptionist trained on roofing industry knowledge. Qualifies leads, answers homeowner questions, and books appointments automatically.",
    features: [
      "Responds in under 3 seconds",
      "Qualifies leads by roof type & damage",
      "Books estimates directly on your calendar",
      "Trained on roofing terminology",
      "Handles multiple conversations at once",
      "Seamless handoff to your team",
    ],
  },
  {
    icon: "📈",
    title: "Lead Generation Engine",
    slug: "lead-generation",
    description:
      "Targeted campaigns that fill your pipeline with homeowners who need roofing work right now. AI-optimized ads and local SEO.",
    features: [
      "Google Ads management",
      "Meta & social media campaigns",
      "Local SEO optimization",
      "AI-powered audience targeting",
      "Landing page optimization",
      "Cost-per-lead tracking & reporting",
    ],
  },
  {
    icon: "🔄",
    title: "Automated Follow-Up System",
    slug: "automated-followups",
    description:
      "Never lose a lead to slow response time. Automated SMS and email sequences triggered the moment a lead comes in.",
    features: [
      "Under 1-minute response time",
      "SMS & email drip sequences",
      "Estimate follow-up automation",
      "Re-engagement campaigns",
      "Appointment reminders",
      "Speed-to-lead optimization",
    ],
  },
  {
    icon: "📊",
    title: "Smart CRM Dashboard",
    slug: "crm-dashboard",
    description:
      "Track every lead from first click to closed deal. Pipeline management, job scheduling, and revenue forecasting in one place.",
    features: [
      "Visual pipeline management",
      "Lead source tracking",
      "Job scheduling & dispatch",
      "Revenue forecasting",
      "Team performance metrics",
      "Mobile app access",
    ],
  },
  {
    icon: "⭐",
    title: "Reputation Management",
    slug: "reputation-management",
    description:
      "Turn happy customers into 5-star reviews without lifting a finger. Automated review requests and Google Business Profile optimization.",
    features: [
      "Automated post-job review requests",
      "Google Business Profile optimization",
      "Review response drafting",
      "Review monitoring & alerts",
      "Social proof widgets for your site",
      "Competitor review tracking",
    ],
  },
];

export const TESTIMONIALS: Testimonial[] = [
  {
    name: "Mike R.",
    title: "Owner",
    company: "Summit Roofing Co.",
    quote:
      "We were missing calls left and right. Since adding the AI chatbot, we've booked 40% more jobs without hiring another person. The chatbot handles the initial conversation better than most salespeople.",
    rating: 5,
  },
  {
    name: "Jessica T.",
    title: "Operations Manager",
    company: "Peak Performance Roofing",
    quote:
      "The automated follow-ups alone paid for the entire service. We used to lose leads because we couldn't get back to people fast enough. Now every lead gets a response within a minute.",
    rating: 5,
  },
  {
    name: "Carlos M.",
    title: "Owner",
    company: "Ironclad Roofing Solutions",
    quote:
      "I was skeptical about AI for a roofing company. But the website they built us looks incredible and actually converts. We went from 5 leads a week to 15+ in the first month.",
    rating: 5,
  },
  {
    name: "Dave K.",
    title: "Founder",
    company: "Ridgeline Roofing",
    quote:
      "The reputation management system is a game-changer. We went from 12 Google reviews to over 80 in six months. Our phone rings more just from the reviews alone.",
    rating: 5,
  },
  {
    name: "Sarah L.",
    title: "Co-Owner",
    company: "Guardian Roof Systems",
    quote:
      "Derek and his team actually understand the roofing business. This isn't some generic tech company — they built tools specifically for how roofers work. The CRM alone saves us hours every week.",
    rating: 5,
  },
  {
    name: "Brian W.",
    title: "Owner",
    company: "Apex Roofing & Restoration",
    quote:
      "Best investment we've made in the business. The AI website with the chatbot generates leads while I'm on the roof. Last month it booked 11 estimates while we were on jobs.",
    rating: 5,
  },
];

export const STATS: Stat[] = [
  {
    value: "3x",
    label: "More Qualified Leads",
    description:
      "Our clients see an average 3x increase in qualified leads within the first 90 days.",
  },
  {
    value: "<1 min",
    label: "Response Time",
    description:
      "AI chatbots respond to every inquiry in under 60 seconds, day or night.",
  },
  {
    value: "50+",
    label: "Roofing Companies Served",
    description:
      "Trusted by roofing contractors across the country to grow their businesses.",
  },
  {
    value: "4.8★",
    label: "Average Google Rating",
    description:
      "Clients using our reputation management see their Google rating climb to 4.8+.",
  },
];

export const HOME_FAQS: FAQ[] = [
  {
    question: "What does Roofers AI actually do?",
    answer:
      "Roofers AI provides a complete AI-powered growth suite for roofing companies. We build high-converting websites, deploy AI chatbots that book estimates 24/7, run targeted lead generation campaigns, automate your follow-up process, manage your online reputation, and give you a CRM dashboard to track everything. Think of us as your entire digital marketing and sales team, powered by AI.",
  },
  {
    question: "How much does it cost to work with Roofers AI?",
    answer:
      "Our pricing is customized based on which services you need and the size of your market. We offer flexible packages starting with just a website and chatbot, all the way up to the full AI suite. Every engagement starts with a free consultation where we assess your current setup and recommend the best plan for your goals and budget.",
  },
  {
    question: "How quickly will I see results?",
    answer:
      "Most clients see a significant increase in leads within the first 30 days. Your AI-powered website and chatbot go live within 1-2 weeks of onboarding. Lead generation campaigns typically reach full optimization within 60-90 days, with results improving month over month as the AI learns your market.",
  },
  {
    question: "Do I need to be tech-savvy to use your tools?",
    answer:
      "Not at all. We handle all the technical setup, and our CRM dashboard is designed to be as simple as checking your email. Most of our clients are roofers who spend their days on roofs, not on computers. If you can use a smartphone, you can use our tools.",
  },
  {
    question: "What makes Roofers AI different from a regular marketing agency?",
    answer:
      "Unlike general marketing agencies, we focus exclusively on the roofing industry. Our AI tools are trained on roofing terminology, customer behavior, and industry-specific conversion patterns. We don't just run ads — we build an entire AI-powered system that generates, qualifies, follows up with, and helps you close leads automatically.",
  },
  {
    question: "Can I keep my existing website?",
    answer:
      "Yes. While we recommend our AI-optimized websites for the best results, we can integrate our chatbot, lead generation, follow-up automation, and reputation management tools with your existing website. We'll assess your current site during the free consultation and recommend the best approach.",
  },
];

export const SERVICES_FAQS: FAQ[] = [
  {
    question: "What is an AI-powered website for roofing companies?",
    answer:
      "An AI-powered website for roofing companies is a conversion-optimized site that uses artificial intelligence to engage visitors, qualify leads, and book appointments automatically. Unlike static template websites, AI-powered sites include intelligent chatbots, dynamic content personalization, smart contact forms, and integrated analytics that continuously improve conversion rates.",
  },
  {
    question: "How does the AI chatbot qualify roofing leads?",
    answer:
      "Our AI chatbot is trained on roofing industry knowledge and asks homeowners targeted questions about their roof type, the nature of the damage or project, their timeline, and their location. Based on these answers, it scores the lead quality and either books an estimate directly on your calendar or flags it for your team to follow up. It handles multiple conversations simultaneously, 24 hours a day.",
  },
  {
    question: "What kind of ROI can I expect from AI lead generation?",
    answer:
      "Roofing companies using our full AI suite typically see a 3x increase in qualified leads within 90 days. The combination of optimized ad campaigns, AI-powered targeting, and instant follow-up significantly reduces cost per lead while increasing conversion rates. We track every metric and provide transparent ROI reporting so you know exactly what you're getting.",
  },
  {
    question: "How does automated follow-up work for roofing estimates?",
    answer:
      "When a homeowner requests an estimate through your website, chatbot, or ad campaign, our system immediately sends a personalized SMS and email confirmation. If they don't respond, a series of timed follow-up messages are sent over the next several days. The average roofing company takes 47 hours to follow up on a lead — our system responds in under 1 minute.",
  },
];

export const CONTACT_FAQS: FAQ[] = [
  {
    question: "What happens after I fill out the contact form?",
    answer:
      "You'll receive a confirmation email immediately. Derek or a team member will personally reach out within 24 hours to schedule your free AI audit. During the audit, we'll review your current online presence, identify growth opportunities, and recommend a customized plan.",
  },
  {
    question: "Is the consultation really free?",
    answer:
      "Yes, 100% free with no obligation. We believe in demonstrating value before asking for commitment. During the consultation, you'll get actionable insights about your roofing company's online presence that you can use whether or not you choose to work with us.",
  },
  {
    question: "Do you work with roofing companies outside of Utah?",
    answer:
      "Absolutely. While we're based in Utah, we work with roofing companies nationwide. All of our services are delivered digitally, so location is never a barrier. We've helped roofers across the country grow their businesses with AI.",
  },
];
