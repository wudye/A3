import type { Translations } from "./types";



export const zhCN: Translations = {
  locale: {
    localName: "中文",
  },
  common: {
    home: "首页",
    settings: "设置",
    save: "保存",
    cancel: "取消",
  },
  home: {
    title: "交易、预测和交流",
    description: "AI 代理平台",
  },
  landing: {
    badge: "AI 驱动的交易, 预测，交流平台",
    headline: "用",
    headlineHighlight: "AI 智能代理",
    subheading: "融合基本面分析、量化建模与机器学习 — 回测策略、预测趋势、与 AI 数字人实时沟通。一切尽在一站式平台。",
    ctaPrimary: "免费开始使用",
    ctaSecondary: "观看演示",
    stats: [
      { label: "已回测策略", value: "1000万+" },
      { label: "每日 AI 预测", value: "50万+" },
      { label: "活跃交易者", value: "5万+" },
    ],
  },
  features: {
    sectionTitle: "智能交易的三大支柱",
    sectionDescription: "一个统一的平台，让 AI 代理处理繁重工作 — 您只需专注于做出更好的决策。",
    items: [
      {
        title: "交易",
        description: "AI 驱动的基本面与量化分析。通过智能回测和实时市场数据，构建、测试并部署交易策略。",
      },
      {
        title: "预测",
        description: "机器学习模型分析市场趋势、检测模式并预测未来走势 — 让您在市场变动之前抢占先机。",
      },
      {
        title: "交流",
        description: "AI 数字人，用于娱乐、教育和实时沟通。您的智能伴侣，与您共同成长、共同学习。",
      },
    ],
  },
  navigation: {
    home: "首页",
    github: "GitHub",
    dashboard: "仪表板",
    profile: "个人资料",
  },
  messages: {
    welcome: (name) => `欢迎，${name}！`,
    itemsCount: (count) => `${count} 个项目`,
  },
  footer: {
    title: "交易、预测和交流 — 由 AI 驱动",
    license: "MIT 许可证授权",
    description: "@ {year} 我的 AI 平台。为金融、预测和交流而生。",
  },
  hero: {
    content: [
      "智能交易策略",
      "未来预测",
      "AI 数字人交流"
    ],
    description: "交易、预测和交流 — 由 AI 驱动",
    versionInfo: "版本 1.0 包括 Agents Harness",
  },

};