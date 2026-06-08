import {
  Play,
  ArrowRight,
  Sparkles,
  ChevronRight,
  
} from "lucide-react";
import { useI18n } from "@/core/i18n/hooks";

import Link from "next/link";  // add this import


const featureIcons = [
  { src: "/images/trade.png", alt: "Trade", bg: "bg-emerald-500/10", href: "/api/trade" },       // ← your URLs
  { src: "/images/predict.png", alt: "Predict", bg: "bg-violet-500/10", href: "/api/predict" },
  { src: "/images/human.jpg", alt: "Human", bg: "bg-orange-500/10", href: "/api/vhtalk" },
];

export function Section() {
    const { t } = useI18n();
    return (
      <>
      <section className="relative flex flex-col items-center justify-center pt-2 pb-2 px-4 sm:px-6 lg:px-8 overflow-hidden">
        {/* Background glow orbs */}
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-violet-500/10 rounded-full blur-[128px]" />
          <div className="absolute top-1/3 right-1/4 w-80 h-80 bg-fuchsia-500/8 rounded-full blur-[100px]" />
          <div className="absolute bottom-1/4 left-1/2 w-72 h-72 bg-orange-500/6 rounded-full blur-[96px]" />
        </div>

        {/* Grid pattern overlay */}
        <div
          className="absolute inset-0 opacity-[0.03] dark:opacity-[0.05]"
          style={{
            backgroundImage:
              "linear-gradient(rgb(120,120,120) 1px, transparent 1px), linear-gradient(90deg, rgb(120,120,120) 1px, transparent 1px)",
            backgroundSize: "64px 64px",
          }}
        />

        <div className="relative z-10 max-w-4xl mx-auto text-center">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-violet-500/20 bg-violet-500/5 text-sm font-medium text-violet-600 dark:text-violet-400 mb-8">
            <Sparkles className="w-3.5 h-3.5" />
            {t.landing.badge}
          </div>

          {/* Headline */}
          <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold tracking-tight leading-[1.1] text-foreground mb-6">
            {t.landing.headline}{" "}
            <span
              className="bg-gradient-to-r from-violet-600 via-fuchsia-500 to-orange-400
                dark:from-violet-400 dark:via-fuchsia-300 dark:to-orange-300
                bg-clip-text text-transparent"
            >
              {t.landing.headlineHighlight}
            </span>
          </h1>

          {/* Subheading */}
          <p className="max-w-2xl mx-auto text-base sm:text-lg text-muted-foreground leading-relaxed mb-10">
            {t.landing.subheading}
          </p>

          {/* CTA Buttons */}
          <div className="flex items-center justify-center gap-4 mb-16">
            <button
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl
                bg-foreground text-background font-semibold text-sm
                hover:bg-foreground/90 transition-all duration-200
                shadow-lg shadow-foreground/10 hover:shadow-foreground/20 hover:-translate-y-0.5"
            >
              {t.landing.ctaPrimary}
              <ArrowRight className="w-4 h-4" />
            </button>
            <button
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl
                border border-border bg-background font-medium text-sm
                hover:bg-accent/50 transition-all duration-200"
            >
              <Play className="w-4 h-4" />
              {t.landing.ctaSecondary}
            </button>
          </div>

          {/* Stats */}
          <div className="flex items-center justify-center gap-8 sm:gap-16">
            {t.landing.stats.map((stat) => (
              <div key={stat.label} className="text-center">
                <div className="text-2xl sm:text-3xl font-bold text-foreground tracking-tight">
                  {stat.value}
                </div>
                <div className="text-xs sm:text-sm text-muted-foreground mt-1">
                  {stat.label}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>
      
      {/* ====== Features Section ====== */}
      <section className="py-20 sm:py-32 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto">
          {/* Section header */}
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-foreground tracking-tight mb-4">
              {t.features.sectionTitle}
            </h2>
            <p className="max-w-2xl mx-auto text-muted-foreground text-base sm:text-lg leading-relaxed">
              {t.features.sectionDescription}
            </p>
          </div>

          {/* Feature cards */}
          <div className="grid gap-6 md:grid-cols-3">
            {t.features.items.map((feature, i) => {
              const iconConfig = featureIcons[i] ?? featureIcons[0];
              const { src, alt, bg , href } = iconConfig;  
              return (
                <div
                  key={feature.title}
                  className="group relative rounded-2xl border border-border/60 bg-card
                    p-8 transition-all duration-300
                    hover:border-violet-500/20 hover:shadow-lg hover:shadow-violet-500/5
                    hover:-translate-y-1"
                >
                  {/* Icon */}
                  <div
                    className={`inline-flex items-center justify-center w-12 h-12 rounded-xl ${bg} mb-6
                      ring-1 ring-border/50 group-hover:ring-violet-500/20 transition-all duration-300`}
                  >
                    <img src={src} alt={alt} className="w-6 h-6" />
                  </div>

                  {/* Title */}
                  <h3 className="text-xl font-semibold text-foreground mb-3">
                    {feature.title}
                  </h3>

                  {/* Description */}
                  <p className="text-sm text-muted-foreground leading-relaxed mb-6">
                    {feature.description}
                  </p>

                  {/* Learn more link */}
                  <Link href={href}
                    className="inline-flex items-center gap-1 text-sm font-medium
                      bg-gradient-to-r from-violet-600 to-fuchsia-500
                      dark:from-violet-400 dark:to-fuchsia-400
                      bg-clip-text text-transparent
                      group-hover:gap-2 transition-all duration-200"
                  >
                    Learn more
                    <ChevronRight className="w-3.5 h-3.5 text-violet-500" />
                  </Link>
                </div>
              );
            })}
          </div>
        </div>
      </section>
      </>
    );
  }