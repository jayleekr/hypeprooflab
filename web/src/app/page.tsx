'use client';

import { motion, useScroll, useTransform } from 'framer-motion';
import { useRef } from 'react';
import Link from 'next/link';

const fadeInUp = {
  initial: { opacity: 1, y: 0 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.8, ease: [0.25, 0.1, 0.25, 1] }
};

const stagger = {
  animate: {
    transition: {
      staggerChildren: 0.1
    }
  }
};

function FloatingOrb({ className, delay = 0 }: { className: string; delay?: number }) {
  return (
    <motion.div
      className={`absolute rounded-full blur-[100px] ${className}`}
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{
        y: [0, -50, 0],
        x: [0, 20, 0],
        scale: [1, 1.2, 1],
        opacity: [0.4, 0.7, 0.4],
      }}
      transition={{
        duration: 10,
        repeat: Infinity,
        ease: "easeInOut",
        delay,
      }}
    />
  );
}

function Logo() {
  return (
    <Link href="/">
      <motion.div 
        className="flex items-center gap-3 cursor-pointer"
        initial={{ opacity: 1 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1 }}
      >
        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-500 to-indigo-600 flex items-center justify-center">
          <span className="text-white font-bold text-sm">H</span>
        </div>
        <span className="text-white font-semibold text-lg tracking-tight">HypeProof AI</span>
      </motion.div>
    </Link>
  );
}

function NavLink({ children, href }: { children: React.ReactNode; href: string }) {
  return (
    <motion.a
      href={href}
      className="text-zinc-400 hover:text-white transition-colors duration-200 text-sm"
      whileHover={{ y: -1 }}
    >
      {children}
    </motion.a>
  );
}

function Hero() {
  const ref = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start start", "end start"]
  });
  
  const y = useTransform(scrollYProgress, [0, 1], [0, 200]);
  const opacity = useTransform(scrollYProgress, [0, 0.5], [1, 0]);

  return (
    <section ref={ref} className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Floating orbs */}
      <FloatingOrb className="w-[800px] h-[800px] bg-purple-600/30 -top-60 -left-60" delay={0} />
      <FloatingOrb className="w-[600px] h-[600px] bg-indigo-600/30 -bottom-40 -right-40" delay={2} />
      <FloatingOrb className="w-[400px] h-[400px] bg-violet-500/25 top-1/3 left-1/3" delay={4} />
      <FloatingOrb className="w-[300px] h-[300px] bg-blue-600/20 bottom-1/4 right-1/4" delay={6} />
      
      <motion.div 
        className="relative z-10 text-center px-6 max-w-4xl mx-auto"
        style={{ y, opacity }}
      >
        <motion.div
          variants={stagger}
          initial="initial"
          animate="animate"
          className="space-y-8"
        >
          {/* Badge */}
          <motion.div variants={fadeInUp}>
            <span className="glass px-4 py-2 text-xs text-zinc-400 uppercase tracking-widest">
              Research Lab
            </span>
          </motion.div>
          
          {/* Main heading */}
          <motion.h1 
            variants={fadeInUp}
            className="text-6xl md:text-8xl font-bold tracking-tight"
          >
            <span className="text-gradient">HypeProof AI</span>
          </motion.h1>
          
          {/* Tagline */}
          <motion.p 
            variants={fadeInUp}
            className="text-xl md:text-2xl text-zinc-500 max-w-2xl mx-auto leading-relaxed"
          >
            AI solves problems.
            <br />
            <span className="text-zinc-300">Humans define them.</span>
          </motion.p>
          
          {/* CTA */}
          <motion.div variants={fadeInUp} className="pt-8 flex justify-center">
            <motion.a
              href="mailto:jayleekr0125@gmail.com"
              className="glass px-8 py-4 text-white font-medium rounded-full border border-purple-500/30 hover:border-purple-500/60 transition-all duration-300 inline-flex items-center gap-2"
              whileHover={{ scale: 1.02, boxShadow: "0 0 30px rgba(168, 85, 247, 0.3)" }}
              whileTap={{ scale: 0.98 }}
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              Contact
            </motion.a>
          </motion.div>
        </motion.div>
      </motion.div>
      
      {/* Scroll indicator */}
      <motion.div 
        className="absolute bottom-12 left-1/2 -translate-x-1/2"
        initial={{ opacity: 1, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 1.5, duration: 0.8 }}
      >
        <motion.div
          className="w-6 h-10 rounded-full border border-zinc-700 flex justify-center pt-2"
          animate={{ opacity: [0.5, 1, 0.5] }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          <motion.div
            className="w-1 h-2 bg-zinc-500 rounded-full"
            animate={{ y: [0, 12, 0] }}
            transition={{ duration: 1.5, repeat: Infinity, ease: "easeInOut" }}
          />
        </motion.div>
      </motion.div>
    </section>
  );
}

