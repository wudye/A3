

from contextlib import asynccontextmanager
from http.client import TEMPORARY_REDIRECT
import socket
from typing import Optional
from jwt import decode
from redis.asyncio import Redis, ConnectionPool, BlockingConnectionPool
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
        
        pool = BlockingConnectionPool.from_url(
            redis_url,
            decode_responses=True,
            max_connections=100,
            socket_keepalive=True,
            retry_on_timeout=True,
            timeout=5,
            health_check_interval=30

        )
        """
        self._client = Redis.from_url(
            redis_url,
            decode_responses=True,
            max_connections=50,
            socket_keepalive=True,
            retry_on_timeout=True,
            health_check_interval=30
        )
        """
        self._client = Redis(connection_pool=pool)


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

"""
Batch using pipeline (recommended)
    redis = redis_manager.client

    # one-shot pipeline
    pipe = redis.pipeline()
    for k, v in items.items():
        pipe.set(k, v)
    # commands are queued, then executed together
    results = await pipe.execute()

Chunked pipelines for very large batches
    async def batch_set(items: dict[str,str], chunk_size: int = 500):
        redis = redis_manager.client
        pairs = list(items.items())
        for i in range(0, len(pairs), chunk_size):
            chunk = pairs[i:i+chunk_size]
            pipe = redis.pipeline()
            for k, v in chunk:
                pipe.set(k, v)
            await pipe.execute()


Add a pipeline helper     
    @asynccontextmanager
    async def pipeline(self):
        pipe = self.client.pipeline()
        try:
            yield pipe
            await pipe.execute()
        finally:
            pass
    usage
    async with redis_manager.pipeline() as pipe:
        pipe.set("a", 1)
        pipe.incr("cnt")
"""