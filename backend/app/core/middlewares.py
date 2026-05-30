
import uuid

from .setup_logging import setup_logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from typing import Any, Callable, Optional
import time
import asyncio
from fastapi.responses import JSONResponse
from starlette.requests import Request
import os
from dotenv import load_dotenv
load_dotenv()




logger = setup_logging(__name__)


try:
    from redis.asyncio import Redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    Redis = None
    logger.warning("resid no installed")





_QUIET_HTTP_PATHS = frozenset({
    "/",
    "/health",
    "/favicon.ico",
    "/openapi.json",
    "/docs",
    "/redoc",
})


def set_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# http response compress
def setup_gzip(app: FastAPI) -> None:
    app.add_middleware(
        middleware_class=GZipMiddleware,
        minimum_size=1000,
    )




def setup_logger(app: FastAPI) -> None:
    @app.middleware("http")
    async def log_requests(request : Request, call_next) -> Any:
        path = str(request.url.path or "")
        quiet: bool = path in _QUIET_HTTP_PATHS

        if not quiet:
            logger.info(f"{request.method} {path}")

        response = await call_next(request)

        if not quiet:
            logger.info(f"{response.status_code}")

        return response


def setup_id(app: FastAPI) -> None:
    @app.middleware("http")
    async def set_request_id(request: Request, call_next) -> Any:
        set_id = request.headers.get("X-Request-ID")
        if set_id is None:
            set_id = str(uuid.uuid4())
        request.state.request_id = set_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = set_id
        return response
    
