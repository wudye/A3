

from contextlib import asynccontextmanager
from http.client import TEMPORARY_REDIRECT
from typing import Optional
from redis.asyncio import Redis
import os
from dotenv import load_dotenv
load_dotenv()

class RedisManager:
    _instance: Optional["RedisManager"] = None
    _client: Optional[Redis] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # 确保每个实例有自己的 _client
        if not hasattr(self, '_client'):
            self._client = None

    def init_app(self, redis_url: Optional[str] = None):

        if redis_url is None:
            redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        
        self._client = Redis.from_url(
            redis_url,
            decode_responses=True,
            max_connections=50,
            socket_keepalive=True,
            retry_on_timeout=True,
            health_check_interval=30
        )

    @property
    def client(self):
        if self._client is None:
            self.init_app()
        return self._client

    async def close(self):
        if self._client:
            await self._client.close()
            self._client = None

    @asynccontextmanager
    async def get_connection(self):
        try:
            yield self.client
        finally:
            pass

    


redis_manager = RedisManager()
