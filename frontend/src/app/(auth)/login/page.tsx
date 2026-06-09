"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useTheme } from "next-themes";
import { useEffect, useState } from "react";

import { Button } from "@/components/ui/button";
import { FlickeringGrid } from "@/components/ui/flickering-grid";
import { Input } from "@/components/ui/input";
import { useAuth } from "@/core/auth/AuthProvider";
import { parseAuthError } from "@/core/auth/types";


function validateNextParam(next: string | null): string | null {
  if (!next) return null;

  if(!next.startsWith("/")) return null;

  if (
    next.startsWith("//") ||
    next.startsWith("http://") ||
    next.startsWith("https://")
  ) {
    return null;
  }

  if(next.includes(":") && !next.startsWith("/")) {
    return null;
  }

  return next;
}

export default function LoginPage() {

  const router = useRouter();
  const searchParams = useSearchParams();
  const { theme, resolvedTheme } = useTheme();
  const { isAuthenticated } = useAuth();


  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLogin, setIsLogin] = useState(true);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const nextParam = searchParams.get("next");
  const redirectPath = validateNextParam(nextParam) ?? "/workspace";

  const actualTheme = theme === "system" ? resolvedTheme : theme;

  useEffect(() => {
    if(isAuthenticated) {
      router.push(redirectPath);
    }
  }, [isAuthenticated, router, redirectPath]);


  useEffect(() => {
    let cancelled = false;

    void fetch("/api/v1/auth/setup-status")
      .then((r) => r.json())
      .then((data: { needs_setup?: boolean }) => {
        if (!cancelled && data.needs_setup) {
          router.push("/setup");
        }
      })
      .catch(() => {
        // Ignore errors; user stays on login page
      });

    return () => {
      cancelled = true;
    };
  }, [router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const endpoint = isLogin 
      ? "/api/v1/auth/login" : "/api/v1/auth/register";
      
      const body = isLogin 
        ? `username=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}` 
        : JSON.stringify({ email, password });
      
      const headers: HeadersInit = isLogin
        ? { "Content-Type": "application/x-www-form-urlencoded" } 
        : { "Content-Type": "application/json" };
      
      const res = await fetch(endpoint, {
        method: "POST",
        credentials: "include",
        headers,
        body,
      });
      
      if (!res.ok) {
        const data = await res.json();
        const authError = parseAuthError(data);
        setError(authError.message);
        return;
      }
      router.push(redirectPath);

    } catch (err) {
        setError("An error occurred while processing your request.");
    } finally {
        setLoading(false);
      }
    }
  return (
    <div className="bg-background relative flex min-h-screen items-center justify-center overflow-x-hidden overflow-y-auto">
      <FlickeringGrid
        className="absolute inset-0 z-0 mask-[url(/images/cc.svg)] mask-size-[100vw] mask-center mask-no-repeat md:mask-size-[72vh]"
        squareSize={4}
        gridGap={4}
        color={actualTheme === "dark" ? "white" : "black"}
        maxOpacity={0.3}
        flickerChance={0.25}
      />
      <div className="border-border/20 bg-background/5 w-full max-w-md space-y-6 rounded-3xl border p-8 backdrop-blur-sm">
        <div className="text-center">
          <h1 className="text-foreground font-serif text-3xl">A3 + Harness</h1>
          <p className="text-muted-foreground mt-2">
            {isLogin ? "Sign in to your account" : "Create a new account"}
          </p>
        </div>
        <form onSubmit={handleSubmit} className="space-y-6">
            <div className="flex flex-col space-y-1">
              <label htmlFor="email" className="text-sm font-medium text-foreground">
                Email
              </label>
              <Input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="bg-background/50"
                placeholder="name@example.com"
              />
            </div>
            <div className="flex flex-col space-y-1">
              <label htmlFor="password" className="text-sm font-medium">
                Password
              </label>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="•••••••"
                required
                minLength={isLogin ? 6 : 8}
              />
            </div>

            {error && <p className="text-sm text-red-500">{error}</p>}

          <Button type="submit" className="w-full"  disabled={loading}>
            {loading ? "pleasing wait..." : isLogin ? "Sign In" : "Create Account"}
          </Button>

        </form>
        <div className="text-center text-sm text-muted-foreground">
          {isLogin ? "Don't have an account?" : "Already have an account?"}{" "}
          <button
            type="button"
            className="text-blue-500 hover:underline"
            onClick={() => setIsLogin(!isLogin)}
          >
            {isLogin ? "Sign Up" : "Sign In"}
          </button>
        </div>

        <div className="text-center text-sm text-muted-foreground mt-4">
          <Link href="/" className="text-blue-500 hover:underline">
            Back to Home
          </Link>

        </div>
      </div>  
    </div>
    );
}