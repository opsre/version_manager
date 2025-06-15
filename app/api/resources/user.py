from flask import request, jsonify
from flask.views import MethodView
from app.services.user_service import UserService
from app.services.operation_log_service import OperationLogService

class UserResource(MethodView):
    def get(self, user_id):
        """获取用户信息"""
        user = UserService.get_user_by_id(user_id)
        if not user:
            return jsonify({'error': '用户不存在'}), 404
        return jsonify(user.to_dict())
    
    def put(self, user_id):
        """更新用户信息"""
        data = request.json
        
        # 获取操作人ID，如果没有提供，则使用默认值1或被修改的用户ID
        operator_id = data.get('operator_id')
        if not operator_id:
            operator_id = 1  # 默认使用ID为1的用户作为操作人
        
        # 从data中移除operator_id，因为User模型中没有这个字段
        if 'operator_id' in data:
            del data['operator_id']
        
        # 获取用户原始信息，用于日志记录
        user = UserService.get_user_by_id(user_id)
        if not user:
            return jsonify({'error': '用户不存在'}), 404
        
        # 记录原始状态，用于日志记录
        old_username = user.username
        old_status = user.status
        old_role_id = user.role_id
        
        # 更新用户
        updated_user = UserService.update_user(user_id, data)
        if not updated_user:
            return jsonify({'error': '更新失败'}), 400
        
        # 构建操作详情
        details = {
            'user_id': user_id,
            'changes': {}
        }
        
        # 检测哪些字段发生了变化
        for key, value in data.items():
            if hasattr(user, key):
                old_value = getattr(user, key)
                if old_value != value and key != 'password_hash':  # 不记录密码相关信息
                    details['changes'][key] = {
                        'old': str(old_value),
                        'new': str(value)
                    }
        
        # 确定操作类型
        operation_type = '更新'
        if 'status' in data and old_status != data.get('status'):
            operation_type = '状态变更'
        elif 'role_id' in data and old_role_id != data.get('role_id'):
            operation_type = '角色变更'
        
        # 记录操作日志
        OperationLogService.create_log(
            operation_type=operation_type,
            object_type='用户',
            object_name=updated_user.username,
            object_id=user_id,
            operator_id=operator_id,
            details=details
        )
        
        return jsonify(updated_user.to_dict())
    
    def delete(self, user_id):
        """删除用户"""
        # 获取操作人ID
        operator_id = request.args.get('operator_id', type=int)
        if not operator_id:
            operator_id = 1  # 默认使用ID为1的用户作为操作人
        
        # 获取用户信息，用于日志记录
        user = UserService.get_user_by_id(user_id)
        if not user:
            return jsonify({'error': '用户不存在'}), 404
        
        username = user.username
        email = user.email
        
        # 删除用户
        result = UserService.delete_user(user_id)
        if not result:
            return jsonify({'error': '删除失败'}), 400
        
        # 记录操作日志
        OperationLogService.create_log(
            operation_type='删除',
            object_type='用户',
            object_name=username,
            object_id=user_id,
            operator_id=operator_id,
            details={
                'username': username,
                'email': email
            }
        )
        
        return jsonify({'message': '用户已删除'})

class UserListResource(MethodView):
    def get(self):
        """获取所有用户"""
        users = UserService.get_all_users()
        return jsonify([user.to_dict() for user in users])
    
    def post(self):
        """创建新用户"""
        data = request.json
        
        # 验证必要字段
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({'error': '缺少必要字段'}), 400
        
        # 检查用户名是否已存在
        if UserService.get_user_by_username(data['username']):
            return jsonify({'error': '用户名已存在'}), 400
        
        # 获取操作人ID，如果没有提供，则使用默认值1（通常为管理员）
        operator_id = data.get('operator_id')
        if not operator_id:
            operator_id = 1  # 默认使用ID为1的用户作为操作人
        
        # 从data中移除operator_id，因为User模型中没有这个字段
        if 'operator_id' in data:
            del data['operator_id']
        
        # 创建用户
        user = UserService.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            is_admin=data.get('is_admin', False),
            role_id=data.get('role_id'),
            department=data.get('department'),
            name=data.get('name')
        )
        
        # 记录操作日志
        OperationLogService.create_log(
            operation_type='创建',
            object_type='用户',
            object_name=user.username,
            object_id=user.id,
            operator_id=operator_id,
            details={
                'username': user.username,
                'email': user.email,
                'is_admin': user.is_admin,
                'role_id': user.role_id,
                'department': user.department,
                'name': user.name
            }
        )
        
        return jsonify(user.to_dict()), 201