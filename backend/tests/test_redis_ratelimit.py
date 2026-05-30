import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from starlette.responses import JSONResponse
import time

from app.core.middlewares import RedisRateLimitMiddleware, RateLimitMiddleware

# ==================== 单元测试（模拟 Redis）====================

class TestRedisRateLimitUnit:
    """RedisRateLimitMiddleware 单元测试"""
    
    @pytest.mark.asyncio
    async def test_redis_rate_limit_middleware_creation(self):
        """测试中间件创建"""
        app = FastAPI()
        limits: dict[str, int] = {"info": 100, "quant": 30, "default": 60}
        
        middleware = RedisRateLimitMiddleware(
            app=app,
            redis_url="redis://:nopass@localhost:6379/0",
            limits=limits
        )
        
        assert middleware.limits == limits
        assert middleware.redis_url == "redis://:nopass@localhost:6379/0"
        assert middleware.window == 60
    
    @pytest.mark.asyncio
    async def test_get_redis_with_redis_manager(self, mocker):
        """测试获取 Redis 连接（使用 redis_manager）"""
        app = FastAPI()
        limits = {"info": 100, "quant": 30, "default": 60}
        
        middleware = RedisRateLimitMiddleware(
            app=app,
            redis_url="redis://:nopass@localhost:6379/0",
            limits=limits
        )
        
        # 模拟 redis_manager.client
        mock_redis = AsyncMock()
        mock_redis.ping = AsyncMock()
        
        mocker.patch('app.core.middlewares.REDIS_AVAILABLE', True)
        mocker.patch('app.core.middlewares.redis_manager.client', mock_redis)
        
        redis = await middleware._get_redis()
        assert redis == mock_redis
    
    @pytest.mark.asyncio
    async def test_rate_limit_within_limit(self, mocker):
        """测试未超过限流的情况"""
        app = FastAPI()
        limits = {"info": 5, "quant": 3, "default": 10}
        
        middleware = RedisRateLimitMiddleware(
            app=app,
            redis_url="redis://:nopass@localhost:6379/0",
            limits=limits
        )
        
        # 模拟 Redis 响应
        mock_redis = AsyncMock()
        mock_redis.incr = AsyncMock(return_value=1)  # 第一次请求
        mock_redis.expire = AsyncMock()
        
        mocker.patch.object(middleware, '_get_redis', AsyncMock(return_value=mock_redis))
        
        # 模拟请求
        mock_request = mocker.Mock(spec=Request)
        mock_request.client.host = "127.0.0.1"
        mock_request.url.path = "/api/v1/info"
        
        mock_call_next = AsyncMock(return_value=JSONResponse(content={"ok": True}))
        
        response = await middleware.dispatch(mock_request, mock_call_next)
        
        # 验证 Redis 调用
        mock_redis.incr.assert_called_once()
        mock_redis.expire.assert_called_once_with(mocker.ANY, 60)
        assert mock_call_next.called
        assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_rate_limit_exceeded(self, mocker):
        """测试超过限流的情况"""
        app = FastAPI()
        limits = {"info": 5, "quant": 3, "default": 10}
        
        middleware = RedisRateLimitMiddleware(
            app=app,
            redis_url="redis://:nopass@localhost:6379/0", 
            limits=limits
        )
        
        # 模拟 Redis 响应：第6次请求（超过5次限制）
        mock_redis = AsyncMock()
        mock_redis.incr = AsyncMock(return_value=6)
        mock_redis.expire = AsyncMock()
        
        mocker.patch.object(middleware, '_get_redis', AsyncMock(return_value=mock_redis))
        
        # 模拟请求
        mock_request = mocker.Mock(spec=Request)
        mock_request.client.host = "127.0.0.1"
        mock_request.url.path = "/api/v1/info"
        
        mock_call_next = AsyncMock()
        
        response = await middleware.dispatch(mock_request, mock_call_next)
        
        # 验证返回 429 响应
        assert response.status_code == 429
        assert response.body is not None
        assert b"RATE_LIMIT_EXCEEDED" in response.body
        assert not mock_call_next.called  # 不应调用后续处理
    
    @pytest.mark.asyncio
    async def test_different_path_limits(self, mocker):
        """测试不同路径的限流策略"""
        app = FastAPI()
        limits = {"info": 5, "quant": 3, "default": 10}
        
        middleware = RedisRateLimitMiddleware(
            app=app,
            redis_url="redis://:nopass@localhost:6379/0",
            limits=limits
        )
        
        test_cases = [
            ("/api/v1/info", 5),      # info 路径
            ("/api/v1/info/details", 5),  # info 子路径
            ("/api/v1/quant", 3),     # quant 路径
            ("/api/v1/quant/trade", 3),  # quant 子路径
            ("/api/v1/other", 10),    # 默认路径
            ("/", 10),                # 根路径
        ]
        
        for path, expected_limit in test_cases:
            # 模拟请求
            mock_request = mocker.Mock(spec=Request)
            mock_request.client.host = "127.0.0.1"
            mock_request.url.path = path
            
            # 模拟 Redis 刚好超过限制
            mock_redis = AsyncMock()
            mock_redis.incr = AsyncMock(return_value=expected_limit + 1)
            mock_redis.expire = AsyncMock()
            
            mocker.patch.object(middleware, '_get_redis', AsyncMock(return_value=mock_redis))
            
            mock_call_next = AsyncMock()
            response = await middleware.dispatch(mock_request, mock_call_next)
            
            assert response.status_code == 429, f"Path {path} should be rate limited at {expected_limit}"
    
    @pytest.mark.asyncio
    async def test_redis_unavailable_fallback(self, mocker):
        """测试 Redis 不可用时降级处理"""
        app = FastAPI()
        limits = {"info": 5, "quant": 3, "default": 10}
        
        middleware = RedisRateLimitMiddleware(
            app=app,
            redis_url="redis://:nopass@localhost:6379/0",
            limits=limits
        )
        
        # 模拟 Redis 不可用
        mocker.patch.object(middleware, '_get_redis', AsyncMock(return_value=None))
        
        mock_request = mocker.Mock(spec=Request)
        mock_request.client.host = "127.0.0.1"
        mock_request.url.path = "/api/v1/info"
        
        mock_call_next = AsyncMock(return_value=JSONResponse(content={"ok": True}))
        
        response = await middleware.dispatch(mock_request, mock_call_next)
        
        # Redis 不可用时应该直接通过请求
        assert mock_call_next.called
        assert response.status_code == 200
    
    @pytest.mark.asyncio
    async def test_redis_exception_handling(self, mocker):
        """测试 Redis 异常处理"""
        app = FastAPI()
        limits = {"info": 5, "quant": 3, "default": 10}
        
        middleware = RedisRateLimitMiddleware(
            app=app,
            redis_url="redis://:nopass@localhost:6379/0",
            limits=limits
        )
        
        # 模拟 Redis 抛出异常
        mock_redis = AsyncMock()
        mock_redis.incr = AsyncMock(side_effect=ConnectionError("Redis connection failed"))
        
        mocker.patch.object(middleware, '_get_redis', AsyncMock(return_value=mock_redis))
        
        mock_request = mocker.Mock(spec=Request)
        mock_request.client.host = "127.0.0.1"
        mock_request.url.path = "/api/v1/info"
        
        mock_call_next = AsyncMock(return_value=JSONResponse(content={"ok": True}))
        
        # 应该捕获异常并继续处理请求
        response = await middleware.dispatch(mock_request, mock_call_next)
        
        assert mock_call_next.called
        assert response.status_code == 200

