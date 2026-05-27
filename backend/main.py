# main.py
from fastapi import FastAPI
from quantam import quantam_test
from predict import predict_test
from app.core.setup_development_logging import setup_development_logging
from app.models.tempLogger import te


# 获取main模块的logger（自动创建 logs/main/ 目录）
logger = setup_development_logging(__name__)


app = FastAPI()

logger.info("🚀 正在启动交易预测系统...")
logger.info(f"日志基础目录: logs/")

# 测试不同模块
quantam_test()
predict_test()

logger.info("✅ 应用启动完成")

print(te())

@app.get("/")
async def root():
    logger.info("📥 收到根路径请求")
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    logger.info(f"👋 收到问候请求: {name}")
    return {"message": f"Hello {name}"}
