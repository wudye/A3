import { describe, it, expect, vi, beforeEach } from "vitest";
import { cookies } from "next/headers"; 


vi.mock("@/core/static-mode", () => ({
    isStaticWebsiteOnly: vi.fn(),
}));

vi.mock("next/headers", () => ({
    cookies: vi.fn()
}));

vi.mock("@/core/auth/gateway-config", () => ({
    getGatewayConfig: vi.fn(),
}));

import { getServerSideUser } from "@/core/auth/server";
import { getGatewayConfig } from "@/core/auth/gateway-config";
import { isStaticWebsiteOnly } from "@/core/static-mode";

async function mockCookies(token: string | null) {

    vi.mocked(cookies).mockResolvedValue({
        get: vi.fn((name: string) => {
            return name === "access_token" && token ? { value: token } : undefined;
        }),
    } as any);
}


const mockGatewayUrl = "http://127.0.0.1:8001";
beforeEach(async () => {
    vi.clearAllMocks();
    vi.restoreAllMocks();
    vi.stubGlobal("fetch", vi.fn());

    vi.mocked(cookies).mockResolvedValue({
        get: vi.fn().mockReturnValue(undefined),
    } as any);
    vi.mocked(
        (await import("@/core/auth/gateway-config")).getGatewayConfig
    ).mockReturnValue({
        internalGatewayUrl: mockGatewayUrl,
        trustedOrigins: ["http://localhost:3000"],
    });
});


describe("getServerSideUser", () => {
    it("returns authenticated user when static website mode is enabled", async () => {
        vi.mocked(isStaticWebsiteOnly).mockReturnValue(true);
        const result = await getServerSideUser();
        expect(result.tag).toBe("authenticated");
        if (result.tag === "authenticated") {
            expect(result.user.id).toBe("static-website-user");
            expect(result.user.email).toBe("static@example.local");
            expect(result.user.name).toBe("static-user");
            expect(result.user.system_role).toBe("admin");
        }
        expect(global.fetch).not.toHaveBeenCalled();
    });

    it("returns fake E2E admin when DEER_FLOW_AUTH_DISABLED=1", async () => {
        vi.mocked(isStaticWebsiteOnly).mockReturnValue(false);
        process.env.DEER_FLOW_AUTH_DISABLED = "1";
        const result = await getServerSideUser();

        expect(result.tag).toBe("authenticated");
        if (result.tag === "authenticated") {
        expect(result.user.id).toBe("e2e-user");
        expect(result.user.email).toBe("e2e@test.local");
        expect(result.user.name).toBe("E2E Test User");
        expect(result.user.system_role).toBe("admin");
        }

        delete process.env.DEER_FLOW_AUTH_DISABLED;
    });

    it("returns config_error when gateway URL is broken", async () => {
        vi.mocked(isStaticWebsiteOnly).mockReturnValue(false);
        vi.mocked(getGatewayConfig).mockImplementation(() => {
            throw new Error("DEER_FLOW_INTERNAL_GATEWAY_BASE_URL not set");
        });
        const result = await getServerSideUser();
        expect(result.tag).toBe("config_error");
        if (result.tag === "config_error") {
            expect(result.message).toBe("Error: DEER_FLOW_INTERNAL_GATEWAY_BASE_URL not set");
        }
    });

});


