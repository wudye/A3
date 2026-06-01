// src/app/[locale]/layout.tsx
import { I18nProviderClient } from '@/components/I18nProviderClient';
import type React from 'react';
import enMessages from '@/messages/en.json';
import zhMessages from '@/messages/zh.json';

interface Props {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}

const messageMap = {
  en: enMessages,
  zh: zhMessages,
};

export default async function LocaleLayout({ children, params }: Props) {
  const { locale } = await params;
  
  // 直接用映射获取，不用动态导入
  const messages = messageMap[locale as keyof typeof messageMap] || enMessages;

  return (
    <I18nProviderClient locale={locale} messages={messages}>
      <script
        dangerouslySetInnerHTML={{
          __html: `document.documentElement.lang = "${locale}";`,
        }}
      />
      {children}
    </I18nProviderClient>
  );
}
