from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# 创建扩展实例
db = SQLAlchemy()
migrate = Migrate()

# 初始化函数
def init_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)