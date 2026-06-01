// src/proxy.ts - 语言检测与重定向
import { NextRequest, NextResponse } from 'next/server';
import { locales, defaultLocale, getLocaleFromHeaders } from '@/lib/i18n';  // ← 新增导入

const PUBLIC_FILE = /\.(.*)$/;

export default function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;
  
  if (PUBLIC_FILE.test(pathname)) return;
  if (pathname.startsWith('/api')) return;
  
  const pathnameHasLocale = locales.some(
    locale => pathname.startsWith(`/${locale}/`) || pathname === `/${locale}`
  );
  
  if (pathnameHasLocale) {
    const response = NextResponse.next();
    const locale = pathname.split('/')[1];
    response.cookies.set('locale', locale);
    return response;
  }
  
  // ← 这里是关键改动：检查浏览器语言，而不是写死 defaultLocale
  const detectedLocale = getLocaleFromHeaders(request.headers);
  const url = request.nextUrl.clone();
  url.pathname = `/${detectedLocale}${pathname}`;
  return NextResponse.redirect(url);
}

export const config = {
  matcher: ['/((?!_next|favicon.ico).*)'],
};
