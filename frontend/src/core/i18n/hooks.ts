"use client"

import { useEffect } from "react"
import { useI18nContext } from "./context"
import { getLocaleFromCookie, setLocaleInCookie } from "./cookies"
import { DEFAULT_LOCALE, detectLocale, normalizeLocale } from "./locale"
import { translations } from "./translations"


export  function useI18n() {
    const {locale, setLocale} = useI18nContext()

    const t = translations[locale] ?? translations[DEFAULT_LOCALE];

    const changeLocale = (newLocale: string) => {
        setLocale(newLocale as any);
        setLocaleInCookie(newLocale);
    };

    useEffect(() => {
        const saved = getLocaleFromCookie();
        if (saved) {
            const normalizedLocale = normalizeLocale(saved);
            if (saved !== normalizedLocale) {
                setLocaleInCookie(normalizedLocale);
            }
            return;
        }

        const detected = detectLocale();
        setLocale(detected);
        setLocaleInCookie(detected);
    }, [setLocale]);
    return {
        locale,
        t,
        changeLocale,
    };

}