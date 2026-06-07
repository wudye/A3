"use client";

import { useI18n } from "@/core/i18n/hooks";
import { SUPPORTED_LOCALES } from "@/core/i18n";
import { ThemeToggle } from "@/components/theme-toggle";
import { Sparkles, Globe, ChevronDown, Zap } from "lucide-react";
import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";

export function Header() {
  const { locale, t, changeLocale } = useI18n();
  const [langOpen, setLangOpen] = useState(false);
  const langRef = useRef<HTMLDivElement>(null);

  // 点击外部关闭语言下拉菜单
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (langRef.current && !langRef.current.contains(e.target as Node)) {
        setLangOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // 当前语言的本地名称映射
  const localeNames: Record<string, string> = {
    en_US: "EN",
    zh_CN: "中文",
  };

  return (
    <header className="fixed top-0 left-0 right-0 z-50">
      {/* 外层容器：毛玻璃 + 底部微妙渐变边框 */}
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div
          className="flex items-center justify-between h-16 rounded-b-2xl
            bg-background/80 backdrop-blur-xl
            border-b border-border/40 shadow-sm
            shadow-black/5 dark:shadow-black/20"
        >
          {/* ====== 左侧：品牌 Logo & 名称 ====== */}
          <div className="flex items-center gap-3">
            {/* AI 图标：旋转渐变圆环 + 内部火花 */}
            <div className="relative flex items-center justify-center w-9 h-9 rounded-xl bg-gradient-to-br from-violet-500 via-purple-500 to-fuchsia-500 shadow-lg shadow-purple-500/25">
              <Sparkles className="w-5 h-5 text-white" strokeWidth={2.5} />
              {/* 脉冲动画环 */}
              <span className="absolute inset-0 rounded-xl animate-ping bg-purple-400/20 opacity-75" />
            </div>

            {/* 品牌文字组 */}
            <div className="flex flex-col">
              <h1
                className="text-lg font-bold tracking-tight leading-none
                  bg-gradient-to-r from-violet-600 via-fuchsia-500 to-orange-400
                  dark:from-violet-400 dark:via-fuchsia-300 dark:to-orange-300
                  bg-clip-text text-transparent"
              >
                {t.home.title}
              </h1>
              <span className="flex items-center gap-1 text-[10px] font-medium text-muted-foreground/70 tracking-wider uppercase mt-0.5">
                <Zap className="w-2.5 h-2.5 text-amber-500" />
                {t.home.description}
              </span>
            </div>
          </div>

          {/* ====== 中间：导航链接（大屏可见） ====== */}
          <nav className="hidden md:flex items-center gap-1">
            {[
              { key: "home", label: t.navigation.home },
              { key: "https://github.com/wudye/A3", label: t.navigation.github },
              { key: "dashboard", label: t.navigation.dashboard },
              { key: "profile", label: t.navigation.profile },
            ].map((item) => (
              <a
                key={item.key}
                href={item.key === "home" ? "/" : 
                  item.key.startsWith("http") ? item.key : `#${item.key}`}
                className={`
                  relative px-4 py-2 text-sm font-medium text-muted-foreground
                  transition-colors duration-200 rounded-lg
                  hover:text-foreground hover:bg-accent/50
                  group
                `}
              >
                {item.label}
                {/* 悬停时底部滑入的下划线 */}
                <span
                  className="absolute bottom-1 left-1/2 -translate-x-1/2 w-0 h-0.5
                    rounded-full bg-gradient-to-r from-violet-500 to-fuchsia-500
                    transition-all duration-300 group-hover:w-4/5"
                />
              </a>
            ))}
          </nav>

          {/* ====== 右侧：操作控件 ====== */}
          <div className="flex items-center gap-1.5">
            {/* 主题切换 */}
            <ThemeToggle />

            {/* 分隔线 */}
            <div className="w-px h-6 bg-border/60 mx-1" />

            {/* 语言切换下拉 */}
            <div ref={langRef} className="relative">
              <button
                onClick={() => setLangOpen(!langOpen)}
                className="
                  flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium
                  rounded-lg border border-border/60 bg-background/60
                  hover:bg-accent/50 hover:border-border
                  transition-all duration-200 cursor-pointer
                "
              >
                <Globe className="w-4 h-4 text-muted-foreground" />
                <span>{localeNames[locale] || locale}</span>
                <ChevronDown
                  className={`w-3.5 h-3.5 text-muted-foreground transition-transform duration-200 ${
                    langOpen ? "rotate-180" : ""
                  }`}
                />
              </button>

              {/* 下拉面板 */}
              {langOpen && (
                <div
                  className="
                    absolute right-0 top-full mt-2 min-w-[140px]
                    rounded-xl border border-border/60 bg-popover/95 backdrop-blur-xl
                    shadow-lg shadow-black/10 p-1.5
                    animate-in fade-in slide-in-from-top-2 duration-200
                  "
                >
                  {SUPPORTED_LOCALES.map((lang) => (
                    <button
                      key={lang}
                      onClick={() => {
                        changeLocale(lang);
                        setLangOpen(false);
                      }}
                      className={`
                        w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm
                        transition-colors duration-150 cursor-pointer
                        ${
                          locale === lang
                            ? "bg-accent font-semibold text-foreground"
                            : "text-muted-foreground hover:bg-accent/50 hover:text-foreground"
                        }
                      `}
                    >
                      <Globe className="w-4 h-4 opacity-60" />
                      <span>{localeNames[lang] || lang.toUpperCase()}</span>
                      {locale === lang && (
                        <span className="ml-auto w-1.5 h-1.5 rounded-full bg-violet-500" />
                      )}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
      {/* 底部微妙渐变光线装饰 */}
      <div
        className="absolute bottom-0 left-1/2 -translate-x-1/2 w-2/3 h-px
          bg-gradient-to-r from-transparent via-violet-500/30 to-transparent"
      />
    </header>
  );
}
