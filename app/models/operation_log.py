from datetime import datetime
from app.extensions import db

class OperationLog(db.Model):
    __tablename__ = 'operation_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    operation_time = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    operation_type = db.Column(db.String(50), nullable=False, index=True)  # 创建、更新、状态变更、删除等
    object_type = db.Column(db.String(50), nullable=False, index=True)  # 产品、版本、用户、权限等
    object_name = db.Column(db.String(100))  # 对象名称
    object_id = db.Column(db.String(50), index=True)  # 对象ID
    operator_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)  # 操作人ID
    details = db.Column(db.Text)  # 操作详情，可以存储JSON字符串
    
    # 关系
    operator = db.relationship('User', backref=db.backref('operations', lazy='dynamic'))
    
    def __repr__(self):
        return f'<OperationLog {self.operation_type} {self.object_type} {self.object_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'operation_time': self.operation_time.isoformat(),
            'operation_type': self.operation_type,
            'object_type': self.object_type,
            'object_name': self.object_name,
            'object_id': self.object_id,
            'operator_id': self.operator_id,
            'operator_name': self.operator.name if self.operator else None,
            'details': self.details
        } 