# 导入Flask框架
from flask import Flask
# 导入数据库和迁移工具扩展
from app.extensions import db, migrate
# 导入日志设置工具
from app.utils.logger import setup_logger
# 导入API路由蓝图
from app.api.routes import api_bp


def create_app(config_object):
    """
    应用工厂函数，创建并配置Flask应用实例
    
    Args:
        config_object: 配置对象，包含应用程序所需的各种配置
        
    Returns:
        配置好的Flask应用实例
    """
    # 创建Flask应用实例
    app = Flask(__name__)
    # 从配置对象加载配置
    app.config.from_object(config_object)

    # 初始化扩展
    db.init_app(app)  # 初始化SQLAlchemy
    migrate.init_app(app, db)  # 初始化Flask-Migrate进行数据库迁移管理

    # 设置日志系统
    setup_logger(app)

    # 注册蓝图，设置URL前缀
    app.register_blueprint(api_bp, url_prefix='/api')

    # 创建数据库表（如果不存在）
    with app.app_context():
        db.create_all()

    return app