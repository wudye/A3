import asyncio
import aiohttp
import time

async def test_rate_limit():
    url = "http://localhost:8080/api/v1/info"  # 假设有这个端点
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(110):  # 超过100次限制
            tasks.append(session.get(url))
        
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        success = 0
        rate_limited = 0
        for i, resp in enumerate(iterable=responses):
            if isinstance(resp, Exception):
                print(f"请求 {i} 异常: {resp}")
            elif resp.status == 200:
                success += 1
            elif resp.status == 429:
                rate_limited += 1
                if rate_limited == 1:  # 只打印第一个限流响应
                    data = await resp.json()
                    print(f"限流响应: {data}")
            else:
                print(f"请求 {i} 状态码: {resp.status}")
        
        print(f"成功: {success}, 被限流: {rate_limited}")

if __name__ == "__main__":
    asyncio.run(test_rate_limit())
