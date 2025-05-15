# 导入日期时间模块，用于自动生成创建和更新时间
from datetime import datetime
# 导入数据库实例
from app.extensions import db


class Version(db.Model):
    """
    版本信息数据模型
    
    用于存储和管理软件版本信息及其关联文件
    """
    __tablename__ = 'versions'  # 指定数据库表名

    # 主键ID
    id = db.Column(db.Integer, primary_key=True)
    # 版本号，不可为空且唯一
    version = db.Column(db.String(50), nullable=False, unique=True)
    # 版本描述
    description = db.Column(db.Text)
    # 关联文件路径
    file_path = db.Column(db.String(255))
    # 记录创建时间，自动设置为当前UTC时间
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # 记录更新时间，创建时为当前时间，更新时自动更新为当前时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """
        将对象转换为字典格式，便于API返回JSON数据
        
        Returns:
            包含版本信息的字典
        """
        return {
            'id': self.id,
            'version': self.version,
            'description': self.description,
            'file_path': self.file_path,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __repr__(self):
        """
        对象的字符串表示，用于调试和日志输出
        
        Returns:
            对象的字符串表示
        """
        return f'<Version {self.version}>'