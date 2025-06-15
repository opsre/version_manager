from flask import request, current_app
from flask.views import MethodView
from app.services.product_service import ProductService
from app.services.operation_log_service import OperationLogService

class ProductListResource(MethodView):
    def get(self):
        """获取产品列表"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        
        pagination = ProductService.get_all_products(
            page=page,
            per_page=per_page,
            status=status
        )
        
        products = pagination.items
        
        return {
            'success': True,
            'data': {
                'products': [product.to_dict() for product in products],
                'total': pagination.total,
                'pages': pagination.pages,
                'current_page': pagination.page
            }
        }
    
    def post(self):
        """创建新产品"""
        data = request.get_json()
        
        if not data:
            return {'success': False, 'message': '无效的请求数据'}, 400
        
        name = data.get('name')
        description = data.get('description', '')
        code = data.get('code')
        status = data.get('status', 'active')
        owner_id = data.get('owner_id')
        
        if not name or not code:
            return {'success': False, 'message': '产品名称和代码不能为空'}, 400
        
        # 创建产品
        product = ProductService.create_product(
            name=name,
            description=description,
            code=code,
            status=status,
            owner_id=owner_id
        )
        
        # 记录操作日志，使用owner_id作为操作人ID
        operator_id = owner_id if owner_id else 1  # 如果没有owner_id，则使用默认ID 1
        
        OperationLogService.create_log(
            operation_type='创建',
            object_type='产品',
            object_name=name,
            object_id=product.id,
            operator_id=operator_id,
            details={
                'name': name,
                'code': code,
                'description': description,
                'status': status
            }
        )
        
        return {'success': True, 'data': product.to_dict()}, 201

class ProductResource(MethodView):
    def get(self, product_id):
        """获取产品详情"""
        product = ProductService.get_product_by_id(product_id)
        
        if not product:
            return {'success': False, 'message': '产品不存在'}, 404
        
        return {'success': True, 'data': product.to_dict()}
    
    def put(self, product_id):
        """更新产品信息"""
        product = ProductService.get_product_by_id(product_id)
        
        if not product:
            return {'success': False, 'message': '产品不存在'}, 404
        
        data = request.get_json()
        
        if not data:
            return {'success': False, 'message': '无效的请求数据'}, 400
        
        # 获取操作人ID，如果没有提供，则使用产品所有者ID作为默认值
        operator_id = data.get('operator_id')
        if not operator_id:
            operator_id = product.owner_id if product.owner_id else 1  # 使用产品所有者ID或默认ID
        
        # 从data中移除operator_id，因为Product模型中没有这个字段
        if 'operator_id' in data:
            del data['operator_id']
        
        # 记录原始状态，用于日志记录
        old_name = product.name
        old_status = product.status
        
        updated_product = ProductService.update_product(
            product_id=product_id,
            **data
        )
        
        # 构建操作详情
        details = {
            'product_id': product_id,
            'changes': {}
        }
        
        # 检测哪些字段发生了变化
        for key, value in data.items():
            if hasattr(product, key):
                old_value = getattr(product, key)
                if old_value != value:
                    details['changes'][key] = {
                        'old': str(old_value),
                        'new': str(value)
                    }
        
        # 确定操作类型
        operation_type = '更新'
        if 'status' in data and old_status != data['status']:
            operation_type = '状态变更'
        
        # 记录操作日志
        OperationLogService.create_log(
            operation_type=operation_type,
            object_type='产品',
            object_name=updated_product.name,
            object_id=product_id,
            operator_id=operator_id,
            details=details
        )
        
        return {'success': True, 'data': updated_product.to_dict()}
    
    def delete(self, product_id):
        """删除产品"""
        # 获取操作人ID
        operator_id = request.args.get('operator_id', type=int)
        
        # 获取产品信息，用于日志记录
        product = ProductService.get_product_by_id(product_id)
        if not product:
            return {'success': False, 'message': '产品不存在'}, 404
        
        # 如果没有提供操作人ID，则使用产品所有者ID作为默认值
        if not operator_id:
            operator_id = product.owner_id if product.owner_id else 1
        
        product_name = product.name
        product_code = product.code
        
        result = ProductService.delete_product(product_id)
        
        if not result:
            return {'success': False, 'message': '产品不存在或无法删除'}, 400
        
        # 记录操作日志
        OperationLogService.create_log(
            operation_type='删除',
            object_type='产品',
            object_name=product_name,
            object_id=product_id,
            operator_id=operator_id,
            details={
                'name': product_name,
                'code': product_code
            }
        )
        
        return {'success': True, 'message': '产品已成功删除'}, 200

    @staticmethod
    def get_all_products():
        """获取所有产品（静态方法，供外部调用）"""
        products = ProductService.get_all_products(page=1, per_page=10000)  # 默认查全部
        return [product.to_dict() for product in products.items]