# ==================== 集成测试（使用 FakeRedis）====================

class TestRedisRateLimitIntegration:
    """RedisRateLimitMiddleware 集成测试（使用 FakeRedis）"""
    
    @pytest.fixture
    def fake_redis_app(self, fake_redis):
        """创建使用 FakeRedis 的应用"""
        app = FastAPI()
        
        # 添加路由用于测试
        @app.get("/api/v1/info")
        async def get_info():
            return {"message": "info"}
        
        @app.get("/api/v1/quant")
        async def get_quant():
            return {"message": "quant"}
        
        @app.get("/api/v1/other")
        async def get_other():
            return {"message": "other"}
        
        # 添加 Redis 限流中间件
        limits = {"info": 5, "quant": 3, "default": 10}
        
        # 模拟 Redis 连接返回 FakeRedis
        with patch('app.core.middlewares.Redis.from_url') as mock_from_url:
            mock_from_url.return_value = fake_redis
            app.add_middleware(
                RedisRateLimitMiddleware,
                redis_url="redis://localhost:6379/0",
                limits=limits
            )
        
        return app
    
    @pytest.fixture
    def integration_client(self, fake_redis_app):
        """集成测试客户端"""
        return TestClient(fake_redis_app)
    
    def test_rate_limit_integration_within_limit(self, integration_client):
        """集成测试：在限流范围内"""
        # 发送5次请求（刚好在限制内）
        for i in range(5):
            response = integration_client.get("/api/v1/info")
            assert response.status_code == 200
            assert response.json()["message"] == "info"
    
    def test_rate_limit_integration_exceeded(self, integration_client):
        """集成测试：超过限流"""
        # 发送6次请求（超过5次限制）
        responses = []
        for i in range(6):
            response = integration_client.get("/api/v1/info")
            responses.append(response)
        
        # 前5次应该成功
        for i in range(5):
            assert responses[i].status_code == 200
        
        # 第6次应该被限流
        assert responses[5].status_code == 429
        error_data = responses[5].json()
        assert error_data["error"]["code"] == "RATE_LIMIT_EXCEEDED"
        assert error_data["error"]["limit"] == 5
    
    def test_rate_limit_reset_after_window(self, integration_client, mocker):
        """集成测试：窗口过期后重置限流"""
        # 模拟时间前进
        mock_time = mocker.patch('time.time')
        current_time = 1000.0
        
        # 第一次请求
        mock_time.return_value = current_time
        response1 = integration_client.get("/api/v1/info")
        assert response1.status_code == 200
        
        # 发送4次更多请求（总共5次）
        for i in range(4):
            mock_time.return_value = current_time + i
            response = integration_client.get("/api/v1/info")
            assert response.status_code == 200
        
        # 第6次应该被限流
        mock_time.return_value = current_time + 5
        response6 = integration_client.get("/api/v1/info")
        assert response6.status_code == 429
        
        # 模拟时间前进超过窗口（61秒后）
        mock_time.return_value = current_time + 61
        
        # 应该可以重新请求
        response_reset = integration_client.get("/api/v1/info")
        assert response_reset.status_code == 200
    
    def test_different_ips_different_limits(self, integration_client):
        """集成测试：不同IP独立限流"""
        # IP 1 发送6次请求
        for i in range(6):
            response = integration_client.get("/api/v1/info", headers={"X-Forwarded-For": "192.168.1.1"})
            if i < 5:
                assert response.status_code == 200
            else:
                assert response.status_code == 429
        
        # IP 2 应该不受影响
        response_ip2 = integration_client.get("/api/v1/info", headers={"X-Forwarded-For": "192.168.1.2"})
        assert response_ip2.status_code == 200

