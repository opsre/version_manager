from functools import wraps
from flask import request, jsonify, current_app
import jwt as pyjwt  # 重命名导入以避免冲突
from app.models.user import User

def token_required(f):
    """
    装饰器函数，用于验证JWT令牌并获取当前用户
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # 从请求头中获取令牌
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'error': '未提供认证令牌'}), 401
        
        try:
            # 验证令牌
            data = pyjwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            
            if not current_user:
                return jsonify({'error': '无效的用户令牌'}), 401
                
            if not current_user.status:
                return jsonify({'error': '用户已被禁用'}), 403
                
        except pyjwt.ExpiredSignatureError:
            return jsonify({'error': '令牌已过期，请重新登录'}), 401
        except pyjwt.InvalidTokenError:
            return jsonify({'error': '无效的令牌'}), 401
            
        # 将当前用户传递给被装饰的函数
        return f(current_user, *args, **kwargs)
    
    return decorated

def admin_required(f):
    """
    装饰器函数，用于验证用户是否为管理员
    """
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if not current_user.is_admin:
            return jsonify({'error': '需要管理员权限'}), 403
        return f(current_user, *args, **kwargs)
    
    return decorated 