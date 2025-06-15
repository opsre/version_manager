from flask import request, jsonify
from flask.views import MethodView
from app.models.user_product_permission import UserProductPermission
from app.extensions import db

class UserProductPermissionListResource(MethodView):
    def get(self):
        """查询所有用户-产品权限关联"""
        permissions = UserProductPermission.query.all()
        return jsonify([p.to_dict() for p in permissions])

    def post(self):
        """新增用户-产品权限关联"""
        data = request.get_json()
        user_id = data.get('user_id')
        product_id = data.get('product_id')
        permission_type = data.get('permission_type')
        if not user_id or not product_id or not permission_type:
            return jsonify({'error': '缺少必要参数'}), 400
        if permission_type not in ['read', 'edit', 'admin']:
            return jsonify({'error': '权限类型无效'}), 400
        perm = UserProductPermission(user_id=user_id, product_id=product_id, permission_type=permission_type)
        db.session.add(perm)
        db.session.commit()
        return jsonify(perm.to_dict()), 201

class UserProductPermissionResource(MethodView):
    def get(self, perm_id):
        """查询单个用户-产品权限关联"""
        perm = UserProductPermission.query.get(perm_id)
        if not perm:
            return jsonify({'error': '未找到'}), 404
        return jsonify(perm.to_dict())

    def put(self, perm_id):
        """更新用户-产品权限关联"""
        perm = UserProductPermission.query.get(perm_id)
        if not perm:
            return jsonify({'error': '未找到'}), 404
        data = request.get_json()
        permission_type = data.get('permission_type')
        if permission_type not in ['read', 'edit', 'admin']:
            return jsonify({'error': '权限类型无效'}), 400
        perm.permission_type = permission_type
        db.session.commit()
        return jsonify(perm.to_dict())

    def delete(self, perm_id):
        """删除用户-产品权限关联"""
        perm = UserProductPermission.query.get(perm_id)
        if not perm:
            return jsonify({'error': '未找到'}), 404
        db.session.delete(perm)
        db.session.commit()
        return jsonify({'message': '删除成功'}) 