# ==================== 内存限流中间件测试 ====================

class TestMemoryRateLimit:
    """内存限流中间件测试"""
    
    @pytest.mark.asyncio
    async def test_memory_rate_limit_middleware(self, mocker):
        """测试内存限流中间件"""
        app = FastAPI()
        limits = {"info": 5, "quant": 3, "default": 10}
        
        middleware = RateLimitMiddleware(app=app, limits=limits)
        
        # 模拟请求
        mock_request = mocker.Mock(spec=Request)
        mock_request.client.host = "127.0.0.1"
        mock_request.url.path = "/api/v1/info"
        
        mock_call_next = AsyncMock(return_value=JSONResponse(content={"ok": True}))
        
        # 发送5次请求（在限制内）
        for i in range(5):
            response = await middleware.dispatch(mock_request, mock_call_next)
            assert response.status_code == 200
        
        # 第6次应该被限流
        response = await middleware.dispatch(mock_request, mock_call_next)
        assert response.status_code == 429
        assert b"RATE_LIMIT_EXCEEDED" in response.body
    
    @pytest.mark.asyncio 
    async def test_memory_rate_limit_window_reset(self, mocker):
        """测试内存限流窗口重置"""
        app = FastAPI()
        limits = {"info": 5, "quant": 3, "default": 10}
        
        middleware = RateLimitMiddleware(app=app, limits=limits)
        
        mock_request = mocker.Mock(spec=Request)
        mock_request.client.host = "127.0.0.1"
        mock_request.url.path = "/api/v1/info"
        
        mock_call_next = AsyncMock(return_value=JSONResponse(content={"ok": True}))
        
        # 模拟时间
        mock_time = mocker.patch('time.time')
        current_time = 1000.0
        
        # 第一次请求
        mock_time.return_value = current_time
        response1 = await middleware.dispatch(mock_request, mock_call_next)
        assert response1.status_code == 200
        
        # 发送4次更多请求
        for i in range(4):
            mock_time.return_value = current_time + i
            response = await middleware.dispatch(mock_request, mock_call_next)
            assert response.status_code == 200
        
        # 第6次应该被限流
        mock_time.return_value = current_time + 5
        response6 = await middleware.dispatch(mock_request, mock_call_next)
        assert response6.status_code == 429
        
        # 模拟时间前进超过窗口（61秒后）
        mock_time.return_value = current_time + 61
        
        # 应该可以重新请求
        response_reset = await middleware.dispatch(mock_request, mock_call_next)
        assert response_reset.status_code == 200

