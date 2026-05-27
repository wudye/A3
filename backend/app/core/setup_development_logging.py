from fileinput import filename
import logging
import os
from os import path
from pathlib import Path

from rich.logging import RichHandler
from rich.console import Console
from datetime import datetime
import inspect

# 全局标志，确保根日志记录器只配置一次
_ROOT_LOGGER_CONFIGURED = False

def setup_development_logging(module_name: str | None):
    """
    为指定模块设置开发日志
    
    Args:
        module_name: 模块名称（通常传入 __name__），如果为 None 则自动检测
    
    Returns:
        logging.Logger: 配置好的日志记录器
    """
    global _ROOT_LOGGER_CONFIGURED
    
    # 1. 确定模块名称
    if module_name is None:
        # 自动检测调用者模块名
        caller_frame = inspect.stack()[1]
        caller_module = inspect.getmodule(caller_frame[0])
        if caller_module and hasattr(caller_module, '__file__') and caller_module.__file__:
            module_name = Path(caller_module.__file__).stem
        else:
            module_name = "unknown"
    
    # 2. 确保 logs 目录存在
    logs_dir = Path(__file__).resolve().parent.parent.parent / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    # 3. 配置根日志记录器（只执行一次）
    if not _ROOT_LOGGER_CONFIGURED:
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        
        # 控制台格式化器
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        
        # Rich 控制台处理器
        console = Console(color_system="truecolor")
        rich_handler = RichHandler(
            console=console,
            rich_tracebacks=True,
            tracebacks_show_locals=True,
            show_level=True,
            show_path=True,
            show_time=True,
            level=logging.INFO
        )
        root_logger.addHandler(rich_handler)
        
        # 普通控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
        
        # 为特定模块设置不同级别
        logging.getLogger("uvicorn").setLevel(logging.WARNING)
        logging.getLogger("quantam").setLevel(logging.DEBUG)
        logging.getLogger("predict").setLevel(logging.DEBUG)
        
        _ROOT_LOGGER_CONFIGURED = True
    
    # 4. 创建模块特定的日志记录器
    module_logger = logging.getLogger(module_name)
    module_logger.setLevel(logging.DEBUG)
    
    # 检查是否已为该模块添加了文件处理器
    log_file: Path = logs_dir / f"{module_name}.log"
    has_file_handler = any(
        isinstance(h, logging.FileHandler) and h.baseFilename == str(log_file)
        for h in module_logger.handlers
    )
    
    if not has_file_handler:
        # 创建文件处理器
        file_handler = logging.FileHandler(
            filename=log_file,
            mode="a",
            encoding="utf-8",
        )
        file_formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        module_logger.addHandler(file_handler)
    
    # 5. 设置传播，确保日志也到达根日志记录器（输出到控制台）
    module_logger.propagate = True
    
    return module_logger
