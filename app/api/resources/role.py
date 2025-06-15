from flask import request, jsonify
from flask.views import MethodView
from app.services.role_service import RoleService

class RoleResource(MethodView):
    def get(self, role_id):
        """获取角色信息"""
        role = RoleService.get_role_by_id(role_id)
        if not role:
            return jsonify({'error': '角色不存在'}), 404
        return jsonify(role.to_dict())
    
    def put(self, role_id):
        """更新角色信息"""
        data = request.json
        role = RoleService.update_role(role_id, data)
        if not role:
            return jsonify({'error': '角色不存在'}), 404
        return jsonify(role.to_dict())
    
    def delete(self, role_id):
        """删除角色"""
        result = RoleService.delete_role(role_id)
        if not result:
            return jsonify({'error': '角色不存在或无法删除'}), 404
        return jsonify({'message': '角色已删除'})

class RoleListResource(MethodView):
    def get(self):
        """获取所有角色"""
        roles = RoleService.get_all_roles()
        return jsonify([role.to_dict() for role in roles])
    
    def post(self):
        """创建新角色"""
        data = request.json
        
        # 验证必要字段
        if 'name' not in data:
            return jsonify({'error': '缺少必要字段: name'}), 400
        
        # 检查角色名是否已存在
        if RoleService.get_role_by_name(data['name']):
            return jsonify({'error': '角色名已存在'}), 400
        
        # 创建角色
        role = RoleService.create_role(
            name=data['name'],
            description=data.get('description', ''),
            status=data.get('status', True)
        )
        
        return jsonify(role.to_dict()), 201 