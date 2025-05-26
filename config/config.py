# 导入操作系统模块和环境变量加载库
import os
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()


class Config:
    """基础配置类，定义应用程序的基本配置项"""
    # 基础配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')  # Flask密钥，用于会话安全等

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://test:123456@localhost/version_test')  # 数据库连接URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 关闭SQLAlchemy的修改跟踪功能，提高性能

    # 服务器配置
    HOST = os.getenv('HOST', '0.0.0.0')  # 服务器绑定的主机地址
    PORT = int(os.getenv('PORT', 5000))  # 服务器端口

    # 日志配置
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')  # 日志级别
    LOG_PATH = os.getenv('LOG_PATH', 'logs')  # 日志存储路径

    # FTP配置
    FTP_HOST = os.environ.get('FTP_HOST')
    FTP_PORT = int(os.environ.get('FTP_PORT', 21))
    FTP_USERNAME = os.environ.get('FTP_USERNAME')
    FTP_PASSWORD = os.environ.get('FTP_PASSWORD')
    FTP_DIRECTORY = os.environ.get('FTP_DIRECTORY')

    # 文件上传配置
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')  # 文件上传目录
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB 上传文件大小限制


class DevelopmentConfig(Config):
    """开发环境配置类"""
    DEBUG = True  # 启用调试模式


class ProductionConfig(Config):
    """生产环境配置类"""
    DEBUG = False  # 禁用调试模式


class TestingConfig(Config):
    """测试环境配置类"""
    TESTING = True  # 启用测试模式
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # 使用内存数据库进行测试


# 配置字典，用于选择不同的配置环境
config = {
    'development': DevelopmentConfig,  # 开发环境
    'production': ProductionConfig,    # 生产环境
    'testing': TestingConfig,          # 测试环境
    'default': DevelopmentConfig       # 默认使用开发环境配置
}