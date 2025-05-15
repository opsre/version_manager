# 导入SQLAlchemy用于数据库ORM操作
from flask_sqlalchemy import SQLAlchemy
# 导入Flask-Migrate用于数据库迁移管理
from flask_migrate import Migrate

# 创建SQLAlchemy实例，用于数据库操作和ORM模型定义
db = SQLAlchemy()
# 创建Migrate实例，用于处理数据库结构变更的迁移
migrate = Migrate()