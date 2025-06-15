from flask import request, jsonify
from flask.views import MethodView
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
import jwt as pyjwt  # 重命名导入以避免冲突
from app.models.user import User
from app.extensions import db
from config import Config

class LoginResource(MethodView):
    def post(self):
        """用户登录API"""
        data = request.get_json()
        
        # 验证请求数据
        if not data:
            return jsonify({"error": "请求数据无效"}), 400
            
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({"error": "用户名和密码不能为空"}), 400
            
        # 查询用户
        user = User.query.filter_by(username=username).first()
        
        # 验证用户存在并且密码正确
        if user and check_password_hash(user.password_hash, password):
            # 更新最后登录时间
            user.last_login_at = datetime.utcnow()
            db.session.commit()
            
            # 生成JWT令牌
            payload = {
                'user_id': user.id,
                'username': user.username,
                'is_admin': user.is_admin,
                'exp': datetime.utcnow() + timedelta(hours=24)  # 令牌有效期24小时
            }
            token = pyjwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
            
            return jsonify({
                'message': '登录成功',
                'token': token,
                'user': user.to_dict()
            }), 200
        else:
            return jsonify({"error": "用户名或密码错误"}), 401 