function FeatureCard({ icon, title, description, delay }: { 
  icon: string; 
  title: string; 
  description: string;
  delay: number;
}) {
  return (
    <motion.div
      className="relative glass p-8 group cursor-pointer overflow-hidden"
      initial={{ opacity: 0, y: 40 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-100px" }}
      transition={{ duration: 0.6, delay, ease: [0.25, 0.1, 0.25, 1] }}
      whileHover={{ 
        y: -8, 
        transition: { duration: 0.3 },
      }}
    >
      <motion.div 
        className="absolute inset-0 bg-gradient-to-br from-purple-500/0 to-indigo-500/0 opacity-0 group-hover:opacity-100 transition-opacity duration-500"
        style={{ background: "radial-gradient(circle at 50% 50%, rgba(168, 85, 247, 0.1), transparent 70%)" }}
      />
      
      <motion.div 
        className="text-5xl mb-6"
        whileHover={{ scale: 1.1, rotate: 5 }}
        transition={{ type: "spring", stiffness: 300 }}
      >
        {icon}
      </motion.div>
      <h3 className="text-xl font-semibold text-white mb-3 group-hover:text-purple-400 transition-colors duration-300">
        {title}
      </h3>
      <p className="text-zinc-400 leading-relaxed">{description}</p>
      
      <motion.div 
        className="absolute bottom-0 left-0 right-0 h-[2px] bg-gradient-to-r from-purple-500 to-indigo-500 scale-x-0 group-hover:scale-x-100 transition-transform duration-500 origin-left"
      />
    </motion.div>
  );
}

function Features() {
  const features = [
    {
      icon: "🔬",
      title: "Research",
      description: "Pushing AI boundaries through daily experiments and rigorous validation"
    },
    {
      icon: "🎙️",
      title: "Content",
      description: "Audio-first content delivering actionable insights"
    },
    {
      icon: "📖",
      title: "Education",
      description: "New paradigms for learning in the age of AI"
    }
  ];

  return (
    <section id="features" className="py-32 px-6">
      <div className="max-w-6xl mx-auto">
        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 1, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <h2 className="text-4xl font-bold text-white mb-4">What We Do</h2>
          <p className="text-zinc-500 max-w-xl mx-auto">
            Three tracks to explore the future of AI
          </p>
        </motion.div>
        
        <div className="grid md:grid-cols-3 gap-6">
          {features.map((feature, i) => (
            <FeatureCard key={feature.title} {...feature} delay={i * 0.1} />
          ))}
        </div>
      </div>
    </section>
  );
}

// Sample columns data - in production, this would come from a CMS or API
const categoryStyles: Record<string, { gradient: string; icon: string }> = {
  "Research": { gradient: "from-purple-600/50 to-indigo-900/50", icon: "🔬" },
  "Analysis": { gradient: "from-blue-600/50 to-cyan-900/50", icon: "📊" },
  "Education": { gradient: "from-emerald-600/50 to-teal-900/50", icon: "📚" },
  "Opinion": { gradient: "from-orange-600/50 to-red-900/50", icon: "💭" },
};

const columns = [
  {
    slug: "claude-opus-4-6-alignment",
    title: "Claude Opus 4.6: When Safety Meets Soul",
    excerpt: "Anthropic's latest release isn't just an upgrade—it's a philosophical statement about where AI alignment is heading.",
    date: "2026-02-06",
    category: "Research",
  },
  {
    slug: "openai-agents-sdk",
    title: "The Rise of Agent Frameworks",
    excerpt: "From OpenAI Swarm to Claude Code SDK, the agent wars are heating up. Here's what it means for developers.",
    date: "2026-02-05",
    category: "Analysis",
  },
  {
    slug: "ai-education-paradigm",
    title: "Teaching AI to Kids: A New Curriculum",
    excerpt: "We designed an AI education program for middle schoolers. The results surprised even us.",
    date: "2026-02-03",
    category: "Education",
  }
];

function ColumnCard({ column, delay }: { column: typeof columns[0]; delay: number }) {
  const style = categoryStyles[column.category] || categoryStyles["Research"];
  
  return (
    <motion.article
      className="group cursor-pointer"
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-50px" }}
      transition={{ duration: 0.6, delay }}
    >
      <Link href={`/columns/${column.slug}`}>
        <div className="flex flex-col md:flex-row gap-6 p-6 glass rounded-2xl hover:border-purple-500/30 transition-all duration-300">
          {/* Image placeholder with category-specific gradient */}
          <div className={`w-full md:w-64 h-40 bg-gradient-to-br ${style.gradient} rounded-xl flex items-center justify-center overflow-hidden flex-shrink-0 group-hover:scale-[1.02] transition-transform duration-300`}>
            <span className="text-5xl opacity-60 group-hover:scale-110 transition-transform duration-300">{style.icon}</span>
          </div>
          
          {/* Content */}
          <div className="flex flex-col justify-center flex-1">
            <div className="flex items-center gap-3 mb-3">
              <span className="text-xs text-purple-400 uppercase tracking-wider font-medium">
                {column.category}
              </span>
              <span className="text-zinc-600">•</span>
              <span className="text-xs text-zinc-500">{column.date}</span>
            </div>
            
            <h3 className="text-xl font-semibold text-white mb-2 group-hover:text-purple-400 transition-colors">
              {column.title}
            </h3>
            
            <p className="text-zinc-400 text-sm leading-relaxed">
              {column.excerpt}
            </p>
            
            <div className="mt-4 flex items-center text-purple-400 text-sm font-medium opacity-0 group-hover:opacity-100 transition-opacity">
              Read more
              <svg className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </div>
        </div>
      </Link>
    </motion.article>
  );
}

function Columns() {
  return (
    <section id="columns" className="py-32 px-6">
      <div className="max-w-4xl mx-auto">
        <motion.div
          className="flex items-center justify-between mb-12"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <div>
            <h2 className="text-4xl font-bold text-white mb-2">Columns</h2>
            <p className="text-zinc-500">Sharp takes on AI, tech, and the future</p>
          </div>
          <Link 
            href="/columns" 
            className="text-purple-400 hover:text-purple-300 text-sm font-medium flex items-center gap-1 transition-colors"
          >
            View all
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </Link>
        </motion.div>
        
        <div className="space-y-6">
          {columns.map((column, i) => (
            <ColumnCard key={column.slug} column={column} delay={i * 0.1} />
          ))}
        </div>
      </div>
    </section>
  );
}

const memberColors: Record<string, string> = {
  "Jay": "from-purple-500 to-indigo-600",
  "Ryan": "from-blue-500 to-cyan-500",
  "JY": "from-emerald-500 to-teal-500",
  "TJ": "from-orange-500 to-red-500",
  "Kiwon": "from-pink-500 to-rose-500",
};

function TeamMember({ name, role, credential, delay }: { 
  name: string; 
  role: string; 
  credential?: string;
  delay: number;
}) {
  const gradient = memberColors[name] || "from-purple-500/20 to-indigo-500/20";
  
  return (
    <motion.div
      className="text-center group"
      initial={{ opacity: 0, scale: 0.9, y: 20 }}
      whileInView={{ opacity: 1, scale: 1, y: 0 }}
      viewport={{ once: true, margin: "-50px" }}
      transition={{ duration: 0.6, delay, ease: [0.25, 0.1, 0.25, 1] }}
    >
      <motion.div 
        className={`w-24 h-24 mx-auto mb-4 rounded-full bg-gradient-to-br ${gradient} p-[2px] cursor-pointer`}
        whileHover={{ scale: 1.1, rotate: 5 }}
        whileTap={{ scale: 0.95 }}
      >
        <div className="w-full h-full rounded-full bg-zinc-950 flex items-center justify-center">
          <span className="text-2xl font-bold text-white">{name[0]}</span>
        </div>
      </motion.div>
      <motion.h4 
        className="text-white font-semibold text-lg"
        whileHover={{ color: "#a855f7" }}
      >
        {name}
      </motion.h4>
      <p className="text-zinc-400 text-sm mt-1">{role}</p>
      {credential && (
        <p className="text-zinc-600 text-xs mt-1 max-w-[180px] mx-auto leading-relaxed">
          {credential}
        </p>
      )}
    </motion.div>
  );
}

function Philosophy() {
  return (
    <section className="py-32 px-6 relative overflow-hidden">
      <FloatingOrb className="w-[500px] h-[500px] bg-indigo-600/20 -left-40 top-0" delay={1} />
      
      <div className="max-w-4xl mx-auto relative z-10">
        <motion.div
          className="text-center"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 1 }}
        >
          <motion.p 
            className="text-2xl md:text-3xl text-zinc-300 leading-relaxed font-light"
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
          >
            &ldquo;We don&apos;t chase <span className="text-white font-medium">Hype</span>.
            <br />
            We <span className="text-purple-400 font-medium">prove</span> it.&rdquo;
          </motion.p>
          
          <motion.div 
            className="mt-12 h-px w-24 mx-auto bg-gradient-to-r from-transparent via-purple-500 to-transparent"
            initial={{ scaleX: 0 }}
            whileInView={{ scaleX: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 1, delay: 0.5 }}
          />
        </motion.div>
      </div>
    </section>
  );
}

