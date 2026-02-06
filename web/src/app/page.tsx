'use client';

import { motion, useScroll, useTransform } from 'framer-motion';
import { useRef } from 'react';

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
    <motion.div 
      className="flex items-center gap-3"
      initial={{ opacity: 1 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 1 }}
    >
      <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-500 to-indigo-600 flex items-center justify-center">
        <span className="text-white font-bold text-sm">H</span>
      </div>
      <span className="text-white font-semibold text-lg tracking-tight">HypeProof</span>
    </motion.div>
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
      {/* Floating orbs - enhanced visibility */}
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
            <span className="text-gradient">HypeProof</span>
          </motion.h1>
          
          {/* Tagline */}
          <motion.p 
            variants={fadeInUp}
            className="text-xl md:text-2xl text-zinc-500 max-w-2xl mx-auto leading-relaxed"
          >
            AI가 문제를 푼다.
            <br />
            <span className="text-zinc-300">인간은 문제를 정의한다.</span>
          </motion.p>
          
          {/* CTA */}
          <motion.div variants={fadeInUp} className="pt-8 flex flex-col sm:flex-row gap-4 justify-center">
            <motion.a
              href="https://discord.gg/clawd"
              target="_blank"
              rel="noopener noreferrer"
              className="glass px-8 py-4 text-white font-medium rounded-full border border-purple-500/30 hover:border-purple-500/60 transition-all duration-300 inline-flex items-center gap-2"
              whileHover={{ scale: 1.02, boxShadow: "0 0 30px rgba(168, 85, 247, 0.3)" }}
              whileTap={{ scale: 0.98 }}
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028 14.09 14.09 0 0 0 1.226-1.994.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.928 1.793 8.18 1.793 12.062 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.892.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.03zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z"/>
              </svg>
              Join Discord
            </motion.a>
            <motion.a
              href="mailto:jayleekr0125@gmail.com"
              className="px-8 py-4 text-zinc-400 font-medium rounded-full border border-zinc-700 hover:border-zinc-500 hover:text-white transition-all duration-300"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              Contact Us
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
      {/* Hover glow effect */}
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
      
      {/* Bottom gradient line on hover */}
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
      description: "AI의 한계를 매일 밀어붙이는 실험과 검증"
    },
    {
      icon: "🎙️",
      title: "Content",
      description: "Audio-First 콘텐츠로 인사이트 전달"
    },
    {
      icon: "📖",
      title: "Education",
      description: "AI 시대의 새로운 교육 패러다임"
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
            세 가지 트랙으로 AI의 미래를 탐구합니다
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
            &ldquo;우리는 <span className="text-white font-medium">Hype</span>를 쫓지 않습니다.
            <br />
            <span className="text-purple-400 font-medium">증명</span>합니다.&rdquo;
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
        <p className="text-zinc-600 text-sm">
          © 2026 HypeProof Lab. All rights reserved.
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
            <NavLink href="#team">Team</NavLink>
          </div>
        </div>
      </motion.nav>
      
      <main>
        <Hero />
        <Features />
        <Philosophy />
        <Team />
      </main>
      
      <Footer />
    </>
  );
}
