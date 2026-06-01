'use client';

import { createContext, useContext, useState, useEffect, type ReactNode } from 'react';

interface Messages {
  [key: string]: any;
}

interface I18nContextType {
  locale: string;
  messages: Messages;
  t: (key: string) => string;
  setLocale: (locale: string) => void;
}

const I18nContext = createContext<I18nContextType>({
  locale: 'en',
  messages: {},
  t: (key) => key,
  setLocale: () => {},
});

export function useI18n() {
  return useContext(I18nContext);
}

// 🔑 Props 名改为匹配 layout 传入的
export function I18nProviderClient({
  children,
  locale,
  messages,
}: {
  children: ReactNode;
  locale: string;
  messages: Messages;
}) {
  const [currentLocale, setCurrentLocale] = useState(locale);
  const [currentMessages, setCurrentMessages] = useState(messages);

  // 🔍 调试：打印接收到的数据
  console.log('📦 I18nProvider 收到:');
  console.log('  locale:', locale);
  console.log('  messages:', JSON.stringify(messages, null, 2));

  // 翻译函数：支持嵌套 key 如 "nav.title"
  const t = (key: string): string => {
    const keys = key.split('.');
    let result: any = currentMessages;
    
    console.log(`🔍 t("${key}") 开始查找:`);
    for (const k of keys) {
      console.log(`  -> ["${k}"] =`, result?.[k]);
      result = result?.[k];
    }
    console.log(`  ✅ 最终结果: "${result || key}"`);
    
    return result || key;
  };

  // 切换语言并刷新页面
  const changeLocale = (newLocale: string) => {
    document.cookie = `locale=${newLocale}; path=/; max-age=31536000`;
    window.location.href = window.location.pathname.replace(/^\/[^\/]+/, newLocale);
  };

  return (
    <I18nContext.Provider 
      value={{ locale: currentLocale, messages: currentMessages, t, setLocale: changeLocale }}
    >
      {children}
    </I18nContext.Provider>
  );
}
