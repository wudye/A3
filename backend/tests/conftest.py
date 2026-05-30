import asyncio
from asyncio.events import AbstractEventLoop
from tkinter import YES
from typing import Any, Generator
from unittest.mock import AsyncMock, patch

from annotated_types import T
import fakeredis
from jwt import decode
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import engine
from main import app

@pytest.fixture
def client() :
    """创建测试客户端夹具"""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def fake_redis():
    reids = fakeredis.FakeRedis(decode_responses=True)
    yield reids
    reids.close()

@pytest.fixture
def mock_redis_client():
    with patch('app.core.redis_manager.Redis') as mock_redis:
        mock_client = AsyncMock()
        mock_redis.from_url.return_value = mock_client
        yield mock_client


@pytest.fixture
def rate_limit_config():
    return {
        "info": 5,
        "quant": 3,
        "default": 10
        
    }

import pytest
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from fastapi.testclient import TestClient
import os

from app.models.base import  Base
from main import app
import pytest_asyncio


TEST_DATABASE_URL ="postgresql+asyncpg://a3_user:nopass@localhost:5432/a3_db"
pytest.fixture(scope="session")
def event_loop() -> Generator[AbstractEventLoop, Any, None]:
    """创建事件循环"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session")
async def test_engine():
    """测试数据库引擎"""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        poolclass=NullPool
    )
    
    # 创建所有表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # 删除所有表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()

@pytest_asyncio.fixture
async def test_session(test_engine):
    """测试数据库会话"""
    async_session = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session
    
    # 清理数据
    async with test_engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete())

@pytest.fixture
def test_client():
    """测试客户端"""
    with TestClient(app) as client:
        yield client