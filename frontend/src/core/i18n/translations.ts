import type {Locale} from "./locale"
import { Translations } from "./locales/types"
import { enUS } from "./locales/en_US"
import { zhCN } from "./locales/zh_CN"


export const translations: Record<Locale, Translations> = {
    "en-US": enUS,
    "zh-CN": zhCN,
}