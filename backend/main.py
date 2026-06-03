# main.py
from tkinter import NO

from fastapi import FastAPI, openapi
from contextlib import asynccontextmanager

# from quantam import quantam_test
# from predict import predict_test
from app.core.setup_logging import setup_logging
from app.core.middlewares import setup_middlewares
from app.core.redis_manager import redis_manager
from app.api.v1 import auth
from app.api.health import router as health_router
from app.core.global_exceptions import setup_exception_handlers
from app.core.postgres_manager import db_manage
from sqlalchemy import text
from alembic.config import Config
from alembic import command
import asyncio
from app.core.pydantic_settings_config import settings


# 获取main模块的logger（自动创建 logs/main/ 目录）
logger = setup_logging(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code here runs on startup
    #logger.info(msg="app startup")
    redis_manager.init_app()
    app.state.redis_manager = redis_manager

    try:
        async with db_manage.engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception as e:
        logger.exception("Database startup check failed")
        raise e
        
    # 生产环境通常需要手动或审批后执行迁移 Optional: run migrations (useful in dev/CI; avoid in production unless intentional)
    try:
        def _run_alembic():
            cfg = Config("alembic.ini")
            command.upgrade(cfg, "head")
        if settings.enviroment == "development":
            await asyncio.to_thread(_run_alembic)
    except Exception as e:
        logger.exception("Database migration failed")
        raise e
        
    try:
        yield
    finally:
        # Code here runs on shutdown
        await redis_manager.close()
        await db_manage.engine.dispose()
        logger.info(msg="app shutdown")

app = FastAPI(
    title="trade,predict,talk",
    description="the platform can do trade, predict, talk",
    docs_url="/docs" if settings.enviroment == "development" else None,
    redoc_url="/redoc" if settings.enviroment == "development" else None,
    openapi_url="/openapi.json",
    version="0.0.1",
    lifespan=lifespan,
    openapi_tags=[
        {
            "name": "auth",
            "description": "user authentication",
        },
        {
            "name": "trade",
            "description": "two parts foundamental and quantative analysis"
        },
        {
            "name": "predict",
            "description": "analyse and predict "
        },
        {
            "name": "vhuman",
            "description": "virtual human for entertainment"
        }
    ]
)

setup_exception_handlers(app)

setup_middlewares(app=app)

app.include_router(auth.router)
app.include_router(health_router)







import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
