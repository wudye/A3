'use client';  // ← 必须加这个！客户端组件才能用 hook

import Header from "@/components/Header";
import { useI18n } from '@/components/I18nProviderClient';  // ← 修正：useI18n

function HomeContent() {
  const { t, locale } = useI18n();  // ← 用 useI18n()

  return (
    <div className="flex flex-col flex-1 items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <Header />
      
      <main className="flex flex-1 w-full max-w-3xl flex-col items-center justify-between py-32 px-16 bg-white dark:bg-black sm:items-start">
        <h1 className="text-4xl font-bold mb-8">{t('welcome.title')}</h1>
        <p className="text-lg text-gray-600 mb-8">{t('welcome.description')}</p>
        
        <div className="grid grid-cols-3 gap-6">
          <div className="p-6 bg-white rounded-lg shadow border">
            <h2 className="text-xl font-semibold">💰 {t('home.investment')}</h2>
            <p className="text-gray-500 mt-2">Investment</p>
          </div>
          
          <div className="p-6 bg-white rounded-lg shadow border">
            <h2 className="text-xl font-semibold">🔮 {t('home.prediction')}</h2>
            <p className="text-gray-500 mt-2">Predict</p>
          </div>
          
          <div className="p-6 bg-white rounded-lg shadow border">
            <h2 className="text-xl font-semibold">💬 {t('home.communication')}</h2>
            <p className="text-gray-500 mt-2">Talk</p>
          </div>
        </div>
      </main>
    </div>
  );
}

export default function Home() {
  return <HomeContent />;
}
