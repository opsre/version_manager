from app.extensions import db
from app.models.product import Product

class ProductService:
    @staticmethod
    def create_product(name, description, code, status='active', owner_id=None):
        """创建新产品"""
        product = Product(
            name=name,
            description=description,
            code=code,
            status=status,
            owner_id=owner_id
        )
        
        db.session.add(product)
        db.session.commit()
        return product
    
    @staticmethod
    def get_product_by_id(product_id):
        """根据 ID 获取产品"""
        return Product.query.get(product_id)
    
    @staticmethod
    def get_all_products(page=1, per_page=20, status=None):
        """获取所有产品，支持分页和状态过滤"""
        query = Product.query
        
        if status:
            query = query.filter_by(status=status)
        
        return query.order_by(Product.created_at.desc()).paginate(page=page, per_page=per_page)
    
    @staticmethod
    def update_product(product_id, **kwargs):
        """更新产品信息"""
        product = Product.query.get(product_id)
        if not product:
            return None
        
        for key, value in kwargs.items():
            if hasattr(product, key):
                setattr(product, key, value)
        
        db.session.commit()
        return product
    
    @staticmethod
    def delete_product(product_id):
        """删除产品"""
        product = Product.query.get(product_id)
        if not product:
            return False
        
        # 检查是否有关联的版本
        if product.versions.count() > 0:
            return False
        
        db.session.delete(product)
        db.session.commit()
        return True