from app.extensions import db

class UserProductPermission(db.Model):
    __tablename__ = 'user_product_permissions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    permission_type = db.Column(db.String(20), nullable=False)  # read/edit/admin
    
    user = db.relationship('User', backref=db.backref('product_permissions', lazy='dynamic'))
    product = db.relationship('Product', backref=db.backref('user_permissions', lazy='dynamic'))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'permission_type': self.permission_type
        } 