# main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from quantam import quantam_test
from predict import predict_test
from app.core.setup_logging import setup_logging
from app.models.tempLogger import te


# 获取main模块的logger（自动创建 logs/main/ 目录）
logger = setup_logging(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code here runs on startup
    #logger.info(msg="app startup")
    try:
        yield
    finally:
        # Code here runs on shutdown
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





@app.get("/")
async def root():
    logger.info("📥 收到根路径请求")
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    logger.info(f"👋 收到问候请求: {name}")
    return {"message": f"Hello {name}"}
