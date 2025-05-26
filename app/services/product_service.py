from app import db
from app.models.product import Product

class ProductService:
    @staticmethod
    def create_product(name, description, code, status):
        product =Product(
            name=name,
            description=description,
            code=code,
            status=status,
        )
        db.session.add(product)
        db.session.commit()
        return product
    @staticmethod
    def get_product_by_id(product_id):
        """根据ID获取产品"""
        return Product.query.get(product_id)
    @staticmethod
    def get_all_products():
        """获取所有产品，支持分页和状态过滤"""
