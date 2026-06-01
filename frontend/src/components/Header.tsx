'use client';

import Link from 'next/link';
import { useI18n } from './I18nProviderClient';

export default function Header() {
  const { locale, t, setLocale } = useI18n();

  console.log('=== HEADER DEBUG ===');
  console.log('locale:', locale);
  console.log('t("nav.title"):', t('nav.title'));
  console.log('t("nav.subtitle"):', t('nav.subtitle'));
  console.log('====================');

  return (
    <header className="flex items-center justify-between gap-4 border-b px-6 py-4 bg-white">
      {/* 左侧：标题 + 语言标识 */}
      <div className="flex items-center gap-3">
        <Link href={`/${locale}`} className="text-lg font-bold tracking-wide">
          🌐 {t('nav.title')}
        </Link>
        {/* 当前语言指示器 */}
        <span className={`px-2 py-0.5 rounded text-xs font-bold ${
          locale === 'zh' ? 'bg-red-100 text-red-700' : 'bg-blue-100 text-blue-700'
        }`}>
          {locale.toUpperCase()}
        </span>
      </div>

      <nav className="flex items-center gap-3">
        {/* 导航链接 */}
        <Link href={`/${locale}/introduce`}
          className="rounded-md bg-black px-4 py-2 text-sm font-medium text-white hover:bg-zinc-800 transition-colors">
          {t('nav.subtitle').split(',')[0]}
        </Link>

        <a href="https://github.com" target="_blank" rel="noreferrer"
          className="rounded-md border px-4 py-2 text-sm font-medium hover:bg-zinc-100 transition-colors">
          GitHub
        </a>

        {/* 🔘 语言切换按钮 */}
        <div className="flex items-center rounded-lg border-2 overflow-hidden">
          <button
            onClick={() => setLocale?.('en')}
            className={`px-4 py-2 text-sm font-semibold transition-all ${
              locale === 'en' 
                ? 'bg-blue-600 text-white shadow-inner' 
                : 'bg-white text-gray-600 hover:bg-gray-50'
            }`}
          >
            🇺🇸 English
          </button>
          
          <button
            onClick={() => setLocale?.('zh')}
            className={`px-4 py-2 text-sm font-semibold transition-all border-l ${
              locale === 'zh' 
                ? 'bg-red-500 text-white shadow-inner' 
                : 'bg-white text-gray-600 hover:bg-gray-50'
            }`}
          >
            🇨🇳 中文
          </button>
          
        </div>
        
        <div className="w-0.5 h-6 bg-gray-300 mx-2" />
        {/* 在 Header.tsx 里添加：*/}
            <button 
            onClick={() => {
                document.cookie = 'locale=; path=/; max-age=0;';
                window.location.href = '/';
            }}
            style={{ fontSize: '12px', color: '#999' }}
            >
            🗑️ Clear Cookie & Test
            </button>

           </nav>
    
    </header>
  );
}
