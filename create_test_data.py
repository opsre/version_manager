from app import create_app, db
from app.models.product import Product
from app.models.user import User
from app.models.version import Version

def create_test_data():
    """创建测试数据"""
    app = create_app()
    with app.app_context():
        print('开始添加测试数据')
        try:
            # 检查是否已存在测试产品
            existing_product = Product.query.filter_by(code='TEST001').first()
            if existing_product:
                print(f'产品 TEST001 已存在，ID: {existing_product.id}')
                product = existing_product
            else:
                # 创建产品
                product = Product(
                    name='测试产品',
                    code='TEST001',
                    description='用于测试的产品'
                )
                db.session.add(product)
                db.session.flush()
                print(f'产品创建成功，ID: {product.id}')
            
            # 检查是否已存在测试用户
            existing_user = User.query.filter_by(username='admin').first()
            if existing_user:
                print(f'用户 admin 已存在，ID: {existing_user.id}')
                user = existing_user
            else:
                # 创建用户
                user = User(
                    username='admin',
                    email='admin@example.com',
                    password_hash='123456',
                    is_admin=True
                )
                db.session.add(user)
                db.session.flush()
                print(f'用户创建成功，ID: {user.id}')
            
            # 检查是否已存在版本
            existing_version = Version.query.filter_by(
                version_number='1.0.0',
                product_id=product.id
            ).first()
            
            if existing_version:
                print(f'版本 1.0.0 已存在，ID: {existing_version.id}')
                version = existing_version
            else:
                # 创建版本
                version = Version(
                    version_number='1.0.0',
                    description='初始版本',
                    status='draft',
                    product_id=product.id,
                    author_id=user.id
                )
                db.session.add(version)
                db.session.commit()
                print(f'版本创建成功，ID: {version.id}')
            
            print('测试数据创建完成')
            print(f'上传文件时请使用以下参数:')
            print(f'version_id={version.id}')
            print(f'uploader_id={user.id}')
            
        except Exception as e:
            db.session.rollback()
            print(f'创建测试数据出错: {str(e)}')

if __name__ == '__main__':
    create_test_data() 