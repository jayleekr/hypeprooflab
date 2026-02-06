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
      className={`absolute rounded-full blur-3xl ${className}`}
      animate={{
        y: [0, -30, 0],
        scale: [1, 1.1, 1],
        opacity: [0.3, 0.5, 0.3],
      }}
      transition={{
        duration: 8,
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
      {/* Floating orbs */}
      <FloatingOrb className="w-[600px] h-[600px] bg-purple-600/20 -top-40 -left-40" delay={0} />
      <FloatingOrb className="w-[500px] h-[500px] bg-indigo-600/20 -bottom-20 -right-20" delay={2} />
      <FloatingOrb className="w-[300px] h-[300px] bg-violet-600/20 top-1/2 left-1/4" delay={4} />
      
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
          <motion.div variants={fadeInUp} className="pt-8">
            <motion.button
              className="glass px-8 py-4 text-white font-medium rounded-full border border-purple-500/30 hover:border-purple-500/60 transition-all duration-300"
              whileHover={{ scale: 1.02, boxShadow: "0 0 30px rgba(168, 85, 247, 0.3)" }}
              whileTap={{ scale: 0.98 }}
            >
              Join the Lab →
            </motion.button>
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
      className="glass p-8 group cursor-pointer"
      initial={{ opacity: 1, y: 40 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-100px" }}
      transition={{ duration: 0.6, delay }}
      whileHover={{ y: -4, transition: { duration: 0.2 } }}
    >
      <div className="text-4xl mb-4">{icon}</div>
      <h3 className="text-xl font-semibold text-white mb-2 group-hover:text-purple-400 transition-colors">
        {title}
      </h3>
      <p className="text-zinc-500 leading-relaxed">{description}</p>
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
    <section className="py-32 px-6">
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

function TeamMember({ name, role, credential, delay }: { 
  name: string; 
  role: string; 
  credential?: string;
  delay: number;
}) {
  return (
    <motion.div
      className="text-center"
      initial={{ opacity: 1, scale: 0.9 }}
      whileInView={{ opacity: 1, scale: 1 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5, delay }}
    >
      <motion.div 
        className="w-20 h-20 mx-auto mb-4 rounded-full bg-gradient-to-br from-purple-500/20 to-indigo-500/20 border border-white/10 flex items-center justify-center"
        whileHover={{ scale: 1.1, borderColor: "rgba(168, 85, 247, 0.5)" }}
      >
        <span className="text-2xl font-bold text-white/80">{name[0]}</span>
      </motion.div>
      <h4 className="text-white font-medium">{name}</h4>
      <p className="text-zinc-500 text-sm">{role}</p>
      {credential && <p className="text-zinc-600 text-xs mt-1">{credential}</p>}
    </motion.div>
  );
}

function Team() {
  const members = [
    { name: "Jay", role: "Host / Tech", credential: "Silicon Valley Staff Engineer" },
    { name: "지웅", role: "Tech / Panel", credential: "Physics PhD, Quant Dev" },
    { name: "진용", role: "Tech / Panel", credential: "AI Engineer @Remember, 물리학 석사" },
    { name: "TJ", role: "Content / Edit" },
    { name: "Kiwon", role: "Marketing" },
  ];

  return (
    <section className="py-32 px-6">
      <div className="max-w-4xl mx-auto">
        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 1, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <h2 className="text-4xl font-bold text-white mb-4">The Team</h2>
        </motion.div>
        
        <div className="flex flex-wrap justify-center gap-12">
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
        className="fixed top-0 left-0 right-0 z-50 px-6 py-4"
        initial={{ opacity: 1, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <Logo />
          <div className="hidden md:flex items-center gap-8">
            <NavLink href="#research">Research</NavLink>
            <NavLink href="#content">Content</NavLink>
            <NavLink href="#team">Team</NavLink>
          </div>
        </div>
      </motion.nav>
      
      <main>
        <Hero />
        <Features />
        <Team />
      </main>
      
      <Footer />
    </>
  );
}
