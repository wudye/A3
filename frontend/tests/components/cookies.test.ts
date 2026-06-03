import { getLocaleFromCookie, setLocaleInCookie } from "@/core/i18n/cookies";
import {describe,beforeEach ,it, expect } from "vitest";


describe("cookies test case",() => {
    beforeEach(() => {
        document.cookie = "";
    });

    it("returns null when no local cookie", () => {
        document.cookie = "";
        expect(getLocaleFromCookie()).toBeNull();
    
    });

    it("parse ande decode cookie", () => {
        document.cookie = "locale=" + encodeURIComponent("en-US");
        expect(getLocaleFromCookie()).toBe("en-US");
    
    })
    it("setlocaleInCookie writes encoded cookie", () => {
        document.cookie = "";
        setLocaleInCookie("zh_CN")
        expect(document.cookie).toContain("locale=" + encodeURIComponent("zh_CN"));

    })
} )