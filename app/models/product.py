# 导入日期时间模块，用于自动生成创建和更新时间
from datetime import datetime
# 导入数据库实例
from app.extensions import db


class Product(db.Model):
    """
    版本信息数据模型
    
    用于存储和管理软件版本信息及其关联文件
    """
    __tablename__ = 'product'  # 指定数据库表名

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    code = db.Column(db.String(50), unique=True, index=True)
    status = db.Column(db.String(20), default='active')  # active, deprecated, discontinued
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    versions = db.relationship('Version', backref='product', lazy='dynamic')


    def to_dict(self):
        """
        将对象转换为字典格式，便于API返回JSON数据
        
        Returns:
            包含版本信息的字典
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'code': self.code,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'version_count': self.versions.count()
        }
    def __repr__(self):
        """
        对象的字符串表示，用于调试和日志输出

        Returns:
            对象的字符串表示
        """
        return f'<Product {self.name}>'