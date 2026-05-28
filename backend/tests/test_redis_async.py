import asyncio

async def test_redis_async():
    try:
        from redis.asyncio import Redis
        print("✅ redis.asyncio.Redis 导入成功")
        
        # 测试异步方法
        r = Redis.from_url("redis://localhost:6379/0", decode_responses=True)
        print("✅ Redis 客户端创建成功")
        
        # 检查 incr 方法
        import inspect
        is_async = inspect.iscoroutinefunction(r.incr)
        print(f"✅ incr 是异步方法: {is_async}")
        
        return True
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_redis_async())
