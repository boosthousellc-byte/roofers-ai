export interface Service {
  icon: string;
  title: string;
  description: string;
  features: string[];
  slug: string;
}

export interface Testimonial {
  name: string;
  title: string;
  company: string;
  quote: string;
  rating: number;
}

export interface Stat {
  value: string;
  label: string;
  description: string;
}

export interface FAQ {
  question: string;
  answer: string;
}

export interface BlogPost {
  slug: string;
  title: string;
  description: string;
  date: string;
  author: string;
  category: string;
  tags: string[];
  readingTime: string;
  content: string;
}

export interface NavLink {
  label: string;
  href: string;
}