describe("when NO session cookie exists", () => {
    beforeEach(async () => {
        vi.mocked(isStaticWebsiteOnly).mockReturnValue(false);
        await mockCookies(null);
    });

    it("returns system_setup_required if backend says needs_setup=true", async () => {
    const mockFetch = vi.fn().mockImplementation((url: string, init?: RequestInit) => {
        if (url.includes("/auth/setup-status")) {
            return Promise.resolve(new Response(JSON.stringify({ needs_setup: true }), { status: 200 }));
        }
        return Promise.resolve(new Response(null, { status: 404 }));
    });
    vi.stubGlobal("fetch", mockFetch);
    const result = await getServerSideUser();
          expect(result.tag).toBe("system_setup_required");
      // Should have called setup-status endpoint
    expect(mockFetch).toHaveBeenCalledWith(
        `${mockGatewayUrl}/api/v1/auth/setup-status`,
        expect.objectContaining({ cache: "no-store" })
      );
    });

    it("returns unauthenticated if backend says needs_setup != true", async () => {
        const mockFetch = vi.fn().mockImplementation((url:string) => {
            if (url.includes("/auth/setup-status")) {
                return Promise.resolve(new Response(JSON.stringify({ needs_setup: false }), { status: 200 }));
            }
            return Promise.resolve(new Response(null, { status: 404 }));
        });

        vi.stubGlobal("fetch", mockFetch);
        const result = await getServerSideUser();
        expect(result.tag).toBe("unauthenticated");
        
        // Should have called setup-status endpoint
        expect(mockFetch).toHaveBeenCalledWith(
            `${mockGatewayUrl}/api/v1/auth/setup-status`,
            expect.objectContaining({ cache: "no-store" })
        );
    });
    it("returns unauthenticated if setup-status request fails", async () => {
        const mockFetch = vi.fn().mockRejectedValue(new Error("Network error"));

        vi.stubGlobal("fetch", mockFetch);
        const result = await getServerSideUser();
        expect(result.tag).toBe("unauthenticated");
    });
    
    it("returns unauthenticated if setup-status times out", async () => {
      // 1. 模拟一个永远挂起的 fetch，除非接收到 abort 信号
      const mockFetch = vi.fn().mockImplementation((_url: string, init?: RequestInit) => {
        return new Promise((_, reject) => {
          if (init?.signal) {
            init.signal.addEventListener('abort', () => {
              reject(new DOMException("Aborted", "AbortError"));
            });
          }
        });
      });
      
      vi.stubGlobal("fetch", mockFetch);
      vi.useFakeTimers();

      // 2. 开始执行函数（不要在这里 await，因为它现在变异步了）
      const promise = getServerSideUser();

      // 3. 关键：推进时间，触发代码内部的 5s 超时逻辑
      // 使用 Async 版本可以确保 Promise 链在时间推进后能正确结算
      await vi.advanceTimersByTimeAsync(6000); 

      const result = await promise;

      expect(result.tag).toBe("unauthenticated");
      
      // 4. 清理环境
      vi.useRealTimers();
    });


});

