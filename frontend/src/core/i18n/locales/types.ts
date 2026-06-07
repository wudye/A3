// 定义完整的翻译结构
export interface Translations {
  // 语言元信息
  locale: {
    localName: string; // 语言本地化名称
  };
  
  // 通用词汇
  common: {
    home: string;
    settings: string;
    save: string;
    cancel: string;
  };
  
  // 页面特定翻译
  home: {
    title: string;
    description: string;
  };
  
  // 着陆页 Hero 区域
  landing: {
    badge: string;
    headline: string;
    headlineHighlight: string;
    subheading: string;
    ctaPrimary: string;
    ctaSecondary: string;
    stats: {
      label: string;
      value: string;
    }[];
  };
  
  // 功能模块卡片
  features: {
    sectionTitle: string;
    sectionDescription: string;
    items: {
      title: string;
      description: string;
    }[];
  };
  
  // 导航
  navigation: {
    home: string;
    github: string;
    dashboard: string;
    profile: string;
  };
  
  // 支持函数类型（动态翻译）
  messages: {
    welcome: (name: string) => string;
    itemsCount: (count: number) => string;
  };


  footer: {
    title: string;
    license: string;
    description: string;
  };
  hero: {
    content: string[];
    description: string;
    versionInfo: string;
  }
}