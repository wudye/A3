// 导出所有工具和类型
export { enUS } from "./locales/en_US";
export { zhCN } from "./locales/zh_CN";
export type { Translations } from "./locales/types";

export {
  DEFAULT_LOCALE,
  SUPPORTED_LOCALES,
  detectLocale,
  isLocale,
  normalizeLocale,
} from "./locale";
export type { Locale } from "./locale";