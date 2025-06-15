from flask import request, current_app
from flask.views import MethodView
from app.services.version_service import VersionService
from app.services.product_service import ProductService
from app.services.operation_log_service import OperationLogService

class VersionListResource(MethodView):
    def get(self):
        """获取版本列表"""
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        product_id = request.args.get('product_id', type=int)
        
        if product_id:
            pagination = VersionService.get_versions_by_product(
                product_id=product_id,
                page=page,
                per_page=per_page,
                status=status
            )
        else:
            # 新增：获取所有版本
            pagination = VersionService.get_all_versions(
                page=page,
                per_page=per_page,
                status=status
            )
        
        versions = pagination.items
        
        return {
            'success': True,
            'data': {
                'versions': [version.to_dict() for version in versions],
                'total': pagination.total,
                'pages': pagination.pages,
                'current_page': pagination.page
            }
        }
    
    def post(self):
        """创建新版本"""
        data = request.get_json()
        
        if not data:
            return {'success': False, 'message': '无效的请求数据'}, 400
        
        product_id = data.get('product_id')
        version_number = data.get('version_number')
        description = data.get('description', '')
        release_notes = data.get('release_notes', '')
        author_id = data.get('author_id')
        status = data.get('status', 'draft')
        lock_status = data.get('lock_status', False)
        
        if not product_id or not version_number or not author_id:
            return {'success': False, 'message': '产品ID、版本号和作者ID不能为空'}, 400
        
        # 检查产品是否存在
        product = ProductService.get_product_by_id(product_id)
        if not product:
            return {'success': False, 'message': '指定的产品不存在'}, 404
        
        version = VersionService.create_version(
            product_id=product_id,
            version_number=version_number,
            description=description,
            release_notes=release_notes,
            author_id=author_id,
            status=status,
            lock_status=lock_status
        )
        
        # 记录操作日志
        OperationLogService.create_log(
            operation_type='创建',
            object_type='版本',
            object_name=version_number,
            object_id=version.id,
            operator_id=author_id,
            details={
                'product_id': product_id,
                'product_name': product.name,
                'version_number': version_number,
                'description': description,
                'status': status
            }
        )
        
        return {'success': True, 'data': version.to_dict()}, 201

class VersionResource(MethodView):
    def get(self, version_id):
        """获取版本详情"""
        version = VersionService.get_version_by_id(version_id)
        
        if not version:
            return {'success': False, 'message': '版本不存在'}, 404
        
        return {'success': True, 'data': version.to_dict()}
    
    def put(self, version_id):
        """更新版本信息"""
        version = VersionService.get_version_by_id(version_id)
        
        if not version:
            return {'success': False, 'message': '版本不存在'}, 404
        
        data = request.get_json()
        
        if not data:
            return {'success': False, 'message': '无效的请求数据'}, 400
        
        # 不允许更改产品ID和作者ID
        if 'product_id' in data:
            del data['product_id']
        if 'author_id' in data:
            del data['author_id']
        
        # 记录原始状态，用于日志记录
        old_status = version.status
        old_version_number = version.version_number
        
        # 获取操作人ID，如果没有提供，则使用版本作者ID作为默认值
        operator_id = data.get('operator_id')
        if not operator_id:
            operator_id = version.author_id  # 使用版本作者ID作为默认操作人ID
        
        # 从data中移除operator_id，因为Version模型中没有这个字段
        if 'operator_id' in data:
            del data['operator_id']
        
        updated_version = VersionService.update_version(
            version_id=version_id,
            **data
        )
        
        # 构建操作详情
        details = {
            'product_id': version.product_id,
            'product_name': version.product.name,
            'version_number': updated_version.version_number,
            'changes': {}
        }
        
        # 检测哪些字段发生了变化
        for key, value in data.items():
            if hasattr(version, key):
                old_value = getattr(version, key)
                if old_value != value:
                    details['changes'][key] = {
                        'old': str(old_value),
                        'new': str(value)
                    }
        
        # 确定操作类型
        operation_type = '更新'
        if 'status' in data and old_status != data['status']:
            if data['status'] == 'released':
                operation_type = '发布'
            elif data['status'] == 'deprecated':
                operation_type = '废弃'
            else:
                operation_type = '状态变更'
        elif 'lock_status' in data:
            if data['lock_status'] == True:
                operation_type = '锁定'
            else:
                operation_type = '解锁'
        
        # 记录操作日志
        OperationLogService.create_log(
            operation_type=operation_type,
            object_type='版本',
            object_name=updated_version.version_number,
            object_id=version_id,
            operator_id=operator_id,
            details=details
        )
        
        return {'success': True, 'data': updated_version.to_dict()}
    
    def delete(self, version_id):
        """删除版本"""
        # 获取操作人ID
        operator_id = request.args.get('operator_id', type=int)
        if not operator_id:
            # 获取版本信息，用于获取默认操作人ID
            version = VersionService.get_version_by_id(version_id)
            if not version:
                return {'success': False, 'message': '版本不存在'}, 404
            operator_id = version.author_id  # 使用版本作者ID作为默认操作人ID
        
        # 获取版本信息，用于日志记录
        version = VersionService.get_version_by_id(version_id)
        if not version:
            return {'success': False, 'message': '版本不存在'}, 404
        
        version_number = version.version_number
        product_id = version.product_id
        product_name = version.product.name
        
        result = VersionService.delete_version(version_id)
        
        if not result:
            return {'success': False, 'message': '版本不存在或无法删除'}, 400
        
        # 记录操作日志
        OperationLogService.create_log(
            operation_type='删除',
            object_type='版本',
            object_name=version_number,
            object_id=version_id,
            operator_id=operator_id,
            details={
                'product_id': product_id,
                'product_name': product_name,
                'version_number': version_number
            }
        )
        
        return {'success': True, 'message': '版本已成功删除'}, 200

class VersionHistoryResource(MethodView):
    def get(self, product_id):
        """获取产品的版本历史"""
        # 检查产品是否存在
        product = ProductService.get_product_by_id(product_id)
        if not product:
            return {'success': False, 'message': '指定的产品不存在'}, 404
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        
        pagination = VersionService.get_versions_by_product(
            product_id=product_id,
            page=page,
            per_page=per_page,
            status=status
        )
        
        versions = pagination.items
        
        return {
            'success': True,
            'data': {
                'product': product.to_dict(),
                'versions': [version.to_dict() for version in versions],
                'total': pagination.total,
                'pages': pagination.pages,
                'current_page': pagination.page
            }
        }