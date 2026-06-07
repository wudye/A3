import type { Translations } from "./types";

export const enUS: Translations = {
  locale: {
    localName: "English",
  },
  common: {
    home: "Home",
    settings: "Settings",
    save: "Save",
    cancel: "Cancel",
  },
  home: {
    title: "Trade, Predict And Communicate",
    description: "AI Agent Platform",
  },
  landing: {
    badge: "AI-Powered Trading, Prediction and Communication Platform",
    headline: "Supercharge Your Trading with",
    headlineHighlight: "AI Agents",
    subheading: "Combine fundamental analysis, quantitative modeling, and machine learning — backtest strategies, predict trends, and communicate with AI digital humans. All in one platform.",
    ctaPrimary: "Get Started Free",
    ctaSecondary: "Watch Demo",
    stats: [
      { label: "Strategies Backtested(Fake Data)", value: "10M+" },
      { label: "AI Predictions Daily(Fake Data)", value: "500K+" },
      { label: "Active Traders(Fake Data)", value: "50K+" },
    ],
  },
  features: {
    sectionTitle: "Three Pillars of Intelligent Trading",
    sectionDescription: "A unified platform where AI agents handle the heavy lifting — so you can focus on making better decisions.",
    items: [
      {
        title: "Trade",
        description: "Fundamental & quantitative analysis powered by AI. Build, test, and deploy trading strategies with intelligent backtesting and real-time market data.",
      },
      {
        title: "Predict",
        description: "Machine learning models that analyze market trends, detect patterns, and forecast future movements — giving you the edge before the market moves.",
      },
      {
        title: "Communicate",
        description: "AI digital humans for entertainment, education, and real-time communication. Your intelligent companion that grows and learns with you.",
      },
    ],
  },
  navigation: {
    home: "Home",
    github: "GitHub",
    dashboard: "Dashboard",
    profile: "Profile",
  },
  messages: {
    welcome: (name) => `Welcome, ${name}!`,
    itemsCount: (count) => `${count} items`,
  },

  footer: {
    title: "Trade, Predict and Communicate — powered by AI",
    license: "Licensed under MIT License",
    description: "@ {year} My AI Platform. Built for the finance, the prediction and the communication.",
  },
  hero: {
    content: [
      "Trading",
      "Future Predictions",
      "AI Communication"
    ],
    description: "Trading,  Prediction and Communication - Powered by AI.", 
    versionInfo: "Version 1.0 By Mingwei Wu"
  
  },
};
    

