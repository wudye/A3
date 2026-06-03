const LOCALE_COOKIE_NAME = "locale"

export function getLocaleFromCookie(): string | null {
    if (typeof document === "undefined") return null;

    const cookies = document.cookie.split(";");
    for (const cookie of cookies) {
        const [name, value] = cookie.trim().split("=");
        if (name === LOCALE_COOKIE_NAME) {
            return decodeURIComponent(value ?? "");
        }
    }
    return null;
}


export function setLocaleInCookie(locale: string) : void {
    if (typeof document === "undefined") return;

    const maxAge = 365 * 24 * 60 * 60;
    document.cookie = `${LOCALE_COOKIE_NAME}=${encodeURIComponent(locale)}; max-age=${maxAge}; path=/;SameSite=Lax`;
}

export async function getLocaleFromCookieServer(): Promise<string | null> {

    try{
        const {cookies} = await import("next/headers")
        const cookieStore = await cookies()
        return cookieStore.get(LOCALE_COOKIE_NAME)?.value ?? null
    } catch {
        return null
    }

    
}