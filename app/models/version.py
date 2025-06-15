from datetime import datetime
from app.extensions import db

class Version(db.Model):
    __tablename__ = 'versions'
    
    id = db.Column(db.Integer, primary_key=True)
    version_number = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    release_notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='draft')  # draft, released, deprecated
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    released_at = db.Column(db.DateTime)
    lock_status = db.Column(db.Boolean, default=False)  # 锁定状态
    
    # 外键
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # 关系
    files = db.relationship('File', backref='version', lazy='dynamic')
    
    def __repr__(self):
        return f'<Version {self.version_number}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'version_number': self.version_number,
            'description': self.description,
            'release_notes': self.release_notes,
            'status': self.status,
            'product_id': self.product_id,
            'author_id': self.author_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'released_at': self.released_at.isoformat() if self.released_at else None,
            'file_count': self.files.count(),
            'lock_status': self.lock_status
        }