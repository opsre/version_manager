from app.extensions import db
from app.models.role import Role

class RoleService:
    @staticmethod
    def create_role(name, description='', status=True):
        """创建新角色"""
        role = Role(
            name=name,
            description=description,
            status=status
        )
        db.session.add(role)
        db.session.commit()
        return role
    
    @staticmethod
    def get_role_by_id(role_id):
        """根据 ID 获取角色"""
        return Role.query.get(role_id)
    
    @staticmethod
    def get_role_by_name(name):
        """根据名称获取角色"""
        return Role.query.filter_by(name=name).first()
    
    @staticmethod
    def get_all_roles():
        """获取所有角色"""
        return Role.query.all()
    
    @staticmethod
    def update_role(role_id, data):
        """更新角色信息"""
        role = Role.query.get(role_id)
        if not role:
            return None
        
        if 'name' in data:
            role.name = data['name']
        if 'description' in data:
            role.description = data['description']
        if 'status' in data:
            role.status = data['status']
        
        db.session.commit()
        return role
    
    @staticmethod
    def delete_role(role_id):
        """删除角色"""
        role = Role.query.get(role_id)
        if not role:
            return False
        
        # 检查是否有用户使用该角色
        if role.users.count() > 0:
            return False
        
        db.session.delete(role)
        db.session.commit()
        return True 