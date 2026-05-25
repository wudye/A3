import { describe, it, expect } from "vitest";
import { temp } from "@/utils/temp";

// 测试套件
describe("temp 函数", () => {
  // 单个测试用例
  it("应该返回字符串 'temp'", () => {
    const result = temp();
    expect(result).toBe("temp");
  });
});
