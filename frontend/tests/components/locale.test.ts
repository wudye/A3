import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";

const mod = await import("@/core/i18n/locale");
const { detectLocale, DEFAULT_LOCALE } = mod;

describe("detectLocale", () => {
    let realWindow: unknown;
    let realNavigator: unknown;

    beforeEach(() => {
        vi.resetModules()
        realWindow = (global as any).window;
        realNavigator = (global).navigator;

    });
    afterEach(() => {
        (global as unknown).window = realWindow;
        (global as unknown).navigator = realNavigator;
    });

    it("return DEFAULT_LOCALE in SSR(no windown)", async() => {
        delete (global as unknown).window;
        delete (global as unknown).navigator;

        const mod = await import("@/core/i18n/locale");
        const { detectLocale, DEFAULT_LOCALE } = mod;
        
        expect(detectLocale()).toBe(DEFAULT_LOCALE);
    
    });

    it("detects exact en_us", async() => {
        (global as unknown).navigator = { language: "en-US"};
        expect (detectLocale()).toBe("en-US")

    });

    it("normalize short en -> en_US", async() => {
        (global as unknown).navigator = { language: "en"};
        expect (detectLocale()).toBe("en-US")

    });
    
      it("maps zh, zh-TW, zh-Hans -> zh-CN", async () => {
        (global as any).navigator = { language: "zh-TW" };
        expect(detectLocale()).toBe("zh-CN");

        vi.resetModules();
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        (global as any).navigator = { language: "zh-Hans" };
        expect(detectLocale()).toBe("zh-CN");

        vi.resetModules();
        (global as any).navigator = { language: "zh" };
        expect(detectLocale()).toBe("zh-CN");

        vi.resetModules();
        (global as any).navigator = { language: "ch-CN" };
        expect(detectLocale()).toBe("en-US");
      });
      
      it("fallback to DEFAULT_LOCALE", async () => {
        (global as any).navigator = { language: "ja" };
        expect(detectLocale()).toBe(DEFAULT_LOCALE);

      })
})