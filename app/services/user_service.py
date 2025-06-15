from app.extensions import db
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class UserService:
    @staticmethod
    def create_user(username, email, password, is_admin=False, role_id=None, department=None, name=None):
        """创建新用户"""
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            is_admin=is_admin,
            role_id=role_id,
            department=department,
            name=name,
            status=True
        )
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def get_user_by_id(user_id):
        """根据 ID 获取用户"""
        return User.query.get(user_id)
    
    @staticmethod
    def get_user_by_username(username):
        """根据用户名获取用户"""
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def get_all_users():
        """获取所有用户"""
        return User.query.all()
    
    @staticmethod
    def update_user(user_id, data):
        """更新用户信息"""
        user = User.query.get(user_id)
        if not user:
            return None
        
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'password' in data:
            user.password_hash = generate_password_hash(data['password'])
        if 'is_admin' in data:
            user.is_admin = data['is_admin']
        if 'role_id' in data:
            user.role_id = data['role_id']
        if 'department' in data:
            user.department = data['department']
        if 'status' in data:
            user.status = data['status']
        if 'name' in data:
            user.name = data['name']
        
        db.session.commit()
        return user
    
    @staticmethod
    def delete_user(user_id):
        """删除用户"""
        user = User.query.get(user_id)
        if not user:
            return False
        
        db.session.delete(user)
        db.session.commit()
        return True
    
    @staticmethod
    def verify_password(user, password):
        """验证用户密码"""
        if not user:
            return False
        return check_password_hash(user.password_hash, password)
        
    @staticmethod
    def update_login_time(user_id):
        """更新用户最后登录时间"""
        user = User.query.get(user_id)
        if user:
            user.last_login_at = datetime.utcnow()
            db.session.commit()
            return True
        return False
        
    @staticmethod
    def get_users_by_role(role_id):
        """获取指定角色的所有用户"""
        return User.query.filter_by(role_id=role_id).all()
        
    @staticmethod
    def get_users_by_department(department):
        """获取指定部门的所有用户"""
        return User.query.filter_by(department=department).all()