describe("when session cookie EXISTS", () => {
    const testToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test-payload";
    beforeEach(async () => {
        vi.mocked(isStaticWebsiteOnly).mockReturnValue(false);
        await mockCookies(testToken);
    });

    it("returns authenticated with valid user data (needs_setup=false)", async () => {
      const mockUser = {
        id: "user-123",
        email: "test@example.com",
        name: "Test User",
        system_role: "user",
        needs_setup: false,
      };
     const mockFetch = vi.fn().mockImplementation((url: string) => {
        if (url.includes("/auth/me")) {
            return Promise.resolve(new Response(JSON.stringify(mockUser), { status: 200 }));
        }
        return Promise.resolve(new Response(null, { status: 404 }));
    });
    vi.stubGlobal("fetch", mockFetch);
    const result = await getServerSideUser();
    expect(result.tag).toBe("authenticated");
    if (result.tag === "authenticated") {
        expect(result.user.id).toBe(mockUser.id);
        expect(result.user.email).toBe(mockUser.email);
        expect(result.user.name).toBe(mockUser.name);
        expect(result.user.system_role).toBe(mockUser.system_role);
        expect(result.user.needs_setup).toBe(mockUser.needs_setup);
    }   
    expect(mockFetch).toHaveBeenCalledWith(
        `${mockGatewayUrl}/api/v1/auth/me`,
        expect.objectContaining({
            headers: { Cookie: `access_token=${testToken}` },
            cache: "no-store",
        })
    );
    });

    it("returns needs_setup when user has needs_setup=true", async () => {
      const mockUser = {
        id: "user-456",
        email: "new@example.com",
        name: "New User",
        system_role: "admin",
        needs_setup: true,
      };

      const mockFetch = vi.fn().mockImplementation((url: string) => {
        if (url.includes("/auth/me")) {
          return Promise.resolve(
            new Response(JSON.stringify(mockUser), { status: 200 })
          );
        }
        return Promise.resolve(new Response(null, { status: 404 }));
      });
      vi.stubGlobal("fetch", mockFetch);

      const result = await getServerSideUser();

      expect(result.tag).toBe("needs_setup");
      if (result.tag === "needs_setup") {
        expect(result.user.id).toBe("user-456");
        expect(result.user.needs_setup).toBe(true);
      }
    });

    it("returns unauthenticated on 401 or 403", async () => {
      const mockFetch = vi.fn().mockImplementation((url: string) => {
        if (url.includes("/auth/me")) {
          return Promise.resolve(new Response(null, { status: 401 }));
        }
        return Promise.resolve(new Response(null, { status: 404 }));
      });
      vi.stubGlobal("fetch", mockFetch);

      const result = await getServerSideUser();
      expect(result.tag).toBe("unauthenticated");

      // Also test 403
      mockFetch.mockClear().mockImplementation((url: string) => {
        if (url.includes("/auth/me")) {
          return Promise.resolve(new Response(null, { status: 403 }));
        }
        return Promise.resolve(new Response(null, { status: 404 }));
      });

      const result2 = await getServerSideUser();
      expect(result2.tag).toBe("unauthenticated");
    });

    it("returns gateway_unavailable on non-200/401/403 status", async () => {
      const mockFetch = vi.fn().mockImplementation((url: string) => {
        if (url.includes("/auth/me")) {
          return Promise.resolve(new Response(null, { status: 500 }));
        }
        return Promise.resolve(new Response(null, { status: 404 }));
      });
      vi.stubGlobal("fetch", mockFetch);

      const result = await getServerSideUser();
      expect(result.tag).toBe("gateway_unavailable");

      // Also test 502
      mockFetch.mockClear().mockImplementation((url: string) => {
        if (url.includes("/auth/me")) {
          return Promise.resolve(new Response(null, { status: 502 }));
        }
        return Promise.resolve(new Response(null, { status: 404 }));
      });

      const result2 = await getServerSideUser();
      expect(result2.tag).toBe("gateway_unavailable");
    });

    it("returns gateway_unavailable when /auth/me returns malformed JSON", async () => {
      const mockFetch = vi.fn().mockImplementation((url: string) => {
        if (url.includes("/auth/me")) {
          // Missing required fields like email (not valid email format)
          return Promise.resolve(
            new Response(JSON.stringify({ id: "bad", name: "NoEmail" }), { status: 200 })
          );
        }
        return Promise.resolve(new Response(null, { status: 404 }));
      });
      vi.stubGlobal("fetch", mockFetch);

      // Spy on console.error to verify it logs
      const errorSpy = vi.spyOn(console, "error").mockImplementation(() => {});

      const result = await getServerSideUser();
      expect(result.tag).toBe("gateway_unavailable");
      expect(errorSpy).toHaveBeenCalledWith(
        expect.stringContaining("[SSR auth] Malformed"),
        expect.anything()
      );

      errorSpy.mockRestore();
    });


    it("returns gateway_unavailable when /auth/me network fails", async () => {
      const mockFetch = vi.fn().mockRejectedValue(new Error("ECONNREFUSED"));
      vi.stubGlobal("fetch", mockFetch);

      const errorSpy = vi.spyOn(console, "error").mockImplementation(() => {});
      const result = await getServerSideUser();

      expect(result.tag).toBe("gateway_unavailable");
      expect(errorSpy).toHaveBeenCalledWith(
        expect.stringContaining("[SSR auth] Failed to reach gateway"),
        expect.any(Error)
      );

      errorSpy.mockRestore();
    });

    it("sends correct Authorization/Cookie header to /auth/me", async () => {
      const specialToken = "my-special-jwt-token-xyz";
      await mockCookies(specialToken);

      const mockFetch = vi.fn().mockResolvedValue(
        new Response(
          JSON.stringify({
            id: "u1",
            email: "a@b.com",
            name: "A",
            system_role: "user",
            needs_setup: false,
          }),
          { status: 200 }
        )
      );
      vi.stubGlobal("fetch", mockFetch);

      await getServerSideUser();

      expect(mockFetch).toHaveBeenCalledWith(
        expect.stringContaining("/auth/me"),
        expect.objectContaining({
          headers: { Cookie: `access_token=${specialToken}` },
          cache: "no-store",
        })
      );
    });
});