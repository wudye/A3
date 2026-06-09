import {z} from "zod";

export const userSchema = z.object({
    id: z.string(),
    email: z.string().email(),
    system_role: z.enum(["admin", "user"]),
    needs_setup: z.boolean().optional().default(false),

})

export type User = z.infer<typeof userSchema>;


export type AuthResult =
  | { tag: "authenticated"; user: User }
  | { tag: "needs_setup"; user: User }
  | { tag: "system_setup_required" }
  | { tag: "unauthenticated" }
  | { tag: "gateway_unavailable" }
  | { tag: "config_error"; message: string };


export function assertNever(x: never): never {
  throw new Error(`Unexpected auth result: ${JSON.stringify(x)}`);
}
export function buildLoginUrl(returnPath: string): string {
  return `/login?next=${encodeURIComponent(returnPath)}`;
}


const AUTH_ERROR_CODES = [
  "invalid_credentials",
  "token_expired",
  "token_invalid",
  "user_not_found",
  "email_already_exists",
  "provider_not_found",
  "not_authenticated",
  "system_already_initialized",
] as const;


export type AuthErrorCode = (typeof AUTH_ERROR_CODES)[number];

export interface AuthErrorResponse {
  code: AuthErrorCode;
  message: string;
}


const AuthErrorSchema = z.object({
  code: z.enum(AUTH_ERROR_CODES),
  message: z.string(),
});



const ErrorDetailSchema = z.object({
  msg: z.string(),
  type: z.enum(["value_error"]),
  loc: z.array(z.string()),
});


export function parseAuthError(data: unknown): AuthErrorResponse {
    const parsed =  AuthErrorSchema.safeParse(data);
    if (parsed.success) {
        return parsed.data;
    }

    if(typeof data === "object" && data !== null && "detail" in data) {
        const detail = (data as Record<string, unknown>).detail;
        const nested = AuthErrorSchema.safeParse(detail);
        if (nested.success) {
            return nested.data;
        }
        if (typeof detail === "string") {
            return {
                code: "invalid_credentials",
                message: detail,
            }
        } else if (Array.isArray(detail)) {
            const errorDetails = detail[0];
            if (typeof errorDetails === "object" && errorDetails !== null) {
                const errorParsed = ErrorDetailSchema.safeParse(errorDetails);
                if (errorParsed.success) {
                    return {
                        code: "invalid_credentials",
                        message: errorParsed.data.msg,
                    }
                }
            }
        } else if (typeof detail === "object" && detail !== null) {
            const errorParsed = ErrorDetailSchema.safeParse(detail);
            if (errorParsed.success) {
                return {
                    code: "invalid_credentials",
                    message: errorParsed.data.msg,
                }
            }
        }
    }
    return {
        code: "invalid_credentials",
        message:  "Authentication failed"
    }
}