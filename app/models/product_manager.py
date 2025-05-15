# 导入日期时间模块，用于自动生成创建和更新时间
from datetime import datetime
# 导入数据库实例
from app.extensions import db


class Product_Manager(db.Model):
    """
    版本信息数据模型
    
    用于存储和管理软件版本信息及其关联文件
    """
    __tablename__ = 'product_manager'  # 指定数据库表名

    # 产品id
    product_id = db.Column(db.Integer, primary_key=True)
    # 产品代码
    product_code = db.Column(db.String(50), nullable=False, unique=True)
    # 产品描述
    product_desc = db.Column(db.Text)
    # 创建用户名
    create_user = db.Column(db.String(50), nullable=False, unique=True)
    # 创建时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """
        将对象转换为字典格式，便于API返回JSON数据
        
        Returns:
            包含版本信息的字典
        """
        return {
            'product_id': self.id,
            'product_code': self.version,
            'product_desc': self.description,
            'create_user': self.created_at.isoformat(),
            'created_at': self.updated_at.isoformat()
        }

    def __repr__(self):
        """
        对象的字符串表示，用于调试和日志输出
        
        Returns:
            对象的字符串表示
        """
        return f'<Version {self.version}>'