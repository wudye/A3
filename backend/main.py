# main.py
from tkinter import NO

from fastapi import FastAPI
from contextlib import asynccontextmanager
from quantam import quantam_test
from predict import predict_test
from app.core import redis_manager
from app.core.setup_logging import setup_logging
from app.core.middlewares import setup_middlewares
from app.core.redis_manager import redis_manager
from app.api.v1 import auth

# 获取main模块的logger（自动创建 logs/main/ 目录）
logger = setup_logging(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code here runs on startup
    #logger.info(msg="app startup")
    redis_manager.init_app()
    try:
        yield
    finally:
        # Code here runs on shutdown
        await redis_manager.close()
        logger.info(msg="app shutdown")

app = FastAPI(
    title="trade,predict,talk",
    description="the platform can do trade, predict, talk",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    version="0.0.1",
    lifespan=lifespan
)



app.include_router(auth.router)


@app.get("/")
async def root():
    logger.info("📥 收到根路径请求")
    redis = redis_manager.client
    if redis is not None:
        await redis.ping()
        await redis.set("te", "hello")
        await redis.set("te2", "hello2")
        t = await redis.get("te")
        logger.info("test redis get ->{t} ")
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    logger.info(f"👋 收到问候请求: {name}")
    return {"message": f"Hello {name}"}





import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