function Team() {
  const members = [
    { name: "Jay", role: "Lead / Tech", credential: "Staff Engineer @ Silicon Valley" },
    { name: "Ryan", role: "Research / Data", credential: "Physics PhD, Quant Dev" },
    { name: "JY", role: "Research / AI", credential: "AI Engineer, M.S. Physics" },
    { name: "TJ", role: "Content / Media", credential: "Ex-Founder, Media Specialist" },
    { name: "Kiwon", role: "Marketing", credential: "GWU, Global Marketing" },
  ];

  return (
    <section id="team" className="py-32 px-6">
      <div className="max-w-4xl mx-auto">
        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 1, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <h2 className="text-4xl font-bold text-white mb-4">The Team</h2>
        </motion.div>
        
        <div className="grid grid-cols-2 md:grid-cols-5 gap-8 md:gap-6">
          {members.map((member, i) => (
            <TeamMember key={member.name} {...member} delay={i * 0.1} />
          ))}
        </div>
      </div>
    </section>
  );
}

function Footer() {
  return (
    <footer className="py-12 px-6 border-t border-white/5">
      <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
        <Logo />
        <div className="flex items-center gap-6">
          <Link href="/columns" className="text-zinc-500 hover:text-white text-sm transition-colors">
            Columns
          </Link>
          <Link href="#team" className="text-zinc-500 hover:text-white text-sm transition-colors">
            Team
          </Link>
        </div>
        <p className="text-zinc-600 text-sm">
          © 2026 HypeProof AI. All rights reserved.
        </p>
      </div>
    </footer>
  );
}

export default function Home() {
  return (
    <>
      <div className="gradient-bg" />
      <div className="grid-pattern" />
      <div className="noise" />
      
      {/* Navigation */}
      <motion.nav 
        className="fixed top-0 left-0 right-0 z-50 px-6 py-4 bg-zinc-950/50 backdrop-blur-lg border-b border-white/5"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.2 }}
      >
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <Logo />
          <div className="hidden md:flex items-center gap-8">
            <NavLink href="#features">What We Do</NavLink>
            <NavLink href="#columns">Columns</NavLink>
            <NavLink href="#team">Team</NavLink>
          </div>
        </div>
      </motion.nav>
      
      <main>
        <Hero />
        <Features />
        <Columns />
        <Philosophy />
        <Team />
      </main>
      
      <Footer />
    </>
  );
}