def setup_monitor(app: FastAPI) -> None:
    @app.middleware("http")
    async def monitor(request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        end = time.time()
        elapsed = end - start
        if elapsed > 1: 
            logger.warning(
                f"请求处理时间:{request.url.path} {elapsed:.4f}s too long")
        else:
            logger.info(
            f"请求处理时间: {elapsed:.4f}s",
            extra={
                "path": request.url.path,
                "method": request.method,
                "elapsed_seconds": elapsed,
                "status_code": response.status_code
            }
        )
        return response

def setup_timeup(app: FastAPI) -> None:
    @app.middleware("http")
    async def timeup(request: Request, call_next):
        try:
            response = await asyncio.wait_for(call_next(request), timeout=30)
            return response
        except asyncio.TimeoutError:
            return JSONResponse(status_code=408, content={"detail": "Request timed out"})
        except Exception as e:
            return JSONResponse(status_code=500, content={"detail": str(e)})        


def setup_ratelimit(app:FastAPI) -> None:
    if not REDIS_AVAILABLE:
        app.add_middleware(
            RateLimitMiddleware,
            limits={
                "info": 100,
                "quant": 30,
                "default": 60
            }
        )
    else:
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        app.add_middleware(
            RedisRateLimitMiddleware,
            redis_url=redis_url,
            limits={
                "info": 100,
                "quant": 30,
                "default": 60
            }
        )

def setup_middlewares(app: FastAPI) -> None:
    # 按推荐顺序重新排列
    setup_ratelimit(app)    # 1. 限流
    setup_timeup(app)       # 2. 超时
    setup_monitor(app)      # 3. 监控
    setup_id(app)           # 4. 请求ID
    setup_logger(app)       # 5. 日志
    set_cors(app)          # 6. CORS
    setup_gzip(app)        # 7. GZip压缩


from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


class RedisRateLimitMiddleware(BaseHTTPMiddleware):

    def __init__(self, app, redis_url: str,  limits: dict):
        super().__init__(app)
        self.limits = limits
        self.redis_url = redis_url 
        self.redis = None  # 类型提示
        self.window = 60
    
    async def _get_redis(self):
        # TODO here get connected future do it again?
        if not REDIS_AVAILABLE:
            return None
        try:
            from app.core.redis_manager import redis_manager
            return redis_manager.client
        except ImportError:
            # 回退到私有连接
            if self.redis is None and Redis is not None:
                self.redis = Redis.from_url(self.redis_url, decode_responses=True)
            return self.redis
    
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        path = request.url.path

        # 确定限流策略
        if path.startswith("/api/v1/info"):
            limit = self.limits.get("info", 100)
        elif path.startswith("/api/v1/quant"):
            limit = self.limits.get("quant", 30)
        else:
            limit = self.limits.get("default", 60)

        # Redis 键格式：ratelimit:{ip}:{path}:{window_start}
        current_time = time.time()
        window_start = int(current_time // self.window) * self.window
        redis_key = f"ratelimit:{client_ip}:{path}:{window_start}"

        try:
            redis = await self._get_redis()
            if redis is None:
                return await call_next(request)

            # 使用 Redis INCR 原子操作
            count = await redis.incr(redis_key)

            if count == 1:
                # 首次请求，设置过期时间
                await redis.expire(redis_key, self.window)

            if count > limit:
                return JSONResponse(
                    status_code=429,
                    content={
                        "error": {
                            "code": "RATE_LIMIT_EXCEEDED",
                            "message": f"请求过于频繁，请在{self.window}秒后再试",
                            "limit": limit,
                            "window": self.window,
                            "current_count": count
                        }
                    }
                )

        except Exception as e:
            logger.error(f"Redis 限流错误: {e}")
            # Redis 出错时允许请求通过（降级处理）
            # 生产环境可以考虑记录告警或切换到备用限流策略
        
        return await call_next(request)
                            
"""
the following is not with redis only for development
# 使用方式：在 main.py 中
from app.core.middlewares import RateLimitMiddleware

app.add_middleware(
    RateLimitMiddleware,
    limits={
        "info": 100,
        "quant": 30,
        "default": 60
    }
)
"""

def setup_rate_limit(app: FastAPI):
    """函数式限流中间件"""
    
    limits = {
        "info": 100,    # 信息模块：每分钟100次
        "quant": 30,    # 量化模块：每分钟30次  
        "default": 60   # 默认：每分钟60次
    }
    
    # 状态存储
    request_counts = {}
    
    def _cleanup_old_records(current_time: float):
        """清理过期记录"""
        expired_keys = [
            key for key, (_, window_start) in request_counts.items()
            if current_time - window_start > 120
        ]
        for key in expired_keys:
            del request_counts[key]
    
    @app.middleware("http")
    async def rate_limit_middleware(request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        path = request.url.path
        
        # 确定限流策略
        if path.startswith("/api/v1/info"):
            limit = limits.get("info", 100)
            window = 60
        elif path.startswith("/api/v1/quant"):
            limit = limits.get("quant", 30)
            window = 60
        else:
            limit = limits.get("default", 60)
            window = 60
        
        # 检查限流
        key = f"{client_ip}:{path}"
        current_time = time.time()
        
        if key in request_counts:
            count, window_start = request_counts[key]
            
            if current_time - window_start > window:
                # 窗口过期，重置
                request_counts[key] = (1, current_time)
            elif count >= limit:
                # 超过限制
                return JSONResponse(
                    status_code=429,
                    content={
                        "error": {
                            "code": "RATE_LIMIT_EXCEEDED",
                            "message": f"请求过于频繁，请在{window}秒后再试",
                            "limit": limit,
                            "window": window
                        }
                    }
                )
            else:
                # 增加计数
                request_counts[key] = (count + 1, window_start)
        else:
            # 首次请求
            request_counts[key] = (1, current_time)
        
        # 清理过期记录
        _cleanup_old_records(current_time)
        
        return await call_next(request)



from starlette.middleware.base import BaseHTTPMiddleware


class RateLimitMiddleware(BaseHTTPMiddleware):
    """限流中间件（信息展示模块轻量级，量化交易模块严格）"""
    
    def __init__(self, app, limits: dict):
        super().__init__(app)
        self.limits = limits
        self.request_counts = {}  # 简单内存存储，生产环境用Redis
    
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        path = request.url.path
        
        # 确定限流策略
        if path.startswith("/api/v1/info"):
            # 信息展示模块：宽松限流
            limit = self.limits.get("info", 100)  # 每分钟100次
            window = 60  # 60秒窗口
        elif path.startswith("/api/v1/quant"):
            # 量化交易模块：严格限流
            limit = self.limits.get("quant", 30)  # 每分钟30次
            window = 60
        else:
            # 默认限流
            limit = self.limits.get("default", 60)
            window = 60
        
        # 检查限流
        key = f"{client_ip}:{path}"
        current_time = time.time()
        
        if key in self.request_counts:
            count, window_start = self.request_counts[key]
            
            if current_time - window_start > window:
                # 窗口过期，重置
                self.request_counts[key] = (1, current_time)
            elif count >= limit:
                # 超过限制
                return JSONResponse(
                    status_code=429,
                    content={
                        "error": {
                            "code": "RATE_LIMIT_EXCEEDED",
                            "message": f"请求过于频繁，请在{window}秒后再试",
                            "limit": limit,
                            "window": window
                        }
                    }
                )
            else:
                # 增加计数
                self.request_counts[key] = (count + 1, window_start)
        else:
            # 首次请求
            self.request_counts[key] = (1, current_time)
        
        # 清理过期记录（简单实现）
        self._cleanup_old_records(current_time)
        
        return await call_next(request)
    
    def _cleanup_old_records(self, current_time: float):
        """清理60秒前的记录"""
        expired_keys = [
            key for key, (_, window_start) in self.request_counts.items()
            if current_time - window_start > 120  # 2倍窗口时间
        ]
        for key in expired_keys:
            del self.request_counts[key]