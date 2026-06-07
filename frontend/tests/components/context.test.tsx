import React from "react";
import { render, fireEvent, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { I18nProvider, useI18nContext } from "@/core/i18n/context";
import { Locale } from "@/core/i18n/locale";


function ShowLocale() {
    const { locale, setLocale } = useI18nContext();
    return <div data-testid="locale">{locale}</div>;
}

function ChangeLocaleButton() {
    const { setLocale } = useI18nContext();
    return <button onClick={() => setLocale("fr" as Locale)}>Change Locale</button>;
}

describe("I18nContext", () => {
    it("throws error when useI18nContext is used outside of I18nProvider", () => {
        function TestComp() {
            useI18nContext();
            return null;
        }
        
        expect(() => render(<TestComp />)).toThrow("useI18nContext must be used within an I18nProvider");
    });

    it("provides locale and setLocale to children", () => {
        render(
            <I18nProvider initialLocale={"en" as Locale}>
                <ShowLocale />
                <ChangeLocaleButton />
            </I18nProvider>
        );
        expect(screen.getByTestId("locale").textContent).toBe("en");

        fireEvent.click(screen.getByText("Change Locale"));
        expect(screen.getByTestId("locale").textContent).toBe("fr");
        expect(document.cookie).toContain("locale=fr");

    });
});
