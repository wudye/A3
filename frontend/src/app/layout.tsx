import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from "@/components/theme-provider"
import { detectLocaleServer } from "@/i18n/server";
import { I18nProvider } from "@/i18n/context";


const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "MY AI WORLD",
  description: "earn money, predict future, talk deeply",
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const locale = await detectLocaleServer();
  return (
    <html
      lang={locale}
      suppressHydrationWarning  
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">
        <ThemeProvider attribute="class">
            <I18nProvider initialLocal={locale}>
              {children}  

            </I18nProvider>
          </ThemeProvider>
        </body>
    </html>
  );
}
