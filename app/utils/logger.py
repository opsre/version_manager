# 导入操作系统模块，用于文件和目录操作
import os
# 导入loguru库的日志记录器
from loguru import logger
# 导入Flask请求上下文工具
from flask import has_request_context, request


def setup_logger(app):
    """
    配置应用程序的日志系统
    
    Args:
        app: Flask应用实例
        
    功能:
        1. 创建日志目录（如果不存在）
        2. 配置日志格式、轮转策略和级别
        3. 设置请求和响应的日志记录
    """
    # 获取配置中的日志路径
    log_path = app.config['LOG_PATH']
    # 如果日志目录不存在，则创建
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    # 设置日志文件路径
    log_file = os.path.join(log_path, 'app.log')

    # 配置日志格式和存储策略
    logger.add(
        log_file,                 # 日志文件路径
        rotation="500 MB",        # 当日志文件达到500MB时轮转
        retention="10 days",      # 保留最近10天的日志
        level=app.config['LOG_LEVEL'],  # 日志级别从配置中获取
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",  # 日志格式
        enqueue=True              # 多进程安全
    )

    # 添加请求前处理器，记录请求信息
    @app.before_request
    def log_request_info():
        """在处理每个请求前记录请求信息"""
        if has_request_context():
            logger.info(f"Request: {request.method} {request.url}")

    # 添加请求后处理器，记录响应信息
    @app.after_request
    def log_response_info(response):
        """
        在处理每个请求后记录响应信息
        
        Args:
            response: Flask响应对象
            
        Returns:
            原始响应对象
        """
        if has_request_context():
            logger.info(f"Response: {response.status}")
        return response