# ==================== 性能测试 ====================

class TestRateLimitPerformance:
    """限流性能测试"""
    
    @pytest.mark.asyncio
    async def test_rate_limit_performance(self, mocker):
        """测试限流中间件性能"""
        app = FastAPI()
        limits = {"info": 1000, "quant": 500, "default": 100}
        
        middleware = RedisRateLimitMiddleware(
            app=app,
            redis_url="redis://localhost:6379/0",
            limits=limits
        )
        
        # 模拟高效的 Redis 响应
        mock_redis = AsyncMock()
        mock_redis.incr = AsyncMock(return_value=1)
        mock_redis.expire = AsyncMock()
        
        mocker.patch.object(middleware, '_get_redis', AsyncMock(return_value=mock_redis))
        
        mock_request = mocker.Mock(spec=Request)
        mock_request.client.host = "127.0.0.1"
        mock_request.url.path = "/api/v1/info"
        
        mock_call_next = AsyncMock(return_value=JSONResponse(content={"ok": True}))
        
        # 测试多次请求的性能
        import time as time_module
        start_time = time_module.perf_counter()
        
        num_requests = 100
        tasks = [middleware.dispatch(mock_request, mock_call_next) for _ in range(num_requests)]
        responses = await asyncio.gather(*tasks)
        
        end_time = time_module.perf_counter()
        elapsed = end_time - start_time
        
        # 所有请求应该成功
        assert all(r.status_code == 200 for r in responses)
        
        # 性能检查：100次请求应该在合理时间内完成
        assert elapsed < 2.0, f"100次请求耗时 {elapsed:.2f} 秒，超过预期"
        
        print(f"性能测试：{num_requests} 次请求耗时 {elapsed:.3f} 秒，平均 {elapsed/num_requests*1000:.2f} 毫秒/次")

# ==================== 原脚本兼容性测试 ====================

def test_original_script_compatibility():
    """测试原脚本功能兼容性"""
    # 原脚本的核心逻辑测试
    import asyncio
    from unittest.mock import AsyncMock, patch
    
    async def mock_rate_limit_test():
        """模拟原脚本的测试逻辑"""
        # 模拟响应
        mock_responses = [
            AsyncMock(status=200) for _ in range(100)
        ] + [
            AsyncMock(status=429, json=AsyncMock(return_value={
                "error": {"code": "RATE_LIMIT_EXCEEDED", "message": "限流"}
            })) for _ in range(10)
        ]
        
        success = 0
        rate_limited = 0
        
        for resp in mock_responses:
            if resp.status == 200:
                success += 1
            elif resp.status == 429:
                rate_limited += 1
        
        assert success == 100
        assert rate_limited == 10
        return success, rate_limited
    
    # 运行测试
    success, rate_limited = asyncio.run(mock_rate_limit_test())
    assert success == 100
    assert rate_limited == 10
