import type {Locale} from "./locale"
import {createContext, useContext} from "react"

export interface I18nContextType{
    locale: Locale,
    setLocale: (locale: Locale) => void;
}

export const I18nContext = createContext<I18nContextType | null>(null)

export const useI18n = () => useContext(I18nContext)