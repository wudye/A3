from fastapi import APIRouter, Request, Depends

from app.core.setup_logging import setup_logging
from app.core.dependencies import get_current_user

# from app.core.redis_manager import redis_manager

logger = setup_logging(__name__)

router = APIRouter(tags=["health"])


@router.get("/", dependencies=[Depends(get_current_user)])
async def root(request: Request):
    from typing import Awaitable, cast

    logger.info("📥 收到根路径请求")
    redis_manager = request.app.state.redis_manager
    redis = redis_manager.client
    if redis is not None:

        result = await cast(Awaitable[bool], redis.ping())
        await redis.set("te", "hello")
        await redis.set("te2", "hello2")
        t = await redis.get("te")
        logger.info("test redis get ->{t} ")
    return {"message": "Hello World"}

@router.get("/hello/{name}",  dependencies=[Depends(get_current_user)])
async def say_hello(name: str):
    logger.info(f"👋 收到问候请求: {name}")
    return {"message": f"Hello {name}"}


@router.get("/health")
async def health():
    return {"status": "ok"}