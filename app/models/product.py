from datetime import datetime
from app.extensions import db

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    code = db.Column(db.String(50), unique=True, index=True)
    status = db.Column(db.String(20), default='active')  # active, deprecated, discontinued
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # 负责人ID
    
    # 关系
    versions = db.relationship('Version', backref='product', lazy='dynamic')
    owner = db.relationship('User', backref='products')
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'code': self.code,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'version_count': self.versions.count(),
            'owner_id': self.owner_id,
            'owner_name': self.owner.name if self.owner else None
        }