# app/core/config.py
from functools import lru_cache
from typing import Optional
from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    """应用配置（支持 .env 文件和系统环境变量）"""
    
    model_config = SettingsConfigDict(
        env_file=[
            ".env",                    # 当前目录
            "../.env",                 # 父目录
            Path(__file__).parent.parent.parent / ".env",  # 绝对路径
        ],        
        env_file_encoding="utf-8",
        env_nested_delimiter="__", # 支持嵌套配置（如 REDIS__HOST）
        case_sensitive=False,      # 不区分大小写
        extra="allow",            #
    )
    
    # Redis 配置
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        description="Redis 连接URL"
    )
    redis_password: Optional[str] = Field(
        default=None,
        description="Redis 密码（可选）"
    )
    redis_max_connections: int = Field(
        default=50,
        ge=1,
        le=100,
        description="Redis 最大连接数"
    )
    
    # 数据库配置
    database_url: Optional[PostgresDsn] = Field(
        default=None,
        description="PostgreSQL 数据库URL"
    )
    
    # API 配置
    api_auth_key: Optional[str] = Field(
        default=None,
        description="API 认证密钥"
    )
    
    # 日志配置
    log_level: str = Field(
        default="INFO",
        pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$"
    )
    
    # LLM 配置（从你的 .env 文件）
    langchain_provider: Optional[str] = None
    langchain_model_name: Optional[str] = None
    openrouter_api_key: Optional[str] = None
    
    # 其他业务配置
    tushare_token: Optional[str] = None
    jwt_secret_key: str = Field(
        default="your-super-secret-key-change-this-in-production",
        min_length=32
    )
    jwt_expire_minutes: int = Field(
        default=1440,
        ge=1
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    获取配置（LRU 缓存确保只加载一次）
    
    使用示例：
        from app.core.config import get_settings
        settings = get_settings()
        redis_url = settings.redis_url
    """
    return Settings()


# 全局配置实例（可选，提供更简单的导入方式）
settings = get_settings()
