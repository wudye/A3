import { cookies } from "next/headers";
import { DEFAULT_LOCALE, normalizeLocale, type Locale } from "./locale";
import { translations } from "./translations";


export async function detectLocaleServer(): Promise<Locale> {
    const cookieStore = await cookies();

    let locale = cookieStore.get("locale")?.value;
    
    // 解码 URL 编码的 Cookie 值
    if (locale !== undefined) {
        try {
        locale = decodeURIComponent(locale);
        } catch {
        // 解码失败时保持原值
        }
    }
    
    return normalizeLocale(locale) || DEFAULT_LOCALE;
}

export async function setLocale(locale: string | Locale) : Promise<Locale> {
    const normalized = normalizeLocale(locale);
    const cookieStore = await cookies();
    cookieStore.set("locale", normalized, { path: "/", maxAge: 365 * 24 * 60 * 60,
         sameSite: "lax" });
    return normalized;
}

export async function getI18n(localeOverride?: string | Locale) {
  const locale = localeOverride
    ? normalizeLocale(localeOverride)
    : await detectLocaleServer();
    
  const t = translations[locale] ?? translations[DEFAULT_LOCALE];
  
  return {
    locale,
    t,
  };
}  