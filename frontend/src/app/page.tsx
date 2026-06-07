"use client";

import { Footer } from "@/components/landing/footer";
import { Header } from "@/components/landing/header";
import { Hero } from "@/components/landing/hero";
import { Section } from "@/components/landing/section";
import { useI18n } from "@/core/i18n/hooks";
import {
  TrendingUp,
  BrainCircuit,
  MessageCircle,
  Play,
  ArrowRight,
  BarChart3,
  Sparkles,
  ChevronRight,
} from "lucide-react";

export default function Home() {
  const { t } = useI18n();

  return (
    <div className="flex flex-col min-h-screen bg-background font-sans">
      <Header />

      {/* ====== Hero Section ====== */}
      <main className="flex w-full flex-col">
        <Hero />
        <Section />

      </main>
  

      {/* ====== Footer decoration ====== */}
      <Footer />
  
    </div>
  );
}
