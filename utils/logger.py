"""
统一日志配置模块
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from config.settings import config


def get_logger(name: str, log_level: str = None):
    """
    获取统一配置的日志器
    
    Args:
        name: 日志器名称
        log_level: 日志级别，默认使用配置中的级别
        
    Returns:
        配置好的日志器对象
    """
    # 创建日志目录
    os.makedirs(config.LOGS_DIR, exist_ok=True)
    
    # 获取日志器
    logger = logging.getLogger(name)
    
    # 如果该日志器还没有处理器，则添加处理器
    if not logger.handlers:
        # 创建旋转文件处理器
        log_file = os.path.join(config.LOGS_DIR, f'{name}.log')
        
        # 检查是否配置了日志轮转
        max_bytes = int(os.getenv('LOG_ROTATION_MAX_SIZE', '10485760'))  # 默认10MB
        backup_count = int(os.getenv('LOG_ROTATION_BACKUP_COUNT', '5'))
        
        handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        
        # 设置处理器格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        # 添加处理器到日志器
        logger.addHandler(handler)
        
        # 设置日志级别
        logger.setLevel(getattr(logging, log_level) if log_level else getattr(logging, config.LOG_LEVEL))
    
    return logger